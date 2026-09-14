"""The sentence in a citing paper that names the dataset.

Given the paper's text and the dataset's DataCite record, find every sentence
that points at this dataset and say how it points. Kinds, strongest first:

    doi          the 10.6073/pasta/... string itself
    package_id   scope.identifier, with or without a revision, dots or slashes
    title        the dataset title, normalised, inside a sentence of the body
    author_year  an in-text marker like (Rivest 2014) or Rivest et al., 2014,
                 from the dataset's first personal creator and its year.
                 Weak: the same author-year can point at a paper
    generic      a sentence naming EDI, the LTER data portal or lternet.edu
                 without identifying which dataset. Weakest: when a paper
                 cites several EDI datasets this cannot say which

Nothing here reads the search index. The ground truth must not know what
the system being tested would find.

Sentence splitting is a regex. It is wrong on "Fig. 3" and "et al." and
that is acceptable for a probe whose output a person reads; offsets are into
the saved `text.txt`, so a wrong boundary is visible and reproducible.
"""

from __future__ import annotations

import re

_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\[\"“])")
_GENERIC = re.compile(
    r"Environmental Data Initiative|\bEDI\b|LTER (?:Network )?Data Portal|"
    r"lternet\.edu|edirepository\.org|portal\.edirepository", re.I)


def sentences(text: str) -> list[tuple[int, int, str]]:
    """(start, end, sentence) over the whole text, paragraph-aware."""
    out = []
    pos = 0
    for para in text.split("\n"):
        start = pos
        for s in _SENT.split(para):
            if s.strip():
                i = text.index(s, start)
                out.append((i, i + len(s), s.strip()))
                start = i + len(s)
        pos += len(para) + 1
    return out


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _surname(creator: str) -> str | None:
    """'Rivest, Emily' -> 'Rivest'; organisations ('Moorea Coral Reef LTER') -> None."""
    if "," in creator:
        return creator.split(",")[0].strip()
    parts = creator.split()
    if 2 <= len(parts) <= 3 and not any(p.isupper() and len(p) > 1 for p in parts):
        return parts[-1]
    return None


def patterns(ds: dict) -> list[tuple[str, re.Pattern]]:
    """Regexes that identify this dataset, strongest first."""
    # pypdf sometimes drops a space into a URL at a line break ("doi.o rg/10.");
    # allow one optional space between any two characters of the DOI
    loose = r"\s?".join(re.escape(c) for c in ds["doi"])
    out = [("doi", re.compile(loose, re.I))]
    if ds.get("scope") and ds.get("identifier"):
        sc, ident = re.escape(ds["scope"]), ds["identifier"]
        out.append(("package_id",
                    re.compile(rf"\b{sc}[./]{ident}(?:[./]\d+)?\b", re.I)))
    title = _norm(ds.get("title") or "")
    # Drop a leading site prefix like "MCR LTER: Coral Reef:" -- papers cite
    # the descriptive part. Keep titles with at least four content words.
    core = title.split(":")[-1].strip() if ":" in (ds.get("title") or "") else title
    core = _norm(core)
    if len(core.split()) >= 4:
        out.append(("title", re.compile(r"\s+".join(map(re.escape, core.split())), re.I)))
    for c in ds.get("creators") or []:
        s = _surname(c)
        if s and ds.get("year"):
            out.append(("author_year", re.compile(
                rf"\b{re.escape(s)}\b[^.;()]{{0,40}}?\b{ds['year']}[a-z]?\b")))
            break
    return out


def find(text: str, ds: dict, max_per_kind: int = 3,
         reflist_start: int = -1) -> list[dict]:
    """Sentences naming the dataset, strongest kind first, deduplicated.

    Each hit says whether it sits in the reference list. A bibliography entry
    proves the paper cites the dataset but is not a query sentence; the query
    is the body sentence that carries the in-text marker for that entry, and
    resolving marker to entry is M3's job, not this probe's.
    """
    sents = sentences(text)
    ntext = text  # patterns are case-insensitive; title matches on the raw text
    # the title pattern needs punctuation-free matching: build a map from a
    # normalised copy back to raw offsets
    norm_chars, back = [], []
    for i, ch in enumerate(text):
        c = ch.lower() if ch.isalnum() else " "
        if c == " " and norm_chars and norm_chars[-1] == " ":
            continue
        norm_chars.append(c)
        back.append(i)
    ntitle = "".join(norm_chars)

    hits: list[dict] = []
    seen: set[tuple[int, int]] = set()

    def add(kind, i):
        for s0, s1, s in sents:
            if s0 <= i < s1:
                if (s0, s1) in seen:
                    return
                seen.add((s0, s1))
                hits.append({"kind": kind, "char_start": s0, "char_end": s1,
                             "in_reference_list": reflist_start >= 0 and s0 >= reflist_start,
                             "sentence": s})
                return

    for kind, rx in patterns(ds):
        n = 0
        if kind == "title":
            for m in rx.finditer(ntitle):
                add(kind, back[m.start()])
                n += 1
                if n >= max_per_kind:
                    break
        else:
            for m in rx.finditer(ntext):
                add(kind, m.start())
                n += 1
                if n >= max_per_kind:
                    break
    if not hits:
        for m in _GENERIC.finditer(text):
            add("generic", m.start())
            if len(hits) >= max_per_kind:
                break
    return hits

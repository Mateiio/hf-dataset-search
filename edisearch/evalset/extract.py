"""The sentence in a citing paper that names the dataset.

Given the paper's text and the dataset's DataCite record, find every sentence
that points at this dataset and say how it points. Kinds, strongest first:

    doi          the 10.6073/pasta/... string itself
    package_id   scope.identifier, with or without a revision, dots or slashes
    title        the dataset title, normalised
    marker       a body sentence carrying the in-text marker of a reference
                 list entry that names the dataset: `[37]`, `(37)`, `(12-15)`
                 for numbered styles, `(Campbell and Green, 2019)` or
                 `Campbell et al. (2019)` for author-year styles. This is how
                 most citations actually appear: the DOI sits in the
                 bibliography and the body says "(37)"
    author_year  the same author-year pattern found without going through a
                 reference entry, from the dataset's first personal creator
                 and year. Weak: the same author and year can name a paper
    generic      a sentence naming EDI, the LTER data portal or lternet.edu
                 without identifying which dataset. Weakest: when a paper
                 cites several EDI datasets this cannot say which

Every hit records whether it sits in the reference list. A bibliography entry
proves the paper cites the dataset but is not a query; the query is a body
sentence. `find` therefore does two passes: direct hits anywhere, then, for
each direct hit that landed in the reference list, the entry's label and the
body sentences that carry it.

Nothing here reads the search index. The ground truth must not know what
the system being tested would find.

Sentence splitting is a regex. It is wrong on "Fig. 3" and "et al." and
that is acceptable for output a person reads; offsets are into the saved
`text.txt`, so a wrong boundary is visible and reproducible.
"""

from __future__ import annotations

import re

_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\[\"“])")
_GENERIC = re.compile(
    r"Environmental Data Initiative|\bEDI\b|LTER (?:Network )?Data Portal|"
    r"lternet\.edu|edirepository\.org|portal\.edirepository", re.I)

# How a reference-list entry starts, in the two families of style. A wrapped
# line inside an entry also starts at column 0 in PDF text, so an author-year
# entry has to look like "Surname AB," or "Surname, A." (surname then
# initials), optionally after a bullet; a capitalised word followed by
# ordinary words ("Data Initiative.") is not an entry start.
_NUM_ENTRY = re.compile(r"(?m)^\s*\[?(\d{1,3})[\].)]?\s+(?=[A-Z])")
_AUTHOR_ENTRY = re.compile(
    r"(?m)^[\s•·*\-–]*([A-Z][A-Za-z'’\-]+(?: [A-Z][A-Za-z'’\-]+)?)"
    r",?\s+(?:[A-Z]{1,3}[.,\s]|[A-Z]\.|[A-Z][a-z]+ [A-Z]\.)")
_YEAR = re.compile(r"\b((?:19|20)\d{2})([a-z]?)\b")

KIND_RANK = {"doi": 0, "package_id": 1, "title": 2, "marker": 3,
             "author_year": 4, "generic": 5}

# A data-availability section lists datasets as full citations, which is
# bibliography by another name: a hit there proves the citation but is not a
# query sentence. Such a section runs from its heading to the next heading
# or the reference list, capped, so a paper's entire discussion is never
# swallowed by a misread.
_DA_HEADING = re.compile(
    r"(?im)^[^\n]{0,20}\b(Data (?:and code |and software )?availability(?: statement)?|"
    r"Code and data availability|Data accessibility(?: statement)?|"
    r"Availability of data(?: and materials)?)\b[^\n]{0,30}$")
_DA_MAX = 20000
_BACK_MATTER = re.compile(
    r"(?im)^[^\n]{0,6}(Author contributions?|Competing interests?|Acknowledge?ments?|"
    r"Financial support|Review statement|Supplement|Code availability|Sample availability|"
    r"Video supplement|Conflicts? of interest|Funding|Disclaimer|Appendix [A-Z]?)\b[^\n]{0,30}$")


def bibliography_spans(text: str, reflist_start: int) -> list[tuple[int, int]]:
    """Character spans that are bibliography-like: the reference list plus any
    data-availability section."""
    spans = []
    if reflist_start >= 0:
        spans.append((reflist_start, len(text)))
    for m in _DA_HEADING.finditer(text):
        start = m.start()
        end = min(len(text), start + _DA_MAX)
        for rx in (_HEADING_LINE_ANY, _BACK_MATTER):
            nxt = rx.search(text, m.end() + 1)
            if nxt and nxt.start() < end:
                end = nxt.start()
        if reflist_start >= 0 and start < reflist_start < end:
            end = reflist_start
        spans.append((start, end))
    return spans


# A numbered section heading: one or two digits per level, so a wrapped line
# that starts with a year ("2008 Anaktuvuk River fire ...") is not one.
_HEADING_LINE_ANY = re.compile(r"(?m)^\d{1,2}(?:\.\d{1,2})*\s+[A-Z][^\n.!?]{0,70}$")


def in_spans(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(a <= pos < b for a, b in spans)


# A line that is a heading or a running header rather than prose: short, no
# sentence punctuation, optionally numbered ("2.1 Field site and data",
# "REFERENCES", "Allen: Seasonal partitioning of precipitation"). Such a line
# is its own segment so it never glues onto the sentence after it.
_HEADING_LINE = re.compile(
    r"^(?:\d+(?:\.\d+)*\s+)?[A-Z][^\n.!?]{0,70}$")


def sentences(text: str) -> list[tuple[int, int, str]]:
    """(start, end, sentence) over the whole text.

    Boundaries come from punctuation, and from heading-like lines. PDF text
    breaks every line, so an ordinary newline is a space here, not a
    boundary; JATS text has one paragraph per line and a paragraph's last
    sentence has its full stop, so the two rarely merge. Offsets are into the
    original text.
    """
    out = []
    block_start, block_lines = 0, []

    def flush(end):
        if not block_lines:
            return
        flat = "\n".join(block_lines).replace("\n", " ")
        start = 0
        for s in _SENT.split(flat):
            if s.strip():
                i = flat.index(s, start)
                out.append((block_start + i, block_start + i + len(s), " ".join(s.split())))
                start = i + len(s)

    pos = 0
    for line in text.split("\n"):
        if _HEADING_LINE.match(line) and len(line.split()) <= 10:
            flush(pos)
            block_lines = []
            if line.strip():
                out.append((pos, pos + len(line), line.strip()))
            block_start = pos + len(line) + 1
        else:
            if not block_lines:
                block_start = pos
            block_lines.append(line)
        pos += len(line) + 1
    flush(pos)
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
    """Regexes that identify this dataset directly, strongest first."""
    # pypdf sometimes drops a space into a URL at a line break ("doi.o rg/10.");
    # allow one optional space between any two characters of the DOI
    loose = r"\s?".join(re.escape(c) for c in ds["doi"])
    out = [("doi", re.compile(loose, re.I))]
    if ds.get("scope") and ds.get("identifier"):
        sc, ident = re.escape(ds["scope"]), ds["identifier"]
        out.append(("package_id",
                    re.compile(rf"\b{sc}[./]{ident}(?:[./]\d+)?\b", re.I)))
    title = ds.get("title") or ""
    # Drop a leading site prefix like "MCR LTER: Coral Reef:" -- papers cite
    # the descriptive part. Keep titles with at least four content words.
    core = _norm(title.split(":")[-1] if ":" in title else title)
    if len(core.split()) >= 4:
        out.append(("title", re.compile(r"\s+".join(map(re.escape, core.split())), re.I)))
    for c in ds.get("creators") or []:
        s = _surname(c)
        if s and ds.get("year"):
            out.append(("author_year", _author_year_pattern(s, str(ds["year"]))))
            break
    return out


def _author_year_pattern(surname: str, year: str) -> re.Pattern:
    """(Surname 2019), (Surname et al., 2019), Surname and X (2019), Surname et al. 2019a."""
    s = re.escape(surname)
    return re.compile(rf"\b{s}\b[^.;()\n]{{0,40}}?\(?\b{year}[a-z]?\b")


# ------------------------------------------------------- reference entries

def entry_label(text: str, span_start: int, hit_pos: int) -> dict | None:
    """The label of the bibliography entry containing `hit_pos`.

    `span_start` is where the reference list or data-availability section
    begins. Looks back from the hit to the nearest entry start. Numbered styles give
    {"style": "number", "n": 37}; author-year styles give
    {"style": "author", "surname": "Campbell", "year": "2019"}.
    """
    if span_start < 0 or hit_pos < span_start:
        return None
    window = text[span_start:hit_pos]
    nums = list(_NUM_ENTRY.finditer(window))
    auths = list(_AUTHOR_ENTRY.finditer(window))
    last_num = nums[-1] if nums else None
    last_auth = auths[-1] if auths else None
    if last_num and (not last_auth or last_num.start() >= last_auth.start()):
        entry = text[span_start + last_num.start(): hit_pos + 200]
        return {"style": "number", "n": int(last_num.group(1)),
                "entry": entry.split("\n")[0][:200]}
    if last_auth:
        entry_start = span_start + last_auth.start()
        entry = text[entry_start: hit_pos + 200].split("\n")[0]
        ys = [a + b for a, b in _YEAR.findall(entry)]
        # APA puts the year after the authors, Copernicus and many others put
        # it last; a dataset title in between often carries its own years.
        # Keep both ends and let the marker search try each.
        years = list(dict.fromkeys([ys[0], ys[-1]])) if ys else []
        return {"style": "author", "surname": last_auth.group(1).split()[-1],
                "year": years[0] if years else None, "years": years,
                "entry": entry[:200]}
    return None


def _number_marker_pattern(n: int) -> re.Pattern:
    """`[37]`, `[12,37]`, `[35–38]`, `(37)`, `( 37 )`, `(12, 37)`."""
    return re.compile(
        r"[\[(]\s*(?:\d{1,3}\s*[,;]\s*)*"
        rf"(?:{n}|(?:\d{{1,3}})\s*[–\-]\s*(?:\d{{1,3}}))"
        r"(?:\s*[,;]\s*\d{1,3})*\s*[\])]")


def _in_range(match_text: str, n: int) -> bool:
    """True if a bracket group like [35–38] or (12, 37) covers n."""
    for a, b in re.findall(r"(\d{1,3})\s*[–\-]\s*(\d{1,3})", match_text):
        if int(a) <= n <= int(b):
            return True
    return bool(re.search(rf"(?<!\d){n}(?!\d)", match_text))


def marker_pattern(label: dict) -> re.Pattern | None:
    if label["style"] == "number":
        return _number_marker_pattern(label["n"])
    years = label.get("years") or ([label["year"]] if label.get("year") else [])
    if label["style"] == "author" and years:
        alt = "|".join(re.escape(y.rstrip("abc")) for y in years)
        s = re.escape(label["surname"])
        return re.compile(rf"\b{s}\b[^.;()\n]{{0,40}}?\(?\b(?:{alt})[a-z]?\b")
    return None


# --------------------------------------------------------------------- find

def find(text: str, ds: dict, max_per_kind: int = 3,
         reflist_start: int = -1) -> list[dict]:
    """Sentences naming the dataset, strongest kind first, deduplicated."""
    sents = sentences(text)
    biblio = bibliography_spans(text, reflist_start)
    norm_chars, back = [], []
    for i, ch in enumerate(text):
        c = ch.lower() if ch.isalnum() else " "
        if c == " " and norm_chars and norm_chars[-1] == " ":
            continue
        norm_chars.append(c)
        back.append(i)
    ntext = "".join(norm_chars)

    hits: list[dict] = []
    seen: set[tuple[int, int]] = set()

    def add(kind, i, extra=None):
        for j, (s0, s1, s) in enumerate(sents):
            if s0 <= i < s1:
                if (s0, s1) in seen:
                    return None
                seen.add((s0, s1))
                # A data-availability line often splits as "Title of data
                # (Author 2020):" / "https://doi.org/..."; a hit that is
                # mostly a URL or very short takes the preceding sentence
                # with it, so the query carries the words and not just the link.
                if j and (len(s) < 80 or re.match(r"^(https?://|at |doi:|URL)", s)):
                    p0, _, ps = sents[j - 1]
                    if s0 - p0 < 400:
                        s0, s = p0, (ps + " " + s).strip()
                h = {"kind": kind, "char_start": s0, "char_end": s1,
                     "in_reference_list": in_spans(s0, biblio),
                     "sentence": s}
                if extra:
                    h.update(extra)
                hits.append(h)
                return h
        return None

    # pass 1: direct mentions anywhere
    direct_positions = []
    for kind, rx in patterns(ds):
        n = 0
        if kind == "title":
            for m in rx.finditer(ntext):
                pos = back[m.start()]
                direct_positions.append(pos)
                add(kind, pos)
                n += 1
                if n >= max_per_kind:
                    break
        else:
            for m in rx.finditer(text):
                direct_positions.append(m.start())
                add(kind, m.start())
                n += 1
                if n >= max_per_kind:
                    break

    # pass 2: for hits in the reference list, resolve the entry's marker in
    # the body. One label per distinct entry; markers ranked by position.
    labels: dict[str, dict] = {}
    for pos in direct_positions:
        span = next(((a, b) for a, b in biblio if a <= pos < b), None)
        lab = entry_label(text, span[0], pos) if span else None
        if lab:
            key = f"{lab['style']}:{lab.get('n') or lab.get('surname')}:{lab.get('year')}"
            labels.setdefault(key, lab)
    body_end = reflist_start if reflist_start >= 0 else len(text)
    da_spans = [(a, b) for a, b in biblio if a != reflist_start]
    for lab in labels.values():
        rx = marker_pattern(lab)
        if not rx:
            continue
        n = 0
        for m in rx.finditer(text, 0, body_end):
            if in_spans(m.start(), da_spans):
                continue
            if lab["style"] == "number" and not _in_range(m.group(0), lab["n"]):
                continue
            if add("marker", m.start(), {"ref_label": lab["n"] if lab["style"] == "number"
                                          else f"{lab['surname']} {lab['year']}",
                                          "ref_entry": lab["entry"]}):
                n += 1
            if n >= max_per_kind:
                break

    if not hits:
        for m in _GENERIC.finditer(text):
            add("generic", m.start())
            if len(hits) >= max_per_kind:
                break

    hits.sort(key=lambda h: (h["in_reference_list"], KIND_RANK[h["kind"]], h["char_start"]))
    return hits


def best_query(hits: list[dict]) -> dict | None:
    """The one body sentence to use as a query, or None if there is none."""
    body = [h for h in hits if not h["in_reference_list"] and h["kind"] != "generic"]
    return body[0] if body else None

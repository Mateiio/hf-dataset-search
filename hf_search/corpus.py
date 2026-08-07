"""Load the corpus and build the text each engine indexes.

`records.json` ships with the repo, so nothing here needs the network or a
model. `harvest.py` regenerates it from the archive if you want to verify it or
pick up newer datasets.
"""

from __future__ import annotations

import re

from hf_search import eml
from hf_search.paths import EML_CACHE, RECORDS

_CACHE: list | None = None


def load(refresh: bool = False, verbose: bool = False) -> list:
    """All 458 parsed datasets. Cached in memory for the process."""
    global _CACHE
    if _CACHE is not None and not refresh:
        return _CACHE
    if RECORDS.exists() and not refresh:
        _CACHE = eml.read_json(RECORDS)
    elif EML_CACHE.exists():
        _CACHE = eml.parse_dir(EML_CACHE, verbose=verbose)
        eml.write_json(_CACHE, RECORDS)
    else:
        raise SystemExit(
            f"No corpus found. Expected {RECORDS} (ships with the repo) or raw "
            f"EML in {EML_CACHE}.\nRun: python -m hf_search.harvest")
    if verbose:
        print(f"loaded {len(_CACHE)} datasets")
    return _CACHE


# A dataset's title is a far stronger relevance signal than one of its 344
# attribute names, but flat TF-IDF treats them alike -- which is why an
# unweighted index ranked hf206 ("Microclimate at ... Towers") seventh for
# "microclimate hemlock tower". Repeating high-value fields is the standard way
# to weight fields inside a single TF-IDF space.
FIELD_WEIGHTS = {"title": 4, "keywords": 3, "abstract": 2, "table": 1}


def lexical_doc(rec) -> str:
    """Text for the TF-IDF index.

    Attribute DEFINITIONS are deliberately excluded, and this was tested both
    ways: folding them in dropped recall@5 from 0.90 to 0.80 and pushed hf206
    from rank 1 to rank 9. Its 344 definitions span soil moisture, wind, air and
    soil temperature, so adding them dilutes any one signal and TF-IDF's length
    normalisation then penalises the document for being long.

    Definitions are indexed separately at attribute granularity by
    `attribute_docs()`; a match there promotes the parent dataset.
    """
    w = FIELD_WEIGHTS
    parts = [(rec.title + " ") * w["title"],
             (" ".join(rec.keywords) + " ") * w["keywords"],
             (rec.abstract + " ") * w["abstract"]]
    for t in rec.tables:
        parts.append((t.description + " ") * w["table"])
        # Filenames carry signal found nowhere else: hf069 is titled "Biomass
        # Inventories" and never says LAI or litterfall, but its tables are
        # hf069-01-lai-plot.csv and hf069-05-litter.csv.
        parts.append(re.sub(r"[-_.]", " ", t.filename) + " ")
        parts.append(" ".join(a.name for a in t.attributes))
    return "\n".join(p for p in parts if p.strip())


def attribute_docs(rec) -> list[tuple[str, str]]:
    """One short document per DISTINCT attribute definition.

    Deduplicated: hf206's six understory PAR sensors share one sentence, and six
    copies would inflate its weight without adding information.
    """
    out, seen = [], set()
    for t in rec.tables:
        for a in t.attributes:
            d = (a.definition or "").strip()
            if not d or d.lower() in seen:
                continue
            seen.add(d.lower())
            unit = f" ({a.unit})" if a.unit else ""
            out.append((f"{t.filename}::{a.name}", f"{a.name}{unit}: {d}"))
    return out


def semantic_doc(rec, limit: int = 20000) -> str:
    """Text that gets embedded.

    Includes column definitions, unlike `lexical_doc`. Tested: abstract-only
    scored 0.14 on paraphrase queries against 0.43 with definitions included --
    the columns carry real signal for a dense encoder even though they hurt
    TF-IDF. The two indexes want different text, which is why they build it
    separately instead of sharing one function.
    """
    parts = [rec.title, ", ".join(rec.keywords), rec.abstract]
    seen, defs = set(), []
    for t in rec.tables:
        for a in t.attributes:
            d = (a.definition or "").strip()
            if d and d.lower() not in seen:
                seen.add(d.lower())
                defs.append(d)
    parts.append(" ".join(defs))
    return "\n".join(p for p in parts if p)[:limit]


def stats(records=None) -> dict:
    recs = records or load()
    return {
        "datasets": len(recs),
        "tables": sum(len(r.tables) for r in recs),
        "attributes": sum(len(t.attributes) for r in recs for t in r.tables),
    }


if __name__ == "__main__":
    for k, v in stats().items():
        print(f"{k:14s} {v:>8,}")

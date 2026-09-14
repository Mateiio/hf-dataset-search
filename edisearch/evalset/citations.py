"""Which papers cite which EDI packages, from DataCite.

Two link sets exist and they are not the same thing:

- `references`, source `crossref`: the publisher deposited the dataset DOI in
  the paper's reference list. Paper is subj, dataset is obj. 2,371 on
  2026-09-13, plus 462 more from `datacite-related`
- `is-cited-by`, source `datacite-crossref` and `datacite-url`: EDI recorded
  the citing paper in the dataset's own DataCite metadata. Dataset is subj,
  paper is obj. 4,860 on 2026-09-13

Both are read; a pair is (dataset DOI, citing DOI) whichever way it was
recorded, and the source is kept because yield may differ between them.

EDI DOIs are all under prefix 10.6073. One DOI per revision, so a series can
carry several; the DataCite record's `url` points at the portal with a
`packageid=`, which gives scope, identifier and revision without a harvest.
"""

from __future__ import annotations

import json
import re
import urllib.parse
from typing import Iterator

from edisearch import net

API = "https://api.datacite.org"
PREFIX = "10.6073"

RELATIONS = (
    ("references", "paper->dataset"),
    ("is-cited-by", "dataset->paper"),
)

_PKG = re.compile(r"packageid=([A-Za-z][A-Za-z0-9_-]*)\.(\d+)\.(\d+)")


def _json(url: str) -> dict:
    code, body, _ = net.get(url)
    if code != 200:
        raise RuntimeError(f"datacite HTTP {code}: {url}")
    return json.loads(body)


def _doi(s: str) -> str:
    return s.strip().lower().replace("https://doi.org/", "").replace("doi:", "")


def iter_events(relation: str, page_size: int = 1000) -> Iterator[dict]:
    """Every event of one relation type for EDI's prefix, cursor-paged."""
    url = (f"{API}/events?prefix={PREFIX}&relation-type-id={relation}"
           f"&page%5Bsize%5D={page_size}&page%5Bcursor%5D=1")
    while url:
        page = _json(url)
        yield from page["data"]
        url = (page.get("links") or {}).get("next")


def links() -> list[dict]:
    """Deduplicated (dataset_doi, citing_doi) pairs from both link sets."""
    seen: dict[tuple[str, str], dict] = {}
    for relation, direction in RELATIONS:
        for ev in iter_events(relation):
            a = ev["attributes"]
            subj, obj = _doi(a["subj-id"]), _doi(a["obj-id"])
            dataset, paper = (obj, subj) if direction == "paper->dataset" else (subj, obj)
            if not dataset.startswith(PREFIX + "/") or paper.startswith(PREFIX + "/"):
                continue
            key = (dataset, paper)
            rec = seen.setdefault(key, {
                "dataset_doi": dataset, "citing_doi": paper,
                "sources": [], "occurred": a.get("occurred-at", "")[:10]})
            src = f"{relation}/{a.get('source-id')}"
            if src not in rec["sources"]:
                rec["sources"].append(src)
    return sorted(seen.values(), key=lambda r: (r["dataset_doi"], r["citing_doi"]))


def dataset(doi: str) -> dict:
    """Title, package id, creators, year and abstract for one EDI DOI."""
    a = _json(f"{API}/dois/{urllib.parse.quote(_doi(doi), safe='')}")["data"]["attributes"]
    m = _PKG.search(a.get("url") or "")
    return {
        "doi": _doi(doi),
        "title": (a.get("titles") or [{}])[0].get("title", ""),
        "package_id": ".".join(m.groups()) if m else None,
        "scope": m.group(1).lower() if m else None,
        "identifier": int(m.group(2)) if m else None,
        "revision": int(m.group(3)) if m else None,
        "creators": [c.get("name", "") for c in a.get("creators") or []],
        "year": a.get("publicationYear"),
        "abstract": " ".join(d.get("description", "")
                             for d in a.get("descriptions") or []),
        "citation_count": a.get("citationCount"),
    }

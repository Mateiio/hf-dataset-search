"""The EDI corpus as the engines see it, and where its vectors live.

`data/records.jsonl` (M1) holds one JSON object per package with the reused
parser's fields plus identity. Read back through `eml.Record.from_dict`, the
rows are the same `Record` objects `hf_search`'s engines were written for, so
`LexicalIndex`, `SemanticIndex` and `HybridIndex` index them unchanged.

Vectors sit beside the Harvard Forest ones under different names, so the
original demo keeps working from the same clone:

    data/embeddings.npy          458 Harvard Forest archive datasets (v1-hf-only)
    data/edi_embeddings.npy      the EDI corpus, however many scopes are harvested

`get_engine` is the one place that knows how to build each engine over the
EDI corpus, mirroring `hf_search.hybrid.get_engine`. Two lexical engines:
`lexical` is the repo's field-weighted TF-IDF with its column-definition
second index, unchanged; `bm25` is the plain baseline the published
dataset-search work uses. `hybrid` fuses TF-IDF with dense; `hybrid-bm25`
fuses BM25 with dense.
"""

from __future__ import annotations

import json

import numpy as np

from hf_search import eml
from hf_search.hybrid import HybridIndex
from hf_search.lexical import LexicalIndex
from hf_search.semantic import SemanticIndex
from edisearch.paths import DATA, RECORDS

EMBEDDINGS = DATA / "edi_embeddings.npy"
EMBEDDING_IDS = DATA / "edi_embedding_ids.json"

_CACHE: list | None = None


def load_records(scope: str | None = None, refresh: bool = False) -> list[eml.Record]:
    """Every harvested package as an `eml.Record`, optionally one scope."""
    global _CACHE
    if _CACHE is None or refresh:
        if not RECORDS.exists():
            raise SystemExit(f"No corpus at {RECORDS}. Run: "
                             "python -m edisearch.acquire.harvest knb-lter-hfr")
        rows = [json.loads(l) for l in RECORDS.read_text(encoding="utf-8").splitlines()]
        _CACHE = [eml.Record.from_dict(r) for r in rows]
        _CACHE_SCOPES.clear()
        _CACHE_SCOPES.update((r["package_id"], r["scope"]) for r in rows)
    if scope:
        return [r for r in _CACHE if _CACHE_SCOPES.get(r.id) == scope]
    return _CACHE


_CACHE_SCOPES: dict[str, str] = {}


def load_semantic(records: list[eml.Record]) -> SemanticIndex:
    if not EMBEDDINGS.exists():
        raise SystemExit(f"No EDI embeddings at {EMBEDDINGS}. Run: "
                         "python -m edisearch.index.semantic --build")
    V = np.load(EMBEDDINGS)
    ids = json.loads(EMBEDDING_IDS.read_text(encoding="utf-8"))
    want = {r.id for r in records}
    keep = [i for i, d in enumerate(ids) if d in want]
    if len(keep) != len(ids):
        V, ids = V[keep], [ids[i] for i in keep]
    return SemanticIndex(ids, V, records)


def get_engine(mode: str = "hybrid", records: list[eml.Record] | None = None,
               verbose: bool = False):
    from edisearch.index.lexical import BM25Index
    records = records if records is not None else load_records()
    if mode == "lexical":
        return LexicalIndex(records, verbose=verbose)
    if mode == "bm25":
        return BM25Index(records)
    if mode == "semantic":
        return load_semantic(records)
    if mode == "hybrid":
        return HybridIndex(semantic=load_semantic(records),
                           lexical=LexicalIndex(records, verbose=verbose),
                           records=records)
    if mode == "hybrid-bm25":
        return HybridIndex(semantic=load_semantic(records),
                           lexical=BM25Index(records), records=records)
    raise ValueError(f"unknown mode {mode!r}; use lexical, bm25, semantic, "
                     "hybrid or hybrid-bm25")


MODES = ("lexical", "bm25", "semantic", "hybrid", "hybrid-bm25")

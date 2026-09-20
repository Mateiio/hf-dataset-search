"""The EDI corpus as the engines see it, and where its vectors live.

`data/records.jsonl` (M1) holds one JSON object per package with the reused
parser's fields plus identity. Read back through `eml.Record.from_dict`, the
rows are the same `Record` objects `hf_search`'s engines were written for, so
`LexicalIndex`, `SemanticIndex` and `HybridIndex` index them unchanged.

Vectors sit beside the Harvard Forest ones under different names, so the
original demo keeps working from the same clone:

    data/embeddings.npy          458 Harvard Forest archive datasets (v1-hf-only)
    data/edi_embeddings.npy      the EDI corpus, however many scopes are harvested

What ships in the repository is the packed form, because GitHub refuses
files over 100 MB and the full corpus is 124 MB as plain JSON lines:

    data/records.jsonl.gz         the same records, gzipped (22 MB)
    data/edi_embeddings.f16.npy   the same vectors as float16 (21 MB; the
                                  largest rounding error is 1.2e-4 on unit
                                  vectors, far below anything a ranking sees)

The loaders prefer the working files and fall back to the packed ones, so a
fresh clone searches the whole of EDI with nothing but Ollama for the query
vector. `python -m edisearch.index.store --pack` regenerates the packed
files after a harvest or an embedding run.

`get_engine` is the one place that knows how to build each engine over the
EDI corpus, mirroring `hf_search.hybrid.get_engine`. Two lexical engines:
`lexical` is the repo's field-weighted TF-IDF with its column-definition
second index, unchanged; `bm25` is the plain baseline the published
dataset-search work uses. `hybrid` fuses TF-IDF with dense; `hybrid-bm25`
fuses BM25 with dense.
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys

import numpy as np

from hf_search import eml
from hf_search.hybrid import HybridIndex
from hf_search.lexical import LexicalIndex
from hf_search.semantic import SemanticIndex
from edisearch.paths import DATA, RECORDS

EMBEDDINGS = DATA / "edi_embeddings.npy"
EMBEDDINGS_PACKED = DATA / "edi_embeddings.f16.npy"
EMBEDDING_IDS = DATA / "edi_embedding_ids.json"
RECORDS_PACKED = DATA / "records.jsonl.gz"

_CACHE: list | None = None


def load_records(scope: str | None = None, refresh: bool = False) -> list[eml.Record]:
    """Every harvested package as an `eml.Record`, optionally one scope."""
    global _CACHE
    if _CACHE is None or refresh:
        if RECORDS.exists():
            text = RECORDS.read_text(encoding="utf-8")
        elif RECORDS_PACKED.exists():
            with gzip.open(RECORDS_PACKED, "rt", encoding="utf-8") as f:
                text = f.read()
        else:
            raise SystemExit(f"No corpus at {RECORDS} or {RECORDS_PACKED}. Run: "
                             "python -m edisearch.acquire.harvest knb-lter-hfr")
        rows = [json.loads(l) for l in text.splitlines() if l.strip()]
        _CACHE = [eml.Record.from_dict(r) for r in rows]
        _CACHE_SCOPES.clear()
        _CACHE_SCOPES.update((r["package_id"], r["scope"]) for r in rows)
    if scope:
        return [r for r in _CACHE if _CACHE_SCOPES.get(r.id) == scope]
    return _CACHE


_CACHE_SCOPES: dict[str, str] = {}


def load_semantic(records: list[eml.Record]) -> SemanticIndex:
    if EMBEDDINGS.exists():
        V = np.load(EMBEDDINGS)
    elif EMBEDDINGS_PACKED.exists():
        V = np.load(EMBEDDINGS_PACKED).astype("float32")
    else:
        raise SystemExit(f"No EDI embeddings at {EMBEDDINGS} or {EMBEDDINGS_PACKED}. Run: "
                         "python -m edisearch.index.semantic --build")
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


def pack() -> None:
    """Write the packed copies that ship in git from the working files."""
    with RECORDS.open("rb") as f, gzip.open(RECORDS_PACKED, "wb", compresslevel=9) as g:
        g.writelines(f)
    V = np.load(EMBEDDINGS)
    np.save(EMBEDDINGS_PACKED, V.astype("float16"))
    print(f"{RECORDS_PACKED.name}: {RECORDS_PACKED.stat().st_size / 2**20:.1f} MB; "
          f"{EMBEDDINGS_PACKED.name}: {EMBEDDINGS_PACKED.stat().st_size / 2**20:.1f} MB "
          f"({V.shape[0]:,} x {V.shape[1]})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="pack the corpus and vectors for git")
    ap.add_argument("--pack", action="store_true")
    if ap.parse_args().pack:
        pack()
    else:
        ap.print_help()
        sys.exit(1)

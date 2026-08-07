"""Semantic search: one bge-m3 vector per dataset, cosine similarity.

Build once (~40 s for 458 datasets), then every query is one embedding call plus
a matrix multiply -- effectively instant. The vectors ship with the repo, so
only the query needs a model at runtime.

This is what lexical search cannot do: on queries that share no vocabulary with
their target, TF-IDF scores 0.00 and this scores 0.43.

    python -m hf_search.semantic --build
    python -m hf_search.semantic "light below the canopy"
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass

import numpy as np

from hf_search import corpus, ollama
from hf_search.lexical import Hit
from hf_search.paths import EMBEDDING_IDS, EMBEDDINGS, EMBED_MODEL, ensure_data_dir


@dataclass
class _Store:
    ids: list
    V: np.ndarray


class SemanticIndex:
    """Dataset-level vectors only.

    Column-level vectors were tried and dropped. Promoting a dataset by its
    best-matching column lost to plain dataset vectors on six of seven
    paraphrase queries: column texts are short, so their cosine against a short
    query runs systematically high, and an unrelated dataset's stray column
    outranks the right dataset's. The trick that helps TF-IDF does not transfer
    to a dense encoder.
    """

    def __init__(self, ids, vectors, records=None):
        self.ids = list(ids)
        self.V = vectors                              # L2-normalised
        self.records = records if records is not None else corpus.load()
        self.by_id = {r.id: r for r in self.records}

    @classmethod
    def load(cls, records=None) -> "SemanticIndex":
        if not EMBEDDINGS.exists():
            raise SystemExit(
                f"No embeddings at {EMBEDDINGS}.\n"
                f"They ship with the repo; if missing, rebuild with:\n"
                f"  python -m hf_search.semantic --build")
        V = np.load(EMBEDDINGS)
        ids = json.loads(EMBEDDING_IDS.read_text(encoding="utf-8"))
        return cls(ids, V, records)

    def embed_query(self, text: str) -> np.ndarray:
        # Ollama returns HTTP 500 on some inputs (empty strings, occasional odd
        # encodings). A zero vector scores zero against everything, which is the
        # honest outcome for a query that could not be embedded -- better than
        # killing a benchmark run of 1,360 queries.
        text = (text or "").strip()[:6000]
        if not text:
            return np.zeros(self.V.shape[1], dtype="float32")
        try:
            q = np.asarray(ollama.embed([text])[0], dtype="float32")
        except ollama.OllamaUnavailable:
            raise
        except Exception:                             # noqa: BLE001
            return np.zeros(self.V.shape[1], dtype="float32")
        return q / (np.linalg.norm(q) or 1.0)

    def search(self, query: str, k: int = 20) -> list[Hit]:
        q = self.embed_query(query)
        sims = self.V @ q                             # cosine: both unit-norm
        out = []
        for i in np.argsort(-sims)[:k]:
            d = self.ids[i]
            out.append(Hit(d, float(sims[i]),
                           self.by_id[d].title if d in self.by_id else "",
                           "semantic similarity"))
        return out


def build(batch: int = 8, verbose: bool = True) -> SemanticIndex:
    """Embed every dataset. Needs Ollama; run once."""
    if not ollama.available():
        raise ollama.OllamaUnavailable()
    if not ollama.has_model():
        raise ollama.OllamaUnavailable(f"Model {EMBED_MODEL} is not pulled.")

    recs = corpus.load(verbose=verbose)
    ids, vecs = [], []
    t0 = time.perf_counter()
    for i in range(0, len(recs), batch):
        chunk = recs[i:i + batch]
        try:
            embs = ollama.embed([corpus.semantic_doc(r) for r in chunk])
        except Exception as e:                        # noqa: BLE001
            print(f"  batch at {i} failed ({str(e)[:60]}); one at a time")
            embs = []
            for r in chunk:
                try:
                    embs.append(ollama.embed([corpus.semantic_doc(r)])[0])
                except Exception:                     # noqa: BLE001
                    embs.append(None)
        for r, e in zip(chunk, embs):
            if e is None:
                print(f"  {r.id}: no embedding, skipped")
                continue
            ids.append(r.id)
            vecs.append(e)
        if verbose and (i // batch) % 10 == 0 and i:
            rate = i / max(time.perf_counter() - t0, 1e-9)
            print(f"  {i}/{len(recs)}  ({rate:.1f}/s, "
                  f"~{(len(recs) - i) / max(rate, 1e-9):.0f}s left)")

    V = np.asarray(vecs, dtype="float32")
    V /= (np.linalg.norm(V, axis=1, keepdims=True) + 1e-12)
    ensure_data_dir()
    np.save(EMBEDDINGS, V)
    EMBEDDING_IDS.write_text(json.dumps(ids), encoding="utf-8")
    if verbose:
        print(f"\nembedded {len(ids)} datasets into {V.shape[1]}-d vectors in "
              f"{time.perf_counter() - t0:.0f}s -> {EMBEDDINGS.name} "
              f"({EMBEDDINGS.stat().st_size / 1e6:.1f} MB)")
    return SemanticIndex(ids, V, recs)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="*")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("-k", type=int, default=10)
    a = ap.parse_args()

    if a.build:
        build()
        sys.exit(0)
    if not a.question:
        print(__doc__)
        sys.exit(1)
    idx = SemanticIndex.load()
    for h in idx.search(" ".join(a.question), k=a.k):
        print(f"  {h.score:.3f}  {h.dataset:8s} {h.title[:66]}")

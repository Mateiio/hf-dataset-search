"""BGE-M3 vectors for the EDI corpus, through the local Ollama, incrementally.

    python -m edisearch.index.semantic --build     embed what is missing
    python -m edisearch.index.semantic --rebuild   embed everything again

Same model, same document text (`hf_search.corpus.semantic_doc`), same
normalisation as the Harvard Forest build in `hf_search.semantic.build`, so
the EDI numbers are comparable with the original demo's. Two differences,
both deliberate:

- Incremental. Package ids carry the revision, so a re-harvested package with
  a new revision is a new id and gets embedded; ids no longer in the corpus
  are dropped. Nothing already embedded is sent to the model twice
- Throughput is measured and printed, because it is the one number M7 needs
  before deciding whether the whole contributed tier can be embedded on this
  machine
"""

from __future__ import annotations

import argparse
import json
import sys
import time

import numpy as np

from hf_search import corpus, ollama
from hf_search.semantic import SemanticIndex
from edisearch.index import store


def build(records=None, batch: int = 8, rebuild: bool = False,
          verbose: bool = True) -> SemanticIndex:
    if not ollama.available():
        raise ollama.OllamaUnavailable()
    if not ollama.has_model():
        raise ollama.OllamaUnavailable(f"Model {ollama.EMBED_MODEL} is not pulled.")
    recs = records if records is not None else store.load_records()

    have_ids, have_V = [], None
    if store.EMBEDDINGS.exists() and not rebuild:
        have_V = np.load(store.EMBEDDINGS)
        have_ids = json.loads(store.EMBEDDING_IDS.read_text(encoding="utf-8"))
    keep = {d: i for i, d in enumerate(have_ids)}
    todo = [r for r in recs if r.id not in keep]
    if verbose:
        print(f"{len(recs)} records; {len(recs) - len(todo)} already embedded; "
              f"{len(todo)} to embed")

    ids, vecs = [], []
    t0 = time.perf_counter()
    chars = 0
    for i in range(0, len(todo), batch):
        chunk = todo[i:i + batch]
        docs = [corpus.semantic_doc(r) for r in chunk]
        chars += sum(len(d) for d in docs)
        try:
            embs = ollama.embed(docs)
        except Exception as e:                        # noqa: BLE001
            print(f"  batch at {i} failed ({str(e)[:60]}); one at a time")
            embs = []
            for d in docs:
                try:
                    embs.append(ollama.embed([d])[0])
                except Exception:                     # noqa: BLE001
                    embs.append(None)
        for r, e in zip(chunk, embs):
            if e is None:
                print(f"  {r.id}: no embedding, skipped")
                continue
            ids.append(r.id)
            vecs.append(e)
        if verbose and i and (i // batch) % 10 == 0:
            rate = i / (time.perf_counter() - t0)
            print(f"  {i}/{len(todo)}  ({rate:.1f}/s, ~{(len(todo) - i) / rate:.0f}s left)")
    elapsed = time.perf_counter() - t0

    new_V = np.asarray(vecs, dtype="float32") if vecs else np.zeros((0, 0), "float32")
    if len(vecs):
        new_V /= (np.linalg.norm(new_V, axis=1, keepdims=True) + 1e-12)

    # merge: existing vectors still in the corpus, then the new ones
    want = {r.id for r in recs}
    kept = [i for i, d in enumerate(have_ids) if d in want]
    parts_ids = [have_ids[i] for i in kept] + ids
    parts_V = [have_V[kept]] if kept else []
    if len(vecs):
        parts_V.append(new_V)
    V = np.concatenate(parts_V) if parts_V else np.zeros((0, 1024), "float32")

    store.DATA.mkdir(parents=True, exist_ok=True)
    np.save(store.EMBEDDINGS, V)
    store.EMBEDDING_IDS.write_text(json.dumps(parts_ids), encoding="utf-8")
    if verbose:
        dim = V.shape[1] if V.size else "?"
        print(f"\n{len(parts_ids)} vectors of dimension {dim} -> {store.EMBEDDINGS.name} "
              f"({store.EMBEDDINGS.stat().st_size / 1e6:.1f} MB)")
        if todo:
            print(f"throughput: {len(ids)} packages, {chars:,} chars, {elapsed:.0f}s "
                  f"= {len(ids) / elapsed:.2f} packages/s, "
                  f"{chars / elapsed / 1000:.1f} kchars/s. "
                  f"At that rate 10,645 packages take {10645 / (len(ids) / elapsed) / 3600:.1f} h")
    return SemanticIndex(parts_ids, V, recs)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--batch", type=int, default=8)
    a = ap.parse_args(argv)
    if a.build or a.rebuild:
        build(batch=a.batch, rebuild=a.rebuild)
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())

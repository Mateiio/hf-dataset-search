"""Search the EDI corpus from the command line.

    python -m edisearch.search "spring leaf emergence"
    python -m edisearch.search "spring leaf emergence" --method bm25 --k 10
    python -m edisearch.search "understory light" --method hybrid --trace

Methods: lexical (the repo's field-weighted TF-IDF), bm25, semantic (BGE-M3
through Ollama), hybrid (TF-IDF + semantic, reciprocal rank fusion),
hybrid-bm25. Every engine answers the same call, `search(query, k)`, and
returns (package_id, score) best first, which is the interface the evaluation
harness scores.
"""

from __future__ import annotations

import argparse
import sys

from edisearch.index import store


def search(query: str, k: int = 10, method: str = "hybrid",
           records=None) -> list[tuple[str, float]]:
    """(package_id, score) ranked best first. The plan's retrieval interface."""
    eng = store.get_engine(method, records)
    return [(h.dataset, h.score) for h in eng.search(query, k=k)]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("query")
    ap.add_argument("--method", default="hybrid", choices=store.MODES)
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--scope", default=None, help="restrict to one scope")
    ap.add_argument("--trace", action="store_true", help="show what each stage did")
    a = ap.parse_args(argv)

    records = store.load_records(scope=a.scope)
    eng = store.get_engine(a.method, records)
    if a.trace:
        from hf_search.hybrid import _print_trace
        from hf_search.trace import Tracer
        tr = Tracer()
        hits = eng.search(a.query, k=a.k, trace=tr)
        _print_trace(tr.events)
        print()
    else:
        hits = eng.search(a.query, k=a.k)
    titles = {r.id: r.title for r in records}
    print(f"{a.method} over {len(records)} packages: {a.query!r}\n")
    for i, h in enumerate(hits, 1):
        print(f"{i:3d}. {h.dataset:26s} {h.score:8.4f}  {titles.get(h.dataset, h.title)[:70]}")
        if h.why:
            print(f"     {h.why[:90]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

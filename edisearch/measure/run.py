"""Run every retrieval method over every query set; write results.jsonl.

    python -m edisearch.measure.run
    python -m edisearch.measure.run --methods lexical bm25 semantic hybrid

Reads `data/queries.jsonl` and `data/qrels.jsonl` (every origin: citation,
generated, human), scores each query with each method over the whole
harvested corpus, and writes one line per (query, method) to
`data/results.jsonl` in the plan's interface:

    {"query_id", "method", "ranked_package_ids", "overlap", "rank", "origin"}

`overlap` is the pinned measure in `overlap.py`, computed between the query
and its relevant package (the maximum over relevant packages when there are
several). Nothing here writes to the query set: the evaluation reads the
ground truth, never the other way round.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict

from edisearch.index import store
from edisearch.measure import metrics, overlap
from edisearch.paths import DATA

QUERIES = DATA / "queries.jsonl"
QRELS = DATA / "qrels.jsonl"
RESULTS = DATA / "results.jsonl"
DEPTH = 100


def load_ground_truth() -> tuple[list[dict], dict[str, set[str]], dict[str, set[str]]]:
    queries = [json.loads(l) for l in QUERIES.read_text(encoding="utf-8").splitlines()]
    rel_series, rel_pkgs = defaultdict(set), defaultdict(set)
    for l in QRELS.read_text(encoding="utf-8").splitlines():
        q = json.loads(l)
        if q.get("relevance", 1) > 0:
            rel_series[q["query_id"]].add(q["series_id"])
            rel_pkgs[q["query_id"]].add(q["package_id"])
    return queries, rel_series, rel_pkgs


def run(methods=store.MODES, verbose: bool = True) -> list[dict]:
    queries, rel_series, rel_pkgs = load_ground_truth()
    if not queries:
        raise SystemExit("no queries in data/queries.jsonl; run edisearch.evalset.build first")
    records = store.load_records()
    by_id = {r.id: r for r in records}
    series_of = {r.id: r.id.rsplit(".", 1)[0] for r in records}
    by_series = defaultdict(list)
    for r in records:
        by_series[series_of[r.id]].append(r)
    if verbose:
        print(f"{len(queries)} queries, {len(records)} packages, methods: {', '.join(methods)}")

    # overlap against the relevant package: the cited revision if it is in
    # the corpus, else the current revision of the same series
    def target_records(qid):
        out = []
        for pid in rel_pkgs[qid]:
            if pid in by_id:
                out.append(by_id[pid])
            else:
                out.extend(by_series.get(pid.rsplit(".", 1)[0], []))
        return out

    ov = {}
    for q in queries:
        targets = target_records(q["query_id"])
        ov[q["query_id"]] = max((overlap.overlap(q["text"], r) for r in targets), default=None)
        if not targets and verbose:
            print(f"  {q['query_id']}: relevant series not in corpus "
                  f"({', '.join(rel_pkgs[q['query_id']])})")

    rows = []
    for m in methods:
        t0 = time.perf_counter()
        eng = store.get_engine(m, records)
        for q in queries:
            ranked = [h.dataset for h in eng.search(q["text"], k=DEPTH)]
            rank = metrics.first_rank(ranked, rel_series[q["query_id"]], series_of)
            rows.append({"query_id": q["query_id"], "method": m, "origin": q.get("origin"),
                         "ranked_package_ids": ranked, "overlap": ov[q["query_id"]],
                         "rank": rank,
                         "ndcg10": metrics.ndcg_at(ranked, rel_series[q["query_id"]], series_of)})
        if verbose:
            hits = sum(1 for r in rows if r["method"] == m and r["rank"] and r["rank"] <= 5)
            print(f"  {m:12s} recall@5 {hits}/{len(queries)}  ({time.perf_counter() - t0:.0f}s)")
    RESULTS.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    if verbose:
        print(f"wrote {RESULTS} ({len(rows)} rows)")
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--methods", nargs="*", default=list(store.MODES))
    a = ap.parse_args(argv)
    run(a.methods)
    return 0


if __name__ == "__main__":
    sys.exit(main())

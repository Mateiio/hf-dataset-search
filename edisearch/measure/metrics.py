"""Series-aware retrieval metrics.

A query built from one revision or one period of a long-running dataset is
not a miss when a sibling is returned, so relevance is judged on series
ids, not package ids: a ranked package counts as a hit if its series is in
the query's relevant set. Series ids are `scope.identifier` (M5's trivial
grouping; the title heuristic for one series under several identifiers is
layered on top when it exists).

All metrics take the ranked list of package ids and a map from package id
to series id. `rank` is 1-based, None when nothing relevant is in the list.
"""

from __future__ import annotations

import math


def first_rank(ranked: list[str], relevant_series: set[str],
               series_of: dict[str, str]) -> int | None:
    for i, pid in enumerate(ranked, 1):
        if series_of.get(pid, pid.rsplit(".", 1)[0]) in relevant_series:
            return i
    return None


def reciprocal_rank(rank: int | None) -> float:
    return 1.0 / rank if rank else 0.0


def recall_at(rank: int | None, k: int) -> float:
    return 1.0 if rank and rank <= k else 0.0


def ndcg_at(ranked: list[str], relevant_series: set[str],
            series_of: dict[str, str], k: int = 10) -> float:
    """Binary-gain nDCG@k with one relevant series counted once."""
    seen, dcg = set(), 0.0
    for i, pid in enumerate(ranked[:k], 1):
        s = series_of.get(pid, pid.rsplit(".", 1)[0])
        if s in relevant_series and s not in seen:
            seen.add(s)
            dcg += 1.0 / math.log2(i + 1)
    ideal = sum(1.0 / math.log2(i + 1) for i in range(1, min(len(relevant_series), k) + 1))
    return dcg / ideal if ideal else 0.0

"""Hybrid: lexical and semantic combined by rank.

The two are complementary. Lexical owns exact identifiers ("hf206",
"par_ac_down") and scores 0.00 on paraphrase; semantic owns paraphrase and is
vaguer on identifiers. Measured recall@5:

    engine     natural   paraphrase
    lexical      0.90       0.00
    semantic     0.90       0.43
    hybrid       1.00       0.29

They are combined by RANK, not by score. Score-level blending was tried and
failed: attribute and dataset cosines live on different scales, and any fixed
weight drowns one signal or the other. Reciprocal rank fusion never needs the
two scales to be commensurable.

Hybrid is the default for normal phrasing. For deliberately loose phrasing,
semantic alone is still better -- lexical contributes noise when it has nothing
to contribute, which is why hybrid's paraphrase number is below semantic's.
"""

from __future__ import annotations

import argparse

import numpy as np

from hf_search import corpus
from hf_search.lexical import Hit, LexicalIndex
from hf_search.semantic import SemanticIndex

# Small, because both input rankings are short and trustworthy. Larger values
# flatten the fusion toward a constant.
RRF_K = 20


class HybridIndex:
    def __init__(self, semantic=None, lexical=None, records=None, verbose=False):
        self.records = records if records is not None else corpus.load()
        self.sem = semantic or SemanticIndex.load(self.records)
        self.lex = lexical or LexicalIndex(self.records, verbose=verbose)
        self.titles = {r.id: r.title for r in self.records}

    def search(self, query: str, k: int = 10) -> list[Hit]:
        q = self.sem.embed_query(query)
        sims = self.sem.V @ q
        sem_rank = {self.sem.ids[i]: r for r, i in enumerate(np.argsort(-sims))}

        lex_hits = self.lex.search(query, k=60)
        lex_rank = {h.dataset: r for r, h in enumerate(lex_hits)}
        why_of = {h.dataset: h.why for h in lex_hits}

        fused = {}
        for d in set(sem_rank) | set(lex_rank):
            s = 0.0
            if d in sem_rank:
                s += 1.0 / (RRF_K + sem_rank[d])
            if d in lex_rank:
                s += 1.0 / (RRF_K + lex_rank[d])
            fused[d] = s

        out = []
        for d, s in sorted(fused.items(), key=lambda x: -x[1])[:k]:
            both = d in sem_rank and d in lex_rank
            why = why_of.get(d) or "semantic similarity"
            if both and d in lex_rank and lex_rank[d] < 20:
                why = f"{why} + semantic"
            out.append(Hit(d, s, self.titles.get(d, ""), why))
        return out


def get_engine(mode: str = "hybrid", records=None, verbose=False):
    """One place that knows how to construct each engine."""
    records = records if records is not None else corpus.load()
    if mode == "lexical":
        return LexicalIndex(records, verbose=verbose)
    if mode == "semantic":
        return SemanticIndex.load(records)
    if mode == "hybrid":
        return HybridIndex(records=records, verbose=verbose)
    raise ValueError(f"unknown mode {mode!r}; use lexical, semantic or hybrid")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="*")
    ap.add_argument("--mode", default="hybrid",
                    choices=["lexical", "semantic", "hybrid"])
    ap.add_argument("-k", type=int, default=10)
    a = ap.parse_args()
    if not a.question:
        print(__doc__)
        raise SystemExit(1)
    eng = get_engine(a.mode)
    for h in eng.search(" ".join(a.question), k=a.k):
        print(f"  {h.score:.4f}  {h.dataset:8s} {h.title[:52]:54s} <- {h.why}")

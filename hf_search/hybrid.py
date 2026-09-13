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
from hf_search.trace import NULL

# Small, because both input rankings are short and trustworthy. Larger values
# flatten the fusion toward a constant.
RRF_K = 20


class HybridIndex:
    def __init__(self, semantic=None, lexical=None, records=None, verbose=False):
        self.records = records if records is not None else corpus.load()
        self.sem = semantic or SemanticIndex.load(self.records)
        self.lex = lexical or LexicalIndex(self.records, verbose=verbose)
        self.titles = {r.id: r.title for r in self.records}

    def search(self, query: str, k: int = 10, trace=NULL) -> list[Hit]:
        q = self.sem.embed_query(query, trace=trace)
        sims = self.sem._sims(q, trace=trace)
        sem_rank = {self.sem.ids[i]: r for r, i in enumerate(np.argsort(-sims))}

        lex_hits = self.lex.search(query, k=60, trace=trace)
        lex_rank = {h.dataset: r for r, h in enumerate(lex_hits)}
        why_of = {h.dataset: h.why for h in lex_hits}

        with trace.stage("rrf", "Reciprocal rank fusion") as st:
            fused = {}
            for d in set(sem_rank) | set(lex_rank):
                s = 0.0
                if d in sem_rank:
                    s += 1.0 / (RRF_K + sem_rank[d])
                if d in lex_rank:
                    s += 1.0 / (RRF_K + lex_rank[d])
                fused[d] = s
            ranked = sorted(fused.items(), key=lambda x: -x[1])

            out = []
            for d, s in ranked[:k]:
                both = d in sem_rank and d in lex_rank
                why = why_of.get(d) or "semantic similarity"
                if both and d in lex_rank and lex_rank[d] < 20:
                    why = f"{why} + semantic"
                out.append(Hit(d, s, self.titles.get(d, ""), why))

            if trace.on:
                in_both = sum(1 for d in fused if d in sem_rank and d in lex_rank)
                st.fact("formula", f"score = 1/({RRF_K}+rank_sem) + 1/({RRF_K}+rank_lex)")
                st.fact("RRF_K", RRF_K)
                st.fact("candidates fused",
                        f"{len(fused)} ({len(sem_rank)} semantic, "
                        f"{len(lex_rank)} lexical, {in_both} in both)")
                st.fact("max possible score", round(2.0 / RRF_K, 4))
                st.note("Ranks, not scores, so a 0.58 cosine and a 0.12 TF-IDF "
                        "never have to be compared. Every dataset has a semantic "
                        "rank (all 458 are scored); only the lexical top 60 "
                        "have a lexical rank, so a dataset lexical never saw "
                        "gets exactly half the formula.")
                rows = []
                for r, (d, s) in enumerate(ranked[:k]):
                    sr = sem_rank.get(d)
                    lr = lex_rank.get(d)
                    rows.append([
                        r + 1, d, self.titles.get(d, "")[:48],
                        (sr + 1) if sr is not None else "-",
                        round(1.0 / (RRF_K + sr), 4) if sr is not None else 0,
                        (lr + 1) if lr is not None else "-",
                        round(1.0 / (RRF_K + lr), 4) if lr is not None else 0,
                        round(s, 4),
                    ])
                st.table("How the final ranking was produced",
                         ["final", "dataset", "title", "sem rank", "sem part",
                          "lex rank", "lex part", "fused"], rows)

                # What each engine's top 5 became after fusion. This is where
                # to look when the answer moved: a lexical #1 that lands at #7
                # got out-voted by semantic.
                movers = []
                for src, rank_of in (("semantic", sem_rank), ("lexical", lex_rank)):
                    for d, r in sorted(rank_of.items(), key=lambda x: x[1])[:5]:
                        final = next((i + 1 for i, (dd, _) in enumerate(ranked)
                                      if dd == d), None)
                        movers.append([src, r + 1, d, self.titles.get(d, "")[:48],
                                       final if final and final <= k else
                                       f"dropped (#{final})"])
                st.table("Where each engine's top 5 ended up",
                         ["engine", "its rank", "dataset", "title", "final"], movers)
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


def _print_trace(events: list) -> None:
    """Terminal rendering of a trace, for `--trace`."""
    for e in events:
        if e["ev"] == "start":
            print(f"\n[{e['i']}/{e['n']}] {e['label']}")
        elif e["ev"] == "end":
            print(f"      {e['ms']:.2f} ms" + (f"  FAILED: {e['failed']}" if e.get("failed") else ""))
            for k, v in e["facts"].items():
                print(f"      {k:36s} {v}")
            for t in e["tables"]:
                print(f"      -- {t['title']}")
                print("      " + " | ".join(f"{c:>10s}" for c in t["columns"]))
                for row in t["rows"]:
                    print("      " + " | ".join(f"{str(c)[:10]:>10s}" for c in row))
            for n in e["notes"]:
                print(f"      note: {n}")
        elif e["ev"] == "error":
            print(f"\nERROR {e['error']}")


if __name__ == "__main__":
    from hf_search.trace import Tracer, intake

    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="*")
    ap.add_argument("--mode", default="hybrid",
                    choices=["lexical", "semantic", "hybrid"])
    ap.add_argument("-k", type=int, default=10)
    ap.add_argument("--trace", action="store_true",
                    help="print every stage the query passes through")
    a = ap.parse_args()
    if not a.question:
        print(__doc__)
        raise SystemExit(1)
    eng = get_engine(a.mode)
    question = " ".join(a.question)
    if a.trace:
        tr = Tracer()
        tr.plan(a.mode)
        intake(tr, question, a.mode, a.k)
        hits = eng.search(question, k=a.k, trace=tr)
        with tr.stage("render", "Attach metadata, emit top k") as st:
            st.fact("hits", len(hits))
        tr.done()
        _print_trace(tr.events)
        drift = tr.unplanned()
        print(f"\ntotal {tr.elapsed_ms:.0f} ms" +
              (f"   plan drift: {drift}" if drift else ""))
        print()
    else:
        hits = eng.search(question, k=a.k)
    for h in hits:
        print(f"  {h.score:.4f}  {h.dataset:8s} {h.title[:52]:54s} <- {h.why}")

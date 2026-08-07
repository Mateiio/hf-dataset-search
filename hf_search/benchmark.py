"""Measuring the three engines.

Two query sets, kept separate on purpose.

**Hand-written** (17 queries). Real phrasing, including deliberately adversarial
paraphrases that share no vocabulary with their target. Small, so treat single
points with suspicion -- but it is the only set that tests what a person would
actually type.

**Auto-derived** (1,360 queries). One per dataset per family, built from the
dataset's own keywords, title and abstract. Large enough to detect a real change
from noise.

The auto-derived set has a flaw worth stating rather than burying: its queries
are excerpts of the indexed text, so lexical matching them is near-trivial and
TF-IDF scores 0.94 there while scoring 0.00 on hand-written paraphrase. Only the
`title` family -- where distinctive words are stripped -- is a fair comparison
between engines. The others are useful for detecting regressions within one
engine, not for ranking engines against each other.

    python -m hf_search.benchmark              hand-written, all engines
    python -m hf_search.benchmark --auto       the 1,360-query set
"""

from __future__ import annotations

import argparse
import random
import re
from dataclasses import dataclass

from hf_search import corpus
from hf_search.hybrid import get_engine

# --- hand-written: natural phrasing, the everyday case -----------------------
NATURAL = [
    ("30-minute below-canopy understory PAR at the EMS tower", {"hf206"}),
    ("plot coordinates latitude longitude for long-term research sites", {"hf375"}),
    ("eddy covariance net ecosystem exchange carbon flux tower", {"hf004"}),
    ("leaf area index measured at HEM and LPH towers", {"hf150"}),
    ("biomass inventory biometric plots EMS tower coarse woody debris", {"hf069"}),
    ("harmonized Landsat Sentinel vegetation indices NDVI EVI2", {"hf365"}),
    ("measured direct and diffuse solar radiation", {"hf249", "hf004", "hf102"}),
    ("microclimate at the hemlock and upper-slope towers", {"hf206"}),
    ("microclimate at the hardwood walk-up tower", {"hf282"}),
    ("spectral vegetation indices at 30 m resolution for plots", {"hf365"}),
]

# --- hand-written: adversarial paraphrase, no shared vocabulary --------------
# These are the reason a dense encoder is here at all. Lexical scores 0.00.
PARAPHRASE = [
    ("light below the canopy", {"hf206"}),
    ("how much sunlight reaches the forest floor", {"hf206"}),
    ("where exactly are the research plots located", {"hf375"}),
    ("carbon dioxide breathing in and out of the forest", {"hf004"}),
    ("how much leaf material falls each autumn", {"hf151"}),
    ("satellite greenness of the forest over time", {"hf365"}),
    ("cloudy versus clear sky sunlight split", {"hf249"}),
]

TITLE_STOP = {
    "harvard", "forest", "at", "the", "of", "in", "and", "for", "on", "since",
    "from", "to", "a", "an", "data", "dataset", "study", "project", "site",
    "sites", "experiment", "measurements", "massachusetts", "usa",
}


@dataclass
class Query:
    text: str
    want: set
    family: str


def auto_queries(rng_seed: int = 11) -> list[Query]:
    """One query per dataset per family, derived mechanically."""
    rng = random.Random(rng_seed)
    out = []
    for r in corpus.load():
        kws = [k for k in r.keywords if k.lower() not in
               {"harvard forest", "hfr", "lter", "usa", "massachusetts",
                "north america"}]
        if len(kws) >= 2:
            out.append(Query(", ".join(kws[:6]), {r.id}, "keywords"))

        words = [w for w in re.findall(r"[A-Za-z][A-Za-z-]+", r.title)
                 if w.lower() not in TITLE_STOP]
        if len(words) >= 3:
            keep = words[:]
            rng.shuffle(keep)
            out.append(Query(" ".join(keep[:max(2, len(keep) - 2)]),
                             {r.id}, "title"))

        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", r.abstract or "")
                 if len(s.strip()) > 60]
        if sents:
            out.append(Query(rng.choice(sents)[:300], {r.id}, "abstract"))
    return out


def rank_of(engine, query: str, want: set, depth: int = 25):
    order = [h.dataset for h in engine.search(query, k=depth)]
    return min((order.index(w) + 1 for w in want if w in order), default=None)


def score(engine, queries: list[Query], k: int = 5) -> dict:
    ranks = [rank_of(engine, q.text, q.want) for q in queries]
    n = len(ranks) or 1
    by_family: dict[str, list] = {}
    for q, r in zip(queries, ranks):
        by_family.setdefault(q.family, []).append(r)

    def agg(rs):
        m = len(rs) or 1
        return {"n": len(rs),
                "r@1": sum(1 for x in rs if x == 1) / m,
                "r@5": sum(1 for x in rs if x and x <= 5) / m,
                "r@10": sum(1 for x in rs if x and x <= 10) / m,
                "mrr": sum(1 / x for x in rs if x) / m}

    return {"overall": agg(ranks),
            "by_family": {f: agg(v) for f, v in by_family.items()}}


def hand_written() -> None:
    sets = {"natural": [Query(q, w, "natural") for q, w in NATURAL],
            "paraphrase": [Query(q, w, "paraphrase") for q, w in PARAPHRASE]}
    records = corpus.load()
    engines = {m: get_engine(m, records) for m in ("lexical", "semantic", "hybrid")}

    for label, qs in sets.items():
        print(f"\n{label}  ({len(qs)} queries)")
        print(f"  {'':50s} {'lex':>5s} {'sem':>5s} {'hyb':>5s}")
        hits = {m: 0 for m in engines}
        for q in qs:
            row = {}
            for m, e in engines.items():
                r = rank_of(e, q.text, q.want)
                row[m] = r
                hits[m] += bool(r and r <= 5)
            print(f"  {q.text[:50]:50s} "
                  + " ".join(f"{str(row[m]):>5s}" for m in
                             ("lexical", "semantic", "hybrid")))
        n = len(qs)
        print(f"  {'recall@5':50s} "
              + " ".join(f"{hits[m] / n:5.2f}" for m in
                         ("lexical", "semantic", "hybrid")))


def auto(limit: int | None = None) -> None:
    qs = auto_queries()
    if limit:
        qs = qs[::max(1, len(qs) // limit)][:limit]
    print(f"auto-derived benchmark: {len(qs):,} queries")
    print("NOTE: queries are excerpts of the indexed text, which flatters "
          "lexical.\n      Only the `title` family is a fair cross-engine "
          "comparison.")
    records = corpus.load()
    for m in ("lexical", "semantic", "hybrid"):
        res = score(get_engine(m, records), qs)
        o = res["overall"]
        print(f"\n{m}   n={o['n']:,}")
        print(f"  {'':10s} {'r@1':>6s} {'r@5':>6s} {'r@10':>6s} {'MRR':>6s}")
        print(f"  {'OVERALL':10s} {o['r@1']:6.3f} {o['r@5']:6.3f} "
              f"{o['r@10']:6.3f} {o['mrr']:6.3f}")
        for f, a in sorted(res["by_family"].items()):
            star = "  <- fair" if f == "title" else ""
            print(f"  {f:10s} {a['r@1']:6.3f} {a['r@5']:6.3f} "
                  f"{a['r@10']:6.3f} {a['mrr']:6.3f}{star}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--auto", action="store_true")
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    auto(a.limit) if a.auto else hand_written()

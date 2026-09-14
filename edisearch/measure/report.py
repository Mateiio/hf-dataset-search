"""Render results.jsonl as the report the current n supports, and no more.

    python -m edisearch.measure.report

The plan's staged ladder is authoritative and is enforced here rather than
left to whoever writes the paper:

    n < 30      a per-query table (query, target, rank under each method,
                overlap) and the disagreement cases written out. Counts, no
                percentages, no correlation, no test, no aggregate claim
    30 <= n < 60  add a scatter of overlap against reciprocal rank, one
                series per method, with Spearman's rho and n. Still no
                significance test between methods
    n >= 60     add a paired Wilcoxon signed-rank on reciprocal rank, hybrid
                against lexical, with the matched-pairs rank-biserial effect
                size and the count of non-tied pairs. No p-value on fewer
                than 15 non-tied pairs

Each origin (citation, generated, human) is reported on its own ladder, and
when a human set exists the correlation between the sets is reported too.
Every number comes from results.jsonl; the report says n, the methods, what
was indexed, and which claims the sample does not support.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import date

from edisearch.index import store
from edisearch.measure.run import RESULTS
from edisearch.paths import DOCS, DATA

REPORT = DOCS / "evaluation.md"
QUERIES = DATA / "queries.jsonl"
METHOD_ORDER = ["lexical", "bm25", "semantic", "hybrid", "hybrid-bm25"]


def _rr(rank):
    return 1.0 / rank if rank else 0.0


def load():
    rows = [json.loads(l) for l in RESULTS.read_text(encoding="utf-8").splitlines()]
    queries = {q["query_id"]: q for q in
               (json.loads(l) for l in QUERIES.read_text(encoding="utf-8").splitlines())}
    return rows, queries


def _scatter_svg(points: dict[str, list[tuple[float, float]]]) -> str:
    """Overlap (x) against reciprocal rank (y), one series per method. Inline SVG."""
    W, H, P = 560, 360, 44
    colours = {"lexical": "#1f77b4", "bm25": "#17becf", "semantic": "#d62728",
               "hybrid": "#2ca02c", "hybrid-bm25": "#9467bd"}
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'font-family="sans-serif" font-size="11">',
           f'<rect width="{W}" height="{H}" fill="white"/>',
           f'<line x1="{P}" y1="{H-P}" x2="{W-P}" y2="{H-P}" stroke="#333"/>',
           f'<line x1="{P}" y1="{P}" x2="{P}" y2="{H-P}" stroke="#333"/>',
           f'<text x="{W/2}" y="{H-10}" text-anchor="middle">overlap |Q∩D|/|Q|</text>',
           f'<text x="14" y="{H/2}" transform="rotate(-90 14 {H/2})" text-anchor="middle">reciprocal rank</text>']
    for t in (0, 0.5, 1):
        x = P + t * (W - 2 * P)
        y = H - P - t * (H - 2 * P)
        out.append(f'<text x="{x}" y="{H-P+14}" text-anchor="middle">{t}</text>')
        out.append(f'<text x="{P-6}" y="{y+4}" text-anchor="end">{t}</text>')
    for i, (m, pts) in enumerate(points.items()):
        c = colours.get(m, "#000")
        out.append(f'<text x="{W-P-120}" y="{P+14*i}" fill="{c}">● {m}</text>')
        for ox, ry in pts:
            x = P + ox * (W - 2 * P) + (i - 2) * 2.5   # small horizontal jitter per method
            y = H - P - ry * (H - 2 * P)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{c}" fill-opacity="0.7"/>')
    out.append("</svg>")
    return "\n".join(out)


def render(rows, queries, records_n: int, scopes_n: int) -> str:
    by_origin = defaultdict(lambda: defaultdict(dict))   # origin -> qid -> method -> row
    for r in rows:
        by_origin[r["origin"] or "citation"][r["query_id"]][r["method"]] = r
    methods = [m for m in METHOD_ORDER if any(m in d for o in by_origin.values() for d in o.values())]

    L = []
    w = L.append
    w("# Evaluation")
    w("")
    w(f"Rendered {date.today().isoformat()} by `python -m edisearch.measure.report` from "
      f"`data/results.jsonl`. Indexed: {records_n:,} current EDI packages across "
      f"{scopes_n} scopes (`data/records.jsonl`). Methods: {', '.join(f'`{m}`' for m in methods)}. "
      "Retrieval depth 100; a query's rank is the first position of any package in its "
      "relevant series (series = `scope.identifier`). Overlap is the pinned measure in "
      "`measure/overlap.py`: stemmed, stopword-free query tokens found anywhere in the "
      "indexed document, over query tokens.")
    w("")
    for origin, qs in sorted(by_origin.items()):
        n = len(qs)
        w(f"## {origin} queries, n = {n}")
        w("")
        stage = "demonstration" if n < 30 else ("correlation" if n < 60 else "paired test")
        w(f"**Stage: {stage}.** " + {
            "demonstration": "Ten-ish queries is an existence proof. The table below is the "
                             "whole result: no percentages, no correlation, no test, no "
                             "claim about which method is better.",
            "correlation": "Thirty-ish queries carries a correlation between overlap and "
                           "rank, reported with n. It does not carry a significance test "
                           "between methods, so none is reported.",
            "paired test": "Sixty or more queries carries a paired comparison. The Wilcoxon "
                           "signed-rank below is hybrid against lexical on reciprocal rank.",
        }[stage])
        w("")
        # per-query table, always
        w("| Query | Target | Overlap | " + " | ".join(f"`{m}`" for m in methods) + " |")
        w("|---|---|---:|" + "---:|" * len(methods))
        hits5 = Counter()
        for qid, byq in sorted(qs.items()):
            any_row = next(iter(byq.values()))
            text = queries[qid]["text"]
            target = queries[qid].get("provenance", {}).get("dataset_doi") or qid
            ov = any_row["overlap"]
            cells = []
            for m in methods:
                r = byq.get(m)
                rk = r["rank"] if r else None
                cells.append(str(rk) if rk else "–")
                if rk and rk <= 5:
                    hits5[m] += 1
            w(f"| {text[:110].replace('|', '/')}{'…' if len(text) > 110 else ''} | `{target}` | "
              f"{ov:.2f} | " + " | ".join(cells) + " |" if ov is not None else
              f"| {text[:110]} | `{target}` | – | " + " | ".join(cells) + " |")
        w(f"| **in top 5, count of {n}** | | | " + " | ".join(str(hits5[m]) for m in methods) + " |")
        w("")
        # disagreements, always
        dis = []
        for qid, byq in sorted(qs.items()):
            ranks = {m: byq[m]["rank"] for m in methods if m in byq}
            in5 = {m for m, rk in ranks.items() if rk and rk <= 5}
            if in5 and len(in5) < len(ranks):
                dis.append((qid, ranks, in5))
        w(f"**Disagreement cases ({len(dis)}):** queries some methods put in the top 5 and "
          "others did not.")
        w("")
        for qid, ranks, in5 in dis:
            miss = [m for m in ranks if m not in in5]
            miss_ranks = ", ".join(f"{m} {ranks[m] or '–'}" for m in miss)
            ov = qs[qid][methods[0]]["overlap"]
            w(f"- `{qid}` — in top 5 for {', '.join(sorted(in5))}; not for "
              f"{', '.join(miss)} ({miss_ranks}). "
              f"Overlap {ov if ov is None else round(ov, 2)}. Query: "
              f"“{queries[qid]['text'][:160]}”")
        w("")
        if n >= 30:
            from scipy import stats
            w("### Overlap against reciprocal rank")
            w("")
            pts = {m: [(byq[m]["overlap"] or 0.0, _rr(byq[m]["rank"])) for byq in qs.values() if m in byq]
                   for m in methods}
            w(_scatter_svg(pts))
            w("")
            w("| Method | Spearman ρ (overlap, RR) | n | MRR | recall@5 | recall@10 | nDCG@10 |")
            w("|---|---:|---:|---:|---:|---:|---:|")
            for m in methods:
                xs = [p[0] for p in pts[m]]
                ys = [p[1] for p in pts[m]]
                rho, _ = stats.spearmanr(xs, ys)
                rr = [_rr(byq[m]["rank"]) for byq in qs.values() if m in byq]
                r5 = sum(1 for byq in qs.values() if m in byq and byq[m]["rank"] and byq[m]["rank"] <= 5)
                r10 = sum(1 for byq in qs.values() if m in byq and byq[m]["rank"] and byq[m]["rank"] <= 10)
                nd = [byq[m]["ndcg10"] for byq in qs.values() if m in byq]
                w(f"| `{m}` | {rho:.2f} | {len(xs)} | {sum(rr)/len(rr):.3f} | {r5/len(rr):.2f} "
                  f"| {r10/len(rr):.2f} | {sum(nd)/len(nd):.3f} |")
            w("")
        if n >= 60 and "hybrid" in methods and "lexical" in methods:
            from scipy import stats
            a = [_rr(byq["hybrid"]["rank"]) for byq in qs.values() if "hybrid" in byq and "lexical" in byq]
            b = [_rr(byq["lexical"]["rank"]) for byq in qs.values() if "hybrid" in byq and "lexical" in byq]
            diffs = [x - y for x, y in zip(a, b)]
            nontied = sum(1 for d in diffs if d != 0)
            w("### Paired comparison, hybrid against lexical, reciprocal rank")
            w("")
            if nontied < 15:
                w(f"{nontied} non-tied pairs of {len(diffs)}: fewer than 15, so no p-value is reported.")
            else:
                res = stats.wilcoxon(a, b, zero_method="wilcox")
                # matched-pairs rank-biserial correlation
                pos = [d for d in diffs if d > 0]
                neg = [d for d in diffs if d < 0]
                ranks = stats.rankdata([abs(d) for d in diffs if d != 0])
                signs = [1 if d > 0 else -1 for d in diffs if d != 0]
                rb = sum(r * s for r, s in zip(ranks, signs)) / sum(ranks)
                w(f"Wilcoxon signed-rank W = {res.statistic:.1f}, p = {res.pvalue:.4f}, "
                  f"{nontied} non-tied pairs of {len(diffs)} ({len(pos)} favour hybrid, "
                  f"{len(neg)} favour lexical), matched-pairs rank-biserial r = {rb:.2f}.")
            w("")
    if "human" in by_origin and len(by_origin) > 1:
        w("## Agreement between query sets")
        w("")
        w("Per-method MRR on each set, side by side. Whether the method ordering agrees "
          "across sets is a finding either way.")
        w("")
        w("| Method | " + " | ".join(f"{o} (n={len(qs)})" for o, qs in sorted(by_origin.items())) + " |")
        w("|---|" + "---:|" * len(by_origin))
        for m in methods:
            cells = []
            for o, qs in sorted(by_origin.items()):
                rr = [_rr(byq[m]["rank"]) for byq in qs.values() if m in byq]
                cells.append(f"{sum(rr)/len(rr):.3f}" if rr else "–")
            w(f"| `{m}` | " + " | ".join(cells) + " |")
        w("")
    w("## What this report does not support")
    w("")
    for origin, qs in sorted(by_origin.items()):
        n = len(qs)
        if n < 30:
            w(f"- `{origin}`, n = {n}: no statement about which method is better, no "
              "correlation with overlap, no effect size. A demonstration only")
        elif n < 60:
            w(f"- `{origin}`, n = {n}: a correlation, not a comparison between methods")
        else:
            w(f"- `{origin}`, n = {n}: a paired comparison of hybrid against lexical only; "
              "other pairs of methods are not tested")
    if "human" not in by_origin:
        w("- No human-written query set exists yet (M4c is blocked on the human-subjects "
          "route), so nothing here says how these queries relate to what people type")
    w("")
    return "\n".join(L)


def main(argv=None) -> int:
    rows, queries = load()
    records = store.load_records()
    scopes = {r.id.rsplit(".", 2)[0] for r in records}
    REPORT.write_text(render(rows, queries, len(records), len(scopes)), encoding="utf-8")
    print(f"wrote {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

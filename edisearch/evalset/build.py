"""M4a: turn the owner's verdicts into queries.jsonl and qrels.jsonl.

    python -m edisearch.evalset.build

The owner reads `docs/yield_probe.md` and writes one word after each
`- **Verdict:**` line:

    usable      a stranger could tell from the sentence what the dataset holds
    use-only    it says what the paper did with the data, not what the data is
    vague       neither
    skip        wrong attribution, not a paper, or otherwise unusable

Optionally `#2` picks the second listed hit instead of the marked candidate,
and anything after that is a note. The verdicts are saved to
`data/evalset/verdicts.json` keyed by (dataset DOI, citing DOI), so they
survive a regenerated report and a larger sample.

Only `usable` pairs become queries. `use-only` pairs are kept in the verdict
file and counted in the report, because the plan's staged ladder reports n
and the yield, not just the survivors. Every query stores the citing DOI and
character offsets into the saved text, which is what a released collection
publishes instead of the harvested sentences (plan, M4a, copyright).

Interfaces are the plan's:

    data/queries.jsonl  {query_id, text, origin, provenance, created_at}
    data/qrels.jsonl    {query_id, package_id, series_id, relevance}
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

from edisearch.evalset import yield_probe
from edisearch.paths import DATA, EVALSET

VERDICTS = EVALSET / "verdicts.json"
QUERIES = DATA / "queries.jsonl"
QRELS = DATA / "qrels.jsonl"

_HEAD = re.compile(r"^### (\d+)\. `([^`]+)` cited by `([^`]+)`", re.M)
_VERDICT = re.compile(r"^- \*\*Verdict:\*\*\s*(.*)$", re.M)
WORDS = ("usable", "use-only", "vague", "skip")


def read_verdicts(report: Path = yield_probe.REPORT) -> dict:
    """{(dataset_doi, citing_doi): {"verdict", "hit", "note"}} from the report."""
    text = report.read_text(encoding="utf-8")
    rows = {(r["dataset_doi"], r["citing_doi"]): r
            for r in (json.loads(l) for l in yield_probe.OUT.read_text(encoding="utf-8").splitlines())}
    by_i = {r["i"]: r for r in rows.values()}
    out = json.loads(VERDICTS.read_text(encoding="utf-8")) if VERDICTS.exists() else {}
    heads = list(_HEAD.finditer(text))
    for k, h in enumerate(heads):
        block = text[h.end(): heads[k + 1].start() if k + 1 < len(heads) else len(text)]
        m = _VERDICT.search(block)
        raw = (m.group(1) if m else "").strip()
        if not raw:
            continue
        word = raw.split()[0].lower().rstrip(".,;:")
        if word not in WORDS:
            print(f"  #{h.group(1)}: verdict {raw[:30]!r} not one of {WORDS}; ignored")
            continue
        r = by_i.get(int(h.group(1)))
        if not r:
            continue
        pick = re.search(r"#(\d+)", raw)
        out[f"{r['dataset_doi']}|{r['citing_doi']}"] = {
            "verdict": word, "hit": int(pick.group(1)) if pick else None,
            "note": re.sub(r"^\S+\s*(#\d+\s*)?", "", raw).strip(),
            "judged": date.today().isoformat()}
    VERDICTS.write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    return out


def build(verdicts: dict | None = None) -> dict:
    verdicts = verdicts if verdicts is not None else read_verdicts()
    rows = [json.loads(l) for l in yield_probe.OUT.read_text(encoding="utf-8").splitlines()]
    queries, qrels, counts = [], [], {w: 0 for w in WORDS}
    counts["unjudged"] = 0
    for r in rows:
        v = verdicts.get(f"{r['dataset_doi']}|{r['citing_doi']}")
        if not v:
            counts["unjudged"] += 1
            continue
        counts[v["verdict"]] += 1
        if v["verdict"] != "usable":
            continue
        hit = (r["hits"][v["hit"] - 1] if v.get("hit") and v["hit"] <= len(r["hits"])
               else r["query_candidate"])
        if not hit:
            print(f"  #{r['i']}: usable but no sentence to take; skipped")
            continue
        qid = f"cit-{len(queries) + 1:06d}"
        pkg = r["dataset"]["package_id"]
        scope, ident, _ = pkg.rsplit(".", 2)
        queries.append({
            "query_id": qid, "text": hit["sentence"], "origin": "citation",
            "provenance": {"citing_doi": r["citing_doi"], "dataset_doi": r["dataset_doi"],
                           "route": r["route"], "kind": hit["kind"],
                           "char_start": hit["char_start"], "char_end": hit["char_end"],
                           "ref_label": hit.get("ref_label")},
            "created_at": date.today().isoformat()})
        qrels.append({"query_id": qid, "package_id": pkg,
                      "series_id": f"{scope}.{ident}", "relevance": 1})
    DATA.mkdir(parents=True, exist_ok=True)
    QUERIES.write_text("".join(json.dumps(q, ensure_ascii=False) + "\n" for q in queries),
                       encoding="utf-8")
    QRELS.write_text("".join(json.dumps(q) + "\n" for q in qrels), encoding="utf-8")
    judged = sum(counts[w] for w in WORDS)
    print(f"{len(rows)} pairs: {judged} judged "
          f"({', '.join(f'{w} {counts[w]}' for w in WORDS)}), {counts['unjudged']} unjudged")
    print(f"{len(queries)} citation queries -> {QUERIES.name}, {len(qrels)} qrels -> {QRELS.name}")
    if judged:
        print(f"yield: {counts['usable']}/{judged} = {100 * counts['usable'] / judged:.0f}% "
              f"of judged pairs, {counts['usable']}/{len(rows)} = "
              f"{100 * counts['usable'] / len(rows):.0f}% of sampled links")
    return {"queries": queries, "qrels": qrels, "counts": counts}


if __name__ == "__main__":
    build()
    sys.exit(0)

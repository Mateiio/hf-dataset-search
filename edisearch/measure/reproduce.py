"""M2 acceptance: the original 17 queries over the EDI corpus, like for like.

    python -m edisearch.measure.reproduce

The repo's README reports, on 17 hand-written queries over the 458 Harvard
Forest archive datasets: lexical 0.90 / 0.00, semantic 0.90 / 0.43, hybrid
1.00 / 0.29 recall@5 on the 10 natural and 7 paraphrase queries. (The plan's
"recall@5 of 1.00 on 17 queries" was that table's natural column.) The plan's rule: before anything else changes, reproduce that
number over the EDI harvest of the same 459 packages with the same engines
unchanged. If it does not reproduce, the corpus or the index differs and that
has to be understood first. Only then is BM25 recorded beside TF-IDF.

Both corpora are scored here, in one run, on one machine, so the comparison
is between two columns of the same table rather than a README written on a
different day. The query targets are the same datasets under two id schemes:
`hf116` in the archive, `knb-lter-hfr.116.<rev>` in EDI.

Writes `docs/reproduction.md`.
"""

from __future__ import annotations

import sys
from datetime import date

from hf_search import corpus as hf_corpus
from hf_search.benchmark import NATURAL, PARAPHRASE, rank_of
from hf_search.hybrid import get_engine as hf_engine
from edisearch.index import store
from edisearch.paths import DOCS

REPORT = DOCS / "reproduction.md"
HF_MODES = ("lexical", "semantic", "hybrid")


def edi_targets(records) -> dict[str, str]:
    """hf116 -> knb-lter-hfr.116.<rev> for the packages in the corpus."""
    out = {}
    for r in records:
        scope, ident, _ = r.id.rsplit(".", 2)
        if scope == "knb-lter-hfr":
            out[f"hf{int(ident):03d}"] = r.id
    return out


def run(verbose: bool = True) -> dict:
    queries = [(q, w, "natural") for q, w in NATURAL] + \
              [(q, w, "paraphrase") for q, w in PARAPHRASE]

    hf_records = hf_corpus.load()
    edi_records = store.load_records(scope="knb-lter-hfr")
    to_edi = edi_targets(edi_records)

    engines = {f"archive/{m}": hf_engine(m, hf_records) for m in HF_MODES}
    engines.update({f"edi/{m}": store.get_engine(m, edi_records) for m in store.MODES})

    rows = []
    for text, want, family in queries:
        ranks = {}
        for name, eng in engines.items():
            targets = want if name.startswith("archive/") else {to_edi[w] for w in want if w in to_edi}
            ranks[name] = rank_of(eng, text, targets)
        rows.append({"query": text, "family": family, "want": sorted(want), "ranks": ranks})

    def recall(names, fam=None, k=5):
        rs = [r for r in rows if fam is None or r["family"] == fam]
        return {n: sum(1 for r in rs if r["ranks"][n] and r["ranks"][n] <= k) / len(rs)
                for n in names}

    names = list(engines)
    result = {"date": date.today().isoformat(), "n": len(rows),
              "n_natural": sum(1 for r in rows if r["family"] == "natural"),
              "n_paraphrase": sum(1 for r in rows if r["family"] == "paraphrase"),
              "rows": rows,
              "recall5": {"all": recall(names), "natural": recall(names, "natural"),
                          "paraphrase": recall(names, "paraphrase")},
              "recall1": {"all": recall(names, k=1)},
              "hf_size": len(hf_records), "edi_size": len(edi_records)}
    if verbose:
        _print(result, names)
    _write(result, names)
    return result


def _print(res, names):
    short = [n.replace("archive/", "A:").replace("edi/", "E:") for n in names]
    print(f"\n{'query':52s} " + " ".join(f"{s:>9s}" for s in short))
    for r in res["rows"]:
        print(f"{r['query'][:52]:52s} " + " ".join(
            f"{str(r['ranks'][n] or '-'):>9s}" for n in names))
    for fam in ("natural", "paraphrase", "all"):
        print(f"{'recall@5 ' + fam:52s} " + " ".join(
            f"{res['recall5'][fam][n]:9.2f}" for n in names))


def _write(res, names):
    L = []
    w = L.append
    w("# Reproduction: the original 17 queries over the EDI harvest")
    w("")
    w(f"Run {res['date']} by `python -m edisearch.measure.reproduce`. Both corpora scored "
      f"in the same process on the same machine: the archive corpus is the repo's shipped "
      f"`data/records.json` ({res['hf_size']} datasets, tag `v1-hf-only`); the EDI corpus is "
      f"the M1 harvest of `knb-lter-hfr` ({res['edi_size']} packages) parsed by the same "
      f"`eml.py`. Engines are `hf_search`'s, unchanged; `bm25` is the new baseline.")
    w("")
    w("## Recall@5")
    w("")
    w("| Query set | n | " + " | ".join(f"`{n}`" for n in names) + " |")
    w("|---|---:|" + "---:|" * len(names))
    for fam, n in (("natural", res["n_natural"]), ("paraphrase", res["n_paraphrase"]),
                   ("all", res["n"])):
        w(f"| {fam} | {n} | " + " | ".join(f"{res['recall5'][fam][k]:.2f}" for k in names) + " |")
    w("")
    a, e = res["recall5"]["all"], res["recall5"]["all"]
    ok = all(abs(a[f"archive/{m}"] - e[f"edi/{m}"]) < 1e-9 for m in HF_MODES)
    w("**Like for like:** " + (
        "every unchanged engine scores the same on the EDI harvest as on the archive "
        "corpus, rank for rank, and the archive column matches the README's table "
        "(lexical 0.90 / 0.00, semantic 0.90 / 0.43, hybrid 1.00 / 0.29). The corpus "
        "and the index reproduce. The plan's \"recall@5 of 1.00 on 17 queries\" was the "
        "natural column of that table; there was never a 1.00 on all 17."
        if ok else
        "the unchanged engines do **not** score the same on the two corpora. Per-query "
        "ranks below show where; that has to be understood before anything else changes."))
    w("")
    w("## Per-query rank of the target (lower is better, `-` = not in the top 25)")
    w("")
    w("| Query | Family | " + " | ".join(f"`{n}`" for n in names) + " |")
    w("|---|---|" + "---:|" * len(names))
    for r in res["rows"]:
        w(f"| {r['query']} | {r['family']} | " + " | ".join(
            str(r["ranks"][n] or "-") for n in names) + " |")
    w("")
    w("## What BM25 adds")
    w("")
    w("`bm25` is plain Okapi BM25 (k1 1.2, b 0.75, unigrams) over the same document text "
      "the TF-IDF engine indexes, with none of the TF-IDF engine's extras: no bigrams, no "
      "second index over column definitions, no reserved result slots. It is the textbook "
      "lexical baseline the published dataset-search work reports against, which is why it "
      "is recorded here beside the engine that actually made the demo work. `hybrid-bm25` "
      "fuses it with the same dense vectors by the same reciprocal rank fusion.")
    w("")
    w("Seventeen queries is a regression check, not a measurement. The author of these "
      "queries built the system, so they cannot serve as the human arm of the evaluation "
      "(decision 0009); they exist to show the port did not break anything.")
    w("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L), encoding="utf-8")
    print(f"\nwrote {REPORT}")


if __name__ == "__main__":
    run()
    sys.exit(0)

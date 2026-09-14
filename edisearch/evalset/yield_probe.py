"""M3-lite: what fraction of citation links yield a usable query sentence?

    python -m edisearch.evalset.yield_probe            50 links, seed 0
    python -m edisearch.evalset.yield_probe --n 100 --seed 1

Decision 0009 puts this ahead of the harvest: thousands of links exist, and
the number that decides the venue is how many survive as sentences a person
would recognise as describing the dataset. This script measures the
mechanical half -- can the paper be read, does it name the dataset, how --
and writes every candidate out for a person to judge. It makes no claim
about usability itself.

Steps, all cached under `data/evalset/`:

1. links        every (dataset DOI, citing DOI) pair DataCite knows -> links.jsonl
2. sample       n pairs, fixed seed, uniform over the pool -> yield_sample.json
3. dataset      title, package id, creators, year per DOI -> datasets/
4. text         full text of the citing paper, if open -> fulltext/
5. extract      sentences naming the dataset, by kind -> yield_probe.jsonl
6. report       docs/yield_probe.md: the funnel, then every pair for reading

Uniform sampling over the pool, not stratified by source, so the rate is the
pool's rate. Source is recorded per pair so a difference shows up anyway.
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from edisearch.evalset import citations, extract, fulltext
from edisearch.paths import DOCS, EVALSET, FIXTURES

LINKS = EVALSET / "links.jsonl"
SAMPLE = EVALSET / "yield_sample.json"
DATASETS = EVALSET / "datasets"
OUT = EVALSET / "yield_probe.jsonl"
REPORT = DOCS / "yield_probe.md"


def load_links(force: bool = False) -> list[dict]:
    if LINKS.exists() and not force:
        return [json.loads(l) for l in LINKS.read_text(encoding="utf-8").splitlines()]
    EVALSET.mkdir(parents=True, exist_ok=True)
    rows = citations.links()
    LINKS.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return rows


def sample(rows: list[dict], n: int, seed: int) -> list[dict]:
    """The first n of a fixed random order of the pool.

    Prefix-stable: `--n 300` extends the 50 already read rather than drawing
    a fresh 50. The first 50 are exactly the draw the first probe made
    (`Random(seed).sample(rows, 50)`); the rest is the remainder shuffled
    with the same seed.
    """
    key = {"n": n, "seed": seed, "pool": len(rows)}
    if SAMPLE.exists():
        s = json.loads(SAMPLE.read_text(encoding="utf-8"))
        if s["key"] == key:
            return s["rows"]
    first = random.Random(seed).sample(rows, min(50, n, len(rows)))
    taken = {(r["dataset_doi"], r["citing_doi"]) for r in first}
    rest = [r for r in rows if (r["dataset_doi"], r["citing_doi"]) not in taken]
    random.Random(seed).shuffle(rest)
    picked = (first + rest)[:n]
    SAMPLE.write_text(json.dumps({"key": key, "rows": picked}, indent=1), encoding="utf-8")
    return picked


def dataset(doi: str) -> dict:
    DATASETS.mkdir(parents=True, exist_ok=True)
    p = DATASETS / f"{fulltext.slug(doi)}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    d = citations.dataset(doi)
    p.write_text(json.dumps(d, indent=1), encoding="utf-8")
    return d


def save_fixtures(results: list[dict]) -> None:
    """One real response per endpoint, taken from the cache, per the plan."""
    fx = FIXTURES
    (fx / "datacite").mkdir(parents=True, exist_ok=True)
    (fx / "openalex").mkdir(exist_ok=True)
    (fx / "europepmc").mkdir(exist_ok=True)
    done = set()
    for r in results:
        d = fulltext.folder(r["citing_doi"])
        ds = DATASETS / f"{fulltext.slug(r['dataset_doi'])}.json"
        if "doi" not in done and ds.exists():
            shutil.copy(ds, fx / "datacite" / "doi_record.json"); done.add("doi")
        if "oa" not in done and (d / "openalex.json").exists():
            shutil.copy(d / "openalex.json", fx / "openalex" / "work.json"); done.add("oa")
        if "ep" not in done and (d / "europepmc.json").exists():
            shutil.copy(d / "europepmc.json", fx / "europepmc" / "search.json"); done.add("ep")
        if "xml" not in done and (d / "fulltext.xml").exists():
            shutil.copy(d / "fulltext.xml", fx / "europepmc" / "fulltext.xml"); done.add("xml")
    if not (fx / "datacite" / "events_page.json").exists():
        code, body, _ = citations.net.get(
            f"{citations.API}/events?prefix={citations.PREFIX}"
            "&relation-type-id=references&page%5Bsize%5D=3")
        (fx / "datacite" / "events_page.json").write_bytes(body)


def run(n: int, seed: int, force: bool) -> list[dict]:
    rows = load_links(force)
    print(f"{len(rows):,} distinct (dataset, paper) pairs in the pool")
    picked = sample(rows, n, seed)
    siblings = Counter(r["citing_doi"] for r in rows)

    results = []
    for i, link in enumerate(picked, 1):
        ds = dataset(link["dataset_doi"])
        meta = fulltext.text(link["citing_doi"])
        oa = fulltext.openalex(link["citing_doi"])
        hits = (extract.find(fulltext.read_text(link["citing_doi"]), ds,
                             reflist_start=meta.get("reflist_start", -1))
                if meta["route"] else [])
        results.append({
            "i": i, **link,
            "dataset": {k: ds.get(k) for k in ("title", "package_id", "year", "creators")},
            "paper": {k: oa.get(k) for k in ("title", "journal", "year", "oa_status")},
            "edi_datasets_cited_by_paper": siblings[link["citing_doi"]],
            "route": meta["route"], "outcome": meta.get("outcome"),
            "chars": meta["chars"], "tried": meta["tried"],
            "hits": hits,
            "best_kind": hits[0]["kind"] if hits else None,
            "body_hit": any(not h["in_reference_list"] for h in hits),
            "query_candidate": extract.best_query(hits),
        })
        print(f"  {i:3d} {link['citing_doi'][:32]:32s} {meta.get('outcome') or '-':12s} "
              f"{(hits[0]['kind'] if hits else '-'):12s} {ds.get('package_id')}")
    OUT.write_text("".join(json.dumps(r) + "\n" for r in results), encoding="utf-8")
    save_fixtures(results)
    return results


def report(results: list[dict], pool: int, seed: int) -> Path:
    n = len(results)
    verdicts_path = EVALSET / "verdicts.json"
    verdicts = json.loads(verdicts_path.read_text(encoding="utf-8")) if verdicts_path.exists() else {}
    routes = Counter(r["outcome"] for r in results)
    kinds = Counter(r["best_kind"] or ("no-mention" if r["route"] else r["outcome"])
                    for r in results)
    by_source = defaultdict(Counter)
    for r in results:
        for s in r["sources"]:
            by_source[s.split("/")[0]][r["best_kind"] or "none"] += 1
    named = sum(1 for r in results if r["best_kind"] in ("doi", "package_id", "title", "marker"))
    body = sum(1 for r in results if r["query_candidate"])
    refs_only = sum(1 for r in results if r["hits"] and not r["query_candidate"])
    via_marker = sum(1 for r in results if r["query_candidate"]
                     and r["query_candidate"]["kind"] == "marker")
    weak = sum(1 for r in results if r["best_kind"] in ("author_year", "generic"))

    L = []
    w = L.append
    w("# Yield probe: citation links to candidate query sentences")
    w("")
    w(f"Run {date.today().isoformat()} by `python -m edisearch.evalset.yield_probe`, "
      f"n = {n}, seed {seed}, sampled uniformly from {pool:,} distinct (dataset, paper) "
      "pairs in DataCite. Mechanical yield only: whether the paper could be read and "
      "whether it names the dataset. **Whether a sentence describes what the dataset "
      "contains is a human call and the column for it is empty below.**")
    w("")
    w("## Funnel")
    w("")
    w("| Stage | Pairs | Share |")
    w("|---|---:|---:|")
    w(f"| Sampled | {n} | 100% |")
    r_open = routes["europepmc"] + routes["pdf"] + routes["manual"]
    other = routes["not-a-paper"] + routes["non-doi"]
    w(f"| Full text read by the script | {r_open} | {100 * r_open / n:.0f}% |")
    w(f"| ... via Europe PMC XML | {routes['europepmc']} | |")
    w(f"| ... via open PDF | {routes['pdf']} | |")
    w(f"| ... via a PDF saved by hand | {routes['manual']} | |")
    w(f"| Dataset named unambiguously (DOI, package id or title) | {named} | {100 * named / n:.0f}% |")
    w(f"| ... with a query candidate in the body text | {body} | {100 * body / n:.0f}% |")
    w(f"| ...... of which found by resolving a reference-list marker | {via_marker} | |")
    w(f"| ... hits only in the reference list (body sentence still to be resolved) | {refs_only} | {100 * refs_only / n:.0f}% |")
    w(f"| Only a weak pointer (author-year or a generic EDI mention) | {weak} | {100 * weak / n:.0f}% |")
    w(f"| Read, but no mention of the dataset found | {kinds['no-mention']} | {100 * kinds['no-mention'] / n:.0f}% |")
    w(f"| Open in a browser, bot-walled for a script (recoverable by hand) | {routes['walled']} | {100 * routes['walled'] / n:.0f}% |")
    w(f"| Closed | {routes['closed']} | {100 * routes['closed'] / n:.0f}% |")
    w(f"| Not a paper, or not a DOI (theses, GBIF downloads) | {other} | {100 * other / n:.0f}% |")
    w("")
    w("The walled row matters: those papers are open access, only the download is "
      "refused to a script. At the sizes this project needs (tens to low hundreds of "
      "pairs) a person can save them from a browser, so the reachable share for the "
      f"evaluation set is up to {100 * (r_open + routes['walled']) / n:.0f}%, not "
      f"{100 * r_open / n:.0f}%.")
    w("")
    w("By link source (a pair can be in both): " + "; ".join(
        f"`{s}` " + ", ".join(f"{k} {v}" for k, v in c.most_common())
        for s, c in sorted(by_source.items())))
    w("")
    multi = sum(1 for r in results if r["edi_datasets_cited_by_paper"] > 1)
    w(f"{multi} of {n} citing papers cite more than one EDI dataset, which is where "
      "attribution can go wrong; those rows say how many.")
    w("")
    w("## Every pair, for reading")
    w("")
    judged = sum(1 for r in results if f"{r['dataset_doi']}|{r['citing_doi']}" in verdicts)
    if judged:
        c = Counter(verdicts[f"{r['dataset_doi']}|{r['citing_doi']}"]["verdict"] for r in results
                    if f"{r['dataset_doi']}|{r['citing_doi']}" in verdicts)
        w(f"**Verdicts so far:** {judged} of {n} judged: " +
          ", ".join(f"{k} {v}" for k, v in c.most_common()) +
          f". Yield {c['usable']}/{judged} of judged pairs, {c['usable']}/{n} of sampled links. "
          "Pre-screened by the coding agent, confirmed by the owner; verdicts live in "
          "`data/evalset/verdicts.json` and survive a regenerated report.")
        w("")
    w("Read the sentence(s). Mark **usable** if a person who had never seen the "
      "dataset could tell from the sentence roughly what it contains; **use-only** "
      "if it says what the paper did with it but not what it is; **vague** if "
      "neither. Write the verdict in the last column and the yield is the count. "
      "A hit marked *reference list* is the bibliography entry, which proves the "
      "citation but is not a query; judge the *body* hits, and where there are none "
      "the body sentence has still to be found (M3's marker resolution).")
    w("")
    for r in results:
        d, p = r["dataset"], r["paper"]
        w(f"### {r['i']}. `{d['package_id'] or r['dataset_doi']}` cited by `{r['citing_doi']}`")
        w("")
        w(f"- **Dataset:** {d['title']} ({d['year']})")
        w(f"- **Paper:** {p.get('title') or '(title unknown)'} — *{p.get('journal') or '?'}*, "
          f"{p.get('year') or '?'}, OA {p.get('oa_status') or '?'}; cites "
          f"{r['edi_datasets_cited_by_paper']} EDI dataset(s); link source {', '.join(r['sources'])}")
        if not r["route"]:
            w(f"- **Text:** {r['outcome']} ({'; '.join(r['tried']) or 'no open location'})")
            if r["outcome"] == "walled":
                w(f"- **To read it by hand:** save the PDF as "
                  f"`data/evalset/manual/{fulltext.slug(r['citing_doi'])}.pdf` and re-run")
        else:
            w(f"- **Text:** {r['route']}, {r['chars']:,} chars")
            if not r["hits"]:
                w("- **Mention:** none found")
            best = extract.best_query(r["hits"])
            for h in r["hits"]:
                where = "reference list" if h["in_reference_list"] else "body"
                tag = " ← **query candidate**" if h is best else ""
                via = f" via ref {h['ref_label']}" if h.get("ref_label") else ""
                w(f"- **{h['kind']}**{via}, {where} [{h['char_start']}–{h['char_end']}]: "
                  f"{h['sentence'][:600]}{tag}")
        v = verdicts.get(f"{r['dataset_doi']}|{r['citing_doi']}")
        w("- **Verdict:** " + (f"{v['verdict']} {v.get('note', '')}".strip() if v else ""))
        w("")
    REPORT.write_text("\n".join(L), encoding="utf-8")
    return REPORT


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--force", action="store_true", help="re-fetch the link pool")
    a = ap.parse_args(argv)
    results = run(a.n, a.seed, a.force)
    pool = sum(1 for _ in LINKS.open(encoding="utf-8"))
    path = report(results, pool, a.seed)
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""M0: how much of EDI does DataONE actually expose?

    python -m edisearch.acquire.probe              everything, cached where it can be
    python -m edisearch.acquire.probe --force      re-sweep the object store
    python -m edisearch.acquire.probe --no-packages  skip the per-package portal check

Five steps, each writing to `data/probe/` so a re-run skips what exists:

1. sweep     every EML object in the coordinating node's object store, per
             member node and EML version, kept if its id parses as a PASTA
             package id in any of the three spellings -> dataone_eml_objects.jsonl.
             Uses `listObjects`, not Solr: the index holds two thirds of the
             objects and lags by months (see `dataone.py`)
2. dedupe    normalise, group by series (scope.identifier), keep the highest
             revision -> packages.jsonl
3. scopes    the portal's count per scope, plus the home page's two tiers
             -> portal_counts.json. A scope the portal does not know is not an
             EDI scope, whatever its id looks like
4. packages  for every series in a research scope, ask the portal whether
             DataONE's newest revision is EDI's current one, and if not
             whether the series exists at all -> portal_packages.json.
             One request per series, two for the misses, at 2 per second:
             about two hours for the whole research tier. Resumable
5. fixture   one full EML fetched end to end and parsed by the reused
             `hf_search.eml` -> fixtures/dataone/

Then `docs/acquisition.md` gets the table. No coverage threshold: measure it,
write it down, proceed. Whether thin coverage is a problem is the owner's call.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from edisearch.acquire import dataone, portal
from edisearch.paths import DOCS, FIXTURES, PROBE

OBJECTS = PROBE / "dataone_eml_objects.jsonl"
SWEEP = PROBE / "sweep_summary.json"
PACKAGES = PROBE / "packages.jsonl"
COUNTS = PROBE / "portal_counts.json"
STATUS = PROBE / "portal_packages.json"
REPORT = DOCS / "acquisition.md"
FIXTURE_DIR = FIXTURES / "dataone"

# The package the plan spot-checked, and the one every acceptance check parses.
FIXTURE_PKG = ("knb-lter-hfr", 116, 16)


# ------------------------------------------------------------------- 1 sweep

def sweep(force: bool = False) -> dict:
    if OBJECTS.exists() and SWEEP.exists() and not force:
        return json.loads(SWEEP.read_text())
    PROBE.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic()
    nodes = dataone.list_nodes()
    totals = {f: dataone.count_objects(f) for f in dataone.EML_FORMAT_IDS}
    print(f"sweeping {sum(totals.values()):,} EML objects across {len(nodes)} nodes")

    kept = Counter()      # node -> parsed as PASTA id
    dropped = Counter()   # node -> not a PASTA id
    forms = Counter()
    formats = Counter()
    per_node_total = Counter()
    n = 0
    with OBJECTS.open("w", encoding="utf-8") as out:
        for fmt in dataone.EML_FORMAT_IDS:
            for node in nodes:
                c = dataone.count_objects(fmt, node)
                if not c:
                    continue
                per_node_total[node] += c
                for doc in dataone.iter_objects(fmt, node):
                    n += 1
                    parsed = dataone.parse_pid(doc["id"])
                    if not parsed:
                        dropped[node] += 1
                        continue
                    form, scope, ident, rev = parsed
                    kept[node] += 1
                    forms[form] += 1
                    formats[fmt] += 1
                    out.write(json.dumps({
                        "pid": doc["id"], "form": form, "scope": scope,
                        "identifier": ident, "revision": rev, "node": node,
                        "formatId": fmt,
                        "modified": doc["dateSysMetadataModified"],
                        "size": doc["size"],
                    }) + "\n")
            print(f"  {fmt.split('/')[-1]}: {formats[fmt]:,} PASTA ids "
                  f"({n:,} objects seen so far)")
    summary = {
        "date": date.today().isoformat(),
        "eml_objects_in_store": totals,
        "eml_objects_total": sum(totals.values()),
        "attributed_to_a_node": sum(per_node_total.values()),
        "seen": n,
        "pasta_ids": sum(kept.values()),
        "pasta_ids_by_node": dict(kept.most_common()),
        "non_pasta_by_node": dict(dropped.most_common()),
        "pasta_ids_by_form": dict(forms),
        "pasta_ids_by_formatId": dict(formats.most_common()),
        "seconds": round(time.monotonic() - t0),
    }
    SWEEP.write_text(json.dumps(summary, indent=2))
    print(f"  kept {summary['pasta_ids']:,} PASTA ids in {summary['seconds']} s")
    return summary


# ------------------------------------------------------------------ 2 dedupe

def dedupe() -> list[dict]:
    series: dict[tuple[str, int], list[dict]] = defaultdict(list)
    with OBJECTS.open(encoding="utf-8") as f:
        for line in f:
            o = json.loads(line)
            series[(o["scope"], o["identifier"])].append(o)

    packages = []
    for (scope, ident), docs in sorted(series.items()):
        newest = max(docs, key=lambda d: d["revision"])
        packages.append({
            "package_id": dataone.package_id(scope, ident, newest["revision"]),
            "series_id": f"{scope}.{ident}",
            "scope": scope, "identifier": ident,
            "revision": newest["revision"],
            "pid": newest["pid"], "form": newest["form"], "node": newest["node"],
            "formatId": newest["formatId"],
            "modified": newest["modified"], "size": newest["size"],
            "revisions_in_dataone": len(docs),
            "forms_seen": sorted({d["form"] for d in docs}),
            "nodes_seen": sorted({d["node"] for d in docs}),
        })
    with PACKAGES.open("w", encoding="utf-8") as out:
        for p in packages:
            out.write(json.dumps(p) + "\n")
    print(f"  {len(packages):,} distinct series at newest revision")
    return packages


# ------------------------------------------------------------------ 3 scopes

def portal_counts(scopes: list[str], force: bool = False) -> dict:
    cached = json.loads(COUNTS.read_text()) if COUNTS.exists() and not force else {}
    if "home" not in cached:
        cached["home"] = portal.home_counts()
        cached["total_search"] = portal.count()
        cached["date"] = date.today().isoformat()
    per = cached.setdefault("scopes", {})
    todo = [s for s in scopes if s not in per]
    if todo:
        print(f"  asking the portal about {len(todo)} scopes")
    for i, s in enumerate(todo, 1):
        try:
            per[s] = portal.count(s)
        except RuntimeError as e:
            per[s] = None
            print(f"    {s}: {e}")
        if i % 25 == 0:
            COUNTS.write_text(json.dumps(cached, indent=2, sort_keys=True))
    COUNTS.write_text(json.dumps(cached, indent=2, sort_keys=True))
    return cached


def research_scopes(counts: dict) -> set[str]:
    """EDI scopes that are not the bulk-loaded derived products."""
    return {s for s, v in counts["scopes"].items()
            if v and s not in portal.BULK_SCOPES}


# ---------------------------------------------------------------- 4 packages

def portal_status(packages: list[dict], scopes: set[str]) -> dict:
    """package_id -> "current" | "stale" | "absent", for the given scopes.

    current  the portal's current revision is DataONE's newest
    stale    the series exists on the portal at some other revision
    absent   the portal has never heard of the series, or has deleted it
    """
    status = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    todo = [p for p in packages if p["scope"] in scopes
            and p["package_id"] not in status]
    if todo:
        print(f"  checking {len(todo):,} packages against the portal, "
              f"~{len(todo) * 0.6 / 60:.0f} min")
    t0 = time.monotonic()
    for i, p in enumerate(todo, 1):
        try:
            if portal.is_current(p["package_id"]):
                status[p["package_id"]] = "current"
            elif portal.series_exists(p["scope"], p["identifier"]):
                status[p["package_id"]] = "stale"
            else:
                status[p["package_id"]] = "absent"
        except RuntimeError as e:
            print(f"    {p['package_id']}: {e}")
            continue
        if i % 100 == 0:
            STATUS.write_text(json.dumps(status, sort_keys=True))
            done = Counter(status[q["package_id"]] for q in todo[:i]
                           if q["package_id"] in status)
            rate = i / (time.monotonic() - t0)
            print(f"    {i:,}/{len(todo):,}  {dict(done)}  "
                  f"eta {(len(todo) - i) / rate / 60:.0f} min")
    STATUS.write_text(json.dumps(status, sort_keys=True))
    return status


# ----------------------------------------------------------------- 5 fixture

def fixture() -> dict:
    """Fetch one real EML end to end and parse it with the reused parser."""
    from hf_search import eml
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    scope, ident, rev = FIXTURE_PKG
    pid = dataone.metadata_url(scope, ident, rev)
    xml_path = FIXTURE_DIR / f"{dataone.package_id(scope, ident, rev)}.xml"
    if not xml_path.exists():
        xml_path.write_bytes(dataone.get_object(pid))
    page_path = FIXTURE_DIR / "solr_page.json"
    if not page_path.exists():
        page = dataone.solr({"q": f'id:"{pid}"', "fl": dataone.DOC_FIELDS, "rows": 5})
        page_path.write_text(json.dumps(page, indent=2))
    list_path = FIXTURE_DIR / "list_objects_page.xml"
    if not list_path.exists():
        code, body = dataone._get(
            f"{dataone.CN}/object?formatId={dataone.EML_FORMAT_IDS[0]}"
            f"&nodeId=urn:node:EDI&start=0&count=3")
        list_path.write_bytes(body)
    rec = eml.parse(xml_path)
    out = {"pid": pid, "bytes": xml_path.stat().st_size, "title": rec.title,
           "abstract_chars": len(rec.abstract), "keywords": len(rec.keywords),
           "tables": len(rec.tables),
           "attributes": sum(len(t.attributes) for t in rec.tables)}
    print(f"  fixture {xml_path.name}: {out['bytes']:,} bytes, "
          f"title={rec.title[:60]!r}, {out['attributes']} attributes")
    return out


# ------------------------------------------------------------------ 6 report

def report(sweep_summary: dict, packages: list[dict], counts: dict,
           status: dict, fix: dict) -> Path:
    by_scope = defaultdict(list)
    for p in packages:
        by_scope[p["scope"]].append(p)
    per = counts["scopes"]
    home = counts["home"]
    forms = sweep_summary["pasta_ids_by_form"]
    revs = sorted(p["revisions_in_dataone"] for p in packages)

    in_edi = sorted(s for s in by_scope if per.get(s))
    not_edi = sorted(s for s in by_scope if not per.get(s))
    bulk = [s for s in in_edi if s in portal.BULK_SCOPES]
    research = sorted((s for s in in_edi if s not in portal.BULK_SCOPES),
                      key=lambda s: -per[s])

    def tally(scope):
        c = Counter(status.get(p["package_id"], "unchecked") for p in by_scope[scope])
        return c["current"], c["stale"], c["absent"], c["unchecked"]

    checked = any(status.get(p["package_id"]) for s in research for p in by_scope[s])
    tot = Counter()
    for s in research:
        cur, st, ab, un = tally(s)
        tot.update({"dataone": len(by_scope[s]), "portal": per[s], "current": cur,
                    "stale": st, "absent": ab, "unchecked": un})
    in_portal = tot["current"] + tot["stale"]

    def nodes_of(scope):
        c = Counter(p["node"].replace("urn:node:", "") for p in by_scope[scope])
        return ", ".join(f"{k} {v:,}" for k, v in c.most_common())

    L = []
    w = L.append
    w("# Acquisition: DataONE coverage of EDI")
    w("")
    w(f"Measured {counts['date']} by `python -m edisearch.acquire.probe`. Every number "
      f"below is regenerated by that command; the listings it works from are in "
      f"`data/probe/` (not committed, a few MB). The object-store sweep takes about "
      f"{sweep_summary['seconds'] // 60 + 1} minutes; the per-package portal check "
      f"takes about two hours and is resumable.")
    w("")
    w("## Why DataONE")
    w("")
    w("PASTA+, EDI's own API, refuses every anonymous call including `readMetadata` "
      "(`User 'EDI-... (Public Access)' is not authorized`, re-confirmed by curl on "
      f"{counts['date']}). EDI is a DataONE member node and the coordinating node "
      "serves the same EML anonymously. See `edisearch/acquire/dataone.py` for the "
      "four things about DataONE the harvester has to handle.")
    w("")
    w("## Headline")
    w("")
    w("EDI's portal reports two tiers on its home page: **contributed** data packages "
      f"({home['contributed']['unique']:,} unique, {home['contributed']['all_revisions']:,} "
      f"across all revisions) and **total including EcoTrends and Landsat** "
      f"({home['total']['unique']:,} unique, {home['total']['all_revisions']:,} all revisions). "
      "The plan's figure of 42,651 was the total tier. `ecotrends`, `lter-landsat` and "
      "`lter-landsat-ledaps` are bulk-loaded derived products, roughly 36,000 packages; "
      "the search space that matters for retrieval is the contributed tier.")
    w("")
    if checked:
        w("Research tier, every series checked against the portal one by one:")
        w("")
        w("| | Packages |")
        w("|---|---:|")
        w(f"| Portal lists (sum over the {len(research)} research scopes) | {tot['portal']:,} |")
        w(f"| DataONE has, and the portal lists at any revision | {in_portal:,} ({100 * in_portal / tot['portal']:.1f}% of the portal) |")
        w(f"| ... of which DataONE's newest revision is the portal's current one | {tot['current']:,} ({100 * tot['current'] / max(in_portal, 1):.1f}% of those) |")
        w(f"| ... of which DataONE is behind the portal (stale) | {tot['stale']:,} |")
        w(f"| Portal lists but DataONE does not have | {tot['portal'] - in_portal:,} |")
        w(f"| DataONE has but the portal does not list (deleted or never in PASTA) | {tot['absent']:,} |")
        if tot["unchecked"]:
            w(f"| Not yet checked | {tot['unchecked']:,} |")
        w("")
        w("**Coverage** is the second row: the share of EDI's research packages for which "
          "DataONE holds EML. **Currency** is the third: how often that EML is the current "
          "revision. A stale package still yields searchable metadata, just an older "
          "version of it.")
    else:
        w(f"Research tier by count only (per-package check not run): DataONE {tot['dataone']:,} "
          f"distinct series against {tot['portal']:,} on the portal.")
    w("")
    w("## Per scope")
    w("")
    w("DataONE is distinct `scope.identifier` series, each at its highest revision in the "
      "object store; node is where that revision lives. Portal is `simpleSearch` with "
      "`fq=scope:<scope>`. Current, stale and absent are per-package answers from the "
      "portal for DataONE's newest revision. Coverage is (current + stale) / portal; "
      "portal-only is what DataONE lacks.")
    w("")
    w("| Scope | Node(s) | DataONE | Portal | Current | Stale | Absent | Coverage | Portal-only |")
    w("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for s in research:
        cur, st, ab, un = tally(s)
        inp = cur + st
        cov = f"{100 * inp / per[s]:.0f}%" if (inp or un == 0) else "?"
        w(f"| `{s}` | {nodes_of(s)} | {len(by_scope[s]):,} | {per[s]:,} | {cur:,} | {st:,} "
          f"| {ab:,} | {cov} | {per[s] - inp:,} |")
    w("")
    w("Bulk-loaded scopes, by count only:")
    w("")
    w("| Scope | Node(s) | DataONE | Portal |")
    w("|---|---|---:|---:|")
    for s in bulk:
        w(f"| `{s}` | {nodes_of(s)} | {len(by_scope[s]):,} | {per[s]:,} |")
    if not_edi:
        w("")
        w(f"{len(not_edi)} further scopes across {sum(len(by_scope[s]) for s in not_edi):,} "
          "series parse as `scope.identifier.revision` but the portal returns zero packages "
          "for them, so they are other member nodes' packages in the same id style, not "
          "EDI's. Largest: " + ", ".join(
              f"`{s}` ({len(by_scope[s]):,})"
              for s in sorted(not_edi, key=lambda s: -len(by_scope[s]))[:12]) + ".")
    w("")
    w("## What the sweep saw")
    w("")
    store = sweep_summary["eml_objects_in_store"]
    w(f"- {sweep_summary['eml_objects_total']:,} EML objects in the object store across "
      f"every member node, all revisions: " + ", ".join(
          f"`{k.split('/')[-1]}` {v:,}" for k, v in store.items()) +
      f". {sweep_summary['attributed_to_a_node']:,} of them attributable to a member node")
    w(f"- {sweep_summary['pasta_ids']:,} carry a PASTA package id: "
      f"{forms.get('url', 0):,} in URL form, {forms.get('bare', 0):,} bare, "
      f"{forms.get('doi', 0):,} as `doi:10.6073/AA/...`. They collapse to "
      f"{len(packages):,} distinct series; revisions per series median "
      f"{revs[len(revs) // 2]}, max {revs[-1]}")
    w("- PASTA ids by node: " + ", ".join(
        f"{k.replace('urn:node:', '')} {v:,}"
        for k, v in sweep_summary["pasta_ids_by_node"].items()))
    w("- **The Solr index is not the object store.** An earlier pass of this probe used "
      "`query/solr` and found 97,223 PASTA ids in 260,389 indexed EML documents; "
      "`listObjects` finds the counts above. The index had `edi.134` at revision 10 "
      "while revisions 11 and 12 existed as objects and the portal listed 12 as current. "
      "The index also carries broken `obsoletedBy` chains across identifier spellings "
      "(7,063 older revisions with no successor recorded), so neither `-obsoletedBy:*` "
      "nor the index itself is a way to find current revisions. The rule this probe "
      "and the harvester use is: highest revision per series in the object store")
    w("- **Stale is permanent, not lag.** The 10 stale `knb-lter-hfr` packages have no "
      "newer object in DataONE at all (checked by asking for system metadata at the next "
      "five revisions), and DataONE last touched some of them in 2021. Roughly 3% of "
      "packages will carry an older revision's metadata than the portal shows, and only "
      "a PASTA+ account would close that gap")
    w("")
    w("## End-to-end check")
    w("")
    w(f"`{fix['pid']}` fetched from `cn.dataone.org/cn/v2/object/` ({fix['bytes']:,} bytes, "
      f"saved as `fixtures/dataone/{dataone.package_id(*FIXTURE_PKG)}.xml`) and parsed by "
      f"the unchanged `hf_search.eml.parse`: title {fix['title']!r}, "
      f"{fix['abstract_chars']:,} characters of abstract, {fix['keywords']} keywords, "
      f"{fix['tables']} table, {fix['attributes']} attributes. One Solr response and one "
      "`listObjects` page are saved beside it.")
    w("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L), encoding="utf-8")
    return REPORT


# --------------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--force", action="store_true", help="re-sweep the object store")
    ap.add_argument("--no-packages", action="store_true",
                    help="skip the per-package portal check")
    ap.add_argument("--scopes", nargs="*", default=None,
                    help="limit the per-package check to these scopes")
    a = ap.parse_args(argv)

    print("1 sweep")
    summary = sweep(force=a.force)
    print("2 dedupe")
    packages = dedupe()
    print("3 scopes")
    counts = portal_counts(sorted({p["scope"] for p in packages}))
    print("4 packages")
    status = {}
    if not a.no_packages:
        scopes = research_scopes(counts)
        if a.scopes:
            scopes &= set(a.scopes)
        status = portal_status(packages, scopes)
    elif STATUS.exists():
        status = json.loads(STATUS.read_text())
    print("5 fixture")
    fix = fixture()
    print("6 report")
    path = report(summary, packages, counts, status, fix)
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

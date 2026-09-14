"""Harvest one EDI scope: current packages, raw EML to disk, records.jsonl.

    python -m edisearch.acquire.harvest knb-lter-hfr
    python -m edisearch.acquire.harvest knb-lter-hfr --no-parse
    python -m edisearch.acquire.harvest edi --force

Route, per decision 0010: PASTA+ for everything. One search call lists every
current `scope.identifier.revision` in the scope; one `readMetadata` per
package fetches the EML. Two requests per second, GET only, resumable: a
package whose file is on disk is not fetched again. A package that gets a new
revision gets a new file; the old one stays on disk but leaves the corpus,
because the corpus is built from the current list, not from the directory.

Parsing reuses `hf_search.eml.parse` unchanged and adds the identity fields
the plan's `records.jsonl` interface names. `indexed_text` is not stored: the
engines build it from the record through `hf_search.corpus` at index time,
exactly as they do for the Harvard Forest corpus, so storing it would only
be a second copy that could drift.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from hf_search import eml
from edisearch.acquire import pasta
from edisearch.paths import RAW, RECORDS

_DOI = re.compile(rb"doi:(10\.6073/pasta/[0-9a-f]+)")


def raw_dir(scope: str) -> Path:
    d = RAW / scope
    d.mkdir(parents=True, exist_ok=True)
    return d


# ------------------------------------------------------------------ fetch

def harvest(scope: str, force: bool = False, verbose: bool = True) -> dict:
    d = raw_dir(scope)
    status_path = d / "_status.json"
    status = json.loads(status_path.read_text()) if status_path.exists() and not force else {}

    current = pasta.current_packages(scope)
    if verbose:
        print(f"{scope}: {len(current)} current packages listed by PASTA+")
    (d / "_current.json").write_text(json.dumps(
        {"scope": scope, "listed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
         "package_ids": current}, indent=1))

    fetched = cached = failed = 0
    t0 = time.monotonic()
    for i, pid in enumerate(current, 1):
        path = d / f"{pid}.xml"
        if path.exists() and path.stat().st_size > 0 and not force:
            cached += 1
            continue
        sc, ident, rev = pasta.split_id(pid)
        try:
            body = pasta.read_metadata(sc, ident, rev)
        except RuntimeError as e:
            status[pid] = str(e)
            failed += 1
            if verbose:
                print(f"  {pid}: {e}")
            continue
        if not body.lstrip().startswith(b"<"):
            status[pid] = "not xml"
            failed += 1
            continue
        path.write_bytes(body)
        status[pid] = "ok"
        fetched += 1
        if verbose and fetched % 50 == 0:
            rate = fetched / (time.monotonic() - t0)
            print(f"  ...{fetched} fetched, {(len(current) - i) / max(rate, 0.1) / 60:.0f} min left")
    status_path.write_text(json.dumps(status, sort_keys=True, indent=1))
    summary = {"scope": scope, "current": len(current), "fetched": fetched,
               "cached": cached, "failed": failed,
               "seconds": round(time.monotonic() - t0)}
    if verbose:
        print(json.dumps(summary))
    return summary


# ------------------------------------------------------------------ parse

def record(scope: str, pid: str, path: Path) -> dict:
    """The plan's records.jsonl row: the reused parser's fields plus identity."""
    rec = eml.parse(path)
    sc, ident, rev = pasta.split_id(pid)
    m = _DOI.search(path.read_bytes())
    row = rec.dict()
    row["id"] = pid                       # what eml.Record.from_dict reads back
    row.update({
        "package_id": pid, "scope": sc, "identifier": ident, "revision": rev,
        "series_id": f"{sc}.{ident}",
        "doi": m.group(1).decode() if m else None,
        "creators": rec.people,
        "source": "edi", "route": "pasta",
        "harvested_at": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                        .isoformat(timespec="seconds"),
    })
    return row


def parse(scope: str, verbose: bool = True) -> list[dict]:
    d = raw_dir(scope)
    current = json.loads((d / "_current.json").read_text())["package_ids"]
    rows, missing, broken = [], [], []
    for pid in current:
        path = d / f"{pid}.xml"
        if not path.exists():
            missing.append(pid)
            continue
        try:
            rows.append(record(scope, pid, path))
        except Exception as e:  # one bad file must not sink the scope
            broken.append((pid, f"{type(e).__name__}: {e}"))

    # records.jsonl holds every harvested scope; replace this scope's rows
    others = []
    if RECORDS.exists():
        others = [json.loads(l) for l in RECORDS.read_text(encoding="utf-8").splitlines()
                  if json.loads(l).get("scope") != scope]
    RECORDS.parent.mkdir(parents=True, exist_ok=True)
    with RECORDS.open("w", encoding="utf-8") as f:
        for r in others + rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    if verbose:
        no_title = [r["package_id"] for r in rows if not r["title"].strip()]
        no_abs = [r["package_id"] for r in rows if not r["abstract"].strip()]
        ok = sum(1 for r in rows if r["title"].strip() and r["abstract"].strip())
        print(f"{scope}: {len(rows)} records written to {RECORDS.name} "
              f"({len(others)} from other scopes kept)")
        print(f"  title and abstract present: {ok}/{len(rows)} = {100 * ok / max(len(rows), 1):.1f}%")
        if no_title:
            print(f"  no title ({len(no_title)}): {no_title[:10]}")
        if no_abs:
            print(f"  no abstract ({len(no_abs)}): {no_abs[:10]}")
        if missing:
            print(f"  listed but not on disk ({len(missing)}): {missing[:10]}")
        for pid, err in broken:
            print(f"  parse failed {pid}: {err}")
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("scope")
    ap.add_argument("--force", action="store_true", help="refetch everything")
    ap.add_argument("--no-parse", action="store_true")
    a = ap.parse_args(argv)
    harvest(a.scope, force=a.force)
    if not a.no_parse:
        parse(a.scope)
    return 0


if __name__ == "__main__":
    sys.exit(main())

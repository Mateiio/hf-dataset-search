"""Fetch the Harvard Forest EML corpus.

`data/records.json` ships with the repo already parsed, so you only need this to
verify the corpus independently or to pick up datasets added since.

Polite by construction: cached, resumable, throttled to ~2 requests/second. This
is a small research station's web server, not a CDN. All Harvard Forest data is
CC0.

    python -m hf_search.harvest              fetch missing, then reparse
    python -m hf_search.harvest --lo 1 --hi 500
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request

from hf_search import eml
from hf_search.paths import EML_CACHE, RECORDS

# harvardforest.fas... 302s to harvardforest1.fas...; go straight to the target.
URL = "https://harvardforest1.fas.harvard.edu/data/eml/{ds}.xml"
UA = ("hf-dataset-search/1.0 (research metadata index; "
      "contact via harvardforest.fas.harvard.edu)")
THROTTLE_S = 0.5
STATUS = EML_CACHE / "_status.json"


def _get(url: str, timeout: int = 60) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except (urllib.error.URLError, TimeoutError) as e:
        return 0, str(e).encode()


def harvest(lo: int = 1, hi: int = 500, force: bool = False,
            verbose: bool = True) -> dict:
    EML_CACHE.mkdir(parents=True, exist_ok=True)
    status = {}
    if STATUS.exists() and not force:
        status = json.loads(STATUS.read_text())

    found = skipped = missing = failed = 0
    for n in range(lo, hi + 1):
        ds = f"hf{n:03d}"
        path = EML_CACHE / f"{ds}.xml"
        if path.exists() and path.stat().st_size > 0 and not force:
            skipped += 1
            continue
        if status.get(ds) == 404 and not force:
            missing += 1
            continue

        code, body = _get(URL.format(ds=ds))
        status[ds] = code
        if code == 200 and body.lstrip().startswith(b"<"):
            path.write_bytes(body)
            found += 1
            if verbose and found % 25 == 0:
                print(f"  ...{found} fetched (at {ds})")
        elif code == 404:
            missing += 1
        else:
            failed += 1
            if verbose:
                print(f"  {ds}: HTTP {code}")
        time.sleep(THROTTLE_S)

    STATUS.write_text(json.dumps(status, sort_keys=True))
    summary = {"fetched": found, "cached": skipped, "not_present": missing,
               "errors": failed,
               "total_on_disk": len(list(EML_CACHE.glob("hf*.xml")))}
    if verbose:
        print(json.dumps(summary, indent=2))
        # Gaps must be explicit: a dataset that is quietly absent looks
        # identical to one that was never checked.
        bad = sorted(d for d, c in status.items() if c not in (200, 404))
        if bad:
            print(f"non-404 failures ({len(bad)}): {bad[:20]}")
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lo", type=int, default=1)
    ap.add_argument("--hi", type=int, default=500)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-parse", action="store_true")
    a = ap.parse_args()

    harvest(a.lo, a.hi, a.force)
    if not a.no_parse:
        recs = eml.parse_dir(EML_CACHE)
        eml.write_json(recs, RECORDS)
        print(f"wrote {RECORDS} ({RECORDS.stat().st_size / 1e6:.1f} MB, "
              f"{len(recs)} datasets)")
        print("\nNext: python -m hf_search.semantic --build")

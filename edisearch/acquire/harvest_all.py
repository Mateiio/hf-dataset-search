"""M7: harvest every research scope in EDI's contributed tier.

    python -m edisearch.acquire.harvest_all
    python -m edisearch.acquire.harvest_all --only edi knb-lter-arc

The scope list is the 37 the portal counts as contributed (M0's
`data/probe/portal_counts.json`, every scope with a nonzero count that is not
one of the three bulk-loaded ones). Each scope goes through `harvest.py` in
turn, so the run is resumable at package granularity and one bad scope does
not stop the rest. At two requests per second the tier is about 90 minutes.
"""

from __future__ import annotations

import argparse
import json
import sys
import time

from edisearch.acquire import harvest, portal
from edisearch.paths import PROBE

COUNTS = PROBE / "portal_counts.json"


def research_scopes() -> list[str]:
    counts = json.loads(COUNTS.read_text(encoding="utf-8"))["scopes"]
    return sorted((s for s, n in counts.items() if n and s not in portal.BULK_SCOPES),
                  key=lambda s: -counts[s])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--skip", nargs="*", default=["knb-lter-hfr"])
    a = ap.parse_args(argv)
    scopes = a.only or [s for s in research_scopes() if s not in (a.skip or [])]
    print(f"{len(scopes)} scopes: {' '.join(scopes)}")
    t0 = time.monotonic()
    totals = {"current": 0, "fetched": 0, "cached": 0, "failed": 0}
    for i, scope in enumerate(scopes, 1):
        print(f"\n[{i}/{len(scopes)}] {scope}  ({(time.monotonic() - t0) / 60:.0f} min elapsed)")
        try:
            s = harvest.harvest(scope)
            harvest.parse(scope)
        except Exception as e:  # noqa: BLE001 -- keep going, report at the end
            print(f"  {scope} FAILED: {type(e).__name__}: {e}")
            continue
        for k in totals:
            totals[k] += s[k]
    print(f"\ndone in {(time.monotonic() - t0) / 60:.0f} min: {json.dumps(totals)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

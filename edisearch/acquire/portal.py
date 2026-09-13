"""EDI's data portal, anonymous, for counts and cross-checks only.

`portal.edirepository.org/nis/simpleSearch` answers anonymously and passes
edismax `q` and `fq` through to PASTA's Solr, but returns HTML, not JSON. It is
a web page, not an API, so this module asks it two narrow questions and no
more than counts. Anonymous requests get the result count but every row
comes back empty (`data-package-id=""`; the CSV download is 460 blank lines for
a 459-package scope), so it cannot *list* packages. It can answer yes/no
questions one package at a time, though: `fq=packageid:scope.id.rev` returns
1 when that exact revision is the portal's current one, and
`fq=id:scope.identifier` returns 1 when the series exists at any revision
(two `fq` parameters at once are a server error, so it is one filter each).
Together those measure, per package, whether DataONE has it and whether
DataONE's newest revision is EDI's newest revision. Not a harvest route: the
metadata viewer redirects anonymous requests to a login page.

Two tiers of "how many packages EDI has" exist and the home page shows both:
"contributed" (research data packages) and "total including EcoTrends and
Landsat" (bulk-loaded derived products under `ecotrends`, `lter-landsat` and
`lter-landsat-ledaps`, ~36,000 packages). The plan's 42,651 was the total tier.
The search space that matters for retrieval is the contributed tier.
"""

from __future__ import annotations

import re
import urllib.parse

from edisearch.acquire.dataone import _get  # same throttle, same user agent

SEARCH = "https://portal.edirepository.org/nis/simpleSearch"
HOME = "https://portal.edirepository.org/nis/home.jsp"

BULK_SCOPES = ("ecotrends", "lter-landsat", "lter-landsat-ledaps")

_COUNT = re.compile(r"of\s+([\d,]+)\s+matching data packages?|"
                    r"([\d,]+)\s+matching data packages?")
_NONE = "No matching data packages were found."
_HOME = re.compile(
    r"<b>(Contributed|Total) Data Packages</b>[^U]*"
    r"Unique:&nbsp;<b>(\d+)</b>;&nbsp;All Revisions:&nbsp;<b>(\d+)</b>")


def _search(fq: list[str], rows: int = 0, start: int = 0) -> str:
    params = [("defType", "edismax"), ("q", "*:*"), ("rows", rows),
              ("start", start)] + [("fq", f) for f in fq]
    code, body = _get(f"{SEARCH}?{urllib.parse.urlencode(params)}")
    if code != 200:
        raise RuntimeError(f"portal HTTP {code} for fq={fq!r}")
    return body.decode("utf-8", "replace")


def _count(fq: list[str]) -> int:
    html = _search(fq)
    if _NONE in html:
        return 0
    m = _COUNT.search(html)
    if not m:
        raise RuntimeError(f"count not found in portal HTML for fq={fq!r}")
    return int((m.group(1) or m.group(2)).replace(",", ""))


def count(scope: str | None = None) -> int:
    """Packages the portal lists for a scope; all of EDI if scope is None."""
    return _count([f"scope:{scope}"] if scope else [])


def is_current(package_id: str) -> bool:
    """True if `scope.identifier.revision` is the portal's current revision."""
    return _count([f"packageid:{package_id}"]) == 1


def series_exists(scope: str, identifier: int) -> bool:
    """True if the portal lists the series at any revision."""
    return _count([f"id:{scope}.{identifier}"]) == 1



def home_counts() -> dict:
    """The two tiers the home page reports, unique and all-revisions."""
    code, body = _get(HOME)
    if code != 200:
        raise RuntimeError(f"portal home HTTP {code}")
    out = {}
    for tier, unique, allrev in _HOME.findall(body.decode("utf-8", "replace")):
        out[tier.lower()] = {"unique": int(unique), "all_revisions": int(allrev)}
    return out

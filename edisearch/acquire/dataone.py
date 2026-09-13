"""DataONE client: search the index, fetch objects, normalise PASTA ids.

Why DataONE and not EDI's own API. PASTA+ at pasta.lternet.edu refuses every
anonymous call this project needs, `readMetadata` included, answering
`User 'EDI-... (Public Access)' is not authorized`. Verified in a browser
2026-09-06 and again by curl 2026-09-13. EDI is a DataONE member node, and the
coordinating node serves the same EML anonymously through a documented API.
The EML itself declares `<principal>public</principal>`, so nothing is being
worked around here; it is the route the material is meant to be read through.

Three facts about the index that every caller must respect, all observed:

- EML formatIds come in two spellings. 2.1.x is `eml://ecoinformatics.org/...`,
  2.2.0 is `https://eml.ecoinformatics.org/...`. `formatId:eml*` misses every
  2.2.0 document. Use `formatId:*eml*`.
- Every revision is retained. Obsolescence chains are supposed to link them,
  but the chains break across identifier spellings (below), so `-obsoletedBy:*`
  is NOT a reliable "current revision" filter. `knb-lter-hfr.116.11` carries no
  `obsoletedBy` while `.../knb-lter-hfr/116/16` exists. The reliable rule is:
  normalise, group by series, take the highest revision.
- The same package appears under three identifier forms depending on era:
  the PASTA metadata URL for recent revisions, bare `scope.identifier.revision`
  for older ones, `doi:10.6073/AA/scope.identifier.revision` for the oldest.
- **The Solr index is incomplete.** It holds about two thirds of the EML
  objects the coordinating node actually stores (29,947 indexed against 79,609
  stored for EML 2.2.0 on 2026-09-13), and lags by months: `edi.134` was
  indexed to revision 10 while revisions 11 and 12 existed as objects. Use
  `listObjects` (`iter_objects` below), which reads the object store, to
  enumerate; use Solr only for fields the object list lacks.

Stdlib only. Throttled to 2 requests per second regardless of what anyone's
documentation says about limits; the coordinating node is shared infrastructure.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Iterator

from edisearch.paths import USER_AGENT

CN = "https://cn.dataone.org/cn/v2"
THROTTLE_S = 0.5
EML_FORMATS = "formatId:*eml*"

# Fields worth carrying out of the index for every EML document.
DOC_FIELDS = "id,formatId,datasource,obsoletedBy,obsoletes,dateUploaded,size"

_last_request = 0.0


def _throttle() -> None:
    global _last_request
    wait = THROTTLE_S - (time.monotonic() - _last_request)
    if wait > 0:
        time.sleep(wait)
    _last_request = time.monotonic()


def _get(url: str, timeout: int = 120, retries: int = 3) -> tuple[int, bytes]:
    """One GET, throttled, with a short retry on transient failure.

    Returns (status, body). A status of 0 means the request never got an HTTP
    answer; the body then holds the error text.
    """
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        _throttle()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return e.code, e.read() if e.fp else b""
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return 0, str(e).encode()
    return 0, b"unreachable"


# ---------------------------------------------------------------- Solr search

def solr(params: dict) -> dict:
    """One page of the coordinating node's Solr index, as parsed JSON."""
    qs = urllib.parse.urlencode({**params, "wt": "json"}, doseq=True)
    code, body = _get(f"{CN}/query/solr/?{qs}")
    if code != 200:
        raise RuntimeError(f"solr HTTP {code}: {body[:200]!r}")
    return json.loads(body)


def count(q: str, fq: list[str] = ()) -> int:
    return solr({"q": q, "fq": list(fq), "rows": 0})["response"]["numFound"]


def iter_solr(q: str, fq: list[str] = (), fl: str = DOC_FIELDS,
              rows: int = 1000, verbose: bool = True) -> Iterator[dict]:
    """Every document matching the query, via cursorMark paging.

    Deep `start=` paging degrades past a few tens of thousands of rows;
    cursorMark does not, and the index supports it (checked 2026-09-13).
    """
    cursor, seen = "*", 0
    while True:
        page = solr({"q": q, "fq": list(fq), "fl": fl, "rows": rows,
                     "sort": "id asc", "cursorMark": cursor})
        docs = page["response"]["docs"]
        yield from docs
        seen += len(docs)
        if verbose and seen % 20000 < rows:
            print(f"  ...{seen:,} of {page['response']['numFound']:,}")
        nxt = page.get("nextCursorMark")
        if not docs or nxt == cursor:
            return
        cursor = nxt


# ------------------------------------------------------------- object list

# The five EML versions PASTA has ever published. DataONE also registers the
# 2.0.0beta4/beta6 *module* formats (eml-dataset, eml-attribute, ...), which
# are pre-2.0 Metacat fragments PASTA never used; they are left out on purpose.
EML_FORMAT_IDS = (
    "https://eml.ecoinformatics.org/eml-2.2.0",
    "eml://ecoinformatics.org/eml-2.1.1",
    "eml://ecoinformatics.org/eml-2.1.0",
    "eml://ecoinformatics.org/eml-2.0.1",
    "eml://ecoinformatics.org/eml-2.0.0",
)


def list_nodes() -> list[str]:
    """Every member node id the coordinating node knows, CNs excluded."""
    code, body = _get(f"{CN}/node")
    if code != 200:
        raise RuntimeError(f"node list HTTP {code}")
    ids = re.findall(r"<identifier>(urn:node:[A-Za-z0-9_]+)</identifier>",
                     body.decode("utf-8", "replace"))
    return [n for n in dict.fromkeys(ids) if not n.startswith("urn:node:CN")
            and n not in ("urn:node:mnORC1", "urn:node:mnUNM1", "urn:node:mnUCSB1")]


def count_objects(format_id: str, node_id: str | None = None) -> int:
    params = {"formatId": format_id, "start": 0, "count": 0}
    if node_id:
        params["nodeId"] = node_id
    code, body = _get(f"{CN}/object?{urllib.parse.urlencode(params)}")
    if code != 200:
        raise RuntimeError(f"listObjects HTTP {code}: {body[:200]!r}")
    m = re.search(rb'total="(\d+)"', body)
    return int(m.group(1)) if m else 0


_OBJ = re.compile(
    r"<objectInfo>\s*<identifier>(.*?)</identifier>\s*<formatId>(.*?)</formatId>"
    r".*?<dateSysMetadataModified>(.*?)</dateSysMetadataModified>\s*<size>(\d+)</size>",
    re.S)


def iter_objects(format_id: str, node_id: str | None = None,
                 count: int = 5000) -> Iterator[dict]:
    """Every object of one format (and optionally one node) in the object store.

    `listObjects` pages by offset and accepts 5,000 per page (checked
    2026-09-13). Unlike Solr it carries no `obsoletedBy` or `datasource`; the
    node comes from asking per node, and "current" is the highest revision.
    """
    start = 0
    while True:
        params = {"formatId": format_id, "start": start, "count": count}
        if node_id:
            params["nodeId"] = node_id
        code, body = _get(f"{CN}/object?{urllib.parse.urlencode(params)}")
        if code != 200:
            raise RuntimeError(f"listObjects HTTP {code}: {body[:200]!r}")
        text = body.decode("utf-8", "replace")
        n = 0
        for pid, fmt, modified, size in _OBJ.findall(text):
            n += 1
            yield {"id": pid.strip(), "formatId": fmt.strip(),
                   "dateSysMetadataModified": modified.strip(),
                   "size": int(size), "datasource": node_id}
        if n < count:
            return
        start += count


# --------------------------------------------------------------- object fetch

def get_object(pid: str) -> bytes:
    """The bytes of one object. For EML pids that is the XML document."""
    code, body = _get(f"{CN}/object/{urllib.parse.quote(pid, safe='')}")
    if code != 200:
        raise RuntimeError(f"object {pid}: HTTP {code}: {body[:200]!r}")
    return body


# -------------------------------------------------------------- PASTA ids

# The three spellings, oldest era last. `pasta-d`/`pasta-s` are EDI's
# development and staging hosts; they should not appear in production DataONE
# but the pattern tolerates them so they get counted rather than silently
# dropped if they do.
_URL = re.compile(
    r"^https?://pasta(?:-[a-z]+)?\.lternet\.edu/package/metadata/eml/"
    r"([A-Za-z][A-Za-z0-9_-]*)/(\d+)/(\d+)/?$")
_DOI = re.compile(r"^doi:10\.6073/AA/([A-Za-z][A-Za-z0-9_-]*)\.(\d+)\.(\d+)$")
_BARE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*)\.(\d+)\.(\d+)$")


def parse_pid(pid: str) -> tuple[str, str, int, int] | None:
    """(form, scope, identifier, revision), or None if not a PASTA package id.

    `form` is "url", "doi" or "bare". The bare form is ambiguous on its own --
    KNB and other member nodes use `scope.id.rev` too -- so callers that need
    EDI membership must check the scope against EDI's portal, not the shape.
    """
    for form, rx in (("url", _URL), ("doi", _DOI), ("bare", _BARE)):
        m = rx.match(pid.strip())
        if m:
            return form, m.group(1).lower(), int(m.group(2)), int(m.group(3))
    return None


def package_id(scope: str, identifier: int, revision: int) -> str:
    return f"{scope}.{identifier}.{revision}"


def metadata_url(scope: str, identifier: int, revision: int) -> str:
    """The URL-form pid, which is also what current revisions are indexed as."""
    return (f"https://pasta.lternet.edu/package/metadata/eml/"
            f"{scope}/{identifier}/{revision}")

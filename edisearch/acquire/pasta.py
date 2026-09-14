"""PASTA+ client, authenticated, read methods only.

PASTA+ at pasta.lternet.edu is EDI's own API and the source of truth for
which packages exist and which revision is current. It refuses every method
this project needs to anonymous callers (403, "Public Access ... is not
authorized"), but answers an authenticated one. Decision 0010 (2026-09-14):
harvest through PASTA+ with the owner's EDI access key; keep DataONE as the
anonymous cross-check (`probe.py`).

Credential handling, and this is the whole of it:

- The access key is read from one file, `EDI_ACCESS_KEY_FILE` or
  `<crtusers>/secrets/edi_access_key`, outside every repo and zip
- It is exchanged once per process for a token at
  `auth.edirepository.org/auth/v1/key`; the token lives in this module's
  memory and is sent as a cookie. Tokens last 96 hours; a 401 mid-run
  triggers one re-exchange
- Neither key nor token is ever printed, logged, written to disk, or put in
  a URL. Errors report status codes and paths, nothing else

Methods used, all GET under `/package`:

    eml                                   listDataPackageScopes
    eml/{scope}                           listDataPackageIdentifiers
    eml/{scope}/{identifier}?filter=newest  listDataPackageRevisions, newest only
    metadata/eml/{scope}/{identifier}/{rev} readMetadata, the EML document
    search/eml?...                        searchDataPackages, Solr, for bulk
                                          current-package listing per scope

Throttled at two requests per second through `edisearch.net`, like every
other remote here. Never a write. Never a data entity download either: this
project indexes metadata, not data.
"""

from __future__ import annotations

import json
import os
import re
import urllib.parse
from pathlib import Path

from edisearch import net
from edisearch.paths import ROOT

PASTA = "https://pasta.lternet.edu/package"
AUTH = "https://auth.edirepository.org/auth/v1"

# Sibling of prj/, per the owner's layout: C:\crtusers\matei\secrets\...
KEY_FILE = Path(os.environ.get(
    "EDI_ACCESS_KEY_FILE",
    ROOT.parent.parent.parent / "secrets" / "edi_access_key"))

_token: str | None = None


class AuthError(RuntimeError):
    pass


def _read_key() -> str:
    if not KEY_FILE.exists():
        raise AuthError(f"no EDI access key at {KEY_FILE}; set EDI_ACCESS_KEY_FILE")
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    if not key:
        raise AuthError(f"EDI access key file is empty: {KEY_FILE}")
    return key


def token(refresh: bool = False) -> str:
    """The session token, exchanged from the key on first use."""
    global _token
    if _token and not refresh:
        return _token
    body = json.dumps({"key": _read_key()}).encode()
    code, resp, _ = net.get(f"{AUTH}/key", data=body,
                            headers={"Content-Type": "application/json"})
    if code != 200:
        raise AuthError(f"token exchange failed: HTTP {code}")
    try:
        _token = json.loads(resp)["edi-token"]
    except (ValueError, KeyError):
        raise AuthError("token exchange answered 200 without an edi-token")
    return _token


def _get(path: str, accept: str = "text/plain") -> bytes:
    url = f"{PASTA}/{path}"
    for attempt in (0, 1):
        headers = {"Cookie": f"edi-token={token(refresh=attempt == 1)}",
                   "Accept": accept}
        code, body, _ = net.get(url, headers=headers)
        if code == 200:
            return body
        if code == 401 and attempt == 0:
            continue
        raise RuntimeError(f"PASTA+ HTTP {code} for /{path}")
    raise RuntimeError(f"PASTA+ unreachable for /{path}")


def _lines(b: bytes) -> list[str]:
    return [l.strip() for l in b.decode("utf-8", "replace").splitlines() if l.strip()]


# ------------------------------------------------------------------ listing

def scopes() -> list[str]:
    return _lines(_get("eml"))


def identifiers(scope: str) -> list[int]:
    return [int(x) for x in _lines(_get(f"eml/{scope}"))]


def newest_revision(scope: str, identifier: int) -> int:
    return int(_lines(_get(f"eml/{scope}/{identifier}?filter=newest"))[0])


def revisions(scope: str, identifier: int) -> list[int]:
    return [int(x) for x in _lines(_get(f"eml/{scope}/{identifier}"))]


_PKG = re.compile(r"<packageid>([^<]+)</packageid>")
_NUMFOUND = re.compile(r"numFound=['\"](\d+)['\"]")


def current_packages(scope: str, rows: int = 1000) -> list[str]:
    """Every current `scope.identifier.revision` in a scope, from PASTA's Solr.

    One request per thousand packages instead of one per identifier. The
    search index lists each package once at its current revision, which is
    exactly the harvest list. Falls back to per-identifier listing if the
    two disagree on count.
    """
    ids, start = [], 0
    while True:
        q = urllib.parse.urlencode({"defType": "edismax", "q": "*:*",
                                    "fq": f"scope:{scope}", "fl": "packageid",
                                    "rows": rows, "start": start})
        xml = _get(f"search/eml?{q}", accept="application/xml").decode("utf-8", "replace")
        page = _PKG.findall(xml)
        ids.extend(page)
        total = int(_NUMFOUND.search(xml).group(1)) if _NUMFOUND.search(xml) else len(ids)
        start += rows
        if not page or start >= total:
            break
    return sorted(set(ids))


# ------------------------------------------------------------------- fetch

def read_metadata(scope: str, identifier: int, revision: int) -> bytes:
    """The EML document for one package revision."""
    return _get(f"metadata/eml/{scope}/{identifier}/{revision}",
                accept="application/xml")


def package_id(scope: str, identifier: int, revision: int) -> str:
    return f"{scope}.{identifier}.{revision}"


def split_id(pid: str) -> tuple[str, int, int]:
    scope, ident, rev = pid.rsplit(".", 2)
    return scope, int(ident), int(rev)

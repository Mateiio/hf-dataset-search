"""One throttled GET for every remote this package talks to.

Two requests per second per host, regardless of what any documentation says
about limits. Every host here is shared research infrastructure: DataONE's
coordinating node, EDI's portal, DataCite, OpenAlex, Europe PMC, publishers.
Short exponential retry on transient failures, none on 403/404.
"""

from __future__ import annotations

import time
import urllib.error
import urllib.parse
import urllib.request

from edisearch.paths import USER_AGENT

THROTTLE_S = 0.5
_last: dict[str, float] = {}


def _throttle(host: str) -> None:
    wait = THROTTLE_S - (time.monotonic() - _last.get(host, 0.0))
    if wait > 0:
        time.sleep(wait)
    _last[host] = time.monotonic()


def get(url: str, headers: dict | None = None, timeout: int = 120,
        retries: int = 3, data: bytes | None = None) -> tuple[int, bytes, str]:
    """(status, body, final_url). Status 0 means no HTTP answer; body is the error.

    With `data` it is a POST. Headers are never logged here or anywhere else in
    this package: the PASTA+ client puts a credential in one.
    """
    host = urllib.parse.urlsplit(url).netloc
    req = urllib.request.Request(url, data=data,
                                 headers={"User-Agent": USER_AGENT, **(headers or {})})
    for attempt in range(retries):
        _throttle(host)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read(), r.geturl()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return e.code, e.read() if e.fp else b"", url
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return 0, str(e).encode(), url
    return 0, b"unreachable", url

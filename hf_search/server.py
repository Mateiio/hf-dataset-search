"""The search bar. Stdlib http.server -- no framework, no build step.

    python -m hf_search.server          ->  http://localhost:8000

Serves web/index.html and two JSON endpoints:

    GET /api/search?q=<query>&mode=hybrid|semantic|lexical&k=10
    GET /api/trace?q=<query>&mode=...&k=10       (server-sent events)

`/api/trace` runs the identical search but streams one event per pipeline
stage as it happens -- plan, start, end, ..., done -- so the page can draw a
progress bar that tracks the real code rather than a spinner. The results
arrive in the final `done` event.

All three engines are built once at startup (a couple of seconds) and held in
memory, so a query is an embedding call plus a matrix multiply.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import numpy as np

from hf_search import corpus, ollama
from hf_search.hybrid import get_engine
from hf_search.paths import WEB
from hf_search.trace import Tracer, intake

_ENGINES: dict = {}
_RECORDS: list = []


def _load_engines(verbose: bool = True) -> None:
    global _RECORDS
    t0 = time.perf_counter()
    _RECORDS = corpus.load(verbose=False)
    _ENGINES["lexical"] = get_engine("lexical", _RECORDS)
    _ENGINES["semantic"] = get_engine("semantic", _RECORDS)
    # Reuse the two already built rather than constructing them twice.
    from hf_search.hybrid import HybridIndex
    _ENGINES["hybrid"] = HybridIndex(semantic=_ENGINES["semantic"],
                                     lexical=_ENGINES["lexical"],
                                     records=_RECORDS)
    if verbose:
        print(f"loaded {len(_RECORDS)} datasets and 3 engines in "
              f"{time.perf_counter() - t0:.1f}s")


def _results(hits) -> list:
    by_id = {r.id: r for r in _RECORDS}
    results = []
    for h in hits:
        rec = by_id.get(h.dataset)
        results.append({
            "id": h.dataset,
            "title": h.title,
            "score": round(h.score, 4),
            "why": h.why,
            "abstract": (rec.abstract[:280] + "...") if rec else "",
            "temporal": (rec.temporal if rec else {}),
            "n_tables": len(rec.tables) if rec else 0,
            "url": f"https://harvardforest.fas.harvard.edu/exist/apps/"
                   f"datasets/showData.html?id={h.dataset}",
        })
    return results


def _jsonable(o):
    """numpy scalars sneak into trace facts; JSON does not know them."""
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError(f"not serialisable: {type(o).__name__}")


class Handler(BaseHTTPRequestHandler):
    # 1.1 so a streamed trace can be close-delimited without confusing the
    # client; every other response carries a Content-Length as before.
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):                # quieter console
        if "/api/" in (args[0] if args else ""):
            super().log_message(fmt, *args)

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, obj) -> None:
        self._send(code, json.dumps(obj).encode(), "application/json")

    def _query(self, parsed):
        qs = urllib.parse.parse_qs(parsed.query)
        q = (qs.get("q") or [""])[0].strip()
        mode = (qs.get("mode") or ["hybrid"])[0]
        k = int((qs.get("k") or ["10"])[0])
        if not q:
            return None, self._json(400, {"error": "empty query"})
        if mode not in _ENGINES:
            return None, self._json(400, {"error": f"unknown mode {mode}"})
        return (q, mode, k), None

    def do_GET(self):                                  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path in ("/", "/index.html"):
            page = WEB / "index.html"
            if not page.exists():
                return self._json(500, {"error": f"missing {page}"})
            return self._send(200, page.read_bytes(), "text/html; charset=utf-8")

        if parsed.path == "/api/status":
            return self._json(200, {
                "datasets": len(_RECORDS),
                "ollama": ollama.available(),
                "model_pulled": ollama.has_model(),
            })

        if parsed.path == "/api/search":
            args, _ = self._query(parsed)
            if args is None:
                return
            q, mode, k = args
            t0 = time.perf_counter()
            try:
                hits = _ENGINES[mode].search(q, k=k)
            except ollama.OllamaUnavailable as e:
                # Lexical needs no model, so say so rather than just failing.
                return self._json(503, {"error": str(e),
                                        "hint": "mode=lexical works offline"})
            except Exception as e:                     # noqa: BLE001
                return self._json(500, {"error": str(e)[:300]})
            return self._json(200, {
                "query": q, "mode": mode,
                "ms": round((time.perf_counter() - t0) * 1000),
                "results": _results(hits),
            })

        if parsed.path == "/api/trace":
            args, _ = self._query(parsed)
            if args is None:
                return
            return self._trace(*args)

        self._json(404, {"error": "not found"})

    def _trace(self, q: str, mode: str, k: int) -> None:
        """Run the search with a tracer whose sink is the socket itself.

        Each stage's event is written and flushed the moment the stage ends,
        so the client sees the pipeline advance in real time. No worker
        thread, no queue: the handler thread does the search, and the tracer
        writes through it.
        """
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()

        alive = True

        def sink(ev: dict) -> None:
            nonlocal alive
            if not alive:
                return
            try:
                self.wfile.write(
                    f"data: {json.dumps(ev, default=_jsonable)}\n\n".encode())
                self.wfile.flush()
            except (BrokenPipeError, ConnectionError, OSError):
                alive = False          # client went away; finish quietly

        tr = Tracer(sink)
        tr.plan(mode)
        try:
            intake(tr, q, mode, k)
            hits = _ENGINES[mode].search(q, k=k, trace=tr)
            with tr.stage("render", "Attach metadata, emit top k") as st:
                results = _results(hits)
                st.fact("hits", len(results))
                st.fact("joined with", "abstract, temporal coverage, table "
                                       "count, archive URL")
            tr.done(query=q, mode=mode, results=results)
        except ollama.OllamaUnavailable as e:
            tr.error(str(e), hint="mode=lexical works offline")
        except Exception as e:                         # noqa: BLE001
            tr.error(str(e)[:300])
        drift = tr.unplanned()
        if drift:
            print(f"  trace plan drift for mode={mode}: {drift}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args(argv)

    _load_engines()
    if not ollama.available():
        print("\n  NOTE: Ollama is not reachable, so semantic and hybrid modes\n"
              "  will fail. Lexical mode works offline.\n"
              "  Fix:  ollama pull bge-m3\n")

    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"\n  search bar:  http://{a.host}:{a.port}\n"
          f"  api:         http://{a.host}:{a.port}/api/search?q=understory+light\n"
          f"  trace:       http://{a.host}:{a.port}/api/trace?q=understory+light\n"
          f"  ctrl-c to stop\n")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

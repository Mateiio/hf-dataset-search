"""The search bar. Stdlib http.server -- no framework, no build step.

    python -m hf_search.server          ->  http://localhost:8000

Serves web/index.html and one JSON endpoint:

    GET /api/search?q=<query>&mode=hybrid|semantic|lexical&k=10

All three engines are built once at startup (a couple of seconds) and held in
memory, so a query is an embedding call plus a matrix multiply.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from hf_search import corpus, ollama
from hf_search.hybrid import get_engine
from hf_search.paths import WEB

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


class Handler(BaseHTTPRequestHandler):
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
            qs = urllib.parse.parse_qs(parsed.query)
            q = (qs.get("q") or [""])[0].strip()
            mode = (qs.get("mode") or ["hybrid"])[0]
            k = int((qs.get("k") or ["10"])[0])
            if not q:
                return self._json(400, {"error": "empty query"})
            if mode not in _ENGINES:
                return self._json(400, {"error": f"unknown mode {mode}"})

            t0 = time.perf_counter()
            try:
                hits = _ENGINES[mode].search(q, k=k)
            except ollama.OllamaUnavailable as e:
                # Lexical needs no model, so say so rather than just failing.
                return self._json(503, {"error": str(e),
                                        "hint": "mode=lexical works offline"})
            except Exception as e:                     # noqa: BLE001
                return self._json(500, {"error": str(e)[:300]})

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
            return self._json(200, {
                "query": q, "mode": mode,
                "ms": round((time.perf_counter() - t0) * 1000),
                "results": results,
            })

        self._json(404, {"error": "not found"})


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
          f"  ctrl-c to stop\n")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""The EDI search bar. Stdlib http.server -- no framework, no build step.

    python -m edisearch.serve.server          ->  http://localhost:8001

Serves web/edi.html and these JSON endpoints:

    GET /api/status
    GET /api/scopes
    GET /api/search?q=<query>&mode=<lexical|bm25|semantic|hybrid|hybrid-bm25>&k=10&scope=<scope>
    GET /api/trace?q=...&mode=...&k=10&scope=...      (server-sent events)
    GET /api/evaluation                                 the current results.jsonl, per query

Same shape as `hf_search.server`, over the whole harvested corpus, with two
lexical engines instead of one and a scope filter. Filtering is applied
after ranking (retrieve deeper, keep the scope, cut to k), so one set of
indexes serves every scope. Every engine is built once at startup: the
lexical indexes over 10,639 packages take a few seconds, the vectors load
from disk.

The evaluation endpoint reads `data/results.jsonl`, `data/queries.jsonl`
and the yield probe's verdict file and returns exactly what
`docs/evaluation.md` shows, so the page can render the per-query table and
the disagreement cases without anyone explaining them.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
from collections import Counter, defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import numpy as np

from hf_search import ollama, trace as hf_trace
from hf_search.trace import Tracer, intake
from hf_search.hybrid import HybridIndex
from hf_search.lexical import LexicalIndex
from edisearch.index import store
from edisearch.index.lexical import BM25Index
from edisearch.paths import DATA, EVALSET, ROOT

WEB = ROOT / "web"
PORTAL = "https://portal.edirepository.org/nis/mapbrowse?packageid={pid}"

_ENGINES: dict = {}
_RECORDS: list = []
_BY_ID: dict = {}
_SCOPES: Counter = Counter()

# Trace plans for the two BM25 modes, registered beside hf_search's own.
_BM25 = ("lex_bm25", "BM25 over dataset documents", "lex")
hf_trace.PLANS.setdefault("bm25", [hf_trace._INTAKE, _BM25, hf_trace._RENDER])
hf_trace.PLANS.setdefault("hybrid-bm25", [hf_trace._INTAKE, hf_trace._EMBED,
                                          hf_trace._COSINE, _BM25, hf_trace._RRF,
                                          hf_trace._RENDER])


def _load_engines(verbose: bool = True) -> None:
    global _RECORDS, _BY_ID, _SCOPES
    t0 = time.perf_counter()
    _RECORDS = store.load_records()
    _BY_ID = {r.id: r for r in _RECORDS}
    _SCOPES = Counter(r.id.rsplit(".", 2)[0] for r in _RECORDS)
    sem = store.load_semantic(_RECORDS)
    lex = LexicalIndex(_RECORDS)
    bm25 = BM25Index(_RECORDS)
    _ENGINES.update({
        "lexical": lex, "bm25": bm25, "semantic": sem,
        "hybrid": HybridIndex(semantic=sem, lexical=lex, records=_RECORDS),
        "hybrid-bm25": HybridIndex(semantic=sem, lexical=bm25, records=_RECORDS),
    })
    if verbose:
        print(f"loaded {len(_RECORDS):,} packages in {len(_SCOPES)} scopes and "
              f"{len(_ENGINES)} engines in {time.perf_counter() - t0:.1f}s")


def _results(hits, scope: str | None, k: int) -> list:
    out = []
    for h in hits:
        rec = _BY_ID.get(h.dataset)
        sc = h.dataset.rsplit(".", 2)[0]
        if scope and sc != scope:
            continue
        out.append({
            "id": h.dataset, "scope": sc, "title": h.title,
            "score": round(float(h.score), 4), "why": h.why,
            "abstract": (rec.abstract[:280] + "...") if rec and rec.abstract else "",
            "temporal": rec.temporal if rec else {},
            "n_tables": len(rec.tables) if rec else 0,
            "url": PORTAL.format(pid=h.dataset),
        })
        if len(out) >= k:
            break
    return out


def _jsonable(o):
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError(f"not serialisable: {type(o).__name__}")


def _evaluation() -> dict:
    """What docs/evaluation.md shows, as data."""
    results_path, queries_path = DATA / "results.jsonl", DATA / "queries.jsonl"
    if not results_path.exists() or not queries_path.exists():
        return {"n": 0, "queries": [], "methods": [], "note": "no evaluation run yet"}
    rows = [json.loads(l) for l in results_path.read_text(encoding="utf-8").splitlines()]
    queries = {q["query_id"]: q for q in
               (json.loads(l) for l in queries_path.read_text(encoding="utf-8").splitlines())}
    by_q = defaultdict(dict)
    for r in rows:
        by_q[r["query_id"]][r["method"]] = r
    methods = [m for m in store.MODES if any(m in d for d in by_q.values())]
    out = []
    for qid, byq in sorted(by_q.items()):
        q = queries.get(qid, {})
        any_row = next(iter(byq.values()))
        target = q.get("provenance", {}).get("dataset_doi")
        ranks = {m: (byq[m]["rank"] if m in byq else None) for m in methods}
        top = {m: byq[m]["ranked_package_ids"][:3] for m in methods if m in byq}
        in5 = [m for m, r in ranks.items() if r and r <= 5]
        out.append({"query_id": qid, "text": q.get("text", ""), "origin": q.get("origin"),
                    "citing_doi": q.get("provenance", {}).get("citing_doi"),
                    "target_doi": target, "overlap": any_row["overlap"], "ranks": ranks,
                    "top3": top, "disagreement": bool(in5) and len(in5) < len(ranks)})
    verdicts_path = EVALSET / "verdicts.json"
    verdicts = Counter(v["verdict"] for v in
                       json.loads(verdicts_path.read_text(encoding="utf-8")).values()) \
        if verdicts_path.exists() else Counter()
    n = len(out)
    return {"n": n, "methods": methods, "queries": out,
            "stage": "demonstration" if n < 30 else "correlation" if n < 60 else "paired test",
            "indexed": len(_RECORDS), "scopes": len(_SCOPES),
            "verdicts": dict(verdicts),
            "in_top5": {m: sum(1 for o in out if o["ranks"][m] and o["ranks"][m] <= 5) for m in methods}}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        if "/api/" in (args[0] if args else ""):
            super().log_message(fmt, *args)

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, obj) -> None:
        self._send(code, json.dumps(obj, default=_jsonable).encode(), "application/json")

    def _query(self, parsed):
        qs = urllib.parse.parse_qs(parsed.query)
        q = (qs.get("q") or [""])[0].strip()
        mode = (qs.get("mode") or ["hybrid"])[0]
        k = max(1, min(50, int((qs.get("k") or ["10"])[0])))
        scope = (qs.get("scope") or [""])[0].strip() or None
        if not q:
            return None, self._json(400, {"error": "empty query"})
        if mode not in _ENGINES:
            return None, self._json(400, {"error": f"unknown mode {mode}"})
        if scope and scope not in _SCOPES:
            return None, self._json(400, {"error": f"unknown scope {scope}"})
        return (q, mode, k, scope), None

    def do_GET(self):  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/index.html", "/edi.html"):
            page = WEB / "edi.html"
            if not page.exists():
                return self._json(500, {"error": f"missing {page}"})
            return self._send(200, page.read_bytes(), "text/html; charset=utf-8")
        if parsed.path == "/api/status":
            return self._json(200, {"packages": len(_RECORDS), "scopes": len(_SCOPES),
                                    "ollama": ollama.available(),
                                    "model_pulled": ollama.has_model()})
        if parsed.path == "/api/scopes":
            return self._json(200, {"scopes": [{"scope": s, "n": n}
                                               for s, n in _SCOPES.most_common()]})
        if parsed.path == "/api/evaluation":
            return self._json(200, _evaluation())
        if parsed.path == "/api/search":
            args, _ = self._query(parsed)
            if args is None:
                return
            q, mode, k, scope = args
            t0 = time.perf_counter()
            try:
                hits = _ENGINES[mode].search(q, k=k * 20 if scope else k)
            except ollama.OllamaUnavailable as e:
                return self._json(503, {"error": str(e), "hint": "mode=lexical or bm25 works offline"})
            except Exception as e:  # noqa: BLE001
                return self._json(500, {"error": str(e)[:300]})
            return self._json(200, {"query": q, "mode": mode, "scope": scope,
                                    "ms": round((time.perf_counter() - t0) * 1000),
                                    "results": _results(hits, scope, k)})
        if parsed.path == "/api/trace":
            args, _ = self._query(parsed)
            if args is None:
                return
            return self._trace(*args)
        self._json(404, {"error": "not found"})

    def _trace(self, q: str, mode: str, k: int, scope: str | None) -> None:
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
                self.wfile.write(f"data: {json.dumps(ev, default=_jsonable)}\n\n".encode())
                self.wfile.flush()
            except (BrokenPipeError, ConnectionError, OSError):
                alive = False

        tr = Tracer(sink)
        tr.plan(mode)
        try:
            intake(tr, q, mode, k)
            hits = _ENGINES[mode].search(q, k=k * 20 if scope else k, trace=tr)
            with tr.stage("render", "Attach metadata, emit top k") as st:
                results = _results(hits, scope, k)
                st.fact("hits", len(results))
                if scope:
                    st.fact("scope filter", f"{scope}: kept {len(results)} of {len(hits)} ranked")
                st.fact("joined with", "abstract, temporal coverage, table count, portal URL")
            tr.done(query=q, mode=mode, results=results)
        except ollama.OllamaUnavailable as e:
            tr.error(str(e), hint="mode=lexical or bm25 works offline")
        except Exception as e:  # noqa: BLE001
            tr.error(str(e)[:300])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8001)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args(argv)
    _load_engines()
    if not ollama.available():
        print("\n  NOTE: Ollama is not reachable; semantic and hybrid modes will fail.\n"
              "  lexical and bm25 work offline.\n")
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"\n  search bar:  http://{a.host}:{a.port}\n"
          f"  api:         http://{a.host}:{a.port}/api/search?q=understory+light\n"
          f"  evaluation:  http://{a.host}:{a.port}/api/evaluation\n  ctrl-c to stop\n")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

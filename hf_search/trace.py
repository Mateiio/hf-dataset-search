"""Traceability: record what each stage of a search actually did.

Nothing here re-implements or simulates a search. Each stage wraps the real
call in `lexical.py`, `semantic.py` and `hybrid.py`, so a trace is a
measurement of the run that produced the results on screen rather than a
narration of what the code is supposed to do. Turning tracing off costs one
attribute lookup per stage -- `NULL` is a no-op object, not a branch at every
call site.

Events are emitted the instant they happen, which is what makes the browser's
progress bar honest: `server.py` writes each one to the socket and flushes, so
a stage shows up when it finishes, not when the whole search does.

    plan   stage list for this mode, so a progress bar can size itself
    start  stage i began
    end    stage i finished, with timing, facts and tables
    done   final results
    error  the search failed, with the message

Timings are real. Local search is fast enough that most stages land in single
milliseconds; the honest display of that is a small number, not a delay.
"""

from __future__ import annotations

import time
from contextlib import contextmanager

# Each stage names the lane it runs in, so the UI can draw the two engines as
# parallel paths converging on the fusion step instead of one flat list.
#   both -> shared          lex -> lexical      sem -> semantic     fuse -> rank fusion
_INTAKE = ("intake", "Parse and normalise the query", "both")
_RENDER = ("render", "Attach metadata, emit top k", "both")
_TFIDF = ("lex_tfidf", "TF-IDF over 458 dataset documents", "lex")
_ATTRS = ("lex_attrs", "TF-IDF over column definitions", "lex")
_MERGE = ("lex_merge", "Reserve slots, merge column matches", "lex")
_EMBED = ("embed", "Embed query with bge-m3 via Ollama", "sem")
_COSINE = ("cosine", "Cosine against dataset vectors", "sem")
_RRF = ("rrf", "Reciprocal rank fusion", "fuse")

PLANS = {
    "lexical": [_INTAKE, _TFIDF, _ATTRS, _MERGE, _RENDER],
    "semantic": [_INTAKE, _EMBED, _COSINE, _RENDER],
    "hybrid": [_INTAKE, _EMBED, _COSINE, _TFIDF, _ATTRS, _MERGE, _RRF, _RENDER],
}


class Stage:
    """Collects what one stage wants to say about itself."""

    def __init__(self, key: str, label: str):
        self.key = key
        self.label = label
        self.facts: dict = {}
        self.tables: list = []
        self.notes: list = []

    def fact(self, name: str, value) -> "Stage":
        self.facts[name] = value
        return self

    def table(self, title: str, columns: list, rows: list, note: str = "") -> "Stage":
        self.tables.append({"title": title, "columns": list(columns),
                            "rows": [list(r) for r in rows], "note": note})
        return self

    def note(self, text: str) -> "Stage":
        self.notes.append(text)
        return self


class _NullStage:
    def fact(self, *a, **k): return self
    def table(self, *a, **k): return self
    def note(self, *a, **k): return self


class NullTracer:
    """What an untraced search gets. Every method is a cheap no-op."""

    on = False

    @contextmanager
    def stage(self, key: str, label: str = ""):
        yield _NullStage()

    def plan(self, mode: str): pass
    def done(self, **kw): pass
    def error(self, msg: str): pass


NULL = NullTracer()


class Tracer:
    """Records stages and pushes each event to `sink` as it happens."""

    on = True

    def __init__(self, sink=None):
        self.sink = sink or (lambda ev: None)
        self.events: list = []
        self._t0 = time.perf_counter()
        self._i = 0
        self._planned: list = []

    @property
    def elapsed_ms(self) -> float:
        return (time.perf_counter() - self._t0) * 1000

    def _emit(self, ev: dict) -> None:
        ev["t"] = round(self.elapsed_ms, 1)
        self.events.append(ev)
        self.sink(ev)

    def plan(self, mode: str) -> None:
        self._planned = PLANS.get(mode, [])
        self._emit({"ev": "plan", "mode": mode, "stages": [
            {"key": k, "label": lab, "lane": lane}
            for k, lab, lane in self._planned]})

    @contextmanager
    def stage(self, key: str, label: str = ""):
        st = Stage(key, label)
        self._i += 1
        i = self._i
        self._emit({"ev": "start", "key": key, "label": label, "i": i,
                    "n": len(self._planned)})
        t = time.perf_counter()
        try:
            yield st
        except Exception as e:                         # noqa: BLE001
            self._emit({"ev": "end", "key": key, "label": label, "i": i,
                        "ms": round((time.perf_counter() - t) * 1000, 2),
                        "failed": str(e)[:300], "facts": st.facts,
                        "tables": st.tables, "notes": st.notes})
            raise
        self._emit({"ev": "end", "key": key, "label": label, "i": i,
                    "ms": round((time.perf_counter() - t) * 1000, 2),
                    "facts": st.facts, "tables": st.tables, "notes": st.notes})

    def done(self, **kw) -> None:
        self._emit({"ev": "done", "ms": round(self.elapsed_ms), **kw})

    def error(self, msg: str, **kw) -> None:
        self._emit({"ev": "error", "error": msg, **kw})

    def unplanned(self) -> list:
        """Stage keys that ran but were not in the plan, and vice versa.

        The plan drives the progress bar, so a plan that has drifted from the
        code would show a bar that never fills. Cheap to check, so check it.
        """
        ran = [e["key"] for e in self.events if e["ev"] == "end"]
        planned = [k for k, _, _ in self._planned]
        return [k for k in ran if k not in planned] + \
               [k for k in planned if k not in ran]


def intake(tr, query: str, mode: str, k: int) -> None:
    """The first stage: what arrived, and what the tokeniser makes of it.

    Lives here rather than in an engine because both `server.py` and the CLI
    run it before handing off, and because it is the one stage that is about
    the request rather than about an index.
    """
    import re

    from hf_search.lexical import TOKEN_RE, normalise

    with tr.stage(*_INTAKE[:2]) as st:
        folded = normalise(query)
        tokens = re.findall(TOKEN_RE, query.lower())
        st.fact("query", query)
        st.fact("mode", mode)
        st.fact("k requested", k)
        st.fact("characters", len(query))
        st.fact("tokens", " / ".join(tokens) or "(none)")
        dropped = [w for w in query.lower().split() if not re.fullmatch(TOKEN_RE, w)]
        if dropped:
            st.fact("words reshaped by tokeniser", " / ".join(dropped[:12]))
            st.note("The token pattern keeps digits and underscores attached so "
                    "'par_ac_down' survives whole; single characters and bare "
                    "numbers fall out.")
        if folded != query:
            extra = folded[len(query) + 1:]
            st.fact("hyphen-folded copy", extra)
            st.note("Hyphenated words are emitted a second time unhyphenated, so "
                    "'walk-up' also matches an abstract that writes 'walkup'.")

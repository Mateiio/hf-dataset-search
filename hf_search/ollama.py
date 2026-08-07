"""Minimal Ollama client. Embeddings only.

Stdlib HTTP -- no `requests`, no SDK. The only thing this project needs from a
model server is "turn text into a vector", and that is one POST.

Ollama renamed the embedding endpoint at some point, so both are tried. The
newer `/api/embed` batches; the older `/api/embeddings` takes one at a time.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from hf_search.paths import EMBED_MODEL, OLLAMA_HOST


class OllamaUnavailable(RuntimeError):
    """Raised when the server is not reachable, with actionable advice."""

    def __init__(self, detail: str = ""):
        super().__init__(
            f"Could not reach Ollama at {OLLAMA_HOST}. {detail}\n"
            f"  1. Install Ollama:  https://ollama.com\n"
            f"  2. Pull the model:  ollama pull {EMBED_MODEL}\n"
            f"  3. Confirm it runs: curl {OLLAMA_HOST}/api/tags\n"
            f"Searching needs it to embed your query. The prebuilt dataset "
            f"vectors in data/ are already computed and do not need it."
        )


def _post(path: str, payload: dict, timeout: int = 120) -> dict:
    req = urllib.request.Request(
        f"{OLLAMA_HOST}{path}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def available() -> bool:
    try:
        with urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=5) as r:
            return r.status == 200
    except Exception:                                 # noqa: BLE001
        return False


def has_model(name: str = EMBED_MODEL) -> bool:
    try:
        with urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=5) as r:
            names = [m["name"] for m in json.loads(r.read()).get("models", [])]
    except Exception:                                 # noqa: BLE001
        return False
    return any(n == name or n.split(":")[0] == name.split(":")[0] for n in names)


def embed(texts: list[str], model: str = EMBED_MODEL) -> list[list[float]]:
    """Embed a batch. Falls back to the older per-text endpoint."""
    try:
        r = _post("/api/embed", {"model": model, "input": texts})
        if "embeddings" in r:
            return r["embeddings"]
    except urllib.error.URLError as e:
        if isinstance(e, urllib.error.HTTPError) and e.code >= 500:
            pass                                       # try the legacy route
        else:
            raise OllamaUnavailable(str(e)) from e
    except Exception:                                  # noqa: BLE001
        pass

    out = []
    for t in texts:
        try:
            out.append(_post("/api/embeddings", {"model": model, "prompt": t})
                       ["embedding"])
        except urllib.error.URLError as e:
            raise OllamaUnavailable(str(e)) from e
    return out

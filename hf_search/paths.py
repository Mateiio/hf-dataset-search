"""Where things live.

Everything is resolved relative to the package, so the repo runs from wherever
it is cloned. The version this was extracted from hardcoded absolute paths under
one machine's drive, which is the single surest way to make code unrunnable by
anyone else.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Overridable so a large EML cache can live outside the repo if you prefer.
DATA = Path(os.environ.get("HF_SEARCH_DATA", ROOT / "data"))
WEB = ROOT / "web"

RECORDS = DATA / "records.json"          # parsed datasets, shipped
EMBEDDINGS = DATA / "embeddings.npy"     # 458 x 1024 float32, shipped
EMBEDDING_IDS = DATA / "embedding_ids.json"
EML_CACHE = DATA / "eml"                 # raw XML, NOT shipped; harvest.py fills it

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.environ.get("HF_SEARCH_EMBED_MODEL", "bge-m3")


def ensure_data_dir() -> Path:
    DATA.mkdir(parents=True, exist_ok=True)
    return DATA

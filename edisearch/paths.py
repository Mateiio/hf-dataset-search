"""Where the EDI corpus lives.

Same pattern as `hf_search.paths`: resolved relative to the repo, overridable
with one environment variable so the raw EML cache can sit on another drive.
The Harvard Forest files under `data/` are untouched; EDI gets its own names.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA = Path(os.environ.get("EDISEARCH_DATA", ROOT / "data"))
FIXTURES = ROOT / "fixtures"
DOCS = ROOT / "docs"

PROBE = DATA / "probe"                   # M0 listings, regenerable, not shipped
RAW = DATA / "raw"                       # M1+ raw EML by scope, not shipped
RECORDS = DATA / "records.jsonl"         # parsed EDI corpus, one JSON per line

USER_AGENT = ("hf-dataset-search/edisearch (research metadata index; "
              "https://github.com/Mateiio/hf-dataset-search)")

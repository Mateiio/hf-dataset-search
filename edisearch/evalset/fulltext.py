"""Full text of a citing paper, when it is open.

Route, in order, stopping at the first that yields text:

1. Europe PMC. If the paper has a PMCID and is open access, `fullTextXML`
   returns JATS with a real `<body>` and `<ref-list>`. Cleanest source
2. OpenAlex `best_oa_location.pdf_url`, then any other OA location with a
   PDF, then a PDF URL derived from the DOI for publishers whose pattern is
   fixed (PLOS, Copernicus, bioRxiv, Nature). Text comes out through pypdf
3. Nothing, in one of two ways that are kept apart because they mean
   different things for the project:
   - `walled`: an open location exists but every fetch got a bot wall (403,
     or HTML where a PDF was promised). Wiley, Elsevier, AMS, OUP, T&F and
     several repositories do this. The paper is open in a browser and a
     person can save it by hand; a script should not pretend to be a browser
   - `closed`: OpenAlex lists no open location at all

Landing pages are not scraped for `citation_pdf_url`: the hosts that would
need it are the same ones that answer 403 (checked 2026-09-13).

Unpaywall is not used: it wants an email in the query string, and OpenAlex
carries its open-access data anyway.

Everything is cached under `data/evalset/fulltext/<doi-slug>/` so a re-run
costs no requests: `openalex.json`, `europepmc.json`, the raw `.xml` or
`.pdf`, and `text.txt`, which is what `extract.py` reads and what character
offsets refer to.
"""

from __future__ import annotations

import io
import json
import re
import urllib.parse
from pathlib import Path

from edisearch import net
from edisearch.paths import FULLTEXT

OPENALEX = "https://api.openalex.org/works/doi:{doi}"
EPMC_SEARCH = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
               "?query=DOI:%22{doi}%22&format=json&resultType=lite")
EPMC_XML = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"


def slug(doi: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", doi.lower())


def folder(doi: str) -> Path:
    d = FULLTEXT / slug(doi)
    d.mkdir(parents=True, exist_ok=True)
    return d


def _cached_json(path: Path, url: str) -> dict | None:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    code, body, _ = net.get(url)
    if code != 200:
        path.write_text(json.dumps({"_http": code}), encoding="utf-8")
        return None
    path.write_bytes(body)
    return json.loads(body)


# ------------------------------------------------------------------ lookups

def openalex(doi: str) -> dict:
    d = _cached_json(folder(doi) / "openalex.json", OPENALEX.format(doi=doi))
    if not d or "_http" in d:
        return {"found": False}
    oa = d.get("open_access") or {}
    best = d.get("best_oa_location") or {}
    pdfs = [best.get("pdf_url")] + [
        loc.get("pdf_url") for loc in d.get("locations") or []
        if loc.get("is_oa") and loc.get("pdf_url")]
    return {
        "found": True,
        "title": d.get("title") or "",
        "year": d.get("publication_year"),
        "type": d.get("type"),
        "journal": ((d.get("primary_location") or {}).get("source") or {}).get("display_name"),
        "is_oa": bool(oa.get("is_oa")),
        "oa_status": oa.get("oa_status"),
        "pdf_urls": [u for u in dict.fromkeys(pdfs) if u],
        "landing": (d.get("primary_location") or {}).get("landing_page_url"),
    }


def europepmc(doi: str) -> dict:
    d = _cached_json(folder(doi) / "europepmc.json",
                     EPMC_SEARCH.format(doi=urllib.parse.quote(doi, safe="")))
    hits = ((d or {}).get("resultList") or {}).get("result") or []
    if not hits:
        return {"found": False}
    r = hits[0]
    return {"found": True, "pmcid": r.get("pmcid"),
            "open": r.get("isOpenAccess") == "Y" and r.get("inEPMC") == "Y"}


# ---------------------------------------------------------- derived PDF urls

_PLOS = {"pone": "plosone", "pbio": "plosbiology", "pclm": "climate",
         "pcbi": "ploscompbiol", "pgen": "plosgenetics", "pntd": "plosntds",
         "pwat": "water", "psus": "sustainabilitytransformation", "pmed": "plosmedicine"}


def derived_pdf_urls(doi: str) -> list[str]:
    """PDF URLs that follow from the DOI alone, for publishers that are regular."""
    out = []
    m = re.match(r"10\.1371/journal\.(\w+)\.\d+$", doi)
    if m and m.group(1) in _PLOS:
        out.append(f"https://journals.plos.org/{_PLOS[m.group(1)]}/article/file"
                   f"?id={doi}&type=printable")
    m = re.match(r"10\.5194/([a-z]+)-(\d+)-(\d+)-(\d{4})$", doi)
    if m:
        j, vol, page, yr = m.groups()
        out.append(f"https://{j}.copernicus.org/articles/{vol}/{page}/{yr}/{j}-{vol}-{page}-{yr}.pdf")
    m = re.match(r"10\.5194/([a-z]+)-(\d{4})-(\d+)$", doi)      # discussion paper
    if m:
        j, yr, n = m.groups()
        out.append(f"https://{j}.copernicus.org/preprints/{j}-{yr}-{n}/{j}-{yr}-{n}.pdf")
    if doi.startswith("10.1101/"):
        out.append(f"https://www.biorxiv.org/content/{doi}v1.full.pdf")
    m = re.match(r"10\.1038/(s\d+-\d+-\d+-\w+|nature\d+|ncomms\d+)$", doi)
    if m:
        out.append(f"https://www.nature.com/articles/{m.group(1)}.pdf")
    return out


# ------------------------------------------------------------------- text

_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"[ \t\r\f\v]+")


def _clean(chunk: str) -> str:
    chunk = re.sub(r"</(p|title|ref|sec|mixed-citation|element-citation)>", "\n", chunk)
    chunk = _TAG.sub(" ", chunk)
    chunk = chunk.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    chunk = _WS.sub(" ", chunk)
    return re.sub(r"\n\s*\n+", "\n", chunk).strip()


def _jats_text(xml: str) -> tuple[str, int]:
    """(text, offset where the reference list starts). Tags stripped."""
    def section(tag):
        m = re.search(rf"<{tag}[\s>].*?</{tag}>", xml, re.S)
        return m.group(0) if m else ""
    main = _clean(section("abstract") + "\n" + section("body"))
    refs = _clean(section("ref-list"))
    return main + "\n" + refs, len(main) + 1


# A heading on its own line; pypdf may leave a line number ("References 382")
# or a qualifier ("LTER Data References") on it. The earliest such heading in
# the last two thirds of the paper starts the reference list.
_REFS_HEADING = re.compile(
    r"^[^\n]{0,20}\b(References?|Literature Cited|Bibliography|Works Cited|"
    r"REFERENCES?|LITERATURE CITED)\b[ \d]{0,8}$", re.M)


def _pdf_text(data: bytes) -> tuple[str, int]:
    """(text, offset where the reference list starts, or -1 if no heading found)."""
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(data))
    pages = [(p.extract_text() or "") for p in reader.pages]
    text = "\n".join(pages)
    text = re.sub(r"-\n(?=[a-z])", "", text)      # re-join words split at line ends
    text = _WS.sub(" ", text).strip()
    heads = [h for h in _REFS_HEADING.finditer(text) if h.start() > len(text) // 3]
    return text, (heads[0].start() if heads else -1)



def text(doi: str) -> dict:
    """{"route": ..., "chars": n, "path": ...} and text.txt on disk, or route None."""
    d = folder(doi)
    meta_path, txt_path = d / "text.json", d / "text.txt"
    if meta_path.exists():
        return json.loads(meta_path.read_text(encoding="utf-8"))

    meta = {"route": None, "chars": 0, "tried": []}
    if not re.match(r"10\.\d{4,}/", doi):
        meta["outcome"] = "non-doi"
        meta_path.write_text(json.dumps(meta), encoding="utf-8")
        return meta
    ep = europepmc(doi)
    oa = {}
    if ep.get("pmcid"):
        code, body, _ = net.get(EPMC_XML.format(pmcid=ep["pmcid"]))
        meta["tried"].append(f"europepmc:{ep['pmcid']}:{code}")
        if code == 200 and b"<body" in body:
            (d / "fulltext.xml").write_bytes(body)
            t, refs = _jats_text(body.decode("utf-8", "replace"))
            txt_path.write_text(t, encoding="utf-8")
            meta.update(route="europepmc", chars=len(t), pmcid=ep["pmcid"],
                        reflist_start=refs)
    if not meta["route"]:
        oa = openalex(doi)
        meta["oa_status"] = oa.get("oa_status")
        meta["type"] = oa.get("type")
        urls = list(dict.fromkeys(oa.get("pdf_urls", []) + derived_pdf_urls(doi)))
        for url in urls:
            code, body, final = net.get(url, headers={"Accept": "application/pdf"})
            is_pdf = body[:5] == b"%PDF-"
            meta["tried"].append(f"pdf:{urllib.parse.urlsplit(url).netloc}:{code}"
                                 f"{'' if is_pdf else ':not-pdf'}")
            if code == 200 and is_pdf:
                (d / "fulltext.pdf").write_bytes(body)
                try:
                    t, refs = _pdf_text(body)
                except Exception as e:  # pypdf on a broken file
                    meta["tried"].append(f"pypdf:{type(e).__name__}")
                    continue
                txt_path.write_text(t, encoding="utf-8")
                meta.update(route="pdf", chars=len(t), pdf_url=url, reflist_start=refs)
                break
    if meta["route"]:
        meta["outcome"] = meta["route"]
    elif oa.get("type") not in (None, "article", "preprint", "review", "book-chapter",
                                "dissertation", "report", "letter", "editorial"):
        meta["outcome"] = "not-a-paper"
    elif oa.get("is_oa") or ep.get("pmcid"):
        meta["outcome"] = "walled"
    else:
        meta["outcome"] = "closed"
    meta_path.write_text(json.dumps(meta), encoding="utf-8")
    return meta


def read_text(doi: str) -> str:
    p = folder(doi) / "text.txt"
    return p.read_text(encoding="utf-8") if p.exists() else ""

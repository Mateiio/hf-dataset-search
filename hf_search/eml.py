"""Parse Harvard Forest EML 2.2.0 into structured records.

The archive's metadata is rich -- abstract, keyword sets, temporal and
geographic coverage, section-titled methods, and per-table attribute lists with
declared units. Search quality depends on preserving that structure rather than
flattening everything to one blob of text, so the parser keeps it.

Stdlib `xml.etree` only. Namespaces are stripped on read: EML qualifies the root
but not its descendants consistently, and fighting qualified tags buys nothing.
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class Attribute:
    name: str
    definition: str = ""
    unit: str = ""
    scale: str = ""


@dataclass
class Table:
    filename: str
    description: str = ""
    attributes: list = field(default_factory=list)


@dataclass
class Record:
    id: str
    title: str = ""
    abstract: str = ""
    keywords: list = field(default_factory=list)
    people: list = field(default_factory=list)
    temporal: dict = field(default_factory=dict)
    geographic: list = field(default_factory=list)
    methods: list = field(default_factory=list)
    tables: list = field(default_factory=list)

    def dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Record":
        tables = [Table(filename=t["filename"], description=t.get("description", ""),
                        attributes=[Attribute(**a) for a in t.get("attributes", [])])
                  for t in d.get("tables", [])]
        return cls(id=d["id"], title=d.get("title", ""),
                   abstract=d.get("abstract", ""), keywords=d.get("keywords", []),
                   people=d.get("people", []), temporal=d.get("temporal", {}),
                   geographic=d.get("geographic", []),
                   methods=d.get("methods", []), tables=tables)

    def attributes(self):
        for t in self.tables:
            for a in t.attributes:
                yield t, a


def _strip_ns(root: ET.Element) -> ET.Element:
    for el in root.iter():
        if isinstance(el.tag, str) and "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]
    return root


def _txt(el, path: str = ".") -> str:
    if el is None:
        return ""
    n = el if path == "." else el.find(path)
    if n is None:
        return ""
    # itertext() so <para>/<section> wrappers do not swallow the content
    return " ".join("".join(n.itertext()).split())


def _unit_and_scale(attr: ET.Element) -> tuple[str, str]:
    ms = attr.find("measurementScale")
    if ms is None:
        return "", ""
    for scale in ("ratio", "interval", "nominal", "ordinal", "dateTime"):
        node = ms.find(scale)
        if node is None:
            continue
        unit = (_txt(node, "unit/standardUnit") or _txt(node, "unit/customUnit")
                or _txt(node, "formatString"))
        return unit, scale
    return "", ""


def parse(path: str | Path) -> Record:
    path = Path(path)
    root = _strip_ns(ET.parse(path).getroot())
    ds = root.find("dataset")
    if ds is None:
        raise ValueError(f"{path.name}: no <dataset> element")

    rec = Record(id=path.stem, title=_txt(ds, "title"), abstract=_txt(ds, "abstract"))
    rec.keywords = [_txt(k) for k in ds.findall(".//keywordSet/keyword") if _txt(k)]
    rec.people = [p for p in (
        " ".join(filter(None, [_txt(c, "individualName/givenName"),
                               _txt(c, "individualName/surName")])).strip()
        for c in ds.findall("creator")) if p]

    cov = ds.find("coverage")
    if cov is not None:
        rec.temporal = {
            "begin": _txt(cov, ".//temporalCoverage/rangeOfDates/beginDate/calendarDate"),
            "end": _txt(cov, ".//temporalCoverage/rangeOfDates/endDate/calendarDate"),
        }
        for g in cov.findall(".//geographicCoverage"):
            b = g.find("boundingCoordinates")
            if b is None:
                continue
            rec.geographic.append({
                "description": _txt(g, "geographicDescription"),
                "north": _txt(b, "northBoundingCoordinate"),
                "south": _txt(b, "southBoundingCoordinate"),
                "east": _txt(b, "eastBoundingCoordinate"),
                "west": _txt(b, "westBoundingCoordinate"),
            })

    for step in ds.findall(".//methods//methodStep"):
        d = step.find("description")
        if d is None:
            continue
        for sec in d.findall("section"):
            rec.methods.append({"title": _txt(sec, "title"), "text": _txt(sec)})
        if not d.findall("section") and _txt(d):
            rec.methods.append({"title": "", "text": _txt(d)})

    for t in ds.findall(".//dataTable"):
        tab = Table(filename=_txt(t, "physical/objectName") or _txt(t, "entityName"),
                    description=_txt(t, "entityDescription"))
        for a in t.findall(".//attribute"):
            unit, scale = _unit_and_scale(a)
            tab.attributes.append(Attribute(
                name=_txt(a, "attributeName"),
                definition=_txt(a, "attributeDefinition"),
                unit=unit, scale=scale))
        rec.tables.append(tab)
    return rec


def parse_dir(directory: str | Path, verbose: bool = True) -> list[Record]:
    directory = Path(directory)
    out, bad = [], []
    for p in sorted(directory.glob("hf*.xml")):
        try:
            out.append(parse(p))
        except Exception as e:                        # noqa: BLE001
            bad.append((p.stem, str(e)[:60]))
    if verbose:
        print(f"parsed {len(out)} EML files"
              + (f"; {len(bad)} failed: {bad[:3]}" if bad else ""))
    return out


def write_json(records: list[Record], path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([r.dict() for r in records], ensure_ascii=False),
                    encoding="utf-8")
    return path


def read_json(path: str | Path) -> list[Record]:
    return [Record.from_dict(d) for d in
            json.loads(Path(path).read_text(encoding="utf-8"))]

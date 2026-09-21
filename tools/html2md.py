"""Markdown twins for the HTML reports in docs/, so GitHub renders them.

    python tools/html2md.py docs/edi-search-report.html docs/fields-and-search.html

GitHub shows an .html file as source. The reports are prose and tables, which
Markdown carries without loss, so each one gets a .md twin generated from the
same file. This converter knows only the handful of structures those reports
use -- headings, paragraphs, lists, tables, callouts, stat tiles, step cards,
key/value grids, formulas -- and is not a general HTML-to-Markdown tool.
Stdlib only.
"""

from __future__ import annotations

import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

_INLINE = {"code", "b", "strong", "em", "i", "a", "span", "sub", "sup", "br"}


class Converter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.buf: list[str] = []
        self.stack: list[tuple[str, dict]] = []
        self.list_stack: list[tuple[str, int]] = []
        self.table: list[list[str]] | None = None
        self.row: list[str] | None = None
        self.cell: list[str] | None = None
        self.header_rows = 0
        self.skip_depth = 0
        self.in_pre = False
        self.quote = False          # inside a callout: each paragraph gets "> "
        self.stat = False           # inside a stat tile: "**number** — label"
        self.kv = False             # inside a key/value grid: one table row per pair

    # ----------------------------------------------------------- helpers
    def _cls(self, attrs) -> set[str]:
        return set((dict(attrs).get("class") or "").split())

    def _emit(self, text: str) -> None:
        if self.cell is not None:
            self.cell.append(text)
        else:
            self.buf.append(text)

    def _flush(self, sep: str = "\n\n") -> None:
        text = "".join(self.buf)
        text = re.sub(r"[ \t]+", " ", text).strip()
        if text:
            self.out.append(text + sep)
        self.buf = []

    # ------------------------------------------------------------ tags
    def handle_starttag(self, tag, attrs):
        cls = self._cls(attrs)
        if self.skip_depth:
            self.skip_depth += 1
            return
        if tag in ("link", "meta", "img"):           # void tags: nothing to close
            return
        if tag in ("style", "nav", "script", "title", "svg"):
            self.skip_depth = 1
            return
        self.stack.append((tag, dict(attrs)))
        if tag in ("h1", "h2", "h3"):
            self._flush()
            self.buf.append("#" * int(tag[1]) + " ")
        elif tag == "p" and "lede" in cls:
            self._flush(); self.buf.append("*")
        elif tag == "p":
            self._flush()
            if self.quote:
                self.buf.append("> ")
        elif tag == "div" and "eyebrow" in cls:
            self._flush(); self.buf.append("<sub>")
        elif tag == "div" and "callout" in cls:
            self._flush(); self.quote = True
            self.stack[-1] = (tag, {"callout": True})
        elif tag == "div" and "formula" in cls:
            self._flush(); self.in_pre = True; self.buf.append("```\n")
        elif tag == "div" and "stat" in cls and "stats" not in cls:
            self._flush(); self.buf.append("- "); self.stat = True
            self.stack[-1] = (tag, {"stat": True})
        elif tag == "div" and "step" in cls:
            self._flush(); self.buf.append("- ")
            self.stack[-1] = (tag, {"step": True})
        elif tag == "div" and "who" in cls:
            self._emit(" — *")
            self.stack[-1] = (tag, {"who": True})
        elif tag == "div" and "example" in cls:
            self._flush(); self.out.append("---\n\n")
        elif tag == "div" and "kv" in cls:
            self._flush(); self.buf.append("| | |\n|---|---|\n"); self.kv = True
            self.stack[-1] = (tag, {"kv": True})
        elif tag == "ul":
            self._flush(); self.list_stack.append(("-", 0))
        elif tag == "ol":
            self._flush(); self.list_stack.append(("1.", 0))
        elif tag == "li":
            marker, n = self.list_stack[-1]
            n += 1
            self.list_stack[-1] = (marker, n)
            self.buf.append(("  " * (len(self.list_stack) - 1)) + (f"{n}. " if marker == "1." else "- "))
        elif tag == "table":
            self._flush(); self.table = []; self.header_rows = 0
        elif tag == "thead":
            pass
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []
            if tag == "th":
                self.stack[-1] = (tag, {"th": True})
        elif tag == "code":
            self._emit("`")
        elif tag in ("b", "strong"):
            parent = self.stack[-2][0] if len(self.stack) > 1 else ""
            if self.kv and parent == "div":
                self.buf.append("| **")
                self.stack[-1] = (tag, {"kvkey": True})
            else:
                self._emit("**")
        elif tag in ("em", "i") and "dot" not in cls:
            self._emit("*")
        elif tag == "i" and "dot" in cls:
            self._emit("–" if "off" in cls else "●")
            self.stack[-1] = (tag, {"dot": True})
        elif tag == "a":
            self._emit("[")
        elif tag == "br":
            self._emit("\n")
        elif tag == "footer":
            self._flush(); self.out.append("---\n\n"); self.buf.append("*")
        elif tag == "span" and ("chip" in cls):
            inside_b = any(t in ("b", "strong") for t, _ in self.stack[:-1])
            if not inside_b:
                self._emit("**")
            self.stack[-1] = (tag, {"chip": True, "plain": inside_b})
        elif tag == "span" and self.kv and len(self.stack) > 1 and self.stack[-2][0] == "div":
            self.stack[-1] = (tag, {"kvval": True})
        elif tag == "span" and self.stack[-2:] and self.stack[-2][0] == "div" and "toc" in self._cls(self.stack[-2][1].items()):
            pass
        elif tag == "sub":
            self._emit("<sub>")
        elif tag == "sup":
            self._emit("<sup>")

    def handle_endtag(self, tag):
        if self.skip_depth:
            self.skip_depth -= 1
            return
        if not self.stack:
            return
        opened, meta = self.stack.pop()
        if tag in ("h1", "h2", "h3"):
            self._flush()
        elif tag == "p":
            if self.buf and self.buf[0] == "*":
                self.buf.append("*")
            self._flush()
        elif tag == "div" and meta.get("kv"):
            self.kv = False; self._flush()
        elif tag == "div" and meta.get("callout"):
            self._flush(); self.quote = False
        elif tag == "div" and meta.get("who"):
            self._emit("*")
        elif tag == "div" and meta.get("stat"):
            self.stat = False; self._flush()
        elif tag == "div":
            if self.buf and self.buf[0] == "<sub>":
                self.buf.append("</sub>")
            if self.in_pre:
                self.buf.append("\n```"); self.in_pre = False
            if self.buf and self.buf[0] in ("- ", "> ", "<sub>", "```\n"):
                self._flush()
        elif tag in ("ul", "ol"):
            self._flush("\n\n"); self.list_stack.pop()
        elif tag == "li":
            self._flush("\n")
        elif tag == "table":
            self._write_table(); self.table = None
        elif tag == "tr":
            if self.row is not None and self.table is not None:
                self.table.append(self.row)
            self.row = None
        elif tag in ("td", "th"):
            text = re.sub(r"\s+", " ", "".join(self.cell or [])).strip().replace("|", "\\|")
            if meta.get("th") and self.table is not None and not self.table:
                self.header_rows = 1
            if self.row is not None:
                self.row.append(text)
            self.cell = None
        elif tag == "code":
            self._emit("`")
        elif tag in ("b", "strong") and meta.get("kvkey"):
            self.buf.append("** | ")
        elif tag in ("b", "strong"):
            parent_meta = self.stack[-1][1] if self.stack else {}
            self._emit("** — " if parent_meta.get("stat") or parent_meta.get("step") else "**")
        elif tag in ("em", "i") and not meta.get("dot"):
            self._emit("*")
        elif tag == "a":
            href = meta.get("href", "")
            self._emit(f"]({href})" if href and not href.startswith("#") else "]")
            if href.startswith("#"):
                # internal anchors: drop the brackets' effect by rewriting the last '['
                pass
        elif tag == "footer":
            self.buf.append("*"); self._flush()
        elif tag == "span" and meta.get("chip"):
            if not meta.get("plain"):
                self._emit("**")
            else:
                self._emit(" ")
        elif tag == "span" and meta.get("kvval"):
            self.buf.append(" |\n")
        elif tag == "sub":
            self._emit("</sub>")
        elif tag == "sup":
            self._emit("</sup>")

    def handle_data(self, data):
        if self.skip_depth:
            return
        if self.in_pre:
            self.buf.append(data)
            return
        text = re.sub(r"\s+", " ", data)
        if self.kv and not text.strip():
            return
        self._emit(text)

    def _write_table(self):
        if not self.table:
            return
        rows = [r for r in self.table if r]
        if not rows:
            return
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        head, body = (rows[0], rows[1:]) if self.header_rows else ([""] * width, rows)
        lines = ["| " + " | ".join(head) + " |", "|" + "---|" * width]
        lines += ["| " + " | ".join(r) + " |" for r in body]
        self.out.append("\n".join(lines) + "\n\n")

    def result(self) -> str:
        self._flush()
        text = "".join(self.out)
        text = re.sub(r"\[([^\]]+)\]\]", r"\1", text)          # stray internal-anchor brackets
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def convert(path: Path) -> Path:
    c = Converter()
    c.feed(path.read_text(encoding="utf-8"))
    md = c.result()
    note = (f"<!-- Generated from {path.name} by tools/html2md.py; edit the HTML, "
            f"then regenerate. The HTML version has the styling. -->\n\n")
    out = path.with_suffix(".md")
    out.write_text(note + md, encoding="utf-8")
    return out


if __name__ == "__main__":
    for arg in sys.argv[1:] or ["docs/edi-search-report.html", "docs/fields-and-search.html"]:
        print("wrote", convert(Path(arg)))

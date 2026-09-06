#!/usr/bin/env python3
"""Generate the Numbers volume's citation ledger table from the book itself.

WHY THIS EXISTS
---------------
The Gospel of Luke volume's ledger declared all 24 Morgan sections to be
summary-only while eight chapters were in fact carrying 29 verbatim quotes —
a ledger that disagreed with its own book, undetected for months because the
quotes were valid markdown and the appendix read as coherent prose. The
lesson recorded in scripts/check-citation-ledger.py is: derive the ledger,
never hand-maintain it.

This walks the chapter files, counts `> "…"` verbatim quotes under each
commentator's `### ` subsection, and rewrites the table between the marker
comments in 99-appendix-references.md.

Usage:  python3 scripts/gen-numbers-citation-ledger.py --write
        python3 scripts/gen-numbers-citation-ledger.py            # print
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "numbers"
LEDGER = BOOKDIR / "99-appendix-references.md"
START = "<!-- gen-citation-ledger:start -->"
END = "<!-- gen-citation-ledger:end -->"

HEADING = re.compile(r"^### (.+?)$", re.M)
QUOTE = re.compile(r'^> "', re.M)
COMMENTATORS = [("馬太·亨利", "亨利"), ("摩根", "摩根")]
# Ante-Nicene fathers appear in five chapters only; counted together so the
# ledger shows what the book actually carries rather than a column of zeros.
FATHERS = ("革利免", "巴拿巴", "游斯丁", "愛任紐")

CJK_NUM = "零一二三四五六七八九十"


def cjk(n):
    if n <= 10:
        return CJK_NUM[n] if n < 10 else "十"
    if n < 20:
        return "十" + CJK_NUM[n - 10]
    return CJK_NUM[n // 10] + "十" + (CJK_NUM[n % 10] if n % 10 else "")


def count(text, name):
    heads = list(HEADING.finditer(text))
    n = 0
    for i, h in enumerate(heads):
        if name not in h.group(1):
            continue
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        nxt = text.find("\n## ", h.end())
        if nxt != -1:
            end = min(end, nxt)
        n += len(QUOTE.findall(text[h.end():end]))
    return n


def title_of(text):
    m = re.search(r"^# (.+?)\s*\(", text, re.M)
    return m.group(1).strip() if m else ""


def build():
    rows = ["| 章 | 章題 | 亨利引文 | 摩根引文 | 教父引文 |",
            "|--------|--------------------|--------|--------|--------|"]
    th = tm = tf = 0
    for f in sorted(BOOKDIR.glob("[0-9][0-9]-*.md")):
        num = int(f.name[:2])
        text = f.read_text(encoding="utf-8")
        h, m = count(text, "亨利"), count(text, "摩根")
        fa = sum(count(text, f) for f in FATHERS)
        if not (h or m or fa):
            continue
        th += h
        tm += m
        tf += fa
        rows.append(f"| 第 {num} 章 | {title_of(text)} | {h} | {m} | {fa or '—'} |")
    rows.append(f"| **合計** | **{len(rows)-2} 章** | **{th}** | **{tm}** | **{tf}** |")
    return "\n".join(rows)


def main():
    table = build()
    if "--write" in sys.argv:
        text = LEDGER.read_text(encoding="utf-8")
        a, b = text.find(START), text.find(END)
        if a < 0 or b < 0:
            sys.exit(f"markers not found in {LEDGER}")
        new = text[:a + len(START)] + "\n" + table + "\n" + text[b:]
        if new != text:
            LEDGER.write_text(new, encoding="utf-8")
            print(f"updated {LEDGER.name}")
        else:
            print(f"{LEDGER.name} already current")
        return 0
    print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())

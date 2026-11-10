#!/usr/bin/env python3
"""Generate the Gospel Harmony volume's 98-appendix-indices.md from the chapters.

WHY THIS EXISTS
---------------
Same rationale as gen-job-scripture-index.py / gen-john-scripture-index.py: an
index kept by hand drifts from the chapters it indexes. This reads the
reference line of each station chapter (01-..39-*.md) and derives two tables:

  (a) 站-by-站 table:  站 N | 章題 | 參照
  (b) Scripture index grouped by book in canonical order
      (馬太福音, 馬可福音, 路加福音, 約翰福音, 使徒行傳, 啟示錄),
      each Bible chapter -> the 站 that read it.

WHERE THE REFERENCES COME FROM (priority order)
-----------------------------------------------
  1. new format  a line  「參照行：馬太福音 1:18-2:12；路加福音 2:1-20」
  2. old format  YAML key 「scripture: 馬太福音 1:18-2:12, 路加福音 2:1-20」
  3. old format  the plain line right under the H1 (no key)
The old plain line is sometimes narrower than the YAML (e.g. 「約翰福音 4:46-5:18」
vs a four-Gospel YAML), so YAML wins over the plain line; the new 參照行 wins
over both. Separators ; ； , ， 、 are all accepted; a segment without a book
name inherits the previous one (「使徒行傳 1:1-11；2:1-47」); a trailing English
word (「啟示錄 Revelation 1-3」) and （parenthetical notes） or trailing notes
(「精選」) are ignored.

Writes ONLY books/bible/gospel-harmony/98-appendix-indices.md.

Usage:  python3 scripts/gen-gospel-harmony-scripture-index.py           # print
        python3 scripts/gen-gospel-harmony-scripture-index.py --write   # update file
        python3 scripts/gen-gospel-harmony-scripture-index.py --check   # exit 1 if stale
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "gospel-harmony"
OUT = BOOKDIR / "98-appendix-indices.md"

# canonical order -> (max chapters, [aliases incl. English tail])
BOOKS = [
    ("馬太福音", 28), ("馬可福音", 16), ("路加福音", 24),
    ("約翰福音", 21), ("使徒行傳", 28), ("啟示錄", 22),
]
MAXCHAP = dict(BOOKS)
ORDER = {n: i for i, (n, _) in enumerate(BOOKS)}
BOOK_RE = re.compile(r"(馬太福音|馬可福音|路加福音|約翰福音|使徒行傳|啟示錄)(?:\s*(?:Acts|Revelation))?")
NUM_RE = re.compile(r"(\d+)(?::(\d+))?(?:\s*[-–—]\s*(\d+)(?::(\d+))?)?")
SEP_RE = re.compile(r"[;；,，、]")

YAML_HEAD = """---
title: 耶穌基督完整生平
subtitle: The Complete Life of Jesus Christ
author: PubHub 三書精讀系統
date: 2026年11月
publisher: 三書精讀出版系統
---
"""


def station_files():
    files = []
    for p in sorted(BOOKDIR.glob("[0-9][0-9]-*.md")):
        n = int(p.name[:2])
        if 1 <= n <= 39:
            files.append((n, p))
    return files


def title_of(text):
    m = re.search(r"^# (.+)$", text, re.M)
    t = m.group(1).strip() if m else "（無標題）"
    t = re.sub(r"\s*[({（].*$", "", t)           # drop the English gloss
    return t.strip()


def ref_string(text):
    """Return (ref string, kind) for a chapter, per the priority in the docstring."""
    m = re.search(r"^參照行[：:]\s*(.+)$", text, re.M)
    if m:
        return m.group(1).strip(), "參照行"
    fm = re.match(r"---\n(.*?)\n---", text, re.S)
    if fm:
        y = re.search(r"^scripture:\s*(.+)$", fm.group(1), re.M)
        if y:
            return y.group(1).strip(), "yaml"
    h = re.search(r"^# .+$\n+(.+)$", text, re.M)
    if h and BOOK_RE.search(h.group(1)):
        return h.group(1).strip(), "plain"
    return "", "none"


def parse_refs(s):
    """Yield (book, chapter) for every chapter touched by a reference string."""
    s = re.sub(r"[（(][^）)]*[）)]", "", s)
    book = None
    out = []
    for seg in SEP_RE.split(s):
        seg = seg.strip()
        if not seg:
            continue
        bm = BOOK_RE.search(seg)
        if bm:
            book = bm.group(1)
            seg = seg[bm.end():]
        if book is None:
            continue
        nm = NUM_RE.search(seg)
        if not nm:
            continue
        c1, v1, a, b = nm.groups()
        c1 = int(c1)
        if v1 is None:
            c2 = int(a) if a else c1               # "3-4"  -> chapters 3..4
        else:
            c2 = int(a) if (a and b) else c1       # "3-4:13" -> 3..4 ; "1:5-56" -> 1
        if c2 < c1:
            c2 = c1
        if c1 < 1 or c2 > MAXCHAP[book]:
            print(f"warning: out-of-range reference {book} {c1}-{c2} in {s!r}", file=sys.stderr)
            continue
        out.extend((book, c) for c in range(c1, c2 + 1))
    return out


def clean_display(s):
    s = re.sub(r"\s*(?:Acts|Revelation)\b", "", s)
    return s.replace("；", "；").strip()


def build():
    stations = []          # (n, title, display, kind)
    index = defaultdict(set)
    for n, p in station_files():
        text = p.read_text(encoding="utf-8")
        ref, kind = ref_string(text)
        if not ref:
            print(f"warning: no reference found in {p.name}", file=sys.stderr)
        stations.append((n, title_of(text), clean_display(ref) or "（待補）", kind))
        for key in parse_refs(ref):
            index[key].add(n)
    return stations, index


def render(stations, index):
    L = [YAML_HEAD,
         "# 附錄：站次與經文索引 (Appendix: Stations and Scripture Index)",
         "",
         "本附錄由各章的「參照行」自動編製（建置時重新產生）：第一部分列出三十七站各自讀的福音經文，"
         "第二部分依福音書章號反查「這一章被哪一站讀到」。章內為解經而引用的其他經文，不列入本索引。",
         "",
         "---",
         "",
         "## 附錄一：三十七站一覽 (The Thirty-Seven Stations)",
         "",
         "| 站 | 章題 | 參照 |",
         "|------|--------------------|------------------------------------------------------|"]
    for n, title, disp, _kind in stations:
        L.append(f"| {n} | {title} | {disp} |")
    L += ["", "---", "", "## 附錄二：福音書經文索引 (Scripture Index of the Gospels and Acts-Revelation)", ""]
    for book, _mx in BOOKS:
        chaps = sorted(c for (b, c) in index if b == book)
        if not chaps:
            continue
        L += [f"### {book}", "",
              "| 章 | 讀於站 |",
              "|------------|--------------------------------------------------------------|"]
        for c in chaps:
            sts = "、".join(f"站 {n}" for n in sorted(index[(book, c)]))
            L.append(f"| {book} {c} | {sts} |")
        L.append("")
    return "\n".join(L).rstrip() + "\n"


def main():
    stations, index = build()
    text = render(stations, index)
    if "--stats" in sys.argv:
        kinds = defaultdict(int)
        for _n, _t, _d, k in stations:
            kinds[k] += 1
        print(f"{len(stations)} stations; reference sources: {dict(kinds)}; "
              f"{len(index)} distinct book-chapters")
        return 0
    if "--write" in sys.argv:
        old = OUT.read_text(encoding="utf-8") if OUT.exists() else None
        if old != text:
            OUT.write_text(text, encoding="utf-8")
            print(f"updated {OUT.name}: {len(stations)} stations, {len(index)} book-chapters")
        else:
            print(f"{OUT.name} already current: {len(stations)} stations, {len(index)} book-chapters")
        return 0
    if "--check" in sys.argv:
        old = OUT.read_text(encoding="utf-8") if OUT.exists() else None
        if old != text:
            print(f"STALE: {OUT} differs from generated output (run with --write)")
            return 1
        print(f"{OUT.name} is current")
        return 0
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

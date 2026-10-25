#!/usr/bin/env python3
"""Generate the 2 Kings volume's citation ledger from the book itself.

A hand-kept ledger drifts from what the chapters contain (the Luke failure,
see check-citation-ledger.py). This walks the chapter files, counts the
`> "…"` verbatim quotes under each commentator's `### ` subsection, and
rewrites two things in 99-appendix-references.md between marker comments:

  gen-citation-ledger     the per-chapter count table
  gen-ledger-lists        one "實際引用於：第N章、…" line per commentator,
                          in the form check-citation-ledger.py parses

Usage:  python3 scripts/gen-kings2-citation-ledger.py --write
        python3 scripts/gen-kings2-citation-ledger.py            # print
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "kings2"
LEDGER = BOOKDIR / "99-appendix-references.md"
T0, T1 = "<!-- gen-citation-ledger:start -->", "<!-- gen-citation-ledger:end -->"
L0, L1 = "<!-- gen-ledger-lists:start -->", "<!-- gen-ledger-lists:end -->"

HEADING = re.compile(r"^### (.+?)$", re.M)
QUOTE = re.compile(r'^> "', re.M)
COMMENTATORS = [("亨利", "馬太·亨利 (Matthew Henry)"), ("巴恩斯", "巴恩斯 (Albert Barnes)"),
                ("劍橋", "劍橋注釋 (Cambridge Bible)"), ("摩根", "G. 坎伯·摩根"),
                ("麥克阿瑟", "麥克阿瑟 (John MacArthur)")]
FATHERS = ("奧古斯丁", "屈梭多模", "耶柔米", "區利羅", "俄利根", "安波羅修", "貴格利", "教父")


def count(text, name):
    # A commentator can be a ### heading OR sit inside the shared 改革宗 ### block as a
    # quote attributed on its `> —` line; count both layouts.
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


def attributed(text, needle):
    """Quotes whose `> — <source>` line names `needle` (改革宗 block holds three authors)."""
    sec = re.search(r"^## 歷代注疏.*?(?=^## )", text, re.M | re.S)
    if not sec:
        return 0
    n = 0
    for m in re.finditer(r'^> "(?:.+?)"\n(?:>.*\n)*?> — ([^\n]+)', sec.group(0), re.M):
        if needle in m.group(1):
            n += 1
    return n


def title_of(text):
    m = re.search(r"^# (.+?)\s*\(", text, re.M)
    return m.group(1).strip() if m else ""


def per_chapter():
    out = []
    for f in sorted(BOOKDIR.glob("[0-9][0-9]-*.md")):
        num = int(f.name[:2])
        if not 1 <= num <= 25:
            continue
        text = f.read_text(encoding="utf-8")
        row = {"num": num, "title": title_of(text)}
        row["亨利"] = attributed(text, "Matthew Henry")
        row["巴恩斯"] = attributed(text, "Barnes")
        row["劍橋"] = attributed(text, "Cambridge")
        row["摩根"] = attributed(text, "Morgan") or count(text, "摩根")
        row["麥克阿瑟"] = attributed(text, "MacArthur") or count(text, "麥克阿瑟")
        row["教父"] = sum(count(text, n) for n in FATHERS)
        out.append(row)
    return out


def table(rows):
    cols = ["亨利", "巴恩斯", "劍橋", "摩根", "麥克阿瑟", "教父"]
    head = ["| 章 | 章題 | 亨利 | 巴恩斯 | 劍橋 | 摩根 | 麥克阿瑟 | 教父 |",
            "|--------|--------------------|------|------|------|------|----------|------|"]
    tot = dict.fromkeys(cols, 0)
    body = []
    for r in rows:
        for c in cols:
            tot[c] += r[c]
        body.append(f"| 第 {r['num']} 章 | {r['title']} | " + " | ".join(str(r[c]) if r[c] else "—" for c in cols) + " |")
    body.append(f"| **合計** | **{len(rows)} 章** | " + " | ".join(f"**{tot[c]}**" for c in cols) + " |")
    return "\n".join(head + body)


def lists(rows):
    # One H2 per commentator whose text contains the name: check-citation-ledger.py
    # isolates each commentator's declared list by H2, and falls back to scanning the
    # whole ledger (merging everyone's lists) when it cannot find one.
    out = []
    for key, label in COMMENTATORS + [("教父", "教父時期")]:
        ch = [f"第{r['num']}章" for r in rows if r[key]]
        out.append(f"## 二、引文核對記錄——{label}\n\n**逐字引用**：{'、'.join(ch) if ch else '（無）'}\n\n"
                   "**要旨綜述的章**：（無——凡標註此家之處均為逐字引句）")
    return "\n\n".join(out)


def replace(text, a, b, body):
    i, j = text.find(a), text.find(b)
    if i < 0 or j < 0:
        sys.exit(f"markers {a} / {b} not found in {LEDGER}")
    return text[:i + len(a)] + "\n" + body + "\n" + text[j:]


def main():
    rows = per_chapter()
    if "--write" not in sys.argv:
        print(table(rows)); print(); print(lists(rows)); return 0
    text = LEDGER.read_text(encoding="utf-8")
    new = replace(replace(text, T0, T1, table(rows)), L0, L1, lists(rows))
    if new != text:
        LEDGER.write_text(new, encoding="utf-8")
        print(f"updated {LEDGER.name}")
    else:
        print(f"{LEDGER.name} already current")
    return 0


if __name__ == "__main__":
    sys.exit(main())

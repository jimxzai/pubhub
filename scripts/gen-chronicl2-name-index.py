#!/usr/bin/env python3
"""Generate the 2 Chronicles volume's person-and-place index from the book's own text.

WHY THIS EXISTS
---------------
Same rationale as scripts/gen-numbers-name-index.py: the volume has a Scripture
index and a citation ledger, both generated, but no way for a reader to answer
"where does this book discuss Manasseh?" or "which chapter covers Lachish?" —
the 讀者可用性 row of the house rubric.

A hand-kept index would drift out of sync the moment a chapter is edited. So
the TERM LIST is curated by hand (which names matter in 2 Chronicles is an
editorial judgment a script cannot make) and the LOCATIONS are derived
mechanically from the chapter files every time it runs.

Only occurrences in the study text are counted — the `## 經文` block is
skipped, because a name appearing in the Bible text itself tells the reader
nothing about where the book *discusses* it.

Usage:  python3 scripts/gen-chronicl2-name-index.py --write
        python3 scripts/gen-chronicl2-name-index.py            # print
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "chronicl2"
APPENDIX = BOOKDIR / "98-appendix-indices.md"
UBIQUITOUS = 15   # above this many chapters, list a note instead of every chapter
START = "<!-- gen-name-index:start -->"
END = "<!-- gen-name-index:end -->"

# Curated: the people and places this book actually turns on — the 21 kings in
# reign order, the figures whose actions are pivotal to a specific chapter,
# and the places that anchor the narrative geographically.
PEOPLE = [
    ("所羅門", ["所羅門"]),
    ("羅波安", ["羅波安"]),
    ("亞比雅", ["亞比雅"]),
    ("亞撒", ["亞撒"]),
    ("約沙法", ["約沙法"]),
    ("約蘭（猶大王）", ["約蘭"]),
    ("亞哈謝（猶大王）", ["亞哈謝"]),
    ("亞他利雅", ["亞他利雅"]),
    ("約阿施（猶大王）", ["約阿施"]),
    ("亞瑪謝", ["亞瑪謝"]),
    ("烏西雅", ["烏西雅"]),
    ("約坦", ["約坦"]),
    ("亞哈斯", ["亞哈斯"]),
    ("希西家", ["希西家"]),
    ("瑪拿西", ["瑪拿西"]),
    ("亞們", ["亞們王", "其子亞們"]),
    ("約西亞", ["約西亞"]),
    ("約哈斯", ["約哈斯"]),
    ("約雅敬", ["約雅敬"]),
    ("約雅斤", ["約雅斤"]),
    ("西底家", ["西底家"]),
    ("耶何耶大", ["耶何耶大"]),
    ("希蘭（推羅王）", ["希蘭"]),
    ("示巴女王", ["示巴女王"]),
    ("耶羅波安", ["耶羅波安"]),
    ("以利亞", ["以利亞"]),
    ("以賽亞", ["以賽亞"]),
    ("戶勒大", ["戶勒大"]),
    ("耶利米", ["耶利米"]),
    ("古列", ["古列"]),
    ("西拿基立", ["西拿基立"]),
    ("示撒", ["示撒"]),
    # "撒迦利亞" alone is ambiguous between Jehoiada's murdered son (ch24) and
    # the prophet (Zech 4:10, 13:1, cited elsewhere as a cross-reference) —
    # simple substring matching cannot tell them apart, so the label says so
    # rather than falsely claiming precision.
    ("撒迦利亞（含先知撒迦利亞書作者，見各章上下文）", ["撒迦利亞"]),
]
PLACES = [
    ("摩利亞山", ["摩利亞"]),
    ("基遍", ["基遍"]),
    ("示劍", ["示劍"]),
    ("以東", ["以東"]),
    ("古實", ["古實"]),
    ("拉末基列", ["拉末"]),
    ("摩押、亞捫", ["摩押", "亞捫"]),
    ("拉吉", ["拉吉"]),
    ("米吉多", ["米吉多"]),
    ("亞述", ["亞述"]),
    ("巴比倫", ["巴比倫"]),
    ("波斯", ["波斯"]),
]


def chapter_files():
    out = []
    for f in sorted(BOOKDIR.glob("[0-9][0-9]-*.md")):
        n = int(f.name[:2])
        if 1 <= n <= 36:
            out.append((n, f))
    return out


def study_text(path):
    """The chapter minus its Scripture block — where the book *discusses*."""
    t = path.read_text(encoding="utf-8")
    return re.sub(r"^## 經文 \(Scripture\).*?(?=^## 背景)", "", t, flags=re.M | re.S)


def build():
    hits = {}
    for num, f in chapter_files():
        text = study_text(f)
        for label, aliases in PEOPLE + PLACES:
            if any(a in text for a in aliases):
                hits.setdefault(label, []).append(num)
    return hits


def render(hits):
    out = []
    for title, group in (("人物", PEOPLE), ("地名", PLACES)):
        out.append(f"\n**{title}**\n")
        out.append("| 名稱 | 本書討論之處 |")
        out.append("|--------------------|--------------------------------|")
        for label, _ in group:
            ch = hits.get(label)
            if not ch:
                continue
            if len(ch) > UBIQUITOUS:
                loc = f"全書多處（{len(ch)} 章），見目次與各章標題"
            else:
                loc = "、".join(f"第 {c} 章" for c in ch)
            out.append(f"| {label} | {loc} |")
    return "\n".join(out)


def main():
    hits = build()
    table = render(hits)
    if "--write" in sys.argv:
        text = APPENDIX.read_text(encoding="utf-8")
        a, b = text.find(START), text.find(END)
        if a < 0 or b < 0:
            sys.exit(f"markers not found in {APPENDIX}")
        new = text[:a + len(START)] + "\n" + table + "\n" + text[b:]
        if new != text:
            APPENDIX.write_text(new, encoding="utf-8")
            print(f"updated {APPENDIX.name}: {len(hits)} indexed terms")
        else:
            print(f"{APPENDIX.name} already current")
        return 0
    print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())

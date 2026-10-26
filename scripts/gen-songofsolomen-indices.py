#!/usr/bin/env python3
"""Generate the Song of Songs volume's appendix of indices (98-appendix-indices.md) from the book's own text.

Same rationale as scripts/gen-joshua-scripture-index.py: a hand-kept index drifts
from the chapters. Three tables, all derived:

  附錄一  Chapter map  — 15 study units <-> the chapters/verses of the Song
          (units are not chapters; the H1 number is the unit number, the real range is in the reference line).
  附錄二  Cross-book Scripture index — every non-Song reference the chapters make.
  附錄三  Subject index — fixed term list, counted in each chapter's own prose
          (Scripture blocks, hymn blocks and tables of references excluded).

Usage:  python3 scripts/gen-songofsolomen-indices.py --write   # rewrite the three generated blocks
        python3 scripts/gen-songofsolomen-indices.py           # print them
"""
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "songofsolomen"
APPENDIX = BOOKDIR / "98-appendix-indices.md"

_spec = importlib.util.spec_from_file_location("john_index", ROOT / "scripts" / "gen-john-scripture-index.py")
john = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(john)
# The John generator leaves John itself out (that book's own text); this book
# cites John often, so put it back and rebuild the parser.
BOOKS = list(john.BOOKS)
BOOKS.insert(next(i for i, (f, _) in enumerate(BOOKS) if f == "路加福音") + 1,
             ("約翰福音", ["約翰福音", "約"]))
ORDER = {full: i for i, (full, _) in enumerate(BOOKS)}
ALIAS = {a: full for full, aliases in BOOKS for a in aliases}
MAXCHAP = dict(john.MAXCHAP, **{"約翰福音": 21})
_SHORT = "|".join(a for a in ALIAS if len(a) == 1)
_LONG = "|".join(sorted((a for a in ALIAS if len(a) > 1), key=len, reverse=True))
REF = re.compile(
    rf"(?:(?:(?<![{john.CJK}A-Za-z0-9])|(?<=[與及和並見如參]))({_SHORT})|(?<![A-Za-z0-9])({_LONG}))"
    rf"\s*(\d+)(?::{john.VERSES})?(?=\s*章?)"
)

AMBIGUOUS = set("但得該拿傳歌書拉")
LIST_PUNCT = set("（(、；;/ 與及和並見如參")

VOLUME = {**{n: "卷一·渴慕與尋見" for n in range(1, 7)},
          **{n: "卷二·園子的敞開" for n in (7, 8)},
          **{n: "卷三·失落與重尋" for n in (9, 10, 11)},
          **{n: "卷四·渴想的反轉與印記" for n in (12, 13, 14, 15)}}

SOURCES = [
    ("000-preface.md", "前言"), ("00-overview.md", "卷首·概覽"), ("00a-song-position.md", "卷首·定位"),
    ("00b-love-spine.md", "卷首·骨幹"), ("00c-revelation-order.md", "卷首·啟示的次序"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}章") for i in range(1, 16)] + [
    ("99-the-open-ending.md", "卷末"), ("999-afterword.md", "跋"),
]

# subject -> regex counted in chapter prose
SUBJECTS = [
    ("良人", r"良人"), ("佳偶", r"佳偶"), ("妹子／新婦", r"妹子|新婦|新娘"), ("書拉密女", r"書拉密"),
    ("所羅門", r"所羅門"), ("耶路撒冷的眾女子", r"眾女子|耶路撒冷的女子"),
    ("不要叫醒／驚動", r"叫醒|驚動|不要.{0,3}喚醒"), ("尋找／尋見", r"尋找|尋見|尋不見"),
    ("歸屬的話（我屬／屬我）", r"屬我的良人|良人屬我"), ("戀慕", r"戀慕"),
    ("園", r"園"), ("葡萄園", r"葡萄園"), ("泉／井", r"泉源|活水|井"),
    ("百合花／玫瑰", r"百合|玫瑰|水仙"), ("沒藥／乳香／香料", r"沒藥|乳香|香料|香膏"),
    ("鴿子", r"鴿"), ("羚羊／小鹿", r"羚羊|小鹿|母鹿"), ("蘋果樹", r"蘋果"), ("酒", r"酒"),
    ("旗", r"旗"), ("印記／戳記", r"印記|戳記"), ("愛如死之堅強", r"如死之堅強|愛情如死"),
    ("耶和華的烈焰", r"烈焰"), ("嫉恨／忌邪", r"嫉恨|嫉妒|忌邪"),
    ("字面讀", r"字面"), ("寓意／預表", r"寓意|預表|寓言"), ("基督與教會", r"基督與教會|基督和教會"),
    ("伯爾拿", r"伯爾拿"), ("紀爾", r"紀爾|吉爾"), ("戴德生", r"戴德生"), ("司布真", r"司布真"),
    ("講者（誰在說話）", r"誰在說話|講者"), ("新耶路撒冷／羔羊的婚筵", r"新耶路撒冷|婚筵|婚娶"),
]


def refs_in(text):
    for m in REF.finditer(text):
        alias = m.group(1) or m.group(2)
        if alias in AMBIGUOUS and m.start() > 0 and text[m.start() - 1] not in LIST_PUNCT:
            continue
        chap = int(m.group(3))
        full = ALIAS[alias]
        if chap < 1 or chap > MAXCHAP[full]:
            continue
        yield full, chap


def source_path(name):
    if name.endswith(".md"):
        return BOOKDIR / name
    hits = sorted(BOOKDIR.glob(f"{name}-*.md"))
    return hits[0] if hits else None


def prose_lines(path, include_tables=False, include_word_study=False):
    """Chapter lines minus the Scripture block and hymn blocks. Table rows are dropped for
    chapters (their 與其他經文的關聯 / 原文研讀 tables would swamp the index) but kept for the
    front-matter files (include_tables=True), where the ten-step order and the speaker and
    reading tables are the discussion itself."""
    out, skip, skip3, in_ws = [], False, False, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            skip = line.startswith(("## 經文", "## 配詩"))
            skip3 = False
            in_ws = line.startswith("## 原文研讀")
        elif line.startswith("### "):
            # house-template boilerplate sections every chapter has; counting them
            # would make 壇 / 禱告 / 基督 appear to be subjects of every chapter
            skip3 = line.startswith(("### 今天的祭壇", "### 禱告回應", "### 默想問題"))
        if skip or skip3 or line.lstrip().startswith("> ^"):
            continue
        if line.lstrip().startswith("|") and not include_tables and not (include_word_study and in_ws):
            continue
        out.append(line)
    return out


def chapter_map():
    rows = ["| 單元 | 雅歌 | 卷 | 章題 | 本章鑰詞 |",
            "|--------|----------------|------------------------|--------------------------------|------------------------------------------|"]
    for i in range(1, 16):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        text = p.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, flags=re.M)
        title = re.sub(r"\s*\(.*\)\s*$", "", h1.group(1)) if h1 else ""
        refline = re.search(r"^雅歌\s*([\d:\-–]+)", text, flags=re.M)
        key = re.search(r"本章鑰詞[：:]\s*\**([^\n\\]*?)\**\s*(?:\\|$)", text, flags=re.M)
        rows.append(f"| {i:02d} | {refline.group(1) if refline else ''} | {VOLUME[i]} | {title} | "
                    f"{key.group(1).strip(' *') if key else ''} |")
    return "\n".join(rows)


def scripture_index():
    index = defaultdict(set)
    for fname, label in SOURCES:
        p = source_path(fname)
        if not p or not p.exists():
            continue
        for line in prose_lines(p, include_tables=not label.startswith("第"), include_word_study=True):
            cleaned = re.sub(r"雅歌\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
            cleaned = re.sub(r"(?<![一-鿿])歌\s*\d+(?::\d+(?:[-–]\d+)?)?", "", cleaned)
            for full, chap in refs_in(cleaned):
                if full == "雅歌":
                    continue
                index[(full, chap)].add(label)
    order = {lbl: i for i, (_, lbl) in enumerate(SOURCES)}
    keys = sorted(index, key=lambda k: (ORDER.get(k[0], 999), k[1]))
    out = ["| 經文 | 本書討論之處 |",
           "|--------------------------|----------------------------------------------------------|"]
    for full, chap in keys:
        out.append(f"| {full} {chap} | {'、'.join(sorted(index[(full, chap)], key=lambda l: order.get(l, 999)))} |")
    return "\n".join(out), len(keys)


# a subject whose hits are only meaningful in some units (Bernard's sermons stop at 3:1, so
# chapters 6-15 can only mention him in a disclaimer; do not index those as discussion)
ONLY_UNITS = {"伯爾拿": range(1, 6)}
# lines that merely say there is no such material are not discussion of the subject
DISCLAIMER = {"司布真": r"沒有|無", "伯爾拿": r"沒有|無"}


def subject_index():
    out = ["| 主題 | 見於 |", "|--------------------------|----------------------------------------------------------|"]
    for name, pat in SUBJECTS:
        where = []
        for i in range(1, 16):
            if name in ONLY_UNITS and i not in ONLY_UNITS[name]:
                continue
            p = source_path(f"{i:02d}")
            neg = DISCLAIMER.get(name)
            if p and sum(len(re.findall(pat, l)) for l in prose_lines(p) if not (neg and re.search(neg, l))) >= 1:
                where.append(f"第{i}章")
        if where:
            out.append(f"| {name} | {'、'.join(where)} |")
    return "\n".join(out)


def hebrew_index():
    """原文研讀 tables of every chapter -> one lookup table (word, where, chapter, first clause of the gloss)."""
    out = ["| 原文 | 出處 | 見 | 要點 |", "|----------------|------------------------|--------|------------------------------------------|"]
    n = 0
    for i in range(1, 16):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^## 原文研讀.*?(?=^## )", t, re.M | re.S)
        if not m:
            continue
        for line in m.group(0).splitlines():
            if not line.startswith("|") or line.startswith("|--") or "| 原文 |" in line:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3 or not re.search(r"[\u0590-\u05FF]", cells[0]):
                continue
            gloss = re.split(r"[；;。]", cells[2])[0]
            gloss = re.sub(r"\*+", "", gloss)
            if len(gloss) > 40:
                cut = gloss[:40]
                gloss = (cut.rsplit("，", 1)[0] if "，" in cut else cut) + "…"
            gloss = re.sub(r"（[^）]*$", "", gloss)
            out.append(f"| {cells[0]} | {cells[1]} | 第{i}章 | {gloss} |")
            n += 1
    return "\n".join(out)


BLOCKS = {"chapter-map": chapter_map, "hebrew-index": hebrew_index, "scripture-index": lambda: scripture_index()[0], "subject-index": subject_index}


def main():
    built = {k: f() for k, f in BLOCKS.items()}
    if "--write" not in sys.argv:
        for k, v in built.items():
            print(f"<!-- gen-{k} -->\n{v}\n")
        return 0
    text = APPENDIX.read_text(encoding="utf-8")
    for k, v in built.items():
        a, b = f"<!-- gen-{k}:start -->", f"<!-- gen-{k}:end -->"
        i, j = text.find(a), text.find(b)
        if i < 0 or j < 0:
            sys.exit(f"markers for {k} not found in {APPENDIX}")
        text = text[:i + len(a)] + "\n" + v + "\n" + text[j:]
    APPENDIX.write_text(text, encoding="utf-8")
    print(f"updated {APPENDIX.name}: map {built['chapter-map'].count(chr(10)) - 1} rows, "
          f"scripture {scripture_index()[1]} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())

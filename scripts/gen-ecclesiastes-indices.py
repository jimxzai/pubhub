#!/usr/bin/env python3
"""Generate the Ecclesiastes volume's appendix of indices (98-appendix-indices.md) from the book's own text.

Same rationale as scripts/gen-joshua-scripture-index.py: a hand-kept index drifts
from the chapters. Three tables, all derived:

  附錄一  Chapter map  — 12 study units <-> the chapters/verses of Ecclesiastes
          (one unit per chapter, so the H1 number is the real chapter number).
  附錄二  Cross-book Scripture index — every non-Ecclesiastes reference the chapters make.
  附錄三  Subject index — fixed term list, counted in each chapter's own prose
          (Scripture blocks, hymn blocks and tables of references excluded).

Usage:  python3 scripts/gen-ecclesiastes-indices.py --write   # rewrite the three generated blocks
        python3 scripts/gen-ecclesiastes-indices.py           # print them
"""
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "ecclesiastes"
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
    rf"(?:(?<![{john.CJK}A-Za-z0-9])({_SHORT})|(?<![A-Za-z0-9])({_LONG}))"
    rf"\s*(\d+)(?::{john.VERSES})?(?=\s*章?)"
)

AMBIGUOUS = set("但得該拿傳歌書拉")
LIST_PUNCT = set("（(、；;/ ")

VOLUME = {1: "卷一·試", 2: "卷一·試",
          3: "卷二·時", 4: "卷二·時", 5: "卷二·時", 6: "卷二·時",
          7: "卷三·問", 8: "卷三·問", 9: "卷三·問", 10: "卷三·問",
          11: "卷四·歸", 12: "卷四·歸"}

SOURCES = [
    ("000-preface.md", "前言"), ("00-overview.md", "卷首·概覽"), ("00a-ecclesiastes-position.md", "卷首·定位"),
    ("00b-vanity-spine.md", "卷首·骨幹"), ("00c-revelation-order.md", "卷首·啟示的次序"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}章") for i in range(1, 13)] + [
    ("99-remember-your-creator.md", "卷末"), ("999-afterword.md", "跋"),
]

# subject -> regex counted in chapter prose
SUBJECTS = [
    ("虛空", r"虛空|הֶבֶל"), ("日光之下", r"日光之下"), ("捕風", r"捕風"), ("益處", r"益處"),
    ("勞碌／勞苦", r"勞碌|勞苦"), ("智慧／愚昧", r"智慧|愚昧"), ("快樂／喜樂", r"快樂|喜樂|歡樂"),
    ("吃喝", r"吃喝"), ("定期／時候", r"定期|定時"), ("永遠／永生", r"永遠|永生"),
    ("神的手／神給", r"神的手|神賜|神給|賜靈"), ("敬畏神", r"敬畏"), ("審問／審判", r"審問|審判"),
    ("死／塵土", r"塵土|死亡|死了|遭喪"), ("陰間", r"陰間"), ("誰知道", r"誰知道"),
    ("欺壓／冤屈", r"欺壓|冤屈"), ("孤單／同伴", r"孤單|同伴|兩個人"), ("財富／銀子", r"財富|資財|銀子"),
    ("王／君王", r"君王|王的"), ("記念", r"記念"), ("牧者", r"牧者|牧人"), ("造你的主", r"造你的主"),
    ("所羅門", r"所羅門"), ("傳道者", r"傳道者"), ("撒種／糧食", r"撒種|糧食"),
    ("少年／年老", r"少年|年老|衰敗"), ("塔木德", r"塔木德|Talmud"), ("新約", r"新約"),
    ("新耶路撒冷", r"新耶路撒冷"),
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


def prose_lines(path):
    """Chapter lines minus the Scripture block, hymn blocks and table rows."""
    out, skip, skip3 = [], False, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            skip = line.startswith(("## 經文", "## 配詩"))
            skip3 = False
        elif line.startswith("### "):
            # house-template boilerplate sections every chapter has; counting them
            # would make 壇 / 禱告 / 基督 appear to be subjects of every chapter
            skip3 = line.startswith(("### 今天的祭壇", "### 禱告回應", "### 默想問題"))
        if skip or skip3 or line.lstrip().startswith(("|", "> ^")):
            continue
        out.append(line)
    return out


def chapter_map():
    rows = ["| 章 | 傳道書 | 卷 | 章題 | 本章鑰詞 |",
            "|--------|----------------|------------------------|--------------------------------|------------------------------------------|"]
    for i in range(1, 13):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        text = p.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, flags=re.M)
        title = re.sub(r"\s*\(.*\)\s*$", "", h1.group(1)) if h1 else ""
        refline = re.search(r"^傳道書\s*([\d:\-–]+)", text, flags=re.M)
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
        for line in prose_lines(p):
            cleaned = re.sub(r"傳道書\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
            cleaned = re.sub(r"(?<![一-鿿])傳\s*\d+(?::\d+(?:[-–]\d+)?)?", "", cleaned)
            for full, chap in refs_in(cleaned):
                index[(full, chap)].add(label)
    order = {lbl: i for i, (_, lbl) in enumerate(SOURCES)}
    keys = sorted(index, key=lambda k: (ORDER.get(k[0], 999), k[1]))
    out = ["| 經文 | 本書討論之處 |",
           "|--------------------------|----------------------------------------------------------|"]
    for full, chap in keys:
        out.append(f"| {full} {chap} | {'、'.join(sorted(index[(full, chap)], key=lambda l: order.get(l, 999)))} |")
    return "\n".join(out), len(keys)


def subject_index():
    out = ["| 主題 | 見於 |", "|--------------------------|----------------------------------------------------------|"]
    for name, pat in SUBJECTS:
        where = []
        for i in range(1, 13):
            p = source_path(f"{i:02d}")
            if p and sum(len(re.findall(pat, l)) for l in prose_lines(p)) >= 1:
                where.append(f"第{i}章")
        if where:
            out.append(f"| {name} | {'、'.join(where)} |")
    return "\n".join(out)


def hebrew_index():
    """原文研讀 tables of every chapter -> one lookup table (word, where, chapter, first clause of the gloss)."""
    out = ["| 原文 | 出處 | 見 | 要點 |", "|--------------------|------------|--------|------------------------------------------------|"]
    n = 0
    for i in range(1, 13):
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

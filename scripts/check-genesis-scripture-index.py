#!/usr/bin/env python3
"""Audit books/bible/genesis/99a-appendix-scripture-index.md against the
book's own chapters, instead of trusting it as hand-maintained prose.

WHY THIS EXISTS
---------------
99a is a hand-compiled index: every cross-reference row was typed in by an
editor, and its own 體例說明 promises every row "直接取自...正文，不另行增補
未曾出現的引文". Nothing has ever checked that promise mechanically. A
2026-09-19 succinct-editing pass trimmed several chapters' closing
paragraphs (removing sentences that repeated a chapter's 基督焦點 verses),
which is exactly the kind of edit that can leave a hand-kept index citing a
sentence that no longer exists -- the Gospel of John's 99a had the same
class of bug (創40:34-35 cited for the tabernacle's glory, which is really
出埃及記 40:34-35) before it was made mechanical.

WHAT IT DOES
------------
1. Scans every genesis chapter file (01-17, plus 00-overview.md and
   00a-revelation-order.md) for every Bible reference to a book OTHER than
   Genesis itself, outside `## 經文` scripture blocks.
2. Parses 99a's own Part 2 (NT) and Part 3 (OT-other) tables into
   {(book, chapter): {genesis chapter labels}}.
3. Reports, per book+chapter:
     MISSING    a real citation in the chapters that 99a's tables never list
     STALE      a 99a row naming a genesis chapter that does not actually
                contain that citation anywhere (the drift class)
   Citations 99a lists AND the chapters actually contain are not reported --
   this script does not grade the THEME prose, only whether the reference
   pointer is honest.

USAGE
    python3 scripts/check-genesis-scripture-index.py
    python3 scripts/check-genesis-scripture-index.py --stats
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "genesis"
INDEX_FILE = BOOKDIR / "99a-appendix-scripture-index.md"

CHAPTERS = [
    ("00-overview.md", "00"),
    ("00a-revelation-order.md", "00"),
    ("01-creation.md", "01"), ("02-fall.md", "02"),
    ("03-cain-abel.md", "03"), ("04-noah.md", "04"),
    ("05-babel.md", "05"), ("06-abraham-call.md", "06"),
    ("07-covenant.md", "07"), ("08-sodom.md", "08"),
    ("09-isaac-sacrifice.md", "09"), ("10-jacob-esau.md", "10"),
    ("11-bethel.md", "11"), ("12-wrestling.md", "12"),
    ("13-joseph-dreams.md", "13"), ("14-joseph-egypt.md", "14"),
    ("15-reconciliation.md", "15"), ("16-blessings.md", "16"),
    ("17-covenant-fulfillment.md", "17"),
]

BOOKS = [
    ("創世記", ["創世記", "創"]), ("出埃及記", ["出埃及記", "出"]),
    ("利未記", ["利未記", "利"]), ("民數記", ["民數記", "民"]),
    ("申命記", ["申命記", "申"]), ("約書亞記", ["約書亞記", "書"]),
    ("士師記", ["士師記", "士"]), ("路得記", ["路得記", "得"]),
    ("撒母耳記上", ["撒母耳記上", "撒上"]), ("撒母耳記下", ["撒母耳記下", "撒下"]),
    ("列王紀上", ["列王紀上", "王上"]), ("列王紀下", ["列王紀下", "王下"]),
    ("歷代志上", ["歷代志上", "代上"]), ("歷代志下", ["歷代志下", "代下"]),
    ("以斯拉記", ["以斯拉記", "拉"]), ("尼希米記", ["尼希米記", "尼"]),
    ("以斯帖記", ["以斯帖記", "斯"]), ("約伯記", ["約伯記", "伯"]),
    ("詩篇", ["詩篇", "詩"]), ("箴言", ["箴言", "箴"]),
    ("傳道書", ["傳道書", "傳"]), ("雅歌", ["雅歌", "歌"]),
    ("以賽亞書", ["以賽亞書", "賽"]), ("耶利米書", ["耶利米書", "耶"]),
    ("耶利米哀歌", ["耶利米哀歌", "哀"]), ("以西結書", ["以西結書", "結"]),
    ("但以理書", ["但以理書", "但"]), ("何西阿書", ["何西阿書", "何"]),
    ("約珥書", ["約珥書", "珥"]), ("阿摩司書", ["阿摩司書", "摩"]),
    ("俄巴底亞書", ["俄巴底亞書", "俄"]), ("約拿書", ["約拿書", "拿"]),
    ("彌迦書", ["彌迦書", "彌"]), ("那鴻書", ["那鴻書", "鴻"]),
    ("哈巴谷書", ["哈巴谷書", "哈"]), ("西番雅書", ["西番雅書", "番"]),
    ("哈該書", ["哈該書", "該"]), ("撒迦利亞書", ["撒迦利亞書", "亞"]),
    ("瑪拉基書", ["瑪拉基書", "瑪"]),
    ("馬太福音", ["馬太福音", "太"]), ("馬可福音", ["馬可福音", "可"]),
    ("路加福音", ["路加福音", "路"]),
    ("使徒行傳", ["使徒行傳", "徒"]), ("羅馬書", ["羅馬書", "羅"]),
    ("哥林多前書", ["哥林多前書", "林前"]), ("哥林多後書", ["哥林多後書", "林後"]),
    ("加拉太書", ["加拉太書", "加"]), ("以弗所書", ["以弗所書", "弗"]),
    ("腓立比書", ["腓立比書", "腓"]), ("歌羅西書", ["歌羅西書", "西"]),
    ("帖撒羅尼迦前書", ["帖撒羅尼迦前書", "帖前"]),
    ("帖撒羅尼迦後書", ["帖撒羅尼迦後書", "帖後"]),
    ("提摩太前書", ["提摩太前書", "提前"]), ("提摩太後書", ["提摩太後書", "提後"]),
    ("提多書", ["提多書", "多"]), ("腓利門書", ["腓利門書", "門"]),
    ("希伯來書", ["希伯來書", "來"]), ("雅各書", ["雅各書", "雅"]),
    ("彼得前書", ["彼得前書", "彼前"]), ("彼得後書", ["彼得後書", "彼後"]),
    ("約翰壹書", ["約翰壹書", "約翰一書", "約壹"]),
    ("約翰貳書", ["約翰貳書", "約貳"]), ("約翰參書", ["約翰參書", "約參"]),
    ("猶大書", ["猶大書", "猶"]), ("啟示錄", ["啟示錄", "啟"]),
]
ALIAS = {}
for full, aliases in BOOKS:
    for a in aliases:
        ALIAS.setdefault(a, full)
MAXCHAP = {
    "創世記": 50, "出埃及記": 40, "利未記": 27, "民數記": 36, "申命記": 34,
    "約書亞記": 24, "士師記": 21, "路得記": 4, "撒母耳記上": 31, "撒母耳記下": 24,
    "列王紀上": 22, "列王紀下": 25, "歷代志上": 29, "歷代志下": 36, "以斯拉記": 10,
    "尼希米記": 13, "以斯帖記": 10, "約伯記": 42, "詩篇": 150, "箴言": 31,
    "傳道書": 12, "雅歌": 8, "以賽亞書": 66, "耶利米書": 52, "耶利米哀歌": 5,
    "以西結書": 48, "但以理書": 12, "何西阿書": 14, "約珥書": 3, "阿摩司書": 9,
    "俄巴底亞書": 1, "約拿書": 4, "彌迦書": 7, "那鴻書": 3, "哈巴谷書": 3,
    "西番雅書": 3, "哈該書": 2, "撒迦利亞書": 14, "瑪拉基書": 4, "馬太福音": 28,
    "馬可福音": 16, "路加福音": 24, "使徒行傳": 28, "羅馬書": 16,
    "哥林多前書": 16, "哥林多後書": 13, "加拉太書": 6, "以弗所書": 6,
    "腓立比書": 4, "歌羅西書": 4, "帖撒羅尼迦前書": 5, "帖撒羅尼迦後書": 3,
    "提摩太前書": 6, "提摩太後書": 4, "提多書": 3, "腓利門書": 1,
    "希伯來書": 13, "雅各書": 5, "彼得前書": 5, "彼得後書": 3,
    "約翰壹書": 5, "約翰貳書": 1, "約翰參書": 1, "猶大書": 1, "啟示錄": 22,
}

CJK = "一-鿿"
SHORT = "|".join(sorted((a for a in ALIAS if len(a) == 1), key=len, reverse=True))
LONG = "|".join(sorted((a for a in ALIAS if len(a) > 1), key=len, reverse=True))
VERSES = r"(\d+(?:[-–]\d+)?(?:\s*,\s*\d+(?:[-–]\d+)?)*)"
REF = re.compile(
    rf"(?:(?<![{CJK}A-Za-z0-9])({SHORT})|(?<![A-Za-z0-9])({LONG}))"
    rf"\s*(\d+)(?::{VERSES})?"
)

SKIP_PREFIX = ("> ^", "> \"", "> 「", "|")  # scripture verses, quotes, tables


def refs_in(text):
    for m in REF.finditer(text):
        alias = m.group(1) or m.group(2)
        full = ALIAS[alias]
        if full == "創世記":
            continue  # Genesis citing itself is not a cross-reference
        chap = int(m.group(3))
        if chap < 1 or chap > MAXCHAP[full]:
            continue
        yield full, chap


def collect_book_refs():
    """{(book, chapter): {genesis chapter label}} from the actual chapters."""
    found = defaultdict(set)
    for fname, label in CHAPTERS:
        p = BOOKDIR / fname
        if not p.exists():
            continue
        in_scripture = False
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.startswith("## 經文"):
                in_scripture = True
                continue
            if line.startswith("## ") and in_scripture:
                in_scripture = False
            if in_scripture:
                continue
            s = line.lstrip()
            if s.startswith(SKIP_PREFIX):
                continue
            for full, chap in refs_in(line):
                found[(full, chap)].add(label)
    return found


ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$")


def parse_index_refs():
    """{(book, chapter): {genesis chapter label}} as 99a's Part 2/3 declare."""
    declared = defaultdict(set)
    text = INDEX_FILE.read_text(encoding="utf-8")
    in_part23 = False
    for line in text.splitlines():
        if line.startswith("## 一、"):
            in_part23 = False
            continue
        if line.startswith("## 二、") or line.startswith("## 三、"):
            in_part23 = True
            continue
        if not in_part23:
            continue
        m = ROW_RE.match(line)
        if not m:
            continue
        ref_cell, _genesis_cell, _theme, chapters_cell = m.groups()
        if ref_cell in ("經文",) or set(ref_cell) == {"-"}:
            continue
        chapters = [c.strip() for c in re.split(r"[,，]", chapters_cell) if c.strip()]
        for full, chap in refs_in(ref_cell):
            declared[(full, chap)].update(chapters)
    return declared


def main():
    actual = collect_book_refs()
    declared = parse_index_refs()

    missing = sorted(k for k in actual if k not in declared)
    stale = []
    for k, labels in declared.items():
        real_labels = actual.get(k, set())
        extra = labels - real_labels
        if extra:
            stale.append((k, sorted(extra)))
    stale.sort()

    if "--stats" in sys.argv:
        print(f"actual citations found in chapters: {len(actual)} distinct book-chapters")
        print(f"declared in 99a Part 2/3: {len(declared)} distinct book-chapters")
        print(f"MISSING (real, not indexed): {len(missing)}")
        print(f"STALE   (indexed, chapter no longer has it): {len(stale)}")
        return 0

    if missing:
        print(f"MISSING -- {len(missing)} citation(s) found in the chapters but not in 99a:")
        for full, chap in missing:
            labels = ", ".join(sorted(actual[(full, chap)]))
            print(f"  {full}{chap}  (cited in ch. {labels})")
    if stale:
        print(f"\nSTALE -- {len(stale)} 99a row(s) name a chapter that no longer contains the citation:")
        for (full, chap), extra in stale:
            print(f"  {full}{chap}  declared for ch. {', '.join(extra)}, but not found there")
    if not missing and not stale:
        print("clean: every 99a Part 2/3 row matches a real citation, and no real citation is unindexed")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

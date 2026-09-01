#!/usr/bin/env python3
"""Generate the Gospel of John volume's Scripture Index from the book's own text.

WHY THIS EXISTS
---------------
`templates/pdf/gospel-of-john.latex` carried a hand-maintained 經文索引 for
months. Because nothing generated it from the text, it drifted: it cited
創世記 40:34-35 for the glory filling the tabernacle (that is 出埃及記 40:34-35,
Genesis 40 being Joseph in prison), and it was neither complete nor guaranteed
to match what the book actually discusses. A scripture index is exactly the
kind of apparatus that must be derived, not curated by hand.

WHAT IT DOES
------------
Walks the source files in the order `scripts/build-gospel-consolidated.sh`
concatenates them, extracts every NON-Gospel-of-John scripture reference, and
emits a LaTeX longtable mapping each reference to the chapters of this book
where it is discussed. Keyed to chapters, not page numbers, so it stays valid
across builds.

Usage:  python3 scripts/gen-john-scripture-index.py            # print LaTeX
        python3 scripts/gen-john-scripture-index.py --stats    # summary only
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "gospel-of-john"

# Source files in build order -> the label the index should point at.
SOURCES = [
    ("000-preface.md",                "前言"),
    ("00-overview.md",                "卷首·概覽"),
    ("00a-revelation-order.md",       "卷首·啟示的次序"),
    ("00b-i-am-deity.md",             "卷首·「我是」骨幹"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
    ("01-prologue.md",                "第1章"),
    ("01b-first-disciples.md",        "第1章（下）"),
    ("02-cana-wedding.md",            "第2章"),
    ("03-nicodemus.md",               "第3章"),
    ("04-samaritan-woman.md",         "第4章"),
    ("04b-nobleman-son.md",           "第4章（下）"),
    ("05-bethesda.md",                "第5章"),
    ("06-bread-of-life.md",           "第6章"),
    ("07-feast-tabernacles.md",       "第7章"),
    ("08-light-of-world.md",          "第8章"),
    ("09-blind-man.md",               "第9章"),
    ("10-good-shepherd.md",           "第10章"),
    ("11-lazarus.md",                 "第11章"),
    ("12-triumphal-entry.md",         "第12章"),
    ("13-washing-feet.md",            "第13章"),
    ("14-way-truth-life.md",          "第14章"),
    ("15-true-vine.md",               "第15章"),
    ("16-holy-spirit.md",             "第16章"),
    ("17-high-priestly-prayer.md",    "第17章"),
    ("18-arrest-trial.md",            "第18章"),
    ("19-crucifixion.md",             "第19章"),
    ("20-resurrection.md",            "第20章"),
    ("21-epilogue.md",                "第21章"),
    ("99-to-revelation.md",           "卷末"),
    ("999-afterword.md",              "跋"),
]

# Canonical order, with every abbreviation the book actually uses.
# (full name, [aliases]) -- longest alias must be tried first when matching.
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
    ("約翰壹書", ["約翰壹書", "約壹"]), ("約翰貳書", ["約翰貳書", "約貳"]),
    ("約翰參書", ["約翰參書", "約參"]), ("猶大書", ["猶大書", "猶"]),
    ("啟示錄", ["啟示錄", "啟"]),
]
ORDER = {full: i for i, (full, _) in enumerate(BOOKS)}
ALIAS = {}
for full, aliases in BOOKS:
    for a in aliases:
        ALIAS[a] = full
# longest aliases first so 撒下 wins over 撒, 林前 over 林, 約壹 over 約
ALT = "|".join(sorted(ALIAS, key=len, reverse=True))

# Real chapter counts. A reference past a book's last chapter is a parse
# artifact, not a citation: 「奧古斯丁算出153是…」 once produced 出埃及記 153.
MAXCHAP = {
    "創世記":50,"出埃及記":40,"利未記":27,"民數記":36,"申命記":34,"約書亞記":24,
    "士師記":21,"路得記":4,"撒母耳記上":31,"撒母耳記下":24,"列王紀上":22,
    "列王紀下":25,"歷代志上":29,"歷代志下":36,"以斯拉記":10,"尼希米記":13,
    "以斯帖記":10,"約伯記":42,"詩篇":150,"箴言":31,"傳道書":12,"雅歌":8,
    "以賽亞書":66,"耶利米書":52,"耶利米哀歌":5,"以西結書":48,"但以理書":12,
    "何西阿書":14,"約珥書":3,"阿摩司書":9,"俄巴底亞書":1,"約拿書":4,"彌迦書":7,
    "那鴻書":3,"哈巴谷書":3,"西番雅書":3,"哈該書":2,"撒迦利亞書":14,"瑪拉基書":4,
    "馬太福音":28,"馬可福音":16,"路加福音":24,"使徒行傳":28,"羅馬書":16,
    "哥林多前書":16,"哥林多後書":13,"加拉太書":6,"以弗所書":6,"腓立比書":4,
    "歌羅西書":4,"帖撒羅尼迦前書":5,"帖撒羅尼迦後書":3,"提摩太前書":6,
    "提摩太後書":4,"提多書":3,"腓利門書":1,"希伯來書":13,"雅各書":5,
    "彼得前書":5,"彼得後書":3,"約翰壹書":5,"約翰貳書":1,"約翰參書":1,
    "猶大書":1,"啟示錄":22,
}

# A one-character abbreviation (出, 拉, 亞, 民, 但 …) also occurs inside ordinary
# words, so it only counts as a citation when it is not preceded by another CJK
# character — 「算出153」 must not read as 出埃及記 153, while 「（出3:14」 must.
CJK = "\u4e00-\u9fff"
SHORT = "|".join(sorted((a for a in ALIAS if len(a) == 1), key=len, reverse=True))
LONG  = "|".join(sorted((a for a in ALIAS if len(a) > 1), key=len, reverse=True))
VERSES = r"(\d+(?:[-–]\d+)?(?:\s*,\s*\d+(?:[-–]\d+)?)*)"
REF = re.compile(
    rf"(?:(?<![{CJK}A-Za-z0-9])({SHORT})|(?<![A-Za-z0-9])({LONG}))"
    rf"\s*(\d+)(?::{VERSES})?(?=\s*章?)"
)

# Skip lines that are the chapter's own Scripture block or its NASB column;
# those are John's text, and John itself is not indexed.
SKIP_PREFIX = ("> ^", "> \\jesus")


def refs_in(text):
    """Yield (full_book, chapter:int, verses:str or None), range-checked."""
    for m in REF.finditer(text):
        alias = m.group(1) or m.group(2)
        chap = int(m.group(3))
        verses = m.group(4)
        full = ALIAS[alias]
        if chap < 1 or chap > MAXCHAP[full]:
            continue          # parse artifact, not a citation
        yield full, chap, verses


def main():
    # ref -> set of chapter labels
    index = defaultdict(set)
    order_seen = {}
    for i, (fname, label) in enumerate(SOURCES):
        p = BOOKDIR / fname
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            s = line.lstrip()
            if s.startswith(SKIP_PREFIX):
                continue
            # a bare 約N:N reference is the Gospel itself; drop those tokens
            cleaned = re.sub(r"(?<![\u4e00-\u9fff])約\s*\d+:\d+(?:[-–]\d+)?", "", line)
            for full, chap, verses in refs_in(cleaned):
                key = (full, chap)
                index[key].add(label)
                order_seen.setdefault(key, i)

    keys = sorted(index, key=lambda k: (ORDER.get(k[0], 999), k[1]))
    if "--stats" in sys.argv:
        books = {k[0] for k in keys}
        print(f"{len(keys)} distinct book-chapters, across {len(books)} books")
        print(f"OT: {sum(1 for k in keys if ORDER[k[0]] < 39)}  "
              f"NT: {sum(1 for k in keys if ORDER[k[0]] >= 39)}")
        return 0

    # labels sort in the order the build script emits them
    LABEL_ORDER = {lbl: i for i, (_, lbl) in enumerate(SOURCES)}

    def chap_sort(lbl):
        return LABEL_ORDER.get(lbl, 999)

    ot = [k for k in keys if ORDER[k[0]] < 39]
    nt = [k for k in keys if ORDER[k[0]] >= 39]
    out = []
    for title, group in (("舊約 Old Testament", ot), ("新約 New Testament", nt)):
        out.append(f"\\section*{{{title}}}\n")
        out.append("{\\small")
        out.append("\\begin{longtable}{@{}p{4.2cm}p{8.6cm}@{}}")
        out.append("\\toprule")
        out.append("\\textbf{經文} & \\textbf{本書討論之處} \\\\")
        out.append("\\midrule")
        out.append("\\endhead")
        for full, chap in group:
            labels = sorted(index[(full, chap)], key=chap_sort)
            out.append(f"{full} {chap} & {'、'.join(labels)} \\\\")
        out.append("\\bottomrule")
        out.append("\\end{longtable}")
        out.append("}\n")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())

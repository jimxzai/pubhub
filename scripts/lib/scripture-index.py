#!/usr/bin/env python3
"""Inject \\index entries for Scripture references into a combined book markdown.

WHY THIS EXISTS
---------------
A study volume is a reference work. The appendix's chapter-level index tells a
reader which CHAPTER discusses a passage; it cannot tell them which PAGE
mentions it. Only a real page-referenced index can, and only LaTeX can build
one, because only LaTeX knows the page numbers.

HOW IT WORKS
    build-<slug>-consolidated.sh calls this on the combined markdown, just
    before handing it to pandoc. For every Scripture reference it recognises it
    appends `\\index[scripture]{...}` right after the reference. pandoc passes
    the raw \\index through to LaTeX; imakeidx collects them and \\printindex
    emits the index with page numbers.

SORTING
    makeindex sorts bytes, so CJK book names would come out in an arbitrary
    order. Every entry therefore carries a numeric sort key before the `@`:

        \\index[scripture]{03@利未記!016:021@16:21}
                           ^^ canonical book order   ^^^^^^^ zero-padded

    giving canonical Bible order at level 1 and numeric verse order at level 2,
    while the reader sees the ordinary Chinese names.

WHAT IS SKIPPED
    * the `## 經文 (Scripture)` block of each chapter — that is the chapter's
      own passage printed in full; indexing every verse of it would bury the
      cross-references a reader actually wants
    * anything inside a fenced code block or a raw LaTeX line
"""
import re
import sys

# canonical order -> the abbreviations this book actually uses
BOOKS = [
    ("01", "創世記", ("創世記", "創")),
    ("02", "出埃及記", ("出埃及記", "出")),
    ("03", "利未記", ("利未記", "利")),
    ("04", "民數記", ("民數記", "民")),
    ("05", "申命記", ("申命記", "申")),
    ("06", "約書亞記", ("約書亞記", "書")),
    ("07", "士師記", ("士師記", "士")),
    ("08", "路得記", ("路得記", "得")),
    ("09", "撒母耳記上", ("撒母耳記上", "撒上")),
    ("10", "撒母耳記下", ("撒母耳記下", "撒下")),
    ("11", "列王紀上", ("列王紀上", "王上")),
    ("12", "列王紀下", ("列王紀下", "王下")),
    ("13", "歷代志上", ("歷代志上", "代上")),
    ("14", "歷代志下", ("歷代志下", "代下")),
    ("15", "以斯拉記", ("以斯拉記", "拉")),
    ("16", "尼希米記", ("尼希米記", "尼")),
    ("17", "以斯帖記", ("以斯帖記", "斯")),
    ("18", "約伯記", ("約伯記", "伯")),
    ("19", "詩篇", ("詩篇", "詩")),
    ("20", "箴言", ("箴言", "箴")),
    ("21", "傳道書", ("傳道書", "傳")),
    ("22", "雅歌", ("雅歌", "歌")),
    ("23", "以賽亞書", ("以賽亞書", "賽")),
    ("24", "耶利米書", ("耶利米書", "耶")),
    ("25", "耶利米哀歌", ("耶利米哀歌", "哀")),
    ("26", "以西結書", ("以西結書", "結")),
    ("27", "但以理書", ("但以理書", "但")),
    ("28", "何西阿書", ("何西阿書", "何")),
    ("29", "約珥書", ("約珥書", "珥")),
    ("30", "阿摩司書", ("阿摩司書", "摩")),
    ("31", "俄巴底亞書", ("俄巴底亞書", "俄")),
    ("32", "約拿書", ("約拿書", "拿")),
    ("33", "彌迦書", ("彌迦書", "彌")),
    ("34", "那鴻書", ("那鴻書", "鴻")),
    ("35", "哈巴谷書", ("哈巴谷書", "哈")),
    ("36", "西番雅書", ("西番雅書", "番")),
    ("37", "哈該書", ("哈該書", "該")),
    ("38", "撒迦利亞書", ("撒迦利亞書", "亞")),
    ("39", "瑪拉基書", ("瑪拉基書", "瑪")),
    ("40", "馬太福音", ("馬太福音", "太")),
    ("41", "馬可福音", ("馬可福音", "可")),
    ("42", "路加福音", ("路加福音", "路")),
    ("43", "約翰福音", ("約翰福音", "約")),
    ("44", "使徒行傳", ("使徒行傳", "徒")),
    ("45", "羅馬書", ("羅馬書", "羅")),
    ("46", "哥林多前書", ("哥林多前書", "林前")),
    ("47", "哥林多後書", ("哥林多後書", "林後")),
    ("48", "加拉太書", ("加拉太書", "加")),
    ("49", "以弗所書", ("以弗所書", "弗")),
    ("50", "腓立比書", ("腓立比書", "腓")),
    ("51", "歌羅西書", ("歌羅西書", "西")),
    ("52", "帖撒羅尼迦前書", ("帖撒羅尼迦前書", "帖前")),
    ("53", "帖撒羅尼迦後書", ("帖撒羅尼迦後書", "帖後")),
    ("54", "提摩太前書", ("提摩太前書", "提前")),
    ("55", "提摩太後書", ("提摩太後書", "提後")),
    ("56", "提多書", ("提多書", "多")),
    ("57", "腓利門書", ("腓利門書", "門")),
    ("58", "希伯來書", ("希伯來書", "來")),
    ("59", "雅各書", ("雅各書", "雅")),
    ("60", "彼得前書", ("彼得前書", "彼前")),
    ("61", "彼得後書", ("彼得後書", "彼後")),
    ("62", "約翰一書", ("約翰一書", "約壹")),
    ("63", "約翰二書", ("約翰二書", "約貳")),
    ("64", "約翰三書", ("約翰三書", "約參")),
    ("65", "猶大書", ("猶大書", "猶")),
    ("66", "啟示錄", ("啟示錄", "啟")),
]

# longest abbreviation first so 林前 wins over 林, 彼前 over 彼, 約壹 over 約
ABBR = []
for order, name, forms in BOOKS:
    for f in forms:
        ABBR.append((f, order, name))
ABBR.sort(key=lambda x: -len(x[0]))

ABBR_ALT = "|".join(re.escape(a) for a, _, _ in ABBR)
LOOKUP = {a: (o, n) for a, o, n in ABBR}

# 利16:21 / 利 16:21 / 來9:12 ; optional verse range, we index the start verse
NAMED_RE = re.compile(rf"(?P<book>{ABBR_ALT})\s?(?P<ch>\d{{1,3}}):(?P<vs>\d{{1,3}})")
# bare 16:21 — inside this book that means Leviticus
BARE_RE = re.compile(r"(?<![\d:：\w])(?P<ch>\d{1,2}):(?P<vs>\d{1,3})(?![\d:])")


def entry(order, name, ch, vs):
    return (f"\\index[scripture]{{{order}@{name}!"
            f"{int(ch):03d}:{int(vs):03d}@{ch}:{vs}}}")


def main(path):
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    out = []
    in_scripture = False   # inside a chapter's own `## 經文` section
    n_named = n_bare = 0

    for line in lines:
        if line.startswith("## "):
            in_scripture = line.startswith("## 經文")
        # a new chapter resets the state
        if line.startswith("# "):
            in_scripture = False

        skip = (
            in_scripture
            or line.startswith("\\")          # raw LaTeX
            or line.strip().startswith("```")
            or not line.strip()
        )
        if skip:
            out.append(line)
            continue

        pieces = []
        last = 0
        # named references first, and remember their spans so the bare pass
        # does not double-index the "16:21" inside "利16:21"
        spans = []
        for m in NAMED_RE.finditer(line):
            order, name = LOOKUP[m.group("book")]
            pieces.append(line[last:m.end()])
            pieces.append(entry(order, name, m.group("ch"), m.group("vs")))
            last = m.end()
            spans.append((m.start(), m.end()))
            n_named += 1
        pieces.append(line[last:])
        merged = "".join(pieces)

        # bare refs: re-scan the ORIGINAL line, then splice into merged only
        # where they fall outside a named-reference span
        bare = []
        for m in BARE_RE.finditer(line):
            if any(s <= m.start() < e for s, e in spans):
                continue
            bare.append(m)
        if bare:
            pieces = []
            last = 0
            for m in bare:
                pieces.append(line[last:m.end()])
                pieces.append(entry("03", "利未記", m.group("ch"), m.group("vs")))
                last = m.end()
                n_bare += 1
            pieces.append(line[last:])
            merged = "".join(pieces)
            # if both kinds occurred on one line, redo named on the spliced text
            if spans:
                res, last = [], 0
                for m in NAMED_RE.finditer(merged):
                    if "\\index" in merged[m.end():m.end() + 8]:
                        continue
                    order, name = LOOKUP[m.group("book")]
                    res.append(merged[last:m.end()])
                    res.append(entry(order, name, m.group("ch"), m.group("vs")))
                    last = m.end()
                res.append(merged[last:])
                merged = "".join(res)

        out.append(merged)

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))

    print(f"  scripture index: {n_named} named + {n_bare} bare reference(s) marked")


if __name__ == "__main__":
    main(sys.argv[1])

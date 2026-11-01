#!/usr/bin/env python3
"""Generate books/bible/Zechariah/98-appendix-indices.md from the chapter files.

The indices point to chapters, not pages: Zechariah is short enough that a
chapter locator is precise, and a chapter locator cannot go stale when a
page moves (cf. build-2-peter-index.py, whose page numbers need a three-pass
rebuild). Re-run after any content edit:

    python3 scripts/gen-zechariah-indices.py          # rewrite the appendix
    python3 scripts/gen-zechariah-indices.py --check  # exit 1 if it is stale
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books/bible/zechariah"
OUT = BOOK / "98-appendix-indices.md"

# Files indexed, with the label printed in the index. Chapter files are
# discovered by glob (NN-*.md) so a renamed chapter file cannot silently
# drop out of the index.
SOURCES = [
    ("00-overview.md", "概覽"),
    ("00a-zechariah-position.md", "位置"),
    ("00c-revelation-order.md", "骨幹"),
]
CHAPTERS = []
for _f in sorted(BOOK.glob("[0-9][0-9]-*.md")):
    _n = int(_f.name[:2])
    if 1 <= _n <= 19:
        SOURCES.append((_f.name, f"第{_n}章"))
        CHAPTERS.append((_n, _f))

# Canonical order of CUV book abbreviations as used in this book's prose.
BOOKS = """創 出 利 民 申 書 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 詩 箴 傳 歌
賽 耶 哀 結 但 何 珥 摩 俄 拿 彌 鴻 哈 番 該 亞 瑪
太 可 路 約 徒 羅 林前 林後 加 弗 腓 西 帖前 帖後 提前 提後 多 門 來 雅
彼前 彼後 約壹 約貳 約參 猶 啟""".split()
ORDER = {b: i for i, b in enumerate(BOOKS)}
# Longest abbreviations first so 約壹 is not read as 約.
ALIAS = {"詩篇": "詩", "約一": "約壹"}
BOOK_RE = "|".join(sorted(BOOKS + list(ALIAS), key=len, reverse=True))
REF = re.compile(
    rf"(?:(?<![一-鿿])|(?<=[與及和在是見至並的或又也從如按依即由到對向跟]))"
    rf"({BOOK_RE})(\d+)(?::(\d+)(?:[-–](\d+))?)?"
)
# Chapters per book, to reject text like 「但13:1」(連詞「但」) or 「加9:13」(「加」＝加上).
MAXCH = dict(zip(BOOKS, [50,40,27,36,34,24,21,4,31,24,22,25,29,36,10,13,10,42,150,31,12,8,66,52,5,48,12,14,3,9,1,4,7,3,3,3,2,14,4,28,16,24,21,28,16,16,13,6,6,4,4,5,3,6,4,3,1,13,5,5,3,5,1,1,1,22]))


TOPICS = [
    ("萬軍之耶和華（יְהוָה צְבָאוֹת）", ["萬軍之耶和華", "萬軍的耶和華"]),
    ("在那日（בַּיּוֹם הַהוּא）", ["在那日", "那日", "當那日"]),
    ("轉向、回頭（שׁוּב）", ["שׁוּב"]),
    ("住在你中間（שָׁכַן）", ["住在你中間", "住在我們中間", "要住在", "同住"]),
    ("「差遣我」的句子", ["差遣我", "差遣了我", "差遣我到"]),
    ("苗（צֶמַח）", ["苗裔", "那苗", "苗」"]),
    ("約書亞（大祭司）", ["大祭司約書亞", "約書亞與"]),
    ("所羅巴伯", ["所羅巴伯"]),
    ("撒但", ["撒但"]),
    ("耶和華的使者、天使", ["使者", "天使"]),
    ("金燈臺與兩棵橄欖樹", ["燈臺", "橄欖樹"]),
    ("準繩、量", ["準繩", "量器"]),
    ("馬與車", ["紅馬", "四輛", "戰車", "馬的鈴鐺"]),
    ("靈（רוּחַ）", ["我的靈", "恩惠的靈", "聖靈", "懇求的靈"]),
    ("七十年", ["七十年"]),
    ("禁食", ["禁食"]),
    ("擔子（מַשָּׂא）", ["擔子"]),
    ("王（מֶלֶךְ）", ["你的王", "王騎", "作全地的王", "那位王"]),
    ("牧人與群羊（רָעָה）", ["牧人", "群羊", "羣羊"]),
    ("三十塊錢", ["三十塊錢", "三十舍客勒"]),
    ("窯戶", ["窯戶"]),
    ("被扎、仰望", ["所扎", "仰望"]),
    ("泉源", ["泉源"]),
    ("橄欖山", ["橄欖山"]),
    ("歸耶和華為聖", ["歸耶和華為聖", "歸萬軍之耶和華為聖"]),
    ("耶路撒冷、錫安", ["耶路撒冷", "錫安"]),
    ("迦南人", ["迦南人"]),
    ("住棚節", ["住棚節"]),
    ("麥克阿瑟的讀法（分別主義、前千禧年）", ["前千禧年", "分別主義"]),
    ("年代與作者", ["年代", "作者"]),
]


def body(text):
    """Drop YAML and the Scripture section (the Jude text itself would make
    every Jude verse appear in every chapter)."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    return re.sub(r"\n## 經文 \(Scripture\)\n.*?(?=\n## )", "\n", text, flags=re.S)


def build():
    refs = defaultdict(set)
    topics = defaultdict(list)
    for fname, label in SOURCES:
        text = body((BOOK / fname).read_text(encoding="utf-8"))
        for m in REF.finditer(text):
            b, c, v1, v2 = m.groups()
            b = ALIAS.get(b, b)
            if b == "亞":
                continue  # Zechariah itself is indexed by section below
            if int(c) > MAXCH[b]:
                continue
            key = (ORDER[b], int(c), int(v1) if v1 else 0, int(v2) if v2 else 0, b, c, v1 or '', v2 or '')
            refs[key].add(label)
        for name, words in TOPICS:
            if any(w in text for w in words):
                topics[name].append(label)

    order = [lab for _, lab in SOURCES]
    lines = [
        "---",
        "title: 撒迦利亞書研讀",
        "subtitle: The Book of Zechariah Deep Study",
        "author: PubHub 三書精讀系統",
        "date: 2026年10月",
        "publisher: 三書精讀出版系統",
        "---",
        "",
        "# 附錄：經文與主題索引 (Appendix: Indices)",
        "",
        "> 本索引由 `scripts/gen-zechariah-indices.py` 從各章正文自動產生，不是手工維護。索引指向章，不指向頁碼——全書十九章，"
        "章的定位已經足夠精確，也不會因排版移動而失效。「概覽」「位置」「骨幹」指卷首三章。",
        "",
        "## 一、撒迦利亞書逐節索引",
        "",
        "| 經文 | 所在章 | 主題 |",
        "|------------|------------|--------------------------------------------------------|",
    ]
    for n, f in CHAPTERS:
        txt = f.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", txt, re.M).group(1)
        h1 = re.sub(r"\s*\(.*\)\s*$", "", h1)
        ref = re.search(r"^撒迦利亞書 (\S+)", txt, re.M).group(1)
        lines.append(f"| {ref} | 第{n}章 | {h1} |")
    lines += [
        "",
        "## 二、其他經卷索引",
        "",
        "| 經文 | 出現於 |",
        "|------------------------|--------------------------------------------------------|",
    ]
    for key in sorted(refs):
        _, _, _, _, b, c, v1, v2 = key
        ref = f"{b}{c}" + (f":{v1}" if v1 else "") + (f"-{v2}" if v2 else "")
        where = "、 ".join(lab for lab in order if lab in refs[key])
        lines.append(f"| {ref} | {where} |")
    lines += ["", "## 三、主題索引", "", "| 主題 | 出現於 |", "|--------------------------------|------------------------------------------------|"]
    for name, _ in TOPICS:
        if topics[name]:
            lines.append(f"| {name} | {'、 '.join(topics[name])} |")
    return "\n".join(lines) + "\n"


def main():
    new = build()
    if "--check" in sys.argv:
        old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if old != new:
            print("STALE: 98-appendix-indices.md does not match the chapters; run scripts/gen-zechariah-indices.py")
            sys.exit(1)
        print("indices current")
        return
    OUT.write_text(new, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({new.count(chr(10))} lines)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate books/bible/john1/98-appendix-indices.md from the chapter files.

Adapted from scripts/gen-john1-indices.py (2026-10-01). Chapter locators,
not pages: six chapters are precise enough, and a chapter locator cannot go
stale when a page moves. The build script runs this before every build.
Bare "N:N" references inside a chapter are 1 John's own verses (prose cites
other books with a CUV abbreviation prefix); 約壹N:N is folded in with them.

    python3 scripts/gen-john1-indices.py          # rewrite the appendix
    python3 scripts/gen-john1-indices.py --check  # exit 1 if it is stale
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books/bible/john1"
OUT = BOOK / "98-appendix-indices.md"

# Files indexed, with the label printed in the index.
SOURCES = [
    ("00c-revelation-order.md", "骨幹"),
    ("01-word-of-life.md", "第1章"),
    ("02-god-is-light.md", "第2章"),
    ("03-abide-in-him.md", "第3章"),
    ("04-children-of-god.md", "第4章"),
    ("05-god-is-love.md", "第5章"),
    ("06-that-you-may-know.md", "第6章"),
]
# Which book chapter is the home of each 1 John verse (chapter, first, last).
HOME = [("第1章", (1, 1), (1, 4)), ("第2章", (1, 5), (2, 11)), ("第3章", (2, 12), (2, 29)),
        ("第4章", (3, 1), (3, 24)), ("第5章", (4, 1), (4, 21)), ("第6章", (5, 1), (5, 21))]
BARE = re.compile(r"(?<![一-鿿0-9:：.])(?<![一-鿿] )([1-5]):(\d{1,2})(?![0-9])")


VERSES = {1: 10, 2: 29, 3: 24, 4: 21, 5: 21}  # 1 John chapter lengths


def home(c, v):
    # A bare reference outside 1 John's real verse range (e.g. 1:14 in a
    # John-vs-1-John comparison table) is not a 1 John verse: drop it.
    if v < 1 or v > VERSES.get(c, 0):
        return None
    for lab, a, b in HOME:
        if a <= (c, v) <= b:
            return lab
    return None

# Canonical order of CUV book abbreviations as used in this book's prose.
BOOKS = """創 出 利 民 申 書 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 詩 箴 傳 歌
賽 耶 哀 結 但 何 珥 摩 俄 拿 彌 鴻 哈 番 該 亞 瑪
太 可 路 約 徒 羅 林前 林後 加 弗 腓 西 帖前 帖後 提前 提後 多 門 來 雅
彼前 彼後 約壹 約貳 約參 猶 啟""".split()
ORDER = {b: i for i, b in enumerate(BOOKS)}
# Longest abbreviations first so 約壹 is not read as 約.
ALIAS = {"詩篇": "詩"}
BOOK_RE = "|".join(sorted(BOOKS + list(ALIAS), key=len, reverse=True))
REF = re.compile(rf"(?<![一-鿿])({BOOK_RE})(\d{{1,3}})(?::(\d+)(?:[-–](\d+))?)?(?!\d)")

TOPICS = [
    ("相交（κοινωνία）", ["相交", "κοινωνία"]),
    ("光與黑暗", ["神就是光", "在光明中"]),
    ("認罪（ὁμολογέω）", ["認罪", "ὁμολογέω"]),
    ("中保（παράκλητος）", ["中保", "παράκλητος"]),
    ("挽回祭（ἱλασμός）", ["挽回祭", "ἱλασμός"]),
    ("新命令、舊命令", ["新命令", "舊命令"]),
    ("世界（κόσμος）", ["不要愛世界", "κόσμος", "勝過世界", "全世界"]),
    ("敵基督", ["敵基督"]),
    ("恩膏（χρῖσμα）", ["恩膏", "χρῖσμα"]),
    ("住在主裏面（μένω）", ["住在主裏面", "μένω"]),
    ("神的兒女", ["神的兒女"]),
    ("不犯罪的張力", ["不犯罪"]),
    ("該隱", ["該隱"]),
    ("試驗諸靈", ["試驗那些靈", "試驗諸靈"]),
    ("成了肉身", ["成了肉身"]),
    ("神就是愛", ["神就是愛"]),
    ("愛裏沒有懼怕", ["愛裏沒有懼怕", "把懼怕除去"]),
    ("水、血與聖靈", ["水和血", "水與血"]),
    ("約翰短句（Comma Johanneum）", ["Comma", "約翰短句"]),
    ("至於死的罪", ["至於死的罪"]),
    ("確據、知道有永生", ["確據", "知道自己有永生"]),
    ("偶像", ["偶像"]),
    ("克林妥", ["克林妥", "Cerinthus"]),
    ("奧古斯丁", ["奧古斯丁"]),
    ("加爾文", ["加爾文"]),
    ("摩根", ["摩根"]),
    ("麥克阿瑟", ["麥克阿瑟"]),
]


def body(text):
    """Drop YAML and the Scripture section (the Jude text itself would make
    every Jude verse appear in every chapter)."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    return re.sub(r"\n## 經文 \(Scripture\)\n.*?(?=\n## )", "\n", text, flags=re.S)


def build():
    refs = defaultdict(set)
    own = defaultdict(set)
    topics = defaultdict(list)
    for fname, label in SOURCES:
        text = body((BOOK / fname).read_text(encoding="utf-8"))
        for m in REF.finditer(text):
            b, c, v1, v2 = m.groups()
            b = ALIAS.get(b, b)
            if b == "約壹":
                if v1:
                    own[(int(c), int(v1))].add(label)
                continue
            key = (ORDER[b], int(c), int(v1) if v1 else 0, int(v2) if v2 else 0, b, c, v1 or '', v2 or '')
            refs[key].add(label)
        stripped = REF.sub("", text)
        for m in BARE.finditer(stripped):
            c, v = int(m.group(1)), int(m.group(2))
            if home(c, v):
                own[(c, v)].add(label)
        for name, words in TOPICS:
            if any(w in text for w in words):
                topics[name].append(label)

    order = [lab for _, lab in SOURCES]
    lines = [
        "---",
        "title: 約翰一書研讀",
        "subtitle: 1 John Deep Study",
        "author: PubHub 三書精讀系統",
        "date: 2026年10月",
        "publisher: 三書精讀出版系統",
        "---",
        "",
        "# 附錄：經文與主題索引 (Appendix: Indices) {.unnumbered}",
        "",
        "> 本索引由 `scripts/gen-john1-indices.py` 從各章正文自動產生，不是手工維護；"
        "建置腳本每次建書前都會重新產生。索引指向章，不指向頁碼。"
        "「骨幹」指卷首〈啟示的次序與神的計劃〉。各章自己經文範圍內的經節不列入第二部分。",
        "",
        "## 一、約翰一書分段與本書章次",
        "",
        "| 經文 | 所在章 | 啟示的次序 |",
        "|--------------|----------|------------------------------------------|",
        "| 1:1-4 | 第1章 | 第一步 顯現 |",
        "| 1:5-2:11 | 第2章 | 第二步 光照 |",
        "| 2:12-29 | 第3章 | 第三步 內住 |",
        "| 3:1-24 | 第4章 | 第四步 兒女 |",
        "| 4:1-21 | 第5章 | 第五步 先愛 |",
        "| 5:1-21 | 第6章 | 第六步 見證 |",
        "",
        "## 二、約翰一書經節的跨章引用",
        "",
        "| 經節 | 另見 |",
        "|----------------------|----------------------------------------------------------|",
    ]
    for (c, v) in sorted(own):
        others = [lab for lab in order if lab in own[(c, v)] and lab != home(c, v)]
        if others:
            lines.append(f"| {c}:{v}（{home(c, v)}） | {'、'.join(others)} |")
    lines += ["", "## 三、其他經卷索引", "", "| 經文 | 出現於 |", "|----------------------|----------------------------------------------------------|"]
    # Fold a reference into a range that contains it (創4:4-5 into 創4:3-9),
    # so the index lists each passage once with every chapter that cites it.
    def span(k):
        v1, v2 = k[2], k[3]
        return (v1, v2 or v1) if v1 else None
    keys = sorted(refs)
    for k in keys:
        if span(k) is None:
            continue
        for big in keys:
            if big is k or big[:2] != k[:2] or span(big) is None or big not in refs:
                continue
            (a1, a2), (b1, b2) = span(k), span(big)
            if b1 <= a1 and a2 <= b2 and (b1, b2) != (a1, a2):
                refs[big] |= refs.pop(k)
                break
    for key in sorted(refs):
        _, _, _, _, b, c, v1, v2 = key
        ref = f"{b}{c}" + (f":{v1}" if v1 else "") + (f"-{v2}" if v2 else "")
        where = "、".join(lab for lab in order if lab in refs[key])
        lines.append(f"| {ref} | {where} |")
    lines += ["", "## 四、主題索引", "", "| 主題 | 出現於 |", "|------------------------------|--------------------------------------------------|"]
    for name, _ in TOPICS:
        if topics[name]:
            lines.append(f"| {name} | {'、'.join(topics[name])} |")
    return "\n".join(lines) + "\n"


def main():
    new = build()
    if "--check" in sys.argv:
        old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if old != new:
            print("STALE: 98-appendix-indices.md does not match the chapters; run scripts/gen-john1-indices.py")
            sys.exit(1)
        print("indices current")
        return
    OUT.write_text(new, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({new.count(chr(10))} lines)")


if __name__ == "__main__":
    main()

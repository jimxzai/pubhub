#!/usr/bin/env python3
"""Generate books/bible/habakkuk/98-appendix-indices.md from the chapter files.

The indices point to chapters, not pages: Habakkuk is short enough that a
chapter locator is precise, and a chapter locator cannot go stale when a
page moves (cf. build-2-peter-index.py, whose page numbers need a three-pass
rebuild). Re-run after any content edit:

    python3 scripts/gen-habakkuk-indices.py          # rewrite the appendix
    python3 scripts/gen-habakkuk-indices.py --check  # exit 1 if it is stale
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books/bible/habakkuk"
OUT = BOOK / "98-appendix-indices.md"

# Files indexed, with the label printed in the index.
SOURCES = [
    ("00-overview.md", "概覽"),
    ("00a-habakkuk-position.md", "位置"),
    ("00c-revelation-order.md", "骨幹"),
    ("01-how-long.md", "第一章"),
    ("02-a-work-you-would-not-believe.md", "第二章"),
    ("03-i-will-stand-at-my-watch.md", "第三章"),
    ("04-the-righteous-shall-live.md", "第四章"),
    ("05-woe-and-the-silence.md", "第五章"),
    ("06-i-have-heard-your-report.md", "第六章"),
    ("07-yet-i-will-rejoice.md", "第七章"),
]

# Canonical order of CUV book abbreviations as used in this book's prose.
BOOKS = """創 出 利 民 申 書 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 詩 箴 傳 歌
賽 耶 哀 結 但 何 珥 摩 俄 拿 彌 鴻 哈 番 該 亞 瑪
太 可 路 約 徒 羅 林前 林後 加 弗 腓 西 帖前 帖後 提前 提後 多 門 來 雅
彼前 彼後 約壹 約貳 約參 猶 啟""".split()
ORDER = {b: i for i, b in enumerate(BOOKS)}
# Longest abbreviations first so 約壹 is not read as 約.
ALIAS = {"詩篇": "詩", "約一": "約壹"}
BOOK_RE = "|".join(sorted(BOOKS + list(ALIAS), key=len, reverse=True))
REF = re.compile(rf"(?<![一-鿿])({BOOK_RE})(\d+)(?::(\d+)(?:[-–](\d+))?)?")

TOPICS = [
    ("要到幾時（עַד־אָנָה）", ["要到幾時", "要等到幾時"]),
    ("強暴（חָמָס）", ["強暴", "חָמָס"]),
    ("不應允、聽見（שָׁמַע）", ["不應允", "聽見了", "שָׁמַע"]),
    ("拯救、救我的神（יָשַׁע）", ["拯救", "救我的神", "יֵשַׁע", "יָשַׁע"]),
    ("看見、觀看（רָאָה／נָבַט）", ["使我看見", "觀看", "看著不理", "רָאָה", "נָבַט"]),
    ("守望所、望樓", ["守望所", "望樓", "守望"]),
    ("異象（חָזוֹן）", ["異象", "חָזוֹן"]),
    ("等候", ["等候"]),
    ("義人（צַדִּיק）", ["義人", "צַדִּיק"]),
    ("因信得生、信（אֱמוּנָה）", ["因信得生", "אֱמוּנָה", "信實"]),
    ("迦勒底人", ["迦勒底"]),
    ("律法、公理（מִשְׁפָּט）", ["公理", "מִשְׁפָּט"]),
    ("出來（יָצָא）", ["יָצָא", "出來"]),
    ("網、向網獻祭", ["向網", "網羅", "那網"]),
    ("禍哉（הוֹי）", ["禍哉", "הוֹי"]),
    ("肅靜（הָס）", ["肅靜", "靜默", "הָס"]),
    ("聖殿", ["聖殿"]),
    ("榮耀的知識充滿遍地", ["榮耀的知識", "充滿遍地"]),
    ("杯", ["那杯", "這杯", "酒杯", "忿怒之杯", "右手的杯"]),
    ("偶像、木偶", ["偶像", "木偶"]),
    ("耶和華的作為（פָּעַל）", ["作為", "行一件事", "פָּעַל"]),
    ("細拉、伶長、歌", ["細拉", "伶長"]),
    ("提幔、巴蘭山", ["提幔", "巴蘭"]),
    ("出埃及、紅海", ["紅海", "出埃及"]),
    ("日月停住", ["日月"]),
    ("受膏者（מָשִׁיחַ）", ["受膏者"]),
    ("歡欣、喜樂", ["歡欣", "喜樂"]),
    ("無花果樹、橄欖樹（農作失收）", ["無花果", "橄欖"]),
    ("母鹿的蹄、高處", ["母鹿", "高處"]),
    ("新約引用：徒13:41、羅1:17、加3:11、來10:37-38", ["徒13:41", "羅1:17", "加3:11", "來10:38", "來10:37"]),
    ("殉道者的問題（啟6:10）", ["啟6:10", "啟6:9"]),
    ("奧古斯丁《上帝之城》", ["奧古斯丁"]),
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
            if b == "哈":
                continue  # Habakkuk itself is indexed by section below
            key = (ORDER[b], int(c), int(v1) if v1 else 0, int(v2) if v2 else 0, b, c, v1 or '', v2 or '')
            refs[key].add(label)
        for name, words in TOPICS:
            if any(w in text for w in words):
                topics[name].append(label)

    order = [lab for _, lab in SOURCES]
    lines = [
        "---",
        "title: 哈巴谷書研讀",
        "subtitle: The Book of Habakkuk Deep Study",
        "author: PubHub 三書精讀系統",
        "date: 2026年10月",
        "publisher: 三書精讀出版系統",
        "---",
        "",
        "# 附錄：經文與主題索引 (Appendix: Indices)",
        "",
        "> 本索引由 `scripts/gen-habakkuk-indices.py` 從各章正文自動產生，不是手工維護；"
        "改動任何一章之後重新執行即可。索引指向章，不指向頁碼——全書七章，"
        "章的定位已經足夠精確，也不會因排版移動而失效。「概覽」「位置」「骨幹」指卷首三章。",
        "",
        "## 一、哈巴谷書逐節索引",
        "",
        "| 經文 | 所在章 | 主題 |",
        "|------------|------------|--------------------------------------------------------|",
        "| 1:1-4 | 第一章 | 你不應允，要到幾時呢？——三項控告 |",
        "| 1:5-11 | 第二章 | 我行一件事，你們總是不信——神的第一個回答 |",
        "| 1:12-2:1 | 第三章 | 你眼目清潔，為何看著不理——再問，然後上守望所 |",
        "| 2:2-5 | 第四章 | 寫下異象；雖然遲延，還要等候；義人因信得生 |",
        "| 2:6-20 | 第五章 | 五個禍哉；全地都當在他面前肅靜 |",
        "| 3:1-15 | 第六章 | 我聽見了你的名聲——神來了 |",
        "| 3:16-19 | 第七章 | 然而，我要因耶和華歡欣 |",
        "",
        "## 二、其他經卷索引",
        "",
        "| 經文 | 出現於 |",
        "|------------------------|--------------------------------------------------------|",
    ]
    for key in sorted(refs):
        _, _, _, _, b, c, v1, v2 = key
        ref = f"{b}{c}" + (f":{v1}" if v1 else "") + (f"-{v2}" if v2 else "")
        where = "、".join(lab for lab in order if lab in refs[key])
        lines.append(f"| {ref} | {where} |")
    lines += ["", "## 三、主題索引", "", "| 主題 | 出現於 |", "|--------------------------------|------------------------------------------------|"]
    for name, _ in TOPICS:
        if topics[name]:
            lines.append(f"| {name} | {'、'.join(topics[name])} |")
    return "\n".join(lines) + "\n"


def main():
    new = build()
    if "--check" in sys.argv:
        old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if old != new:
            print("STALE: 98-appendix-indices.md does not match the chapters; run scripts/gen-habakkuk-indices.py")
            sys.exit(1)
        print("indices current")
        return
    OUT.write_text(new, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({new.count(chr(10))} lines)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate 96-appendix-5-scripture-index.md for Biblegreek from the book's own Part-1 text (derived, never hand-kept).
Scans chapters and appendices of Part One for Scripture references (Chinese abbreviations and English names) and
lists each reference with the chapters where it appears. Part Two (p2-*) is excluded: it is organised by book already."""
import collections, glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "books/bible/Biblegreek")
BOOKS = [("創", "Genesis"), ("出", "Exodus"), ("利", "Leviticus"), ("民", "Numbers"), ("申", "Deuteronomy"), ("書", "Joshua"),
         ("詩", "Psalm"), ("箴", "Proverbs"), ("賽", "Isaiah"), ("耶", "Jeremiah"), ("結", "Ezekiel"), ("但", "Daniel"),
         ("太", "Matthew"), ("可", "Mark"), ("路", "Luke"), ("約", "John"), ("徒", "Acts"), ("羅", "Romans"),
         ("林前", "1 Corinthians"), ("林後", "2 Corinthians"), ("加", "Galatians"), ("弗", "Ephesians"), ("腓", "Philippians"),
         ("西", "Colossians"), ("帖前", "1 Thessalonians"), ("帖後", "2 Thessalonians"), ("提前", "1 Timothy"),
         ("提後", "2 Timothy"), ("多", "Titus"), ("門", "Philemon"), ("來", "Hebrews"), ("雅", "James"), ("彼前", "1 Peter"),
         ("彼後", "2 Peter"), ("約壹", "1 John"), ("約貳", "2 John"), ("約參", "3 John"), ("猶", "Jude"), ("啟", "Revelation")]
ZH = {z: i for i, (z, e) in enumerate(BOOKS)}
EN = {e: i for i, (z, e) in enumerate(BOOKS)}
zh_alt = "|".join(sorted(ZH, key=len, reverse=True))
en_alt = "|".join(sorted(EN, key=len, reverse=True))
RX = re.compile(rf"(?:({zh_alt})\s?|\b({en_alt})\s)(\d{{1,3}})\s?[:：]\s?(\d{{1,3}})(?:\s?[-–]\s?(\d{{1,3}}))?")
LABEL = {"000-preface": "前言", "00c-revelation-order": "骨幹章", "04b-basic-grammar": "第 4 章（續）", "96-appendix-1-reading-map": "讀經地圖附錄",
         "96-appendix-2-practice": "練習附錄", "96-appendix-3-word-contexts": "核心字附錄", "98-appendix-sources": "來源附錄", "999-afterword": "跋"}


def label(name):
    if name in LABEL: return LABEL[name]
    m = re.match(r"(\d\d)-", name)
    return f"第 {int(m.group(1))} 章" if m else name


def main():
    hits = collections.defaultdict(lambda: collections.defaultdict(set))   # (book,ch,v1,v2) -> label -> {}
    files = [f for f in sorted(glob.glob(os.path.join(D, "[0-9]*.md"))) if not os.path.basename(f).startswith(("96-appendix-4", "97-", "96-appendix-5", "96-appendix-6"))]
    for f in files:
        name = os.path.basename(f)[:-3]
        text = open(f, encoding="utf-8").read()
        text = text.split("\n---\n", 2)[-1] if text.startswith("---") else text
        for m in RX.finditer(text):
            z, e, ch, v1, v2 = m.groups()
            if z in ("出", "多", "來", "但", "加", "書", "西", "門", "民", "利", "結") and m.start() and text[m.start() - 1] in "不看說指找讀查寫算數演走拿提發露顯表現輸傳":
                continue   # 看不出 1:3 is not Exodus 1:3: these common characters count only when not glued to a preceding word
            b = ZH[z] if z else EN[e]
            v2 = int(v2) if v2 and int(v2) > int(v1) else int(v1)
            hits[(b, int(ch), int(v1), v2)][label(name)].add(name)
    rows = []
    for key in sorted(hits):
        b, ch, v1, v2 = key
        ref = f"{BOOKS[b][0]} {ch}:{v1}" + (f"-{v2}" if v2 != v1 else "")
        labs = sorted(hits[key], key=lambda l: [os.path.basename(f)[:-3] for f in files if l == label(os.path.basename(f)[:-3])][0])
        rows.append(f"| {ref} | {'、'.join(labs)} |")
    out = ["---", "title: 附錄", "subtitle: 經文索引", "author: PubHub 三書精讀系統", "date: 2026年11月", "publisher: 三書精讀出版系統", "---", "",
           "# 經文索引 (Scripture Index) {.unnumbered}", "",
           f"卷一各章與附錄裏明引的經文出處，共 {len(rows)} 處，由程式從書稿掃描產生，指向章次而非頁碼。只掃描「書卷簡稱＋章:節」寫法（如「約 1:1」「John 1:1」）；沒有寫出處的間接提及不收。卷二（各卷的希臘文）已按書卷編排，不在此列。", "",
           "| 經文 | 見於 |", "|" + "-" * 30 + "|" + "-" * 70 + "|"] + rows
    open(os.path.join(D, "96-appendix-5-scripture-index.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("scripture index rows", len(rows))
    topics([f for f in files if not os.path.basename(f).startswith("96-appendix-6")])


TOPICS = [  # topic -> keywords that must literally appear in the text (derived, so the index cannot point at a chapter that lacks the word)
    ("字母、發音、重音、氣號", ["字母", "氣號", "重音"]), ("格（主格、屬格、與格、對格、呼格）", ["主格", "屬格", "與格", "對格", "呼格"]),
    ("冠詞", ["冠詞"]), ("名詞與詞尾", ["詞尾"]), ("動詞時態與「動作的樣子」（體）", ["未完成式", "完成式", "簡單過去式", "動作樣子", "動作的樣子"]),
    ("語態（主動、中間、被動）", ["中間語態", "被動語態", "主動語態", "語態"]), ("語氣與分詞", ["命令語氣", "虛擬語氣", "分詞"]),
    ("字根謬誤與字源", ["字根謬誤", "字源"]), ("時代錯置", ["時代錯置"]), ("愛的兩個動詞（ἀγαπάω 與 φιλέω）", ["φιλέω"]),
    ("共同語（Koine）", ["Koine", "共同語"]), ("對照本與詞典", ["對照本", "詞典"]), ("強氏編號", ["強氏"]),
    ("譯本比較（和合本、NASB）", ["和合本", "NASB"]), ("四步階梯", ["四步階梯"]), ("MorphGNT／SBLGNT 語料", ["MorphGNT", "SBLGNT"]), ("七十士譯本", ["七十士"]),
    ("歌與記憶", ["核心字歌", "Doxology", "奇異恩典", "Kyrie"]), ("八週計劃", ["八週"]), 
]


def topics(files):
    texts = {}
    for f in files:
        n = os.path.basename(f)[:-3]
        t = open(f, encoding="utf-8").read()
        texts[n] = (label(n), t.split("\n---\n", 2)[-1] if t.startswith("---") else t)
    skip = ("96-appendix-3", "96-appendix-4", "98-", "999-")
    rows = []
    for name, kws in TOPICS:
        labs = []
        for n, (lab, t) in texts.items():
            if n.startswith(skip) or n.startswith("000-"):
                continue
            if any(k in t for k in kws):
                labs.append(lab)
        if labs:
            rows.append(f"| {name} | {'、'.join(labs)} |")
    out = ["---", "title: 附錄", "subtitle: 主題索引", "author: PubHub 三書精讀系統", "date: 2026年11月", "publisher: 三書精讀出版系統", "---", "",
           "# 主題索引 (Topic Index) {.unnumbered}", "",
           "下列主題，由程式檢查卷一各章的文字裏是否真的出現該主題的關鍵詞後列出，指向章次而非頁碼；關鍵詞表是編者定的，只涵蓋本書的主要主題。出現只是提到，不一定是專門講解。", "",
           "| 主題 | 見於 |", "|" + "-" * 30 + "|" + "-" * 70 + "|"] + rows
    open(os.path.join(D, "96-appendix-6-topic-index.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("topic index rows", len(rows), "of", len(TOPICS))


if __name__ == "__main__":
    main()

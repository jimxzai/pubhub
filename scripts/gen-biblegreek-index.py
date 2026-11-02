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
RX = re.compile(rf"(?:(?<![一-鿿])({zh_alt})\s?|\b({en_alt})\s)(\d{{1,3}})\s?[:：]\s?(\d{{1,3}})(?:\s?[-–]\s?(\d{{1,3}}))?")
LABEL = {"000-preface": "前言", "00c-revelation-order": "骨幹章", "04b-basic-grammar": "第 4 章（續）", "96-appendix-1-reading-map": "附錄一",
         "96-appendix-2-practice": "附錄二", "96-appendix-3-word-contexts": "附錄三", "98-appendix-sources": "附錄來源", "999-afterword": "跋"}


def label(name):
    if name in LABEL: return LABEL[name]
    m = re.match(r"(\d\d)-", name)
    return f"第 {int(m.group(1))} 章" if m else name


def main():
    hits = collections.defaultdict(lambda: collections.defaultdict(set))   # (book,ch,v1,v2) -> label -> {}
    files = [f for f in sorted(glob.glob(os.path.join(D, "[0-9]*.md"))) if not os.path.basename(f).startswith(("96-appendix-4", "97-", "96-appendix-5"))]
    for f in files:
        name = os.path.basename(f)[:-3]
        text = open(f, encoding="utf-8").read()
        text = text.split("\n---\n", 2)[-1] if text.startswith("---") else text
        for m in RX.finditer(text):
            z, e, ch, v1, v2 = m.groups()
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


if __name__ == "__main__":
    main()

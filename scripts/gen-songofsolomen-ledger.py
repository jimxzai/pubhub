#!/usr/bin/env python3
"""Generate the Song of Songs volume's citation ledger (99-appendix-references.md) from the book's own text.

The ledger is the honesty account for the promise 「不編造一段出處」. A hand-kept ledger
drifts from the chapters (Luke declared zero Morgan quotes and carried 29), so every
count and every source line below is read back out of the book files.

How quotes are found: every `> "…"` block in a chapter or front-matter file, followed by its
`> — source` line, is classified by that source line (a 「同上」 line inherits the previous
quote's owner). The 經文 and 配詩 sections are skipped (Scripture blocks and hymn stanzas are
not commentary). Chapters 11-12 arrange 歷代注疏 by topic, so section headings are not trusted.

Per commentator, one table gives the quotes inside each chapter's 歷代注疏 section, one row per
「第N章」 (scripts/check-citation-ledger.py --attr parses those rows); a second table gives quotes
that sit elsewhere (another section of a chapter, or a front-matter file), labelled 「單元 NN」 or
by file so that they are never mistaken for 歷代注疏 rows.

Usage:  python3 scripts/gen-songofsolomen-ledger.py --write
        python3 scripts/gen-songofsolomen-ledger.py          # print
"""
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "songofsolomen"
OUT = BOOK / "99-appendix-references.md"

# key -> (H2 title, what the file is, where it lives, attribution regex)
WHO = OrderedDict([
    ("gill", ("紀爾（John Gill）——寓意讀法",
              "John Gill, *Exposition of the Entire Bible*（雅歌卷），經 biblehub 逐節取得，公有領域",
              "`.sources/commentary/gill-NN.txt`", r"Gill")),
    ("kd", ("凱爾與德利奇（Keil & Delitzsch）——字面為主",
            "C. F. Keil & F. Delitzsch, *Biblical Commentary on the Old Testament*（雅歌卷，德利奇撰），經 biblehub 逐節取得，公有領域。biblehub 壓平排版，希伯來文與部分標點有損；{TRUNC}，截斷處附近的 K&D 論述可能不完整",
            "`.sources/commentary/kd-NN.txt`", r"Delitzsch|Keil")),
    ("pulpit", ("《講壇釋經》（The Pulpit Commentary）",
                "*The Pulpit Commentary*（雅歌卷），經 biblehub 逐節取得，公有領域",
                "`.sources/commentary/pulpit-NN.txt`", r"Pulpit Commentary")),
    ("cambridge", ("劍橋聖經（The Cambridge Bible for Schools and Colleges）",
                   "*The Cambridge Bible for Schools and Colleges*（雅歌卷），經 biblehub 逐節取得，公有領域；該注釋的導論與附錄不在本書的來源檔內",
                   "`.sources/commentary/cambridge-NN.txt`", r"Cambridge")),
    ("jfb", ("JFB（Jamieson, Fausset & Brown）",
             "Jamieson, Fausset & Brown, *Commentary Critical and Explanatory on the Whole Bible*（雅歌卷），經 biblehub 逐節取得，公有領域",
             "`.sources/commentary/jfb-NN.txt`", r"Jamieson|JFB|Fausset")),
    ("ellicott", ("艾利考特（C. J. Ellicott）",
                  "C. J. Ellicott 編，*A Commentary for English Readers*（雅歌卷），經 biblehub 逐節取得，公有領域；該注釋的附論（Excursus）不在本書的來源檔內",
                  "`.sources/commentary/ellicott-NN.txt`", r"Ellicott")),
    ("poole", ("波爾（Matthew Poole）",
               "Matthew Poole, *Annotations upon the Holy Bible*（雅歌卷），經 biblehub 逐節取得，公有領域；1:1 等題辭節沒有注釋",
               "`.sources/commentary/poole-NN.txt`", r"Poole")),
    ("barnes", ("巴恩斯（Albert Barnes）",
                "Albert Barnes, *Notes on the Bible*（雅歌卷），經 biblehub 逐節取得，公有領域",
                "`.sources/commentary/barnes-NN.txt`", r"Barnes")),
    ("benson", ("本森（Joseph Benson）",
                "Joseph Benson, *Commentary on the Old and New Testaments*（雅歌卷），經 biblehub 逐節取得，公有領域",
                "`.sources/commentary/benson-NN.txt`", r"Benson")),
    ("geneva", ("日內瓦聖經注釋（Geneva Study Bible）",
                "*Geneva Study Bible*（雅歌卷），經 biblehub 逐節取得，公有領域；每節只有簡注",
                "`.sources/commentary/geneva-NN.txt`", r"Geneva")),
    ("henry", ("馬太·亨利（Matthew Henry）",
               "Matthew Henry, *Commentary on the Whole Bible*, vol. III（雅歌卷，原著 1706-1721），CCEL 全文，公有領域",
               "`.sources/longform/henry-chNN.txt`", r"Henry")),
    ("taylor", ("戴德生（J. Hudson Taylor）",
                "J. Hudson Taylor, *Union and Communion; or, Thoughts on the Song of Solomon*（1894），Project Gutenberg #26172 排印本，公有領域；非十九世紀原印本的字句",
                "`.sources/longform/taylor-sec*.txt`", r"Taylor")),
    ("bernard", ("伯爾拿（Bernard of Clairvaux）",
                 "*St. Bernard's Sermons on the Canticle of Canticles*（tr. a Priest of Mount Melleray, Dublin: Browne & Nolan, 1920），archive.org OCR，經 `scripts/normalize-ocr-source.py` 清洗；八十六篇止於歌 3:1，故只覆蓋單元 01-05",
                 "`.sources/longform/bernard-sermon-NN.txt`", r"Bernard")),
    ("spurgeon", ("司布真（C. H. Spurgeon）",
                  "C. H. Spurgeon, *Metropolitan Tabernacle Pulpit*，CCEL 排印本（現代化拼寫與人稱，非原印本逐字）與 Spurgeon Gems PDF，公有領域；本書存檔只有十一篇講雅歌經節（spurgeon.org 的索引另列更多篇；存檔不是窮盡的）",
                  "`.sources/longform/spurgeon-*.txt`", r"Spurgeon")),
    ("morgan", ("摩根（G. Campbell Morgan）——只用於前言與〈雅歌的位置〉",
                "G. Campbell Morgan, *The Analyzed Bible*, vol. II（1907）雅歌段（頁 63-68；archive.org `analyzedbible02morg` 的 OCR）：前半是講者與段落綱要（表格 OCR 損壞，不引），後半是約八十餘行散文導論；本書只引導論裏 OCR 完好的句子，十五個單元都不引摩根",
                "`.sources/longform/morgan-analyzed-bible-song.txt`", r"Morgan")),
])

FRONT = [("000-preface.md", "前言"), ("00-overview.md", "卷首·總覽"), ("00a-song-position.md", "卷首·定位"),
         ("00b-love-spine.md", "卷首·骨幹"), ("00c-revelation-order.md", "卷首·啟示的次序"),
         ("99-the-open-ending.md", "卷末"), ("999-afterword.md", "跋")]

BLOCK = re.compile(r'^> "[^\n]*\n(?:>[^\n]*\n)*?> — ([^\n]+)', re.M)


def classify(attr):
    for k, (_, _, _, pat) in WHO.items():
        if re.search(pat, attr):
            return k
    return None


def chapters():
    return sorted(p for p in BOOK.glob("*.md") if re.match(r"^(0[1-9]|1[0-5])-", p.name))


def split_sections(text):
    """[(heading line, body)] for each `## ` section; text before the first one has heading ''."""
    parts = re.split(r"(?m)^(## .+)$", text)
    out = [("", parts[0])]
    for i in range(1, len(parts), 2):
        out.append((parts[i], parts[i + 1]))
    return out


def scan():
    """sect[key][n] -> [attr] (inside 歷代注疏); other[key] -> [(label, attr)]"""
    sect = {k: defaultdict(list) for k in WHO}
    other = {k: [] for k in WHO}
    ref = {}

    def collect(text, label, chapter_no=None):
        last = None
        for head, body in split_sections(text):
            if head.startswith(("## 經文", "## 配詩")):
                continue
            for q in BLOCK.finditer(body):
                attr = re.sub(r"\*", "", q.group(1)).strip()
                key = classify(attr)
                if key is None and "同上" in attr:
                    key = last
                if key is None:
                    continue
                last = key
                if chapter_no is not None and head.startswith("## 歷代注疏"):
                    sect[key][chapter_no].append(attr)
                else:
                    other[key].append((label, attr))

    for p in chapters():
        n = int(p.name[:2])
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^雅歌\s*([\d:\-–]+)", t, re.M)
        ref[n] = m.group(1) if m else ""
        collect(t, f"單元 {n:02d}", chapter_no=n)
    for fn, label in FRONT:
        p = BOOK / fn
        if p.exists():
            collect(p.read_text(encoding="utf-8"), label)
    return sect, other, ref


def hymns():
    out = []
    for p in chapters():
        n = int(p.name[:2])
        t = p.read_text(encoding="utf-8")
        sec = re.search(r"^## 配詩.*?(?=^## )", t, re.M | re.S)
        if not sec:
            continue
        title = re.search(r"^> \*\*(.+?)\*\*", sec.group(0), re.M)
        cred = re.search(r"^> \*(?!\*)(.+?)\*\s*\\?\s*$", sec.group(0), re.M)
        out.append((n, title.group(1) if title else "", cred.group(1) if cred else ""))
    return out


def tables(key, sect, other, ref):
    parts = []
    in_sec = sum(len(v) for v in sect[key].values())
    elsewhere = len(other[key])
    if sect[key]:
        rows = ["| 單元 | 雅歌 | 逐字引文（條） | 出處行（每一條一項，依在章中出現的次序；書名寫法照各章實印，並未統一） |",
                "|--------|----------------|----------------|------------------------------------------------------|"]
        for n in sorted(sect[key]):
            rows.append(f"| 第{n}章 | {ref.get(n, '')} | {len(sect[key][n])} | " + "；".join(sect[key][n]) + " |")
        parts.append("\n".join(rows))
    if other[key]:
        by = defaultdict(list)
        for label, attr in other[key]:
            by[label].append(attr)
        rows = ["章內歷代注疏以外的位置與卷首各檔：", "",
                "| 位置 | 逐字引文（條） | 出處行 |",
                "|----------------|----------------|------------------------------------------------------|"]
        for label in sorted(by):
            rows.append(f"| {label} | {len(by[label])} | " + "；".join(by[label]) + " |")
        parts.append("\n".join(rows))
    return "\n\n".join(parts), in_sec, elsewhere


def trunc_note():
    hits = []
    for f in sorted((BOOK / ".sources" / "commentary").glob("kd-[0-9][0-9].txt")):
        n = f.read_text(encoding="utf-8", errors="ignore").count("continued...")
        if n:
            hits.append((f.stem, n))
    total = sum(n for _, n in hits)
    return f"另有 {total} 處 \"continued…\" 截斷標記（" + "、".join(f"{f} {n} 處" for f, n in hits) + "）"


def build():
    sect, other, ref = scan()
    out = []
    grand = sum(len(v) for k in WHO for v in sect[k].values()) + sum(len(other[k]) for k in WHO)
    out.append(f"""---
title: 雅歌研讀
subtitle: Song of Songs Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---

# 附錄：引用出處總表 (Appendix: Reference Ledger)

本表是「不編造一段出處」這句話的帳目。每條數字與出處行，都由 `scripts/gen-songofsolomen-ledger.py` 從各章與卷首各檔的原文讀回，不以手工維護；
各章「歷代注疏」一節的體例說明所指的「卷末附錄」就是這一份。凡加引號並附英文原文者，均為**逐字引文**：
本書把每一條與來源檔比對（比對忽略大小寫與標點，對用字嚴格），腳本為 `scripts/verify-song-quotes.py`。

**本書全部逐字引文合計 {grand} 條**（十五個單元與卷首、卷末各檔；經文區塊與配詩不算）。下面每位注疏者的 H2 列出他的條數：
一張表是各章「歷代注疏」一節內的引文（每章一列），另一張表是章內其他位置與卷首各檔的引文。
""")
    digits = "一二三四五六七八九"
    zh = [d for d in digits] + ["十"] + ["十" + d for d in digits] + ["二十"] + ["二十" + d for d in digits]
    n_order = 0
    for key, (title, what, where, _) in WHO.items():
        tbl, in_sec, elsewhere = tables(key, sect, other, ref)
        out.append(f"\n## {zh[n_order]}、{title}\n")
        n_order += 1
        total = in_sec + elsewhere
        what = what.replace("{TRUNC}", trunc_note())
        out.append(f"- 版本：{what}\n- 來源檔：{where}\n- 本書逐字引文合計：{total} 條（歷代注疏一節內 {in_sec} 條；其他位置 {elsewhere} 條）\n")
        out.append(tbl + "\n" if total else "（本書沒有這一家的逐字引文；若他處提及，皆為不加引號的轉述。）\n")

    out.append(f"\n## {zh[n_order]}、麥克阿瑟——本書沒有逐字引文\n")
    n_order += 1
    out.append("*（本節為手寫：由本腳本內的固定文字輸出，不是從各章讀回；內容若與各章不符，以各章與來源檔為準。）*\n\n")
    out.append("""查到的 gty.org 頁面（`.sources/gty-sitemap.xml`，2026-10-26 取得的站點地圖）裏，沒有雅歌的逐節講道系列；站點地圖只列網址與標題（講章、文章、部落格、會議），沒有「書卷導論」這一類頁面，所以本書**不能**用它證明「麥克阿瑟沒有雅歌導論」，只能說：本書查到的頁面裏沒有可引的雅歌講道。站點地圖裏與雅歌字面相近的只有〈The Rape of Solomon's Song〉系列與〈Intimacy with Christ〉一篇；這兩者本書未讀其內容，只從標題判斷其題目（前者論現代音樂），所以不引。《麥克阿瑟研讀本》的注釋有版權，不引。本書因此**沒有任何麥克阿瑟引文**，也不憑記憶引他。
""")
    out.append(f"\n## {zh[n_order]}、本書沒有的聲音（誠實限制）\n")
    n_order += 1
    out.append("*（本節為手寫：由本腳本內的固定文字輸出，不是從各章讀回；內容若與各章不符，以各章與來源檔為準。）*\n\n")
    out.append("""- **老弟兄（黃長老）：** 本項目沒有他講雅歌的第一手錄影或筆記。各章「老弟兄查經」一節是依 ask-elder-wong 的方法所做的**方法性撮述**，不是逐字語錄；方法依據是他讀詩歌的「愛的詩歌——對象是耶穌」一把鑰匙，那是他對林前 13 章說的，本書把這個提問用在雅歌上，是編者的延伸。卷首三章的「編者一句話」是編者的概括，也不是他的話。
- **加爾文：** 沒有雅歌註釋，不引。
- **教父與改革家：** 本書沒有專節。歐利根與尼撒的貴格利的雅歌講章的英譯本不在公有領域，本書不引；他們的讀法若出現，只經由紀爾、亨利、德利奇等注疏轉述，並標「經某某轉引」。
- **伯爾拿：** 只到歌 3:1；單元 06-15 沒有伯爾拿論該段的說法。倉庫另一卷（`john-thursday-wong/book/appendix-03-commentary-excerpts.md`）把一段約翰福音 15:1-5 的話署為伯爾拿《雅歌講道集》，本書查無支持，**未引用**。
- **司布真：** 本書存檔裏沒有論歌 1:4、2:16、5:2-8、5:16、7:10 的講章可引（spurgeon.org 的索引另列更多篇，本書存檔只有十一篇）。
""")
    out.append(f"\n## {zh[n_order]}、聖經版本與核對方式\n")
    n_order += 1
    out.append("*（本節為手寫：由本腳本內的固定文字輸出，不是從各章讀回；內容若與各章不符，以各章與來源檔為準。）*\n\n")
    out.append("""- **中文：** 和合本（CUV）。底本以 ai-eden.com 的 JSON 介面為準（書卷代碼 `song-of-solomon`），與 fhl.net 與 cnbible.com 三向對校，差異記錄在 `.sources/CUV-DIFF-REPORT.txt`：專名（利巴嫩／黎巴嫩、大馬色／大馬士革）從 ai-eden；cnbible 為 2011 現代標點和合本，非 1919 原本。和合本的講者標題（「新娘」「新郎」）是版本編者所加，不是經文，書中另列「誰在說話」表。
- **英文：** NASB 1995，取自 biblehub.com 的 NASB 章頁（含斜體與引號），對 ai-eden NASB 逐節核對。
- **希伯來文：** Sefaria, *Miqra according to the Masorah*；節號依英文節號標示，與希伯來節號的對照見 `.sources/hebrew/hebrew-versification.tsv`（英 6:13 = 希 7:1；英 7:n = 希 7:n+1）。
- **他卷經文：** 取自 ai-eden（和合本＋NASB），快取於 `.sources/xref/`；快取沒有的經文，本書只寫出處，不引字句。
- **字典：** Strong's 號與 BDB 詞條取自 biblehub.com/hebrew/<號>.htm 頁；那些頁面沒有存檔在 `.sources/`，核對者要重驗須自行上網。
""")
    out.append(f"\n## {zh[n_order]}、配詩出處（公有領域）\n")
    n_order += 1
    out.append("| 單元 | 聖詩 | 作者／譯者／年份 |\n|--------|----------------------------|----------------------------------------------------------|")
    for n, t, c in hymns():
        out.append(f"| 第{n}章 | {t} | {c} |")
    out.append("\n每首只取一節。印本來源記在 `.sources/hymns.md`（主要為 *The Army and Navy Hymnal*, 1920 的 Wikisource 轉錄；第 15 首只有 Wikisource 頁，沒有掃描印本；第 1 首另核對 Formby, *Catholic Hymns*, 1853）。\n")
    out.append(f"\n## {zh[n_order]}、機器核對現況（誠實記錄）\n")
    n_order += 1
    out.append("*（本節為手寫：由本腳本內的固定文字輸出，不是從各章讀回；內容若與各章不符，以各章與來源檔為準。）*\n\n")
    out.append(f"""- `scripts/verify-song-quotes.py`：逐條比對每一條 `> "…"` 英文引文與其出處所屬來源家族的全部檔案。本書逐字引文合計 {grand} 條（見上），核對時無 MISS。該腳本只掃檔名以數字起頭的檔，`elder-wong-systematic-study.md` 不在其內（該檔沒有加引號的英文區塊）。
- 這個核對只證明**引句是來源檔的子字串**，不證明該句的「出處行」寫對了卷、節或篇號，也不證明本書對它的理解正確；這兩件事靠獨立校對。
- 司布真與戴德生的檔是現代化排印本，引句與十九世紀原印本可能有拼寫與人稱的差別。
- `scripts/check-citation-ledger.py` 以 `--attr 名稱=正則`（每位注疏者一個，例如 `--attr "紀爾=Gill"`）核對上列各章「歷代注疏」一節內的列是否與各章相符；不帶 `--attr` 時它只核對摩根與麥克阿瑟（兩者本書各章都沒有引文）。
""")
    out.append(f"\n## {zh[n_order]}、仍未完成\n")
    out.append("*（本節為手寫：由本腳本內的固定文字輸出，不是從各章讀回；內容若與各章不符，以各章與來源檔為準。）*\n\n")
    out.append("""- 配詩只核對了一節的印本；第 15 首沒有掃描印本，來源等級較低。
- K&D 的檔在 biblehub 被截斷處（見上，處數由腳本計），德利奇較完整的論述可能存在，但不在本書所用檔內；本書不替他補寫。
- 劍橋聖經的導論與艾利考特的附論不在來源檔內，所以關於作者、年代與全詩結構的爭論，本書只能依注疏逐節檔所透露的部分並陳。
- 猶太會堂在逾越節誦讀雅歌，本書手邊只有巴恩斯在 2:8 的一句推測（"perhaps"，barnes-04.txt）；拉比阿基巴稱雅歌為「聖中之聖」不在任何來源檔內（JFB 只說「猶太人」把雅歌比作至聖所），本書沒有寫。
- Strong's 與 BDB 的引用取自 biblehub 頁面，沒有存檔；獨立核對者須自行重取。
""")
    if (ROOT / "docs" / "scores" / "songofsolomen-2026-10-26.md").exists():
        out.append("- 全書的獨立校對輪與評分見 `docs/scores/songofsolomen-2026-10-26.md`。\n")
    return "\n".join(out)


def main():
    text = build()
    if "--write" not in sys.argv:
        print(text)
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

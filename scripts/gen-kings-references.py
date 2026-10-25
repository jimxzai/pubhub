#!/usr/bin/env python3
"""Generate books/bible/kings/99-appendix-references.md (the citation ledger) from the chapters.

The ledger is the book's honesty account. It is DERIVED from what the chapters actually
contain (check-citation-ledger.py's lesson: a hand-kept ledger drifts from its own book).
Per chapter, per commentator: how many verbatim `> "English"` quotes, and the 出處 line(s).

Usage: python3 scripts/gen-kings-references.py --write   (or no flag: print)
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "kings"
OUT = BOOK / "99-appendix-references.md"
UNIT_TO_KCH = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 8, 10: 9, 11: 10, 12: 11, 13: 12,
               14: 12, 15: 13, 16: 14, 17: 15, 18: 16, 19: 17, 20: 18, 21: 19, 22: 20, 23: 21, 24: 22}


def roman(n):
    r = ""
    for v, s in [(20, "xx"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]:
        while n >= v:
            r += s
            n -= v
    return r


def parse():
    """{unit: [(commentator-key, display, nquotes, [source lines])]}"""
    data = {}
    for f in sorted(BOOK.glob("[0-2][0-9]-*.md")):
        n = int(f.name[:2])
        t = f.read_text(encoding="utf-8")
        a = t.find("## 歷代注疏")
        b = t.find("\n## ", a + 5)
        sec = t[a:b]
        # split into commentator blocks: a bold-name line (with Latin letters) or a ### 摩根 heading
        parts = re.split(r"(?m)^(?=\*\*[^*\n]*[A-Za-z][^*\n]*\*\*|### 摩根|### 麥克阿瑟)", sec)
        rows = []
        for p in parts[1:]:
            if p.startswith("### 摩根"):
                key, disp = "摩根", "G. Campbell Morgan"
            elif p.startswith("### 麥克阿瑟"):
                key, disp = "麥克阿瑟", "John MacArthur"
            else:
                m = re.match(r"\*\*([^*\n]+)\*\*", p)
                disp = m.group(1)
                key = disp.split("(")[0].strip()
            if p.startswith("### "):
                # a ### commentator block runs to the next ### heading (never swallow the next commentator)
                body = re.split(r"(?m)^### ", p[4:], maxsplit=1)[0]
            else:
                body = re.split(r"(?m)^### ", p, maxsplit=1)[0]
            nq = len(re.findall(r'^> "', body, re.M))
            src = [l[2:].strip() for l in body.splitlines() if l.startswith("> 出處：") or l.startswith("> — ")]
            rows.append((key, disp, nq, src))
        data[n] = rows
    return data


def chapters_of(data, key):
    return sorted(n for n, rows in data.items() for r in rows if r[0] == key and r[2] > 0)


def zh_list(ns):
    return "、".join(f"第{n}章" for n in ns) if ns else "（無）"


def render(data):
    out = []
    w = out.append
    w("---\ntitle: 列王紀上研讀\nsubtitle: 1 Kings Deep Study\nauthor: PubHub 三書精讀系統\ndate: 2026年10月\npublisher: 三書精讀出版系統\n---\n")
    w("# 附錄：引用出處總表 (Appendix: References)\n")
    w("本附錄記錄全書 24 個研讀單元「歷代注疏 (Historical Commentary)」所引用的全部來源，並如實說明本書與本系列其他書卷在資料基礎上的差異。本表由 `scripts/gen-kings-references.py` 自各章檔案程式生成，非手工維護：每章引了誰、引了幾條逐字引文、出處標註為何，都是從該章的原文數出來的。\n")
    w("**列王紀上在本項目的原始檔案庫中沒有第一手教導記錄可用**——僅有一份〈列王紀上·逐卷查經〉綱要（`books/historyBooks/10-1kings-study.md`）。因此每一章的「老弟兄查經」小節均為編者依老弟兄一貫查經方法論在列王紀上經文上的方法性應用，不是對任何歷史記錄的逐字引用；全書沒有任何一句加引號歸給老弟兄的話。\n")
    mc = chapters_of(data, "麥克阿瑟")
    if mc:
        w("**麥克阿瑟 (John MacArthur, gty.org)**：gty.org 沒有逐節講解列王紀上的系列。所引均為他在其他主題的講章（如羅馬書、腓立比書、希伯來書、提摩太前書、但以理書導論）或網誌（辨別力、神的拯救）中，順帶談到王上人物與事件的段落；每則在章內註明是專論還是順帶，並以講章編號對照 gty.org 逐字稿逐字核對。沒有可核對段落的章，不作無出處的綜述，也沒有麥克阿瑟小節。\n")
    else:
        w("**麥克阿瑟 (John MacArthur, gty.org)**：本卷未引用任何麥克阿瑟的話。\n")
    w("**摩根 (G. Campbell Morgan)**：使用兩份公有領域材料：《The Analyzed Bible》卷一（1907）中「I. Kings」一節的結構總覽，以及《Exposition on the Whole Bible》對王上每章的一段概述（取自 studylight.org）。兩者都不是逐節講解；每個研讀單元至少有一則可逐字核對的摩根引句。\n")
    w("---\n")
    # Morgan
    mn = chapters_of(data, "摩根")
    w("## 一、摩根 G. Campbell Morgan\n")
    w("**來源一：《Exposition on the Whole Bible》**（王上第 1–22 章各一段概述）取自 studylight.org 所載全文（本地快取 `sources/fathers/morgan_exposition_1kings.txt`）；該文本偶有排印錯字（如 oveewhelming、pries!），含錯字的句子不引。\n")
    w("**來源二：《The Analyzed Bible》**，Vol. I (Fleming H. Revell, 1907)。archive.org 識別碼 `analyzedbible01morg`，全文純文字：`https://archive.org/download/analyzedbible01morg/analyzedbible01morg_djvu.txt`（本地快取 `sources/fathers/morgan_analyzed_v1.txt`）。這份 1907 年的掃描文本有頁碼、斷詞雜訊（如行尾連字號斷詞）；引用時只取同一頁內、無 OCR 錯誤的句子，並將行尾連字號斷詞接回；`verify-citations.py` 對這類句子標為 OK-OCR。\n")
    w("| 章 | 逐字引句數 | 出處 |\n|---|---|---|")
    for n in mn:
        r = [x for x in data[n] if x[0] == "摩根"][0]
        w(f"| 第 {n} 章 | {r[2]} | {'；'.join(r[3]) or '—'} |")
    w("")
    w("**要旨綜述的章**：（無——凡標註摩根之處均為逐字引句；沒有摩根小節的章，不作無出處的綜述）\n")
    # MacArthur
    w("## 二、麥克阿瑟 John MacArthur, gty.org\n")
    if mc:
        w("**來源**：gty.org 講章逐字稿（出處行註明 sermon 編號）；網誌（blog B 編號）不是講道，`verify-sermon-quotes.py` 不認，由編者對網誌全文手動逐字比對。\n")
        w("| 章 | 逐字引句數 | 出處 |\n|---|---|---|")
        for n in mc:
            r = [x for x in data[n] if x[0] == "麥克阿瑟"][0]
            w(f"| 第 {n} 章 | {r[2]} | {'；'.join(r[3]) or '—'} |")
        w("")
        w("**逐字引用**：" + zh_list(mc) + "\n")
        w("**要旨綜述的章**：（無——凡標註麥克阿瑟之處均為逐字引句）\n")
    else:
        w("**逐字引用**：（無）\n")
        w("**要旨綜述的章**：（無）\n")
        w("本卷不引用麥克阿瑟；詳見前言。\n")
    # Henry
    hn = chapters_of(data, "馬太·亨利")
    w("## 三、馬太·亨利 Matthew Henry, *Commentary on the Whole Bible*, Vol. II (Joshua to Esther)\n")
    w("**來源**：CCEL 全文 `https://ccel.org/ccel/henry/mhc2.iKi.{ii…xxiii}.html`（本地快取 `sources/ccel/`，純文字 `sources/txt/henry.txt`）。王上第 N 章對應頁碼為羅馬數字 N+1（如王上 3 章＝`mhc2.iKi.iv`）。英文引句為原書逐字（現代英文拼寫依 CCEL 所載文本，未改動）；中譯為編者所譯。\n")
    w("| 章 | 王上章 | 逐字引句數 | CCEL 頁 |\n|---|---|---|---|")
    for n in hn:
        r = [x for x in data[n] if x[0] == "馬太·亨利"][0]
        k = UNIT_TO_KCH[n]
        w(f"| 第 {n} 章 | {k} | {r[2]} | mhc2.iKi.{roman(k + 1)} |")
    w("")
    # Others
    w("## 四、教父時期與其他近代作者（逐章所引，全為公有領域）\n")
    w("以下是各章「教父時期」「改革宗時期」小節裏，亨利與摩根以外的作者及其逐字引句。**教父時期覆蓋很薄**：許多單元查無可逐字核對、確實論及該段經文的教父原文，書中便以一句「未能找到」說明，不湊數。\n")
    w("| 章 | 作者 | 逐字引句數 | 出處（書中所標） |\n|---|---|---|---|")
    for n in sorted(data):
        for key, disp, nq, src in data[n]:
            if key in ("馬太·亨利", "摩根"):
                continue
            w(f"| 第 {n} 章 | {disp} | {nq} | {'；'.join(src) or '（綜述，無引號）'} |")
    w("")
    none_fathers = [n for n in sorted(data) if not any(k in ("奧古斯丁", "耶柔米", "屈梭多模", "安波羅修", "居普良") for k, *_ in data[n])]
    w(f"**無教父引文的章（書中均已誠實註明「未能找到」）**：{zh_list(none_fathers)}。\n")
    w("**本地快取的原文**：New Advent 教父文本（奧古斯丁《上帝之城》第 16-18 卷、奧古斯丁詩篇講章與約翰福音講章、耶柔米《駁約維尼安》與書信、居普良論著、安波羅修《論職責》、屈梭多模馬太福音／使徒行傳／希伯來書講道），CCEL 加爾文《基督教要義》與聖經注釋，Project Gutenberg #42891（法勒《列王紀上》，Expositor's Bible, 1893），archive.org 邁爾《Elijah and the Secret of His Power》。逐一網址見 `sources/fathers/_urls.tsv`（本機，不入版）。\n")
    w("## 五、聖經版本與核對方式\n")
    w("- **中文**：和合本 (CUV)，自 `bible.fhl.net` 的 `unv`（1919 和合本）逐章下載快取；全書依本系列用字政策統一「裏」（非「裡」）。經文區塊由 `sources/mkscr.py` 自快取直接生成，並以 `sources/verify_blocks.py` 逐節機器比對。\n")
    w("- **English**：NASB 1995，自 `biblehub.com/nasb/1_kings/{章}.htm` 逐章下載快取（無底線路徑為 1995 版）。\n")
    w("- **希伯來文與 Strong's**：希伯來文取自 Sefaria 的 Miqra according to the Masorah（本機快取），字根與意義依 OpenScriptures Hebrew Lexicon（Strong's）；列王紀上的希伯來文節數與英文有差（希伯來 5:1-14＝英 4:21-34；希伯來 5:15-32＝英 5:1-18；22:43 後半＝希伯來 22:44），本書一律用英文節數，由 `sources/heb.py` 轉換。書中凡寫「某字出現 N 次」，均自本機快取的希伯來文逐節計得。\n")
    w("- **聖詩**：全為公有領域（1929 年前）英文詩，每節皆自已快取的 Wikisource／archive.org 頁面逐行核對；中譯為編者所譯。詩的年代若來源頁面未載，書中標「約」或僅標作者。\n")
    w("## 六、機器逐字核對現況\n")
    w("`verify-citations.py`：全書逐字引句逐一對照上列快取原文；無 DRIFT、無 MISS（OK-OCR 為掃描文本的斷詞容忍）。`verify-prose-citations.py` 另查行文中「引號＋出處」的中文經文引句。`check-book-spine.py`：四項全清。尚未完成的部分見評分表《仍未完成》。\n")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    text = render(parse())
    if "--write" in sys.argv:
        OUT.write_text(text, encoding="utf-8")
        print(f"wrote {OUT} ({len(text)} chars)")
    else:
        print(text)

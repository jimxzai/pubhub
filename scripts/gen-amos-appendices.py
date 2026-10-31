#!/usr/bin/env python3
"""Generate the Amos volume's two appendices from the book's own text.

  98-appendix-indices.md     chapter map / cross-book Scripture index / subject index / Hebrew word index
  99-appendix-references.md  citation ledger (who is quoted where, what was machine-checked, what is unfinished)

Same rationale as scripts/gen-nehemiah-indices.py and gen-nehemiah-ledger.py: a hand-kept index or
ledger drifts from the chapters.  Every count below is read back out of the chapter files, and the
machine-check section RUNS the verification scripts and prints what they actually said.

Usage:  python3 scripts/gen-amos-appendices.py --write        # rewrite both files
        python3 scripts/gen-amos-appendices.py                # print both
        python3 scripts/gen-amos-appendices.py --no-run --write   # skip the slow verification runs
"""
import importlib.util
import re
import subprocess
import sys
import urllib.parse
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "Amos"
SRC = BOOK / "sources"
OUT_INDEX = BOOK / "98-appendix-indices.md"
OUT_LEDGER = BOOK / "99-appendix-references.md"
NUNITS = 12

FRONT = """---
title: 阿摩司書研讀
subtitle: Amos Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---
"""

VOLUME = {}
for rng, name in [((1, 2), "卷一·吼聲與列國"), ((3, 4), "卷二·揀選與管教"), ((5, 7), "卷三·尋求與安逸"),
                  ((8, 10), "卷四·準繩與籃子"), ((11, 12), "卷五·篩子與帳幕")]:
    for i in range(rng[0], rng[1] + 1):
        VOLUME[i] = name

# ---------------------------------------------------------------- shared helpers
_spec = importlib.util.spec_from_file_location("john_index", ROOT / "scripts" / "gen-john-scripture-index.py")
john = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(john)
BOOKS = list(john.BOOKS)
ORDER = {full: i for i, (full, _) in enumerate(BOOKS)}
ALIAS = {a: full for full, aliases in BOOKS for a in aliases}
MAXCHAP = dict(john.MAXCHAP)
_SHORT = "|".join(a for a in ALIAS if len(a) == 1)
_LONG = "|".join(sorted((a for a in ALIAS if len(a) > 1), key=len, reverse=True))
REF = re.compile(
    rf"(?:(?<![{john.CJK}A-Za-z0-9])({_SHORT})|(?<![A-Za-z0-9])({_LONG}))"
    rf"\s*(\d+)(?::{john.VERSES})?(?=\s*章?)"
)
AMBIGUOUS = set("但得該拿傳歌書拉")
LIST_PUNCT = set("（(、；;/ ")

SOURCES = [
    ("000-preface.md", "前言"), ("00-overview.md", "卷首·概覽"), ("00a-amos-position.md", "卷首·位置"),
    ("00b-hearing-spine.md", "卷首·骨幹"), ("00c-revelation-order.md", "卷首·啟示的次序"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}篇") for i in range(1, NUNITS + 1)] + [
    ("99-to-revelation.md", "卷末"), ("999-afterword.md", "跋"),
]

SUBJECTS = [
    ("聽（שׁמע）", r"聽"), ("吼叫（שׁאג）", r"吼叫|咆哮"), ("三番四次", r"三番四次"), ("你們仍不歸向我", r"不歸向我"),
    ("尋求與存活", r"尋求|存活"), ("公平與公義", r"公平|公義"), ("窮人／貧窮", r"窮乏|貧寒|窮人|貧窮|困苦"),
    ("節期與敬拜的虛假", r"節期|聖會|燔祭|素祭"), ("伯特利", r"伯特利"), ("吉甲", r"吉甲"), ("撒馬利亞", r"撒馬利亞"),
    ("耶和華的日子", r"耶和華的日子"), ("準繩", r"準繩"), ("夏天的果子", r"夏天的果子"), ("篩子", r"篩"),
    ("帳幕", r"帳幕"), ("拔出與栽植", r"拔出|栽於|栽植"), ("後悔", r"後悔"), ("代求", r"代求|求你赦免|求你止息"),
    ("亞瑪謝", r"亞瑪謝"), ("耶羅波安", r"耶羅波安"), ("烏西雅", r"烏西雅"), ("提哥亞／牧人", r"提哥亞|牧人"),
    ("以東", r"以東"), ("先知", r"先知"), ("餘民", r"餘民|餘剩"), ("列國", r"列國|萬國|萬族"),
    ("老弟兄的方法（提問）", r"提問"), ("你看見耶穌了嗎", r"看見耶穌"),
]


def source_path(name):
    if name.endswith(".md"):
        return BOOK / name
    hits = sorted(BOOK.glob(f"{name}-*.md"))
    return hits[0] if hits else None


def prose_lines(path):
    """Chapter lines minus the Scripture block, hymn blocks, template boilerplate and table rows."""
    out, skip, skip3 = [], False, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            skip = line.startswith(("## 經文", "## 配詩"))
            skip3 = False
        elif line.startswith("### "):
            skip3 = line.startswith(("### 今天的祭壇", "### 禱告回應", "### 默想問題"))
        if skip or skip3 or line.lstrip().startswith(("|", "> ^")):
            continue
        out.append(line)
    return out


def refs_in(text):
    for m in REF.finditer(text):
        alias = m.group(1) or m.group(2)
        if alias in AMBIGUOUS and m.start() > 0 and text[m.start() - 1] not in LIST_PUNCT:
            continue
        chap = int(m.group(3))
        full = ALIAS[alias]
        if chap < 1 or chap > MAXCHAP[full]:
            continue
        yield full, chap


# ---------------------------------------------------------------- indices
def chapter_map():
    rows = ["| 篇 | 阿摩司書 | 卷 | 篇題 | 本章鑰詞 |",
            "|--------|----------------|------------------------|--------------------------------|------------------------------------------|"]
    for i in range(1, NUNITS + 1):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        text = p.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, flags=re.M)
        title = re.sub(r"\s*\(.*\)\s*$", "", h1.group(1)) if h1 else ""
        refline = re.search(r"^阿摩司書\s*([\d:\-–]+)", text, flags=re.M)
        key = re.search(r"本章鑰詞[：:]\s*\**([^\n\\]*?)\**\s*(?:\\|$)", text, flags=re.M)
        rows.append(f"| {i:02d} | {refline.group(1) if refline else ''} | {VOLUME[i]} | {title} | "
                    f"{key.group(1).strip(' *') if key else ''} |")
    return "\n".join(rows)


def scripture_index():
    index = defaultdict(set)
    for fname, label in SOURCES:
        p = source_path(fname)
        if not p or not p.exists():
            continue
        for line in prose_lines(p):
            cleaned = re.sub(r"阿摩司書\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
            cleaned = re.sub(r"(?<![一-鿿])摩\s*\d+(?::\d+(?:[-–,，]\s*\d+)*)?", "", cleaned)
            for full, chap in refs_in(cleaned):
                if full == "阿摩司書":
                    continue
                index[(full, chap)].add(label)
    order = {lbl: i for i, (_, lbl) in enumerate(SOURCES)}
    keys = sorted(index, key=lambda k: (ORDER.get(k[0], 999), k[1]))
    out = ["| 經文 | 本書討論之處 |",
           "|--------------------------|----------------------------------------------------------|"]
    for full, chap in keys:
        out.append(f"| {full} {chap} | {'、'.join(sorted(index[(full, chap)], key=lambda l: order.get(l, 999)))} |")
    return "\n".join(out), len(keys)


def subject_index():
    out = ["| 主題 | 見於 |", "|--------------------------|----------------------------------------------------------|"]
    for name, pat in SUBJECTS:
        where = []
        for i in range(1, NUNITS + 1):
            p = source_path(f"{i:02d}")
            if p and sum(len(re.findall(pat, l)) for l in prose_lines(p)) >= 1:
                where.append(f"第{i}篇")
        if where:
            out.append(f"| {name} | {'、'.join(where)} |")
    return "\n".join(out)


def hebrew_index():
    out = ["| 原文 | 出處 | 見 | 要點 |", "|--------------------|------------|--------|------------------------------------------------|"]
    for i in range(1, NUNITS + 1):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^## 原文研讀.*?(?=^## )", t, re.M | re.S)
        if not m:
            continue
        for line in m.group(0).splitlines():
            if not line.startswith("|") or line.startswith("|--") or "| 原文 |" in line:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3 or not re.search(r"[\u0590-\u05FF]", cells[0]):
                continue
            gloss = re.split(r"[；;。]", cells[2])[0]
            gloss = re.sub(r"\*+", "", gloss)
            if len(gloss) > 40:
                cut = gloss[:40]
                gloss = (cut.rsplit("，", 1)[0] if "，" in cut else cut) + "…"
            gloss = re.sub(r"（[^）]*$", "", gloss)
            out.append(f"| {cells[0]} | {cells[1]} | 第{i}篇 | {gloss} |")
    return "\n".join(out)


def build_index():
    sc, nsc = scripture_index()
    return FRONT + f"""
# 附錄：經文與主題索引 (Appendix: Scripture & Subject Indices)

本附錄依全書正文實際出現的內容編製，不另行增列各篇未曾論及的經文或主題。四張表都由
`scripts/gen-amos-appendices.py` 直接從各篇原文抽取生成，不以手工維護，以免與正文脫節。

---

## 附錄一：本書篇次與阿摩司書經文對照 (Chapter Map)

本書十二篇，每篇一個研讀單元；**篇次序號是本書的單元序號，不是阿摩司書的章號**，真實章節範圍在下表第二欄。

{chapter_map()}

---

## 附錄二：跨書經文索引 (Cross-Book Scripture Index)

下表列出各篇行文所引用的**阿摩司書以外**的經文章次（節號不列；阿摩司書本身的引用不入此表）。「經文」區塊、配詩與引用表格不計；只有「章」層級，節號以各篇為準。共 {nsc} 條。

{sc}

---

## 附錄三：主題索引 (Subject Index)

以下主題由各篇行文（不含經文區塊、配詩、今天的祭壇、禱告回應、默想問題與引用表格）逐篇計數得出，出現至少一次即列。

{subject_index()}

---

## 附錄四：原文詞彙索引 (Hebrew Word Index)

各篇〈原文研讀〉表格中的希伯來文詞，依篇次列出（每條只取該列意義欄第一個分句）。

{hebrew_index()}
"""


# ---------------------------------------------------------------- ledger
WHO = OrderedDict([
    ("calvin", ("John Calvin", "加爾文（John Calvin），*Commentaries on the Twelve Minor Prophets*, vol. 2（Joel, Amos, Obadiah），約翰·歐文（John Owen）英譯")),
    ("henry", ("Matthew Henry", "馬太·亨利（Matthew Henry），*Commentary on the Whole Bible*，阿摩司書卷")),
    ("morgan", ("G. Campbell Morgan", "摩根（G. Campbell Morgan），*The Message of Amos*，載 *Living Messages of the Books of the Bible*, Old Testament（1912）")),
    ("macarthur", ("John MacArthur", "麥克阿瑟（John MacArthur），gty.org 講章與文章")),
    ("fathers", ("", "教父（NPNF／ANF 公有領域英譯，取自 newadvent.org）")),
])
FATHER_KEYS = ["Chrysostom", "Augustine", "Justin", "Tertullian", "Jerome", "Cyprian", "Irenaeus", "Gregory", "Clement", "Basil", "Cyril", "Methodius", "Origen", "Cassian", "Damascus", "Hippolytus", "Ambrose"]
SOURCE_FILE = {
    "calvin": "`sources/commentary/calvin/amos-calvin.txt`（自 ccel.org 的 `calcom27` 切出 Amos 全卷，講章 49–70；英譯本內的編者按語〔— Ed.〕一律不引）",
    "henry": "`sources/commentary/henry/amos-page-*.txt`（ccel.org，*Commentary on the Whole Bible* vol. 4〔`mhc4`〕；`i`＝導論，`ii`–`x`＝阿摩司書 1–9 章；整章全文，無節號）",
    "morgan": "`sources/commentary/morgan-amos.txt`（自 Nehemiah 卷的 `m-livingmessagesof01morgiala.txt` 切出〈The Message of Amos〉pp. 197–211；archive.org *Living Messages of the Books of the Bible* 的 OCR；只有一篇全書概觀；頁碼取自頁眉記號）",
    "macarthur": "`sources/commentary/gty/<CODE>.txt`（gty.org 講章逐字稿／文章；索引見 `sources/commentary/gty/INDEX.md`）",
    "fathers": "`sources/commentary/fathers/*.txt`（每檔含 AUTHOR／WORK／TRANSLATOR／SOURCE_URL 四行標頭；索引見 `sources/commentary/fathers/INDEX.md`）",
}


def classify(src):
    for k, n in [("John Calvin", "calvin"), ("Matthew Henry", "henry"), ("G. Campbell Morgan", "morgan"),
                 ("John MacArthur", "macarthur")]:
        if k in src:
            return n
    if any(f in src for f in FATHER_KEYS):
        return "fathers"
    return None


QUOTE = re.compile(r'^> "(.+?)"\s*\n> — (.+)$', re.M)


def chapters():
    return [(int(p.name[:2]), p) for p in sorted(BOOK.glob("[0-9][0-9]-*.md")) if 1 <= int(p.name[:2]) <= NUNITS]


def scan():
    rows = defaultdict(lambda: defaultdict(list))
    ref = {}
    for n, p in chapters():
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^阿摩司書\s*([\d:\-–]+)", t, re.M)
        ref[n] = m.group(1) if m else ""
        for m in QUOTE.finditer(t):
            who = classify(m.group(2))
            if who:
                rows[who][n].append(m.group(2).strip())
    return rows, ref


def table(who, rows, ref):
    head = ["| 篇 | 阿摩司書 | 逐字引文（條） | 出處行（各條，本書實印） |",
            "|--------|----------------|----------------|------------------------------------------------------|"]
    body = []
    for n in sorted(rows[who]):
        srcs = rows[who][n]
        distinct = list(OrderedDict.fromkeys(re.sub(r"\*", "", s) for s in srcs))
        body.append(f"| 第{n}篇 | {ref[n]} | {len(srcs)} | " + "；".join(distinct) + " |")
    total = sum(len(v) for v in rows[who].values())
    return "\n".join(head + body), total


def run(cmd, timeout=900):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa: BLE001
        return f"ERROR {e}"


def machine_checks(skip):
    if skip:
        return "（本次生成以 `--no-run` 略過逐項執行；請不帶該旗標重新生成。）"
    py = sys.executable
    corpus = SRC / "commentary" / "corpus-all.txt"
    lines = []
    out = run([py, "scripts/verify-citations.py", str(BOOK), "--source", str(corpus)])
    m = re.search(r"verbatim OK:\s*(\d+)\s+OK-OCR:\s*(\d+)\s+DRIFT:\s*(\d+)\s+MISS:\s*(\d+)", out)
    lines.append("- **注疏引文逐字核對**（`verify-citations.py`，對合併語料 `sources/commentary/corpus-all.txt`＝亨利＋加爾文＋摩根＋全部教父檔＋全部 gty 檔）："
                 + (f"逐字吻合 {m[1]}、OCR 斷詞吻合 {m[2]}、DRIFT {m[3]}、MISS {m[4]}。" if m else "無法讀出結果。")
                 + "此項只證明引文是來源語料的連續子字串，**不證明歸屬正確**；歸屬另由下列一項與各章撰寫時的逐檔核對負責。")
    out = run([py, "scripts/verify-sermon-quotes.py", str(BOOK)])
    m = re.search(r"verified:\s*(\d+)\s+missing from own transcript:\s*(\d+)\s+unresolved:\s*(\d+)", out)
    lines.append("- **麥克阿瑟引文對各自講章核對**（`verify-sermon-quotes.py`，每條只對它自己出處行的講章編號）："
                 + (f"核對 {m[1]} 條吻合，不在自己講章內 {m[2]} 條，無法解析 {m[3]} 條。" if m else "無法讀出結果。"))
    out = run([py, "scripts/verify-prose-citations.py", str(BOOK), "--self", "摩"])
    m = re.search(r"(\d+) in-prose citation\(s\) checked \| (\d+) MISS \| (\d+) reviewed-as-term \| (\d+) unresolved", out)
    lines.append("- **行文中的經文引句**（`verify-prose-citations.py … --self 摩`，對 fhl 和合本）："
                 + (f"檢查 {m[1]} 個「引號＋出處」，MISS {m[2]}，unresolved {m[4]}。" if m else "無法讀出結果。")
                 + "unresolved 是該腳本不能解析出處的條目，不是已核對的錯誤，也不是已核對無誤。")
    out = run([py, "scripts/check-prose-scripture-quotes.py", str(BOOK)])
    m = re.search(r"(\d+) file\(s\) scanned; (\d+) quote\(s\) not found", out)
    lines.append("- **行文引句對本篇經文區塊**（`check-prose-scripture-quotes.py`）："
                 + (f"掃描 {m[1]} 個檔，{m[2]} 條不在該篇印出的經文內；這些是引用阿摩司書**其他單元**或他書的句子（標 NOT-IN-UNIT），已由上一項對全書和合本核對。" if m else "無法讀出結果。"))
    out = run([py, "scripts/lint-chapter-markup.py", str(BOOK)])
    m = re.search(r"clean: (\d+) files", out)
    lines.append("- **標記檢查**（`lint-chapter-markup.py`）：" + (f"{m[1]} 個檔乾淨。" if m else (out.strip().splitlines()[-1] if out.strip() else "無輸出。")))
    out = run([py, "scripts/lint-scripture-text.py", str(BOOK)])
    m = re.search(r"(\d+) finding\(s\)", out)
    lines.append("- **和合本字形檢查**（`lint-scripture-text.py`）：" + (f"{m[1]} 項候選，須以第二來源核對。" if m else "無候選。"))
    out = run([py, "scripts/check-book-spine.py", str(BOOK)])
    ok = re.findall(r"\[(ok |GAP|--- )\]\s*(.+)", out)
    lines.append("- **骨幹檢查**（`check-book-spine.py`）：" + "；".join(f"{a.strip()} {b.strip()}" for a, b in ok))
    return "\n".join(lines)


def hymn_table():
    rows = ["| 篇 | 聖詩 | 作者 | 年份（來源頁所印） | 來源 |",
            "|--------|------------------------------|--------------------|--------------------|------------------------------|"]
    nostated = 0
    for f in sorted((SRC / "hymns").glob("[0-9][0-9]-*.txt")):
        h = {}
        for line in f.read_text(encoding="utf-8").splitlines()[:4]:
            k, _, v = line.partition(":")
            h[k.strip()] = v.strip()
        year = h.get("YEAR", "")
        if "not stated" in year.lower():
            nostated += 1
            year = "來源頁未印"
        else:
            ym = re.match(r"(\d{4})", year)
            year = (ym.group(1) + ("（依同站另一頁）" if "versions page" in year else "")) if ym else year
        url = urllib.parse.unquote(h.get('SOURCE_URL', ''))
        host = re.sub(r'^https?://', '', url).split('/')[0]
        page = re.sub(r'^https?://[^/]+/(wiki/|text/|w/index\.php\?title=)?', '', url).replace('_', ' ')
        rows.append(f"| 第{int(f.name[:2])}篇 | {h.get('TITLE', '')} | {h.get('AUTHOR', '')} | {year} | {host}：{page.replace('/', ' / ')} |")
    return "\n".join(rows), nostated


def cuv_diff_count():
    P = re.compile(r'[\s，。、；：！？「」『』（）—…·,.;:!?"\'“”‘’a-z0-9<>/=]+')
    def n(t):
        return P.sub('', t.replace('裡', '裏').replace('甚麼', '什麼').replace('玷污', '玷汙'))
    d = SRC / "scripture"
    a = {l.split('\t')[0]: n(l.split('\t', 1)[1]) for l in open(d / "cuv.tsv", encoding="utf-8")}
    b = {l.split('\t')[0]: n(l.split('\t', 1)[1]) for l in open(d / "cuvmpt.tsv", encoding="utf-8")}
    return sum(1 for k in a if a[k] != b.get(k)), len(a)


def build_ledger(skip_run):
    rows, ref = scan()
    total = sum(len(v) for w in rows.values() for v in w.values())
    n_in = 0
    for n, p in chapters():
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^## 歷代注疏.*?(?=^## )", t, re.M | re.S)
        if m:
            n_in += sum(1 for q in QUOTE.finditer(m.group(0)) if classify(q.group(2)))
    L = [FRONT, f"""
# 附錄：引用出處總表 (Appendix: Reference Ledger)

各章「歷代注疏」一節的體例說明指向本附錄。本附錄回答三件事：每條引文取自哪裏、如何核對、哪些地方只做到這一步為止。下列各表的篇次與條數由 `scripts/gen-amos-appendices.py` 直接從各篇原文讀出，不是手寫的記憶；`scripts/check-citation-ledger.py` 可再把它與各篇對照。

全書帶引號並附「— 作者，書名」出處行的逐字引文共 **{total}** 條（其中 {n_in} 條在〈歷代注疏〉一節，其餘在〈背景〉〈全經連線〉等處）。

---"""]
    for who, num in zip(WHO, "一二三四五"):
        tbl, tot = table(who, rows, ref)
        L.append(f"\n## {num}、{WHO[who][1]}\n")
        L.append(f"來源檔：{SOURCE_FILE[who]}。本書引用 **{tot}** 條，列如下。\n")
        have = sorted(rows[who])
        lack = [i for i in range(1, NUNITS + 1) if i not in rows[who]]
        if who == "morgan":
            L.append("摩根只有一篇全書概觀（pp. 197–211），不是逐章逐節的注釋；本書只在確實切題處引用，頁碼一律標出。頁碼取自 OCR 頁眉，個別頁眉被 OCR 打壞處，實際頁碼可能差一頁。"
                     f"沒有可用摩根文字的單元：{'、'.join(f'第{i}篇' for i in lack) or '無'}。以下各篇的逐字引文：\n")
        if who == "macarthur":
            L.append("gty.org 沒有麥克阿瑟的阿摩司書逐節講道，也沒有把「阿摩司書」列為經文的講章。本書引的是講別的主題、順帶讀並解釋阿摩司書段落的講章（11 篇，見 `sources/commentary/gty/INDEX.md`）。"
                     f"沒有可查材料、不立此節的單元：{'、'.join(f'第{i}篇' for i in lack) or '無'}。以下各篇的逐字引文：\n")
        if who == "calvin":
            L.append("加爾文的英譯本夾有編者按語（`— Ed.`），本書一律不當作加爾文本人的話引用。以下各篇的逐字引文：\n")
        if who == "fathers":
            L.append(f"教父引文取自 newadvent.org 的 NPNF／ANF 公有領域英譯；沒有可定位教父文字、不立〈教父時期〉的單元：{'、'.join(f'第{i}篇' for i in lack) or '無'}。耶柔米《阿摩司書注釋》不在 newadvent.org，現代版權譯本一律不用。部分教父引用的是七十士譯本型態的經文（與和合本字句不同），各篇已註明。以下各篇的逐字引文：\n")
        L.append(tbl)
        if who in ("morgan", "macarthur"):
            units = "、".join(f"第{n}章" for n in sorted(rows[who]))
            L.append(f"\n逐字引文所在單元（供 `check-citation-ledger.py` 讀取；此處「章」指本書第 N 個研讀單元，即上表的「第 N 篇」，不是阿摩司書的章）：{units}。")

    L.append("\n---\n\n## 六、機器核對現況（誠實記錄）\n")
    L.append(machine_checks(skip_run))

    nd, nv = cuv_diff_count()
    ht, nostated = hymn_table()
    L.append(f"""
---

## 七、聖經版本與核對方式

**中文：和合本（CUV）。** 底本取信望愛（fhl）的和合本（`bible.fhl.net` 的 `unv`），並與 cnbible.com 的現代標點和合本（CUVMPT）逐節比對。

- 兩者在全書 {nv} 節中，忽略標點、空格與「甚麼／什麼」等後，仍有 {nd} 節不同；多為字形、慣用詞與譯註括號的差異，不是意思的差異。本書從 fhl 的 1919 年和合本寫法。
- **「做／作」等字形未以第三來源（ai-eden.com）逐節核對**（見「十、仍未完成」）；`lint-scripture-text.py` 只做詞彙範圍的初篩。
- **fhl 的註記。** fhl 的和合本把小字譯註（「原文是」「或譯」）印進正文括號（7:14；8:14；9:13 等），本書照留。
- **專名。** 和合本專名一律照 fhl（例：泰爾，不是推羅；便哈達、哈薛、亞文、吉珥、迦斐託、亞瑪謝）。
- **希伯來文節號與中文節號一致**（阿摩司書 146 節，兩者相同），不需換算。

**英文：NASB 1995。** 取自 biblehub.com 各章頁（`biblehub.com/nasb/amos/N.htm`；斜體＝譯者補字，印為 *斜體*）。**本書沒有逐節把 biblehub 與第二個來源的 NASB 對校**，所以這一項只有單一來源。

**希伯來文。** 字頻與詞形取自 Sefaria 所載 *Miqra according to the Masorah*（本地 `sources/hebrew/amos-N.json`）。他書的希伯來文以 `sources/heb.py` 取同一來源。**全書字頻多由各篇撰寫者以正則表達式對這份資料自行計算**，每個數字附計法；未另行獨立重算，見「十、仍未完成」。

**聖詩。** 十二首，英文逐字取自下表來源頁，中譯為編者所作。來源頁沒有印年份的 {nostated} 首，出處行只寫作者。第 4、5、12 篇是替代詩（原定的〈Sinners, Turn〉〈Come, Ye Sinners〉在 Wikisource 只有目錄條目沒有歌詞，〈Jesus Shall Reign〉的文字行序錯亂）。個別來源頁的 OCR 瑕疵與節略，見 `sources/hymns/INDEX.md`。

{ht}

---

## 八、本書沒有的其他聲音

- **老弟兄**：沒有講阿摩司書的第一手教導（見〈前言〉）；各篇〈老弟兄查經〉一節只用他的方法，不加引號歸話給他。
- **麥克阿瑟**：沒有阿摩司書逐節講道；第 1、2、8、9、11 篇無可查材料。
- **教父**：耶柔米《阿摩司書注釋》不在 newadvent.org；沒有教父討論準繩異象（第 8 篇）。
- **摩根**：只有全書概觀（pp. 197–211），沒有逐章；第 5、9 篇無可用的摩根文字。

---

## 九、本書標明的未解與並陳之處

以下是各篇已在正文標明「並陳、不定案」的重點（細節以各篇為準）：3:6 災禍與耶和華；4:5 有酵的感謝祭（加爾文與亨利不同讀法）；5:13 智慧人的靜默；5:25-27 的「摩洛／神星」與徒 7:42-43 的差異；7:14 無繫詞句（「原不是」與「不是」）；7:7 אֲנָךְ 的字義；8:1-2 的雙關；9:7 的列國出埃及；9:11 的「倒塌的帳幕」；9:12 與徒 15:17 的字句差異。

---

## 十、仍未完成

1. **沒有人類審稿者。**全書的撰寫者與核對者都是 AI，各篇由同一套規格與腳本核對；沒有另一位讀者逐章通讀。這一輪尚未做獨立校對（proofread）輪，也尚未做「同一個點全章只講一次」的精簡輪。
2. **各篇篇幅偏長。**多數單元約 24–27 KB（含經文區塊），略超規格建議的 18–24 KB。
3. **「做／作」等和合本字形沒有第三來源逐節核對**（見「七」）。
4. **摩根的頁碼取自 OCR 頁眉**，個別頁碼可能差一頁。
5. **字頻與詞義。**各篇的字頻由撰寫者以正則表達式計算，可能漏算未想到的詞形（例：שׁמע 的基本詞幹 8 節，使役式 הִשְׁמִיעוּ 另見 3:9；4:5，不在其內）；若干詞義與詞形觀察是編者自己的，各篇已標明，但沒有現成注疏可對。
6. **聖詩。**{nostated} 首來源頁沒有印年份；多首為 Army and Navy Hymnal 的節略本，來源頁尚未完全校對；三首為替代詩（見「七」）。
7. **作者需要決定的事**：是否在公開發行前請人類查經老師通讀。
""")
    fm = defaultdict(int)
    for name in ["000-preface.md", "00-overview.md", "00a-amos-position.md", "00b-hearing-spine.md",
                 "00c-revelation-order.md", "elder-wong-systematic-study.md", "99-to-revelation.md", "999-afterword.md"]:
        pth = BOOK / name
        if not pth.exists():
            continue
        t = pth.read_text(encoding="utf-8")
        for m in QUOTE.finditer(t):
            w = classify(m.group(2))
            if w:
                fm[(name, w)] += 1
    if fm:
        L.append("\n---\n\n## 附：卷首與卷末框架檔的逐字引文\n")
        L.append(f"卷首與卷末框架檔另有 **{sum(fm.values())}** 條帶出處行的逐字引文：")
        for (name, w), n in sorted(fm.items()):
            L.append(f"- `{name}`：{WHO[w][0] or '教父'} {n} 條")
    return "\n".join(L)


def main():
    skip = "--no-run" in sys.argv
    idx = build_index()
    led = build_ledger(skip)
    if "--write" in sys.argv:
        OUT_INDEX.write_text(idx + "\n", encoding="utf-8")
        OUT_LEDGER.write_text(led + "\n", encoding="utf-8")
        print(f"wrote {OUT_INDEX.name} ({len(idx)} chars), {OUT_LEDGER.name} ({len(led)} chars)")
    else:
        print(idx)
        print(led)


if __name__ == "__main__":
    main()

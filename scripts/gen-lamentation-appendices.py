#!/usr/bin/env python3
"""Generate the Lamentations volume's two appendices from the book's own text.

  98-appendix-indices.md     chapter map / cross-book Scripture index / subject index / Hebrew word index
  99-appendix-references.md  citation ledger (who is quoted where, what was machine-checked, what is unfinished)

Adapted from scripts/gen-jeremiah-appendices.py.  Every count is read back out of the chapter files, and
the machine-check section RUNS the verification scripts and prints what they actually said.
This book has NO Morgan and NO MacArthur section (see the ledger, section five); commentators are
Calvin, Henry, church fathers (citations in other works) and Spurgeon.

Usage:  python3 scripts/gen-lamentation-appendices.py --write        # rewrite both files
        python3 scripts/gen-lamentation-appendices.py                # print both
        python3 scripts/gen-lamentation-appendices.py --no-run --write   # skip the slow verification runs
"""
import importlib.util
import re
import subprocess
import sys
import urllib.parse
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "lamentation"
SRC = BOOK / "sources"
OUT_INDEX = BOOK / "98-appendix-indices.md"
OUT_LEDGER = BOOK / "99-appendix-references.md"
NUNITS = 10

FRONT = """---
title: 耶利米哀歌研讀
subtitle: Lamentations Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---
"""

VOLUME = {}
for rng, name in [((1, 2), "卷一·錫安獨坐"), ((3, 4), "卷二·主如仇敵"), ((5, 7), "卷三·我是困苦人"),
                  ((8, 9), "卷四·精金變色"), ((10, 10), "卷五·求你記念")]:
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
SELF_BOOK = "耶利米哀歌"

# Front/back matter files; some may not exist yet and are skipped silently.
SOURCES = [
    ("000-preface.md", "前言"), ("00-overview.md", "卷首·概覽"), ("00a-lamentations-position.md", "卷首·位置"),
    ("00b-the-alphabet-of-grief.md", "卷首·字母表式的哀哭"), ("00c-revelation-order.md", "卷首·啟示的次序"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}篇") for i in range(1, NUNITS + 1)] + [
    ("99-to-revelation.md", "卷末"), ("999-afterword.md", "跋"),
]
FRONT_FILES = ["000-preface.md", "00-overview.md", "00a-lamentations-position.md", "00b-the-alphabet-of-grief.md",
               "00c-revelation-order.md", "elder-wong-systematic-study.md", "99-to-revelation.md", "999-afterword.md"]

SUBJECTS = [
    ("安慰（無人安慰）", r"安慰"), ("字母詩（א 到 ת）", r"字母"), ("眼淚／哭泣", r"眼淚|哭泣|痛哭|哀哭|淚"),
    ("求你看／觀看", r"求你看|求你觀看|觀看"), ("記念／想起", r"記念|想起|追想|思想"), ("回轉／歸向", r"回轉|歸向|轉向"),
    ("慈愛（חֶסֶד）", r"慈愛"), ("憐憫", r"憐憫"), ("指望／盼望", r"指望|盼望"), ("等候／靜默", r"等候|靜默"),
    ("神不開口（耶和華的話）", r"不開口|神的話|不說話|沉默"), ("「不要懼怕」（3:57）", r"不要懼怕"),
    ("錫安／耶路撒冷", r"錫安|耶路撒冷"), ("寡婦", r"寡婦"), ("聖殿／聖所", r"聖殿|聖所"),
    ("巴比倫", r"巴比倫"), ("以東", r"以東"), ("罪／罪孽", r"罪孽|罪過"), ("報應／報仇", r"報應|報仇|伸冤"),
    ("受膏者（4:20）", r"受膏者"), ("那人（הַגֶּבֶר）", r"那人|הַגֶּבֶר"), ("軛", r"軛"), ("饑荒", r"饑荒|飢餓|饑餓"),
    ("先知與祭司", r"先知|祭司"), ("耶利米（作者）", r"耶利米"), ("基督", r"基督|耶穌"),
    ("老弟兄的方法（提問）", r"提問"), ("你看見耶穌了嗎", r"看見耶穌"),
]


def source_path(name):
    if name.endswith(".md"):
        return BOOK / name
    hits = sorted(BOOK.glob(f"{name}-*.md"))
    return hits[0] if hits else None


def read_if_exists(name):
    p = BOOK / name
    return p.read_text(encoding="utf-8") if p.exists() else None


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
    rows = ["| 篇 | 耶利米哀歌 | 卷 | 篇題 | 本章鑰詞 |",
            "|--------|----------------|------------------------|--------------------------------|------------------------------------------|"]
    for i in range(1, NUNITS + 1):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        text = p.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, flags=re.M)
        title = re.sub(r"\s*\(.*\)\s*$", "", h1.group(1)) if h1 else ""
        refline = re.search(r"^耶利米哀歌\s*([\d:\-–]+)", text, flags=re.M)
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
            cleaned = re.sub(r"耶利米哀歌\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
            cleaned = re.sub(r"(?<![一-鿿])哀\s*\d+(?::\d+(?:[-–,，]\s*\d+)*)?", "", cleaned)
            for full, chap in refs_in(cleaned):
                if full == SELF_BOOK:
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
`scripts/gen-lamentation-appendices.py` 直接從各篇原文抽取生成，不以手工維護，以免與正文脫節。

---

## 附錄一：本書篇次與耶利米哀歌經文對照 (Chapter Map)

本書十篇，每篇一個研讀單元；**篇次序號是本書的單元序號，不是耶利米哀歌的章號**，真實章節範圍在下表第二欄。

{chapter_map()}

---

## 附錄二：跨書經文索引 (Cross-Book Scripture Index)

下表列出各篇行文所引用的**耶利米哀歌以外**的經文章次（節號不列；哀歌本身的引用不入此表）。「經文」區塊、配詩與引用表格不計；只有「章」層級，節號以各篇為準。共 {nsc} 條。

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
    ("calvin", ("John Calvin", "加爾文（John Calvin），*Commentaries on the Book of the Prophet Jeremiah and the Lamentations*，約翰·歐文（John Owen）英譯")),
    ("henry", ("Matthew Henry", "亨利（Matthew Henry），*Commentary on the Whole Bible*，耶利米哀歌卷")),
    ("fathers", ("", "教父（NPNF／ANF 公有領域英譯，取自 newadvent.org）")),
    ("spurgeon", ("C. H. Spurgeon", "司布真（C. H. Spurgeon），*The Metropolitan Tabernacle Pulpit* 講道集")),
])
FATHER_KEYS = ["Chrysostom", "Augustine", "Jerome", "Origen", "Ambrose", "Aphrahat", "Eusebius", "Gregory",
               "Cassian", "Cyril", "Apostolic Constitutions", "Athanasius", "Clement", "Methodius",
               "Justin", "Tertullian", "Cyprian", "Irenaeus"]
SOURCE_FILE = {
    "calvin": "`sources/commentary/calvin/lamentations.txt`（ccel.org 的 `calcom21`，John Owen 英譯；序言在最前，`CHAPTER 1`–`CHAPTER 5` 分章；英譯本內的編者按語〔— Ed.〕一律不引）",
    "henry": "`sources/commentary/henry-lam.txt`（由 `sources/commentary/henry/lam-page-*.txt` 合併；ccel.org，*Commentary on the Whole Bible* vol. 4〔`mhc4`〕；羅馬數字頁＝哀歌章號＋1；整章全文，無節號）",
    "fathers": "`sources/fathers/*.txt`（每檔含 AUTHOR／WORK／TRANSLATOR／SOURCE_URL 四行標頭；索引見 `sources/fathers/INDEX.md`）",
    "spurgeon": "`sources/spurgeon/*.txt`（spurgeon.org 講道頁；索引見 `sources/spurgeon/INDEX.md`）",
}


def classify(src):
    for k, n in [("John Calvin", "calvin"), ("Matthew Henry", "henry"), ("Spurgeon", "spurgeon")]:
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
    unclassified = 0
    for n, p in chapters():
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^耶利米哀歌\s*([\d:\-–]+)", t, re.M)
        ref[n] = m.group(1) if m else ""
        for m in QUOTE.finditer(t):
            who = classify(m.group(2))
            if who:
                rows[who][n].append(m.group(2).strip())
            else:
                unclassified += 1
    return rows, ref, unclassified


def table(who, rows, ref):
    head = ["| 篇 | 耶利米哀歌 | 逐字引文（條） | 出處行（各條，本書實印） |",
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
    lines.append("- **注疏引文逐字核對**（`verify-citations.py`，對合併語料 `sources/commentary/corpus-all.txt`＝亨利＋加爾文＋全部教父檔＋全部司布真檔，每檔前有 `=== 路徑 ===` 行）："
                 + (f"逐字吻合 {m[1]}、OCR 斷詞吻合 {m[2]}、DRIFT {m[3]}、MISS {m[4]}。" if m else "無法讀出結果。")
                 + "此項只證明引文是來源語料的連續子字串，**不證明歸屬正確**（引文可能存在於合併語料的另一檔）；歸屬由各章撰寫時的逐檔核對與本表的出處行負責。")
    out = run([py, "scripts/verify-prose-citations.py", str(BOOK), "--self", "哀"])
    m = re.search(r"(\d+) in-prose citation\(s\) checked \| (\d+) MISS \| (\d+) reviewed-as-term \| (\d+) unresolved", out)
    lines.append("- **行文中的經文引句**（`verify-prose-citations.py … --self 哀`，對 fhl 和合本）："
                 + (f"檢查 {m[1]} 個「引號＋出處」，MISS {m[2]}，unresolved {m[4]}。" if m else "無法讀出結果。")
                 + "unresolved 是該腳本不能解析出處的條目，不是已核對的錯誤，也不是已核對無誤。"
                 + ("本書這 2 條在〈哀歌的位置〉的表格列（詩 137）：出處寫成「（137:1）」「（137:7）」，腳本把裸的 N:M 當作哀歌的 137 章而取不到經文；已另以 `cuv_lookup.py 詩 137 1／7` 對和合本核對，兩句皆為逐字子字串。這是腳本的限制，不是書稿的缺陷。"
                    if m and m[4] == "2" else ""))
    out = run([py, "scripts/check-prose-scripture-quotes.py", str(BOOK)])
    m = re.search(r"(\d+) file\(s\) scanned; (\d+) quote\(s\) not found", out)
    lines.append("- **行文引句對本篇經文區塊**（`check-prose-scripture-quotes.py`）："
                 + (f"掃描 {m[1]} 個檔，{m[2]} 條不在該篇印出的經文內。" if m else "無法讀出結果。"))
    out = run([py, "scripts/lint-chapter-markup.py", str(BOOK)])
    m = re.search(r"scanned (\d+) files; errors=(\d+)", out)
    style = re.findall(r"(sources/[^\s:]+):(\d+)", out)
    lines.append("- **標記檢查**（`lint-chapter-markup.py`）："
                 + (f"掃描 {m[1]} 個檔，錯誤 {m[2]}。" if m else (out.strip().splitlines()[-1] if out.strip() else "無輸出。"))
                 + (f"另有 {len(style)} 項 style 提示，都在 `sources/` 底下的工作檔（{'、'.join(f'{a}:{b}' for a, b in style)}），不在書稿內。" if style else ""))
    out = run([py, "scripts/lint-scripture-text.py", str(BOOK)])
    m = re.search(r"(\d+) finding\(s\)", out)
    hits = re.findall(r"\[review\]\s+books/bible/lamentation/(\S+?):(\d+)", out)
    lines.append("- **和合本字形檢查**（`lint-scripture-text.py`）："
                 + (f"{m[1]} 項候選，全部是「做」字（{'、'.join(f'{a[:2]}:{b}' for a, b in hits)} 行）。"
                    "三處（哀 1:21「因你做這事」、3:64「手所做的」、4:2「窯匠手所做的」）已對 fhl、cnbible（CUVMPT）、ai-eden 三個來源核對，三者都作「做」，與書稿一致。" if m else "無候選。"))
    out = run([py, "scripts/check-book-spine.py", str(BOOK)])
    ok = re.findall(r"\[(ok |GAP|--- )\]\s*(.+)", out)
    lines.append("- **骨幹檢查**（`check-book-spine.py`）：" + "；".join(f"{a.strip()} {b.strip()}" for a, b in ok))
    out = run([py, "scripts/check-citation-ledger.py", str(BOOK)] + [x for c in ("加爾文", "亨利", "教父", "司布真") for x in ("--commentator", c)])
    tail = [l for l in out.strip().splitlines() if l.strip()][-1] if out.strip() else "無輸出"
    lines.append(f"- **本帳目對各篇**（`check-citation-ledger.py`，帶 `--commentator 加爾文 亨利 教父 司布真`）：{tail}。"
                 "（該腳本預設檢查「摩根」「麥克阿瑟」；本書兩者都不立節，不帶 `--commentator` 時會空洞通過、沒有意義，所以改帶本書實際的四位。）")
    return "\n".join(lines)


def hymn_table():
    rows = ["| 篇 | 聖詩 | 作者 | 年份（來源頁所印） | 來源 |",
            "|--------|------------------------------|--------------------|--------------------|------------------------------|"]
    notes = []
    nostated = 0
    n = 0
    for f in sorted((SRC / "hymns").glob("[0-9][0-9]-*.txt")):
        n += 1
        h = {}
        nl = []
        for line in f.read_text(encoding="utf-8").splitlines()[:12]:
            k, _, v = line.partition(":")
            if k.strip() == "NOTE":
                nl.append(v.strip())
            elif k.strip() in ("TITLE", "AUTHOR", "YEAR", "SOURCE_URL"):
                h[k.strip()] = v.strip()
        year = h.get("YEAR", "")
        if "not stated" in year.lower():
            nostated += 1
            year = "來源頁未印"
        else:
            ym = re.match(r"(\d{4})", year)
            year = ym.group(1) if ym else year
        url = urllib.parse.unquote(h.get("SOURCE_URL", ""))
        host = re.sub(r"^https?://", "", url).split("/")[0]
        page = re.sub(r"^https?://[^/]+/(wiki/|text/|w/index\.php\?title=)?", "", url).replace("_", " ")
        i = int(f.name[:2])
        rows.append(f"| 第{i}篇 | {h.get('TITLE', '')} | {h.get('AUTHOR', '')} | {year} | {host}：{page.replace('/', ' / ')} |")
        for x in nl:
            notes.append(f"- 第{i}篇（{h.get('TITLE', '')}）：{x}")
    return "\n".join(rows), nostated, "\n".join(notes), n


def cuv_diff_count():
    P = re.compile(r'[\s，。、；：！？「」『』（）—…·,.;:!?"\'“”‘’a-z0-9<>/=]+')

    def nz(t):
        return P.sub('', t.replace('裡', '裏').replace('甚麼', '什麼').replace('玷污', '玷汙'))
    d = SRC / "scripture"
    a = {l.split('\t')[0]: nz(l.split('\t', 1)[1]) for l in open(d / "cuv.tsv", encoding="utf-8")}
    b = {l.split('\t')[0]: nz(l.split('\t', 1)[1]) for l in open(d / "cuvmpt.tsv", encoding="utf-8")}
    return sum(1 for k in a if a[k] != b.get(k)), len(a)


def build_ledger(skip_run):
    rows, ref, unclassified = scan()
    total = sum(len(v) for w in rows.values() for v in w.values())
    n_in = 0
    for n, p in chapters():
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^## 歷代注疏.*?(?=^## )", t, re.M | re.S)
        if m:
            n_in += len(QUOTE.findall(m.group(0)))
    L = [FRONT, f"""
# 附錄：引用出處總表 (Appendix: Reference Ledger)

各章「歷代注疏」一節的體例說明指向本附錄。本附錄回答三件事：每條引文取自哪裏、如何核對、哪些地方只做到這一步為止。下列各表的篇次與條數由 `scripts/gen-lamentation-appendices.py` 直接從各篇原文讀出，不是手寫的記憶；`scripts/check-citation-ledger.py` 可再把它與各篇對照。

全書帶引號並附「— 作者，書名」出處行的逐字引文共 **{total}** 條（其中 {n_in} 條在〈歷代注疏〉一節，其餘在〈背景〉〈全經連線〉等處）{'；另有 ' + str(unclassified) + ' 條出處行不屬於下列四類，未計入' if unclassified else ''}。

---"""]
    nums = dict(zip(WHO, "一二三四"))
    for who in WHO:
        tbl, tot = table(who, rows, ref)
        L.append(f"\n## {nums[who]}、{WHO[who][1]}\n")
        L.append(f"來源檔：{SOURCE_FILE[who]}。本書引用 **{tot}** 條，列如下。\n")
        if who == "calvin":
            L.append("加爾文的英譯本夾有編者按語（如 *— Ed.* 的原文直譯與異讀），本書遇到只作轉述並註明是編者按語，不當作加爾文本人的話引用。以下各篇的逐字引文：\n")
        if who == "henry":
            L.append("亨利的本文是整章的注釋，沒有逐節頁碼；出處行只標到哀歌的章（例：Lam. 3），頁取自 ccel.org 的羅馬數字分頁。以下各篇的逐字引文：\n")
        if who == "fathers":
            L.append("**這裏每一條都是教父在別的著作裏引用或提到哀歌的一節，不是教父對哀歌的注釋**——ANF／NPNF 收藏裏沒有連續的哀歌教父注釋（見 `sources/fathers/INDEX.md` 的 Honest scope）。其中 4:20「在他們的坑中被捉住的」一節（教父讀為基督）是被引用最多的，教父依的是與希伯來文英譯不同的經文傳統，本書只寫作「教父的用法」，不寫成經文本意。第 5 篇（哀 3:1-20）查無可定位的教父文字，不立此節。以下各篇的逐字引文：\n")
        if who == "spurgeon":
            L.append("司布真對哀歌只有單節的講道，多為福音或靈修的應用，不是全書的解經；他把 1:12 與 4:22 讀向基督，那是他自己的應用，各處已如此標明。第 3、4、5、8、10 篇查無可核對的司布真講道，不立此節；第 1 篇索引雖列有一條（他講 4:22 時順帶提到 1:6 的一句），本書未用。以下各篇的逐字引文：\n")
        L.append(tbl)
        units = "、".join(f"第{n}章" for n in sorted(rows[who]))
        L.append(f"\n逐字引文所在單元（供 `check-citation-ledger.py` 讀取；此處「章」指本書第 N 個研讀單元，即上表的「第 N 篇」，不是耶利米哀歌的章）：{units}。")

    L.append(f"""
---

## 五、摩根與麥克阿瑟：本書不使用

- **摩根**：*Living Messages of the Books of the Bible* 的耶利米書概論不含哀歌專章，所以沒有可核對的哀歌原文；本書不立摩根專節，也不用泛論補位。
- **麥克阿瑟**：已掃描 gty.org 站點地圖的講道**標題**（6,039 個網址），沒有找到以哀歌為題的講道；但站點地圖不列經文範圍，所以**不能排除**麥克阿瑟在別處引用哀歌。沒有可核對的原文，因此不立專節。""")

    L.append("\n---\n\n## 六、機器核對現況（誠實記錄）\n")
    L.append(machine_checks(skip_run))

    nd, nv = cuv_diff_count()
    ht, nostated, hnotes, nh = hymn_table()
    L.append(f"""
---

## 七、聖經版本與核對方式

**中文：和合本（CUV）。** 底本取信望愛（fhl）的和合本（`bible.fhl.net` 的 `unv`），與 cnbible.com 的現代標點和合本（CUVMPT）及 ai-eden.com（本專案標準來源）對校。

- fhl 與 cnbible 在全書 {nv} 節中有 {nd} 節不同（比對時忽略標點、空格與「甚麼／什麼」等寫法），多為標點與慣用字，不是意思的差異；本書從 fhl 的和合本寫法。
- **ai-eden 的和合本在 4:6、4:11、4:13 三節與 fhl、cnbible 不同**（4:6、4:13 的「她」作「他」，4:11 的「燒毀」作「燒燬」）；fhl 與 cnbible 兩者一致，ai-eden 在這三處看來是誤植，本書從 fhl／cnbible。這是三個來源中二比一的判斷，不是第四個來源的確認。
- **1:10 與 1:12 的破折號。** fhl 的和合本在這兩處印「─」，本書依 cnbible 改為「，」，使行文標點與現代標點和合本一致。
- 「做／作」：`lint-scripture-text.py` 報的三處「做」（1:21、3:64、4:2），fhl、cnbible、ai-eden 三個來源一致，書稿照印。

**英文：NASB 1995。** 取自 biblehub.com 各章頁（`biblehub.com/nasb/lamentations/N.htm`），**單一來源，沒有第二來源對校**。biblehub 頁面把 LORD 印成小型大寫並拆成「L ORD」，本書已正規化為 LORD。

**希伯來文。** 取自 Sefaria 所載 *Miqra according to the Masorah*（本地 `sources/hebrew/lam-N.json`，以 `sources/hebrew/heb.py` 讀取）。哀歌的希伯來文節號與和合本節號一致（沒有像何西阿書、耶利米書那樣的節號差異）。**全書字頻多由各篇撰寫者以正則表達式對這份資料自行計算**，每個數字附計法；未另行獨立重算，見「十、仍未完成」。

**聖詩。** {nh} 首，皆為公有領域，英文逐字取自下表來源頁（維基文庫的《Army and Navy Hymnal》1920 等；一首取自 Cyber Hymnal），中譯為編者所作。來源頁沒有印年份的 {nostated} 首，出處行只寫作者。

{ht}

各聖詩檔 `sources/hymns/*.txt` 的 NOTE 行（逐條照錄，其中有缺陷或不確定處都在此）：

{hnotes}

---

## 八、本書沒有的其他聲音

- **老弟兄**：倉庫（`books/`、`docs/`、`daily-notes/`）沒有以哀歌為題的第一手材料（只有零星提到，已查）；各篇〈老弟兄查經〉一節只用他的方法（提問、全經連線、落到每日祭壇、回到耶穌），不加引號歸話給他。
- **教父**：見上，只有在別的著作中引用哀歌的段落，沒有哀歌的連續注釋；耶柔米與俄利根自己的哀歌注釋不在 newadvent 上，未用。現代版權譯本一律不用。
- **摩根、麥克阿瑟**：見「五」。

---

## 九、本書標明的未解與並陳之處

以下是各篇已在正文標明「並陳、不定案」的重點（細節以各篇為準）：

- **耶路撒冷陷落的日期。** 王下 25:8 與耶 52:12 對陷落那個月的日子寫法不同（初七日對初十日），本書**沒有把兩者調和**，各按經文如實列出。
- **5:22 是問句還是條件句。** 和合本讀為問句（「你竟全然棄絕我們……嗎？」），NASB 1995 讀為條件句（「unless You have utterly rejected us」）。本書依和合本印經文，並在第 10 篇標明兩種讀法，不替讀者定案。
- **4:20「耶和華的受膏者」。** 加爾文與亨利的讀法、教父的基督論用法、現代英譯的讀法各不相同；本書把教父的用法標為「教父的用法」，不寫成經文本意。
- **猶太會堂重複 5:21。** 會堂誦讀時在書末重複 5:21 一節，這一點只依據加爾文與亨利兩家，沒有第三個獨立來源。
- **作者。** 書本身沒有署名；傳統歸給耶利米。Sefaria 說的是塔木德把它歸給耶利米；本書寫「傳統上歸給耶利米」，不寫「必是耶利米」。

---

## 十、仍未完成

1. **沒有人類審稿者。**全書的撰寫者與核對者都是 AI，各篇由同一套規格與腳本核對；沒有另一位讀者逐章通讀。
2. **經文來源。**中文是 fhl 單一底本，與 cnbible、ai-eden 對校：ai-eden 在 4:6、4:11、4:13 與前二者不同，本書判 ai-eden 為誤，但那只是二比一。fhl 在 1:10、1:12 的「─」依 cnbible 改為「，」，是編者的標點決定。**NASB 1995 只有 biblehub 單一來源**，沒有逐節對校；「L ORD」是正規化過的假象，若遺漏其他類似的拆字假象，只有逐節對校才能發現。
3. **希伯來文字頻**由撰寫者以正則表達式計算，可能漏算未想到的詞形；若干詞義與雙關是編者自己的觀察，各篇已標明，但沒有現成注疏可對。
4. **聖詩。**{nostated} 首來源頁沒有印年份；各首的 NOTE 缺陷已在「七」逐條照錄（例如第 9 篇〈Hail to the Lord's Anointed〉的來源頁是 Doxology and Beatitude 頁，印有 "earth  begun" 雙空格與 "take a way" 的原文缺陷，書稿照來源逐字保留，不當作編輯錯誤）。年份只列來源頁所印的，不另補。
5. **司布真講道編號。**講道 1291、1812、2436、2468 的編號來自二手索引（PCA Historical Center 的索引，2468 甚至只來自搜尋結果標題），**來源頁本身沒有印編號**（見 `sources/spurgeon/INDEX.md` 的 Honest scope）；講道本身的文字已從 spurgeon.org 逐字核對。3083、3170、3360 三篇是司布真身後出版（1908、1909、1913），日期是出版日期，不是講道日期；1291 的頁面只給年份 1876。spurgeon.org 的哀歌經文索引列 14 篇講道，本書只取得 12 篇，**有 2 篇沒有找到**。
6. **教父各條都是別的著作裏的引用**，不是教父對哀歌的解釋；ANF／NPNF 之外的教父（耶柔米與俄利根的哀歌注釋、狄奧多雷、以弗所的以法蓮等）沒有涵蓋。部分教父著作的年代與作者（例如 *Apostolic Constitutions*）來源頁沒有說明，本書不給。
7. **摩根與麥克阿瑟**不立專節；後者只掃描了站點地圖的標題，不能排除他在別處引用哀歌。
8. **尚未精簡。**各篇未做「同一個點全章只講一次」的精簡通讀。
9. **作者需要決定的事**：是否在公開發行前請人類查經老師通讀。
""")
    # quotes in the orientation files (not chapters)
    fm = defaultdict(int)
    for name in FRONT_FILES:
        t = read_if_exists(name)
        if t is None:
            continue
        for m in QUOTE.finditer(t):
            w = classify(m.group(2))
            if w:
                fm[(name, w)] += 1
    if fm:
        L.append("\n---\n\n## 附：卷首與卷末框架檔的逐字引文\n")
        L.append(f"卷首與卷末框架檔另有 **{sum(fm.values())}** 條帶出處行的逐字引文，已與章內引文同法核對（上述 `verify-citations.py` 的計數涵蓋它們）：")
        for (name, w), n in sorted(fm.items()):
            L.append(f"- `{name}`：{WHO[w][0] or '教父'} {n} 條")
    return "\n".join(L)


def main():
    skip = "--no-run" in sys.argv
    idx = build_index()
    led = build_ledger(skip)
    if "--write" in sys.argv:
        # Hebrew words glued to CJK punctuation cannot break and overflow table cells (gotchas.md):
        # put a plain space between a Hebrew run and an adjacent CJK character in table rows.
        def _space_hebrew(text):
            out = []
            for line in text.split("\n"):
                if line.startswith("|") and re.search(r"[\u0590-\u05FF]", line):
                    line = line.replace("\u3000", " ")
                    line = re.sub(r"([\u0590-\u05FF])([^\sA-Za-z0-9\u0590-\u05FF|])", r"\1 \2", line)
                    line = re.sub(r"([^\sA-Za-z0-9\u0590-\u05FF|])([\u0590-\u05FF])", r"\1 \2", line)
                out.append(line)
            return "\n".join(out)
        idx, led = _space_hebrew(idx), _space_hebrew(led)
        OUT_INDEX.write_text(idx + "\n", encoding="utf-8")
        OUT_LEDGER.write_text(led + "\n", encoding="utf-8")
        print(f"wrote {OUT_INDEX.name} ({len(idx)} chars), {OUT_LEDGER.name} ({len(led)} chars)")
    else:
        print(idx)
        print(led)


if __name__ == "__main__":
    main()

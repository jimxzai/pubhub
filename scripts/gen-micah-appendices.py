#!/usr/bin/env python3
"""Generate the Micah volume's two appendices from the book's own text.

  98-appendix-indices.md     chapter map / cross-book Scripture index / subject index / Hebrew word index
  99-appendix-references.md  citation ledger (who is quoted where, what was machine-checked, what is unfinished)

Adapted from scripts/gen-jeremiah-appendices.py.  Every count is read back out of the chapter files and
the source folders; the machine-check section RUNS the verification scripts and prints what they said.
Front/back-matter files that do not exist yet are skipped, so the script can be re-run as they appear.

Usage:  python3 scripts/gen-micah-appendices.py --write        # rewrite both files
        python3 scripts/gen-micah-appendices.py                # print both
        python3 scripts/gen-micah-appendices.py --no-run --write   # skip the slow verification runs
"""
import importlib.util
import re
import subprocess
import sys
import tempfile
import urllib.parse
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "Micah"
SRC = BOOK / "sources"
OUT_INDEX = BOOK / "98-appendix-indices.md"
OUT_LEDGER = BOOK / "99-appendix-references.md"
NUNITS = 9

FRONT = """---
title: 彌迦書研讀
subtitle: Micah Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---
"""

VOLUME = {}
for rng, name in [((1, 2), "卷一·聽——神親自下來"), ((3, 6), "卷二·官長與山"), ((7, 9), "卷三·爭辯與等候")]:
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
SELF_BOOK = next((full for full, al in BOOKS if "彌迦書" in al or full == "彌迦書"), "彌迦書")

SOURCES = [
    ("000-preface.md", "前言"), ("00-overview.md", "卷首·概覽"), ("00a-micah-position.md", "卷首·位置"),
    ("00b-hear-spine.md", "卷首·骨幹"), ("00c-revelation-order.md", "卷首·啟示的次序"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}篇") for i in range(1, NUNITS + 1)] + [
    ("99-to-revelation.md", "卷末"), ("999-afterword.md", "跋"),
]
FRAME_FILES = [n for n, _ in SOURCES if n.endswith(".md")]

SUBJECTS = [
    ("聽", r"聽"), ("見證", r"見證"), ("降臨", r"降臨"), ("高處／邱壇", r"高處|邱壇"),
    ("撒瑪利亞", r"撒瑪利亞"), ("耶路撒冷", r"耶路撒冷"), ("田地", r"田地|田畝|田"),
    ("首領／官長", r"首領|官長|審判官|君王"), ("先知／假先知", r"假先知|先知"), ("祭司", r"祭司"),
    ("平安", r"平安"), ("餘民／餘剩", r"餘民|餘剩|剩下"), ("招聚", r"招聚|聚集"),
    ("山／殿的山", r"殿的山|耶和華殿的山|錫安山|山"), ("末後的日子", r"末後的日子|末後"),
    ("刀／犁頭", r"犁頭|刀打成"), ("伯利恆", r"伯利恆"), ("牧養／牧者", r"牧養|牧者|牧人"),
    ("亙古", r"亙古|永古|從太初"), ("爭辯／辨屈", r"爭辯|辨屈|辯論"), ("公義", r"公義"),
    ("憐憫／慈愛", r"憐憫|慈愛"), ("謙卑", r"謙卑"), ("獻祭／燔祭", r"獻祭|燔祭|祭物"),
    ("暗利／亞哈", r"暗利|亞哈"), ("哀哭／哀號", r"哀哭|哀號|哀鳴"), ("等候／仰望", r"等候|仰望"),
    ("赦免", r"赦免|赦罪|饒恕"), ("深海", r"深海"), ("亞伯拉罕", r"亞伯拉罕"),
    ("耶利米書（跨書）", r"耶利米書|耶\s*26"), ("以賽亞書（賽2）", r"賽\s*2|以賽亞書\s*2"),
    ("老弟兄的方法（提問）", r"提問"), ("你看見耶穌了嗎", r"看見耶穌"),
]


def source_path(name):
    if name.endswith(".md"):
        p = BOOK / name
        return p if p.exists() else None
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
    rows = ["| 篇 | 彌迦書 | 卷 | 篇題 | 本章鑰詞 |",
            "|--------|----------------|------------------------|--------------------------------|------------------------------------------|"]
    for i in range(1, NUNITS + 1):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        text = p.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, flags=re.M)
        title = re.sub(r"\s*\(.*\)\s*$", "", h1.group(1)) if h1 else ""
        refline = re.search(r"^彌迦書\s*([\d:\-–]+)", text, flags=re.M)
        key = re.search(r"本章鑰詞[：:]\s*\**([^\n\\]*?)\**\s*(?:\\|$)", text, flags=re.M)
        rows.append(f"| {i:02d} | {refline.group(1) if refline else ''} | {VOLUME[i]} | {title} | "
                    f"{key.group(1).strip(' *') if key else ''} |")
    return "\n".join(rows)


def scripture_index():
    index = defaultdict(set)
    for fname, label in SOURCES:
        p = source_path(fname)
        if not p:
            continue
        for line in prose_lines(p):
            # Micah's own references (full name or the short 彌) are not another book; a bare "5:2" carries
            # no book alias and so is never matched by REF in the first place.
            cleaned = re.sub(r"彌迦書\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
            cleaned = re.sub(r"(?<![一-鿿])彌\s*\d+(?::\d+(?:[-–,，]\s*\d+)*)?", "", cleaned)
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
        out.append(f"| {name} | {'、'.join(where) if where else '（本書正文未見）'} |")
    return "\n".join(out)


def hebrew_index():
    out = ["| 原文 | 出處 | 見 | 要點 |", "|--------------|------------------------------|------------|------------------------------------|"]
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
            out.append(f"| {cells[0]} | {cells[1].replace('；', '； ')} | 第{i}篇 | {gloss} |")
    return "\n".join(out)


def build_index():
    sc, nsc = scripture_index()
    return FRONT + f"""
# 附錄：經文與主題索引 (Appendix: Scripture & Subject Indices)

本附錄依全書正文實際出現的內容編製，不另行增列各篇未曾論及的經文或主題。四張表都由
`scripts/gen-micah-appendices.py` 直接從各篇原文抽取生成，不以手工維護，以免與正文脫節。

---

## 附錄一：本書篇次與彌迦書經文對照 (Chapter Map)

本書九篇，每篇一個研讀單元；**篇次序號是本書的單元序號，不是彌迦書的章號**，真實章節範圍在下表第二欄（第 5 篇跨 4:9–5:1；和合本 5:1 即希伯來文 4:14）。

{chapter_map()}

---

## 附錄二：跨書經文索引 (Cross-Book Scripture Index)

下表列出各篇行文所引用的**彌迦書以外**的經文章次（節號不列；彌迦書本身的引用，不論寫全名、簡稱或只寫「5:2」，都不入此表）。「經文」區塊、配詩與引用表格不計；只有「章」層級，節號以各篇為準。共 {nsc} 條。

{sc}

---

## 附錄三：主題索引 (Subject Index)

以下主題由各篇行文（不含經文區塊、配詩、今天的祭壇、禱告回應、默想問題與引用表格）逐篇以正則表達式計數得出，出現至少一次即列；正文未見者明列「未見」，不省略。

{subject_index()}

---

## 附錄四：原文詞彙索引 (Hebrew Word Index)

各篇〈原文研讀〉表格中的希伯來文詞，依篇次列出（每條只取該列意義欄第一個分句）。

{hebrew_index()}
"""


# ---------------------------------------------------------------- ledger
WHO = OrderedDict([
    ("calvin", ("John Calvin", "加爾文（John Calvin），*Commentaries on the Twelve Minor Prophets*, vol. 3（Jonah, Micah, Nahum），約翰·歐文（John Owen）英譯")),
    ("henry", ("Matthew Henry", "馬太·亨利（Matthew Henry），*Commentary on the Whole Bible*，彌迦書卷")),
    ("morgan", ("G. Campbell Morgan", "摩根（G. Campbell Morgan），*The Message of Micah*，載 *Living Messages of the Books of the Bible*, vol. 1（1912）")),
    ("macarthur", ("John MacArthur", "麥克阿瑟（John MacArthur），gty.org 講章")),
    ("fathers", ("", "教父（NPNF／ANF 公有領域英譯，取自 newadvent.org）")),
])
FATHER_KEYS = ["Chrysostom", "Augustine", "Justin", "Origen", "Eusebius", "Tertullian", "Jerome", "Cyprian", "Irenaeus"]
SOURCE_FILE = {
    "calvin": "`sources/commentary/calvin/micah-only.txt`（取自 ccel.org 的 `calcom28`，加爾文《十二小先知書注釋》第三卷〔約拿、彌迦、鴻〕中彌迦書的部分；英譯本內的編者按語〔段尾署 — Ed.〕一律不當作加爾文引用）",
    "henry": "`sources/commentary/henry/mic-page-i.txt`–`mic-page-viii.txt`（ccel.org，*Commentary on the Whole Bible* vol. 4〔`mhc4.Mic`〕第 i–viii 頁；整章全文，無節號）",
    "morgan": "`sources/commentary/morgan/message-of-micah.txt`（archive.org *Living Messages of the Books of the Bible* vol. 1 的 OCR 掃描；只有一篇全書概觀，pp. 243–255；頁碼取自 OCR 頁眉，頁眉偶有錯字）",
    "macarthur": "`sources/gty/<CODE>.txt`（gty.org 講章逐字稿；索引見 `sources/gty/INDEX.md`）",
    "fathers": "`sources/fathers/*.txt`（newadvent.org 的 NPNF／ANF 摘錄檔；索引見 `sources/fathers/INDEX.md`）",
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
        m = re.search(r"^彌迦書\s*([\d:\-–]+)", t, re.M)
        ref[n] = m.group(1) if m else ""
        for m in QUOTE.finditer(t):
            who = classify(m.group(2))
            if who:
                rows[who][n].append(m.group(2).strip())
    return rows, ref


def table(who, rows, ref):
    head = ["| 篇 | 彌迦書 | 逐字引文（條） | 出處行（各條，本書實印） |",
            "|------------|----------------|----------------|----------------------------------------------------|"]
    body = []
    for n in sorted(rows[who]):
        srcs = rows[who][n]
        distinct = list(OrderedDict.fromkeys(re.sub(r"\*", "", s) for s in srcs))
        body.append(f"| 第{n}篇 | {ref[n]} | {len(srcs)} | " + "；".join(distinct) + " |")
    total = sum(len(v) for v in rows[who].values())
    return "\n".join(head + body), total


def units_text(units):
    units = sorted(units)
    return "、".join(f"第{n}篇" for n in units) if units else "（無）"


def run(cmd, timeout=900):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa: BLE001
        return f"ERROR {e}"


def combined_corpus(tmpdir):
    """corpus.txt holds Calvin + Henry + Morgan only; gty and fathers are separate folders."""
    out = Path(tmpdir) / "corpus-all.txt"
    parts = [(SRC / "commentary" / "corpus.txt").read_text(encoding="utf-8", errors="replace")]
    for folder in ("gty", "fathers"):
        for f in sorted((SRC / folder).glob("*.txt")):
            parts.append(f"\n=== SOURCE: {folder} {f.stem} ===\n" + f.read_text(encoding="utf-8", errors="replace"))
    out.write_text("\n".join(parts), encoding="utf-8")
    return out


def machine_checks(skip, n_mac=0):
    if skip:
        return "（本次生成以 `--no-run` 略過逐項執行；請不帶該旗標重新生成。）"
    py = sys.executable
    book = str(BOOK)
    lines = []
    pat = r"verbatim OK:\s*(\d+)\s+OK-OCR:\s*(\d+)\s+DRIFT:\s*(\d+)\s+MISS:\s*(\d+)"
    out = run([py, "scripts/verify-citations.py", book, "--source", str(SRC / "commentary" / "corpus.txt")])
    m = re.search(pat, out)
    miss_kinds = defaultdict(int)
    for who in re.findall(r"^\s*MISS\s+\[([^\]]+)\]", out, re.M):
        miss_kinds[who.split(" (")[0]] += 1
    lines.append("- **注疏引文逐字核對，對 `sources/commentary/corpus.txt`**（`verify-citations.py`；此語料只含加爾文＋亨利＋摩根三家，**不含**教父與麥克阿瑟）："
                 + (f"逐字吻合 {m[1]}、OCR 斷詞吻合 {m[2]}、DRIFT {m[3]}、MISS {m[4]}。" if m else "無法讀出結果。")
                 + (f"MISS 全數屬於不在該語料內的兩家：{'、'.join(f'{k} {v}' for k, v in sorted(miss_kinds.items()))}（教父在書稿中置於「教父時期」小節）；這是語料範圍所致，不是已核對的錯誤，下一項補上。" if miss_kinds else ""))
    with tempfile.TemporaryDirectory() as td:
        corpus = combined_corpus(td)
        out2 = run([py, "scripts/verify-citations.py", book, "--source", str(corpus)])
    m = re.search(pat, out2)
    lines.append("- **注疏引文逐字核對，對合併語料**（同一腳本，語料＝上述三家＋`sources/gty/*.txt`＋`sources/fathers/*.txt`，由本生成器於執行時暫時合併）："
                 + (f"逐字吻合 {m[1]}、OCR 斷詞吻合 {m[2]}、DRIFT {m[3]}、MISS {m[4]}。" if m else "無法讀出結果。")
                 + "此項只證明引文是來源語料的連續子字串，**不證明歸屬正確**，也不證明該句在原著中的語境。")
    out = run([py, "scripts/verify-sermon-quotes.py", book])
    m = re.search(r"verified:\s*(\d+)\s+missing from own transcript:\s*(\d+)\s+unresolved:\s*(\d+)", out)
    lines.append("- **麥克阿瑟引文對各自講章核對**（`verify-sermon-quotes.py`，每條只對它自己出處行 `sermon CODE` 的講章）："
                 + (f"核對 {m[1]} 條吻合，不在自己講章內 {m[2]} 條，無法解析 {m[3]} 條。" if m else "無法讀出結果。")
                 + (f"（本表由 `> — ` 出處行逐條計得的麥克阿瑟引文為 {n_mac} 條；腳本的 {m[1]} 條是它自己對 `> \"…\"` 與出處行的配對方式所得，兩個數字相差 {int(m[1]) - n_mac}，**這個差額未逐條追查**。）" if m and int(m[1]) != n_mac else ""))
    out = run([py, "scripts/verify-prose-citations.py", book, "--self", "彌"])
    m = re.search(r"(\d+) in-prose citation\(s\) checked \| (\d+) MISS \| (\d+) reviewed-as-term \| (\d+) unresolved", out)
    lines.append("- **行文中的經文引句**（`verify-prose-citations.py … --self 彌`，對 fhl 和合本）："
                 + (f"檢查 {m[1]} 個「引號＋出處」，MISS {m[2]}，reviewed-as-term {m[3]}，unresolved {m[4]}。" if m else "無法讀出結果。")
                 + "unresolved 是該腳本不能解析出處的條目，不是已核對的錯誤，也不是已核對無誤。"
                 + ("MISS 條目（腳本實印）：" + "；".join(f"{a}（{b}）" for a, b in re.findall(r"^\s*MISS\s+(\S+)\s+（(.+?)）", out, re.M)) + "。" if m and m[2] != "0" else ""))
    out = run([py, "scripts/check-prose-scripture-quotes.py", book])
    m = re.search(r"(\d+) file\(s\) scanned; (\d+) quote\(s\) not found", out)
    lines.append("- **行文引句對本篇經文區塊**（`check-prose-scripture-quotes.py`）："
                 + (f"掃描 {m[1]} 個檔，{m[2]} 條不在該篇印出的經文內。" if m else "無法讀出結果。"))
    out = run([py, "scripts/lint-chapter-markup.py", book])
    m = re.search(r"clean: (\d+) files", out)
    lines.append("- **標記檢查**（`lint-chapter-markup.py`）：" + (f"{m[1]} 個檔乾淨。" if m else out.strip().splitlines()[-1] if out.strip() else "無輸出。"))
    out = run([py, "scripts/lint-scripture-text.py", book])
    m = re.search(r"(\d+) finding\(s\)", out)
    cand = re.findall(r"^\s*\[review\]\s+(\S+?):(\d+)\s+「(.+?)」", out, re.M)
    lines.append("- **和合本字形檢查**（`lint-scripture-text.py`）："
                 + (f"{m[1]} 項候選（皆為「須回查」的候選，不是已確認的錯字）" + ("：" + "；".join(f"{a}:{b}「{c}」" for a, b, c in cand) if cand else "") + "。" if m else "無候選。"))
    out = run([py, "scripts/check-citation-ledger.py", book])
    last = [l.strip() for l in out.strip().splitlines() if l.strip()]
    lines.append("- **帳目與書稿對照**（`check-citation-ledger.py`，讀的是上一次寫出的本附錄，故首次生成後須再跑一次才反映本次內容）：" + (last[-1] if last else "無輸出。"))
    out = run([py, "scripts/check-book-spine.py", book])
    ok = re.findall(r"\[(ok |GAP|--- )\]\s*(.+)", out)
    lines.append("- **骨幹檢查**（`check-book-spine.py`）：" + "；".join(f"{a.strip()} {b.strip()}" for a, b in ok))
    return "\n".join(lines)


def hymn_table():
    rows = ["| 篇 | 聖詩 | 作者 | 年份（來源頁所印） | 來源 |",
            "|----------|--------------------|----------------|----------|------------------------------------------|"]
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
            year = (ym.group(1) + ("（依同站另一頁）" if "per en.wikisource page" in year else "")) if ym else year
        url = urllib.parse.unquote(h.get('SOURCE_URL', ''))
        host = re.sub(r'^https?://', '', url).split('/')[0]
        page = re.sub(r'^https?://[^/]+/(wiki/|text/|w/index\.php\?title=)?', '', url).replace('_', ' ')
        rows.append(f"| 第{int(f.name[:2])}篇 | {h.get('TITLE', '')} | {h.get('AUTHOR', '')} | {year} | {host}：{page.replace('/', ' / ')} |")
    return "\n".join(rows), nostated, len(rows) - 2


def cuv_diff_count():
    """Same comparison as sources/scripture/extract.py prints as DIFF (punctuation and spaces ignored only)."""
    P = re.compile(r'[\s，。、；：！？「」『』（）—…·,.;:!?"\'“”‘’]')
    d = SRC / "scripture"
    a = {l.split('\t')[0]: P.sub('', l.split('\t', 1)[1]) for l in open(d / "cuv.tsv", encoding="utf-8")}
    b = {l.split('\t')[0]: P.sub('', l.split('\t', 1)[1]) for l in open(d / "cuvmpt.tsv", encoding="utf-8")}
    return sum(1 for k in a if a[k] != b.get(k)), len(a)


def fathers_character():
    """Count the 性質 column of sources/fathers/INDEX.md."""
    disc = using = 0
    p = SRC / "fathers" / "INDEX.md"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if line.startswith("| ") and len(cells) >= 7:
                if cells[6].startswith("discussing Micah"):
                    disc += 1
                elif cells[6].startswith("using Micah"):
                    using += 1
    return disc, using


def build_ledger(skip_run):
    rows, ref = scan()
    total = sum(len(v) for w in rows.values() for v in w.values())
    n_in = 0
    for n, p in chapters():
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^## 歷代注疏.*?(?=^## )", t, re.M | re.S)
        if m:
            n_in += len(QUOTE.findall(m.group(0)))
    all_units = set(range(1, NUNITS + 1))
    present = {n for n, _ in chapters()}
    L = [FRONT, f"""
# 附錄：引用出處總表 (Appendix: Reference Ledger)

各章「歷代注疏」一節的體例說明指向本附錄。本附錄回答三件事：每條引文取自哪裏、如何核對、哪些地方只做到這一步為止。下列各表的篇次與條數由 `scripts/gen-micah-appendices.py` 直接從各篇原文讀出，不是手寫的記憶。

全書各篇帶引號並附「— 作者，書名」出處行的逐字引文共 **{total}** 條（其中 {n_in} 條在〈歷代注疏〉一節，其餘在〈背景〉〈全經連線〉等處）。目前讀到的研讀單元檔共 {len(present)} 個。

---"""]
    cnt = {w: sum(len(v) for v in rows[w].values()) for w in WHO}
    for who, num in zip(WHO, "一二三四五"):
        tbl, tot = table(who, rows, ref)
        have = set(rows[who])
        L.append(f"\n## {num}、{WHO[who][1]}\n")
        L.append(f"來源檔：{SOURCE_FILE[who]}。本書引用 **{tot}** 條，分布在 {len(have)} 篇，列如下。\n")
        if who == "calvin":
            ed = 0
            mp = SRC / "commentary" / "calvin" / "micah-only.txt"
            if mp.exists():
                ed = len(re.findall(r"[—-]\s*Ed\.", mp.read_text(encoding="utf-8", errors="replace")))
            L.append(f"加爾文的英譯本夾有大量編者按語（`micah-only.txt` 內段尾署 — Ed. 的字樣共 {ed} 處）與他人引文（Henderson、Henry 等），本書一律不當作加爾文本人的話引用，要提只作轉述並註明是編者按語。無加爾文引文的篇：{units_text(all_units - have)}。以下各篇的逐字引文：\n")
        if who == "henry":
            L.append(f"亨利無引文的篇：{units_text(all_units - have)}。以下各篇的逐字引文：\n")
        if who == "morgan":
            pages = sorted({int(x) for s in rows[who].values() for e in s for x in re.findall(r"\bp\.\s*(\d+)", e)})
            L.append(f"摩根只有一篇全書概觀（pp. 243–255），主題是「權柄」，不是逐章逐節的注釋；本書只在確實切題處引用，頁碼一律標出（本書用到的頁碼：{'、'.join(f'p. {x}' for x in pages) or '（無）'}）。其中頁碼取自 OCR 頁眉，頁眉偶有錯字，實際頁碼可能差一頁。摩根沒有引文的篇：{units_text(all_units - have)}（`sources/commentary/morgan/INDEX.md` 載明他只引用 3:1-3、3:5、3:11、5:2、5:4、5:5，並概括提到 5:10-14；書稿不可把其他經文的解釋歸給他）。以下各篇的逐字引文：\n")
        if who == "macarthur":
            ng = len(list((SRC / "gty").glob("[0-9]*.txt")))
            cited = {c for s in rows[who].values() for e in s for c in re.findall(r"sermon\s+([\d-]+)", e)}
            L.append(f"gty.org **沒有麥克阿瑟的彌迦書逐節講道系列**；`sources/gty/INDEX.md` 收了 {ng} 篇他在講別的題目時讀出彌迦經文並加以解說的講章（聖誕節 5:2、赦罪 7:18-19、聖靈 3:8、謙卑 6:8 等）。本書只能寫成「他在講某題時引用彌迦書某節」，不是「麥克阿瑟注釋彌迦書」。已引用的講章 {len(cited)} 篇（{'、'.join(sorted(cited))}）。沒有麥克阿瑟段落的篇：{units_text(all_units - have)}。以下各篇的逐字引文：\n")
        if who == "fathers":
            disc, using = fathers_character()
            L.append(f"教父摘錄檔的索引（`sources/fathers/INDEX.md`）共 {disc + using} 條：其中 {disc} 條是教父**針對彌迦經文本身**作的解說或論證（discussing Micah），{using} 條只是**借彌迦書作別的論證**（護教、年代、祭祀神學、敘事；using Micah for another argument）。後者不可寫成「某教父注釋彌迦書」。教父引文所在的篇：{units_text(have)}；沒有教父引文的篇：{units_text(all_units - have)}；這些篇在 newadvent.org 取得的檔案內查無可定位的教父文字。現代版權譯本一律不用。以下各篇的逐字引文：\n")
        L.append(tbl)
        if who in ("morgan", "macarthur"):
            units = "、".join(f"第{n}章" for n in sorted(rows[who]))
            L.append(f"\n逐字引文所在單元（供 `check-citation-ledger.py` 讀取；此處「章」指本書第 N 個研讀單元，即上表的「第 N 篇」，不是彌迦書的章）：{units or '（無）'}。")

    L.append("\n---\n\n## 六、機器核對現況（誠實記錄）\n")
    L.append(machine_checks(skip_run, cnt['macarthur']))

    nd, nv = cuv_diff_count()
    ht, nostated, nh = hymn_table()
    L.append(f"""
---

## 七、聖經版本與核對方式

**中文：和合本（CUV）。** 底本取信望愛（fhl）的和合本（`bible.fhl.net` 的 `unv`），再與 cnbible.com 的現代標點和合本（CUVMPT）對校（`sources/scripture/extract.py` 的 DIFF 輸出）。

- 兩者在 {nd} 節（全書 {nv} 節）有出入，這是只忽略標點與空格、未做任何字形或譯名正規化時的原始節數；多數是 cnbible 頁面的註腳殘留與現代、舊式字形或譯名寫法的差異（如「裡／裏」「甚麼／什麼」），不是意思的差異。本書從 fhl 的 1919 年和合本寫法。
- **ai-eden.com 第三來源核對：未做。** `sources/scripture/` 內沒有 ai-eden 核對的產出或腳本（`inject_scripture.py` 僅在註解中提到它）。因此「做／作」等字形沒有逐節以 ai-eden 核對，見「九、仍未完成」。
- **和合本併節。** 和合本在少數節把相鄰節併排印出（以 `inject_scripture.py` 處理），英文 NASB 仍分節，所以兩欄的節號在併節處可能不同。
- **希伯來文節號。** Sefaria 採希伯來文節號：和合本 5:1 ＝ 希伯來文 4:14，希伯來文 5:1–14 ＝ 和合本 5:2–15（例如 5:15 在希伯來文是 5:14）。本書正文一律用和合本節號，引用希伯來文時已換算。
- **fhl 的註記。** fhl 的和合本把小字譯註（「原文是」「或譯」）印進正文括號，本書照留。

**英文：NASB 1995。** 取自 biblehub.com 各章頁（`biblehub.com/nasb/micah/N.htm`；斜體＝譯者補字，印為 *斜體*）。本書沒有把 biblehub 與第二來源逐節對校，所以這一項只有單一來源。

**希伯來文。** 字頻與詞形取自 Sefaria 所載 *Miqra according to the Masorah*（本地 `sources/hebrew/mic-N.json`）。**全書字頻多由各篇撰寫者以正則表達式對這份資料自行計算**，每個數字附計法；未另行獨立重算，見「九、仍未完成」。

**聖詩。** {nh} 首，英文取自下表來源頁，中譯為編者所作。來源頁沒有印年份的 {nostated} 首，出處行只寫作者。

{ht}

聖詩來源的誠實註記：第 3 篇〈O Spirit of the Living God〉保留來源頁 OCR 的字距，不更動；第 2 篇〈The King of Love My Shepherd Is〉的來源頁連字號斷詞已去除；第 6 篇〈O Little Town of Bethlehem〉取自 *Our American Holidays: Christmas* 一書，不是詩集單頁；第 8、9 篇取自 *Olney Hymns*（1840 年版）。

---

## 八、本書沒有的其他聲音

- **老弟兄**：倉庫內查無他講彌迦書的第一手材料（已 grep）；各篇〈老弟兄查經〉一節只用他的方法（提問），不加引號歸話給他。
- **麥克阿瑟**：沒有彌迦書逐節講道；沒有麥克阿瑟段落的篇：{units_text(all_units - set(rows['macarthur']))}。
- **教父**：沒有教父引文的篇：{units_text(all_units - set(rows['fathers']))}。
- **摩根**：只有全書概觀，沒有逐章；沒有摩根引文的篇：{units_text(all_units - set(rows['morgan']))}。
- **加爾文**：沒有加爾文引文的篇：{units_text(all_units - set(rows['calvin']))}。
- **亨利**：沒有亨利引文的篇：{units_text(all_units - set(rows['henry']))}。
""")
    big = []
    for n, p in chapters():
        sz = p.stat().st_size
        if sz > 26 * 1024:
            big.append(f"第 {n} 篇 {sz / 1024:.1f} KB")
    missing_front = [n for n in FRAME_FILES if not (BOOK / n).exists()]
    ed = 0
    mp = SRC / "commentary" / "calvin" / "micah-only.txt"
    if mp.exists():
        ed = len(re.findall(r"[—-]\s*Ed\.", mp.read_text(encoding="utf-8", errors="replace")))
    disc, using = fathers_character()
    L.append(f"""---

## 九、仍未完成

1. **沒有獨立校對輪。**全書的撰寫者與核對者都是 AI；尚未做過另一位讀者（人類或不看既有報告、向原始來源重新取證的獨立 AI 代理）逐章通讀的校對輪。上列機器核對只證明引文與來源語料吻合，不證明歸屬與語境正確。
2. **尚未精簡。**九篇各篇篇幅 {min((p.stat().st_size for _, p in chapters()), default=0) / 1024:.1f}–{max((p.stat().st_size for _, p in chapters()), default=0) / 1024:.1f} KB（含經文區塊），尚未做「同一個點全章只講一次」的精簡通讀。{'超過 26 KB 的篇：' + '、'.join(big) + '。' if big else '沒有超過 26 KB 的篇。'}
3. **和合本「做／作」等字形未逐節對 ai-eden 核對**（見「七」；`lint-scripture-text.py` 的候選見「六」）。
4. **加爾文編者按語。**`micah-only.txt` 內有 {ed} 處編者按語，雖已規定不引，但篇內轉述是否都有註明「編者按語」未逐條覆核。
5. **麥克阿瑟的缺口。**他沒有彌迦書逐節講道；沒有他段落的篇：{units_text(all_units - set(rows['macarthur']))}；有段落的篇也只是他講別的題目時順帶解說，不是逐節解經。
6. **摩根的缺口。**只有 pp. 243–255 的全書概觀，OCR 掃描、頁碼取自頁眉可能差一頁；沒有他段落的篇：{units_text(all_units - set(rows['morgan']))}。
7. **教父的缺口。**教父摘錄 {disc + using} 條中，只有 {disc} 條是針對彌迦經文本身的解說，{using} 條是借彌迦書作別的論證；沒有教父段落的篇：{units_text(all_units - set(rows['fathers']))}。
8. **字頻與詞義。**各篇的字頻由撰寫者以正則表達式計算，可能漏算未想到的詞形；若干詞義與雙關是編者自己的觀察，各篇已標明，但這些觀察沒有現成注疏可對。
9. **聖詩。**{nostated} 首來源頁沒有印年份；第 3 篇保留 OCR 字距、第 2 篇連字號斷詞已去除（見「七」）；聖詩與經文的關聯是編者所選，各篇配詩說明不宜宣稱互相引用。
10. **卷首與卷末框架檔。**{'尚未寫成、本次生成時不存在的檔案：' + '、'.join(f'`{n}`' for n in missing_front) + '（寫成後請重新執行本生成器，索引與帳目會自動納入）。' if missing_front else '框架檔皆已存在。'}
11. **作者需要決定的事**：是否在公開發行前請人類查經老師通讀。
""")
    # quotes in the orientation files (not chapters)
    fm = defaultdict(int)
    for name in FRAME_FILES:
        p = BOOK / name
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
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
        OUT_INDEX.write_text(idx + "\n", encoding="utf-8")
        OUT_LEDGER.write_text(led + "\n", encoding="utf-8")
        print(f"wrote {OUT_INDEX.name} ({len(idx)} chars), {OUT_LEDGER.name} ({len(led)} chars)")
    else:
        print(idx)
        print(led)


if __name__ == "__main__":
    main()

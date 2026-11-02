#!/usr/bin/env python3
"""check-worship-book.py — structural, spine and honesty checks for books/bible/hymnWorship.

Why this exists: the Worship Book is one generated file, so the per-chapter checkers
(check-book-spine.py, lint-chapter-markup.py, verify-citations.py) cannot read it.  Every class of
defect below was found by an independent human-style proofread of this book; each is now a check.

Checks (each prints PASS/FAIL; exit 1 if any FAIL):
  spine     orientation chapter with 全書座標 and a closing 「你看見耶穌了嗎」; each 卷 carries
            「啟示的次序·第N步」 and 「全書座標」 and closes with 「你看見耶穌了嗎」
  items     every psalm has a labelled 看見耶穌 line; every hymn has 詞與年份 / 出處註記 / 配經 / 默想 / 見於本庫
  xref      every 「聖詩 N《title》」 equals the numbered heading N
  counts    counts the preface/appendix claim (hymns, psalms) equal the headings
  scripture every psalm block equals ai-eden cuv.json (modulo the documented Ps 46:4 patch,
            placeholders dropped)
  elder     every quotation printed next to 老弟兄 occurs verbatim in the repo file it cites
  style     no 祢 / 什麼 / 上帝 in editor-written text (verbatim scripture blocks exempt)
  leaks     no unexpanded template markers
Usage: scripts/check-worship-book.py [path-to-body.md]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BODY = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "output" / "hymnworship-body.md"
CUV = Path("/Users/jimxiao/dev/ai-eden/data/cuv.json")
SOURCES = {
    "psalm/13-prayer-testimony.md": ROOT / "books/bible/psalm/13-prayer-testimony.md",
    "gospel-of-john/04-samaritan-woman.md": ROOT / "books/bible/gospel-of-john/04-samaritan-woman.md",
}
text = BODY.read_text(encoding="utf-8")
fails = []


def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (f"  — {detail}" if detail and not ok else ""))
    if not ok:
        fails.append(name)


def sections(level="# "):
    """Split on top-level headings: [(title, body)]"""
    parts = re.split(rf"(?m)^{re.escape(level)}(.+?)(?: \{{\.unnumbered\}})?$", text)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


S = sections()
titles = [t for t, _ in S]
vols = [(t, b) for t, b in S if t.startswith("卷")]
spine = [(t, b) for t, b in S if t.startswith("敬拜的次序")]

# ---- spine
check("spine: orientation chapter present", len(spine) == 1)
if spine:
    b = spine[0][1]
    check("spine: orientation chapter has 全書座標", "全書座標" in b)
    check("spine: orientation chapter closes with 你看見耶穌了嗎", "你看見耶穌了嗎" in b[-900:])
check("spine: six volumes", len(vols) == 6, f"found {len(vols)}")
for i, (t, b) in enumerate(vols, 1):
    head = b[:700]
    check(f"spine: {t[:6]} has 啟示的次序·第{i}步", re.search(rf"啟示的次序·第{'一二三四五六'[i-1]}步", head) is not None)
    check(f"spine: {t[:6]} has 全書座標", "全書座標" in head)
    check(f"spine: {t[:6]} closes with 你看見耶穌了嗎", "你看見耶穌了嗎" in b[-1500:])

# ---- items
psalm_blocks = re.split(r"(?m)^### 詩篇 (\d+)\n", text)
psalms = {int(psalm_blocks[i]): psalm_blocks[i + 1].split("\n### ")[0].split("\n## ")[0] for i in range(1, len(psalm_blocks) - 1, 2)}
bad = [n for n, b in psalms.items() if not re.search(r"\*\*看見耶穌\*\*（(新約引用|主題呼應|傳統)）", b)]
check("items: every psalm has a labelled 看見耶穌 line", not bad, f"missing/unlabelled: {bad}")
hymn_blocks = re.split(r"(?m)^### (\d+)\. (.+?)（.+）\n", text)
hymns = {int(hymn_blocks[i]): (hymn_blocks[i + 1], re.split(r"(?m)^#{1,3} ", hymn_blocks[i + 2])[0]) for i in range(1, len(hymn_blocks) - 2, 3)}
bad = [n for n, (_, b) in hymns.items() if not all(k in b for k in ("**配經**", "**默想**", "見於本庫", "**詞與年份**", "**出處註記**"))]
check("items: every hymn has 詞與年份 / 出處註記 / 配經 / 默想 / 見於本庫", not bad, f"incomplete: {bad}")
check("items: hymn numbers are 1..N without gaps", sorted(hymns) == list(range(1, len(hymns) + 1)))

# ---- coordinates of the groups inside 卷四 / 卷五, and a year (or an honest note) on every hymn credit
def h2_blocks(vol_prefix, skip):
    body = next(b for t_, b in vols if t_.startswith(vol_prefix))
    parts = re.split(r"(?m)^## (.+)$", body)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2) if not any(parts[i].startswith(k) for k in skip)]
bad = [t_ for t_, b in h2_blocks("卷四", ("詩篇禱讀四步",)) if "**座標**" not in b[:400]]
check("coords: every psalm group in 卷四 carries a 座標 line", not bad, str(bad))
bad = [t_ for t_, b in h2_blocks("卷五", ("現代讚美詩",)) if "**座標**" not in b[:400]]
check("coords: every hymn theme in 卷五 carries a 座標 line", not bad, str(bad))
bad = [n for n, (_, b) in hymns.items() if not (re.search(r"\*\*詞與年份\*\*：[^\n]*(?:\d{3,4}|［年份)", b))]
check("credits: every hymn credit shows a year or says why not", not bad, str(bad))

# ---- xref
bad = []
for n, ttl in re.findall(r"聖詩 (\d+)《([^》]+)》", text):
    if int(n) not in hymns or hymns[int(n)][0].strip() != ttl.strip():
        bad.append((n, ttl))
check("xref: every 聖詩 N《title》 matches its heading", not bad, str(bad[:4]))

# ---- counts
m = re.search(r"本書依主題挑選其中公有領域的 (\d+) 首", text)
check("counts: preface hymn count equals headings", bool(m) and int(m.group(1)) == len(hymns), f"{m.group(1) if m else None} vs {len(hymns)}")
m = re.search(r"(\d+) 篇完整和合本詩篇", text)
check("counts: how-to-use psalm count equals headings", bool(m) and int(m.group(1)) == len(psalms), f"{m.group(1) if m else None} vs {len(psalms)}")
idx = re.findall(r"(?m)^\| (\d+) \| (.+?) \| .+? \| \d+ \| (?:\d+|—) \|$", text)
idx = [(int(a), b) for a, b in idx if int(a) in hymns]
check("counts: appendix hymn index lists every hymn with the right title", len(idx) == len(hymns) and all(hymns[a][0].strip() == b.strip() for a, b in idx), f"{len(idx)} rows")

# ---- scripture (psalms vs cuv.json)
cuv = json.load(open(CUV, encoding="utf-8"))
cuv["psalms-46"]["4"] = cuv["psalms-46"]["4"].replace("這河的分使", "這河的分汊使")
norm = lambda s: re.sub(r"\s+", "", s)
bad = []
for n, b in psalms.items():
    first = re.search(r"(?m)^> \\textsuperscript\{1\}\{\}.*(?:\n>.*)*", b)
    if not first:
        bad.append(n); continue
    chinese = first.group(0)
    chinese = re.sub(r"\\textsuperscript\{\d+\}\{\}", "", chinese)
    chinese = chinese.replace(">", "")
    src = "".join(v for k, v in cuv[f"psalms-{n}"].items() if len(v.strip()) > 2 and "併入" not in v and "合和譯本" not in v)
    if norm(chinese).split("*（和合本")[0] != norm(src) and not norm(chinese).startswith(norm(src)[:40]):
        bad.append(n)
        continue
    if norm(src) not in norm(chinese):
        bad.append(n)
check("scripture: every psalm's Chinese block equals cuv.json", not bad, f"{bad}")

# ---- elder quotes
src_text = [re.sub(r"\s", "", p.read_text(encoding="utf-8")) for p in SOURCES.values() if p.exists()]
bad = []
lines = text.split("\n")
for i, l in enumerate(lines):
    if "老弟兄" not in l or "不是老弟兄說的" in l:
        continue
    scope = l
    for nxt in lines[i + 1:i + 5]:          # a quote block may follow after one blank line
        if nxt.startswith(">"):
            scope += "\n" + nxt
        elif nxt.strip():
            break
    for q in re.findall(r"「([^」]{8,})」", scope):
        for part in re.sub(r"\s", "", q).split("……"):
            if part and not any(part in s for s in src_text):
                bad.append(part[:30])
check("elder: every quotation on a line naming 老弟兄 occurs in the cited repo file", not bad, f"{bad}")
check("elder: appendix states which sayings are NOT 老弟兄's", "不是老弟兄說的" in text)

# ---- tables
L = text.split("\n")
bad = []
for i, l in enumerate(L):
    if re.match(r"\|[-: |]+\|\s*$", l) and i >= 1 and L[i - 1].startswith("|") and (i < 2 or not L[i - 2].startswith("|")):
        if i >= 2 and L[i - 2].strip() != "":          # header row must be preceded by a blank line
            bad.append(L[i - 1][:40])
check("tables: every table is preceded by a blank line (otherwise pandoc prints it as raw text)", not bad, str(bad[:3]))

# ---- external quotations (Appendix 七): every English quotation printed there must equal a text that
# .sources/verify_external_quotes.py has re-confirmed in every source page it lists
EV = ROOT / "books/bible/hymnWorship/.sources/external-quotes-verified.json"
if "## 附錄七" in text:
    app7 = text[text.index("## 附錄七"):]
    check("external: verification record exists", EV.exists())
    if EV.exists():
        ev = json.load(open(EV, encoding="utf-8"))
        norm_en = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
        recorded = {norm_en(v["text"]) for k, v in ev.items() if not k.startswith("_") and "text" in v}
        failed = [k for k, v in ev.items() if not k.startswith("_") and not v["ok"]]
        check("external: every source check in the record is OK", not failed, str(failed))
        printed = [l[2:] for l in app7.split("\n") if l.startswith("> ") and re.search(r"[A-Za-z]{4}", l)
                   and not re.search(r"[\u4e00-\u9fff]", l) and not l.startswith("> —")]
        bad = [q[:50] for q in printed if norm_en(q) not in recorded]
        check("external: every English quotation in 附錄七 equals a verified record text", bool(printed) and not bad, str(bad))
        # ...and every externally sourced quotation anywhere else in the book: a quote block whose citation line names
        # Erb / Wesley / Graham must equal a verified record text (the volumes reuse the appendix quotations)
        Lb = text.split("\n")
        used_ext, bad2 = 0, []
        for i, l in enumerate(Lb):
            if re.match(r"> — (Clayton Erb|John Wesley|Billy Graham|John MacArthur|Cliff Barrows|Ira D\. Sankey|C\. H\. Spurgeon|John Calvin|BGEA 官網 Cliff Barrows)", l):
                j = i - 1
                if Lb[j].strip() == ">":          # the empty quote line between the quotation and its citation
                    j -= 1
                block = []
                while j >= 0 and Lb[j].startswith(">") and Lb[j].strip() != ">":
                    block.insert(0, Lb[j][2:]); j -= 1
                used_ext += 1
                if norm_en(" ".join(block).rstrip("…")) not in recorded:
                    bad2.append(" ".join(block)[:50])
        check("external: every quotation attributed to Erb / Wesley / Graham / MacArthur / Barrows / Sankey / Spurgeon / Calvin, anywhere in the book, equals a verified record text", used_ext >= 23 and not bad2, f"{used_ext} found; bad: {bad2}")
    check("external: appendix says which material was NOT verified", "沒有找到、或不能核對的部分" in app7)

# ---- style
editor = "\n".join(l for l in text.split("\n") if "\\textsuperscript" not in l)   # only verbatim scripture lines are exempt; prayers in blockquotes are editor text
bad = [w for w in ("祢", "什麼", "上帝") if w in editor]
check("style: no 祢 / 什麼 / 上帝 in editor-written text", not bad, str(bad))
bad = [w for w in ("{H(", "{inline", "{len(", "{USED", "{FULL_N", "{NOFULL_N", "{FAIL_N", "{MISS_N") if w in text]
check("leaks: no unexpanded template markers", not bad, str(bad))
check("leaks: no placeholder verse text (a / 合和譯本併入上一節)", "合和譯本併入" not in text)

print()
print("ALL PASS" if not fails else f"{len(fails)} FAILED: {fails}")
sys.exit(1 if fails else 0)

#!/usr/bin/env python3
"""worship-page-index.py <pdf> — find the printed page of every heading of the Worship Book.

Reads books/bible/hymnWorship/.sources/headings.json (written by build_book.py), walks the PDF page by page
(pdftotext), and for each heading in document order finds the next page that has the heading as a line.
Printed page = PDF page - (PDF page of the first body page) + 1; the body starts at the 前言 heading.
Writes .sources/pages.json = {"sig", "n", "pages"}; the generator uses it only if its own heading signature
matches, so a stale file can never put wrong numbers in the index.  Exit 1 if a heading cannot be located."""
import hashlib, json, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "books/bible/hymnWorship/.sources"
pdf = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else str(ROOT / "output/hymnworship-consolidated.pdf")
H = json.load(open(SRC / "headings.json", encoding="utf-8"))
heads, n = [tuple(x) for x in H["headings"]], H["prefix_len"]
pages = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True, check=True).stdout.split("\f")
norm = lambda s: re.sub(r"[\s　]+", "", s)
plines = [[norm(l) for l in p.split("\n") if l.strip()] for p in pages]
# the body begins at the second page that has the 前言 heading as a line (the first is the table of contents)
first = norm(heads[0][1])
hits = [i for i, ls in enumerate(plines) if any(l.startswith(first[:8]) and "…" not in l and "." * 4 not in l for l in ls)]
if not hits:
    sys.exit("cannot find the first heading")
start = hits[0] if len(hits) == 1 else hits[1]
res, ptr, missing = [], start, []
for lv, tx in heads:
    full = norm(tx)
    key = full[:10]
    short = len(full) <= 10            # short headings (e.g. 詩篇 1) must equal a whole line: 詩篇1 is a prefix of 詩篇13
    found = None
    for pi in range(ptr, len(plines)):
        if any((l == full if short else l.startswith(key)) and "." * 4 not in l for l in plines[pi]):
            found = pi; break
    if found is None:
        missing.append(tx); res.append(res[-1] if res else 1); continue
    ptr = found; res.append(found - start + 1)
sig = hashlib.sha1("\n".join(f"{a}|{b}" for a, b in heads[:n]).encode()).hexdigest()
json.dump({"sig": sig, "n": n, "pages": res}, open(SRC / "pages.json", "w", encoding="utf-8"))
print(f"headings {len(heads)}  located {len(heads) - len(missing)}  missing {len(missing)}  body starts at pdf page {start + 1}")
for m in missing[:10]: print("  not found:", m)
if missing: sys.exit(1)

# ---- verify the printed index against the PDF: every psalm heading and hymn heading must really be on the page we claim
body = (ROOT / "output/hymnworship-body.md").read_text(encoding="utf-8")
bad = []
for lv, tx in heads[:n]:
    pass
pj = json.load(open(SRC / "pages.json", encoding="utf-8"))["pages"]
for i, (lv, tx) in enumerate(heads[:n]):
    if lv == 3 and (re.match(r"詩篇 \d+$", tx) or re.match(r"\d+\. ", tx)):
        pdfp = pj[i] + start - 1
        if not any(l == norm(tx) or l.startswith(norm(tx)[:10]) for l in plines[pdfp]):
            bad.append((tx, pj[i]))
dashes = 0
# the numbers actually printed in the index tables of the body that produced this PDF must equal the measured pages
head_page = {}
for i, (lv, tx) in enumerate(heads[:n]):
    if lv == 3: head_page.setdefault(tx, pj[i])
for num, grp, pgs in re.findall(r"(?m)^\| (\d+) \| (讚美與敬拜|認罪與悔改|患難、信靠與安息|感恩與盼望|聖言與彌賽亞) \| (\d+|—) \|$", body):
    if pgs == "—":
        dashes += 1
    elif pgs != str(head_page.get(f"詩篇 {num}")): bad.append((f"index psalm {num}", pgs, head_page.get(f"詩篇 {num}")))
hymn_page = {re.match(r"(\d+)\. ", tx).group(1): pj[i] for i, (lv, tx) in enumerate(heads[:n]) if lv == 3 and re.match(r"\d+\. ", tx)}
for num, ttl, pgs in re.findall(r"(?m)^\| (\d+) \| (.+?) \| .+? \| \d+ \| (\d+|—) \|$", body):
    if pgs == "—":
        dashes += 1
    elif num in hymn_page and pgs != str(hymn_page[num]): bad.append((f"index hymn {num}", pgs, hymn_page[num]))
if "--strict" in sys.argv and dashes:
    bad.append(("index still has — placeholders", dashes, 0))
print("index verification:", "OK" if not bad else f"{len(bad)} WRONG {bad[:5]}", f"(placeholders: {dashes})")
sys.exit(1 if bad else 0)

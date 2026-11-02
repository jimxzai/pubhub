#!/usr/bin/env python3
"""Second, independent witness for the NASB text: biblehub.com/nasb/<book>/<ch>.htm (page title 'NASB 1995').
Compares, verse by verse, the ai-eden text printed in the book against biblehub. Letters only (case, punctuation,
brackets ignored).  Classes: SAME, SITE-EXTRA (ai-eden has leading words biblehub does not, e.g. a psalm
superscription), BH-EXTRA, DIFF."""
import html, json, re, runpy, sys, time, urllib.request
from pathlib import Path
HERE = Path(__file__).parent; OUT = HERE / "biblehub"; OUT.mkdir(exist_ok=True)
sys.argv = ["x", "/dev/null"]
g = runpy.run_path(str(HERE.parent / "build_book.py"))
parse = g["parse"]; nasb_chapter = g["nasb_chapter"]
need = {}
for ref in set(g["USED"]) | {f"詩 {n}" for n in g["PSALM_SET"]}:
    code, ch, vs, _ = parse(ref); need.setdefault((g["BOOKS"][code], ch), set()).update(vs)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15"}
def page(book, ch):
    f = OUT / f"{book}-{ch}.html"
    if f.exists(): return f.read_text(encoding="utf-8", errors="ignore")
    for _ in range(3):
        try:
            h = urllib.request.urlopen(urllib.request.Request(f"https://biblehub.com/nasb/{book.replace('-', '_')}/{ch}.htm", headers=UA), timeout=40).read().decode("utf-8", "ignore")
            assert "NASB 1995" in h[:2000], "not NASB 1995 page"
            f.write_text(h, encoding="utf-8"); time.sleep(1); return h
        except Exception as e:
            print("retry", book, ch, e); time.sleep(3)
    return None
def verses(h):
    parts = re.split(r'<span class="reftext">.*?<b>(\d+)</b></a></span>', h, flags=re.S)
    out = {}
    for i in range(1, len(parts) - 1, 2):
        body = parts[i + 1]
        body = re.split(r"<p>\s*(?:<font|<span class=\"reftext\"|<b>|<i>)|<hr|<div", body)[0] if False else body
        body = re.sub(r"<br\s*/?>", " ", body); body = re.sub(r"<[^>]+>", "", body)
        t = html.unescape(body).replace("\x92", "'").replace("\x93", '"').replace("\x94", '"').replace("\xa0", " ")
        out[int(parts[i])] = t
    return out
norm = lambda s: re.sub(r"[^a-z]", "", s.lower())
res = {"SAME": 0, "SITE-EXTRA": 0, "BH-EXTRA": 0, "DIFF": 0}; bad = []; miss = []
for (book, ch), vs in sorted(need.items()):
    h = page(book, ch)
    if not h: miss.append((book, ch)); continue
    bh = verses(h); site = nasb_chapter(book, ch)
    for v in sorted(vs):
        a, b = norm(site[v]), norm(bh.get(v, ""))
        if not b: miss.append((book, ch, v)); continue
        if a == b: res["SAME"] += 1
        elif a.endswith(b): res["SITE-EXTRA"] += 1; bad.append(("SITE-EXTRA", book, ch, v, site[v][:90], bh[v][:90]))
        elif b.startswith(a): res["BH-EXTRA"] += 1; bad.append(("BH-EXTRA", book, ch, v, site[v][:90], bh[v][:90]))
        else: res["DIFF"] += 1; bad.append(("DIFF", book, ch, v, site[v], bh[v]))
print(res, "missing:", len(miss), miss[:5])
json.dump({"res": res, "bad": bad, "missing": miss}, open(HERE / "nasb-biblehub-diff.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for x in bad[:60]: print(x)

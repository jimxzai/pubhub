#!/usr/bin/env python3
"""Fetch every chapter the worship book cites from ai-eden.com's public API (one request per chapter, 1 s apart),
cache as aieden/<book>-<ch>.json, and diff the Chinese against ai-eden/data/cuv.json verse by verse."""
import json, re, runpy, sys, time, urllib.request
from pathlib import Path
HERE = Path(__file__).parent; OUT = HERE / "aieden"; OUT.mkdir(exist_ok=True)
sys.argv = ["x", "/dev/null"]
g = runpy.run_path(str(HERE.parent / "build_book.py"))
cuv = g["cuv"]; parse = g["parse"]
need = {}
for ref in set(g["USED"]) | {f"詩 {n}" for n in g["PSALM_SET"]}:
    code, ch, vs, _ = parse(ref)
    need.setdefault((g["BOOKS"][code], ch), set()).update(vs)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15"}
def fetch(book, ch):
    f = OUT / f"{book}-{ch}.json"
    if f.exists(): return json.load(open(f, encoding="utf-8"))
    for attempt in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(f"https://www.ai-eden.com/api/bible/{book}/{ch}", headers=UA), timeout=40)
            d = json.load(r); assert d.get("success"); f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8"); time.sleep(1); return d
        except Exception as e:
            print("retry", book, ch, e); time.sleep(3)
    return None
norm = lambda s: re.sub(r"\s+", "", s)
diffs, missing, n = [], [], 0
for (book, ch), vs in sorted(need.items()):
    d = fetch(book, ch)
    if not d: missing.append((book, ch)); continue
    by = {v["verse"]: v for v in d["data"]["verses"]}
    for v in sorted(vs):
        n += 1
        a = by.get(v)
        if a is None: missing.append((book, ch, v)); continue
        z, c = norm(a.get("textZh", "")), norm(cuv[f"{book}-{ch}"][str(v)])
        if z != c: diffs.append((book, ch, v, c, z))
print(f"chapters {len(need)}  verses compared {n}  CUV-differences {len(diffs)}  missing {len(missing)}")
json.dump({"diffs": diffs, "missing": missing}, open(HERE / "aieden-diff.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for x in diffs[:40]: print(x)

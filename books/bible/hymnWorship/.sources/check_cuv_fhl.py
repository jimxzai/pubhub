#!/usr/bin/env python3
"""Second witness for the 和合本 text: FHL (bible.fhl.net, version unv). One request per chapter, cached.
Classes per verse: SAME (exact, whitespace ignored) / PUNCT (equal once punctuation is removed) / CHAR (characters differ)."""
import json, re, runpy, sys, time, urllib.parse, urllib.request
from pathlib import Path
HERE = Path(__file__).parent; OUT = HERE / "fhl"; OUT.mkdir(exist_ok=True)
sys.argv = ["x", "/dev/null"]
g = runpy.run_path(str(HERE.parent / "build_book.py"))
parse, cuv = g["parse"], g["cuv"]
FHL = {"約壹": "約一"}
need = {}
for ref in set(g["USED"]) | {f"詩 {n}" for n in g["PSALM_SET"]}:
    code, ch, vs, _ = parse(ref); need.setdefault((code, ch), set()).update(vs)
def chap(code, ch):
    f = OUT / f"{code}-{ch}.json"
    if f.exists(): return json.load(open(f, encoding="utf-8"))
    u = "https://bible.fhl.net/json/qb.php?" + urllib.parse.urlencode({"chineses": FHL.get(code, code), "chap": ch, "sec": "1-180", "version": "unv", "gb": 0})
    for _ in range(3):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40))
            assert d["status"] == "success" and d["record_count"] > 0
            f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8"); time.sleep(1); return d
        except Exception as e:
            print("retry", code, ch, e); time.sleep(3)
punct = re.compile(r"[\s、，。；：！？「」『』（）．·—…─\-,.;:!?\"'()\[\]]")
cnt = {"SAME": 0, "PUNCT": 0, "CHAR": 0}; chars = []; miss = []
for (code, ch), vs in sorted(need.items()):
    d = chap(code, ch)
    if not d: miss.append((code, ch)); continue
    fh = {r["sec"]: r["bible_text"] for r in d["record"]}
    key = f"{g['BOOKS'][code]}-{ch}"
    for v in sorted(vs):
        a, b = cuv[key][str(v)], fh.get(v)
        if b is None: miss.append((code, ch, v)); continue
        if re.sub(r"\s", "", a) == re.sub(r"\s", "", b): cnt["SAME"] += 1
        elif punct.sub("", a) == punct.sub("", b): cnt["PUNCT"] += 1
        else:
            cnt["CHAR"] += 1
            sm = __import__("difflib").SequenceMatcher(None, punct.sub("", a), punct.sub("", b))
            ops = [(t, punct.sub("", a)[i1:i2], punct.sub("", b)[j1:j2]) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != "equal"]
            chars.append((code, ch, v, ops, a[:50]))
print(cnt, "missing", len(miss), miss[:5])
json.dump({"cnt": cnt, "char": chars, "missing": miss}, open(HERE / "cuv-fhl-diff.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(Counter((o[1], o[2]) for c in chars for o in c[3]).most_common(25))
for c in chars[:40]: print(c)

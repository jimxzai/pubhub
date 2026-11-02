#!/usr/bin/env python3
"""For each hymnal.net fetch, compare the repo's already-verified English stanzas against the fetched stanzas.
Writes hymns_hn/calibration.json: {key: {"ok": bool, "min_ratio": x, "detail": [...]}}"""
import difflib, json, re, sys
from pathlib import Path
sys.argv = ['x', '/dev/null']
HERE = Path(__file__).parent
g = {'__file__': str(HERE.parent / 'build_book.py')}
exec(compile(open(HERE.parent / 'build_book.py', encoding='utf-8').read().split('# ------------------------------------------------------------------ psalms')[0], 'bb', 'exec'), g)
n = lambda s: " ".join(re.sub(r"[^a-z' ]", " ", s.lower().replace("’", "'")).split())
def repo_stanzas(key):
    st, cur = [], []
    for l in g['best'][key][0].split("\n")[2:]:
        l = re.sub(r"^>\s?", "", l).rstrip(" \\").rstrip()
        if re.search(r"[一-鿿]", l): 
            if cur: st.append(" ".join(cur)); cur = []
            continue
        if not l.strip():
            if cur: st.append(" ".join(cur)); cur = []
        elif re.search(r"[A-Za-z]{3}", l): cur.append(l)
    if cur: st.append(" ".join(cur))
    # drop attribution line (starts with a name/year) : keep lines that look like lyrics => skip first stanza if it contains a year
    return [s for s in st if not re.search(r"\b1[5-9]\d\d\b|text from|tr\.|Army and Navy|trans", s)]
res = {}
for f in sorted((HERE / "hymns_hn").glob("*.json")):
    if f.name == "calibration.json": continue
    k = f.stem; d = json.load(open(f)); hn = [n(s["text"]) for s in d["stanzas"]]
    det = []
    for s in repo_stanzas(k):
        ns = n(s)
        if len(ns.split()) < 8: continue
        best = max((difflib.SequenceMatcher(None, ns, h).ratio() for h in hn), default=0)
        det.append(round(best, 3))
    res[k] = {"ok": bool(det) and min(det) >= 0.97, "min_ratio": min(det) if det else None, "detail": det, "n": len(d["stanzas"])}
    print(("OK  " if res[k]["ok"] else "FAIL"), k, res[k]["detail"])
json.dump(res, open(HERE / "hymns_hn" / "calibration.json", "w"), indent=1)
print(sum(r["ok"] for r in res.values()), "of", len(res))

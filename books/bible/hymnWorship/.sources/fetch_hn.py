#!/usr/bin/env python3
"""Fetch full hymn text from hymnal.net (hand-typed, structured by stanza) as a second witness.
A page is accepted only if its first stanza matches the repo's already-verified first English line.
Writes hymns_hn/<key>.json = {"url":..., "stanzas":[{"type":"verse|chorus","text":"..."}]}"""
import html, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
sys.argv = ['x', '/dev/null']
HERE = Path(__file__).parent; OUT = HERE / "hymns_hn"; OUT.mkdir(exist_ok=True)
g = {'__file__': str(HERE.parent / 'build_book.py')}
exec(compile(open(HERE.parent / 'build_book.py', encoding='utf-8').read().split('# ------------------------------------------------------------------ psalms')[0], 'bb', 'exec'), g)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15"}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode("utf-8", "ignore")
norm = lambda s: re.sub(r"[^a-z]", "", s.lower().replace("’", "").replace("'", "")).replace("thy", "your").replace("thee", "you")
def first_line(key):
    for l in g['best'][key][0].split("\n")[2:]:
        l = re.sub(r"^>\s*", "", l).rstrip(" \\")
        if l and re.search(r"[A-Za-z]{4}", l) and not re.search(r"[一-鿿]", l): return l
def parse(page):
    i = page.find('class="lyrics"'); body = page[i:]
    out = []
    for m in re.finditer(r'<div data-type="(\w+)" class="verse[^"]*">.*?<div class="text-container">(.*?)</div>', body, re.S):
        t = re.sub(r"<br\s*/?>", "\n", m.group(2)); t = html.unescape(re.sub(r"<[^>]+>", "", t)).replace("\xa0", " ")
        out.append({"type": m.group(1), "text": "\n".join(l.strip() for l in t.split("\n") if l.strip())})
    return out
for k, _, _ in g['ALL']:
    f = OUT / f"{k}.json"
    if f.exists(): continue
    fl = first_line(k); title = g['TITLE'][k]; done = None
    qs = [title, " ".join(re.sub(r"[^A-Za-z' ]", "", fl).split()[:4])]
    seen = []
    for q in qs:
        try: s = get("https://www.hymnal.net/en/search/all/all/" + urllib.parse.quote(q))
        except Exception as e: print("search err", k, e); continue
        for h in re.findall(r'href="(/en/hymn/[a-z]+/\d+[a-z0-9]*)"', s):
            if h in seen: continue
            seen.append(h)
            if len(seen) > 8: break
    for h in seen:
        try: p = get("https://www.hymnal.net" + h)
        except Exception: continue
        st = parse(p)
        if st and norm(fl)[:12] in norm(" ".join(x["text"] for x in st)):
            done = (h, st); break
        time.sleep(0.3)
    if done: f.write_text(json.dumps({"url": "https://www.hymnal.net" + done[0], "stanzas": done[1]}, ensure_ascii=False, indent=1)); print("OK  ", k, done[0], len(done[1]), "stanzas")
    else: print("MISS", k, "|", fl, "|", seen[:4])
    time.sleep(0.4)

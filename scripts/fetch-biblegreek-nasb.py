#!/usr/bin/env python3
"""Fetch NASB 1995 text (ai-eden.com API) for every reference listed in the Biblegreek scripture index and cache it in
docs/sources/biblegreek/nasb-index-cache.json, so the build itself needs no network. Run after the index's reference list changes."""
import json, os, re, urllib.request, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, "books/bible/Biblegreek/96-appendix-5-scripture-index.md")
OUT = os.path.join(ROOT, "docs/sources/biblegreek/nasb-index-cache.json")
SLUG = {"創": "genesis", "出": "exodus", "利": "leviticus", "申": "deuteronomy", "耶": "jeremiah", "太": "matthew", "可": "mark", "路": "luke",
        "約": "john", "徒": "acts", "羅": "romans", "林後": "2-corinthians", "加": "galatians", "帖前": "1-thessalonians", "彼前": "1-peter", "約壹": "1-john", "啟": "revelation", "詩": "psalms", "賽": "isaiah", "林前": "1-corinthians", "帖後": "2-thessalonians", "彼後": "2-peter"}
cache = {}
chap = {}
for line in open(IDX, encoding="utf-8"):
    m = re.match(r"\| (\S+) (\d+):(\d+)(?:-(\d+))? \|", line)
    if not m: continue
    z, c, v1, v2 = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4) or m.group(3))
    key = f"{z} {c}:{v1}" + (f"-{v2}" if v2 != v1 else "")
    k = (SLUG[z], c)
    if k not in chap:
        req = urllib.request.Request(f"https://www.ai-eden.com/api/bible/{k[0]}/{k[1]}?t=NASB1995", headers={"User-Agent": "Mozilla/5.0"})
        chap[k] = {v["verse"]: v["text"] for v in json.load(urllib.request.urlopen(req))["data"]["verses"]}
    cache[key] = [chap[k][v] for v in range(v1, v2 + 1) if v in chap[k]]
json.dump(cache, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(cache), "refs cached;", sum(1 for v in cache.values() if not v), "empty")

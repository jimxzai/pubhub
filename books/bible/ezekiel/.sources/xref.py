#!/usr/bin/env python3
"""Cached ai-eden verse lookup for cross-references (CUV + NASB).

  python3 xref.py john 8:24-28        -> verses 24-28 of John 8
  python3 xref.py revelation 21       -> whole chapter
  python3 xref.py ezekiel 36:26       -> one verse
Book = ai-eden slug (john, revelation, jeremiah, 1-corinthians, hebrews, matthew,
isaiah, daniel, psalms? -> check the spelling with a chapter-level call).
Chapters are cached in xref-cache/ so every verse any chapter cites comes from the
same fetched text. Throttled: 2 s between network hits; retries with back-off.
Output columns: ref | 和合本 (CUV) | NASB.  Quote ONLY what this prints.
"""
import json, sys, time, urllib.request, pathlib, re
CACHE = pathlib.Path(__file__).resolve().parent / "xref-cache"
CACHE.mkdir(exist_ok=True)

def chapter(book, ch):
    f = CACHE / f"{book}-{ch}.json"
    if not f.exists():
        for a in range(6):
            try:
                req = urllib.request.Request(f"https://www.ai-eden.com/api/bible/{book}/{ch}?t=CUV,NASB",
                                             headers={"User-Agent": "Mozilla/5.0"})
                d = urllib.request.urlopen(req, timeout=30).read()
                j = json.loads(d)
                if j.get("success"):
                    f.write_bytes(d); time.sleep(2); break
                sys.exit(f"ai-eden: {book} {ch}: {j.get('error')}")
            except Exception as e:
                time.sleep(4 * (a + 1))
        else:
            sys.exit(f"ai-eden: giving up on {book} {ch}")
    return {v["verse"]: (v["textZh"], v["text"]) for v in json.load(open(f))["data"]["verses"]}

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(__doc__)
    book, ref = sys.argv[1], sys.argv[2]
    m = re.fullmatch(r"(\d+)(?::(\d+)(?:-(\d+))?)?", ref)
    if not m: sys.exit("ref must be N or N:v or N:v1-v2")
    ch, a, b = int(m[1]), m[2], m[3]
    vs = chapter(book, ch)
    lo = int(a) if a else min(vs); hi = int(b) if b else (int(a) if a else max(vs))
    for v in range(lo, hi + 1):
        if v in vs: print(f"{book} {ch}:{v} | {vs[v][0]} | {vs[v][1]}")
        else: print(f"{book} {ch}:{v} | (no such verse in ai-eden)")

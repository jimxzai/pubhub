#!/usr/bin/env python3
"""Print 和合本 (bible.fhl.net unv) for refs like '羅 10:15' '詩 2:1-4'; cache under scripture/xref/."""
import sys, json, urllib.request, urllib.parse, time, re
from pathlib import Path
C = Path(__file__).resolve().parent / "scripture" / "xref"; C.mkdir(exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124"}
for ref in sys.argv[1:]:
    book, cv = ref.split()
    ch, sec = (cv.split(":") + ["1-999"])[:2] if ":" in cv else (cv, "1-999")
    f = C / f"{book}{ch}_{sec}.json".replace(":", "_")
    if not f.exists():
        url = f"https://bible.fhl.net/json/qb.php?chineses={urllib.parse.quote(book)}&chap={ch}&sec={sec}&gb=0"
        f.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read()); time.sleep(0.6)
    d = json.loads(f.read_text(encoding="utf-8"))
    print(f"[{ref}]", " ".join(f"{r['sec']}{r['bible_text']}" for r in d["record"]).replace("裡", "裏"))

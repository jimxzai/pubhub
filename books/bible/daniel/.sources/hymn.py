#!/usr/bin/env python3
"""hymn.py "Take My Life, and Let It Be"      -> print the hymn text from Wikisource (Army and Navy Hymnal 1920, PD)
hymn.py --search "Lo! He comes with clouds"  -> list Wikisource page titles that match (any hymnal), to pick an exact page
hymn.py --page "Some Hymnal/Hymns/Title"      -> print an exact Wikisource page
Text is cached in .sources/hymns/. The first lines after the title block give author/year as printed."""
import html, json, re, sys, urllib.parse, urllib.request
from pathlib import Path
UA = {"User-Agent": "pubhub-research/1.0 (sales@xwire.ai)"}
OUT = Path(__file__).parent / "hymns"; OUT.mkdir(exist_ok=True)
def api(**kw):
    url = "https://en.wikisource.org/w/api.php?" + urllib.parse.urlencode(dict(format="json", **kw))
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))
def show(title):
    d = api(action="parse", page=title, prop="text", redirects=1)
    h = d["parse"]["text"]["*"]
    h = re.sub(r"<style.*?</style>", "", h, flags=re.S)
    h = re.sub(r"<br\s*/?>", "\n", h); h = re.sub(r"</(p|div|tr|li)>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", "", h))
    t = "\n".join(l for l in t.split("\n") if not l.startswith(".mw-") and "{" not in l[:3])
    t = re.sub(r"\n\s*\n+", "\n\n", t).strip()
    (OUT / (re.sub(r"[^A-Za-z0-9]+", "-", title)[:80] + ".txt")).write_text(f'SOURCE: Wikisource, "{title}"\n\n{t}\n')
    print(f'SOURCE: Wikisource, "{title}"\n\n{t}')
a = sys.argv[1:]
if not a: sys.exit(__doc__)
if a[0] == "--search":
    for r in api(action="query", list="search", srsearch=a[1], srlimit=12)["query"]["search"]: print(r["title"])
elif a[0] == "--page": show(a[1])
else:
    try: show("The Army and Navy Hymnal/Hymns/" + a[0])
    except Exception as e: print("not in Army and Navy Hymnal:", e, "\ntry --search")

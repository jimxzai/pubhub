#!/usr/bin/env python3
"""Re-fetch every external source behind Appendix 七 and confirm that each English quotation (EXT) occurs in EVERY url
listed for it, and that each factual needle (EXT_FACTS) occurs in its page.  Letters-only comparison (case, punctuation,
curly quotes, hyphenation ignored).  Writes external-quotes-verified.json; exit 1 on any failure.
Pages that refuse automated fetching are reported as UNREACHABLE (not as OK)."""
import datetime, html, json, re, runpy, subprocess, sys, tempfile, urllib.request
from pathlib import Path
HERE = Path(__file__).parent
sys.argv = ["x", "/dev/null"]
g = runpy.run_path(str(HERE.parent / "build_book.py"))
EXT, FACTS = g["EXT"], g["EXT_FACTS"]
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15"}
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
cache = {}
def page(url):
    if url in cache: return cache[url]
    raw = None
    for _ in range(3):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=150).read(); break
        except Exception as e:
            err = e
    if raw is None:
        cache[url] = None; return None
    if url.lower().endswith(".pdf"):
        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(raw); f.flush()
            txt = subprocess.run(["pdftotext", f.name, "-"], capture_output=True, text=True).stdout
    elif url.lower().endswith(".txt"):
        txt = raw.decode("utf-8", "ignore")          # plain-text OCR: do not strip "tags" (OCR may contain < and >)
    else:
        h = raw.decode("utf-8", "ignore")
        h = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", h)
        txt = html.unescape(re.sub(r"<[^>]+>", " ", h)).replace("\xa0", " ")
    cache[url] = norm(txt); return cache[url]
res, bad = {}, []
for k, (text, label, urls) in EXT.items():
    per = {}
    for u in urls:
        p = page(u)
        per[u] = "UNREACHABLE" if p is None else ("OK" if norm(text) in p else "MISSING")
    ok = all(v == "OK" for v in per.values())
    res[k] = {"text": text, "ok": ok, "urls": per}
    if not ok: bad.append((k, per))
for k, (needles, u) in FACTS.items():
    p = page(u); per = {n: ("UNREACHABLE" if p is None else ("OK" if norm(n) in p else "MISSING")) for n in needles}
    ok = all(v == "OK" for v in per.values()); res["fact:" + k] = {"ok": ok, "url": u, "needles": per}
    if not ok: bad.append((k, per))
res["_retrieved"] = datetime.date.today().isoformat()
json.dump(res, open(HERE / "external-quotes-verified.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in res.items():
    if k != "_retrieved": print(("OK   " if v["ok"] else "FAIL ") + k)
print("ALL OK" if not bad else f"{len(bad)} FAILED: {bad}")
sys.exit(1 if bad else 0)

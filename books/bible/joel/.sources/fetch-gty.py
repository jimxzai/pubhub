#!/usr/bin/env python3
"""fetch-gty.py CODE [CODE ...]  — fetch MacArthur sermons from gty.org into commentary/gty/CODE.txt
(transcript only, for reading) and sermon-cache/gty-CODE.txt (full page text, for verify-sermon-quotes.py).
MacArthur preached no verse-by-verse Joel series; these are the sermons that treat Joel's texts or cite Joel
(Acts 2, the Day of the LORD, Revelation 9 locusts, Matthew 24, repentance). Slugs come from gty.org/sitemap.xml."""
import html, re, subprocess, sys, time
from pathlib import Path
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15"
here = Path(__file__).parent
out = here / "commentary" / "gty"; out.mkdir(parents=True, exist_ok=True)
cache = here / "sermon-cache"; cache.mkdir(exist_ok=True)
sm = Path(sys.argv[0]).resolve().parent.joinpath("gty-sitemap-locs.txt").read_text().split()
slug = {}
for u in sm:
    m = re.match(r"https://www\.gty\.org/sermons/([0-9A-Za-z-]+)/([a-z0-9-]+)$", u)
    if m: slug[m.group(1)] = m.group(2)
for code in sys.argv[1:]:
    f = out / f"{code}.txt"
    if f.exists() and f.stat().st_size > 5000: continue
    if code not in slug: print("no slug for", code); continue
    raw = subprocess.run(["curl", "-sL", "-m", "90", "-A", UA, f"https://www.gty.org/sermons/{code}/{slug[code]}"], capture_output=True, text=True).stdout
    full = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    full = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", full)))
    (cache / f"gty-{code}.txt").write_text(full, encoding="utf-8")
    m = re.search(r'expand--content[^>]*>(.*?)</div>', raw, flags=re.S)
    body = html.unescape(re.sub(r"<[^>]+>", "\n", m.group(1))) if m else full
    body = re.sub(r"\n\s*\n+", "\n\n", body).strip()
    f.write_text(f"# gty.org sermon {code} — {slug[code]}\n# https://www.gty.org/sermons/{code}/{slug[code]}\n\n{body}\n", encoding="utf-8")
    print(code, slug[code], len(body), "Joel x%d" % len(re.findall(r"\bJoel\b", body))); time.sleep(2)

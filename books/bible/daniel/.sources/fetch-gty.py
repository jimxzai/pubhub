#!/usr/bin/env python3
"""Fetch MacArthur's Daniel series (gty.org 27-01..27-31): full-page text for the verifier cache, transcript text for reading."""
import html, re, subprocess, sys, time
from pathlib import Path
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15"
out = Path(__file__).parent / "commentary" / "gty"; out.mkdir(parents=True, exist_ok=True)
cache = Path("/tmp/sermon-cache"); cache.mkdir(exist_ok=True)
sm = Path("/Users/jimxiao/dev/pubhub/books/bible/nehemiah/sources/commentary/gty-sitemap.xml").read_text()
urls = sorted(set(re.findall(r"https://www\.gty\.org/sermons/(27-\d\d)/([a-z0-9-]+)", sm)))
for code, slug in urls:
    f = out / f"{code}.txt"
    if f.exists() and f.stat().st_size > 5000: continue
    raw = subprocess.run(["curl", "-sL", "-m", "90", "-A", UA, f"https://www.gty.org/sermons/{code}/{slug}"], capture_output=True, text=True).stdout
    full = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    full = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", full)))
    (cache / f"gty-{code}.txt").write_text(full, encoding="utf-8")
    m = re.search(r'expand--content[^>]*>(.*?)</div>', raw, flags=re.S)
    body = html.unescape(re.sub(r"<[^>]+>", "\n", m.group(1))) if m else full
    body = re.sub(r"\n\s*\n+", "\n\n", body).strip()
    f.write_text(f"# gty.org sermon {code} — {slug}\n# https://www.gty.org/sermons/{code}/{slug}\n\n{body}\n", encoding="utf-8")
    print(code, slug, len(body)); time.sleep(2)

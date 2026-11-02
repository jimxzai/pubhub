#!/usr/bin/env python3
"""Collect every verse 《讀懂聖經的希伯來文》 quotes and store CUV + NASB 1995 for it in
docs/sources/biblehebrew/scripture-excerpts.json.

What is "quoted": the blockquote lines ending ——<書> N:N（和合本…） in the chapters, and the song-card verses
(SONGS in gen-biblehebrew-data.py). NASB is fetched from TWO independent sources and compared:
  1. biblehub.com chapter pages (https://biblehub.com/nasb/<book>/<ch>.htm), the stored text
  2. the live ai-eden.com pages (https://ai-eden.com/bible/<book>/<ch>)
A disagreement (after normalising quote marks and a psalm superscription) is printed and the verse is NOT stored.
CUV comes from ai-eden's data/cuv.json (AI_EDEN_DIR, default ../ai-eden).   Usage: fetch-nasb-excerpts.py [--dry]
"""
import glob, html, json, os, re, sys, time, unicodedata, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_DIR = os.path.join(ROOT, "books/bible/Biblehebrew")
XJ = os.path.join(ROOT, "docs/sources/biblehebrew/scripture-excerpts.json")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"
ZH = {"創": "genesis", "出": "exodus", "申": "deuteronomy", "詩": "psalms", "賽": "isaiah", "結": "ezekiel", "珥": "joel",
      "摩": "amos", "彌": "micah", "該": "haggai", "太": "matthew", "路": "luke", "約": "john", "來": "hebrews"}
OSIS = {"Deut": "deuteronomy", "Ps": "psalms", "Isa": "isaiah", "Gen": "genesis"}


def wanted():
    need = {}
    for f in sorted(glob.glob(os.path.join(BOOK_DIR, "[0-9]*.md")) + glob.glob(os.path.join(BOOK_DIR, "p2-*.md"))):
        for l in open(f, encoding="utf-8"):
            m = re.match(r"^> (.+?)——([^（]+?)（和合本[^）]*）\s*$", l.strip())
            if not m: continue
            r = re.match(r"(\S+?)\s*(\d+):(\d+)(?:-(\d+))?$", m.group(2).strip())
            if r and r.group(1) in ZH:
                need.setdefault((ZH[r.group(1)], int(r.group(2))), set()).update(range(int(r.group(3)), int(r.group(4) or r.group(3)) + 1))
    spec = __import__("importlib.util").util.spec_from_file_location("g", os.path.join(ROOT, "scripts/gen-biblehebrew-data.py"))
    g = __import__("importlib.util").util.module_from_spec(spec); spec.loader.exec_module(g)
    for sg in g.SONGS.values():
        osis, ch, v = sg["ref"].split(".")
        need.setdefault((OSIS[osis], int(ch)), set()).add(int(v))
    return need


def get(url):
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(r, timeout=40).read().decode("utf-8", "replace")


def biblehub(book, ch):
    body = get(f"https://biblehub.com/nasb/{book}/{ch}.htm")
    body = body[body.find('<div class="chap">'):].split("</div>")[0]
    body = re.sub(r'<font color="#000000"><b><i>.*?</i></b></font>', "", body, flags=re.S)
    parts = re.split(r'<span class="reftext"><a [^>]*><b>(\d+)</b></a></span>', body)
    out = {}
    for i in range(1, len(parts), 2):
        t = re.sub(r"<br\s*/?>", " ", parts[i + 1]); t = re.sub(r"<[^>]+>", "", t)
        out[int(parts[i])] = re.sub(r"\s+", " ", html.unescape(t).replace("\xa0", " ")).strip()
    return out


def aieden(book, ch):
    t = get(f"https://ai-eden.com/bible/{book}/{ch}")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
    out = {}
    for m in re.finditer(r"NASB (\d+) (.*?) CUV \1 (.*?)(?= NASB \d+ |$)", t):
        out[int(m.group(1))] = m.group(2).strip()
    return out


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("[", "").replace("]", "")           # ai-eden prints NASB italics (supplied words) in brackets
    return re.sub(r"[\s'\".,;:!?—-]+", "", s).lower()


def main():
    need = wanted()
    cuv = json.load(open(os.path.join(os.environ.get("AI_EDEN_DIR", os.path.join(os.path.dirname(ROOT), "ai-eden")), "data/cuv.json"), encoding="utf-8"))
    store = json.load(open(XJ, encoding="utf-8"))
    agree = disagree = 0
    for (book, ch), vs in need.items():
        bh = biblehub(book, ch); time.sleep(1.2)
        ae = aieden(book, ch); time.sleep(1.2)
        for v in sorted(vs):
            key = f"{book}.{ch}.{v}"
            a, b = bh.get(v), ae.get(v)
            if not a or not b: print("MISSING", key, "biblehub" if not a else "", "ai-eden" if not b else ""); disagree += 1; continue
            # the live page may print a psalm superscription inside verse 1 and, for the last verse, the page footer:
            # require the biblehub text (no title) to be the START of what follows any title in the ai-eden text
            if norm(a) in norm(b) and (norm(b).startswith(norm(a)) or norm(b).endswith(norm(a)) or norm(a) in norm(b)[:len(norm(a)) + 60]):
                agree += 1
                store[key] = {"cuv": cuv[f"{book}-{ch}"][str(v)], "nasb1995": a}
            else:
                disagree += 1; print("DISAGREE", key, "\n  biblehub:", a, "\n  ai-eden :", b[:200])
    if "--dry" not in sys.argv:
        json.dump(dict(sorted(store.items())), open(XJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{agree} verses agree across both sources, {disagree} problems; {len(store)} verses stored")


if __name__ == "__main__":
    main()

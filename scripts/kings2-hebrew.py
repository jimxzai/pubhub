#!/usr/bin/env python3
"""Print the Hebrew text (vowels kept, cantillation stripped) of 2 Kings verses.

    python3 scripts/kings2-hebrew.py 1:2 1:10-12 5:14 [--root yarad-regex]

Source: Sefaria API (Miqra according to the Masorah), cached in
$KINGS2_HEBREW_CACHE (default /tmp/kings2-hebrew-cache). Verse numbering is the
HEBREW numbering, which differs from the 和合本 at a few places (e.g. 12:4 in
Hebrew = 12:3 in 和合本; 11:21 ↔ 12:1 etc.) — check before quoting a Hebrew word
against a Chinese verse number.

    --find 'REGEX'   also search the whole book's CONSONANTAL text (niqqud,
                     cantillation and maqqef stripped) and list matching verses —
                     the way the 話與黏附 counts (לא סר, כדבר, דבק …) were made.
"""
import json, os, pathlib, re, sys, time, unicodedata, urllib.request

CACHE = pathlib.Path(os.environ.get("KINGS2_HEBREW_CACHE", "/tmp/kings2-hebrew-cache"))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15", "Accept": "application/json"}


def chapter(c):
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"{c:02d}.json"
    if not f.exists():
        for i in range(4):
            try:
                d = json.loads(urllib.request.urlopen(urllib.request.Request(
                    f"https://www.sefaria.org/api/v3/texts/II_Kings.{c}?version=hebrew", headers=UA), timeout=40).read())
                f.write_text(json.dumps(d["versions"][0]["text"], ensure_ascii=False), encoding="utf8")
                break
            except Exception:
                time.sleep(2 * (i + 1))
        else:
            raise SystemExit("fetch failed for chapter %d" % c)
        time.sleep(0.4)
    return json.loads(f.read_text(encoding="utf8"))


def clean(t, consonantal=False):
    t = re.sub(r"<[^>]+>", "", t).replace("&nbsp;", " ").replace("&thinsp;", "")
    t = re.sub(r"\{.\}", "", t)
    if consonantal:
        t = t.replace("־", " ")
        t = "".join(ch for ch in unicodedata.normalize("NFD", t) if not unicodedata.combining(ch))
    else:
        t = re.sub(r"[֑-ֽ֯׀]", "", t).replace("־", "־")
    return re.sub(r"\s+", " ", t).strip()


def main(argv):
    if "--find" in argv:
        pat = re.compile(argv[argv.index("--find") + 1])
        hits = []
        for c in range(1, 26):
            for i, v in enumerate(chapter(c), 1):
                if pat.search(clean(v, True)):
                    hits.append(f"{c}:{i}")
        print(len(hits), " ".join(hits))
        return
    for ref in [a for a in argv if re.match(r"^\d+:\d+(-\d+)?$", a)]:
        c, rest = ref.split(":")
        a, _, b = rest.partition("-")
        verses = chapter(int(c))
        for v in range(int(a), int(b or a) + 1):
            print(f"{c}:{v}  {clean(verses[v - 1])}")


if __name__ == "__main__":
    main(sys.argv[1:])

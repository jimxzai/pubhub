#!/usr/bin/env python3
"""xref.py "太 24:15-16" ["羅 8:1" ...] [--nasb]

Verbatim Scripture for cross-references OUTSIDE Daniel, so no author-agent ever
types a verse. CUV: bible.fhl.net 'unv' (carries punctuation) with the same
modernisation fixes gen-daniel-scripture.py applies (牠/她→他, 嗎→麼, 裡→裏 ...).
--nasb: biblehub /nasb/ (NASB 1995). Chapters are cached in .sources/xref-cache/.

Ref grammar:  <書> <章>:<節>[-<節>]   e.g. 太 24:15-16 | 啟 7:13 | 林前 6:2 | 約 5:28-29
Books use the standard 和合本 abbreviations (創出利民申書士得撒上撒下王上王下代上代下拉尼斯伯
詩箴傳歌賽耶哀結但何珥摩俄拿彌鴻哈番該亞瑪 太可路約徒羅林前林後加弗腓西帖前帖後提前提後多門來雅彼前彼後
約一約二約三猶啟).
Output: one line per verse:  <ref>\t<text>.  Characters are fhl's after fixes; they are NOT
re-checked against ai-eden, so run scripts/lint-scripture-text.py on anything you quote.
"""
import html, json, re, subprocess, sys
from pathlib import Path
from urllib.parse import quote

CACHE = Path(__file__).parent / "xref-cache"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15"

BH = {  # abbreviation -> biblehub slug
    "創": "genesis", "出": "exodus", "利": "leviticus", "民": "numbers", "申": "deuteronomy", "書": "joshua",
    "士": "judges", "得": "ruth", "撒上": "1_samuel", "撒下": "2_samuel", "王上": "1_kings", "王下": "2_kings",
    "代上": "1_chronicles", "代下": "2_chronicles", "拉": "ezra", "尼": "nehemiah", "斯": "esther", "伯": "job",
    "詩": "psalms", "箴": "proverbs", "傳": "ecclesiastes", "歌": "songs", "賽": "isaiah", "耶": "jeremiah",
    "哀": "lamentations", "結": "ezekiel", "但": "daniel", "何": "hosea", "珥": "joel", "摩": "amos",
    "俄": "obadiah", "拿": "jonah", "彌": "micah", "鴻": "nahum", "哈": "habakkuk", "番": "zephaniah",
    "該": "haggai", "亞": "zechariah", "瑪": "malachi", "太": "matthew", "可": "mark", "路": "luke",
    "約": "john", "徒": "acts", "羅": "romans", "林前": "1_corinthians", "林後": "2_corinthians",
    "加": "galatians", "弗": "ephesians", "腓": "philippians", "西": "colossians", "帖前": "1_thessalonians",
    "帖後": "2_thessalonians", "提前": "1_timothy", "提後": "2_timothy", "多": "titus", "門": "philemon",
    "來": "hebrews", "雅": "james", "彼前": "1_peter", "彼後": "2_peter", "約一": "1_john", "約二": "2_john",
    "約三": "3_john", "猶": "jude", "啟": "revelation",
}
FIXES = [("牠", "他"), ("她", "他"), ("嗎", "麼"), ("祕", "秘"), ("毘", "毗"), ("焰", "燄"), ("裡", "裏")]


def run(url):
    return subprocess.run(["curl", "-sL", "-m", "40", "-A", UA, url], capture_output=True, text=True).stdout


def cuv_chapter(book, ch):
    f = CACHE / f"cuv-{book}-{ch}.json"
    if not f.exists():
        raw = run(f"https://bible.fhl.net/json/qb.php?chineses={quote(book)}&chap={ch}&version=unv&gb=0")
        json.loads(raw)  # fail loudly on garbage
        CACHE.mkdir(exist_ok=True)
        f.write_text(raw, encoding="utf-8")
    out = {}
    for r in json.loads(f.read_text(encoding="utf-8"))["record"]:
        t = r["bible_text"].replace("•", "‧")
        for a, b in FIXES:
            t = t.replace(a, b)
        out[r["sec"]] = t.strip()
    return out


def nasb_chapter(book, ch):
    f = CACHE / f"nasb-{book}-{ch}.htm"
    if not f.exists():
        CACHE.mkdir(exist_ok=True)
        f.write_text(run(f"https://biblehub.com/nasb/{BH[book]}/{ch}.htm"), encoding="utf-8")
    t = f.read_text(encoding="utf-8", errors="ignore")
    a = t.find('<div class="chap">')
    seg = t[a:t.find("</div>", a)]
    seg = re.sub(r'L<font size="1">ORD</font>', "LORD", seg)
    seg = re.sub(r'<font size="1">([^<]*)</font>', r"\1", seg)
    parts = re.split(r'<span class="reftext"><a [^>]*><b>(\d+)</b></a></span>', seg)
    out = {}
    for i in range(1, len(parts), 2):
        b = parts[i + 1]
        b = re.sub(r"<i>(.*?)</i>", r"*\1*", b, flags=re.S)
        b = re.sub(r"<br\s*/?>|<p>", " ", b)
        b = html.unescape(re.sub(r"<[^>]+>", "", b)).replace("\xa0", " ")
        b = re.sub(r"[‘’]", "'", b)
        b = re.sub(r"[“”]", '"', b)
        b = re.sub(r"\s+", " ", b).strip()
        b = re.sub(r'(?<=[.:;,!?"—\'])\s*\*[A-Z][^*]*\*\s*$', "", b)
        b = re.sub(r"(?<=\*)\s*\*[A-Z][A-Za-z ,']*[a-z]\*\s*$", "", b)
        out[int(parts[i])] = b
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    nasb = "--nasb" in sys.argv
    if not args:
        sys.exit(__doc__)
    for ref in args:
        m = re.match(r"^\s*(\S+?)\s*(\d+):(\d+)(?:[-–](\d+))?\s*$", ref)
        if not m or m.group(1) not in BH:
            print(f"!! cannot parse {ref!r}", file=sys.stderr)
            continue
        book, ch, v1 = m.group(1), int(m.group(2)), int(m.group(3))
        v2 = int(m.group(4) or v1)
        verses = (nasb_chapter if nasb else cuv_chapter)(book, ch)
        for v in range(v1, v2 + 1):
            print(f"{book} {ch}:{v}\t{verses.get(v, '!! MISSING')}")


if __name__ == "__main__":
    main()

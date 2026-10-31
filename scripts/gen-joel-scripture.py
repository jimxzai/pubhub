#!/usr/bin/env python3
"""Generate each Joel chapter's `## 經文` block (CUV + NASB 1995) from fetched sources.

Same design as gen-daniel-scripture.py: no author-agent ever types Scripture. Every
chapter pastes the block this script prints, and `--check` re-derives it and diffs
against the chapter file. Joel's verse numbering is the ENGLISH one (3 chapters,
73 verses; Hebrew 2:28-32 = English 2:28-32 -> MT 3:1-5, MT 4 = English 3).

SOURCES (books/bible/joel/.sources/)
  cuv/fhl-unv-NN.json      bible.fhl.net 'unv'  - punctuation, 「」, 　神 spacing
  cuv/aieden-NN.json       ai-eden.com API      - project-standard characters/names
  cnbible/N.htm            cnbible.com CUVT     - third source (characters only)
  nasb/biblehub-NN.htm     biblehub.com/nasb/   - NASB 1995 (italics = supplied words)

CUV rule: fhl text as the base (it carries punctuation), with the character/name
choices where fhl modernises and ai-eden + cnbible keep the 1919 form (CUV_FIXES, and
the two verse-scoped fixes in VERSE_FIXES: 嗎/麼 is NOT one global rule in 和合本).
`--check` also proves the generated CUV equals ai-eden AND cnbible on every verse
once punctuation and 「」 are stripped (73/73 or it fails).

USAGE
  python3 scripts/gen-joel-scripture.py            # write .sources/units/NN.scripture.md + scripture-all.tsv
  python3 scripts/gen-joel-scripture.py --check    # diff each chapter's 經文 block + CUV source agreement
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "joel"
SRC = BOOK / ".sources"

# unit file stem -> (reference line, chapter, first verse, last verse, paragraph-start verses)
UNITS = {
    "01-the-word-came": ("約珥書 1:1-4", 1, 1, 4, [1, 2]),
    "02-the-land-mourns": ("約珥書 1:5-12", 1, 5, 12, [5, 8, 11]),
    "03-consecrate-a-fast": ("約珥書 1:13-20", 1, 13, 20, [13, 15, 19]),
    "04-blow-the-trumpet-in-zion": ("約珥書 2:1-11", 2, 1, 11, [1, 3, 7, 10]),
    "05-rend-your-heart": ("約珥書 2:12-17", 2, 12, 17, [12, 15]),
    "06-then-the-lord-was-jealous": ("約珥書 2:18-27", 2, 18, 27, [18, 21, 23, 25]),
    "07-afterward-i-will-pour-out": ("約珥書 2:28-32", 2, 28, 32, [28, 30]),
    "08-the-valley-of-jehoshaphat": ("約珥書 3:1-8", 3, 1, 8, [1, 4]),
    "09-the-valley-of-decision": ("約珥書 3:9-16", 3, 9, 16, [9, 13]),
    "10-the-lord-dwells-in-zion": ("約珥書 3:17-21", 3, 17, 21, [17, 18]),
}

# fhl 'unv' modernises these; ai-eden and cnbible (CUVT) keep the 1919 form.
CUV_FIXES = [("牠", "他"), ("毘", "毗"), ("泰爾", "推羅"), ("希臘人", "希利尼人"),
             ("裡", "裏"), ("　", ""), ("吧！", "罷！"), ("原文是事", "原文作事")]
# 嗎 vs 麼 is verse by verse in 和合本 (1:16 keeps 嗎; 1:2 and 3:4 print 麼); 2:26 prints 不至.
# 火焰/火燄 is verse by verse too: 1:19 prints 火焰; 2:3 and 2:5 print 火燄.
VERSE_FIXES = {
    (1, 2): [("嗎", "麼")],
    (2, 3): [("焰", "燄")],
    (2, 5): [("焰", "燄")],
    (3, 4): [("嗎", "麼")],
    (2, 26): [("不致", "不至")],
}


def cuv(chapter):
    rec = json.load(open(SRC / "cuv" / f"fhl-unv-{chapter:02d}.json"))["record"]
    out = {}
    for r in rec:
        t = r["bible_text"].replace("•", "‧")
        for a, b in CUV_FIXES:
            t = t.replace(a, b)
        for a, b in VERSE_FIXES.get((chapter, r["sec"]), []):
            t = t.replace(a, b)
        out[r["sec"]] = t.strip()
    return out


def nasb(chapter):
    t = open(SRC / "nasb" / f"biblehub-{chapter:02d}.htm", encoding="utf8", errors="ignore").read()
    a = t.find('<div class="chap">')
    seg = t[a:t.find("</div>", a)]
    seg = re.sub(r'L<font size="1">ORD</font>', "LORD", seg)
    seg = re.sub(r'<font size="1">([^<]*)</font>', r"\1", seg)
    parts = re.split(r'<span class="reftext"><a [^>]*><b>(\d+)</b></a></span>', seg)
    out = {}
    for i in range(1, len(parts), 2):
        body = parts[i + 1]
        body = re.sub(r"<i>(.*?)</i>", r"*\1*", body, flags=re.S)
        body = re.sub(r"<br\s*/?>|<p>", " ", body)
        body = re.sub(r"<[^>]+>", "", body)
        body = html.unescape(body).replace("\xa0", " ")
        body = body.translate({0x91: "'", 0x92: "'", 0x93: '"', 0x94: '"', 0x96: "-", 0x97: "—"})
        body = re.sub(r"[‘’]", "'", body)
        body = re.sub(r"[“”]", '"', body)
        body = re.sub(r"\s+", " ", body).strip()
        # biblehub appends the NEXT section's heading in italics after the last verse of a section
        body = re.sub(r'(?<=[.:;,!?"—\'])\s*\*[A-Z][^*]*\*\s*$', "", body)
        body = re.sub(r'(?<=\*)\s*\*[A-Z][A-Za-z ,\']*[a-z]\*\s*$', "", body)
        out[int(parts[i])] = body
    return out


def block(stem):
    ref, ch, v1, v2, starts = UNITS[stem]
    zh, en = cuv(ch), nasb(ch)

    def paras(src, sep=""):
        chunks, cur = [], []
        for v in range(v1, v2 + 1):
            if v in starts and cur:
                chunks.append(cur)
                cur = []
            cur.append(f"^{v}^{src[v]}")
        chunks.append(cur)
        return "\n\n".join("> " + sep.join(c) for c in chunks)

    return ("### 中文 — 和合本 (CUV)\n\n" + paras(zh) + "\n\n### English — NASB\n\n" + paras(en, " ") + "\n")


LETTERS = re.compile(r"[^一-鿿]")


def letters(s):
    """CJK ideographs only: strips punctuation, 「」, spaces, and the （原文…） gloss brackets' ASCII."""
    return LETTERS.sub("", s.replace("裡", "裏"))   # house style 裏 (2026-07 policy) over the sources' 裡


def source_agreement():
    """Generated CUV vs ai-eden and cnbible CUVT, ideographs only. Returns list of problems."""
    bad = []
    for ch in (1, 2, 3):
        mine = cuv(ch)
        ai = {v["verse"]: v["textZh"] for v in json.load(open(SRC / "cuv" / f"aieden-{ch:02d}.json"))["data"]["verses"]}
        cn = {}
        t = open(SRC / "cnbible" / f"{ch}.htm", encoding="utf8", errors="ignore").read()
        for m in re.finditer(r'<span class="reftext"><a href="/joel/%d-(\d+)\.htm"><b>\d+</b></a></span><span class="btext3">([^<]*)</span>' % ch, t):
            cn.setdefault(int(m.group(1)), m.group(2))
        for v, txt in sorted(mine.items()):
            a, b, c = letters(txt), letters(ai[v]), letters(cn[v])
            if not (a == b == c):
                bad.append((ch, v, txt, ai[v], cn[v]))
    return bad


def main():
    out = BOOK / ".sources" / "units"
    if "--check" in sys.argv:
        bad = 0
        for stem in UNITS:
            f = BOOK / f"{stem}.md"
            if not f.exists():
                print(f"MISSING  {f.name}")
                bad += 1
                continue
            text = f.read_text()
            m = re.search(r"^## 經文.*?\n(.*?)^---\s*$", text, flags=re.S | re.M)
            have = (m.group(1) if m else "").strip()
            want = block(stem).strip()
            if have != want:
                bad += 1
                print(f"DIFFERS  {f.name}")
            else:
                print(f"OK       {f.name}")
        problems = source_agreement()
        for p in problems:
            print("CUV-SOURCE-DISAGREE", p)
        print(f"CUV generated vs ai-eden vs cnbible: {73 - len(problems)}/73 verses agree (ideographs only)")
        sys.exit(1 if (bad or problems) else 0)
    out.mkdir(exist_ok=True)
    for stem in UNITS:
        (out / f"{stem}.scripture.md").write_text(block(stem))
        print("wrote", stem)
    rows = []
    for ch in (1, 2, 3):
        zh, en = cuv(ch), nasb(ch)
        for v in sorted(zh):
            rows.append(f"{ch}:{v}\t{zh[v]}\t{en[v]}")
    (SRC / "scripture-all.tsv").write_text("# verse\tCUV (ai-eden characters, fhl punctuation)\tNASB 1995 (biblehub)\n" + "\n".join(rows) + "\n")
    print("wrote scripture-all.tsv", len(rows), "verses")


if __name__ == "__main__":
    main()

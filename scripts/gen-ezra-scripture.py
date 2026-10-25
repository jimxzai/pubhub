#!/usr/bin/env python3
"""Generate each Ezra chapter's `## 經文` block (CUV + NASB 1995) from fetched sources.

WHY A SCRIPT
------------
Scripture text typed or "recalled" by an author-agent is where this repo has
shipped its worst defects (98 wrong characters in Acts, a fabricated verse in
Job's front matter). The Ezra volume therefore never lets an agent write
Scripture: every chapter pastes the block this script prints, and the book
check (`--check`) re-derives it and diffs against the chapter file.

SOURCES (books/bible/ezra/.sources/)
  cuv/fhl-unv-NN.json      bible.fhl.net 'unv'  - punctuation, 「」, 　神 spacing
  cuv/aieden-NN.json       ai-eden.com API      - project-standard characters/names
  cnbible/N.htm            cnbible.com          - third source for the diff
  nasb/biblehub-NN.htm     biblehub.com/nasb/   - NASB 1995 (italics = supplied words)

CUV rule: fhl text as the base (it carries punctuation and the 　神 spacing),
with the nine proper-name/character choices where fhl modernises and BOTH
ai-eden and cnbible agree on the old form (推羅 利巴嫩 毗 瑪 梁 瑪代 他們).
Name dots U+2022 -> U+2027, matching the other volumes.

USAGE
  python3 scripts/gen-ezra-scripture.py            # write .sources/units/NN.scripture.md
  python3 scripts/gen-ezra-scripture.py --check    # diff each chapter's 經文 block
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "ezra"
SRC = BOOK / ".sources"

# unit file stem -> (reference line, chapter, first verse, last verse, paragraph-start verses)
UNITS = {
    "01-cyrus-decree-and-the-vessels": ("以斯拉記 1:1-11", 1, 1, 11, [1, 2, 5, 7]),
    "02-the-list-of-the-returned": ("以斯拉記 2:1-70", 2, 1, 70, [1, 2, 36, 40, 43, 55, 59, 64, 68]),
    "03-altar-before-foundation": ("以斯拉記 3:1-13", 3, 1, 13, [1, 2, 7, 10, 12]),
    "04-adversaries-and-the-stopped-work": ("以斯拉記 4:1-24", 4, 1, 24, [1, 6, 7, 8, 11, 17, 23]),
    "05-prophets-and-the-governors-letter": ("以斯拉記 5:1-17", 5, 1, 17, [1, 3, 6, 11]),
    "06-the-scroll-at-ecbatana": ("以斯拉記 6:1-12", 6, 1, 12, [1, 3, 6, 12]),
    "07-dedication-and-passover": ("以斯拉記 6:13-22", 6, 13, 22, [13, 16, 19]),
    "08-ezra-the-scribe": ("以斯拉記 7:1-10", 7, 1, 10, [1, 6, 10]),
    "09-the-kings-decree-for-ezra": ("以斯拉記 7:11-28", 7, 11, 28, [11, 12, 27]),
    "10-fast-at-the-ahava-canal": ("以斯拉記 8:1-23", 8, 1, 23, [1, 15, 21]),
    "11-treasure-and-the-road": ("以斯拉記 8:24-36", 8, 24, 36, [24, 31, 33]),
    "12-ezras-confession": ("以斯拉記 9:1-15", 9, 1, 15, [1, 3, 5, 6, 10]),
    "13-shecaniah-and-the-covenant": ("以斯拉記 10:1-17", 10, 1, 17, [1, 5, 9, 10]),
    "14-the-register-of-the-guilty": ("以斯拉記 10:18-44", 10, 18, 44, [18, 25, 44]),
}

# fhl 'unv' modernises these; ai-eden and cnbible both keep the 1919 form.
CUV_FIXES = [("泰爾", "推羅"), ("黎巴嫩", "利巴嫩"), ("毘", "毗"), ("撒馬利亞", "撒瑪利亞"),
             ("樑", "梁"), ("米底亞", "瑪代"), ("離絕她們所", "離絕他們所"),
             ("裡", "裏")]   # house style: 裏 (see 2026-07 style policy)


def cuv(chapter):
    rec = json.load(open(SRC / "cuv" / f"fhl-unv-{chapter:02d}.json"))["record"]
    out = {}
    for r in rec:
        t = r["bible_text"].replace("•", "‧")
        for a, b in CUV_FIXES:
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
        # NASB prints a closing quote mark after the italic closer: *it.*" is fine; normalise '* ' spacing
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
        sys.exit(1 if bad else 0)
    out.mkdir(exist_ok=True)
    for stem in UNITS:
        (out / f"{stem}.scripture.md").write_text(block(stem))
        print("wrote", stem)


if __name__ == "__main__":
    main()

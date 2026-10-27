#!/usr/bin/env python3
"""Generate each Daniel chapter's `## 經文` block (CUV + NASB 1995) from fetched sources.

Same design as gen-ezra-scripture.py: no author-agent ever types Scripture. Every
chapter pastes the block this script prints, and `--check` re-derives it and diffs
against the chapter file.

SOURCES (books/bible/daniel/.sources/)
  cuv/fhl-unv-NN.json      bible.fhl.net 'unv'  - punctuation, 「」『』, 　神 spacing
  cuv/aieden-NN.json       ai-eden.com API      - project-standard characters/names
  cnbible/N.htm            cnbible.com          - third source (mixed versions; tie-break only)
  nasb/biblehub-NN.htm     biblehub.com/nasb/   - NASB 1995 (italics = supplied words)

CUV rule: fhl text as the base (it carries punctuation and the 　神 spacing), with the
character/name choices where fhl modernises and ai-eden keeps the 1919 form (see
CUV_FIXES; full list in .sources/CUV-DIFF-REPORT.txt).

USAGE
  python3 scripts/gen-daniel-scripture.py            # write .sources/units/NN.scripture.md
  python3 scripts/gen-daniel-scripture.py --check    # diff each chapter's 經文 block
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "daniel"
SRC = BOOK / ".sources"

# unit file stem -> (reference line, chapter, first verse, last verse, paragraph-start verses)
UNITS = {
    "01-the-lord-gave": ("但以理書 1:1-21", 1, 1, 21, [1, 3, 8, 17]),
    "02-the-forgotten-dream": ("但以理書 2:1-23", 2, 1, 23, [1, 4, 12, 17, 20]),
    "03-the-image-and-the-stone": ("但以理書 2:24-49", 2, 24, 49, [24, 31, 36, 46]),
    "04-even-if-not": ("但以理書 3:1-30", 3, 1, 30, [1, 8, 13, 19, 24, 28]),
    "05-the-most-high-rules": ("但以理書 4:1-37", 4, 1, 37, [1, 4, 19, 28, 34]),
    "06-the-writing-on-the-wall": ("但以理書 5:1-31", 5, 1, 31, [1, 5, 10, 13, 17, 25, 30]),
    "07-the-lions-den": ("但以理書 6:1-28", 6, 1, 28, [1, 6, 10, 16, 19, 25]),
    "08-four-beasts-and-the-son-of-man": ("但以理書 7:1-14", 7, 1, 14, [1, 2, 9, 13]),
    "09-the-kingdom-given-to-the-saints": ("但以理書 7:15-28", 7, 15, 28, [15, 19, 23, 26]),
    "10-the-ram-and-the-goat": ("但以理書 8:1-27", 8, 1, 27, [1, 3, 9, 15, 19, 27]),
    "11-daniels-prayer": ("但以理書 9:1-19", 9, 1, 19, [1, 3, 4, 15]),
    "12-seventy-sevens": ("但以理書 9:20-27", 9, 20, 27, [20, 24, 26]),
    "13-the-unseen-conflict": ("但以理書 10:1-21", 10, 1, 21, [1, 4, 10, 15, 18]),
    "14-kings-of-the-south-and-north": ("但以理書 11:1-35", 11, 1, 35, [1, 5, 20, 29, 32]),
    "15-the-king-who-exalts-himself": ("但以理書 11:36-45", 11, 36, 45, [36, 40, 44]),
    "16-rise-to-your-lot": ("但以理書 12:1-13", 12, 1, 13, [1, 4, 5, 8, 13]),
}

# fhl 'unv' modernises these; ai-eden (the project standard) keeps the 1919 form.
CUV_FIXES = [("牠", "他"), ("她", "他"), ("嗎", "麼"), ("祕", "秘"), ("希臘王", "希利尼王"),
             ("毘", "毗"), ("吧！", "罷！"), ("焰", "燄"), ("米底亞", "瑪代"), ("利比亞", "呂彼亞"),
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
        # ...and when the verse's last words are themselves italic (Dan 7:8) the heading follows a closing '*'
        body = re.sub(r'(?<=\*)\s*\*[A-Z][A-Za-z ,\']*[a-z]\*\s*$', "", body)
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

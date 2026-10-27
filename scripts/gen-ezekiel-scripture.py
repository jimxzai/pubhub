#!/usr/bin/env python3
"""Generate each Ezekiel chapter's `## 經文` block (CUV + NASB 1995) from fetched sources.

WHY A SCRIPT
------------
Scripture text typed or "recalled" by an author-agent is where this repo has
shipped its worst defects. The Ezekiel volume therefore never lets an agent
write Scripture: every chapter pastes the block this script prints, and the
book check (`--check`) re-derives it and diffs against the chapter file.

SOURCES (books/bible/ezekiel/.sources/)
  cuv/fhl-unv-NN.json      bible.fhl.net 'unv'  - punctuation, 「」, 　神 spacing
  aieden/aieden-NN.json    ai-eden.com API      - project-standard characters/names (+ its NASB)
  cuv/cnbible-NN.htm       cnbible.com          - third source for the diff (CUV column)
  nasb/biblehub-NN.htm     biblehub.com/nasb/   - NASB 1995 (italics = supplied words)

CUV rule: fhl text as the base (it carries punctuation and the 　神 spacing),
with proper-name/character choices where fhl modernises and BOTH ai-eden and
cnbible agree on the old form (CUV_FIXES below, derived from `--diff`).
Name dots U+2022 -> U+2027, matching the other volumes.

USAGE
  python3 scripts/gen-ezekiel-scripture.py --diff    # three-source CUV disagreements (to derive CUV_FIXES)
  python3 scripts/gen-ezekiel-scripture.py           # write .sources/units/NN-*.scripture.md
  python3 scripts/gen-ezekiel-scripture.py --check   # diff each chapter file's 經文 block
  python3 scripts/gen-ezekiel-scripture.py --write-chapters   # rewrite each chapter's 經文 block from the generator
"""
import html
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "ezekiel"
SRC = BOOK / ".sources"

# unit stem -> (reference line, first chapter, first verse, last chapter, last verse)
UNITS = {
    "01-by-the-river-chebar": (1, 1, 1, 28),
    "02-eat-this-scroll": (2, 1, 3, 15),
    "03-the-watchman": (3, 16, 3, 27),
    "04-signs-without-words": (4, 1, 5, 17),
    "05-to-the-mountains-of-israel": (6, 1, 7, 27),
    "06-idols-in-the-temple": (8, 1, 8, 18),
    "07-the-mark-and-the-threshold": (9, 1, 10, 22),
    "08-the-glory-leaves-the-city": (11, 1, 11, 25),
    "09-baggage-and-false-peace": (12, 1, 13, 23),
    "10-idols-in-the-heart": (14, 1, 15, 8),
    "11-the-foundling": (16, 1, 16, 63),
    "12-the-two-eagles-and-the-twig": (17, 1, 17, 24),
    "13-the-soul-that-sins": (18, 1, 18, 32),
    "14-lament-and-the-history-of-rebellion": (19, 1, 20, 44),
    "15-the-song-of-the-sword": (20, 45, 21, 32),
    "16-the-city-of-blood": (22, 1, 22, 31),
    "17-two-sisters": (23, 1, 23, 49),
    "18-the-pot-and-the-wifes-death": (24, 1, 24, 27),
    "19-neighbors-and-tyre": (25, 1, 26, 21),
    "20-lament-for-the-ship": (27, 1, 27, 36),
    "21-the-prince-of-tyre": (28, 1, 28, 26),
    "22-pharaoh-and-the-nile": (29, 1, 30, 26),
    "23-the-cedar-and-the-pit": (31, 1, 32, 32),
    "24-the-watchman-restored": (33, 1, 33, 33),
    "25-the-shepherds": (34, 1, 34, 31),
    "26-two-mountains": (35, 1, 36, 15),
    "27-a-new-heart": (36, 16, 36, 38),
    "28-the-dry-bones": (37, 1, 37, 28),
    "29-gog-and-magog": (38, 1, 39, 29),
    "30-the-measuring": (40, 1, 42, 20),
    "31-the-glory-returns": (43, 1, 44, 31),
    "32-the-prince-and-the-land": (45, 1, 46, 24),
    "33-the-river": (47, 1, 47, 23),
    "34-the-lord-is-there": (48, 1, 48, 35),
}

# fhl 'unv' modernises these; ai-eden and cnbible both keep the 1919 form.
# (filled from `--diff`; each pair verified against both other sources)
CUV_FIXES = [
    ("泰爾", "推羅"), ("撒馬利亞", "撒瑪利亞"), ("黎巴嫩", "利巴嫩"), ("大馬士革", "大馬色"),
    ("毘", "毗"), ("利比亞", "呂彼亞"), ("阿拉伯", "亞拉伯"), ("約旦", "約但"),
    ("被火燒毀了", "被火燒燬了"), ("猛烈的火焰", "猛烈的火燄"), ("可做掌權者的杖", "可作掌權者的杖"),
    ("裡", "裏"),   # house style: 裏 (see 2026-07 style policy)
]
# Deliberate exception: 47:3-5 keep fhl's 蹚 (ai-eden/cnbible print 逿, a glyph Songti SC lacks).

_START = re.compile(r"^(人子啊|主耶和華如此說|耶和華的話|第[一二三四五六七八九十]+年|[一二三四五六七八九十]+年|我們被擄|以後|當那日|到那日)")


def _fhl(ch):
    rec = json.load(open(SRC / "cuv" / f"fhl-unv-{ch:02d}.json"))["record"]
    return {r["sec"]: r["bible_text"].replace("•", "‧").strip() for r in rec}


def _aieden(ch):
    d = json.load(open(SRC / "aieden" / f"aieden-{ch:02d}.json"))["data"]["verses"]
    return {v["verse"]: (v["textZh"], v["text"]) for v in d}


def _cnbible(ch):
    t = open(SRC / "cuv" / f"cnbible-{ch:02d}.htm", encoding="utf8", errors="ignore").read()
    out = {}
    # each verse row: reftext <b>N</b> ... btext3 (characters separated by spaces)
    for m in re.finditer(r'<span class="reftext"><a [^>]*><b>(\d+)</b></a></span><span class="btext3">(.*?)</span>', t, flags=re.S):
        s = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        # the page lists traditional CUV first, then simplified CUV, both as btext3: keep the first
        out.setdefault(int(m.group(1)), re.sub(r"(?<=\S) (?=\S)", "", s).replace(" ", "").strip())
    return out


# fhl 'unv' also modernises pronouns and particles (她/它/牠 for 他; 嗎 for 麼; 吧 for 罷). The project
# standard is ai-eden's 1919 form, so at those positions (and only those) adopt ai-eden's character.
_ADOPT = {("她", "他"), ("它", "他"), ("牠", "他"), ("嗎", "麼"), ("吧", "罷")}


def _adopt_aieden(t, z):
    z = z.replace("﹖", "？")
    plain = re.sub("[「」『』]", "", t)
    if plain == t:
        probe, keep = t, None
    else:
        probe, keep = plain, t
    sm = difflib.SequenceMatcher(None, probe, z, autojunk=False)
    swaps = {}
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "replace" and (probe[i1:i2], z[j1:j2]) in _ADOPT:
            swaps[i1] = (probe[i1:i2], z[j1:j2])
    if not swaps:
        return t
    # apply on the original string, skipping quote marks when counting positions
    out, pos = [], 0
    for ch in t:
        if ch in "「」『』":
            out.append(ch); continue
        if pos in swaps and ch == swaps[pos][0]:
            out.append(swaps[pos][1])
        else:
            out.append(ch)
        pos += 1
    return "".join(out)


def cuv(ch):
    out = {}
    ai = _aieden(ch)
    for sec, t in _fhl(ch).items():
        for a, b in CUV_FIXES:
            t = t.replace(a, b)
        if sec in ai:
            t = _adopt_aieden(t, ai[sec][0])
        if t.strip() == "a":   # 39:27 is a bare placeholder in fhl, ai-eden and cnbible; its content sits in 39:26
            t = "（此節與上節在本書所用的和合本來源中併為一節；見附錄說明）"
        out[sec] = t
    return out


def nasb(ch):
    t = open(SRC / "nasb" / f"biblehub-{ch:02d}.htm", encoding="utf8", errors="ignore").read()
    a = t.find('<div class="chap">')
    seg = t[a:t.find("</div>", a)]
    seg = re.sub(r'L<font size="1">ORD</font>', "LORD", seg)
    seg = re.sub(r'G<font size="1">OD</font>', "GOD", seg)
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
        out[int(parts[i])] = body
    return out


def _norm_zh(s):
    return re.sub(r"[\s　，。、；：！？「」『』（）()\-—…‧•·]", "", s)


def _norm_en(s):
    return re.sub(r"[^a-z0-9]", "", s.replace("*", "").replace("[", "").replace("]", "").lower())


def diff():
    n = 0
    for ch in range(1, 49):
        f, a, c = _fhl(ch), _aieden(ch), _cnbible(ch)
        for v in sorted(f):
            x, y, z = _norm_zh(f[v]), _norm_zh(a[v][0]), _norm_zh(c.get(v, ""))
            if not (x == y == z):
                n += 1
                print(f"CUV-DIFF {ch}:{v}")
                print(f"  fhl    : {f[v]}")
                print(f"  ai-eden: {a[v][0]}")
                print(f"  cnbible: {c.get(v, '(missing)')}")
    print(f"-- {n} verses differ", file=sys.stderr)
    m = 0
    for ch in range(1, 49):
        a, b = _aieden(ch), nasb(ch)
        for v in sorted(a):
            if _norm_en(a[v][1]) != _norm_en(b.get(v, "")):
                m += 1
                print(f"NASB-DIFF {ch}:{v}\n  ai-eden : {a[v][1]}\n  biblehub: {b.get(v, '(missing)')}")
    print(f"-- {m} NASB verses differ (ai-eden vs biblehub)", file=sys.stderr)


def block(stem):
    c1, v1, c2, v2 = UNITS[stem]
    zh = {ch: cuv(ch) for ch in range(c1, c2 + 1)}
    en = {ch: nasb(ch) for ch in range(c1, c2 + 1)}
    keys = []
    for ch in range(c1, c2 + 1):
        lo = v1 if ch == c1 else 1
        hi = v2 if ch == c2 else max(zh[ch])
        keys += [(ch, v) for v in range(lo, hi + 1)]

    def label(ch, v):
        # multi-chapter units: show chapter:verse at each chapter start (verse label elsewhere)
        return f"{v}" if c1 == c2 else (f"{ch}:{v}" if v == 1 or (ch, v) == keys[0] else f"{v}")

    # paragraph starts: derived from the Chinese text so both columns break at the same verses
    starts, run = {keys[0]}, 0
    for (ch, v) in keys[1:]:
        run += 1
        t = zh[ch][v]
        new_chapter = v == 1
        if new_chapter or (run >= 3 and _START.match(t)) or run >= 9:
            starts.add((ch, v)); run = 0

    # fold a trailing one-verse paragraph into the previous one (unless it opens a new chapter)
    last = max(starts, key=keys.index)
    if len(keys) - keys.index(last) == 1 and last != keys[0] and last[1] != 1:
        starts.discard(last)

    def paras(src, sep):
        chunks, cur = [], []
        for k in keys:
            if k in starts and cur:
                chunks.append(cur); cur = []
            cur.append(f"^{label(*k)}^{src[k[0]][k[1]]}")
        chunks.append(cur)
        return "\n\n".join("> " + sep.join(c) for c in chunks)

    return ("### 中文 — 和合本 (CUV)\n\n" + paras(zh, "") + "\n\n### English — NASB\n\n" + paras(en, " ") + "\n")


def main():
    if "--diff" in sys.argv:
        return diff()
    out = SRC / "units"
    if "--write-chapters" in sys.argv:
        for stem in UNITS:
            f = BOOK / f"{stem}.md"
            text = f.read_text()
            m = re.search(r"^## 經文.*?\n(.*?)^---\s*$", text, flags=re.S | re.M)
            tail = "\n\n" if m.group(1).endswith("\n\n") else "\n"
            new = text[:m.start(1)] + block(stem).strip() + tail + text[m.end(1):]
            if new != text:
                f.write_text(new); print("rewrote", f.name)
        return
    if "--check" in sys.argv:
        bad = 0
        for stem in UNITS:
            f = BOOK / f"{stem}.md"
            if not f.exists():
                print(f"MISSING  {f.name}"); bad += 1; continue
            text = f.read_text()
            m = re.search(r"^## 經文.*?\n(.*?)^---\s*$", text, flags=re.S | re.M)
            have = (m.group(1) if m else "").strip()
            if have != block(stem).strip():
                bad += 1; print(f"DIFFERS  {f.name}")
            else:
                print(f"OK       {f.name}")
        sys.exit(1 if bad else 0)
    out.mkdir(exist_ok=True)
    for stem in UNITS:
        (out / f"{stem}.scripture.md").write_text(block(stem))
        print("wrote", stem)


if __name__ == "__main__":
    main()

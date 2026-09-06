#!/usr/bin/env python3
"""Verify Scripture quoted in EDITORIAL PROSE, not in the 經文 blocks.

WHY THIS SURFACE
----------------
verify_nasb.py and verify_cuv_dual.py both parse only the `### 中文 — 和合本 (CUV)`
and `### English — NASB` blocks. But the book also quotes Scripture inline, all
through its commentary: 「耶和華─你們的神本是上天下地的神」（2:11）. Nothing has ever
checked those. The 2026-09-06 CUV round found four defects there — the 和合本 破折號
dropped at 書2:11 (×3) and 申29:18 — and found them by grep, by luck, not by any audit.
This is the audit that surface should have had.

METHOD
  Take every 「…」（ref） on a non-scripture-block line, resolve the reference (a bare
  N:N means Joshua; a prefixed one is mapped to its fhl 書卷代碼), fetch the verse(s)
  from bible.fhl.net, and require the quote to appear inside them.

  Normalisation matches verify_cuv.py's: 裏/裡, the honorific full-width space before
  神, all punctuation. The 破折號 is NOT normalised away — it is exactly what went wrong.

  A quote spanning a range (N:N-N) is checked against the concatenated verses, so a
  citation stitching two verses together still passes.

Reported:
  MISS   quote not found in the cited verse(s) — a real finding
  SKIP   reference could not be resolved (unmapped book abbreviation)

Usage: python3 verify-prose-citations.py <book-dir> --self <和合本書卷代碼>

  --self names the abbreviation a bare "N:M" reference means (書 for Joshua, 路 for Luke…).
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

CACHE = Path(__file__).resolve().parent / "fhl-prose-cache"
PUNCT = "，。；：、！？「」『』（）〔〕—…·　 　〈〉《》"

# fhl 書卷代碼 for every abbreviation this book actually uses
BOOKS = {
    "創": "創", "出": "出", "利": "利", "民": "民", "申": "申", "書": "書",
    "士": "士", "得": "得", "撒上": "撒上", "撒下": "撒下", "王上": "王上",
    "王下": "王下", "代上": "代上", "代下": "代下", "尼": "尼", "伯": "伯",
    "詩": "詩", "箴": "箴", "傳": "傳", "賽": "賽", "耶": "耶", "結": "結",
    "但": "但", "何": "何", "摩": "摩", "拿": "拿", "彌": "彌", "亞": "亞",
    "瑪": "瑪", "瑪拉基書": "瑪", "太": "太", "可": "可", "路": "路",
    "約": "約", "徒": "徒", "羅": "羅", "林前": "林前", "林後": "林後",
    "加": "加", "弗": "弗", "腓": "腓", "西": "西", "帖前": "帖前",
    "提前": "提前", "提後": "提後", "多": "多", "門": "門", "來": "來",
    "雅": "雅", "彼前": "彼前", "彼後": "彼後", "約一": "約一", "啟": "啟",
}

# The reference usually abuts the closing 」 but not always — the book writes
# 「…」——不待萬事太平才說 and 「…」的宣告（21:45）. Allow a short run of prose
# between them; anything longer risks pairing a quote with someone else's reference.
CITE = re.compile(r"「([^」]{4,120})」[^「」（）]{0,12}（([^）]{2,40})）")
REF = re.compile(r"^(?:參|如|另見|見)?\s*([一-鿿]{0,4}?)\s*(\d+):(\d+)(?:[-–](\d+))?")


def norm(s):
    s = s.replace("裡", "裏")
    s = re.sub(r"【[^】]*】", "", s)     # CUV's own bracketed gloss, which this book omits
    s = re.sub(r"[（(](?:原文|或譯|或作)[^）)]*[）)]", "", s)   # ditto, parenthesised
    s = s.replace("祂", "他")           # house convention: reverential pronoun for deity
    for c in PUNCT:
        s = s.replace(c, "")
    return re.sub(r"\s+", "", s)


def fragments(q):
    """An elided quote 「A……B」 is a legitimate citation: check each side separately."""
    parts = [x for x in re.split(r"…+|\.{3,}", q) if len(x.strip()) >= 3]
    return parts or [q]


def fetch(code, chap):
    CACHE.mkdir(exist_ok=True)
    safe = "".join(f"{ord(c):04x}" for c in code)
    f = CACHE / f"{safe}-{chap}.json"
    if not f.exists() or f.stat().st_size < 200:
        from urllib.parse import quote
        subprocess.run(["curl", "-s", "-m", "40", "-A", "Mozilla/5.0",
                        f"https://bible.fhl.net/json/qb.php?chineses={quote(code)}"
                        f"&chap={chap}&version=unv&gb=0", "-o", str(f)], check=True)
        time.sleep(1.2)
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if d.get("status") != "success":
        return {}
    return {int(r["sec"]): r.get("bible_text", "") for r in d.get("record", [])}


def load_accept(book):
    """{(filename, quote)} reviewed as a TERM rather than a quotation.

    Chinese uses 「」 for terms and labels too, where the adjacent （ref） is a
    "see also" pointer, not an attribution. Only entries read in context belong
    here — never a mismatch that has not been run down.
    """
    f = book / ".prose-citation-accept"
    out = set()
    if f.exists():
        for line in f.read_text(encoding="utf-8").split("\n"):
            if line.startswith("#") or "|" not in line:
                continue
            fn, q = line.split("|")[:2]
            out.add((fn.strip(), q.strip()))
    return out


def main():
    book = Path(sys.argv[1])
    self_code = "書"
    if "--self" in sys.argv:
        self_code = sys.argv[sys.argv.index("--self") + 1]
    accept = load_accept(book)
    checked = miss = skip = accepted = 0
    findings = []
    for path in sorted(book.glob("*.md")):
        for ln, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            if line.startswith(">") and "^" in line:
                continue                                  # scripture block
            for quote_txt, ref in CITE.findall(line):
                m = REF.match(ref)
                if not m:
                    continue
                abbr, ch, v1, v2 = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
                code = BOOKS.get(abbr) if abbr else self_code
                if code is None:
                    skip += 1
                    continue
                verses = fetch(code, ch)
                if not verses:
                    skip += 1
                    continue
                span = range(v1, int(v2) + 1) if v2 else [v1]
                hay = norm("".join(verses.get(v, "") for v in span))
                needle = norm(quote_txt)
                checked += 1
                pieces = [norm(x) for x in fragments(quote_txt)]
                if needle and needle not in hay and not all(
                        pc and pc in hay for pc in pieces):
                    if (path.name, quote_txt) in accept:
                        accepted += 1
                        continue
                    miss += 1
                    findings.append((path.name, ln, abbr or self_code, ch, v1, v2,
                                     quote_txt, verses.get(v1, "")))
    for fn, ln, abbr, ch, v1, v2, q, src in findings:
        rng = f"{ch}:{v1}" + (f"-{v2}" if v2 else "")
        print(f"  MISS {fn}:{ln}  （{abbr} {rng}）")
        print(f"       book: 「{q[:60]}」")
        print(f"       fhl : {src[:76]}")
    print(f"\n{checked} in-prose citation(s) checked | {miss} MISS | "
          f"{accepted} reviewed-as-term | {skip} unresolved")


if __name__ == "__main__":
    main()

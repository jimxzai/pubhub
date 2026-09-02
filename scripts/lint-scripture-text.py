#!/usr/bin/env python3
"""Static check for 和合本 (CUV) transcription slips inside scripture blocks.

WHY THIS EXISTS
---------------
2026-08-31: books/bible/2-peter claimed in its own appendix that every verse
had been checked 「逐節經 cnbible.com 核對」. A programmatic verse-by-verse diff
against two independent sources found four character-level errors that had
survived that claimed check and shipped:

    2:6   鑒戒   → CUV 鑑戒
    2:13  行得不義 → CUV 行的不義
    2:19  卻做敗壞 → CUV 卻作敗壞
    3:12  烈火熔化 → CUV 烈火鎔化

A full two-source diff is the real check, but it costs a network round trip per
chapter and nobody runs it on 969 files. This is the cheap half: a static pass
that flags the *character classes* those errors belong to, everywhere, in a
second. Same reasoning as scripts/lint-templates.sh — "an instruction to go
grep is a task nobody performs; a script runs every time."

WHAT IT CAN AND CANNOT DO
-------------------------
CAN:    flag characters CUV does not use (鑒/熔/汙/裡) and characters CUV uses
        rarely enough that every instance deserves a human look (做).
CANNOT: catch context-dependent slips like 行的/行得 or 速速的/速速地 — those
        are real CUV usage in some places and errors in others, so only a
        source diff settles them. Findings here are a floor, not a ceiling.

Scripture blocks are identified by the house format: blockquote lines carrying
^n^ verse markers. Commentary prose is deliberately not checked — 鑒戒 is
perfectly good modern Chinese and only wrong when it is standing in for a
quoted CUV verse.

Usage:  python3 scripts/lint-scripture-text.py [path ...]      # default books/bible
        python3 scripts/lint-scripture-text.py --all-text ...  # prose too
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "books" / "bible"

# Rules are WORD-scoped wherever CUV's choice is word-dependent, and only
# character-scoped where CUV is genuinely consistent.
#
# This distinction was learned the hard way: an earlier character-scoped rule
# for 「鑒」 flagged 彼前2:12「鑒察的日子」 as an error. Checked against
# cnbible.com, CUV really does write 鑒察 there — while writing 鑑戒 at 彼後2:6.
# A blanket 鑒→鑑 "fix" would have corrupted a correct verse. Same trap with
# 做/作: CUV writes 作妻子的 (彼前3:1) but 做工 (林前4:12), both verified.
# Where CUV is genuinely mixed, the rule FLAGS and refuses to suggest.
#
# pattern -> (suggestion or None, severity, note)
SUSPECT_RULES = [
    ("鑒戒", "鑑戒", "error",
     "CUV 作「鑑戒」（彼後2:6 等）；注意 CUV 另有「鑒察」用「鑒」，不可一律替換"),
    ("熔化", "鎔化", "error",
     "CUV 作「鎔化」（彼後3:12 等）"),
    ("汙", "污", "error",
     "CUV 作「污穢」「玷污」"),
    ("裡", "裏", "style",
     "本系列既定用字體例為「裏」；CUV 各數位版本身混用，屬體例而非誤植"),
    ("什麼", "甚麼", "style",
     "本系列既定用字體例為「甚麼」"),
    ("做", None, "review",
     "CUV 兩者皆用（作妻子的／做工，均經查證）——無法自動判定，須逐處回查原文"),
]

# kept for backward compatibility with callers importing SUSPECT
SUSPECT = {p: (s or "?", n) for p, s, _sev, n in
           [(r[0], r[1], r[2], r[3]) for r in SUSPECT_RULES]}

VERSE_MARK = re.compile(r"\^\d")
# a blockquote opening with a bold scripture reference: > **彼後 3:18** …
BOLD_REF = re.compile(r"^>\s*\*\*(?:NASB\s*)?[\u4e00-\u9fff A-Za-z]{0,12}\d+:\d")
# a heading that opens a block of quoted scripture with no per-verse markers
QUOTE_HEADING = re.compile(r"^#{2,4}\s*(詩篇|詩\s|經文)")
# the run of blockquote lines under such a heading ends at the next heading or
# at the first non-blockquote, non-blank line
HEADING = re.compile(r"^#{1,6}\s")


def scripture_lines(path, all_text=False):
    """Yield (lineno, text) for lines that are quoted scripture.

    Three shapes count, because the book uses all three and the first version
    of this script only knew about one:

      1. blockquotes carrying ^n^ verse markers      (the chapter 經文 blocks)
      2. blockquotes opening with a bold reference   (> **彼後 3:18** …)
      3. blockquote runs under a 詩篇/經文 heading    (the 詩篇回應 blocks)

    Shape 3 is why this matters. The 2 Peter 詩篇回應 sections carry ~25 verses
    of quoted CUV with no verse markers at all, so the marker-only rule made
    them invisible — to this linter AND to the verse-diff harness. They went
    unchecked through five review passes before anyone looked.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return
    under_quote_heading = False
    for i, ln in enumerate(lines, 1):
        if all_text:
            yield i, ln
            continue
        s = ln.lstrip()
        if HEADING.match(s):
            under_quote_heading = bool(QUOTE_HEADING.match(s))
            continue
        if not s.startswith(">"):
            # a blank line does not end the run; prose does
            if s:
                under_quote_heading = False
            continue
        if VERSE_MARK.search(s) or BOLD_REF.match(s) or under_quote_heading:
            yield i, ln


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    all_text = "--all-text" in sys.argv
    targets = [Path(a) for a in args] or [DEFAULT]

    files = []
    for t in targets:
        files.extend(sorted(t.rglob("*.md")) if t.is_dir() else [t])

    findings = {}       # volume -> list of (relpath, lineno, char, ctx)
    scanned = blocks = 0
    for f in files:
        scanned += 1
        for lineno, ln in scripture_lines(f, all_text):
            blocks += 1
            for pat, should, sev, _why in SUSPECT_RULES:
                if pat in ln:
                    ch = pat
                    should = should or "（須回查，CUV 兩者皆用）"
                    idx = ln.index(pat)
                    ctx = ln[max(0, idx - 12): idx + 13].replace("\n", " ")
                    try:
                        vol = f.relative_to(DEFAULT).parts[0]
                    except ValueError:
                        vol = f.parent.name
                    try:
                        rel = f.relative_to(ROOT)
                    except ValueError:
                        rel = f            # target outside the repo (e.g. a
                                           # git-extracted copy under /tmp)
                    findings.setdefault(vol, []).append(
                        (rel, lineno, ch, should, ctx, sev))

    total = sum(len(v) for v in findings.values())
    print(f"scanned {scanned} file(s), {blocks} scripture line(s)\n")
    if not total:
        print("clean: no suspect characters in any scripture block")
        return 0

    for vol in sorted(findings, key=lambda v: -len(findings[v])):
        rows = findings[vol]
        print(f"── {vol}  ({len(rows)} finding(s))")
        for rel, lineno, ch, should, ctx, sev in rows[:12]:
            print(f"   [{sev:<6}] {rel}:{lineno}  「{ch}」→「{should}」   …{ctx}…")
        if len(rows) > 12:
            print(f"   … and {len(rows) - 12} more")
        print()

    print(f"{total} finding(s) across {len(findings)} volume(s).")
    print("Each is a CANDIDATE — confirm against cnbible.com / bible.fhl.net")
    print("before changing anything; some are genuine CUV edition variants.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

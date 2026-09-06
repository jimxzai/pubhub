#!/usr/bin/env python3
"""Normalize a scanned public-domain source text before feeding it to
verify-citations.py, so page headers/numbers and line-wrap hyphenation
don't produce false DRIFT/MISS results.

WHY THIS EXISTS
---------------
verify-citations.py's norm() collapses whitespace and strips punctuation
(including hyphens) to a single space each, then does substring matching.
That defeats two extremely common OCR artifacts in 19th/early-20th-century
scanned book text:

  1. A word split across a page's line-wrap: "afflic-\ntions" survives
     norm() as two separate words "afflic tions", which will never contain
     the needle "afflictions" as a substring -- a false MISS or DRIFT even
     though the quote is perfectly verbatim.
  2. A running head or bare page number sitting on its own line where a
     page break falls mid-sentence: "...the last line of page 6\nCHAPTER
     I. 7\ncontinuing here..." gets glued into one haystack string with
     "chapter i 7" wedged between two halves of a real, unbroken sentence.

Both were confirmed live on Ruth's three sources (2026-09): Fuller's OCR
carries "CHAPTER I. <n>" (or OCR-mangled "CHAPTER r." / "CHAPTER J.")
running heads roughly every 70 lines; Morgan and Henry carry bare "RUTH"
/ "R U T H" running heads and bare page-number lines at page breaks.

WHAT IT DOES
------------
1. Drops lines that are ONLY a running head and/or a page number -- never
   touches a line that also carries prose, so a real sentence is never cut.
2. Rejoins a hyphenated line-wrap ("word-\n  word2" -> "wordword2").
3. Leaves everything else byte-identical -- this is a source-fidelity tool,
   not a rewrite. Run a diff-of-word-count sanity check before trusting a
   normalized file: it should lose only the header/number lines, nothing else.

USAGE
    python3 scripts/normalize-ocr-source.py <infile> <outfile>
    python3 scripts/normalize-ocr-source.py <infile> <outfile> --report

--report prints how many header/number lines were dropped and how many
hyphenated line-wraps were rejoined, so you can sanity-check the delta
isn't implausibly large (a real bug here would silently eat real prose).
"""
import argparse
import re
import sys
from pathlib import Path

# A line that is PURELY a running head and/or page number -- no other prose.
# Deliberately conservative: requires the whole line (after stripping) to
# match, so a sentence that merely contains a number is never touched.
HEADER_LINE_RE = re.compile(
    r"""^\s*(
        R\s*U\s*T\s*H                                  |  # spaced running head
        RUTH                                            |  # plain running head
        CHAPTER\s+[IVXLCDM]+\.?\s*\d*                    |  # "CHAPTER I. 7"
        CHAPTER\s+[a-zA-Z]\.\s*\d*                       |  # OCR-mangled "CHAPTER r. 15"
        \d{1,4}                                          |  # bare page number
        \d{1,4}\s+ruth                                   |  # "118 ruth"
        S\s*A\s*M\s*U\s*E\s*L\.?                          |
        Faith\s+and\s+Faithlessness\s+\d{1,4}             |  # Morgan's own running head
        (?:The\s+)?(?:Choice|Venture|Reward)\s+of\s+Faith\s*\d{0,4}
    )\s*$""",
    re.X | re.I,
)

# Hyphenated word split across a line-wrap: lowercase-hyphen-newline-lowercase.
# Only lowercase-to-lowercase, so we never touch a genuine em-dash-style
# break between sentences (which would be capitalized on one side) or a
# hyphenated proper noun spanning majuscules.
LINEWRAP_HYPHEN_RE = re.compile(r"([a-z])-\s*\n\s*([a-z])")


def normalize(text):
    lines = text.split("\n")
    kept = []
    dropped = 0
    for line in lines:
        if line.strip() and HEADER_LINE_RE.match(line):
            dropped += 1
            continue
        kept.append(line)
    text = "\n".join(kept)

    text, n_joins = LINEWRAP_HYPHEN_RE.subn(r"\1\2", text)

    return text, dropped, n_joins


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile")
    ap.add_argument("outfile")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    src = Path(args.infile).read_text(encoding="utf-8", errors="replace")
    out, dropped, joins = normalize(src)
    Path(args.outfile).write_text(out, encoding="utf-8")

    if args.report:
        before_words = len(src.split())
        after_words = len(out.split())
        print(f"{args.infile} -> {args.outfile}")
        print(f"  header/page-number lines dropped: {dropped}")
        print(f"  hyphenated line-wraps rejoined:    {joins}")
        print(f"  word count: {before_words} -> {after_words} "
              f"({before_words - after_words} words removed by header-stripping)")
        if before_words - after_words > dropped * 6:
            print("  WARNING: word-count drop looks larger than the dropped "
                  "header lines can explain -- inspect before trusting this file.",
                  file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())

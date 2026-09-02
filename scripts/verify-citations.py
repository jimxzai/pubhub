#!/usr/bin/env python3
"""Verify a book's quoted commentary against a local copy of the real source.

WHY THIS EXISTS
---------------
2026-08-31, Gospel of Luke: the book's own citation ledger
(99-appendix-references.md) declared that all 24 chapters' Morgan sections were
summary-only with no verbatim quotes. Eight chapters actually carried 29 quoted
English passages. When they were finally checked against the published text,
28 matched exactly -- and four in one chapter turned out to be reworded
paraphrases wearing quotation marks ("heart-break in them" printed as
"heartbreak in these words", "irrevocable" as "inevitable"). Nothing in the
build pipeline can see that: xelatex typesets a fabricated quote as happily as
a real one, and a human spot-check reads a plausible-sounding sentence and
moves on.

The lesson matches scripts/lint-templates.sh: an instruction to go verify is a
task nobody performs; a script runs every time.

WHAT IT DOES
------------
Given a book directory and one or more --source files (plain-text copies of the
works being quoted), it extracts every `> "English quote"` line that sits under
a commentator heading and reports, per chapter:

    OK    quote found verbatim in a source
    DRIFT quote is *nearly* present -- a long fragment matches but the whole
          does not. This is the dangerous class: a real quote that has been
          silently reworded. Printed with the source's actual wording so you
          can fix the file rather than guess.
    MISS  no meaningful fragment found in any source; treat as unverified
          until you locate it or convert the point to unquoted summary.

Matching is deliberately forgiving about things that are not the author's
words -- case, curly vs straight quotes, dashes, ellipses, and the stray OCR
artifacts common in scanned public-domain text -- and strict about everything
else.

It also audits format consistency: quotes whose translation is inlined as
`> "English"（中文）` rather than the house two-line form, since a book that
mixes both looks unedited.

USAGE
    python3 scripts/verify-citations.py books/bible/gospel-of-luke \
        --source /path/to/cmorgan_luke.txt \
        [--heading 摩根] [--quiet]

Exit 1 if any DRIFT or MISS is found.
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

QUOTE_RE = re.compile(r'^> "(.+?)"', re.M)
INLINE_RE = re.compile(r'^> ".+?"（.+?）\s*$', re.M)
HEADING_RE = re.compile(r'^### (.+?)$', re.M)


def norm(text):
    """Fold away everything that is not the author's actual words."""
    text = unicodedata.normalize("NFKC", text)
    for a, b in [("’", "'"), ("‘", "'"), ("“", '"'),
                 ("”", '"'), ("—", " "), ("–", " "),
                 ("…", "...")]:
        text = text.replace(a, b)
    text = re.sub(r'["\']', "", text)
    text = re.sub(r"[^\w\s.]", " ", text)     # punctuation is OCR-unstable
    return re.sub(r"\s+", " ", text).strip().lower()


def fragments(quote):
    """Split a quote on ellipses; each part must stand on its own."""
    return [f.strip() for f in re.split(r"\.\.\.", norm(quote)) if len(f.strip()) > 15]


def longest_prefix_in(frag, haystack, floor=40):
    """Longest leading run of frag present in haystack, for DRIFT diagnosis."""
    lo, hi, best = floor, len(frag), 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if frag[:mid] in haystack:
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    return best


def section_of(text, pos):
    """Which ### heading does this offset live under?"""
    last = None
    for m in HEADING_RE.finditer(text):
        if m.start() > pos:
            break
        last = m.group(1)
    return last or "(no ### heading)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir")
    ap.add_argument("--source", action="append", default=[],
                    help="plain-text copy of a quoted work (repeatable)")
    ap.add_argument("--heading", default=None,
                    help="only check quotes under ### headings containing this")
    ap.add_argument("--quiet", action="store_true", help="only show problems")
    ap.add_argument("--accept", default=None,
                    help="file of reviewed, accepted deviations (see .citation-accept)")
    args = ap.parse_args()

    if not args.source:
        sys.exit("need at least one --source plain-text file to verify against")

    accepted = []
    if args.accept and Path(args.accept).exists():
        for line in Path(args.accept).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "|" in line:
                verdict, prefix, reason = (line.split("|", 2) + ["", ""])[:3]
                accepted.append((verdict.strip(), prefix.strip(), reason.strip()))

    sources = {}
    for s in args.source:
        raw = Path(s).read_text(encoding="utf-8", errors="replace")
        sources[Path(s).name] = norm(raw)
        print(f"source: {Path(s).name} ({len(raw):,} chars)")

    files = sorted(Path(args.book_dir).glob("[0-9]*.md"))
    totals = {"OK": 0, "DRIFT": 0, "MISS": 0, "ACCEPT": 0}
    inline = []

    for f in files:
        text = f.read_text(encoding="utf-8")
        rows = []
        for m in QUOTE_RE.finditer(text):
            head = section_of(text, m.start())
            if args.heading and args.heading not in head:
                continue
            quote = m.group(1)
            frags = fragments(quote) or [norm(quote)]
            verdict, note = "MISS", ""
            for name, hay in sources.items():
                if all(fr in hay for fr in frags):
                    verdict, note = "OK", name
                    break
            if verdict == "MISS":
                best_n, best_src, best_frag = 0, "", ""
                for name, hay in sources.items():
                    for fr in frags:
                        n = longest_prefix_in(fr, hay)
                        if n > best_n:
                            best_n, best_src, best_frag = n, name, fr
                if best_n >= 60:
                    verdict = "DRIFT"
                    ctx_at = sources[best_src].find(best_frag[:best_n])
                    note = (f"{best_src}: first {best_n} chars match, then diverges\n"
                            f"        source reads: ...{sources[best_src][ctx_at:ctx_at+best_n+90]}...")
            for av, aprefix, areason in accepted:
                if verdict == av and quote.startswith(aprefix):
                    verdict, note = "ACCEPT", areason
                    break
            totals[verdict] = totals.get(verdict, 0) + 1
            rows.append((verdict, head, quote, note))

        for m in INLINE_RE.finditer(text):
            head = section_of(text, m.start())
            if args.heading and args.heading not in head:
                continue
            inline.append((f.name, m.group(0)[:70]))

        shown = [r for r in rows if not args.quiet or r[0] != "OK"]
        if shown:
            print(f"\n{f.name}")
            for verdict, head, quote, note in shown:
                print(f"  {verdict:5s} [{head}] {quote[:72]}")
                if note and verdict != "OK":
                    print(f"        {note}")

    print(f"\n{'='*60}\nverbatim OK: {totals['OK']}   DRIFT: {totals['DRIFT']}   "
          f"MISS: {totals['MISS']}   accepted-deviation: {totals['ACCEPT']}")
    if inline:
        print(f"\nformat: {len(inline)} quote(s) inline the translation as \"English\"（中文）")
        print("        house style puts it on its own line after a bare '>' line")
        for fn, snip in inline[:12]:
            print(f"  {fn}: {snip}")
    sys.exit(1 if (totals["DRIFT"] or totals["MISS"]) else 0)


if __name__ == "__main__":
    main()

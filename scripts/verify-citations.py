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


LETTERS_ONLY = re.compile(r"[^a-z]")


def ocr_fold(normed):
    """Letters only -- the fold that makes a match survive a scanned source.

    `norm` keeps spaces and digits, so three kinds of scanner noise defeat it,
    and all three are noise the AUTHOR never wrote:

      * words broken across a line and rejoined with a space
        ("murmur ing", "in ability", "revealecla lory")
      * a page number dropped into the middle of a sentence
        ("...to be the means of restoring them by prayer. 222 job in the
        sacred act of intercession...")
      * a marginal verse reference set into the text
        ("If I did despise to be [Job xxxi,] judged in the cause of my
        manservant")

    Folding to letters alone is immune to all three without guessing at what
    the scanner meant -- no dictionary, no heuristic rejoining, nothing that
    could quietly "fix" a quote into matching. A run of 100+ letters matching
    by chance does not happen.

    A match found only after this fold is reported as OK-OCR, never as OK: it
    says the wording is the author's and the difference is in the scan, which
    is a weaker and more honest claim than "verbatim".
    """
    return LETTERS_ONLY.sub("", normed)


MAX_GAP = 16      # longest interpolation tolerated at one point
BASE_GAPS = 3     # interpolations allowed before length is considered
GAP_PER_CHARS = 120   # one more allowed per this many letters of quote
ANCHOR = 40       # letters that must match exactly before any gap is allowed


def _walk(frag, hay, k, pos, max_gap, budget):
    """Extend a match forward from frag[k]/hay[pos]. Returns gaps used or None."""
    gaps = 0
    while k < len(frag):
        probe = frag[k:k + 8]
        if hay.startswith(probe, pos):
            pos += len(probe)
            k += len(probe)
            continue
        if hay[pos:pos + 1] == frag[k:k + 1]:
            pos += 1
            k += 1
            continue
        if gaps >= budget:
            return None
        d = hay.find(probe, pos + 1, pos + 1 + max_gap + len(probe))
        if d == -1:
            return None
        pos, gaps = d, gaps + 1
    return gaps


def gap_budget(frag):
    """How many interpolations a fragment of this length may absorb.

    Page furniture appears once per page, so a long quote legitimately meets
    more of it than a short one: the 581-letter Morgan passage in chapter 30
    spans several pages of the scan. A flat allowance either fails long true
    quotes or is far too generous for short ones. Scaling with length keeps the
    allowance proportional to the number of page breaks actually crossed.
    """
    return BASE_GAPS + len(frag) // GAP_PER_CHARS


def contains_with_gaps(frag, hay, max_gap=MAX_GAP, max_gaps=None):
    """Is `frag` present in `hay` allowing a few short interpolations?

    Scanners splice page furniture into the middle of a sentence. Morgan's
    running head lands inside its own text --

        ...in it there are three THE DRAMA movements, the first consists
        of a terrible cursing of the day of his birth...

    -- and the same happens with 'JOB', 'CH. XXIII', 'BOOK', and stray roman
    numerals. None of it is the author's words; it is furniture the OCR could
    not tell from prose.

    An exact ANCHOR-letter window has to be found somewhere in the fragment
    before any tolerance applies -- anchoring only at the START was too rigid,
    because the header often lands within the first few words ('in it there
    are three THE DRAMA movements' breaks at letter 17). The match then extends
    forward from the anchor, and backward by running the same walk over both
    strings reversed.

    The tolerance is deliberately mean: each gap is at most max_gap letters and
    a fragment may absorb at most max_gaps of them, over and above an exact
    40-letter anchor. Those bounds are what keep this a verification rather
    than a wish -- the reworded quotes this script exists to catch
    ("irrevocable" printed as "inevitable") change words in place, which no
    amount of gap tolerance forgives.

    Returns the number of gaps used, or None.
    """
    if max_gaps is None:
        max_gaps = gap_budget(frag)
    if len(frag) <= ANCHOR:
        return 0 if frag in hay else None
    for i in range(0, min(len(frag) - ANCHOR, 96) + 1, 8):
        anchor = frag[i:i + ANCHOR]
        seed = hay.find(anchor)
        while seed != -1:
            fwd = _walk(frag, hay, i + ANCHOR, seed + ANCHOR, max_gap, max_gaps)
            if fwd is not None:
                if i == 0:
                    return fwd
                back = _walk(frag[:i][::-1], hay[:seed][::-1], 0, 0,
                             max_gap, max_gaps - fwd)
                if back is not None:
                    return fwd + back
            seed = hay.find(anchor, seed + 1)
    return None


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


# The gap tolerance above is the one place where this script could quietly stop
# being a verification. Loosen max_gap or max_gaps far enough and a reworded
# quote slips through as OK-OCR, which is exactly the failure the script was
# written to prevent. These cases pin the boundary: page furniture passes,
# every kind of rewording is refused. Run with --selftest; it needs no sources.
SELFTEST = [
    (True,  "verbatim",
     "In it there are three movements. The first consists of a terrible "
     "cursing of the day of his birth and the night of his conception."),
    (True,  "running head spliced into the sentence",
     "In it there are three THE DRAMA movements. The first consists of a "
     "terrible cursing of the day of his birth and the night of his conception."),
    (True,  "word broken across a line by the scanner",
     "In it there are three move ments. The first consists of a terrible "
     "cursing of the day of his birth and the night of his con ception."),
    (True,  "page number dropped mid-sentence",
     "In it there are three movements. The first consists 222 of a terrible "
     "cursing of the day of his birth and the night of his conception."),
    (False, "one word swapped mid-quote",
     "In it there are three movements. The first consists of a dreadful "
     "cursing of the day of his birth and the night of his conception."),
    (False, "synonym at the end",
     "In it there are three movements. The first consists of a terrible "
     "cursing of the day of his birth and the night of his begetting."),
    (False, "clause reordered",
     "In it there are three movements. The first consists of a cursing "
     "terrible of the day of his birth and the night of his conception."),
    (False, "invented sentence on the same topic",
     "In it there are three movements, each of them mourning the day that "
     "he was born and the night of his conception."),
    (False, "words that all occur in the source, reassembled",
     "The description of the oppressing sorrows consists of a terrible "
     "lamentation over the fact of his preservation and of his birth."),
    (False, "true opening, then a clause the author never wrote",
     "In it there are three movements. The first consists of a terrible "
     "cursing of the day of his birth and the silence of God in heaven."),
]
SELFTEST_SOURCE = (
    "a rather than a description of the oppressing sorrows. in it there are "
    "three THE DRAMA movements. the first consists of a terrible cursing of "
    "the day of his birth and the night of his conception. the second "
    "consists of lamentation over the fact of his preservation."
)


def selftest():
    hay = ocr_fold(norm(SELFTEST_SOURCE))
    bad = 0
    for should_match, label, quote in SELFTEST:
        fr = ocr_fold(norm(quote))
        got = fr in hay or contains_with_gaps(fr, hay) is not None
        ok = got == should_match
        bad += not ok
        print(f"  {'pass' if ok else 'FAIL'}  "
              f"{'accept' if should_match else 'reject':6s}  {label}")
    print(f"\n{'selftest clean' if not bad else str(bad) + ' selftest failure(s)'}")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir", nargs="?")
    ap.add_argument("--selftest", action="store_true",
                    help="check the gap tolerance still refuses reworded quotes")
    ap.add_argument("--source", action="append", default=[],
                    help="plain-text copy of a quoted work (repeatable)")
    ap.add_argument("--heading", default=None,
                    help="only check quotes under ### headings containing this")
    ap.add_argument("--quiet", action="store_true", help="only show problems")
    ap.add_argument("--accept", default=None,
                    help="file of reviewed, accepted deviations (see .citation-accept)")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())
    if not args.book_dir:
        ap.error("give a book dir (or --selftest)")
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
    sources_ocr = {}
    for s in args.source:
        raw = Path(s).read_text(encoding="utf-8", errors="replace")
        sources[Path(s).name] = norm(raw)
        sources_ocr[Path(s).name] = ocr_fold(sources[Path(s).name])
        print(f"source: {Path(s).name} ({len(raw):,} chars)")

    files = sorted(Path(args.book_dir).glob("[0-9]*.md"))
    totals = {"OK": 0, "OK-OCR": 0, "DRIFT": 0, "MISS": 0, "ACCEPT": 0}
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
                # Second pass: same words, scanner noise between them.
                ofrags = [ocr_fold(fr) for fr in frags]
                for name, hay in sources_ocr.items():
                    if all(fr in hay for fr in ofrags if fr):
                        verdict, note = "OK-OCR", f"{name} (matches once scan noise is folded out)"
                        break
            if verdict == "MISS":
                # Third pass: allow a running head spliced into the sentence.
                for name, hay in sources_ocr.items():
                    gaps = [contains_with_gaps(fr, hay) for fr in ofrags if fr]
                    if gaps and all(g is not None for g in gaps):
                        verdict = "OK-OCR"
                        note = (f"{name} (matches with {sum(gaps)} running-head "
                                f"interpolation(s) skipped)")
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

        shown = [r for r in rows if not args.quiet or r[0] not in ("OK", "OK-OCR")]
        if shown:
            print(f"\n{f.name}")
            for verdict, head, quote, note in shown:
                print(f"  {verdict:5s} [{head}] {quote[:72]}")
                if note and verdict not in ("OK", "OK-OCR"):
                    print(f"        {note}")

    print(f"\n{'='*60}\nverbatim OK: {totals['OK']}   OK-OCR: {totals['OK-OCR']}   "
          f"DRIFT: {totals['DRIFT']}   MISS: {totals['MISS']}   "
          f"accepted-deviation: {totals['ACCEPT']}")
    if inline:
        print(f"\nformat: {len(inline)} quote(s) inline the translation as \"English\"（中文）")
        print("        house style puts it on its own line after a bare '>' line")
        for fn, snip in inline[:12]:
            print(f"  {fn}: {snip}")
    sys.exit(1 if (totals["DRIFT"] or totals["MISS"]) else 0)


if __name__ == "__main__":
    main()

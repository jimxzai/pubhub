#!/bin/bash
# driver.sh — build + verify one of this repo's consolidated PDF books.
#
# This is the programmatic "run and observe" harness for a build pipeline
# that has no GUI/server/REPL: the "app" is `pandoc --pdf-engine=xelatex`
# driven by scripts/build-<book>-consolidated.sh, and "interacting with it"
# means building the PDF and checking it actually rendered correctly —
# not just that pandoc exited 0.
#
# Usage:
#   .claude/skills/eat-bible/driver.sh <book-slug> [page-to-screenshot]
#
# <book-slug> must match scripts/build-<book-slug>-consolidated.sh
# Run from the repo root (where scripts/ and output/ live).
#
# Examples verified this session:
#   .claude/skills/eat-bible/driver.sh 1-timothy
#   .claude/skills/eat-bible/driver.sh pastoral-epistles 1

set -uo pipefail

SLUG="${1:-}"
SCREENSHOT_PAGE="${2:-1}"

if [ -z "$SLUG" ]; then
  echo "Usage: $0 <book-slug> [page-to-screenshot]" >&2
  echo "Available books:" >&2
  ls scripts/build-*-consolidated.sh 2>/dev/null | sed -E 's#scripts/build-(.*)-consolidated\.sh#  \1#' >&2
  exit 2
fi

BUILD_SCRIPT="scripts/build-${SLUG}-consolidated.sh"
LOG="/tmp/build-${SLUG}-driver.log"

# Do NOT assume the PDF is output/<slug>-consolidated.pdf — the slug is the
# build script's name, which is not always the output's name (build-gospel-
# consolidated.sh writes gospel-of-john-consolidated.pdf). Read the real path
# out of the build script instead.
PDF=$(sed -nE 's#^OUTPUT_PDF="\$OUTPUT_DIR/(.*)"$#output/\1#p' "$BUILD_SCRIPT" 2>/dev/null | head -1)
[ -n "$PDF" ] || PDF="output/${SLUG}-consolidated.pdf"
LATEX_LOG="${PDF%.pdf}-build.log"

if [ ! -f "$BUILD_SCRIPT" ]; then
  echo "FAIL: no such build script: $BUILD_SCRIPT" >&2
  exit 1
fi

echo "== 1/5 build: $BUILD_SCRIPT =="
bash "$BUILD_SCRIPT" > "$LOG" 2>&1
BUILD_EXIT=$?
echo "  exit code: $BUILD_EXIT"
if [ "$BUILD_EXIT" -ne 0 ]; then
  echo "FAIL: build script exited nonzero. Last 40 log lines:" >&2
  tail -40 "$LOG" >&2
  exit 1
fi

echo "== 2/5 check for missing-glyph warnings =="
# These greps are only as good as what the build script puts in the log.
# pandoc swallows the xelatex log unless it is passed --verbose, so a build
# script that omits it makes every check below pass vacuously. The build
# scripts route their verbose log to output/<book>-build.log and re-echo the
# offending lines here via scripts/lib/latex-check.sh; if that summary is
# absent, this driver is not actually verifying anything.
if ! grep -q "missing-glyph warnings:" "$LOG"; then
  echo "  WARNING: $BUILD_SCRIPT printed no xelatex log summary. It is" >&2
  echo "  probably not passing --verbose to pandoc, in which case steps 2-3" >&2
  echo "  below cannot fail no matter how broken the PDF is. See" >&2
  echo "  scripts/lib/latex-check.sh." >&2
fi
MISSING=$(grep -c "Missing character" "$LOG")
echo "  Missing character warnings: $MISSING"
if [ "$MISSING" -gt 0 ]; then
  echo "FAIL: found glyph warnings — a font is being asked to render a" >&2
  echo "  character it doesn't have (classic cause: CJK text scoped under" >&2
  echo "  a Latin-only font like Baskerville/Menlo). First few:" >&2
  grep "Missing character" "$LOG" | head -5 >&2
  exit 1
fi

echo "== 3/5 check for LaTeX errors =="
LATEX_ERR=$(grep -icE '! LaTeX Error|! Undefined control sequence|! Package .* Error' "$LOG")
echo "  LaTeX error lines: $LATEX_ERR"
if [ "$LATEX_ERR" -gt 0 ]; then
  echo "FAIL: LaTeX reported errors even though pandoc exited 0 (xelatex" >&2
  echo "  can still emit a PDF after a recoverable error). First few:" >&2
  grep -iE '! LaTeX Error|! Undefined control sequence|! Package .* Error' "$LOG" | head -5 >&2
  exit 1
fi

echo "== 3b/5 report overfull boxes (non-fatal) =="
# An overfull \hbox means content printed outside its column or past the text
# block — a Hebrew cell overprinting the column beside it, an appendix box
# bleeding into the margin. It is invisible to every other check here: exit
# code 0, no glyph warnings, no LaTeX error. Reported rather than failed
# because most books in this repo have never been measured for it; treat a
# nonzero count as work to do, not as a passing build.
# Take the count from the build script's own summary line: it re-echoes only
# the first handful of offending lines, so counting them here would cap at
# that limit and understate the damage.
OVERFULL=$(sed -nE 's/^ *overfull-box warnings: +([0-9]+)$/\1/p' "$LOG" | head -1)
[ -n "$OVERFULL" ] || OVERFULL=$(grep -c "Overfull \\\\hbox" "$LOG")
echo "  Overfull \\hbox warnings: $OVERFULL"
if [ "$OVERFULL" -gt 0 ]; then
  grep "Overfull \\\\hbox" "$LOG" | head -5
  echo "  → full list: $LATEX_LOG"
fi

if [ ! -f "$PDF" ]; then
  echo "FAIL: build reported success but $PDF does not exist" >&2
  exit 1
fi

echo "== 4/5 check embedded fonts =="
if ! command -v pdffonts >/dev/null 2>&1; then
  echo "  SKIP: pdffonts not installed (brew install poppler)"
else
  NOT_EMBEDDED=$(pdffonts "$PDF" 2>/dev/null | awk 'NR>2' | grep -vc "yes yes yes" || true)
  PAGES=$(pdfinfo "$PDF" 2>/dev/null | awk -F': *' '/^Pages/{print $2}')
  SIZE=$(du -h "$PDF" | cut -f1)
  echo "  pages: $PAGES   size: $SIZE   fonts not fully embedded: $NOT_EMBEDDED"
  if [ "$NOT_EMBEDDED" -gt 0 ]; then
    echo "FAIL: found a font that isn't embedded/subset — the PDF will not" >&2
    echo "  render correctly on a machine without that font installed." >&2
    pdffonts "$PDF" 2>/dev/null | awk 'NR>2' | grep -v "yes yes yes" >&2
    exit 1
  fi
fi

echo "== 5/5 render page $SCREENSHOT_PAGE to PNG for visual check =="
OUT_PNG="/tmp/${SLUG}-p${SCREENSHOT_PAGE}"
if ! command -v pdftoppm >/dev/null 2>&1; then
  echo "  SKIP: pdftoppm not installed (brew install poppler)"
else
  pdftoppm -png -r 130 -f "$SCREENSHOT_PAGE" -l "$SCREENSHOT_PAGE" "$PDF" "$OUT_PNG"
  PNG_FILE=$(ls "${OUT_PNG}"*.png 2>/dev/null | head -1)
  if [ -n "$PNG_FILE" ]; then
    echo "  wrote: $PNG_FILE"
    echo "  → open/Read this file to actually LOOK at the page. A green exit"
    echo "    code here does not mean the page looks right — missing-glyph"
    echo "    warnings only catch glyphs that don't exist in a font at all,"
    echo "    not glyphs that render as the wrong thing, overflow a box, or"
    echo "    a full-bleed background that doesn't reach the page edge."
    echo "    Bold CJK text specifically can render flat/weak with zero"
    echo "    warnings (BoldFont glyph-fallback bug, see SKILL.md Gotchas) —"
    echo "    on a busy content page this is easy to miss by eye even when"
    echo "    looking for it; if this template's bold is unverified, run"
    echo "    the isolated repro in SKILL.md instead of trusting a glance."
  else
    echo "FAIL: pdftoppm ran but produced no PNG" >&2
    exit 1
  fi
fi

echo ""
echo "PASS: $PDF ($PAGES pages) built and verified clean."

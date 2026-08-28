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
#   .claude/skills/eat-bible/driver.sh <book-slug> --record-baseline
#
# <book-slug> must match scripts/build-<book-slug>-consolidated.sh
# Run from the repo root (where scripts/ and output/ live).
#
# The final step compares this build against baselines.tsv (checked in beside
# this script) and FAILS on a regression — more overfull boxes or more missing
# glyphs than last recorded. Absolute counts alone are useless here: several
# books have carried defects since they were created, so gating on "nonzero"
# would just mean the driver always fails and everyone stops reading it.
# Gating on "worse than before" is what actually catches an edit.
#
# --record-baseline accepts the current numbers as the new reference. Use it
# after deliberately fixing (or knowingly accepting) a change — never to
# silence a regression you haven't looked at.
#
# Examples verified this session:
#   .claude/skills/eat-bible/driver.sh 1-timothy
#   .claude/skills/eat-bible/driver.sh pastoral-epistles 1
#   .claude/skills/eat-bible/driver.sh isaiah --record-baseline

set -uo pipefail

SLUG=""
SCREENSHOT_PAGE=1
RECORD_BASELINE=0
for arg in "$@"; do
  case "$arg" in
    --record-baseline) RECORD_BASELINE=1 ;;
    -*) echo "unknown flag: $arg" >&2; exit 2 ;;
    *) if [ -z "$SLUG" ]; then SLUG="$arg"; else SCREENSHOT_PAGE="$arg"; fi ;;
  esac
done

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
BASELINE_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/baselines.tsv"

if [ ! -f "$BUILD_SCRIPT" ]; then
  echo "FAIL: no such build script: $BUILD_SCRIPT" >&2
  exit 1
fi

echo "== 1/6 build: $BUILD_SCRIPT =="
bash "$BUILD_SCRIPT" > "$LOG" 2>&1
BUILD_EXIT=$?
echo "  exit code: $BUILD_EXIT"
if [ "$BUILD_EXIT" -ne 0 ]; then
  echo "FAIL: build script exited nonzero. Last 40 log lines:" >&2
  tail -40 "$LOG" >&2
  exit 1
fi

echo "== 2/6 check for missing-glyph warnings =="
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

echo "== 3/6 check for LaTeX errors =="
LATEX_ERR=$(grep -icE '! LaTeX Error|! Undefined control sequence|! Package .* Error' "$LOG")
echo "  LaTeX error lines: $LATEX_ERR"
if [ "$LATEX_ERR" -gt 0 ]; then
  echo "FAIL: LaTeX reported errors even though pandoc exited 0 (xelatex" >&2
  echo "  can still emit a PDF after a recoverable error). First few:" >&2
  grep -iE '! LaTeX Error|! Undefined control sequence|! Package .* Error' "$LOG" | head -5 >&2
  exit 1
fi

echo "== 3b/6 report overfull boxes (non-fatal) =="
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

echo "== 4/6 check embedded fonts =="
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

echo "== 5/6 render page $SCREENSHOT_PAGE to PNG for visual check =="
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

echo "== 6/6 compare against baseline =="
BASE_ROW=$(awk -F'\t' -v s="$SLUG" '$1==s {print; exit}' "$BASELINE_FILE" 2>/dev/null)

if [ "$RECORD_BASELINE" -eq 1 ]; then
  # BSD grep has no -P, so drop the existing row with awk on the tab-split
  # first field rather than a regex over the whole line.
  TMP=$(mktemp)
  {
    echo "# slug	pages	missing-glyphs	overfull-boxes	recorded"
    if [ -f "$BASELINE_FILE" ]; then
      awk -F'\t' -v s="$SLUG" '!/^#/ && $1!=s' "$BASELINE_FILE"
    fi
    printf '%s\t%s\t%s\t%s\t%s\n' "$SLUG" "$PAGES" "$MISSING" "$OVERFULL" "$(date +%Y-%m-%d)"
  } > "$TMP"
  { head -1 "$TMP"; tail -n +2 "$TMP" | sort; } > "$BASELINE_FILE"
  rm -f "$TMP"
  echo "  recorded: pages=$PAGES missing=$MISSING overfull=$OVERFULL"
  echo ""
  echo "PASS: $PDF ($PAGES pages) built; baseline updated."
  exit 0
fi

if [ -z "$BASE_ROW" ]; then
  echo "  no baseline for '$SLUG' in $BASELINE_FILE"
  echo "  → re-run with --record-baseline to start tracking this book."
else
  BASE_PAGES=$(echo "$BASE_ROW" | cut -f2)
  BASE_MISSING=$(echo "$BASE_ROW" | cut -f3)
  BASE_OVERFULL=$(echo "$BASE_ROW" | cut -f4)
  BASE_DATE=$(echo "$BASE_ROW" | cut -f5)
  echo "  baseline ($BASE_DATE): pages=$BASE_PAGES missing=$BASE_MISSING overfull=$BASE_OVERFULL"
  echo "  now:                   pages=$PAGES missing=$MISSING overfull=$OVERFULL"

  REGRESSED=0
  if [ "$OVERFULL" -gt "$BASE_OVERFULL" ]; then
    echo "REGRESSION: overfull boxes went $BASE_OVERFULL → $OVERFULL" >&2
    echo "  Something now prints outside its column or past the text block." >&2
    echo "  Diff the new entries in $LATEX_LOG against what you changed." >&2
    REGRESSED=1
  fi
  if [ "$MISSING" -gt "$BASE_MISSING" ]; then
    echo "REGRESSION: missing glyphs went $BASE_MISSING → $MISSING" >&2
    REGRESSED=1
  fi
  if [ "$REGRESSED" -eq 1 ]; then
    exit 1
  fi
  if [ "$OVERFULL" -lt "$BASE_OVERFULL" ]; then
    echo "  improved: overfull $BASE_OVERFULL → $OVERFULL — re-run with"
    echo "  --record-baseline to lock the gain in."
  fi
fi

echo ""
echo "PASS: $PDF ($PAGES pages) built and verified clean."

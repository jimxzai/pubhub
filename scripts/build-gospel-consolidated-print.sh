#!/bin/bash
# Gospel of John — GRAYSCALE PRINT EDITION
# Reuses output/gospel-of-john-consolidated.md produced by
# build-gospel-consolidated.sh, and a grayscale variant of the template:
# every named color collapses to black/gray so the book prints cleanly
# in one ink. Words of Jesus (\jesus) become bold instead of red.

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMBINED_MD="$PROJECT_ROOT/output/gospel-of-john-consolidated.md"
TEMPLATE_SRC="$PROJECT_ROOT/templates/pdf/gospel-of-john.latex"
TEMPLATE_BW="$PROJECT_ROOT/output/.gospel-of-john-print.latex"
OUTPUT_PDF="$PROJECT_ROOT/output/gospel-of-john-consolidated-print.pdf"

if [ ! -f "$COMBINED_MD" ]; then
    echo "❌ $COMBINED_MD not found — run build-gospel-consolidated.sh first"
    exit 1
fi

echo "🖨  Building grayscale print edition..."

# Derive the BW template: collapse colors, embolden Jesus' words.
sed \
  -e 's/\\definecolor{ChapterBlue}{RGB}{[0-9, ]*}/\\definecolor{ChapterBlue}{RGB}{0,0,0}/' \
  -e 's/\\definecolor{ScriptureGold}{RGB}{[0-9, ]*}/\\definecolor{ScriptureGold}{RGB}{60,60,60}/' \
  -e 's/\\definecolor{CommentaryBrown}{RGB}{[0-9, ]*}/\\definecolor{CommentaryBrown}{RGB}{40,40,40}/' \
  -e 's/\\definecolor{JesusRed}{RGB}{[0-9, ]*}/\\definecolor{JesusRed}{RGB}{0,0,0}/' \
  -e 's/\\newcommand{\\jesus}\[1\]{\\textcolor{JesusRed}{#1}}/\\newcommand{\\jesus}[1]{\\textbf{#1}}/' \
  "$TEMPLATE_SRC" > "$TEMPLATE_BW"

pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --pdf-engine=xelatex \
  --template="$TEMPLATE_BW" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter \
  -V tocdepth=0

echo "✅ Print edition: $OUTPUT_PDF ($(du -h "$OUTPUT_PDF" | cut -f1))"

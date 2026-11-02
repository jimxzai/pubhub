#!/bin/bash
# 讀懂聖經的希伯來文 — Reading the Hebrew Old Testament: a first guide for new Bible students
# = preface + order-of-revelation chapter + 13 chapters + appendices (series words, top-100 words, parsing glossary, songs, sources) + afterword
# Data (counts, parse table, grammar tables, song cards) is generated from OSHB by gen-biblehebrew-data.py;
# series vocabulary comes from mine-hebrew-wordstudies.py. Template: templates/pdf/biblehebrew.latex

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/Biblehebrew"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/biblehebrew-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/biblehebrew-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/biblehebrew.latex"

[ -f "$TEMPLATE" ] || { echo "ERROR: Template not found: $TEMPLATE"; exit 1; }
mkdir -p "$OUTPUT_DIR"
python3 "$SCRIPT_DIR/mine-hebrew-wordstudies.py" || { echo "❌ series mining failed"; exit 1; }
python3 "$SCRIPT_DIR/gen-biblehebrew-data.py" || { echo "❌ data generation failed"; exit 1; }
python3 "$SCRIPT_DIR/combine-biblehebrew.py" "$INPUT_DIR" "$COMBINED_MD" || { echo "❌ combine failed"; exit 1; }
# pipe-table separators shorter than --columns compile to unwrappable `l` columns (see eat-bible gotchas)
python3 "$SCRIPT_DIR/widen-table-separators.py" "$COMBINED_MD" >/dev/null 2>&1 || true

source "$SCRIPT_DIR/lib/latex-check.sh"
LATEX_LOG="${OUTPUT_PDF%.pdf}-build.log"
pandoc "$COMBINED_MD" -o "$OUTPUT_PDF" --verbose --pdf-engine=xelatex --template="$TEMPLATE" \
  --from=markdown-superscript-subscript --top-level-division=chapter > "$LATEX_LOG" 2>&1
latex_build_report "$?" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1

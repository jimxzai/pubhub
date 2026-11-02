#!/bin/bash
# 舊約希伯來文彙編 — A Hebrew Companion to the Old Testament Series
# = preface + how-to-use + overview + book-by-book + lemma index + sources + afterword
# Data comes from mine-hebrew-wordstudies.py (the OT books' 原文研讀 tables) and OSHB, via gen-hebrew-compendium.py.
# Template: templates/pdf/hebrew-compendium.latex (derived from biblehebrew.latex <- revelation.latex)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/Biblehebrew-compendium"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/hebrew-compendium-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/hebrew-compendium-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/hebrew-compendium.latex"

[ -f "$TEMPLATE" ] || { echo "ERROR: Template not found: $TEMPLATE"; exit 1; }
mkdir -p "$OUTPUT_DIR"
python3 "$SCRIPT_DIR/mine-hebrew-wordstudies.py" || { echo "❌ series mining failed"; exit 1; }
python3 "$SCRIPT_DIR/gen-hebrew-compendium.py" >/dev/null || { echo "❌ data generation failed"; exit 1; }
python3 "$SCRIPT_DIR/combine-hebrew-compendium.py" "$INPUT_DIR" "$COMBINED_MD" || { echo "❌ combine failed"; exit 1; }
python3 "$SCRIPT_DIR/widen-table-separators.py" "$COMBINED_MD" >/dev/null 2>&1 || true

source "$SCRIPT_DIR/lib/latex-check.sh"
LATEX_LOG="${OUTPUT_PDF%.pdf}-build.log"
pandoc "$COMBINED_MD" -o "$OUTPUT_PDF" --verbose --pdf-engine=xelatex --template="$TEMPLATE" \
  --from=markdown-superscript-subscript --top-level-division=chapter > "$LATEX_LOG" 2>&1
latex_build_report "$?" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1

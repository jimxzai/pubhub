#!/bin/bash

# Psalms Liturgical PDF Builder - 2026 EDITION
# = Overview + five books of the Psalter, each book paired:
#   whole-book deep study (01-05) followed by psalm-by-psalm reception guide (06-10)
# Sources from books/bible/psalm/ (Elder-Huang Christological reading, CUV verified via cnbible.com)
# Uses templates/pdf/psalm-liturgical.latex (8.5×11" Lectern/Ceremonial, gold-border cover)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/psalm"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/psalm-liturgical-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/psalm-liturgical-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/psalm-liturgical.latex"

echo "=========================================="
echo "📖 Psalms Liturgical PDF (2026)"
echo "=========================================="
echo ""
echo "Format: 8.5×11\" Letter (Lectern/Ceremonial)"
echo "Template: psalm-liturgical.latex"
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "詩篇全卷逐篇領受"
subtitle: "The Whole Psalter — Liturgical Edition"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "Soli Deo Gloria"
---

HEADER

# Helper: append a source file with its front matter stripped
append_file() {
    local f="$1"
    echo "  Adding: $(basename "$f")"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$f" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
}

# 1. Overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    append_file "$INPUT_DIR/00-overview.md"
else
    echo "❌ Missing 00-overview.md in $INPUT_DIR — aborting build"
    exit 1
fi

# 2. Five books, each paired: deep study (0N) then psalm-by-psalm guide (0N+5)
file_count=1
for pair in "01 06" "02 07" "03 08" "04 09" "05 10"; do
    for i in $pair; do
        found=""
        for f in "$INPUT_DIR/$i-"*.md; do
            if [ -f "$f" ]; then
                append_file "$f"
                ((file_count++))
                found=1
                break
            fi
        done
        if [ -z "$found" ]; then
            echo "❌ Missing file for prefix '$i-' in $INPUT_DIR — aborting build"
            exit 1
        fi
    done
done

# 3. Historical backgrounds deep-read
if [ -f "$INPUT_DIR/12-backgrounds.md" ]; then
    append_file "$INPUT_DIR/12-backgrounds.md"
    ((file_count++))
fi

# 4. The Life of Christ through the Psalms
if [ -f "$INPUT_DIR/14-christ-through-psalms.md" ]; then
    append_file "$INPUT_DIR/14-christ-through-psalms.md"
    ((file_count++))
fi

# 5. Hebrew poetics primer
if [ -f "$INPUT_DIR/15-hebrew-poetics.md" ]; then
    append_file "$INPUT_DIR/15-hebrew-poetics.md"
    ((file_count++))
fi

# 6. Prayer edition + liturgical use guide
if [ -f "$INPUT_DIR/13-prayer-testimony.md" ]; then
    append_file "$INPUT_DIR/13-prayer-testimony.md"
    ((file_count++))
fi

# 6b. Liturgical use guide (church year, daily hours, responsive reading)
if [ -f "$INPUT_DIR/16-liturgical-use.md" ]; then
    append_file "$INPUT_DIR/16-liturgical-use.md"
    ((file_count++))
fi

# 7. Expositors' voices (Morgan + MacArthur)
if [ -f "$INPUT_DIR/11-voices-morgan-macarthur.md" ]; then
    append_file "$INPUT_DIR/11-voices-morgan-macarthur.md"
    ((file_count++))
fi

# 8. Appendices
for app in 99a-appendix-nt-quotations.md 99b-appendix-pastoral-index-reading-plan.md 99c-appendix-structure-themes.md 99d-appendix-references.md; do
    if [ -f "$INPUT_DIR/$app" ]; then
        append_file "$INPUT_DIR/$app"
        ((file_count++))
    fi
done

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $file_count files)"
echo ""
echo "🔨 Generating PDF with psalm-liturgical.latex template..."

pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter \
  -V tocdepth=0

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ PDF generated: $OUTPUT_PDF ($(du -h "$OUTPUT_PDF" | cut -f1))"
else
    echo "❌ PDF generation failed"
    exit 1
fi

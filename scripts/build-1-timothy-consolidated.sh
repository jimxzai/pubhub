#!/bin/bash

# 1 Timothy PDF Builder - CONSOLIDATED 2026 EDITION
# = Overview + 6 per-chapter files + references appendix
# Sources from books/bible/pauline-epistles/1-timothy/
# Uses templates/pdf/1-timothy.latex (Teal/Gold Pillar theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/pauline-epistles/1-timothy"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
INDICES_FILE="$INPUT_DIR/98-appendix-indices.md"
REFS_FILE="$INPUT_DIR/99-appendix-references.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/1-timothy-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/1-timothy-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/1-timothy.latex"

echo "=========================================="
echo "📖 1 Timothy PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "提摩太前書研讀"
subtitle: "1 Timothy Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老 Thursday 查經班筆記** — 2024-2025 原始查經筆記

  • **John MacArthur** — 逐節解經傳統

  • **G. Campbell Morgan** — 教牧書信解經傳統

  All rights reserved.
---

HEADER

# 1. Overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 2. Elder Wong systematic reception (structure-based deep study)
#    Demote headings one level so the whole study is a single top-level chapter
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——黃長老查經法 (Systematic Reception)\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 3. All 6 chapters in order
chapter_count=0
for i in 01 02 03 04 05 06; do
    found=""
    for f in "$INPUT_DIR/$i-"*.md; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            tail -n +8 "$f" | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
            printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
            ((chapter_count++))
            found=1
            break
        fi
    done
    if [ -z "$found" ]; then
        echo "❌ Missing chapter file for prefix '$i-' in $INPUT_DIR — aborting build"
        exit 1
    fi
done

# 4. Scripture & theme indices appendix
if [ -f "$INDICES_FILE" ]; then
    echo "  Adding: 98-appendix-indices.md"
    tail -n +8 "$INDICES_FILE" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 5. References appendix
if [ -f "$REFS_FILE" ]; then
    echo "  Adding: 99-appendix-references.md"
    tail -n +8 "$REFS_FILE" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters + overview + references)"
echo ""
echo "🔨 Generating PDF with 1-timothy.latex template..."
echo "   (\\paul{...} speaker tags pass through as raw LaTeX; \\newcommand{\\paul} is defined in the template)"

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

#!/bin/bash

# 2 Timothy PDF Builder - CONSOLIDATED 2026 EDITION
# = Overview + 4 chapters + references appendix
# Sources from books/bible/pauline-epistles/2-timothy/ (Elder Wong Thursday notes + MacArthur + Morgan)
# Uses templates/pdf/2-timothy.latex (Crimson/Gold Soldier's Legacy theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/pauline-epistles/2-timothy"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
INDICES_FILE="$INPUT_DIR/98-appendix-indices.md"
REFS_FILE="$INPUT_DIR/99-appendix-references.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/2-timothy-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/2-timothy-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/2-timothy.latex"

echo "=========================================="
echo "📖 2 Timothy PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "提摩太後書研讀"
subtitle: "2 Timothy Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老 Thursday 查經筆記** — 真實的「盡職四大點」服事框架（2024-2025年查經筆記）

  • **John MacArthur** — 逐節解經講道 (gty.org)

  • **G. Campbell Morgan** — 屬靈組織分析

  All rights reserved.
---

HEADER

# 1. Overview (strip its own front matter block: two '---' lines)
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

# 3. All 4 chapters in order
chapter_count=0
for i in 01 02 03 04; do
    found=""
    for f in "$INPUT_DIR/$i-"*.md; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            tail -n +8 "$f" | sed 's/\^\([^\^]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
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
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INDICES_FILE" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 5. References appendix
if [ -f "$REFS_FILE" ]; then
    echo "  Adding: 99-appendix-references.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$REFS_FILE" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters + overview + references)"
echo ""
echo "🔨 Generating PDF with 2-timothy.latex template..."

# --verbose is load-bearing, not chatter: without it pandoc swallows the whole
# xelatex log and every grep-the-log check below (and in driver.sh) passes
# vacuously. See scripts/lib/latex-check.sh for the full explanation.
source "$SCRIPT_DIR/lib/latex-check.sh"
LATEX_LOG="${OUTPUT_PDF%.pdf}-build.log"
pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --verbose \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter \
  -V tocdepth=0 > "$LATEX_LOG" 2>&1
PANDOC_EXIT=$?

latex_build_report "$PANDOC_EXIT" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1

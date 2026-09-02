#!/bin/bash

# Genesis PDF Builder - 2026 EDITION
# 16 chapters covering Genesis 1-50 (Creation through Jacob's Blessings)
# Uses the dedicated template: templates/pdf/genesis.latex

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/genesis"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/genesis-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/genesis.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/genesis.latex"

echo "=========================================="
echo "📖 Genesis PDF (2026 EDITION)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "創世記研讀"
subtitle: "Genesis Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老查經法** — 整本聖經脈絡的深度領受，以約翰福音1:1-18與希伯來書為理解創世記的鑰匙

  • **John MacArthur** — 逐節解經講道 (gty.org)

  • **G. Campbell Morgan** — 解經王子 (*The Analyzed Bible*)

  **起初的道——創造萬有的主，也是後來道成肉身的主**

  「太初有道，道與神同在，道就是神……萬物是藉著他造的。」——約翰福音 1:1,3

  All rights reserved.
---

HEADER

# 1. Overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    tail -n +8 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 2. All 17 chapters in order
chapter_count=0
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17; do
    for f in "$INPUT_DIR/$i-"*.md; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            tail -n +8 "$f" | sed 's/\^\([0-9:]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
            printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
            ((chapter_count++))
            break
        fi
    done
done

# 3. Appendices (99a-99i), in order
appendix_count=0
for i in 99a 99b 99c 99d 99e 99f 99g 99h 99i; do
    for f in "$INPUT_DIR/$i-"*.md; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            tail -n +8 "$f" | sed 's/\^\([0-9:]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
            printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
            ((appendix_count++))
            break
        fi
    done
done

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters, $appendix_count appendices)"
echo ""
echo "🔨 Generating PDF with dedicated template (genesis.latex)..."

# --verbose is load-bearing, not chatter: without it pandoc swallows the whole
# xelatex log and every grep-the-log check (and in driver.sh) passes vacuously.
# See scripts/lib/latex-check.sh for the full explanation.
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

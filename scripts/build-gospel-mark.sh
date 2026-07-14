#!/bin/bash

# Gospel of Mark PDF Builder - 2026 EDITION
# 20 chapter files across 4 parts (Prologue, Galilean Ministry, Journey to Jerusalem, Passion & Resurrection)
# Uses the dedicated template: templates/pdf/gospel-of-mark.latex

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-mark"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-mark-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-mark.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-mark.latex"

echo "=========================================="
echo "📖 Gospel of Mark PDF (2026 EDITION)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "馬可福音研讀"
subtitle: "Gospel of Mark Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老查經法** — 整本聖經脈絡的深度領受

  • **John MacArthur** — 逐節解經講道 (gty.org)

  • **G. Campbell Morgan** — 解經王子 (*The Gospel According to Mark*, 1927)

  **僕人基督——服事者的典範**

  「因為人子來，並不是要受人的服事，乃是要服事人，並且要捨命作多人的贖價。」——馬可福音 10:45

  All rights reserved.
---

HEADER

# 1. Overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    tail -n +8 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 1b. Systematic Reception chapter (全書領受總綱)
if [ -f "$INPUT_DIR/00b-systematic-reception.md" ]; then
    echo "  Adding: 00b-systematic-reception.md"
    tail -n +8 "$INPUT_DIR/00b-systematic-reception.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 2. All 20 chapters in canonical order
chapter_count=0
for i in 01a 01b 01c 01d 02 03 04 05 06 07 08a 08b 09 10 11 12 13 14 15 16; do
    for f in "$INPUT_DIR/$i-"*.md; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            tail -n +8 "$f" | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
            printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
            ((chapter_count++))
            break
        fi
    done
done

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""

# Convert red letter markers for Jesus's words
echo "Converting red letter markers..."
sed -i.bak \
    -e 's/<red>/\\jesus{/g' \
    -e 's/<\/red>/}/g' \
    "$COMBINED_MD"
rm -f "${COMBINED_MD}.bak" 2>/dev/null || true

echo "🔨 Generating PDF with dedicated template (gospel-of-mark.latex)..."

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

#!/bin/bash

# Gospel of John PDF Builder - NIV Version
# Uses NIV (New International Version) for English Scripture

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-john-niv"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-john-niv-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-john-niv.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-john-original.latex"

echo "=========================================="
echo "📖 Gospel of John PDF Generator (NIV)"
echo "=========================================="
echo "English Scripture: New International Version"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Combine all markdown files
echo "📝 Combining ALL chapters..."
cat > "$COMBINED_MD" << 'HEADER'
---
title: "約翰福音研讀"
subtitle: "Gospel of John Deep Study (NIV)"
author: "PubHub 三書精讀系統"
date: "2026年1月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 解經王子 (1909)

  **English Scripture: NIV (New International Version)**

  **榮耀 = 恩典 + 真理**

  七個神蹟 (works) 彰顯恩典 | 七個「我是」(words) 彰顯真理

  Scripture quotations marked NIV are taken from the Holy Bible,
  New International Version®, NIV®.
  Copyright © 1973, 1978, 1984, 2011 by Biblica, Inc.™
  Used by permission of Zondervan. All rights reserved worldwide.
---

HEADER

# Add overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    tail -n +2 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# Add all chapters
chapter_count=0
for i in 01 01b 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21; do
    chapter_file="$INPUT_DIR/$i-"*.md
    for f in $chapter_file; do
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
echo "✅ Combined markdown created"
echo "   Chapters: $chapter_count"
echo ""

# Generate PDF
echo "🔨 Generating PDF..."
pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter \
  -V tocdepth=0 \
  2>&1 | grep -v "^$" | head -20

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ NIV PDF Generated Successfully!"
    echo "=========================================="
    echo ""
    echo "📄 Output: $OUTPUT_PDF"
    echo "📊 Size: $(du -h "$OUTPUT_PDF" | cut -f1)"
    echo ""
    echo "To open:"
    echo "  open \"$OUTPUT_PDF\""
else
    echo "❌ PDF generation failed"
    exit 1
fi

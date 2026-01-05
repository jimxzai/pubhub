#!/bin/bash

# Gospel of John PDF Builder - Professional 2026 Template
# Uses the new professional template with emoji, numbered elements, glossary support

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-john"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-john-professional-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-john-professional.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-professional-2026.latex"

echo "=========================================="
echo "📖 Gospel of John PDF Generator"
echo "   Professional 2026 Template"
echo "=========================================="
echo "Template: gospel-professional-2026.latex"
echo "Features: Emoji, Numbered Elements, Glossary"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check if template exists
if [ ! -f "$TEMPLATE" ]; then
    echo "❌ Template not found: $TEMPLATE"
    exit 1
fi

# Combine all markdown files
echo "📝 Combining ALL chapters..."
cat > "$COMBINED_MD" << 'HEADER'
---
title: "約翰福音研讀"
subtitle: "Gospel of John Deep Study (ESV)"
author: "PubHub 三書精讀系統"
date: "2026年1月"
publisher: "三書精讀出版系統"
lof: false
lot: false
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 解經王子 (1909)

  **English Scripture: ESV (English Standard Version)**

  **榮耀 = 恩典 + 真理**

  七個神蹟 (works) 彰顯恩典 | 七個「我是」(words) 彰顯真理

  Scripture quotations are from The ESV® Bible (The Holy Bible,
  English Standard Version®), copyright © 2001 by Crossway,
  a publishing ministry of Good News Publishers.
  Used by permission. All rights reserved.
---

HEADER

# Add overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    tail -n +2 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# Add all chapters in order
chapter_count=0
for i in 01 01b 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21; do
    chapter_file="$INPUT_DIR/$i-"*.md
    for f in $chapter_file; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            # Skip YAML frontmatter (lines 1-7) and convert superscripts
            tail -n +8 "$f" | sed 's/\^\\([0-9]*\\)\^/\\textsuperscript{\\1}/g' >> "$COMBINED_MD"
            printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
            ((chapter_count++))
            break
        fi
    done
done

echo ""
echo "✅ Combined markdown created"
echo "   Chapters: $chapter_count"
echo "   Lines: $(wc -l < "$COMBINED_MD")"
echo ""

# Generate PDF using professional template
echo "🔨 Generating PDF with Professional 2026 template..."
echo ""

pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter \
  -V tocdepth=0 \
  2>&1 | grep -v "^$" | head -30

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Professional PDF Generated Successfully!"
    echo "=========================================="
    echo ""
    echo "📄 Output: $OUTPUT_PDF"
    echo "📊 Size: $(du -h "$OUTPUT_PDF" | cut -f1)"
    echo "📑 Chapters: $chapter_count"
    echo ""
    echo "Professional 2026 Features:"
    echo "  ✓ Emoji font support (Apple Color Emoji)"
    echo "  ✓ Numbered figures (圖 Figure X.Y)"
    echo "  ✓ Numbered tables (表 Table X.Y)"
    echo "  ✓ Numbered notes (註 Note X.Y)"
    echo "  ✓ Scripture/Greek/Application boxes"
    echo "  ✓ Red Letter Bible support"
    echo "  ✓ Professional 7×10 inch format"
    echo ""
    echo "To open:"
    echo "  open \"$OUTPUT_PDF\""
else
    echo ""
    echo "❌ PDF generation failed"
    echo "Check the error messages above"
    exit 1
fi

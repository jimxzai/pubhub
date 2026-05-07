#!/bin/bash

# Gospel of John PDF Builder - PREMIUM VERSION
# Uses custom Gospel-themed LaTeX template (fontspec + XeLaTeX, NO xeCJK)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-john"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-john-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-john-premium.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-john-simple.latex"

echo "=========================================="
echo "📖 Gospel of John PDF Generator (PREMIUM)"
echo "=========================================="
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Combine all markdown files
echo "📝 Combining markdown files..."
cat > "$COMBINED_MD" << 'HEADER'
---
title: "約翰福音研讀"
subtitle: "Gospel of John Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年1月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Jim Xiao

  **三大核心資源整合：**

  • **黃長老週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 解經王子 (1909)

  **榮耀 = 恩典 + 真理**

  七個神蹟 (works) 彰顯恩典 | 七個「我是」(words) 彰顯真理

  All rights reserved.
---

HEADER

# Add overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    echo "" >> "$COMBINED_MD"
    tail -n +2 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# Add all chapter files in order (01-21)
chapter_count=0
for i in {01..21}; do
    chapter_file=$(ls "$INPUT_DIR/$i-"*.md 2>/dev/null | head -1)
    if [ -f "$chapter_file" ]; then
        echo "  Adding: $(basename "$chapter_file")"
        cat "$chapter_file" >> "$COMBINED_MD"
        printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
        ((chapter_count++))
    fi
done

echo ""
echo "✅ Combined markdown created"
echo "   Chapters: $chapter_count"
echo "   Lines: $(wc -l < "$COMBINED_MD")"
echo ""

# Generate PDF using custom Gospel of John premium template
echo "🔨 Generating Premium PDF with XeLaTeX..."
echo "   Template: gospel-john-simple.latex"
echo ""

pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --toc \
  --toc-depth=2 \
  --number-sections \
  2>&1 | grep -v "^$" | head -20

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Premium PDF Generated Successfully!"
    echo "=========================================="
    echo ""
    echo "📄 Output: $OUTPUT_PDF"
    echo "📊 Size: $(du -h "$OUTPUT_PDF" | cut -f1)"
    echo "📑 Chapters: $chapter_count"
    echo "📏 Pages: ~$(echo "scale=0; $(wc -l < "$COMBINED_MD") / 50" | bc)"
    echo ""
    echo "Features:"
    echo "  ✓ Gospel-themed colors (Gold, Blue, Green)"
    echo "  ✓ Premium typography (Songti SC, Kaiti SC)"
    echo "  ✓ Professional layout (6×9 inches)"
    echo "  ✓ Decorative chapter headers"
    echo "  ✓ Scripture quotation styling"
    echo "  ✓ Bilingual support (繁中 + English)"
    echo ""
    echo "To open:"
    echo "  open \"$OUTPUT_PDF\""
    echo ""
else
    echo ""
    echo "❌ PDF generation failed"
    echo "Check the error messages above"
    exit 1
fi

#!/bin/bash

# Basic Gospel of John PDF Builder
# Uses simpler LaTeX without CJK dependencies

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-john"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-john-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-john.pdf"

echo "========================================="
echo "📖 Gospel of John PDF Generator (Basic)"
echo "========================================="
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Combine all markdown files
echo "📝 Combining markdown files..."
cat > "$COMBINED_MD" << 'HEADER'
---
title: "約翰福音研讀 Gospel of John Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年1月 January 2026"
---

# 約翰福音研讀 (Gospel of John Deep Study)

**Author**: PubHub 三書精讀系統
**Date**: 2026年1月 (January 2026)
**Status**: MVP Complete - All 21 Chapters

---

HEADER

# Add overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "" >> "$COMBINED_MD"
    echo "---" >> "$COMBINED_MD"
    echo "" >> "$COMBINED_MD"
    tail -n +2 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
fi

# Add all chapter files in order
for i in {01..21}; do
    chapter_file=$(ls "$INPUT_DIR/$i-"*.md 2>/dev/null | head -1)
    if [ -f "$chapter_file" ]; then
        echo "   Adding: $(basename "$chapter_file")"
        echo "" >> "$COMBINED_MD"
        echo "---" >> "$COMBINED_MD"
        echo "" >> "$COMBINED_MD"
        tail -n +2 "$chapter_file" >> "$COMBINED_MD"
    fi
done

echo ""
echo "✅ Combined markdown: $(basename "$COMBINED_MD")"
echo "   Size: $(wc -l < "$COMBINED_MD") lines"
echo ""

# Generate PDF using basic template
echo "🔨 Generating PDF..."
echo ""

pandoc "$COMBINED_MD" \
    -o "$OUTPUT_PDF" \
    --pdf-engine=pdflatex \
    --toc \
    --toc-depth=2 \
    --number-sections \
    -V geometry:margin=2.5cm \
    -V documentclass=book \
    -V papersize=a4 \
    -V fontsize=11pt \
    -V linkcolor=blue \
    2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "✅ PDF Generated Successfully!"
    echo "========================================="
    echo ""
    echo "📄 File: $OUTPUT_PDF"
    echo "📊 Size: $(du -h "$OUTPUT_PDF" | cut -f1)"
    echo "📝 Pages: Approximately $(echo "scale=0; $(wc -l < "$COMBINED_MD") / 50" | bc)"
    echo ""
    echo "To view:"
    echo "  open \"$OUTPUT_PDF\""
    echo ""
else
    echo ""
    echo "❌ PDF generation failed"
    exit 1
fi

#!/bin/bash

# Simple Gospel of John PDF Builder
# Generates a clean PDF without complex LaTeX dependencies

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-john"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-john-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-john.pdf"

echo "========================================="
echo "📖 Gospel of John PDF Generator"
echo "========================================="
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
documentclass: book
papersize: a4
fontsize: 12pt
geometry: margin=2.5cm
mainfont: "PingFang SC"
CJKmainfont: "PingFang SC"
monofont: "Menlo"
linkcolor: blue
toc: true
toc-depth: 2
---

HEADER

# Add overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "" >> "$COMBINED_MD"
    echo "\\newpage" >> "$COMBINED_MD"
    echo "" >> "$COMBINED_MD"
    tail -n +2 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
fi

# Add all chapter files in order
for i in {01..21}; do
    chapter_file=$(ls "$INPUT_DIR/$i-"*.md 2>/dev/null | head -1)
    if [ -f "$chapter_file" ]; then
        echo "   Adding: $(basename "$chapter_file")"
        echo "" >> "$COMBINED_MD"
        echo "\\newpage" >> "$COMBINED_MD"
        echo "" >> "$COMBINED_MD"
        tail -n +2 "$chapter_file" >> "$COMBINED_MD"
    fi
done

echo ""
echo "✅ Combined markdown created: $(basename "$COMBINED_MD")"
echo ""

# Generate PDF
echo "🔨 Generating PDF with XeLaTeX..."
echo ""

pandoc "$COMBINED_MD" \
    -o "$OUTPUT_PDF" \
    --pdf-engine=xelatex \
    --pdf-engine-opt=-interaction=nonstopmode \
    --toc \
    --toc-depth=2 \
    --number-sections \
    -V CJKmainfont="PingFang SC" \
    -V mainfont="PingFang SC" \
    -V monofont="Menlo" \
    -V geometry:margin=2.5cm \
    -V documentclass=book \
    -V papersize=a4 \
    -V fontsize=12pt \
    2>&1 | grep -v "^$"

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "✅ PDF Generated Successfully!"
    echo "========================================="
    echo ""
    echo "📄 Output: $OUTPUT_PDF"
    echo "📊 Size: $(du -h "$OUTPUT_PDF" | cut -f1)"
    echo ""
    echo "To open:"
    echo "  open $OUTPUT_PDF"
    echo ""
else
    echo ""
    echo "❌ PDF generation failed"
    echo "Check the error messages above"
    exit 1
fi

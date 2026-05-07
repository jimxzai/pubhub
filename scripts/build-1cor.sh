#!/bin/bash
# ============================================================================
# 1 Corinthians PDF Builder
# 哥林多前書研讀 - First Corinthians Study
# 7×10" Professional Bible Study Format
# Theme: Holy Spirit's Five-Fold Work + Resurrection Hope
# Uses the 1cor.latex template
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/1cor"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/1cor-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/1cor.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/1cor.latex"

echo "============================================"
echo "1 Corinthians PDF Generator"
echo "哥林多前書研讀"
echo "First Corinthians Study"
echo "============================================"
echo ""
echo "Format: 7×10\" Professional Bible Study"
echo "Template: 1cor.latex"
echo "Theme: Holy Spirit's Five-Fold Work"
echo ""

# Verify template exists
if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Combine all markdown files
echo "Combining chapters..."
cat > "$COMBINED_MD" << 'HEADER'
---
title: "哥林多前書研讀"
subtitle: "First Corinthians - The Holy Spirit's Five-Fold Work"
author: "PubHub 三書精讀系統"
date: "2026年1月"
publisher: "Soli Deo Gloria"
---

HEADER

# Add overview (convert # to ## to avoid chapter numbering)
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md (as front matter)"
    awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$INPUT_DIR/00-overview.md" \
        | sed 's/^# /## /' \
        | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
fi

# Add all chapters in order (01-16)
chapter_count=0
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16; do
    chapter_file="$INPUT_DIR/ch$i.md"
    if [ -f "$chapter_file" ]; then
        echo "  Adding: ch$i.md"
        # Skip YAML frontmatter and convert verse superscripts
        awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$chapter_file" \
            | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
        printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
        ((chapter_count++))
    else
        echo "  WARNING: Missing ch$i.md"
    fi
done

echo ""
echo "Combined markdown created"
echo "   Chapters: $chapter_count"
echo "   Lines: $(wc -l < "$COMBINED_MD")"
echo ""

# Convert emojis to text equivalents for PDF
echo "Converting emojis to text..."
sed -i '' \
    -e 's/📖/(Book)/g' \
    -e 's/🙏/(Prayer)/g' \
    -e 's/💡/(Insight)/g' \
    -e 's/✝️/(Cross)/g' \
    -e 's/🕊️/(Dove)/g' \
    -e 's/⭐/(Star)/g' \
    -e 's/🌟/(Star)/g' \
    -e 's/❤️/(Heart)/g' \
    -e 's/💖/(Heart)/g' \
    -e 's/🔑/(Key)/g' \
    -e 's/🎯/(Target)/g' \
    -e 's/📝/(Note)/g' \
    -e 's/✅/(Check)/g' \
    -e 's/❌/(X)/g' \
    -e 's/🤖/(AI)/g' \
    -e 's/🌙/(Moon)/g' \
    -e 's/☀️/(Sun)/g' \
    -e 's/🌊/(Wave)/g' \
    -e 's/🍞/(Bread)/g' \
    -e 's/🍷/(Wine)/g' \
    -e 's/🏛️/(Temple)/g' \
    -e 's/⛪/(Church)/g' \
    -e 's/🗣️/(Speaking)/g' \
    -e 's/👁️/(Eye)/g' \
    -e 's/🐑/(Sheep)/g' \
    -e 's/🍇/(Grapes)/g' \
    -e 's/✓/+/g' \
    -e 's/→/->/g' \
    "$COMBINED_MD"

# Convert red letter markers for Jesus's words
echo "Converting red letter markers..."
sed -i '' \
    -e 's/<red>/\\jesus{/g' \
    -e 's/<\/red>/}/g' \
    "$COMBINED_MD"

# Generate PDF
echo "Generating PDF with XeLaTeX..."
echo ""

pandoc "$COMBINED_MD" \
    -o "$OUTPUT_PDF" \
    --pdf-engine=xelatex \
    --template="$TEMPLATE" \
    --from=markdown-superscript-subscript \
    --toc \
    --toc-depth=2 \
    --top-level-division=chapter

if [ -f "$OUTPUT_PDF" ]; then
    SIZE=$(ls -lh "$OUTPUT_PDF" | awk '{print $5}')
    PAGES=$(pdfinfo "$OUTPUT_PDF" 2>/dev/null | grep Pages | awk '{print $2}' || echo "unknown")
    echo ""
    echo "============================================"
    echo "SUCCESS: 1 Corinthians PDF Generated!"
    echo "============================================"
    echo ""
    echo "   Title: 哥林多前書研讀"
    echo "   Format: 7×10\" Professional Bible Study"
    echo "   File: $OUTPUT_PDF"
    echo "   Size: $SIZE"
    echo "   Pages: $PAGES"
    echo "   Chapters: $chapter_count"
    echo ""
    echo "   Key Themes:"
    echo "   - Holy Spirit's Five-Fold Work"
    echo "   - Wisdom (Ch 1-4)"
    echo "   - Holiness (Ch 5-6)"
    echo "   - Freedom (Ch 7-10)"
    echo "   - Gifts (Ch 11-14)"
    echo "   - Hope/Resurrection (Ch 15-16)"
    echo "============================================"
    echo ""

    # Open the PDF
    if command -v open &> /dev/null; then
        echo "Opening PDF..."
        open "$OUTPUT_PDF"
    fi
else
    echo "FAILED: PDF not created"
    exit 1
fi

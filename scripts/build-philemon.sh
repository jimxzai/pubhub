#!/bin/bash
# ============================================================================
# Philemon PDF Builder
# 腓利門書研讀 - Three Books Deep Reading Edition
# 8.5×11" Professional Bible Study Format
# Theme: Grace, Redemption, Reconciliation
# Uses the philemon-study.latex template
# ============================================================================

set -e

# Add TeX Live to PATH
export PATH="/Library/TeX/texbin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/1philimon"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/philemon-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/philemon.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/philemon-study.latex"

echo "============================================"
echo "Philemon PDF Generator"
echo "腓利門書研讀"
echo "Three Books Deep Reading Edition"
echo "============================================"
echo ""
echo "Format: 8.5×11\" Professional Bible Study"
echo "Template: philemon-study.latex"
echo "Theme: Grace, Redemption, Reconciliation"
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
title: "腓利門書研讀"
subtitle: "Philemon: The Embrace of Grace - Three Books Deep Reading Edition"
author: "PubHub 三書精讀系統"
date: "2026年2月"
publisher: "Soli Deo Gloria"
---

HEADER

# Add dedication (if exists) - convert # to ## to avoid chapter numbering
if [ -f "$INPUT_DIR/dedication.md" ]; then
    echo "  Adding: dedication.md (as front matter)"
    awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$INPUT_DIR/dedication.md" \
        | sed 's/^# /## /' \
        | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
fi

# Add preface (if exists) - convert # to ## to avoid chapter numbering
if [ -f "$INPUT_DIR/preface.md" ]; then
    echo "  Adding: preface.md (as front matter)"
    awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$INPUT_DIR/preface.md" \
        | sed 's/^# /## /' \
        | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
fi

# Introduction merged into preface.md - skip separate introduction.md

# Add overview (convert # to ## to avoid chapter numbering)
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md (as front matter)"
    awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$INPUT_DIR/00-overview.md" \
        | sed 's/^# /## /' \
        | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
fi

# Add all chapters in order (01-19)
chapter_count=0
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19; do
    chapter_file="$INPUT_DIR/ch$i-"*.md
    for f in $chapter_file; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$f" \
                | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' \
                | sed 's/^## [一二三四五六七八九十][一二三四五六七八九十]*、/## /' \
                | sed 's/^### [0-9][0-9]*\.[0-9][0-9]* /### /' \
                | sed 's/^### [0-9][0-9]*\. /### /' \
                | sed 's/^### [一二三四五六七八九十][一二三四五六七八九十]*、/### /' >> "$COMBINED_MD"
            printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
            ((chapter_count++))
            break
        fi
    done
done

# Add study guide
if [ -f "$INPUT_DIR/study-guide.md" ]; then
    echo "  Adding: study-guide.md"
    awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$INPUT_DIR/study-guide.md" \
        | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
fi

# Add outline (deep study materials) - convert top-level headers to avoid chapter numbering issues
if [ -f "$INPUT_DIR/outline.md" ]; then
    echo "  Adding: outline.md (深度研讀材料)"
    printf '\n\n# 深度研讀材料\n**Deep Study Materials: Literary Analysis and Theological Reflection**\n\n' >> "$COMBINED_MD"
    awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$INPUT_DIR/outline.md" \
        | sed 's/^# /## /' \
        | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
fi

# Add appendices in order
appendix_count=0
for i in 01 02 03 04 05 06 07 08 09; do
    appendix_file="$INPUT_DIR/appendix-$i-"*.md
    for f in $appendix_file; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$f" \
                | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
            printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
            ((appendix_count++))
            break
        fi
    done
done

# Add index (if exists)
if [ -f "$INPUT_DIR/index.md" ]; then
    echo "  Adding: index.md"
    awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$INPUT_DIR/index.md" \
        | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
fi

echo ""
echo "Combined markdown created"
echo "   Chapters: $chapter_count"
echo "   Appendices: $appendix_count"
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

# Replace section dividers (---) with decorative cross dividers
echo "Converting section dividers..."
awk 'NR<=10{print;next} /^---$/{print ""; print "```{=latex}"; print "\\sectiondiv"; print "```"; print ""; next} {print}' "$COMBINED_MD" > "${COMBINED_MD}.tmp" && mv "${COMBINED_MD}.tmp" "$COMBINED_MD"

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
    echo "SUCCESS: Philemon PDF Generated!"
    echo "============================================"
    echo ""
    echo "   Title: 腓利門書研讀"
    echo "   Format: 8.5×11\" Professional Bible Study"
    echo "   File: $OUTPUT_PDF"
    echo "   Size: $SIZE"
    echo "   Pages: $PAGES"
    echo "   Chapters: $chapter_count"
    echo "   Appendices: $appendix_count"
    echo ""
    echo "   Three Books Features:"
    echo "   - 聖經經卷: 腓利門書 (Philemon)"
    echo "   - 世界文學: 悲慘世界 + 復活"
    echo "   - 生命實踐: 18週讀書會指南"
    echo "   - 希臘原文詞彙研究"
    echo "   - 中英雙語對照"
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

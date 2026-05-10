#!/bin/bash
# ============================================================================
# Gospel Harmony PDF Builder - Liturgical Premium Edition (2026)
# 耶穌基督完整生平 - The Complete Life of Jesus Christ
# 8.5×11" Letter Size for Lectern/Ceremonial Use
# Large Print + Red Letter Bible + Liturgical Diagrams
# Uses the gospel-harmony-liturgical.latex template
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-harmony"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-harmony-liturgical-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-harmony-liturgical.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-harmony-liturgical.latex"

echo "============================================"
echo "Gospel Harmony PDF Generator - Liturgical Edition"
echo "耶穌基督完整生平"
echo "The Complete Life of Jesus Christ"
echo "============================================"
echo ""
echo "Format: 8.5×11\" Letter (Lectern/Ceremonial)"
echo "Template: gospel-harmony-liturgical.latex"
echo "Features: Large Print, Liturgical Year Wheel, Red Letter Bible"
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
title: "耶穌基督完整生平"
subtitle: "The Complete Life of Jesus Christ - A Gospel Harmony (Liturgical Edition)"
author: "PubHub 三書精讀系統"
date: "2026年1月"
publisher: "Soli Deo Gloria"
---

HEADER

# Add overview (convert # to ## to avoid chapter numbering)
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md (as front matter)"
    awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$INPUT_DIR/00-overview.md" \
        | sed 's/^# /## /' >> "$COMBINED_MD"
    printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
fi

# Add prologue (convert # to ## to avoid chapter numbering)
if [ -f "$INPUT_DIR/00-prologue-logos.md" ]; then
    echo "  Adding: 00-prologue-logos.md (as front matter)"
    awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$INPUT_DIR/00-prologue-logos.md" \
        | sed 's/^# /## /' \
        | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
fi

# Add all chapters in order (01-37)
chapter_count=0
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37; do
    chapter_file="$INPUT_DIR/$i-"*.md
    for f in $chapter_file; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            # Skip YAML frontmatter and convert verse superscripts
            awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$f" \
                | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
            printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
            chapter_count=$((chapter_count + 1))
            break  # Only process first match
        fi
    done
done

echo ""
echo "Combined markdown created"
echo "   Chapters: $chapter_count"
echo "   Lines: $(wc -l < "$COMBINED_MD")"
echo ""

# Convert red letter markers for Jesus's words
echo "Converting red letter markers..."
sed -i.bak \
    -e 's/<red>/\\jesus{/g' \
    -e 's/<\/red>/}/g' \
    "$COMBINED_MD"

# Convert emojis to text equivalents for PDF
echo "Converting emojis to text..."
sed -i.bak \
    -e 's/🦁/獅/g' \
    -e 's/🐂/牛/g' \
    -e 's/👤/人/g' \
    -e 's/🦅/鷹/g' \
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
    "$COMBINED_MD"

# Clean up sed backup files (cross-platform sed -i.bak workaround)
rm -f "${COMBINED_MD}.bak" 2>/dev/null || true

# Linux-only workaround: substitute problematic CJK punctuation with ASCII equivalents
# This is needed because Linux font stack (Droid Sans Fallback + DejaVu) has gaps in
# Halfwidth/Fullwidth Forms transitions, especially in bold/italic contexts where
# only regular-weight CJK font is available. Mac builds with Songti SC don't need this.
if command -v fc-list &> /dev/null && ! fc-list 2>/dev/null | grep -qi "Songti SC"; then
    echo "Substituting full-width punctuation for Linux build..."
    sed -i.bak \
        -e 's/）/)/g' \
        -e 's/（/(/g' \
        -e 's/，/,/g' \
        -e 's/。/. /g' \
        -e 's/：/:/g' \
        -e 's/；/;/g' \
        -e 's/！/!/g' \
        -e 's/？/?/g' \
        -e 's/．/./g' \
        -e 's/、/, /g' \
        "$COMBINED_MD"
    rm -f "${COMBINED_MD}.bak" 2>/dev/null || true
fi

# Auto-detect platform: use Linux template if Songti SC unavailable
TEMPLATE_USED="$TEMPLATE"
if command -v fc-list &> /dev/null; then
    if ! fc-list 2>/dev/null | grep -qi "Songti SC"; then
        LINUX_TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-harmony-liturgical-linux.latex"
        if [ -f "$LINUX_TEMPLATE" ]; then
            echo "Songti SC not found — using Linux template with DejaVu + Droid Sans Fallback"
            TEMPLATE_USED="$LINUX_TEMPLATE"
        fi
    fi
fi

# Generate PDF
echo "Generating PDF with XeLaTeX..."
echo ""

pandoc "$COMBINED_MD" \
    -o "$OUTPUT_PDF" \
    --pdf-engine=xelatex \
    --template="$TEMPLATE_USED" \
    --from=markdown-superscript-subscript \
    --toc \
    --toc-depth=2 \
    --top-level-division=chapter

if [ -f "$OUTPUT_PDF" ]; then
    SIZE=$(ls -lh "$OUTPUT_PDF" | awk '{print $5}')
    PAGES=$(pdfinfo "$OUTPUT_PDF" 2>/dev/null | grep Pages | awk '{print $2}' || echo "unknown")
    echo ""
    echo "============================================"
    echo "SUCCESS: Gospel Harmony Liturgical PDF Generated!"
    echo "============================================"
    echo ""
    echo "   Title: 耶穌基督完整生平"
    echo "   Format: 8.5×11\" Letter (Lectern Edition)"
    echo "   File: $OUTPUT_PDF"
    echo "   Size: $SIZE"
    echo "   Pages: $PAGES"
    echo "   Chapters: $chapter_count"
    echo ""
    echo "   Liturgical Features:"
    echo "   - Large Print (12pt) for lectern reading"
    echo "   - Red Letter Bible (Jesus's words in red)"
    echo "   - Liturgical Year Wheel"
    echo "   - Liturgical Colors Chart"
    echo "   - Lectionary Cycle Diagram"
    echo "   - Daily Office Hours"
    echo "   - Eucharistic Prayer Structure"
    echo "   - Holy Land Map"
    echo "   - Four Gospels Overview Box"
    echo "   - Gospel Harmony Structure Diagram"
    echo "   - Seven Signs & I AM boxes"
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

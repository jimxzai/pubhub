#!/bin/bash
# ============================================================================
# Build Gospel of John - NIV Study Bible Edition (2026)
# 7×9.25" Study Bible Size with Two-Column Layout
# Extensive Study Notes, Cross-References, Maps, Word Studies
# Uses the gospel-niv-study-2026.latex template
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration
VERSION="${1:-esv}"  # Default to ESV, can pass nasb, nkjv, niv
BOOK_DIR="$PROJECT_ROOT/books/bible/gospel-of-john"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-niv-study-2026.latex"
OUTPUT_DIR="$PROJECT_ROOT/output"

# Display usage if help requested
if [ "$VERSION" = "-h" ] || [ "$VERSION" = "--help" ]; then
    echo "Usage: $0 [version]"
    echo ""
    echo "  Builds Gospel of John NIV Study Bible PDF with the specified English version."
    echo "  This is a STUDY BIBLE edition (7×9.25\") with comprehensive study features."
    echo ""
    echo "  Versions:"
    echo "    esv   - English Standard Version (default)"
    echo "    nasb  - New American Standard Bible"
    echo "    nkjv  - New King James Version"
    echo "    niv   - New International Version"
    echo ""
    echo "  Examples:"
    echo "    $0           # Build with ESV (default)"
    echo "    $0 esv       # Build with ESV"
    echo "    $0 nasb      # Build with NASB"
    echo "    $0 nkjv      # Build with NKJV"
    echo "    $0 niv       # Build with NIV"
    echo ""
    echo "  Template: gospel-niv-study-2026.latex"
    echo "  Features:"
    echo "    - 7×9.25\" Study Bible size"
    echo "    - Two-column layout"
    echo "    - Red Letter Bible (Jesus's words in red)"
    echo "    - Comprehensive Study Notes (footnotes)"
    echo "    - Cross-references"
    echo "    - Book Introductions and Outlines"
    echo "    - Gospel Structure Chart"
    echo "    - Seven Signs Chart"
    echo "    - I AM Statements Chart"
    echo "    - Holy Land Map"
    echo "    - Timeline"
    echo "    - Word Study boxes"
    echo "    - Character Profile boxes"
    echo "    - Theological Note boxes"
    echo "    - Historical/Cultural Background boxes"
    exit 0
fi

# Set directory based on version
if [ "$VERSION" != "esv" ]; then
    BOOK_DIR="$PROJECT_ROOT/books/bible/gospel-of-john-${VERSION}"
fi

OUTPUT_FILE="$OUTPUT_DIR/gospel-of-john-niv-study-${VERSION}.pdf"

VERSION_UPPER=$(echo "$VERSION" | tr '[:lower:]' '[:upper:]')

echo "============================================"
echo "Building Gospel of John - NIV Study Bible Edition (2026)"
echo "Version: $VERSION_UPPER"
echo "Format: 7×9.25\" Study Bible (Two-Column)"
echo "Features: Study Notes, Cross-References, Charts, Maps"
echo "Source: $BOOK_DIR"
echo "Template: $TEMPLATE"
echo "Output: $OUTPUT_FILE"
echo "============================================"

# Verify source directory exists
if [ ! -d "$BOOK_DIR" ]; then
    echo "ERROR: Source directory not found: $BOOK_DIR"
    exit 1
fi

# Verify template exists
if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Combine all markdown files in order
COMBINED_FILE="$OUTPUT_DIR/gospel-of-john-niv-study-combined.md"

echo "Combining markdown files..."

# Bible version full names
case "$VERSION" in
    esv)  VERSION_FULL="English Standard Version (ESV)" ;;
    nasb) VERSION_FULL="New American Standard Bible (NASB)" ;;
    nkjv) VERSION_FULL="New King James Version (NKJV)" ;;
    niv)  VERSION_FULL="New International Version (NIV)" ;;
    *)    VERSION_FULL="English Standard Version (ESV)" ;;
esac

# Start with YAML front matter
cat > "$COMBINED_FILE" << EOF
---
title: 約翰福音研讀
subtitle: Gospel of John Deep Study - $VERSION_UPPER NIV Study Bible Edition
author: 三書精讀出版系統
date: 2026年1月
publisher: Soli Deo Gloria
---

EOF

# Add each chapter file in order
CHAPTER_COUNT=0
for f in "$BOOK_DIR"/[0-2]*.md; do
    if [ -f "$f" ]; then
        echo "  Adding: $(basename "$f")"
        echo "" >> "$COMBINED_FILE"
        # Skip YAML front matter in individual files (macOS compatible)
        # Also convert ^n^ to \textsuperscript{n} for LaTeX compatibility inside \jesus{}
        awk 'BEGIN{skip=0} /^---$/{if(NR==1){skip=1;next}else if(skip){skip=0;next}} !skip{print}' "$f" \
            | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_FILE"
        echo "" >> "$COMBINED_FILE"
        echo "\\pagebreak" >> "$COMBINED_FILE"
        echo "" >> "$COMBINED_FILE"
        ((CHAPTER_COUNT++))
    fi
done

echo ""
echo "Chapters found: $CHAPTER_COUNT"

# Convert emojis to text equivalents for PDF compatibility
echo "Converting emojis to text equivalents..."
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
    -e 's/🤖/(Robot)/g' \
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
    "$COMBINED_FILE"

echo "Running pandoc with XeLaTeX..."

# Build PDF with pandoc
pandoc "$COMBINED_FILE" \
    --pdf-engine=xelatex \
    --template="$TEMPLATE" \
    --from=markdown-superscript-subscript \
    --toc \
    --toc-depth=2 \
    --top-level-division=chapter \
    -o "$OUTPUT_FILE"

# Check result
if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
    PAGES=$(pdfinfo "$OUTPUT_FILE" 2>/dev/null | grep Pages | awk '{print $2}' || echo "unknown")
    echo ""
    echo "============================================"
    echo "SUCCESS: Gospel of John NIV Study Bible ($VERSION_UPPER)"
    echo "   Format: 7x9.25\" Study Bible Edition"
    echo "   File: $OUTPUT_FILE"
    echo "   Size: $SIZE"
    echo "   Pages: $PAGES"
    echo "   Chapters: $CHAPTER_COUNT"
    echo ""
    echo "   NIV Study Bible Features:"
    echo "   - Two-column layout"
    echo "   - Red Letter Bible (Jesus's words in red)"
    echo "   - Book Introduction & Outline"
    echo "   - Gospel Structure Chart"
    echo "   - Seven Signs Chart"
    echo "   - I AM Statements Chart"
    echo "   - Holy Land Map"
    echo "   - Ministry Timeline"
    echo "   - Word Study boxes"
    echo "   - Character Profile boxes"
    echo "   - Theological Note boxes"
    echo "   - Historical/Cultural boxes"
    echo "============================================"

    # Open the PDF
    if command -v open &> /dev/null; then
        echo ""
        echo "Opening PDF..."
        open "$OUTPUT_FILE"
    fi
else
    echo "FAILED: PDF not created"
    exit 1
fi

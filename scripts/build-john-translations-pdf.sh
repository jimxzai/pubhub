#!/bin/bash

# Gospel of John Multi-Translation PDF Builder
# Generates a parallel translation study Bible with Red Letter edition

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-john-translations"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-john-translations-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-john-translations.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-john-translations.latex"

echo "=========================================="
echo "📖 Gospel of John Multi-Translation PDF"
echo "=========================================="
echo "Translations: ESV (Red Letter), NKJV, NASB, NIV, CUV"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check if template exists
if [ ! -f "$TEMPLATE" ]; then
    echo "⚠️  Template not found: $TEMPLATE"
    echo "Creating from gospel-of-john-original.latex..."
    cp "$PROJECT_ROOT/templates/pdf/gospel-of-john-original.latex" "$TEMPLATE" 2>/dev/null || {
        echo "❌ Could not create template. Please create $TEMPLATE first."
        exit 1
    }
fi

# Combine all markdown files
echo "📝 Combining translation chapters..."
cat > "$COMBINED_MD" << 'HEADER'
---
title: "Gospel of John - Multi-Translation Study Bible"
subtitle: "約翰福音多譯本研讀聖經"
author: "PubHub 三書精讀系統"
date: "2026年1月"
publisher: "三書精讀出版系統"
copyright: |
  © 2026 Soli Deo Gloria — 唯獨榮耀神

  **Translations Used:**

  • ESV - English Standard Version (Crossway)

  • NKJV - New King James Version (Thomas Nelson)

  • NASB - New American Standard Bible (Lockman)

  • NIV - New International Version (Biblica)

  • CUV - 和合本聖經 (Public Domain)

  **Red Letter Edition**: Jesus's words displayed in red (#CC0000)

  **Glory = Grace + Truth**
---

HEADER

# Add overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    tail -n +8 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# Add all chapters in order
chapter_count=0
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21; do
    chapter_file="$INPUT_DIR/$i-"*.md
    for f in $chapter_file; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            # Skip YAML frontmatter (lines 1-7) and add content
            # Convert ^number^ to \textsuperscript{number} for LaTeX compatibility
            tail -n +8 "$f" | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
            printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
            ((chapter_count++))
        fi
    done
done

echo ""
echo "✅ Combined markdown created"
echo "   Chapters: $chapter_count"
echo "   Lines: $(wc -l < "$COMBINED_MD")"
echo ""

# Generate PDF
echo "🔨 Generating PDF with multi-translation template..."
echo "   Template: gospel-of-john-translations.latex"
echo ""

pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=2 \
  --top-level-division=chapter \
  -V tocdepth=1 \
  2>&1 | grep -v "^$" | head -30

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Multi-Translation PDF Generated!"
    echo "=========================================="
    echo ""
    echo "📄 Output: $OUTPUT_PDF"
    echo "📊 Size: $(du -h "$OUTPUT_PDF" | cut -f1)"
    echo "📑 Chapters: $chapter_count"
    echo ""
    echo "Features:"
    echo "  ✓ ESV Red Letter Edition"
    echo "  ✓ NKJV, NASB, NIV parallels"
    echo "  ✓ Chinese Union Version (CUV)"
    echo "  ✓ Greek word studies"
    echo "  ✓ Translation comparison notes"
    echo ""
    echo "To open:"
    echo "  open \"$OUTPUT_PDF\""
    echo ""
else
    echo ""
    echo "⚠️  PDF generation failed"
    echo "Check the template at: $TEMPLATE"
    echo "Or try running with verbose output"
    exit 1
fi

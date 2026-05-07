#!/bin/bash

# Gospel of Matthew PDF Builder - ORIGINAL VERSION
# Uses the premium template with TikZ diagrams and Red Letter Bible feature

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-matthew"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-matthew-combined-full.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-matthew-original.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-matthew.latex"

echo "=========================================="
echo "📖 Gospel of Matthew PDF Generator"
echo "=========================================="
echo "Template: gospel-of-matthew.latex (Royal Purple Theme)"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Combine all markdown files
echo "📝 Combining ALL 28 chapters..."
cat > "$COMBINED_MD" << 'HEADER'
---
title: "馬太福音研讀"
subtitle: "Gospel of Matthew Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年1月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Jim Xiao

  **三大核心資源整合：**

  • **黃長老週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **D.A. Carson** — Matthew Commentary

  **天國君王 = 應許 + 成就**

  五大講論呼應摩西五經 | 耶穌：新的摩西

  All rights reserved.
---

HEADER

# Add overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    tail -n +2 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# Add all 28 chapters in order
chapter_count=0
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28; do
    chapter_file="$INPUT_DIR/$i-"*.md
    for f in $chapter_file; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            # Skip YAML frontmatter (lines 1-7) and add content
            # Convert ^number^ to \textsuperscript{number} for LaTeX compatibility inside \jesus{}
            tail -n +8 "$f" | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
            printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
            ((chapter_count++))
            break  # Only process first match
        fi
    done
done

echo ""
echo "✅ Combined markdown created"
echo "   Chapters: $chapter_count"
echo "   Lines: $(wc -l < "$COMBINED_MD")"
echo ""

# Generate PDF using premium template
echo "🔨 Generating PDF with premium template (TikZ diagrams)..."
echo "   Template: gospel-of-matthew.latex"
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
    echo "✅ Matthew PDF Generated Successfully!"
    echo "=========================================="
    echo ""
    echo "📄 Output: $OUTPUT_PDF"
    echo "📊 Size: $(du -h "$OUTPUT_PDF" | cut -f1)"
    echo "📑 Chapters: $chapter_count of 28"
    echo ""
    echo "Features of Matthew template:"
    echo "  ✓ Royal purple theme (King of Heaven)"
    echo "  ✓ TikZ diagrams (crown, star, maps)"
    echo "  ✓ Five Discourses structure diagram"
    echo "  ✓ Beatitudes mountain visual"
    echo "  ✓ Kingdom Parables diagram"
    echo "  ✓ Red Letter Bible support (\\jesus{} command)"
    echo "  ✓ Professional 7×10 inch format"
    echo ""
    echo "To open:"
    echo "  open \"$OUTPUT_PDF\""
    echo ""
else
    echo ""
    echo "⚠️  PDF generation failed"
    echo "Check the error messages above for details"
    exit 1
fi

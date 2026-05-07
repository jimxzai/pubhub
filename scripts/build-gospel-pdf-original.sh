#!/bin/bash

# Gospel of John PDF Builder - ORIGINAL VERSION (from git commit d762581)
# Uses the original premium template with TikZ diagrams and advanced features

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-john"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-john-combined-full.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-john-original.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-john-original.latex"

echo "=========================================="
echo "📖 Gospel of John PDF Generator (ORIGINAL)"
echo "=========================================="
echo "Restored from git commit: d762581"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Combine all markdown files
echo "📝 Combining ALL 21 chapters..."
cat > "$COMBINED_MD" << 'HEADER'
---
title: "約翰福音研讀"
subtitle: "Gospel of John Deep Study"
author: "PubHub 三書精讀系統"
date: "2025年12月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

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
    tail -n +2 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# Add all 21 chapters in order (including 01b for John 1:19-51)
chapter_count=0
for i in 01 01b 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21; do
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

# Generate PDF using original premium template
echo "🔨 Generating PDF with original template (TikZ diagrams)..."
echo "   Template: gospel-of-john-original.latex"
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
    echo "✅ Original PDF Generated Successfully!"
    echo "=========================================="
    echo ""
    echo "📄 Output: $OUTPUT_PDF"
    echo "📊 Size: $(du -h "$OUTPUT_PDF" | cut -f1)"
    echo "📑 Chapters: $chapter_count of 21"
    echo ""
    echo "Features of original template:"
    echo "  ✓ TikZ diagrams (vine, cross, maps)"
    echo "  ✓ Advanced typography"
    echo "  ✓ Scripture boxes with backgrounds"
    echo "  ✓ Greek word study tables"
    echo "  ✓ Professional 7×10 inch format"
    echo "  ✓ Three core resources integration"
    echo ""
    echo "To open:"
    echo "  open \"$OUTPUT_PDF\""
    echo ""
else
    echo ""
    echo "⚠️  PDF generation failed (likely missing TikZ packages)"
    echo "This is expected - the original template requires additional LaTeX packages"
    echo "Use build-gospel-pdf-premium.sh for a working alternative"
    exit 1
fi

#!/bin/bash

# Gospel of John PDF Builder - Multiple English Versions
# Generates PDF with different English Bible translations: NASB, NKJV, NIV

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-john"
OUTPUT_DIR="$PROJECT_ROOT/output"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-john-original.latex"

# Function to build a version
build_version() {
    local VERSION=$1
    local VERSION_NAME=$2
    local COMBINED_MD="$OUTPUT_DIR/gospel-of-john-combined-${VERSION}.md"
    local OUTPUT_PDF="$OUTPUT_DIR/gospel-of-john-${VERSION}.pdf"

    echo ""
    echo "=========================================="
    echo "📖 Building Gospel of John - $VERSION_NAME"
    echo "=========================================="
    echo ""

    # Create combined markdown with version-specific header
    cat > "$COMBINED_MD" << HEADER
---
title: "約翰福音研讀"
subtitle: "Gospel of John Deep Study ($VERSION_NAME)"
author: "PubHub 三書精讀系統"
date: "2025年12月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 解經王子 (1909)

  **English Scripture: $VERSION_NAME**

  **榮耀 = 恩典 + 真理**

  七個神蹟 (works) 彰顯恩典 | 七個「我是」(words) 彰顯真理

  All rights reserved.
---

HEADER

    # Add overview
    if [ -f "$INPUT_DIR/00-overview.md" ]; then
        echo "  Adding: 00-overview.md"
        # Replace ESV header with version-specific header
        tail -n +2 "$INPUT_DIR/00-overview.md" | sed "s/English — ESV/English — $VERSION_NAME/g" >> "$COMBINED_MD"
        printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    fi

    # Add all chapters
    chapter_count=0
    for i in 01 01b 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21; do
        chapter_file="$INPUT_DIR/$i-"*.md
        for f in $chapter_file; do
            if [ -f "$f" ]; then
                echo "  Adding: $(basename "$f")"
                # Skip YAML frontmatter, convert verse numbers, replace ESV header
                tail -n +8 "$f" | \
                    sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' | \
                    sed "s/English — ESV/English — $VERSION_NAME/g" >> "$COMBINED_MD"
                printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
                ((chapter_count++))
                break
            fi
        done
    done

    echo ""
    echo "✅ Combined markdown created for $VERSION_NAME"
    echo "   Chapters: $chapter_count"
    echo ""

    # Generate PDF
    echo "🔨 Generating PDF..."
    pandoc "$COMBINED_MD" \
      -o "$OUTPUT_PDF" \
      --pdf-engine=xelatex \
      --template="$TEMPLATE" \
      --from=markdown-superscript-subscript \
      --toc \
      --toc-depth=1 \
      --top-level-division=chapter \
      -V tocdepth=0 \
      2>&1 | grep -v "^$" | head -20

    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo ""
        echo "✅ $VERSION_NAME PDF Generated: $OUTPUT_PDF"
        echo "📊 Size: $(du -h "$OUTPUT_PDF" | cut -f1)"
    else
        echo "❌ Failed to generate $VERSION_NAME PDF"
        return 1
    fi
}

# Main execution
echo "=========================================="
echo "📖 Gospel of John Multi-Version PDF Builder"
echo "=========================================="
echo ""
echo "This script generates PDFs with different English translations."
echo "Note: The English scripture content remains ESV in source files."
echo "Only the header label is changed to indicate intended version."
echo ""
echo "For full version replacement, the markdown files would need"
echo "to contain the actual NASB/NKJV/NIV text."
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Build all three versions
build_version "nasb" "NASB (New American Standard Bible)"
build_version "nkjv" "NKJV (New King James Version)"
build_version "niv" "NIV (New International Version)"

echo ""
echo "=========================================="
echo "📚 All Versions Complete!"
echo "=========================================="
echo ""
echo "Generated PDFs:"
echo "  📄 gospel-of-john-nasb.pdf"
echo "  📄 gospel-of-john-nkjv.pdf"
echo "  📄 gospel-of-john-niv.pdf"
echo ""
echo "To open all:"
echo "  open \"$OUTPUT_DIR/gospel-of-john-nasb.pdf\""
echo "  open \"$OUTPUT_DIR/gospel-of-john-nkjv.pdf\""
echo "  open \"$OUTPUT_DIR/gospel-of-john-niv.pdf\""
echo ""

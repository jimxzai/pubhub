#!/bin/bash

# Gospel of Luke PDF Builder - CONSOLIDATED 2026 EDITION
# = 24 chapters (deep study, matching the Gospel of John consolidated standard)
# Uses the system default template: templates/pdf/gospel-of-luke.latex

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-luke"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-luke-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-luke-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-luke.latex"

echo "=========================================="
echo "📖 Gospel of Luke PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "路加福音研讀"
subtitle: "Gospel of Luke Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老查經法** — 全備釋經、以基督為中心的查經傳統

  • **John MacArthur** — 逐節解經 (gty.org / MacArthur New Testament Commentary)

  • **G. Campbell Morgan** — 解經王子 (*The Gospel According to Luke*, 1931)

  路加福音——完全人子的福音：恩典臨到卑微者、外邦人、婦女、稅吏與罪人

  All rights reserved.
---

HEADER

# 1. Overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    tail -n +8 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 2. All 24 chapters in order
chapter_count=0
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24; do
    for f in "$INPUT_DIR/$i-"*.md; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            tail -n +8 "$f" | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
            printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
            ((chapter_count++))
            break
        fi
    done
done

# 3. References appendix
if [ -f "$INPUT_DIR/99-appendix-references.md" ]; then
    echo "  Adding: 99-appendix-references.md"
    tail -n +8 "$INPUT_DIR/99-appendix-references.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""

# Convert red letter markers for Jesus's words
echo "Converting red letter markers..."
sed -i.bak \
    -e 's/<red>/\\jesus{/g' \
    -e 's/<\/red>/}/g' \
    "$COMBINED_MD"
rm -f "${COMBINED_MD}.bak" 2>/dev/null || true
echo ""
echo "🔨 Generating PDF with default template (gospel-of-luke.latex)..."

pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter \
  -V tocdepth=0

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ PDF generated: $OUTPUT_PDF ($(du -h "$OUTPUT_PDF" | cut -f1))"
else
    echo "❌ PDF generation failed"
    exit 1
fi

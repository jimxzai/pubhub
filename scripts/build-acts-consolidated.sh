#!/bin/bash

# Acts of the Apostles PDF Builder - CONSOLIDATED 2026 EDITION
# = Overview (with embedded 全書領受總綱) + 15 chapter files (使徒行傳 1:1-28:31)
# Uses templates/pdf/acts.latex (Flame/Ember theme, matching the Gospel of John /
# Gospel Harmony Liturgical series standard: cover art, frontispiece, map, appendices)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/acts"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/acts-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/acts-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/acts.latex"

echo "=========================================="
echo "🔥 Acts of the Apostles PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "使徒行傳研讀"
subtitle: "Acts of the Apostles Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 《使徒行傳》(1924)

  **能力 = 聖靈藉見證彰顯**

  耶路撒冷 (1-7章) | 猶太．撒瑪利亞 (8-12章) | 直到地極 (13-28章)

  All rights reserved.
---

HEADER

# 1. Overview (includes the embedded 全書領受總綱 section)
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md (incl. 全書領受總綱)"
    tail -n +8 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 2. All 15 chapter files in order
chapter_count=0
for i in 01 02 03-04 05-06 07 08-09 10-11 12 13-14 15 16-18 19-20 21-23 24-26 27-28; do
    found=""
    for f in "$INPUT_DIR/$i-"*.md; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            tail -n +8 "$f" >> "$COMBINED_MD"
            printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
            ((chapter_count++))
            found=1
            break
        fi
    done
    if [ -z "$found" ]; then
        echo "❌ Missing chapter file for prefix '$i-' in $INPUT_DIR — aborting build"
        exit 1
    fi
done

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters + overview)"
echo ""
echo "🔨 Generating PDF with acts.latex template..."

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

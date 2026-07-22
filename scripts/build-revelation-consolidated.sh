#!/bin/bash
# Revelation PDF Builder - CONSOLIDATED 2026 EDITION
# = Overview + 35 per-pericope files (John/Mark/Hebrews-standard 領受 framing, ai-eden.com citations)
# Sources from books/bible/revelation/
# Uses templates/pdf/revelation.latex (Crown of Victory / 得勝之冠 theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/revelation"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/revelation-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/revelation-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/revelation.latex"

echo "=========================================="
echo "📖 Revelation PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
  echo "ERROR: Template not found: $TEMPLATE"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "得勝之冠"
subtitle: "啟示錄研讀 Revelation Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老式查經** — 整本聖經脈絡的深度領受
  • **John MacArthur** — 逐節解經講道 (gty.org)
  • **G.K. Beale / Robert Mounce / Grant Osborne** — 當代學術注釋

  **經文核對**：[ai-eden.com/bible](https://www.ai-eden.com/bible)

  All rights reserved.
---

HEADER

# 1. Overview (strip its own front matter block: two '---' lines)
if [ -f "$INPUT_DIR/00-overview.md" ]; then
  echo "  Adding: 00-overview.md"
  awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
  printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 2. All pericope files in filename order (01a-prologue.md ... 14-epilogue.md)
#    Convert ^n^ verse-number superscripts to \textsuperscript{n}, strip each
#    file's own 7-line YAML front matter (tail -n +8 keeps from the blank
#    line after the closing '---' onward).
chapter_count=0
for f in "$INPUT_DIR"/[0-9]*.md; do
  [ -f "$f" ] || continue
  echo "  Adding: $(basename "$f")"
  tail -n +8 "$f" | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
  printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
  ((chapter_count++))
done

if [ "$chapter_count" -eq 0 ]; then
  echo "❌ No chapter files found in $INPUT_DIR — aborting build"
  exit 1
fi

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count pericope files + overview)"
echo ""
echo "🔨 Generating PDF with revelation.latex template..."

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

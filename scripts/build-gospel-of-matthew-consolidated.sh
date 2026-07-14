#!/bin/bash

# Gospel of Matthew PDF Builder - CONSOLIDATED 2026 EDITION
# = Prologue + 5 thematic chapters (渐进启示 framework, 天國之王)
# Sources from books/bible/matthew/book/ (the current, actively maintained project)
# Uses templates/pdf/gospel-of-matthew.latex (Royal Purple King theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/matthew/book"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-matthew-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-matthew-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-matthew.latex"

echo "=========================================="
echo "📖 Gospel of Matthew PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "馬太福音研讀"
subtitle: "天國之王 — Gospel of Matthew Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 解經王子，*The Gospel According to Matthew* (1929)

  **以馬內利 = 天國近了 + 我常與你們同在**

  五大講論呼應摩西五經 | 十個神蹟彰顯君王的權能 | 十次應驗公式宣告漸進啟示的成就

  All rights reserved.
---

HEADER

# 1. Overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    cat "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 2. Prologue (canonical context)
if [ -f "$INPUT_DIR/prologue-canonical-context.md" ]; then
    echo "  Adding: prologue-canonical-context.md"
    cat "$INPUT_DIR/prologue-canonical-context.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 3. Chapter 1 (skip the redundant book-title preamble unique to this file: lines 1-11)
if [ -f "$INPUT_DIR/chapter-01-king-identity.md" ]; then
    echo "  Adding: chapter-01-king-identity.md"
    tail -n +12 "$INPUT_DIR/chapter-01-king-identity.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 4. Chapters 2-5 in order
chapter_count=2
for f in chapter-02-sermon-on-mount.md chapter-03-kings-power.md chapter-04-discipleship.md chapter-05-passion-week.md; do
    if [ -f "$INPUT_DIR/$f" ]; then
        echo "  Adding: $f"
        cat "$INPUT_DIR/$f" >> "$COMBINED_MD"
        printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
        ((chapter_count++))
    fi
done

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters + overview + prologue)"
echo ""
echo "🔨 Generating PDF with gospel-of-matthew.latex template..."

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

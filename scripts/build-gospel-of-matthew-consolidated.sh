#!/bin/bash

# Gospel of Matthew PDF Builder - CONSOLIDATED 2026 EDITION
# = Overview + Elder Wong study + Prologue + 28 per-chapter files (渐进启示 framework, 天國之王)
# Sources from books/bible/matthew/book/ (the current, actively maintained project)
# Uses templates/pdf/gospel-of-matthew.latex (Royal Purple King theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/matthew/book"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
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

# 2. Elder Wong systematic reception (structure-based deep study)
#    Demote headings one level so the whole study is a single top-level chapter
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——黃長老查經法 (Systematic Reception)\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 3. Prologue (canonical context)
if [ -f "$INPUT_DIR/prologue-canonical-context.md" ]; then
    echo "  Adding: prologue-canonical-context.md"
    cat "$INPUT_DIR/prologue-canonical-context.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 4. 28 per-chapter files, in order
chapter_count=0
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28; do
    for f in "$INPUT_DIR/$i-"*.md; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            cat "$f" >> "$COMBINED_MD"
            printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
            ((chapter_count++))
            break
        fi
    done
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

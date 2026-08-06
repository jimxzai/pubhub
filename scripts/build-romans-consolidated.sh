#!/bin/bash

# Romans PDF Builder - CONSOLIDATED 2026 EDITION
# = Overview + systematic study + 16 chapters + index + references appendices
# Sources from books/bible/pauline-epistles/romans/ (Elder Wong methodology + MacArthur + Morgan)
# Uses templates/pdf/romans.latex (Navy/Gold Imperial Rome theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/pauline-epistles/romans"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
INDICES_FILE="$INPUT_DIR/98-appendix-indices.md"
REFS_FILE="$INPUT_DIR/99-appendix-references.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/romans-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/romans-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/romans.latex"

echo "=========================================="
echo "📖 Romans PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "羅馬書研讀"
subtitle: "Romans Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **聖經版本 / Bible Versions**

  中文經文以和合本修訂版（RCUV）為主，部分章節因原始資料來源限制，經核實後改用和合本（CUV）；各章實際版本來源請見附錄二（99-appendix-references.md）逐章說明。

  Chinese Scripture is primarily RCUV, with some chapters using verified CUV as a documented fallback where RCUV could not be reliably sourced; see the references appendix for the exact per-chapter breakdown.

  English: English Standard Version (ESV)

  **主要參考資料 / Primary Sources：**

  • 黃長老查經方法論與神學框架之應用（本書無對應之黃長老羅馬書逐節查經筆記原始記錄；詳見附錄二誠實說明）

  • **John MacArthur** — 逐節解經講道 (gty.org)

  • **G. Campbell Morgan** — 屬靈組織分析

  All rights reserved.
---

HEADER

# 1. Overview (strip its own front matter block: two '---' lines)
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
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

# 3. All 16 chapters in order
chapter_count=0
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16; do
    found=""
    for f in "$INPUT_DIR/$i-"*.md; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            tail -n +8 "$f" | sed 's/\^\([^\^]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
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

# 4. Scripture & theme indices appendix
if [ -f "$INDICES_FILE" ]; then
    echo "  Adding: 98-appendix-indices.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INDICES_FILE" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 5. References appendix
if [ -f "$REFS_FILE" ]; then
    echo "  Adding: 99-appendix-references.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$REFS_FILE" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters + overview + references)"
echo ""
echo "🔨 Generating PDF with romans.latex template..."

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

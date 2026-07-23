#!/bin/bash

# Psalms PDF Builder - CONSOLIDATED 2026 EDITION
# = Overview + five book-by-book deep-study files (Books I-V of the Psalter)
# Sources from books/bible/psalm/ (Elder-Huang Christological reading, CUV verified via cnbible.com)
# Uses templates/pdf/psalm.latex (Parchment Brown/Gold Psalter theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/psalm"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/psalm-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/psalm-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/psalm.latex"

echo "=========================================="
echo "📖 Psalms PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "詩篇研讀"
subtitle: "The Whole Psalter — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **讀詩篇的鑰匙：**

  詩篇 150 篇——主角永遠是耶穌。從祂的角度讀，光就照進來。

  **五卷結構**：卷一 (1–41) · 卷二 (42–72) · 卷三 (73–89) · 卷四 (90–106) · 卷五 (107–150)

  **經文核對**：以 [ai-eden.com/bible](https://www.ai-eden.com/bible) 為標準來源（和合本 CUV）；逐字核對經 cnbible.com 進行，並經 ai-eden.com 抽樣覆核一致（標點從 CUV 現代標點版）

  All rights reserved.
---

HEADER

# 1. Overview (strip its own front matter block: two '---' lines)
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
else
    echo "❌ Missing 00-overview.md in $INPUT_DIR — aborting build"
    exit 1
fi

# 2. Five books of the Psalter in order
book_count=0
for i in 01 02 03 04 05; do
    found=""
    for f in "$INPUT_DIR/$i-"*.md; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$f" >> "$COMBINED_MD"
            printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
            ((book_count++))
            found=1
            break
        fi
    done
    if [ -z "$found" ]; then
        echo "❌ Missing book file for prefix '$i-' in $INPUT_DIR — aborting build"
        exit 1
    fi
done

# 3. Historical backgrounds deep-read
if [ -f "$INPUT_DIR/12-backgrounds.md" ]; then
    echo "  Adding: 12-backgrounds.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INPUT_DIR/12-backgrounds.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 4. Christ through the Psalms + Hebrew poetics + Prayer edition + appendices
for extra in 14-christ-through-psalms.md 15-hebrew-poetics.md 13-prayer-testimony.md; do
    if [ -f "$INPUT_DIR/$extra" ]; then
        echo "  Adding: $extra"
        awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INPUT_DIR/$extra" >> "$COMBINED_MD"
        printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    fi
done

# 5. Expositors' voices (Morgan + MacArthur)
if [ -f "$INPUT_DIR/11-voices-morgan-macarthur.md" ]; then
    echo "  Adding: 11-voices-morgan-macarthur.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INPUT_DIR/11-voices-morgan-macarthur.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 6. Appendices
for app in 99a-appendix-nt-quotations.md 99b-appendix-pastoral-index-reading-plan.md; do
    if [ -f "$INPUT_DIR/$app" ]; then
        echo "  Adding: $app"
        awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INPUT_DIR/$app" >> "$COMBINED_MD"
        printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    fi
done

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, overview + $book_count books)"
echo ""
echo "🔨 Generating PDF with psalm.latex template..."

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

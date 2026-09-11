#!/bin/bash

# Psalms Liturgical PDF Builder - 2026 EDITION
# = Overview + five books of the Psalter, each book paired:
#   whole-book deep study (01-05) followed by psalm-by-psalm reception guide (06-10)
# Sources from books/bible/psalm/ (Elder-Huang Christological reading, CUV verified via cnbible.com)
# Uses templates/pdf/psalm-liturgical.latex (8.5×11" Lectern/Ceremonial, gold-border cover)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/psalm"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/psalm-liturgical-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/psalm-liturgical-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/psalm-liturgical.latex"

echo "=========================================="
echo "📖 Psalms Liturgical PDF (2026)"
echo "=========================================="
echo ""
echo "Format: 8.5×11\" Letter (Lectern/Ceremonial)"
echo "Template: psalm-liturgical.latex"
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "詩篇全卷逐篇領受"
subtitle: "The Whole Psalter — Liturgical Edition"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "Soli Deo Gloria"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **聖經版本 / Bible Versions**

  中文：和合本 (CUV)；English: New American Standard Bible (NASB 1995)

  **經文核對**：以 [ai-eden.com/bible](https://www.ai-eden.com/bible) 為標準來源（和合本 CUV）；逐字核對經 cnbible.com 進行，並經 ai-eden.com 抽樣覆核一致（標點從 CUV 現代標點版）

  Scripture quotations taken from the New American Standard Bible®
  (NASB), Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation.
  Used by permission. All rights reserved. lockman.org

  本書為三書精讀項目成果之一。Part of the Three Books Deep Reading Project.
---

HEADER

# Helper: append a source file with its front matter stripped
append_file() {
    local f="$1"
    echo "  Adding: $(basename "$f")"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$f" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
}

# 1. Overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    append_file "$INPUT_DIR/00-overview.md"
else
    echo "❌ Missing 00-overview.md in $INPUT_DIR — aborting build"
    exit 1
fi

# 1b. Order of revelation / plan of God — the spine chapter
if [ -f "$INPUT_DIR/00a-revelation-order.md" ]; then
    append_file "$INPUT_DIR/00a-revelation-order.md"
fi

# 2. Five books, each paired: deep study (0N) then psalm-by-psalm guide (0N+5)
file_count=1
for pair in "01 06" "02 07" "03 08" "04 09" "05 10"; do
    for i in $pair; do
        found=""
        for f in "$INPUT_DIR/$i-"*.md; do
            if [ -f "$f" ]; then
                append_file "$f"
                ((file_count++))
                found=1
                break
            fi
        done
        if [ -z "$found" ]; then
            echo "❌ Missing file for prefix '$i-' in $INPUT_DIR — aborting build"
            exit 1
        fi
    done
done

# 3. Historical backgrounds deep-read
if [ -f "$INPUT_DIR/12-backgrounds.md" ]; then
    append_file "$INPUT_DIR/12-backgrounds.md"
    ((file_count++))
fi

# 4. The Life of Christ through the Psalms
if [ -f "$INPUT_DIR/14-christ-through-psalms.md" ]; then
    append_file "$INPUT_DIR/14-christ-through-psalms.md"
    ((file_count++))
fi

# 5. Hebrew poetics primer
if [ -f "$INPUT_DIR/15-hebrew-poetics.md" ]; then
    append_file "$INPUT_DIR/15-hebrew-poetics.md"
    ((file_count++))
fi

# 6. Prayer edition + liturgical use guide
if [ -f "$INPUT_DIR/13-prayer-testimony.md" ]; then
    append_file "$INPUT_DIR/13-prayer-testimony.md"
    ((file_count++))
fi

# 6b. Liturgical use guide (church year, daily hours, responsive reading)
if [ -f "$INPUT_DIR/16-liturgical-use.md" ]; then
    append_file "$INPUT_DIR/16-liturgical-use.md"
    ((file_count++))
fi

# 7. Expositors' voices (Morgan + MacArthur)
if [ -f "$INPUT_DIR/11-voices-morgan-macarthur.md" ]; then
    append_file "$INPUT_DIR/11-voices-morgan-macarthur.md"
    ((file_count++))
fi

# 8. Appendices
for app in 99a-appendix-nt-quotations.md 99b-appendix-pastoral-index-reading-plan.md 99c-appendix-structure-themes.md 99d-appendix-references.md; do
    if [ -f "$INPUT_DIR/$app" ]; then
        append_file "$INPUT_DIR/$app"
        ((file_count++))
    fi
done

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $file_count files)"
echo ""
echo "🔨 Generating PDF with psalm-liturgical.latex template..."

# --verbose is load-bearing, not chatter: without it pandoc swallows the whole
# xelatex log and every grep-the-log check below (and in driver.sh) passes
# vacuously. See scripts/lib/latex-check.sh for the full explanation.
source "$SCRIPT_DIR/lib/latex-check.sh"
LATEX_LOG="${OUTPUT_PDF%.pdf}-build.log"
pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --verbose \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter \
  -V tocdepth=0 > "$LATEX_LOG" 2>&1
PANDOC_EXIT=$?

latex_build_report "$PANDOC_EXIT" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1

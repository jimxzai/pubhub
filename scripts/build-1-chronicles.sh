#!/bin/bash

# 1 Chronicles PDF Builder — standalone volume
# Uses the dedicated template: templates/pdf/1-chronicles.latex

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/sam1-2-chroni1-2/1-chronicles"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/1-chronicles-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/1-chronicles.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/1-chronicles.latex"

echo "=========================================="
echo "📖 1 Chronicles PDF (standalone volume)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Strip each chapter file's YAML frontmatter (--- ... ---, plus the blank
# line that follows) before concatenating. Frontmatter length varies per
# file (00-overview.md has a multi-line copyright block), so this is done
# dynamically rather than with a fixed `tail -n +N`.
strip_frontmatter() {
  awk '
    NR==1 && $0=="---" {infm=1; next}
    infm && $0=="---" {infm=0; skipblank=1; next}
    infm {next}
    skipblank && $0=="" {skipblank=0; next}
    {print}
  ' "$1" | sed 's/\^\([0-9:]*\)\^/\\textsuperscript{\1}/g'
}

{
cat <<'FRONT'
---
title: "歷代志上研讀"
subtitle: "1 Chronicles Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老式查經** — 整本聖經脈絡的深度領受

  • **John MacArthur** — 逐節解經講道 (gty.org)

  • **G. Campbell Morgan** — 屬靈組織分析 (*Living Messages of the Books of the Bible*)

  「國度也是你的，並且你為至高，為萬有之首。」——歷代志上 29:11

  All rights reserved.
---

FRONT
} > "$COMBINED_MD"

chapter_count=0

if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    strip_frontmatter "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

for f in $(ls -1 "$INPUT_DIR"/*.md 2>/dev/null | grep -v '/00-overview\.md$' | sort -V); do
    echo "  Adding: $(basename "$f")"
    strip_frontmatter "$f" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
done

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with dedicated template (1-chronicles.latex)..."

# --verbose is load-bearing, not chatter: without it pandoc swallows the whole
# xelatex log and every grep-the-log check (and in driver.sh) passes vacuously.
# See scripts/lib/latex-check.sh for the full explanation.
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

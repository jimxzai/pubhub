#!/bin/bash

# Samuel-Chronicles PDF Builder
# Combines whichever of 1-Samuel / 2-Samuel / 1-Chronicles / 2-Chronicles
# have been written under books/bible/sam1-2-chroni1-2/ into one manuscript.
# Uses the dedicated template: templates/pdf/samuel-chronicles.latex
#
# Re-run this any time a new book's chapters are added — it only includes
# subdirectories that actually exist.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ROOT_DIR="$PROJECT_ROOT/books/bible/sam1-2-chroni1-2"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/samuel-chronicles-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/samuel-chronicles.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/samuel-chronicles.latex"

echo "=========================================="
echo "📖 Samuel-Chronicles PDF"
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

BOOKS_INCLUDED=""

{
cat <<'FRONT'
---
title: "撒母耳記與歷代志研讀"
subtitle: "1-2 Samuel & 1-2 Chronicles Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老式查經** — 整本聖經脈絡的深度領受

  • **John MacArthur** — 逐節解經講道 (gty.org)

  • **G. Campbell Morgan** — 屬靈組織分析 (*Living Messages of the Books of the Bible*)

  「耶和華不像人看人，人是看外貌，耶和華是看內心。」——撒母耳記上 16:7

  All rights reserved.
---

FRONT
} > "$COMBINED_MD"

add_book() {
  local dir="$1"
  local label="$2"
  if [ ! -d "$ROOT_DIR/$dir" ]; then
    echo "  (skipping $label — $dir/ not found)"
    return
  fi

  echo "▸ $label"
  local count=0

  if [ -f "$ROOT_DIR/$dir/00-overview.md" ]; then
    echo "    Adding: 00-overview.md"
    strip_frontmatter "$ROOT_DIR/$dir/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
  fi

  for f in $(ls -1 "$ROOT_DIR/$dir"/*.md 2>/dev/null | grep -v '/00-overview\.md$' | sort -V); do
    echo "    Adding: $(basename "$f")"
    strip_frontmatter "$f" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((count++))
  done

  echo "    ($count chapters)"
  BOOKS_INCLUDED="$BOOKS_INCLUDED $label($count)"
}

add_book "1-samuel"    "1 Samuel"
add_book "2-samuel"    "2 Samuel"
add_book "1-chronicles" "1 Chronicles"
add_book "2-chronicles" "2 Chronicles"

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines)"
echo "   Books included:$BOOKS_INCLUDED"
echo ""
echo "🔨 Generating PDF with dedicated template (samuel-chronicles.latex)..."

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

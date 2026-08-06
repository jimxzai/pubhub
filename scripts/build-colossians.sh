#!/usr/bin/env bash
# Build the 《歌羅西書：基督的豐富與得勝》manuscript: combined markdown + EPUB + PDF.
# Usage: bash scripts/build-colossians.sh
# Requires: pandoc (EPUB), pandoc + xelatex (PDF).
# Uses the dedicated template: templates/pdf/colossians.latex
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="$ROOT/books/col"
OUT_MD="$ROOT/output/colossians-combined.md"
OUT_EPUB="$ROOT/output/colossians.epub"
OUT_PDF="$ROOT/output/colossians.pdf"
TEMPLATE="$ROOT/templates/pdf/colossians.latex"

if [ ! -f "$TEMPLATE" ]; then
  echo "ERROR: Template not found: $TEMPLATE"
  exit 1
fi

mkdir -p "$ROOT/output"

# Strip each chapter file's YAML frontmatter (--- ... ---, plus the blank
# line that follows) before concatenating. Line counts vary per file (00
# has an extra "subtitle:" line), so this is done dynamically rather than
# with a fixed `tail -n +N`.
strip_frontmatter() {
  awk '
    NR==1 && $0=="---" {infm=1; next}
    infm && $0=="---" {infm=0; skipblank=1; next}
    infm {next}
    skipblank && $0=="" {skipblank=0; next}
    {print}
  ' "$1"
}

# 1) Combine front matter (for pandoc $title$/$copyright$ metadata used by
#    the template) + all chapter bodies (frontmatter stripped) in filename order.
{
cat <<'FRONT'
---
title: 歌羅西書：基督的豐富與得勝
subtitle: Colossians — The Fullness and Triumph of Christ
author: PubHub 三書精讀系統
publisher: 三書精讀出版系統
edition: 第一版
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老式查經** — 整本聖經脈絡的深度領受

  • **John MacArthur** — 逐節解經講道 (gty.org)

  • **G. Campbell Morgan** — 屬靈組織分析 (*The Westminster Pulpit*)

  「因為神本性一切的豐盛，都有形有體地居住在基督裡面，你們在他裡面也得了豐盛。」——歌羅西書 2:9-10

  All rights reserved.
---

FRONT
for f in $(ls -1 "$DIR"/*.md | sort); do
  strip_frontmatter "$f"
  printf '\n\n\\newpage\n\n'
done
} > "$OUT_MD"
echo "✓ combined markdown → $OUT_MD"

# 2) EPUB (robust for CJK + Greek; uses reader fonts, no custom LaTeX template).
if command -v pandoc >/dev/null 2>&1; then
  pandoc "$OUT_MD" -o "$OUT_EPUB" --toc --toc-depth=1 --metadata lang=zh-Hant
  echo "✓ EPUB → $OUT_EPUB"
else
  echo "… pandoc not found; skipping EPUB"
fi

# 3) PDF via xelatex, using the dedicated Colossians template (cover art,
#    frontispiece, back-matter appendices, themed back cover).
if command -v pandoc >/dev/null 2>&1 && command -v xelatex >/dev/null 2>&1; then
  pandoc "$OUT_MD" \
    -o "$OUT_PDF" \
    --pdf-engine=xelatex \
    --template="$TEMPLATE" \
    --toc --toc-depth=1 \
    --top-level-division=chapter \
    -V tocdepth=0 \
    || echo "… PDF build failed"
  [ -f "$OUT_PDF" ] && echo "✓ PDF → $OUT_PDF"
else
  echo "… pandoc or xelatex not found; skipping PDF"
fi

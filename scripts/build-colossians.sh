#!/usr/bin/env bash
# Build the 《歌羅西書：基督的豐富與得勝》manuscript: combined markdown + EPUB + PDF.
# Usage: bash scripts/build-colossians.sh
# Requires: pandoc (EPUB), pandoc + xelatex (PDF).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="$ROOT/books/col"
OUT_MD="$ROOT/output/colossians-combined.md"
OUT_EPUB="$ROOT/output/colossians.epub"
OUT_PDF="$ROOT/output/colossians.pdf"

mkdir -p "$ROOT/output"

# 1) Combine front matter + all chapter files in filename order.
{
cat <<'FRONT'
---
title: 歌羅西書：基督的豐富與得勝 — 黃長老查經
subtitle: Colossians — The Fullness and Triumph of Christ, Bible Study in the Voice of Elder Wong
edition: 第一版
---

# 歌羅西書：基督的豐富與得勝
# Colossians — The Fullness and Triumph of Christ

> 以「整本聖經」為根基,以「認識耶穌基督」為中心,以「聽見就去行」為目標。

每篇查經按「經文→精義一句話→黃長老這樣帶你讀→整本聖經的連結→讓話語住在裡面→你看見耶穌了嗎？」展開,中英對照(和合本/ESV)。

> 出版前須核對:經文對照 ai-eden.com/bible(和合本 / ESV / NASB),另以 cnbible.com 核對逐節文字;MacArthur、Campbell Morgan 引文須標明出處。

---

FRONT
for f in $(ls -1 "$DIR"/*.md | sort); do
  cat "$f"
  printf '\n\n\\newpage\n\n'
done
} > "$OUT_MD"
echo "✓ combined markdown → $OUT_MD"

# 2) EPUB (robust for CJK + Greek; uses reader fonts).
if command -v pandoc >/dev/null 2>&1; then
  pandoc "$OUT_MD" -o "$OUT_EPUB" --toc --toc-depth=1 --metadata lang=zh-Hant
  echo "✓ EPUB → $OUT_EPUB"
else
  echo "… pandoc not found; skipping EPUB"
fi

# 3) PDF via xelatex. Needs a CJK font (PingFang SC on macOS) and a main
#    font with Greek coverage (Times New Roman). Override via env:
#    CJK_FONT / MAIN_FONT.
CJK_FONT="${CJK_FONT:-PingFang SC}"
MAIN_FONT="${MAIN_FONT:-Times New Roman}"
if command -v pandoc >/dev/null 2>&1 && command -v xelatex >/dev/null 2>&1; then
  pandoc "$OUT_MD" -o "$OUT_PDF" \
    --pdf-engine=xelatex --toc --toc-depth=1 \
    -V documentclass=report -V geometry:margin=2.3cm \
    -V CJKmainfont="$CJK_FONT" -V mainfont="$MAIN_FONT" \
    || echo "… PDF build failed (check fonts: CJK_FONT='$CJK_FONT', MAIN_FONT='$MAIN_FONT')"
  [ -f "$OUT_PDF" ] && echo "✓ PDF → $OUT_PDF"
else
  echo "… pandoc or xelatex not found; skipping PDF"
fi

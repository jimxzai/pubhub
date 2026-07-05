#!/usr/bin/env bash
# Build the 《歌羅西書：基督的豐富與得勝》manuscript: combined markdown + EPUB + PDF.
# Usage: bash scripts/build-col.sh
# Requires: pandoc (EPUB), pandoc + xelatex (PDF).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="$ROOT/books/col"
OUT_MD="$ROOT/output/col-combined.md"
OUT_EPUB="$ROOT/output/col.epub"
OUT_PDF="$ROOT/output/col.pdf"

mkdir -p "$ROOT/output"

# 1) Combine front matter + all numbered chapter files (00..NN) in order.
{
cat <<'FRONT'
---
title: 歌羅西書：基督的豐富與得勝
subtitle: Colossians — The Fullness and Triumph of Christ
edition: 第一版
---

# 歌羅西書：基督的豐富與得勝
# Colossians — The Fullness and Triumph of Christ

> 以「整本聖經」為根基,以「認識耶穌基督」為中心,以「聖靈引導」為途徑,以「生命的領受」為目標。

> 出版前須核對:經文對照 ai-eden.com/bible(和合本 CUV / ESV / NASB);引文須可查證,不可杜撰。

---

FRONT
for f in $(ls -1 "$DIR"/[0-9]*.md | sort); do
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

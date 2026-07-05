#!/usr/bin/env bash
# Build the 《耶穌的比喻》 manuscript: combined markdown + EPUB + PDF.
# Usage: bash scripts/build-jesus-parables.sh
# Requires: pandoc (EPUB), pandoc + xelatex (PDF).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="$ROOT/books/JesusParables"
OUT_MD="$ROOT/output/jesus-parables-combined.md"
OUT_EPUB="$ROOT/output/jesus-parables.epub"
OUT_PDF="$ROOT/output/jesus-parables.pdf"

mkdir -p "$ROOT/output"

# 1) Combine front matter + all numbered chapter files (00..29) in order.
{
cat <<'FRONT'
---
title: 耶穌的比喻 — 黃長老查經
subtitle: The Parables of Jesus — Bible Study in the Voice of Elder Huang
edition: 第一版合輯(三輪)
---

# 耶穌的比喻 — 黃長老查經
# The Parables of Jesus

> 以「整本聖經」為根基,以「認識耶穌基督」為中心,以「聽見就去行」為目標。

本合輯三輪內容:
- **第一輪**(屬靈領受):總論 + 27 章,每章「念→找→問→連→住→行」,中英對照(RCUV/ESV),每個比喻都回到「這讓我更深認識耶穌嗎?」
- **第二輪**(原文字義 + 約翰福音貫通):希臘文字義 + 七個「我是」/七個「兆頭」對照。
- **第三輪**(對觀平行 + 歷史背景):三福音平行對照 + 第一世紀文化考據。

> 出版前須核對:經文對照 ai-eden.com/bible(和合本 / ESV / NKJV / NASB);希臘文對照 NA28/UBS5 與 BDAG;背景對照 Jeremias / Bailey;Campbell Morgan 引文出自《The Parables and Metaphors of Our Lord》。

---

FRONT
for f in $(ls -1 "$DIR"/[0-9]*.md | sort); do
  cat "$f"
  printf '\n\n\\newpage\n\n'
done
} > "$OUT_MD"
echo "✓ combined markdown → $OUT_MD"

# 2) EPUB (robust for CJK + Greek + Hebrew; uses reader fonts).
if command -v pandoc >/dev/null 2>&1; then
  pandoc "$OUT_MD" -o "$OUT_EPUB" --toc --toc-depth=1 --metadata lang=zh-Hant
  echo "✓ EPUB → $OUT_EPUB"
else
  echo "… pandoc not found; skipping EPUB"
fi

# 3) PDF via xelatex. Needs a CJK font (PingFang SC on macOS) and a main
#    font with Greek/Hebrew coverage (Times New Roman). Override via env:
#    CJK_FONT / MAIN_FONT.
CJK_FONT="${CJK_FONT:-PingFang SC}"
MAIN_FONT="${MAIN_FONT:-Times New Roman}"
if command -v pandoc >/dev/null 2>&1 && command -v xelatex >/dev/null 2>&1; then
  node "$ROOT/scripts/build-pdf.js" --format jesus-parables --input "$DIR" --output "$OUT_PDF"
else
  echo "… pandoc or xelatex not found; skipping PDF"
fi

#!/bin/bash
# Build PDF books for SGP (Sun Tzu-Graham-Practice) Investment Book
# Requires: pandoc, xelatex (MacTeX)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create output directory
mkdir -p output

echo "=========================================="
echo "Building Chinese Silicon Jim PDF..."
echo "=========================================="
pandoc zh/silicon-jim.md \
  -o output/silicon-jim-zh.pdf \
  --pdf-engine=xelatex \
  --template=templates/book-zh-simple.latex \
  --metadata title="硅谷阿甘" \
  --metadata subtitle="一个硅谷人眼中的25年变迁" \
  --metadata author="Jim Xiao" \
  --metadata date="2025年12月" \
  --toc \
  --toc-depth=2

echo "=========================================="
echo "Building English Silicon Jim PDF..."
echo "=========================================="
pandoc en/silicon-jim.md \
  -o output/silicon-jim-en.pdf \
  --pdf-engine=xelatex \
  --template=templates/book-en-simple.latex \
  --metadata title="Silicon Jim" \
  --metadata subtitle="A Silicon Valley Forrest Gump's 25-Year Journey" \
  --metadata author="Jim Xiao" \
  --metadata date="December 2025" \
  --toc \
  --toc-depth=2

echo "=========================================="
echo "Building Advisory Book (阿甘的投资备忘录) PDF..."
echo "=========================================="

# Combine all advisory chapters into one markdown file
ADVISORY_COMBINED="output/advisory-combined.md"
cat << 'HEADER' > "$ADVISORY_COMBINED"
---
title: "阿甘的投资备忘录"
subtitle: "25年硅谷生存智慧 · 简单实用版"
author: "Jim Xiao"
date: "2025年12月"
---

HEADER

# Add index
cat zh/advisory/00-index.md >> "$ADVISORY_COMBINED"
printf '\n\n\\newpage\n\n' >> "$ADVISORY_COMBINED"

# Add prologue (00-wisdom)
if [ -f "zh/advisory/00-wisdom.md" ]; then
  echo "  Adding: zh/advisory/00-wisdom.md"
  cat zh/advisory/00-wisdom.md >> "$ADVISORY_COMBINED"
  printf '\n\n\\newpage\n\n' >> "$ADVISORY_COMBINED"
fi

# Add all chapters in order (01-26)
for i in $(seq -w 1 26); do
  chapter_file="zh/advisory/${i}-*.md"
  for f in $chapter_file; do
    if [ -f "$f" ]; then
      echo "  Adding: $f"
      cat "$f" >> "$ADVISORY_COMBINED"
      printf '\n\n\\newpage\n\n' >> "$ADVISORY_COMBINED"
    fi
  done
done

# Add appendices
for appendix in zh/advisory/appendix-*.md; do
  if [ -f "$appendix" ]; then
    echo "  Adding: $appendix"
    cat "$appendix" >> "$ADVISORY_COMBINED"
    printf '\n\n\\newpage\n\n' >> "$ADVISORY_COMBINED"
  fi
done

# Build the PDF
pandoc "$ADVISORY_COMBINED" \
  -o output/advisory-book-zh.pdf \
  --pdf-engine=xelatex \
  --template=templates/book-zh-simple.latex \
  --toc \
  --toc-depth=2

echo ""
echo "=========================================="
echo "Done! PDFs generated:"
echo "=========================================="
ls -la output/*.pdf

echo ""
echo "Opening PDFs..."
open output/silicon-jim-zh.pdf
open output/advisory-book-zh.pdf

#!/bin/bash
# Build PDF books for Book 5: Retirement Planning
# Requires: pandoc, xelatex (MacTeX)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create output directory
mkdir -p output

echo "=========================================="
echo "Book 5: Retirement Planning"
echo "=========================================="

# ==========================================
# Build Chinese Version
# ==========================================
echo ""
echo "Building Chinese Version (中文版)..."
echo "=========================================="

ZH_COMBINED="output/book5-zh-combined.md"
cat << 'HEADER' > "$ZH_COMBINED"
---
title: "退休规划"
subtitle: "硅谷阿甘投资备忘录 · 第五本"
author: "Jim Xiao"
date: "2025年12月"
---

HEADER

# Add chapters
for chapter in zh/25-retirement.md zh/26-healthcare.md; do
  if [ -f "$chapter" ]; then
    echo "  Adding: $chapter"
    cat "$chapter" >> "$ZH_COMBINED"
    printf '\n\n\\newpage\n\n' >> "$ZH_COMBINED"
  fi
done

# Build Chinese PDF
pandoc "$ZH_COMBINED" \
  -o output/book5-retirement-zh.pdf \
  --pdf-engine=xelatex \
  --template=templates/book-zh.latex \
  --toc \
  --toc-depth=2

if [ $? -eq 0 ]; then
  echo "  ✓ Chinese PDF built successfully"
else
  echo "  ✗ Chinese PDF build failed"
fi

# ==========================================
# Build English Version
# ==========================================
echo ""
echo "Building English Version..."
echo "=========================================="

EN_COMBINED="output/book5-en-combined.md"
cat << 'HEADER' > "$EN_COMBINED"
---
title: "Retirement Planning"
subtitle: "Silicon Valley Forrest's Investment Memo · Book Five"
author: "Jim Xiao"
date: "December 2025"
---

HEADER

# Add chapters
for chapter in en/25-retirement.md en/26-healthcare.md; do
  if [ -f "$chapter" ]; then
    echo "  Adding: $chapter"
    cat "$chapter" >> "$EN_COMBINED"
    printf '\n\n\\newpage\n\n' >> "$EN_COMBINED"
  fi
done

# Build English PDF
pandoc "$EN_COMBINED" \
  -o output/book5-retirement-en.pdf \
  --pdf-engine=xelatex \
  --template=templates/book-en.latex \
  --toc \
  --toc-depth=2

if [ $? -eq 0 ]; then
  echo "  ✓ English PDF built successfully"
else
  echo "  ✗ English PDF build failed"
fi

# ==========================================
# Summary
# ==========================================
echo ""
echo "=========================================="
echo "Build Complete!"
echo "=========================================="
echo ""
echo "Generated PDFs:"
ls -la output/*.pdf 2>/dev/null || echo "  No PDFs generated"

echo ""
echo "To open the PDFs:"
echo "  open output/book5-retirement-zh.pdf"
echo "  open output/book5-retirement-en.pdf"

#!/bin/bash

# Titus PDF Builder - CONSOLIDATED 2026 EDITION
# = Overview + Elder Wong systematic reception + 3 chapter files + indices appendix + references appendix
# Sources from books/bible/pauline-epistles/titus/
# Uses templates/pdf/titus.latex (Aegean Teal/Terracotta theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/pauline-epistles/titus"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
INDICES_FILE="$INPUT_DIR/98-appendix-indices.md"
REFS_FILE="$INPUT_DIR/99-appendix-references.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/titus-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/titus-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/titus.latex"

echo "=========================================="
echo "📖 Titus PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "提多書研讀"
subtitle: "Titus Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老式查經** — Thursday 查經筆記，整本聖經脈絡的深度領受

  • **John MacArthur** — 逐節解經 (The MacArthur New Testament Commentary)

  • **G. Campbell Morgan** — 屬靈組織分析 (*Living Messages of the Books of the Bible*)

  **經文版本**：中文和合本 (CUV) · English Standard Version (ESV)

  All rights reserved.
---

HEADER

# 1. Overview (strip its own frontmatter block: two '---' lines)
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "  Adding: 00-overview.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 2. Elder Wong systematic reception (structure-based deep study)
#    Demote headings one level so the whole study is a single top-level chapter
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——黃長老查經法 (Systematic Reception)\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 3. All 3 chapters in order
chapter_count=0
for i in 01 02 03; do
    found=""
    for f in "$INPUT_DIR/$i-"*.md; do
        if [ -f "$f" ]; then
            echo "  Adding: $(basename "$f")"
            tail -n +8 "$f" | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
            printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
            ((chapter_count++))
            found=1
            break
        fi
    done
    if [ -z "$found" ]; then
        echo "❌ Missing chapter file for prefix '$i-' in $INPUT_DIR — aborting build"
        exit 1
    fi
done

# 4. Indices appendix (Scripture Index + Key Themes Index)
if [ -f "$INDICES_FILE" ]; then
    echo "  Adding: 98-appendix-indices.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INDICES_FILE" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 5. References appendix
if [ -f "$REFS_FILE" ]; then
    echo "  Adding: 99-appendix-references.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$REFS_FILE" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters + overview + systematic study + indices + references)"
echo ""

# Convert markdown **bold** to \textbf{} INSIDE \paul{...} spans only.
# Pandoc treats \paul{...} as opaque raw LaTeX and does not re-parse markdown
# inside it, so **bold** markers would otherwise pass through literally.
echo "Converting bold markers inside \\paul{...} spans..."
COMBINED_MD_PATH="$COMBINED_MD" python3 <<'PYEOF'
import os, re

path = os.environ['COMBINED_MD_PATH']
with open(path, encoding='utf-8') as f:
    text = f.read()

out = []
i = 0
n = len(text)
tag = '\\paul{'
while i < n:
    idx = text.find(tag, i)
    if idx == -1:
        out.append(text[i:])
        break
    out.append(text[i:idx])
    j = idx + len(tag)
    depth = 1
    start_inner = j
    while j < n and depth > 0:
        if text[j] == '{':
            depth += 1
        elif text[j] == '}':
            depth -= 1
        j += 1
    inner = text[start_inner:j - 1]
    inner_conv = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', inner)
    out.append(tag + inner_conv + '}')
    i = j

with open(path, 'w', encoding='utf-8') as f:
    f.write(''.join(out))
PYEOF

echo "🔨 Generating PDF with titus.latex template..."

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

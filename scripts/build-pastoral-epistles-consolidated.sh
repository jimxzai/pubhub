#!/bin/bash

# Pastoral Epistles Combined PDF Builder - 2026 EDITION
# = Synthesis essay + 1 Timothy (overview+6ch) + 2 Timothy (overview+4ch) + Titus (overview+3ch) + merged references appendix
# This is a NEW synthesis volume alongside (not replacing) the three standalone book PDFs.
# Uses templates/pdf/pastoral-epistles.latex (Forest Green/Amber, Shepherd's Staff theme)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BASE_DIR="$PROJECT_ROOT/books/bible/pauline-epistles"
SYNTHESIS_FILE="$BASE_DIR/00-pastoral-epistles-synthesis.md"
INDICES_FILE="$BASE_DIR/98-appendix-indices.md"
REFS_FILE="$BASE_DIR/99-appendix-references.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/pastoral-epistles-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/pastoral-epistles-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/pastoral-epistles.latex"

echo "=========================================="
echo "📖 Pastoral Epistles Combined PDF (2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "三提合參"
subtitle: "盡職事奉的四大點 — A Combined Study of 1 Timothy, 2 Timothy, and Titus"
author: "PubHub 三書精讀系統"
date: "2026年7月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **本卷為合參綜合本，非逐字合併三本獨立研讀。**

  **三大核心資源整合：**

  • **黃長老 Thursday 查經筆記** — 真實的「盡職四大點」「三提合一」「清潔的良心」服事框架

  • **John MacArthur** — 逐節解經講道

  • **G. Campbell Morgan** — 屬靈組織分析

  All rights reserved.
---

HEADER

# 1. Synthesis essay (strip its own frontmatter block: two '---' lines)
if [ -f "$SYNTHESIS_FILE" ]; then
    echo "  Adding: 00-pastoral-epistles-synthesis.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$SYNTHESIS_FILE" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 2. Each book: overview + its chapters, in canonical reading order
add_book() {
    local book_dir="$1"
    local book_label="$2"
    shift 2
    local chapters=("$@")

    if [ -f "$book_dir/00-overview.md" ]; then
        echo "  Adding: $book_label/00-overview.md"
        awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$book_dir/00-overview.md" >> "$COMBINED_MD"
        printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    fi

    for i in "${chapters[@]}"; do
        local found=""
        for f in "$book_dir/$i-"*.md; do
            if [ -f "$f" ]; then
                echo "  Adding: $book_label/$(basename "$f")"
                tail -n +8 "$f" | sed 's/\^\([^\^]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
                printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
                ((chapter_count++))
                found=1
                break
            fi
        done
        if [ -z "$found" ]; then
            echo "❌ Missing chapter file for prefix '$i-' in $book_dir — aborting build"
            exit 1
        fi
    done
}

chapter_count=0
add_book "$BASE_DIR/1-timothy" "1-timothy" 01 02 03 04 05 06
add_book "$BASE_DIR/2-timothy" "2-timothy" 01 02 03 04
add_book "$BASE_DIR/titus" "titus" 01 02 03

# 3. Merged scripture/theme indices appendix
if [ -f "$INDICES_FILE" ]; then
    echo "  Adding: 98-appendix-indices.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$INDICES_FILE" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

# 4. Merged references appendix
if [ -f "$REFS_FILE" ]; then
    echo "  Adding: 99-appendix-references.md"
    awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$REFS_FILE" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
fi

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters + synthesis + 3 overviews + indices + references)"
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

echo "🔨 Generating PDF with pastoral-epistles.latex template..."

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

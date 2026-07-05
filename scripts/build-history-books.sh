#!/bin/bash
# ============================================================================
# History Books PDF Builder — Kings Edition
# 舊約歷史書精讀 — 撒母耳記上下・歷代志上下
# The Old Testament History Books — Israel's Story (Christ-Centered Study)
# Uses the history-books.latex template (XeLaTeX + ucharclasses)
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/samuel-chronicles"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/history-books-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/history-books-combined.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/history-books.latex"

echo "============================================"
echo " History Books PDF Builder — Kings Edition"
echo " 舊約歷史書精讀"
echo " Samuel I & II · Chronicles I & II"
echo "============================================"
echo ""
echo " Format   : 6×9\" Trade Paperback"
echo " Template : history-books.latex"
echo " Engine   : XeLaTeX + ucharclasses"
echo " Features : Hebrew/Greek fonts, Kings colour palette"
echo ""

# Verify template exists
if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    echo "       Expected: $TEMPLATE"
    exit 1
fi

# Verify input directory exists
if [ ! -d "$INPUT_DIR" ]; then
    echo "ERROR: Input directory not found: $INPUT_DIR"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# ── Compose combined markdown ────────────────────────────────
echo "Combining chapters..."

cat > "$COMBINED_MD" << 'HEADER'
---
title: "舊約歷史書精讀 — 以色列走過的路"
subtitle: "The Old Testament History Books — Israel's Story (Christ-Centered Study)"
author: "PubHub 三書精讀系統"
date: "2026年6月"
publisher: "三書精讀出版系統"
copyright: "Copyright © 2026 PubHub 三書精讀系統\nAll rights reserved.\n\n本書以黃長老查經風格為藍本，整合 John MacArthur 及 G. Campbell Morgan 解經洞見，以基督為中心研讀以色列歷史書。"
---

HEADER

# Strip YAML frontmatter helper — processes one file
strip_yaml() {
    awk 'BEGIN{skip=0; count=0}
         /^---$/ {
             count++
             if (count == 1) { skip=1; next }
             if (count == 2) { skip=0; next }
         }
         !skip { print }' "$1"
}

# ── Series overview (00) ────────────────────────────────────
for f in "$INPUT_DIR"/00-*.md; do
    [ -f "$f" ] || continue
    echo "  Adding: $(basename "$f")"
    strip_yaml "$f" >> "$COMBINED_MD"
    printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
done

# ── Main book files (01-06) ─────────────────────────────────
chapter_count=0
for i in 01 02 03 04 05 06 07 08 09 10; do
    for f in "$INPUT_DIR"/"$i"-*.md; do
        [ -f "$f" ] || continue
        echo "  Adding: $(basename "$f")"
        strip_yaml "$f" \
            | sed 's/\^\([0-9]*\)\^/\\textsuperscript{\1}/g' \
            >> "$COMBINED_MD"
        printf '\n\n\\pagebreak\n\n' >> "$COMBINED_MD"
        ((chapter_count++))
        break
    done
done

echo ""
echo " Chapters combined : $chapter_count"
echo " Total lines       : $(wc -l < "$COMBINED_MD")"
echo ""

# ── Post-processing ──────────────────────────────────────────
echo "Converting red-letter markers..."
sed -i '' \
    -e 's/<red>/\\jesus{/g' \
    -e 's/<\/red>/}/g' \
    "$COMBINED_MD"

echo "Stripping emojis..."
sed -i '' \
    -e 's/📖/(Book)/g' \
    -e 's/🙏/(Prayer)/g' \
    -e 's/💡/(Insight)/g' \
    -e 's/✝️/(Cross)/g' \
    -e 's/👑/(Crown)/g' \
    -e 's/⚔️/(Sword)/g' \
    -e 's/🏛️/(Temple)/g' \
    -e 's/📜/(Scroll)/g' \
    -e 's/🔑/(Key)/g' \
    -e 's/✅/(+)/g' \
    -e 's/❌/(x)/g' \
    -e 's/➡️/(→)/g' \
    -e 's/⬆️/(↑)/g' \
    -e 's/🌟/(★)/g' \
    -e 's/⭐/(★)/g' \
    -e 's/❤️/(Heart)/g' \
    -e 's/🕍/(Temple)/g' \
    -e 's/🗡️/(Sword)/g' \
    -e 's/🐑/(Sheep)/g' \
    -e 's/✓/(✓)/g' \
    "$COMBINED_MD"

# ── Generate PDF ─────────────────────────────────────────────
echo "Generating PDF (XeLaTeX)..."
echo ""

pandoc "$COMBINED_MD" \
    -o "$OUTPUT_PDF" \
    --pdf-engine=xelatex \
    --template="$TEMPLATE" \
    --from=markdown-superscript-subscript \
    --toc \
    --toc-depth=3 \
    --top-level-division=chapter \
    -V geometry:margin=0.75in

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "ERROR: pandoc/XeLaTeX failed (exit $EXIT_CODE)"
    echo "       Check LaTeX log above for details."
    exit $EXIT_CODE
fi

if [ -f "$OUTPUT_PDF" ]; then
    SIZE=$(ls -lh "$OUTPUT_PDF" | awk '{print $5}')
    PAGES=$(python3 -c "
import subprocess, sys
try:
    out = subprocess.check_output(['pdfinfo', '$OUTPUT_PDF'], stderr=subprocess.DEVNULL).decode()
    for line in out.splitlines():
        if 'Pages:' in line:
            print(line.split(':')[1].strip())
            sys.exit(0)
    print('?')
except:
    print('?')
" 2>/dev/null || echo "?")

    echo ""
    echo "============================================"
    echo " SUCCESS: History Books PDF Generated!"
    echo "============================================"
    echo ""
    echo "   Title    : 舊約歷史書精讀"
    echo "   Books    : 1 Samuel, 2 Samuel, 1 Chronicles, 2 Chronicles"
    echo "   Pages    : $PAGES"
    echo "   Size     : $SIZE"
    echo "   Output   : $OUTPUT_PDF"
    echo "   Chapters : $chapter_count"
    echo ""
    echo "   Content highlights:"
    echo "   - Kings meta-narrative (Eden → Saul → David → Jesus)"
    echo "   - Hebrew word studies with auto-rendered characters"
    echo "   - Psalms on the same map (Ps 51, 89, 132, 137, 126...)"
    echo "   - Elder Wong teaching points with probing questions"
    echo "   - MacArthur + G. Campbell Morgan commentary"
    echo "   - Prophets on the same map (Isaiah, Jeremiah, Ezekiel)"
    echo "============================================"
    echo ""

    # Open the PDF on macOS
    if command -v open &> /dev/null; then
        echo "Opening PDF..."
        open "$OUTPUT_PDF"
    fi
else
    echo "ERROR: PDF file not created despite exit 0"
    exit 1
fi

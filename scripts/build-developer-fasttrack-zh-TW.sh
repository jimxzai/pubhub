#!/bin/bash
# ============================================================================
# 加州開發商快速通道指南 — PDF Builder (繁體中文版)
# California Developer Fast Track Guide — Traditional Chinese Edition
# 8.5×11" Letter Size Professional Reference
# Uses the developer-fasttrack-zh-TW.latex template
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/biz-developer-fasttrack/california-zh-TW"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/developer-fasttrack-zh-TW-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/developer-fasttrack-zh-TW.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/developer-fasttrack-zh-TW.latex"

echo "============================================"
echo "加州開發商快速通道指南 (繁體中文版)"
echo "PDF Generator"
echo "============================================"
echo ""
echo "Format: 8.5×11\" Letter (Professional Reference)"
echo "Template: developer-fasttrack-zh-TW.latex"
echo ""

# Verify template exists
if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

# Verify input directory exists
if [ ! -d "$INPUT_DIR" ]; then
    echo "ERROR: Input directory not found: $INPUT_DIR"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# ============================================================================
# Helper: strip YAML frontmatter if present
# ============================================================================
strip_yaml() {
    local first_line
    first_line=$(head -1 "$1")
    if [ "$first_line" = "---" ]; then
        awk 'BEGIN{in_yaml=1; count=0}
             /^---$/{count++; if(count==2){in_yaml=0; next} else {next}}
             !in_yaml{print}' "$1"
    else
        cat "$1"
    fi
}

# Start combined markdown with YAML front matter
echo "Combining chapters..."
cat > "$COMBINED_MD" << 'HEADER'
---
title: "加州開發商快速通道指南"
subtitle: "住宅、酒店與模組化建造從業者實務指南"
author: "Jim Xiao"
date: "2026年2月"
publisher: "PubHub Publishing"
---

HEADER

# ============================================================================
# Function to add a chapter file
# ============================================================================
add_chapter() {
    local file="$1"
    echo "  Adding: $(basename "$file")"
    strip_yaml "$file" >> "$COMBINED_MD"
    printf '\n\n' >> "$COMBINED_MD"
}

# ============================================================================
# Front Matter: Preface
# ============================================================================
if [ -f "$INPUT_DIR/00-preface.md" ]; then
    add_chapter "$INPUT_DIR/00-preface.md"
fi

# ============================================================================
# Table of Contents
# ============================================================================
printf '\\setcounter{tocdepth}{3}\n\\tableofcontents\n\\clearpage\n\n' >> "$COMBINED_MD"

# ============================================================================
# Switch to main matter
# ============================================================================
printf '\\mainmatter\n\n' >> "$COMBINED_MD"

# ============================================================================
# Introduction
# ============================================================================
if [ -f "$INPUT_DIR/00-introduction.md" ]; then
    add_chapter "$INPUT_DIR/00-introduction.md"
fi

# Restore section numbering for numbered chapters
printf '\\setcounter{secnumdepth}{2}\n\n' >> "$COMBINED_MD"

# ============================================================================
# Part I: 加州規劃法基礎 (Ch 1-4)
# ============================================================================
printf '\\part{加州規劃法基礎}\n\n' >> "$COMBINED_MD"

chapter_count=0
for i in 01 02 03 04; do
    for file in "$INPUT_DIR"/ch${i}-*.md; do
        if [ -f "$file" ]; then
            add_chapter "$file"
            ((chapter_count++))
            break
        fi
    done
done

# ============================================================================
# Part II: CEQA — 加州環境品質法 (Ch 5-6)
# ============================================================================
printf '\\part{CEQA --- 加州環境品質法}\n\n' >> "$COMBINED_MD"

for i in 05 06; do
    for file in "$INPUT_DIR"/ch${i}-*.md; do
        if [ -f "$file" ]; then
            add_chapter "$file"
            ((chapter_count++))
            break
        fi
    done
done

# ============================================================================
# Part III: 土地細分 (Ch 7)
# ============================================================================
printf '\\part{土地細分}\n\n' >> "$COMBINED_MD"

for i in 07; do
    for file in "$INPUT_DIR"/ch${i}-*.md; do
        if [ -f "$file" ]; then
            add_chapter "$file"
            ((chapter_count++))
            break
        fi
    done
done

# ============================================================================
# Part IV: 酒店與飯店開發 (Ch 8-9)
# ============================================================================
printf '\\part{酒店與飯店開發}\n\n' >> "$COMBINED_MD"

for i in 08 09; do
    for file in "$INPUT_DIR"/ch${i}-*.md; do
        if [ -f "$file" ]; then
            add_chapter "$file"
            ((chapter_count++))
            break
        fi
    done
done

# ============================================================================
# Part V: 模組化建造 (Ch 10-12)
# ============================================================================
printf '\\part{模組化建造}\n\n' >> "$COMBINED_MD"

for i in 10 11 12; do
    for file in "$INPUT_DIR"/ch${i}-*.md; do
        if [ -f "$file" ]; then
            add_chapter "$file"
            ((chapter_count++))
            break
        fi
    done
done

# ============================================================================
# Part VI: 技術盡職調查 (Ch 13-14)
# ============================================================================
printf '\\part{技術盡職調查}\n\n' >> "$COMBINED_MD"

for i in 13 14; do
    for file in "$INPUT_DIR"/ch${i}-*.md; do
        if [ -f "$file" ]; then
            add_chapter "$file"
            ((chapter_count++))
            break
        fi
    done
done

# ============================================================================
# Part VII: 工具與財務分析 (Ch 15-16)
# ============================================================================
printf '\\part{工具與財務分析}\n\n' >> "$COMBINED_MD"

for i in 15 16; do
    for file in "$INPUT_DIR"/ch${i}-*.md; do
        if [ -f "$file" ]; then
            add_chapter "$file"
            ((chapter_count++))
            break
        fi
    done
done

# ============================================================================
# Appendices
# ============================================================================
printf '\\appendix\n\\part{附錄}\n\n' >> "$COMBINED_MD"

appendix_count=0
for appendix in "$INPUT_DIR"/appendix-*.md; do
    if [ -f "$appendix" ]; then
        add_chapter "$appendix"
        ((appendix_count++))
    fi
done

# ============================================================================
# Back Matter: Subject Index & Case Study Index
# ============================================================================
if [ -f "$INPUT_DIR/00-index.md" ]; then
    echo "  Adding: 00-index.md (as back matter index)"
    strip_yaml "$INPUT_DIR/00-index.md" \
        | sed '1{/^# /d;}' \
        | awk '/^## /,0' >> "$COMBINED_MD"
    printf '\n\n' >> "$COMBINED_MD"
fi

echo ""
echo "Combined markdown created"
echo "   Chapters: $chapter_count"
echo "   Appendices: $appendix_count"
echo "   Lines: $(wc -l < "$COMBINED_MD")"
echo ""

# Clean up markdown for LaTeX compatibility
echo "Cleaning up markdown for LaTeX..."

# Strip "Chapter X:" prefix from chapter headers
sed -i '' -E 's/^# Chapter [0-9]+: /# /g' "$COMBINED_MD"

# Strip "Appendix X:" prefix from appendix headers
sed -i '' -E 's/^# Appendix [A-Z]: /# /g' "$COMBINED_MD"

# Normalize ALL-CAPS titles to title case
sed -i '' 's/^# FRONTIER BUILDER CASE STUDIES & AI-AGILE STRATEGIES/# Frontier Builder Case Studies \& AI-Agile Strategies/' "$COMBINED_MD"
sed -i '' 's/^# PRO FORMA FINANCIAL DECISION FRAMEWORK/# Pro Forma Financial Decision Framework/' "$COMBINED_MD"
sed -i '' 's/^# PROFESSIONAL TEAM ASSEMBLY & ENGAGEMENT TIMING/# Professional Team Assembly \& Engagement Timing/' "$COMBINED_MD"

# Strip manual section numbers from sub-headers
sed -i '' -E 's/^(#{2,}) [A-Z0-9]+\.[0-9]+(\.[0-9]+)? /\1 /g' "$COMBINED_MD"
sed -i '' -E 's/^(#{2,}) [0-9]+[A-Z]\. /\1 /g' "$COMBINED_MD"

# Replace horizontal rule separators with gold-accented rule (skip YAML frontmatter)
sed -i '' '9,$ s/^---$/\\ornsep/' "$COMBINED_MD"

# Convert checkbox markers to LaTeX-friendly format
sed -i '' \
    -e 's/- \[ \]/- □/g' \
    "$COMBINED_MD"

# Remove emojis that might cause XeLaTeX issues
sed -i '' \
    -e 's/📖/(Book)/g' \
    -e 's/🏗️/(Construction)/g' \
    -e 's/🏨/(Hotel)/g' \
    -e 's/🏠/(House)/g' \
    -e 's/📋/(Checklist)/g' \
    -e 's/✅/(Check)/g' \
    -e 's/❌/(X)/g' \
    -e 's/⚠️/(Warning)/g' \
    -e 's/⚠/(Warning)/g' \
    -e 's/💡/(Insight)/g' \
    -e 's/🔑/(Key)/g' \
    -e 's/📝/(Note)/g' \
    -e 's/🎯/(Target)/g' \
    -e 's/✓/+/g' \
    -e 's/✗/X/g' \
    -e 's/→/->/g' \
    -e 's/←/<-/g' \
    -e 's/↑/^/g' \
    -e 's/↓/v/g' \
    -e 's/↔/<->/g' \
    -e 's/│/|/g' \
    -e 's/├/|-/g' \
    -e 's/└/\\-/g' \
    -e 's/┤/-|/g' \
    -e 's/┌/,-/g' \
    -e 's/┐/-,/g' \
    -e "s/┘/-'/g" \
    -e 's/─/-/g' \
    -e 's/━/=/g' \
    -e 's/═/=/g' \
    -e 's/▼/v/g' \
    -e 's/▲/^/g' \
    -e 's/►/>/g' \
    -e 's/◄/</g' \
    -e 's/□/ [ ] /g' \
    -e 's/■/[X]/g' \
    -e 's/×/x/g' \
    "$COMBINED_MD"

# Generate PDF
echo "Generating PDF with XeLaTeX..."
echo "(This may take 2-3 minutes for a large book with CJK fonts)"
echo ""

pandoc "$COMBINED_MD" \
    -o "$OUTPUT_PDF" \
    --pdf-engine=xelatex \
    --template="$TEMPLATE" \
    --from=markdown-smart-tex_math_dollars+pipe_tables+backtick_code_blocks+fenced_code_blocks \
    --top-level-division=chapter \
    --columns=80 \
    --no-highlight \
    -V documentclass=book \
    -V classoption=openany \
    -V classoption=twoside

if [ -f "$OUTPUT_PDF" ]; then
    SIZE=$(ls -lh "$OUTPUT_PDF" | awk '{print $5}')
    PAGES=$(pdfinfo "$OUTPUT_PDF" 2>/dev/null | grep Pages | awk '{print $2}' || echo "unknown")
    echo ""
    echo "============================================"
    echo "SUCCESS: 繁體中文版 PDF 生成完畢！"
    echo "============================================"
    echo ""
    echo "   Title: 加州開發商快速通道指南"
    echo "   Format: 8.5×11\" Letter (Professional Reference)"
    echo "   File: $OUTPUT_PDF"
    echo "   Size: $SIZE"
    echo "   Pages: $PAGES"
    echo "   Chapters: $chapter_count"
    echo "   Appendices: $appendix_count"
    echo ""
    echo "   Contents:"
    echo "   - Part I:   加州規劃法基礎 (Ch 1-4)"
    echo "   - Part II:  CEQA 加州環境品質法 (Ch 5-6)"
    echo "   - Part III: 土地細分 (Ch 7)"
    echo "   - Part IV:  酒店與飯店開發 (Ch 8-9)"
    echo "   - Part V:   模組化建造 (Ch 10-12)"
    echo "   - Part VI:  技術盡職調查 (Ch 13-14)"
    echo "   - Part VII: 工具與財務分析 (Ch 15-16)"
    echo "   - 附錄 A-J"
    echo "============================================"
    echo ""

    # Open the PDF
    if command -v open &> /dev/null; then
        echo "Opening PDF..."
        open "$OUTPUT_PDF"
    fi
else
    echo "FAILED: PDF not created"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check that XeLaTeX is installed: which xelatex"
    echo "  2. Check that Pandoc is installed: which pandoc"
    echo "  3. Check the combined markdown: $COMBINED_MD"
    echo "  4. Try running pandoc manually with --verbose flag"
    exit 1
fi

#!/bin/bash
# ============================================================================
# California Developer Fast Track Guide — PDF Builder
# A Practitioner's Guide to Residential, Hotel & Modular Development
# 8.5×11" Letter Size Professional Reference
# Uses the developer-fasttrack.latex template
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/biz-developer-fasttrack/california"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/developer-fasttrack-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/developer-fasttrack.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/developer-fasttrack.latex"

echo "============================================"
echo "California Developer Fast Track Guide"
echo "PDF Generator"
echo "============================================"
echo ""
echo "Format: 8.5×11\" Letter (Professional Reference)"
echo "Template: developer-fasttrack.latex"
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
# Helper: strip YAML frontmatter if present (lines between --- at top of file)
# These chapter files do NOT have YAML frontmatter, so we just cat them.
# Only the 00-index.md might have it.
# ============================================================================
strip_yaml() {
    # Check if file starts with ---
    local first_line
    first_line=$(head -1 "$1")
    if [ "$first_line" = "---" ]; then
        # Has YAML frontmatter — skip until second ---
        awk 'BEGIN{in_yaml=1; count=0}
             /^---$/{count++; if(count==2){in_yaml=0; next} else {next}}
             !in_yaml{print}' "$1"
    else
        # No YAML frontmatter — output everything
        cat "$1"
    fi
}

# Start combined markdown with YAML front matter
echo "Combining chapters..."
cat > "$COMBINED_MD" << 'HEADER'
---
title: "California Developer Fast Track Guide"
subtitle: "A Practitioner's Guide to Residential, Hotel & Modular Development in California"
author: "Jim Xiao"
date: "February 2026"
publisher: "PubHub Publishing"
---

HEADER

# Note: 00-index.md (Subject Index, Case Study Index) added at end of book

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
# Front Matter: Preface (before TOC, Roman numeral pages)
# ============================================================================
if [ -f "$INPUT_DIR/00-preface.md" ]; then
    add_chapter "$INPUT_DIR/00-preface.md"
fi

# ============================================================================
# Table of Contents (after Preface)
# ============================================================================
printf '\\setcounter{tocdepth}{3}\n\\tableofcontents\n\\clearpage\n\n' >> "$COMBINED_MD"

# ============================================================================
# Switch to main matter (Arabic page numbers start at 1)
# ============================================================================
printf '\\mainmatter\n\n' >> "$COMBINED_MD"

# ============================================================================
# Introduction (unnumbered, but Arabic page 1)
# ============================================================================
if [ -f "$INPUT_DIR/00-introduction.md" ]; then
    add_chapter "$INPUT_DIR/00-introduction.md"
fi

# Restore section numbering for numbered chapters
printf '\\setcounter{secnumdepth}{2}\n\n' >> "$COMBINED_MD"

# ============================================================================
# Part I: California Planning Law Foundation (Ch 1-4)
# ============================================================================
printf '\\part{California Planning Law Foundation}\n\n' >> "$COMBINED_MD"

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
# Part II: CEQA (Ch 5-6)
# ============================================================================
printf '\\part{CEQA --- California Environmental Quality Act}\n\n' >> "$COMBINED_MD"

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
# Part III: Subdivision (Ch 7)
# ============================================================================
printf '\\part{Subdivision}\n\n' >> "$COMBINED_MD"

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
# Part IV: Hotel & Hospitality Development (Ch 8-9)
# ============================================================================
printf '\\part{Hotel \\& Hospitality Development}\n\n' >> "$COMBINED_MD"

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
# Part V: Modular Construction (Ch 10-12)
# ============================================================================
printf '\\part{Modular Construction}\n\n' >> "$COMBINED_MD"

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
# Part VI: Technical Due Diligence (Ch 13-14)
# ============================================================================
printf '\\part{Technical Due Diligence}\n\n' >> "$COMBINED_MD"

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
# Part VII: Tools & Financial Analysis (Ch 15-16)
# ============================================================================
printf '\\part{Tools \\& Financial Analysis}\n\n' >> "$COMBINED_MD"

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
printf '\\appendix\n\\part{Appendices}\n\n' >> "$COMBINED_MD"

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
    # Extract only the Subject Index and Case Study sections (skip TOC/overview)
    strip_yaml "$INPUT_DIR/00-index.md" \
        | sed '1{/^# /d;}' \
        | awk '/^## Abbreviations & Acronyms/,0' >> "$COMBINED_MD"
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

# Strip "Chapter X:" prefix from chapter headers (LaTeX adds "Chapter X" automatically)
sed -i '' -E 's/^# Chapter [0-9]+: /# /g' "$COMBINED_MD"

# Strip "Appendix X:" prefix from appendix headers (LaTeX adds "Appendix X" automatically)
sed -i '' -E 's/^# Appendix [A-Z]: /# /g' "$COMBINED_MD"

# Normalize Appendix F & G ALL-CAPS titles to title case
sed -i '' 's/^# FRONTIER BUILDER CASE STUDIES & AI-AGILE STRATEGIES/# Frontier Builder Case Studies \& AI-Agile Strategies/' "$COMBINED_MD"
sed -i '' 's/^# PRO FORMA FINANCIAL DECISION FRAMEWORK/# Pro Forma Financial Decision Framework/' "$COMBINED_MD"
sed -i '' 's/^# PROFESSIONAL TEAM ASSEMBLY & ENGAGEMENT TIMING/# Professional Team Assembly \& Engagement Timing/' "$COMBINED_MD"

# Strip manual section numbers from sub-headers (e.g., "## 1.1 Title" -> "## Title")
# Handles patterns like 1.1, 2.3, A.1, B.10, F.4, etc.
sed -i '' -E 's/^(#{2,}) [A-Z0-9]+\.[0-9]+(\.[0-9]+)? /\1 /g' "$COMBINED_MD"
# Also strip patterns like "2A. " or "1A. " (number+letter+dot)
sed -i '' -E 's/^(#{2,}) [0-9]+[A-Z]\. /\1 /g' "$COMBINED_MD"

# Replace horizontal rule separators with gold-accented rule (skip YAML frontmatter lines 1-8)
sed -i '' '9,$ s/^---$/\\ornsep/' "$COMBINED_MD"

# Convert checkbox markers to LaTeX-friendly format
sed -i '' \
    -e 's/- \[ \]/- □/g' \
    "$COMBINED_MD"

# Remove any emojis that might cause XeLaTeX issues
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
    -e 's/┘/-'"'"'/g' \
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

# Replace Chinese characters that Palatino can't render
sed -i '' \
    -e 's/和合本修訂版/RCUV/g' \
    "$COMBINED_MD"

# Generate PDF
echo "Generating PDF with XeLaTeX..."
echo "(This may take 1-2 minutes for a large book)"
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
    echo "SUCCESS: Developer Fast Track PDF Generated!"
    echo "============================================"
    echo ""
    echo "   Title: California Developer Fast Track Guide"
    echo "   Format: 8.5×11\" Letter (Professional Reference)"
    echo "   File: $OUTPUT_PDF"
    echo "   Size: $SIZE"
    echo "   Pages: $PAGES"
    echo "   Chapters: $chapter_count"
    echo "   Appendices: $appendix_count"
    echo ""
    echo "   Contents:"
    echo "   - Part I:   CA Planning Law (Ch 1-4)"
    echo "   - Part II:  CEQA (Ch 5-6)"
    echo "   - Part III: Subdivision (Ch 7)"
    echo "   - Part IV:  Hotel & Hospitality (Ch 8-9)"
    echo "   - Part V:   Modular Construction (Ch 10-12)"
    echo "   - Part VI:  Technical Due Diligence (Ch 13-14)"
    echo "   - Part VII: Tools & Financial (Ch 15-16)"
    echo "   - Appendices A-I"
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

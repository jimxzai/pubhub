#!/bin/bash
# Build script for The AI-Powered One-Person Company
# O'Reilly Style LaTeX Book
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BOOK_DIR="$PROJECT_DIR/Book"
COVER_DIR="$PROJECT_DIR/Cover"
OUTPUT_DIR="$PROJECT_DIR/output"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Building: The AI-Powered One-Person Company${NC}"
echo -e "${GREEN}========================================${NC}"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check for required tools
check_tool() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed.${NC}"
        echo "Please install it first:"
        case "$1" in
            pdflatex|xelatex|lualatex)
                echo "  macOS: brew install --cask mactex"
                echo "  Ubuntu: sudo apt-get install texlive-full"
                ;;
            gs)
                echo "  macOS: brew install ghostscript"
                echo "  Ubuntu: sudo apt-get install ghostscript"
                ;;
        esac
        exit 1
    fi
}

check_tool "pdflatex"
check_tool "gs"

# Build function
build_latex() {
    local tex_file="$1"
    local output_name="$2"
    local work_dir="$(dirname "$tex_file")"

    echo -e "${YELLOW}Compiling: $tex_file${NC}"

    cd "$work_dir"

    # First pass
    pdflatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$(basename "$tex_file")" || {
        echo -e "${RED}First pass failed. Check the log file.${NC}"
        exit 1
    }

    # Second pass (for TOC, references)
    pdflatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$(basename "$tex_file")" || {
        echo -e "${RED}Second pass failed. Check the log file.${NC}"
        exit 1
    }

    echo -e "${GREEN}✓ Compiled: $output_name${NC}"
}

# Build the book
echo ""
echo -e "${YELLOW}Step 1: Building main book...${NC}"
build_latex "$BOOK_DIR/book.tex" "book.pdf"

# Build the cover (optional)
if [ -f "$COVER_DIR/cover.tex" ]; then
    echo ""
    echo -e "${YELLOW}Step 2: Building cover...${NC}"

    # Check if cover image exists, if not skip cover
    if [ -f "$PROJECT_DIR/images/cover-animal.png" ]; then
        build_latex "$COVER_DIR/cover.tex" "cover.pdf"

        # Merge cover and book
        echo ""
        echo -e "${YELLOW}Step 3: Merging cover and book...${NC}"
        gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite \
           -sOutputFile="$OUTPUT_DIR/ai-one-person-company-complete.pdf" \
           "$OUTPUT_DIR/cover.pdf" \
           "$OUTPUT_DIR/book.pdf"

        echo -e "${GREEN}✓ Complete book with cover: output/ai-one-person-company-complete.pdf${NC}"
    else
        echo -e "${YELLOW}Skipping cover (no cover-animal.png found)${NC}"
    fi
fi

# Clean up auxiliary files
echo ""
echo -e "${YELLOW}Cleaning up auxiliary files...${NC}"
cd "$OUTPUT_DIR"
rm -f *.aux *.log *.toc *.out *.lof *.lot *.bbl *.blg *.idx *.ind *.ilg 2>/dev/null || true

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Build complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Output files:"
ls -la "$OUTPUT_DIR"/*.pdf 2>/dev/null || echo "No PDF files generated."
echo ""
echo "To view the book:"
echo "  open $OUTPUT_DIR/book.pdf"

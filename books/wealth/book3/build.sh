#!/bin/bash
# Build script for Book 3: Jim's Investment Memo / 阿甘的投资备忘录
# Usage: ./build.sh [zh|en|all]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/output"

# Create output directory
mkdir -p "$OUTPUT_DIR"

build_zh() {
    echo "📚 Building Chinese version (阿甘的投资备忘录)..."
    node "$PROJECT_ROOT/scripts/build-pdf.js" \
        --format advisory-zh \
        --input "$SCRIPT_DIR/zh" \
        --output "$OUTPUT_DIR/advisory-zh.pdf" \
        --title "阿甘的投资备忘录" \
        --author "Jim Xiao" \
        --verbose
    echo "✓ Chinese PDF: $OUTPUT_DIR/advisory-zh.pdf"
}

build_en() {
    echo "📚 Building English version (Jim's Investment Memo)..."
    node "$PROJECT_ROOT/scripts/build-pdf.js" \
        --format advisory-en \
        --input "$SCRIPT_DIR/en" \
        --output "$OUTPUT_DIR/advisory-en.pdf" \
        --title "Jim's Investment Memo" \
        --author "Jim Xiao" \
        --verbose
    echo "✓ English PDF: $OUTPUT_DIR/advisory-en.pdf"
}

case "${1:-all}" in
    zh)
        build_zh
        ;;
    en)
        build_en
        ;;
    all)
        build_zh
        echo ""
        build_en
        ;;
    *)
        echo "Usage: $0 [zh|en|all]"
        echo "  zh  - Build Chinese version only"
        echo "  en  - Build English version only"
        echo "  all - Build both versions (default)"
        exit 1
        ;;
esac

echo ""
echo "✅ Build complete!"
echo "📁 Output directory: $OUTPUT_DIR"
ls -la "$OUTPUT_DIR"/*.pdf 2>/dev/null || echo "   (No PDF files yet)"

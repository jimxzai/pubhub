#!/bin/bash
# Philemon EPUB builder — accessibility / EU distribution path.
#
# WHY a separate output: the PDF is produced by XeLaTeX, which cannot emit a
# tagged (structurally accessible) PDF. Since June 2025 the European
# Accessibility Act requires accessible ebooks for EU sale, so the accessible
# edition has to be EPUB, not PDF. EPUB 3 carries real document structure,
# reflows, and works with screen readers.
#
# Reuses the combined markdown the PDF build already produces, so the two
# editions can never diverge in content.

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/philemon-consolidated.md"
EPUB_MD="$OUTPUT_DIR/philemon-epub.md"
OUTPUT_EPUB="$OUTPUT_DIR/philemon.epub"

if [ ! -f "$COMBINED_MD" ]; then
    echo "Run scripts/build-philemon-consolidated.sh first (it produces $COMBINED_MD)."
    exit 1
fi

echo "📱 Philemon EPUB"
echo ""

# The print source carries LaTeX that has no meaning in EPUB. Raw LaTeX is
# DROPPED by pandoc for non-LaTeX writers -- and \textcolor{..}{\textbf{TEXT}}
# would take TEXT with it, silently deleting every emphasised line in the book.
# Convert those to markdown emphasis first, then discard what is left.
COMBINED_MD_PATH="$COMBINED_MD" EPUB_MD_PATH="$EPUB_MD" python3 <<'PYEOF'
import os, re
src = open(os.environ['COMBINED_MD_PATH'], encoding='utf-8').read()

# \textcolor{X}{\textbf{...}} and \textcolor{X}{...} -> **...**
def strip_color(m):
    inner = m.group(2)
    inner = re.sub(r'\\textbf\{(.*?)\}', r'\1', inner, flags=re.S)
    inner = re.sub(r'\\large\s*', '', inner)
    return '**' + inner.strip() + '**'
prev = None
while prev != src:                      # nested spans
    prev = src
    src = re.sub(r'\\textcolor\{([A-Za-z]+)\}\{((?:[^{}]|\{[^{}]*\})*)\}',
                 strip_color, src, flags=re.S)

src = re.sub(r'\\begin\{center\}(.*?)\\end\{center\}', r'\1', src, flags=re.S)
src = re.sub(r'^```\{=latex\}.*?^```\s*$', '', src, flags=re.S | re.M)   # tikz, \sectiondiv, \newpage
src = re.sub(r'\\textsuperscript\{([^}]*)\}', r'^\1^', src)
src = re.sub(r'\\(newpage|clearpage|cleardoublepage|frontmatter|mainmatter|sectiondiv|pagebreak)\b', '', src)
src = re.sub(r'\\rule\{[^}]*\}\{[^}]*\}', '', src)
src = re.sub(r'\n{4,}', '\n\n\n', src)
open(os.environ['EPUB_MD_PATH'], 'w', encoding='utf-8').write(src)
print("  EPUB source prepared: %d lines" % src.count('\n'))
PYEOF

pandoc "$EPUB_MD" \
    -o "$OUTPUT_EPUB" \
    --from=markdown+superscript \
    --to=epub3 \
    --toc --toc-depth=2 \
    --split-level=1 \
    --metadata title="腓利門書研讀：恩典的懷抱" \
    --metadata subtitle="Philemon: The Embrace of Grace" \
    --metadata author="三書精讀出版系統 / PubHub" \
    --metadata lang="zh-Hant" \
    --metadata date="2026" \
    --metadata rights="Scripture quotations are in the public domain: 和合本 (1919); World English Bible (eBible.org)."

if [ -f "$OUTPUT_EPUB" ]; then
    echo ""
    echo "✅ $OUTPUT_EPUB  ($(ls -lh "$OUTPUT_EPUB" | awk '{print $5}'))"
    command -v epubcheck >/dev/null 2>&1 && epubcheck "$OUTPUT_EPUB" || \
      echo "   (install epubcheck to validate: brew install epubcheck)"
else
    echo "❌ EPUB not produced"; exit 1
fi

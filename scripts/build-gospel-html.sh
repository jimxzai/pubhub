#!/bin/bash

# Gospel of John HTML Builder
# Generates beautiful HTML that can be printed to PDF from browser

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-john"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-john-combined.md"
OUTPUT_HTML="$OUTPUT_DIR/gospel-of-john.html"

echo "========================================="
echo "📖 Gospel of John HTML Generator"
echo "========================================="
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Combine all markdown files
echo "📝 Combining markdown files..."
cat > "$COMBINED_MD" << 'HEADER'
---
title: "約翰福音研讀"
subtitle: "Gospel of John Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年1月"
---

HEADER

# Add overview
if [ -f "$INPUT_DIR/00-overview.md" ]; then
    echo "" >> "$COMBINED_MD"
    tail -n +2 "$INPUT_DIR/00-overview.md" >> "$COMBINED_MD"
fi

# Add all chapter files in order
for i in {01..21}; do
    chapter_file=$(ls "$INPUT_DIR/$i-"*.md 2>/dev/null | head -1)
    if [ -f "$chapter_file" ]; then
        echo "   Adding Chapter $i: $(basename "$chapter_file")"
        echo "" >> "$COMBINED_MD"
        echo "---" >> "$COMBINED_MD"
        echo "" >> "$COMBINED_MD"
        tail -n +2 "$chapter_file" >> "$COMBINED_MD"
    fi
done

echo ""
echo "✅ Combined markdown: $(wc -l < "$COMBINED_MD") lines"
echo ""

# Generate HTML with beautiful styling
echo "🎨 Generating HTML..."

pandoc "$COMBINED_MD" \
    -o "$OUTPUT_HTML" \
    --standalone \
    --toc \
    --toc-depth=2 \
    --number-sections \
    --css=https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown.min.css \
    --metadata title="約翰福音研讀 - Gospel of John Deep Study" \
    --template=<(cat << 'TEMPLATE'
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>$title$</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      line-height: 1.8;
      max-width: 900px;
      margin: 0 auto;
      padding: 40px 20px;
      background: #f5f5f5;
    }
    .container {
      background: white;
      padding: 60px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      border-radius: 8px;
    }
    h1 {
      color: #2c3e50;
      border-bottom: 3px solid #3498db;
      padding-bottom: 15px;
      font-size: 2.5em;
    }
    h2 {
      color: #34495e;
      margin-top: 40px;
      border-left: 4px solid #3498db;
      padding-left: 15px;
    }
    h3 {
      color: #555;
      margin-top: 30px;
    }
    blockquote {
      border-left: 5px solid #3498db;
      padding: 15px 25px;
      margin: 25px 0;
      background: #f8f9fa;
      font-style: italic;
      color: #555;
    }
    code {
      background: #f4f4f4;
      padding: 2px 6px;
      border-radius: 3px;
      font-family: "Menlo", "Monaco", "Courier New", monospace;
      font-size: 0.9em;
    }
    pre {
      background: #2c3e50;
      color: #ecf0f1;
      padding: 20px;
      border-radius: 5px;
      overflow-x: auto;
    }
    pre code {
      background: none;
      color: inherit;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    th, td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    th {
      background: #3498db;
      color: white;
    }
    tr:hover {
      background: #f5f5f5;
    }
    #TOC {
      background: #f8f9fa;
      padding: 25px;
      border-radius: 5px;
      margin-bottom: 40px;
      border: 1px solid #e0e0e0;
    }
    #TOC ul {
      list-style-type: none;
      padding-left: 0;
    }
    #TOC li {
      margin: 8px 0;
    }
    #TOC a {
      color: #3498db;
      text-decoration: none;
    }
    #TOC a:hover {
      text-decoration: underline;
    }
    .title-block {
      text-align: center;
      margin-bottom: 50px;
      padding-bottom: 30px;
      border-bottom: 2px solid #e0e0e0;
    }
    .title-block h1 {
      border: none;
      font-size: 3em;
      color: #2c3e50;
    }
    .title-block .subtitle {
      font-size: 1.5em;
      color: #7f8c8d;
      font-style: italic;
    }
    .title-block .author {
      margin-top: 20px;
      color: #95a5a6;
    }
    hr {
      border: none;
      border-top: 2px solid #e0e0e0;
      margin: 40px 0;
    }
    @media print {
      body {
        background: white;
        padding: 0;
      }
      .container {
        box-shadow: none;
        padding: 0;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="title-block">
      <h1>約翰福音研讀</h1>
      <div class="subtitle">Gospel of John Deep Study</div>
      <div class="author">PubHub 三書精讀系統 | 2026年1月</div>
    </div>
$if(toc)$
<nav id="$idprefix$TOC" role="doc-toc">
<h2>目錄 (Table of Contents)</h2>
$toc$
</nav>
$endif$
$body$
  </div>
</body>
</html>
TEMPLATE
)

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "✅ HTML Generated Successfully!"
    echo "========================================="
    echo ""
    echo "📄 File: $OUTPUT_HTML"
    echo "📊 Size: $(du -h "$OUTPUT_HTML" | cut -f1)"
    echo ""
    echo "🖨️  To convert to PDF:"
    echo "   1. Open in browser:"
    echo "      open \"$OUTPUT_HTML\""
    echo "   2. Press Cmd+P (Print)"
    echo "   3. Save as PDF"
    echo ""
    echo "   Or use this command:"
    echo "      /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --headless --print-to-pdf=\"$OUTPUT_DIR/gospel-of-john-print.pdf\" \"file://$OUTPUT_HTML\""
    echo ""
else
    echo "❌ HTML generation failed"
    exit 1
fi

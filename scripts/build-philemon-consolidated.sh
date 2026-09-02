#!/bin/bash
# Philemon PDF Builder — CONSOLIDATED 2026 EDITION
# 腓利門書研讀：恩典的懷抱
#
# Book-level spine (Gospel-of-John standard):
#   前言 → 卷首·定位 → 全書領受總綱 → 第一卷 經文逐段(1-7)
#   → 第二~七卷 主題/文學(8-26) → 卷末 → 跋 → 讀書會手冊 → 附錄 → 索引
#
# Sources from books/bible/1philimon/ ; template templates/pdf/philemon-study.latex
# NOTE: outline.md is a historical working draft and is deliberately NOT included;
#       its still-useful material lives in appendix-10 and appendix-11.

export PATH="/Library/TeX/texbin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/1philimon"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/philemon-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/philemon-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/philemon-study.latex"

echo "=========================================="
echo "📖 Philemon PDF (CONSOLIDATED 2026)"
echo "   腓利門書研讀：恩典的懷抱"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "腓利門書研讀"
subtitle: "恩典的懷抱 — Philemon Deep Study, 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
---

HEADER

# Strip a leading YAML frontmatter block (two '---' lines), and drop any
# trailing blank lines plus a trailing horizontal rule.
#
# The trailing rule matters: '---' at the end of a file becomes a \sectiondiv
# (a decorative cross) with no content after it, which lands alone on a fresh
# page and produces a near-empty page carrying a running head and folio.
# 23 of the source files ended that way.
strip_fm() {
    awk '
      BEGIN { c = 0; n = 0 }
      NR == 1 && $0 == "---" { c = 1; next }
      c == 1 && $0 == "---"  { c = 2; next }
      c != 1 { buf[n++] = $0 }
      END {
        while (n > 0 && buf[n-1] ~ /^[[:space:]]*$/) n--          # trailing blanks
        if (n > 0 && buf[n-1] == "---") {                          # trailing rule
          n--
          while (n > 0 && buf[n-1] ~ /^[[:space:]]*$/) n--
        }
        for (i = 0; i < n; i++) print buf[i]
      }' "$1"
}

# add a file at chapter level (its own top-level '#' stays a chapter)
add_file() {
    local f="$1"
    if [ ! -f "$f" ]; then
        echo "❌ Missing: $f — aborting build"
        exit 1
    fi
    echo "  Adding: $(basename "$f")"
    strip_fm "$f" | sed 's/\^\([0-9:]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
}

# add a file demoted one level (used for front matter that should not be a chapter)
add_front() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding (front matter): $(basename "$f")"
    strip_fm "$f" | sed 's/^# /## /' \
        | sed 's/\^\([0-9:]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
}

# ---- Front matter (roman folios) --------------------------------------------
# Trade order: half-title / title / copyright (all in the template)
#   -> dedication -> contents -> preface -> \mainmatter
# The template hands the front matter off to us here so the dedication can
# precede the contents; it used to land after them, inside main matter.
printf '```{=latex}\n\\frontmatter\n```\n\n' >> "$COMBINED_MD"
add_front "$INPUT_DIR/dedication.md"
printf '```{=latex}\n\\cleardoublepage\n{\\color{DeepBlue}\\tableofcontents}\n\\cleardoublepage\n```\n\n' >> "$COMBINED_MD"
add_front "$INPUT_DIR/preface.md"
printf '```{=latex}\n\\mainmatter\n```\n\n' >> "$COMBINED_MD"

# ---- 卷首 · 定位 -------------------------------------------------------------
add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-philemon-position.md"
add_file "$INPUT_DIR/00b-usefulness-spine.md"

# ---- 全書領受總綱 ------------------------------------------------------------
add_file "$INPUT_DIR/elder-wong-systematic-study.md"

# ---- 第一卷：經文逐段研讀 (1-7) ----------------------------------------------
printf '\n# 第一卷 · 經文逐段研讀 (Part One: Verse by Verse)\n\n' >> "$COMBINED_MD"
printf '腓利門書二十五節，逐段走完一遍。先讀經文，再讀回聲。\n\n\\newpage\n\n' >> "$COMBINED_MD"
exposition_count=0
for i in 01 02 03 04 05 06 07; do
    found=""
    for f in "$INPUT_DIR/$i-"*.md; do
        [ -f "$f" ] || continue
        add_file "$f"
        exposition_count=$((exposition_count+1))
        found=1
        break
    done
    [ -n "$found" ] || { echo "❌ Missing exposition chapter '$i-*' — aborting"; exit 1; }
done

# ---- 第二~七卷：主題／文學研讀 (8-26) ----------------------------------------
printf '\n# 第二卷至第七卷 · 主題與文學研讀 (Parts Two–Seven: Themes and Echoes)\n\n' >> "$COMBINED_MD"
printf '把這封信的四個主題——罪、律法、恩典、和好——放進兩部世界文學與當代處境裡回響。\n\n\\newpage\n\n' >> "$COMBINED_MD"
theme_count=0
for i in 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26; do
    found=""
    for f in "$INPUT_DIR/$i-"*.md; do
        [ -f "$f" ] || continue
        add_file "$f"
        theme_count=$((theme_count+1))
        found=1
        break
    done
    [ -n "$found" ] || { echo "❌ Missing thematic chapter '$i-*' — aborting"; exit 1; }
done

# ---- 卷末 · 跋 ---------------------------------------------------------------
add_file "$INPUT_DIR/99-the-open-door.md"
add_file "$INPUT_DIR/999-afterword.md"

# ---- 讀書會手冊 ---------------------------------------------------------------
add_file "$INPUT_DIR/study-guide.md"

# ---- 附錄 --------------------------------------------------------------------
appendix_count=0
for i in 01 02 03 04 05 06 07 08 09 10 11 12; do
    for f in "$INPUT_DIR/appendix-$i-"*.md; do
        [ -f "$f" ] || continue
        add_file "$f"
        appendix_count=$((appendix_count+1))
        break
    done
done

# ---- 索引 --------------------------------------------------------------------
add_file "$INPUT_DIR/index.md"

echo ""
echo "✅ Combined markdown: $COMBINED_MD"
echo "   $(wc -l < "$COMBINED_MD") lines | 經文章 $exposition_count | 主題章 $theme_count | 附錄 $appendix_count"
echo ""

# Emoji / arrow normalisation for XeLaTeX (the CJK fonts carry no emoji glyphs)
echo "Normalising emoji and arrows..."
sed -i '' \
    -e 's/📖/(Book)/g' -e 's/🙏/(Prayer)/g' -e 's/💡/(Insight)/g' \
    -e 's/✝️/(Cross)/g' -e 's/🕊️/(Dove)/g' -e 's/⭐/(Star)/g' -e 's/🌟/(Star)/g' \
    -e 's/❤️/(Heart)/g' -e 's/💖/(Heart)/g' -e 's/🔑/(Key)/g' -e 's/🎯/(Target)/g' \
    -e 's/📝/(Note)/g' -e 's/✅/(Check)/g' -e 's/❌/(X)/g' -e 's/🤖/(AI)/g' \
    -e 's/🌙/(Moon)/g' -e 's/☀️/(Sun)/g' -e 's/🌊/(Wave)/g' -e 's/🍞/(Bread)/g' \
    -e 's/🍷/(Wine)/g' -e 's/🏛️/(Temple)/g' -e 's/⛪/(Church)/g' -e 's/🗣️/(Speaking)/g' \
    -e 's/👁️/(Eye)/g' -e 's/🐑/(Sheep)/g' -e 's/🍇/(Grapes)/g' \
    -e 's/✓/+/g' -e 's/→/->/g' \
    "$COMBINED_MD"

# Horizontal rules become decorative cross dividers (skip the YAML header)
echo "Converting section dividers..."
awk 'NR<=10{print;next} /^---$/{print ""; print "```{=latex}"; print "\\sectiondiv"; print "```"; print ""; next} {print}' \
    "$COMBINED_MD" > "${COMBINED_MD}.tmp" && mv "${COMBINED_MD}.tmp" "$COMBINED_MD"

echo "🔨 Generating PDF with philemon-study.latex template..."
echo ""

# --verbose is load-bearing, not chatter: without it pandoc swallows the whole
# xelatex log and every grep-the-log check (here and in driver.sh) passes
# vacuously. See scripts/lib/latex-check.sh.
source "$SCRIPT_DIR/lib/latex-check.sh"
LATEX_LOG="${OUTPUT_PDF%.pdf}-build.log"
pandoc "$COMBINED_MD" \
    -o "$OUTPUT_PDF" \
    --verbose \
    --pdf-engine=xelatex \
    --template="$TEMPLATE" \
    --from=markdown-superscript-subscript \
    --toc \
    --toc-depth=1 \
    --top-level-division=chapter > "$LATEX_LOG" 2>&1
PANDOC_EXIT=$?

latex_build_report "$PANDOC_EXIT" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1

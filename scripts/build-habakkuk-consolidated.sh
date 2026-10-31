#!/bin/bash

# Habakkuk PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + orientation (overview / position / order of revelation)
#   + 7 chapters of Habakkuk in 5 sections (one part divider per step of the spine)
#   + 卷末 (systematic reception) + appendices + afterword
# Sources from books/bible/habakkuk/ (老弟兄 methodology + Calvin + Henry + Morgan
# + Augustine, CUV + NASB 1995 scripture; no MacArthur — gty.org has no Habakkuk series).
# Modeled on scripts/build-obadiah-consolidated.sh (unnumbered front/back matter so
# the seven chapters number 1..7; part dividers carry the spine:
# 「啟示的次序·第N步」 + 貫穿的線 table).
# Uses templates/pdf/habakkuk.latex (night-watch indigo / gold, full-bleed front and back covers).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/habakkuk"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/habakkuk-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/habakkuk-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/habakkuk.latex"

echo "=========================================="
echo "📖 Habakkuk PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "哈巴谷書研讀"
subtitle: "The Book of Habakkuk Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **資源整合：**

  • **老弟兄查經方法論之應用**（倉庫中沒有老弟兄以哈巴谷書為題的查經記錄，詳見附錄〈引用出處總表〉的誠實聲明）

  • **John Calvin** — *Commentaries on the Twelve Minor Prophets*, vol. 4（Habakkuk, Zephaniah, Haggai），tr. John Owen（公有領域）

  • **Matthew Henry** — *An Exposition of the Old and New Testament*（公有領域）

  • **G. Campbell Morgan** — *Living Messages of the Books of the Bible*（公有領域）

  • **Augustine** — *The City of God*, Book 18, tr. Marcus Dods（公有領域）

  • 本書沒有 John MacArthur 的引文：gty.org 沒有以哈巴谷書為題的講道系列

  **你心裏的「要到幾時」，向神說過嗎？**

  「然而，我要因耶和華歡欣，因救我的神喜樂。」（哈3:18）

  **經文版權聲明 (Scripture Copyright Notices)**

  2026 年 10 月 · 初版。本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本，屬公有領域；逐節核對來源見附錄〈引用出處總表〉。

  Scripture quotations taken from the New American Standard Bible® (NASB),
  Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. Used by
  permission. All rights reserved. lockman.org
---

HEADER

chapter_count=0

# Strip the 7-line YAML front matter, convert ^n^ / ^24-25^ verse markers to
# \textsuperscript{}{} (the trailing {} keeps a digit from abutting a following
# \textbf{ — see build-2-peter-consolidated.sh for the root cause).
emit() {
    tail -n +8 "$1" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}{}/g'
}

# A numbered chapter (the seven chapters of Habakkuk).
add_file() {
    local f="$1"
    [ -f "$f" ] || { echo "❌ Missing file: $1 — aborting build"; exit 1; }
    echo "  Adding: $(basename "$f")"
    emit "$f" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Front/back matter: first H1 marked unnumbered so it does not consume a
# chapter number.
add_front() {
    local f="$1"
    [ -f "$f" ] || { echo "❌ Missing file: $1 — aborting build"; exit 1; }
    echo "  Adding (unnumbered): $(basename "$f")"
    emit "$f" \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); if($0 !~ /\{\.unnumbered\}$/) $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Part divider. $2 is the one-line description (carries 「啟示的次序·第N步」);
# optional $3-$5 add the 貫穿的線 / 鑰節 / 貫穿的問題 table.
# printf '%s' (not %b) on purpose: descriptions are plain text, and %b would
# turn a literal backslash sequence into a control character.
add_volume() {
    printf '# %s {.unnumbered}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| | |\n|---|---|\n| **貫穿的線** | %s |\n| **鑰節** | %s |\n| **貫穿的問題** | %s |\n' \
            "$3" "$4" "$5" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

add_chapter() {
    local f
    for f in "$INPUT_DIR/$1-"*.md; do
        [ -f "$f" ] && { add_file "$f"; return 0; }
    done
    echo "❌ Missing chapter file for prefix '$1-' in $INPUT_DIR — aborting build"
    exit 1
}

# 前言
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這三章：地圖、座標、骨幹——啟示的次序與神的計劃。"
add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-habakkuk-position.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# ============================================================
# 正文 · 五步（七章）
# ============================================================
add_volume "第一步 · 哈巴谷書 1:1-4 節 (Step One)" \
    "啟示的次序·第一步：神讓先知先開口——三項控告被收進正典，沒有刪，沒有責備：你不應允、你還不拯救、你為何使我看見。" \
    "**不聽、不救、使我看見**——先知的三項控告" \
    "2節「你不應允，要到幾時呢？」" \
    "我最想問神的那一個「要到幾時」，我對祂說出口了嗎？"
add_chapter 01

add_volume "第二步 · 哈巴谷書 1:5-11 節 (Step Two)" \
    "啟示的次序·第二步：神的回答比問題更大——「我行一件事」，興起迦勒底人；雖有人告訴你們，你們總是不信。" \
    "**我行**——神在做的事，比人所求的更大" \
    "5節「在你們的時候，我行一件事，雖有人告訴你們，你們總是不信」" \
    "神若用我不能接受的方式回答我，我還認得出那是祂嗎？"
add_chapter 02

add_volume "第三步 · 哈巴谷書 1:12-2:1 節 (Step Three)" \
    "啟示的次序·第三步：先知再問，然後不再追問——你眼目清潔，為何看著不理？他站上守望所，看祂對我說甚麼話。" \
    "**看**——從「為何使我看見」到「我要觀看」" \
    "2:1「我要站在守望所，立在望樓上觀看」" \
    "我的問題問完之後，我站在哪裏？"
add_chapter 03

add_volume "第四步 · 哈巴谷書 2:2-20 節 (Step Four)" \
    "啟示的次序·第四步：神再次開口——寫下異象；雖然遲延，還要等候；義人因信得生。然後是五個禍哉，和一個肅靜。" \
    "**義人**——從被圍困（1:4）到必活（2:4）；**強暴**——從先知的呼喊到神的判詞（2:8、2:17）" \
    "2:4「惟義人因信得生」" \
    "我在等候的時候，靠甚麼活？"
add_chapter 04
add_chapter 05

add_volume "第五步 · 哈巴谷書 3:1-19 節 (Step Five)" \
    "啟示的次序·第五步，也是全書的終點：先知聽見了——禱告、神來了、然而歡欣；三個動詞全部回來，處境仍在，人站在高處。" \
    "**聽見、拯救、看見**——三個動詞，在第三章全部回來" \
    "3:18「然而，我要因耶和華歡欣，因救我的神喜樂」" \
    "我的「然而」，說在哪一句後面？"
add_chapter 06
add_chapter 07

# ============================================================
# 卷末 · 全書領受總綱
# ============================================================
add_volume "卷末 · 回望 (Looking Back)" \
    "五步讀完，把全書的領受收攏成一張圖——先知從「要到幾時」走到「然而」，我們也要看見那位把整個問題帶進十字架、又走出來的主。"

# The study file is a synthesis OF the five steps, so it sits after them
# (as in Jude), not in the front matter. No YAML: first line is its H1.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——老弟兄查經法 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}{}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
else
    echo "❌ Missing file: $STUDY_FILE — aborting build"
    exit 1
fi

# ============================================================
# 附錄
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引、讀經計劃、引用出處總表——供查閱、跨章對照，並如實交代每一處引句的查證方式。"
add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/96-appendix-reading-plan.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — last content file: no trailing \newpage (the colophon opens its own page).
[ -f "$INPUT_DIR/999-afterword.md" ] || { echo "❌ Missing file: $INPUT_DIR/999-afterword.md — aborting build"; exit 1; }
echo "  Adding (unnumbered): 999-afterword.md"
emit "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); if($0 !~ /\{\.unnumbered\}$/) $0=$0" {.unnumbered}"; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count sections)"
echo ""

# Wrap Greek runs in an explicit {\greekfont …} group passed through pandoc as
# raw LaTeX (see build-2-peter-consolidated.sh for why ucharclasses alone is
# not trusted with bold spans, and why the group must be a `…`{=latex} span —
# a bare {…} is escaped by pandoc into an unscoped font switch). Chapter
# markdown therefore carries plain Greek, never a hand-written wrap.
echo "Wrapping Greek Unicode runs in {\\greekfont ...}..."
COMBINED_MD_PATH="$COMBINED_MD" python3 <<'PYEOF'
import os, re
path = os.environ['COMBINED_MD_PATH']
text = open(path, encoding='utf-8').read()
# Skip anything already inside a backtick span.
parts = re.split(r'(`[^`]*`(?:\{=latex\})?)', text)
greek_run = re.compile(r'[Ͱ-Ͽἀ-῿]+(?: [Ͱ-Ͽἀ-῿]+)*')
n = 0
for i in range(0, len(parts), 2):
    def wrap(m):
        global n
        n += 1
        return '`{\\greekfont ' + m.group(0) + '}`{=latex}'
    parts[i] = greek_run.sub(wrap, parts[i])
open(path, 'w', encoding='utf-8').write(''.join(parts))
print(f"  Wrapped {n} Greek run(s)")
PYEOF

echo "🔨 Generating PDF with habakkuk.latex template..."

# --verbose is load-bearing: without it pandoc swallows the xelatex log and
# every grep-the-log check (here and in driver.sh) passes vacuously.
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

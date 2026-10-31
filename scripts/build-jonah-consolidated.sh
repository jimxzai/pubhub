#!/bin/bash

# Jonah PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + orientation (overview / position / order of revelation)
#   + 8 sections of Jonah in 4 parts (one part divider per step of the spine)
#   + 卷末 (systematic reception) + appendices + afterword
# Sources from books/bible/Jonah/ (老弟兄 methodology + Augustine + Calvin +
# Matthew Henry + Morgan, CUV + NASB 1995 scripture). No MacArthur: he has no
# Jonah series on gty.org.
# Modeled on scripts/build-jonah-consolidated.sh, itself on build-2-peter-consolidated.sh (unnumbered front/back
# matter so the five sections number 1..5) and scripts/build-james-consolidated.sh
# (part dividers carrying the spine: 「啟示的次序·第N步」 + 貫穿的線 table).
# Uses templates/pdf/jonah.latex (deep sea teal / gold; Revelation-style full-bleed covers).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/Jonah"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/jonah-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/jonah-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/jonah.latex"

echo "=========================================="
echo "📖 Jonah PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "約拿書研讀"
subtitle: "The Book of Jonah Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **資源整合：**

  • **老弟兄查經方法論之應用**（倉庫中沒有老弟兄以約拿書為題的查經記錄，詳見附錄〈引用出處總表〉的誠實聲明）

  • **奧古斯丁** — *Letter 102*（《尼西亞及後尼西亞教父》第一輯第一冊，公有領域）

  • **John Calvin** — *Commentaries on the Twelve Minor Prophets*, vol. 3（公有領域）

  • **Matthew Henry** — *Commentary on the Whole Bible*（公有領域）

  • **G. Campbell Morgan** — *An Exposition of the Whole Bible*（短引，每處不逾兩句；版權狀態見附錄〈引用出處總表〉）

  • **John MacArthur** — 無約拿書逐節講道可引，本書不列

  **神的話兩次臨到，神的問題留在最後**

  「何況這尼尼微大城，其中不能分辨左手右手的有十二萬多人，並有許多牲畜，我豈能不愛惜呢？」（拿4:11）

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

# A numbered chapter (the eight sections of Jonah).
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
add_front "$INPUT_DIR/00a-jonah-position.md"
add_front "$INPUT_DIR/00b-revelation-order.md"

# ============================================================
# 正文 · 四步
# ============================================================
add_volume "第一步 · 約拿書 1:1-16 (Step One)" \
    "啟示的次序·第一步：神先開口，也先動手——話臨到約拿；約拿起來逃，神就使海中起大風，風、籤、海都聽從，連水手也認識了耶和華，只有先知不聽。" \
    "**神先開口，也先動手**——凡受造的都聽從這句話，只有受託的人往反方向走" \
    "1:2「你起來往尼尼微大城去」" \
    "神的話臨到我的時候，我是「起來，去」，還是「起來，逃」？"
add_chapter 01
add_chapter 02
add_chapter 03

add_volume "第二步 · 約拿書 1:17-2:10 (Step Two)" \
    "啟示的次序·第二步：預備在先，禱告在後——大魚是神「安排」的，在約拿開口以前就已經在那裏；禱告出自魚腹，結論只有一句：「救恩出於耶和華。」" \
    "**安排在先，禱告在後**——救恩不是被呼求「換」來的，是先預備好的" \
    "2:9「救恩出於耶和華」" \
    "我的禱告，是在換取拯救，還是在認出拯救已經先到了？"
add_chapter 04

add_volume "第三步 · 約拿書 3:1-10 (Step Three)" \
    "啟示的次序·第三步：話二次臨到——神重新差遣逃跑的先知，不加責備；尼尼微悔改，神看見他們的行為，就後悔，不降所說的災。" \
    "**第二次**——差遣可以重來，審判也可以收回" \
    "3:10「神察看他們的行為，見他們離開惡道，他就後悔」" \
    "我相信神給人第二次機會，包括我不喜歡的那些人嗎？"
add_chapter 05
add_chapter 06

add_volume "第四步 · 約拿書 4:1-11 (Step Four)" \
    "啟示的次序·第四步，也是全書的終點：神以問題收尾——約拿引神的恩慈作為自己逃的理由；神安排蓖麻、蟲、東風，最後問：「我豈能不愛惜呢？」約拿的回答，經文沒有寫。" \
    "**愛惜**——約拿愛惜一棵蓖麻，神愛惜一座大城" \
    "4:11「我豈能不愛惜呢？」" \
    "神問了我，我的回答是甚麼？"
add_chapter 07
add_chapter 08

# ============================================================
# 卷末 · 全書領受總綱
# ============================================================
add_volume "卷末 · 回望 (Looking Back)" \
    "四步讀完，把全書的領受收攏成一張圖——再一次站在神的問題面前，看見那位發問的神。"

# The study file is a synthesis OF the chapters, so it sits after them
# (as in 2 Peter / Jude), not in the front matter. No YAML: first line is its H1.
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

echo "🔨 Generating PDF with jonah.latex template..."

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

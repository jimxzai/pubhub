#!/bin/bash

# Lamentations PDF Builder - CONSOLIDATED 2026 EDITION
# = preface + orientation (overview / position / alphabet of grief / order of
#   revelation) + 全書領受總綱 + 5 volumes / 10 study units (one volume divider
#   per step of the spine) + 卷末 (to Revelation) + appendices + afterword
# Sources from books/bible/lamentation/ (老弟兄查經方法論 + Henry + Calvin +
# early fathers + Spurgeon, CUV + NASB 1995 scripture; no Morgan/MacArthur
# section -- no verifiable source exists, see the copyright block below).
# Modeled on scripts/build-jude-consolidated.sh (add_file/add_front abort on a
# missing file) and scripts/build-jeremiah-consolidated.sh (systematic study
# placed after the orientation chapters).
# Uses templates/pdf/lamentation.latex (charcoal / candle amber).
# Usage: scripts/build-lamentation-consolidated.sh [--verbose]
#   --verbose  also stream the full xelatex log to the terminal after the
#              build (it is always written to output/lamentation-build.log).

VERBOSE=0
[ "${1:-}" = "--verbose" ] && VERBOSE=1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/lamentation"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/lamentation-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/lamentation-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/lamentation.latex"

echo "=========================================="
echo "📖 Lamentations PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "耶利米哀歌研讀"
subtitle: "Lamentations Deep Study — 2026 整編版"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **資源整合：**

  • **Matthew Henry** — Commentary on the Whole Bible

  • **John Calvin** — Commentaries on the Book of the Prophet Jeremiah and the Lamentations（John Owen 英譯，CCEL）

  • **早期教父** — 引文取自 ANF／NPNF 公有領域譯本（newadvent.org）

  • **C. H. Spurgeon** — 講道（公有領域）

  • **老弟兄查經方法論之應用**（倉庫中沒有老弟兄以哀歌為題的查經記錄）

  本卷未立摩根、麥克阿瑟專節——查無可核對的原文，不用泛論補位。

  **神不開口的書——人怎樣對沉默的神說話**

  卷一 錫安獨坐 (1-2章) | 卷二 主如仇敵 (3-4) | 卷三 我是困苦人 (5-7)

  卷四 精金變色 (8-9) | 卷五 求你記念 (10)

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

# A numbered chapter (the ten study units).
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
    "讀正文之前先讀這幾章：地圖、座標、字母詩的形式、骨幹——啟示的次序，以及全書領受總綱。"
add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-lamentations-position.md"
add_front "$INPUT_DIR/00b-the-alphabet-of-grief.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# 全書領受總綱 — a synthesis, placed after the orientation chapters (as in
# Jeremiah). The file's own H1 is replaced by an unnumbered one; every line
# after that first H1 is kept, whatever the length of its front matter, and
# headings are demoted one level so it reads as a single chapter.
[ -f "$STUDY_FILE" ] || { echo "❌ Missing file: $STUDY_FILE — aborting build"; exit 1; }
echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
printf '# 全書領受總綱——老弟兄查經法 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
awk 'f{print} /^# /&&!f{f=1}' "$STUDY_FILE" | sed 's/^#/##/' \
    | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}{}/g' >> "$COMBINED_MD"
printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
((chapter_count++))

# ============================================================
# 正文 · 五卷十章
# ============================================================
add_volume "卷一 錫安獨坐 (Zion Sits Alone) · 哀1 · 第1-2章" \
    "啟示的次序·第 1 步：無人安慰，人先開口——『安慰者』的位置空著五次（1:2, 9, 16, 17, 21）；詩的第一個動作不是神的答覆，是人從談論轉向呼求：『耶和華啊，求你觀看』（1:11, 1:20）。"
add_chapter 01
add_chapter 02

add_volume "卷二 主如仇敵 (The Lord Is Like an Enemy) · 哀2 · 第3-4章" \
    "啟示的次序·第 2 步：神親手拆毀，因為祂說過的話——主是動詞的主語（2:1-8），『耶和華成就了他所定的』（2:17）；苦難有地址，所以哭泣也有地址：『在主面前傾心如水』（2:19）。"
add_chapter 03
add_chapter 04

add_volume "卷三 我是困苦人 (The Man Who Has Seen Affliction) · 哀3 · 第5-7章" \
    "啟示的次序·第 3 步：在最深處，指望是想起來的（3:21）；第 4 步：神曾說『不要懼怕』（3:57）——全書唯一以直接引語記下的神的話，是受苦者回憶出來的；然後是查驗己行、歸向耶和華（3:40）。"
add_chapter 05
add_chapter 06
add_chapter 07

add_volume "卷四 精金變色 (How the Gold Has Grown Dim) · 哀4 · 第8-9章" \
    "啟示的次序·第 5 步：沒有回答的禱告——金子變色、受膏者被擄、仇敵歡樂；詩以旁述者一句話收束：『錫安的民哪，你罪孽的刑罰受足了』（4:22）。"
add_chapter 08
add_chapter 09

add_volume "卷五 求你記念 (Remember, O LORD) · 哀5 · 第10章" \
    "啟示的次序·第 5 步（續）：全體『我們』的禱告——『你存到永遠』（5:19）、『求你使我們向你回轉』（5:21）；最後一節是問句（5:22），書沒有給答案。"
add_chapter 10

# ============================================================
# 卷末 · 通往啟示錄
# ============================================================
add_front "$INPUT_DIR/99-to-revelation.md"

# ============================================================
# 附錄 — every chapter's 體例說明 points the reader at 《附錄：引用出處總表》;
# both appendices must be concatenated or those pointers dangle.
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引、引用出處總表——供查閱、跨章對照，並如實交代每一處引句的查證方式。"
add_front "$INPUT_DIR/98-appendix-indices.md"
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

echo "🔨 Generating PDF with lamentation.latex template..."

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

[ "$VERBOSE" -eq 1 ] && cat "$LATEX_LOG"
latex_build_report "$PANDOC_EXIT" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1

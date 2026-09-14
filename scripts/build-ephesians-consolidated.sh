#!/bin/bash

# Ephesians PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine/revelation-order) + 全書領受總綱
#   + 三卷 11 章 + 卷末 + 跋 + 附錄
# Uses templates/pdf/ephesians.latex (Indigo/Heaven-blue/Mystery-gold theme,
# matching the Gospel of John / Acts of the Apostles / Job series standard:
# cover art, frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/ephisian"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/ephesians-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/ephesians-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/ephesians.latex"

echo "=========================================="
echo "📖 Ephesians Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "以弗所書研讀"
subtitle: "Ephesians Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  **以弗所書研讀** (A Study of the Book of Ephesians)

  三書精讀出版系統 · 天上的福氣到天上的爭戰系列

  初版　2026 年 9 月

  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  本版為教會內部贈閱版（非賣品），未公開發行；公開發行時另行申請 ISBN。
  歡迎為個人研讀與教會查經複印使用，請保留完整版權頁。

  **經文版權聲明 (Scripture Copyright Notices)**

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (NASB) are from the NEW AMERICAN STANDARD
  BIBLE®, Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977,
  1995 by The Lockman Foundation. Used by permission. www.Lockman.org.
  All rights reserved.

  **注疏引用 (Commentary Sources)**

  本書引用之歷代注疏均屬公有領域。逐條出處、版本與核校方式，
  見卷末《附錄：參考資料》。
---

HEADER

chapter_count=0

# Append one source file: strip its 7-line YAML front matter, convert ^n^ verse
# markers to \textsuperscript, then start a new page.
add_file() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding: $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Front/back matter and volume dividers: same as add_file but marks the H1
# {.unnumbered}, so the 11 study units number 1-11 instead of the front
# matter consuming the first several chapter numbers (same fix as
# build-job-consolidated.sh / build-isaiah-consolidated.sh).
add_front() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding (unnumbered): $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

add_volume() {
    # %b (not %s) for the description: several volume descriptions carry a
    # literal \n>\n> to open a second blockquote paragraph (the 啟示的次序
    # marker). printf only expands escapes inside the FORMAT string, so with
    # %s those arrive in the markdown as the two characters \ and n and
    # xelatex then dies on "Undefined control sequence \n".
    printf '# %s {.unnumbered}\n\n> %b\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| %s | %s |\n|---|---|\n' "$3" "$4" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append the file matching an exact chapter filename (no combined-file globbing —
# every chapter is its own file).
add_chapter() {
    add_file "$INPUT_DIR/$1"
}

# 前言 — preface
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: overview, position, spine, revelation order
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這五章：全書地圖、以弗所書在正典的位置、坐行站的骨幹，以及最要緊的一章——神在這卷書裏按甚麼次序顯明自己。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-ephesians-position.md"
add_front "$INPUT_DIR/00b-sit-walk-stand.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +8 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 三卷 · 11 段
# ============================================================
add_volume "卷一 · 你的地位——坐 (Your Position: Sit) · 弗1-3章" \
    "神顯明自己的第一、二、三步：在教會還沒有存在以前的三一工作、死而復活的個人與群體、藉教會顯給天使看的奧秘。\n>\n> **啟示的次序·第一至三步**：你的身分先於你的行為——這是後面一切勸勉的根基。"
for f in 01-chosen-in-christ.md 02-prayer-for-enlightenment.md 03-from-death-to-life.md \
         04-one-new-humanity.md 05-stewardship-of-mystery.md 06-prayer-for-power.md; do
    add_chapter "$f"
done

add_volume "卷二 · 你的行為——行 (Your Conduct: Walk) · 弗4-5章" \
    "神顯明自己的第四步：藉教會最平凡的日常生活——合一、聖潔、光明、智慧、家庭——把前三章的身分活出來。\n>\n> **啟示的次序·第四步**：神向天使顯明祂的智慧，也向鄰舍、配偶、兒女顯明同一個智慧。"
for f in 07-unity-and-gifts.md 08-new-self.md 09-walk-in-love-light-wisdom.md \
         10-household-in-christ.md; do
    add_chapter "$f"
done

add_volume "卷三 · 你的站立——站 (Your Stance: Stand) · 弗6章" \
    "神顯明自己的第五步：回到全書開頭同一個「天上」的座標，卻換了身分——不再只是領受祝福之處，是要站立得住的戰場。\n>\n> **啟示的次序·第五步**：先領受，才站立；次序不能顛倒。"
add_chapter "11-armor-of-god.md"

# ============================================================
# 卷末 · 從蒙揀選到站立得住
# ============================================================
add_volume "卷末 · 從蒙揀選到站立得住 (From Chosen to Standing Firm)" \
    "全書從創立世界以前的揀選起頭，走過死而復活、合一而立、脫舊穿新，最終停在全副軍裝的站立——這條路沒有一步繞過基督走。"
add_front "$INPUT_DIR/99-heavenlies-and-earth.md"

# 跋 — afterword.
if [ -f "$INPUT_DIR/999-afterword.md" ]; then
    echo "  Adding (unnumbered): 999-afterword.md"
    tail -n +8 "$INPUT_DIR/999-afterword.md" \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 附錄 — bibliography and indices
# ============================================================
add_volume "附錄 (Appendices)" \
    "參考資料、逐章引句一覽、經文索引與主題索引——各章正文所指的「卷末附錄」即此。"
add_front "$INPUT_DIR/99-appendix-references.md"
add_front "$INPUT_DIR/98-appendix-indices.md"

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with ephesians.latex template..."

# --verbose is load-bearing, not chatter: without it pandoc swallows the whole
# xelatex log and every grep-the-log check below (and in driver.sh) passes
# vacuously. See scripts/lib/latex-check.sh for the full explanation.
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
  --top-level-division=chapter \
  -V tocdepth=0 > "$LATEX_LOG" 2>&1
PANDOC_EXIT=$?

latex_build_report "$PANDOC_EXIT" "$LATEX_LOG" "$OUTPUT_PDF" || exit 1

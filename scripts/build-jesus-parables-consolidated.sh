#!/bin/bash

# The Parables of Jesus — CONSOLIDATED 2026 EDITION
# Rebuilt to the Gospel of John standard (the series reference):
#   preface → 卷首·定位 → 全書領受總綱 → 五卷 27 單元 → 卷末 → 跋 → 附錄
# Uses templates/pdf/jesus-parables.latex.
#
# Replaces the older scripts/build-jesus-parables.sh, which concatenated 30
# loose files through scripts/build-pdf.js with no volume structure, no
# front/back matter, and no build verification.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/JesusParables"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/jesus-parables-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/jesus-parables-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/jesus-parables.latex"

echo "=========================================="
echo "📜 The Parables of Jesus PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "耶穌的比喻"
subtitle: "The Parables of Jesus — 隱藏，是為了要顯明"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — *The Parables and Metaphors of Our Lord*

  **全書鑰匙 = 太13:35「我要開口用比喻，把創世以來所隱藏的事發明出來。」**

  天國的奧祕 (1-5) | 尋回與饒恕 (6-9) | 等候與交帳 (10-13)
  錢財、禱告與尋回 (14-20) | 邀請、代價與根基 (21-27)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (ESV) are from the ESV® Bible
  (The Holy Bible, English Standard Version®), © 2001 by Crossway,
  a publishing ministry of Good News Publishers. Used by permission.
  All rights reserved.

  All rights reserved.
---

HEADER

chapter_count=0

# Append one source file. YAML headers vary in length across this book's
# sources, so detect and strip rather than assuming a fixed line count.
add_file() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding: $(basename "$f")"
    local start=1
    if [ "$(head -n 1 "$f")" = "---" ]; then
        start=$(( $(awk 'NR>1 && /^---$/{print NR; exit}' "$f") + 1 ))
    fi
    tail -n +$start "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page carrying the volume's theme.
add_volume() {
    printf '# %s\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Chapters are addressed by their two-digit file prefix.
add_chapter() { for f in "$INPUT_DIR/$1-"*.md; do add_file "$f"; break; done; }

# 前言
add_file "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀比喻之前先站遠一點：耶穌為甚麼用比喻說話，比喻在四福音中怎樣分布，全書的骨幹是哪一條線。"

add_chapter 00
add_file "$INPUT_DIR/00a-parables-position.md"
add_file "$INPUT_DIR/00b-hidden-revealed-spine.md"

# 全書領受總綱
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception)\n\n' >> "$COMBINED_MD"
    tail -n +8 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 五卷 · 27 個比喻
# ============================================================
add_volume "卷一 · 天國的奧祕 (The Mysteries of the Kingdom) · 比喻一至五" \
    "馬太福音十三章的一組比喻。撒種的比喻是「比喻的總鑰匙」——這一個不通，別的也別想通。"
for i in 01 02 03 04 05; do add_chapter "$i"; done

add_volume "卷二 · 尋回與饒恕 (Found and Forgiven) · 比喻六至九" \
    "浪子、鄰舍、惡僕、工人——四個故事問同一件事：你憑甚麼站在這裡？"
for i in 06 07 08 09; do add_chapter "$i"; done

add_volume "卷三 · 等候與交帳 (Waiting and Reckoning) · 比喻十至十三" \
    "十童女、按才幹受託、綿羊與山羊、法利賽人與稅吏——主回來的時候，衡量的是甚麼？"
for i in 10 11 12 13; do add_chapter "$i"; done

add_volume "卷四 · 錢財、禱告與尋回 (Money, Prayer and the Lost) · 比喻十四至二十" \
    "從無知的財主到財主與拉撒路。這一卷最貼身：耶穌談錢，談得比談天堂還多。"
for i in 14 15 16 17 18 19 20; do add_chapter "$i"; done

add_volume "卷五 · 邀請、代價與根基 (Invitation, Cost and Foundation) · 比喻二十一至二十七" \
    "筵席已經預備好了，門也開著。剩下的問題是：你來不來，你算過代價沒有，你把房子蓋在哪裡。"
for i in 21 22 23 24 25 26 27; do add_chapter "$i"; done

# ============================================================
# 卷末
# ============================================================
add_volume "卷末 · 隱與顯，是同一位主 (Hidden and Revealed)" \
    "二十七個故事講完了。最後一個問題還是那一個：你看見耶穌是誰？"
add_file "$INPUT_DIR/99-hidden-and-revealed.md"

# 跋
add_file "$INPUT_DIR/999-afterword.md"

# ============================================================
# 附錄
# ============================================================
add_volume "附錄 (Appendices)" \
    "原文字義與約翰福音貫通；對觀三福音平行對照與第一世紀文化背景。"
add_chapter 28
add_chapter 29

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count units)"
echo ""
echo "🔨 Generating PDF with jesus-parables.latex template..."

# --verbose is load-bearing, not chatter: without it pandoc swallows the whole
# xelatex log and every grep-the-log check (here and in driver.sh) passes
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

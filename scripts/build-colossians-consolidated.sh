#!/bin/bash

# Colossians PDF Builder — CONSOLIDATED 2026 EDITION
# Rebuilt to the Gospel of John standard (the series reference):
#   preface → 卷首·定位 → 全書領受總綱 → 六卷 13 單元 → 卷末 → 跋 → 附錄
# Uses templates/pdf/colossians.latex.
#
# Replaces the older scripts/build-colossians.sh, which concatenated 7 loose
# units with no volume structure and no front/back matter.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/col"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/colossians-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/colossians-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/colossians.latex"

echo "=========================================="
echo "📜 Colossians Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "歌羅西書研讀"
subtitle: "Colossians Deep Study — 基督的豐盛與元首"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 屬靈組織分析法

  **基督是元首 = 萬有的元首 + 教會的元首**

  感謝與代求 (1:1-14) | 基督的超越 (1:15-23) | 奧祕的執事 (1:24-2:5)
  豐盛與假教訓 (2:6-23) | 新生命的實際 (3:1-4:1) | 禱告與問安 (4:2-18)

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

# Volume divider: a part-title page carrying the volume's theme.
add_volume() {
    printf '# %s\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

add_chapter() { add_file "$INPUT_DIR/$1"; }

# 前言
add_file "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀歌羅西書之前先站遠一點：這封信為何而寫，它在保羅書信中站在哪裡，全書的骨幹是哪一條線。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-colossians-position.md"
add_file "$INPUT_DIR/00b-fullness-spine.md"

# 全書領受總綱
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception)\n\n' >> "$COMBINED_MD"
    tail -n +8 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 六卷 · 13 單元
# ============================================================
add_volume "卷一 · 感謝與代求 (Thanksgiving and Intercession) · 1:1-14" \
    "保羅還沒開始辯論，先感謝、先禱告——他要的不是贏過假教師，是這群人「滿心知道神的旨意」。"
for f in 01-greeting-thanksgiving.md 02-prayer-for-knowledge.md; do add_chapter "$f"; done

add_volume "卷二 · 基督的超越 (The Supremacy of Christ) · 1:15-23" \
    "全書的心臟。一首詩把基督放在創造與救贖的雙重首位——祂是萬有的元首，也是教會的元首。"
for f in 03-christ-hymn.md 04-reconciled-and-presented.md; do add_chapter "$f"; done

add_volume "卷三 · 奧祕的執事 (Minister of the Mystery) · 1:24-2:5" \
    "歷世歷代所隱藏的奧祕，如今顯明了——「基督在你們心裡成了有榮耀的盼望」。"
for f in 05-ministry-of-the-mystery.md 06-struggle-for-you.md; do add_chapter "$f"; done

add_volume "卷四 · 豐盛與假教訓的對決 (Fullness versus Philosophy) · 2:6-23" \
    "假教訓要人再加點甚麼；保羅的回答是：你們在他裡面「已經」得了豐盛，還要加甚麼？"
for f in 07-rooted-and-built-up.md 08-shadow-and-substance.md; do add_chapter "$f"; done

add_volume "卷五 · 新生命的實際 (The New Life in Practice) · 3:1-4:1" \
    "教義不停在教義。與基督一同復活的人，脫去舊人、穿上新人，一路穿到家裡與工作裡。"
for f in 09-seek-things-above.md 10-put-on-love.md 11-household-code.md; do add_chapter "$f"; done

add_volume "卷六 · 禱告、使命與問安 (Prayer, Witness and Greetings) · 4:2-18" \
    "一封講宇宙性基督的信，收尾在一串人名上——教義最後總要落在有名有姓的人身上。"
for f in 12-prayer-and-witness.md 13-greetings-and-chains.md; do add_chapter "$f"; done

# ============================================================
# 卷末
# ============================================================
add_volume "卷末 · 豐盛的實現 (The Fullness Realised)" \
    "「你們在他裡面也得了豐盛」——這句話今天還沒有走到盡頭，因為那位元首還要顯現。"
add_file "$INPUT_DIR/99-fullness-realized.md"

# 跋
if [ -f "$INPUT_DIR/999-afterword.md" ]; then
    echo "  Adding: 999-afterword.md"
    tail -n +8 "$INPUT_DIR/999-afterword.md" >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 附錄
# ============================================================
add_volume "附錄 (Appendices)" \
    "查閱用的索引、主題彙整、原文詞彙表與讀經計劃。"
for f in "$INPUT_DIR"/99[a-z]-*.md; do add_file "$f"; done

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count units)"
echo ""
echo "🔨 Generating PDF with colossians.latex template..."

# --verbose is load-bearing, not chatter: without it pandoc swallows the whole
# xelatex log and every grep-the-log check (and in driver.sh) passes vacuously.
# See scripts/lib/latex-check.sh for the full explanation.
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

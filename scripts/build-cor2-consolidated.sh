#!/bin/bash

# 2 Corinthians PDF Builder — CONSOLIDATED 2026 EDITION
# Rebuilt to the Gospel of John standard (the series reference):
#   preface → 卷首·定位 → 全書領受總綱 → 五卷 24 單元 → 卷末 → 跋
# Uses templates/pdf/cor2.latex (which carries appendices A-E).
#
# Replaces the older scripts/build-cor2.sh, which concatenated the syllabus
# overview plus 24 loose lessons with no volume structure, no front/back
# matter, and no build verification.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/cor2"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/cor2-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/cor2-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/cor2.latex"

echo "=========================================="
echo "📜 2 Corinthians Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "哥林多後書研讀"
subtitle: "2 Corinthians Deep Study — 恩典夠用，能力在軟弱上顯得完全"
author: "PubHub 三書精讀系統"
date: "2026年8月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 屬靈組織分析法

  **全書骨幹 = 軟弱 + 安慰 + 十字架的形狀**

  患難與坦誠 (1:1-2:17) | 新約執事的榮耀 (3:1-4:18) | 和好與復和 (5:1-7:16)
  捐輸的恩典 (8:1-9:15) | 使徒權柄的辯護 (10:1-13:14)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations taken from the New American Standard Bible®
  (NASB), Copyright © 1960, 1971, 1977, 1995 by The Lockman
  Foundation. Used by permission. All rights reserved. lockman.org
---

HEADER

chapter_count=0

# Append one source file. Sources are mixed: the newer front/back-matter files
# carry a 7-line YAML header, the 24 lesson files do not. Strip the header only
# when it is actually there, then convert ^n^ verse markers.
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

add_chapter() { for f in "$INPUT_DIR/$1-"*.md; do add_file "$f"; break; done; }

# 前言
add_file "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀哥林多後書之前先站遠一點：這封信為何而寫，它在保羅書信中站在哪裏，全書的骨幹是哪一條線。"

add_file "$INPUT_DIR/00-overview.md"
add_file "$INPUT_DIR/00a-cor2-position.md"
add_file "$INPUT_DIR/00b-weakness-spine.md"

# 全書領受總綱
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception)\n\n' >> "$COMBINED_MD"
    tail -n +8 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 五卷 · 24 單元
# ============================================================
add_volume "卷一 · 患難中的安慰與坦誠 (Comfort and Candour) · 1:1-2:17" \
    "保羅要為自己的使徒身分辯護，第一步不是舉證，是承認自己曾經絕望——「連活命的指望都絕了」。"
for i in 01 02 03 04; do add_chapter "$i"; done

add_volume "卷二 · 新約執事的榮耀 (The Glory of the New Covenant) · 3:1-4:18" \
    "全書領受最密的一段：新約的榮耀遠超舊約，而承載這榮耀的器皿卻是會破的。兩者同時是真的。"
for i in 05 06 07 08 09; do add_chapter "$i"; done

add_volume "卷三 · 和好與復和 (Reconciliation and Restoration) · 5:1-7:16" \
    "眼光拉到永恆——帳棚與房屋、基督台前——再從永恆拉回一件具體的差事：作和好的使者。"
for i in 10 11 12 13 14; do add_chapter "$i"; done

add_volume "卷四 · 捐輸的恩典 (The Grace of Giving) · 8:1-9:15" \
    "兩章講捐款，卻一次也沒有從「需要」講起。他從基督講起——「他本來富足，卻為你們成了貧窮」。"
for i in 15 16 17 18; do add_chapter "$i"; done

add_volume "卷五 · 使徒權柄的辯護 (The Defence of Apostolic Authority) · 10:1-13:14" \
    "語氣急轉。別人的履歷寫成就，保羅寫鞭傷、船難、飢渴——最後寫那根沒有被拿走的刺。"
for i in 19 20 21 22 23 24; do add_chapter "$i"; done

# ============================================================
# 卷末
# ============================================================
add_volume "卷末 · 恩典夠用 (Grace Sufficient)" \
    "保羅求了三次，主一次也沒有拿走。這樣的結局，反而成了全書的高峰。"
add_file "$INPUT_DIR/99-grace-sufficient.md"

# 跋
add_file "$INPUT_DIR/999-afterword.md"

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count units)"
echo ""
echo "🔨 Generating PDF with cor2.latex template..."

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

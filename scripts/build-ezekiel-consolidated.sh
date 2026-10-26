#!/bin/bash

# Ezekiel PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine/order) + 全書領受總綱 + 六卷 34 章 + 卷末 + 附錄 + 跋
# Uses templates/pdf/ezekiel.latex (Sapphire/Amber/Fire theme, derived from ezra.latex)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/ezekiel"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/ezekiel-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/ezekiel-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/ezekiel.latex"

echo "=========================================="
echo "Ezekiel Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "以西結書研讀"
subtitle: "Ezekiel Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年10月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **主要參考資料整合：**

  • **John Calvin** — Commentary on Ezekiel（僅第 1–20 章）

  • **Matthew Henry** — Commentary on the Whole Bible

  • **Keil & Delitzsch** — Biblical Commentary on the Old Testament

  • **J. Skinner** — Ezekiel (The Expositor's Bible, 1895)；**A. B. Davidson** — The Cambridge Bible: Ezekiel；《Pulpit Commentary》；JFB；Gill

  • **教父**：Irenaeus、Origen、Tertullian、Cyril of Jerusalem、Gregory Nazianzen、Chrysostom、Cyprian 等（ANF／NPNF 譯本，見卷末出處總表）

  • **G. Campbell Morgan** — The Analyzed Bible（Job to Malachi），僅用分段大綱

  **榮耀離開，榮耀回來——四十八章經文，三十四篇研讀**

  卷一：榮耀臨到被擄之地 (1-3篇) | 卷二：榮耀離開 (4-8篇) | 卷三：審判的理由 (9-18篇)
  卷四：列國也要知道 (19-23篇) | 卷五：口開了，神自己來 (24-29篇) | 卷六：榮耀回來 (30-34篇)

  **經文版權聲明 (Scripture Copyright Notices)**

  本版為教會內部贈閱版（非賣品）；公開發行時另行申請 ISBN。

  中文經文引自《聖經》和合本（1919），屬公有領域。

  Scripture quotations marked (NASB) are from the NEW AMERICAN STANDARD
  BIBLE®, Copyright © 1960, 1962, 1963, 1968, 1971, 1972, 1973, 1975, 1977,
  1995 by The Lockman Foundation. Used by permission. www.Lockman.org.
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

# Front/back matter and volume dividers: same as add_file but marks the H1
# {.unnumbered}. Without this LaTeX numbers EVERY chapter sequentially, so the
# preface, orientation chapters and the six volume divider pages would consume
# numbers and the book's own first study would not come out as 1.
add_front() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding (unnumbered): $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' \
      | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

# Volume divider: a part-title page carrying the volume's theme.
add_volume() {
    printf '# %s {.unnumbered}\n\n> %s\n' "$1" "$2" >> "$COMBINED_MD"
    if [ -n "$3" ]; then
        printf '\n| %s | %s |\n|---|---|\n' "$3" "$4" >> "$COMBINED_MD"
    fi
    printf '\n\\newpage\n\n' >> "$COMBINED_MD"
    echo "  --- $1"
}

# Append the study unit whose filename starts with NN- (every unit is its own file).
add_unit() {
    local f
    f=$(ls "$INPUT_DIR"/"$1"-*.md 2>/dev/null | head -1)
    if [ -z "$f" ]; then echo "  MISSING unit $1" >&2; return 0; fi
    add_file "$f"
}

# 前言 — preface
add_front "$INPUT_DIR/000-preface.md"

# ============================================================
# 卷首 · 定位 — orientation: overview, position, spine, order
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：總覽、位置、骨幹、啟示的次序。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-ezekiel-position.md"
add_front "$INPUT_DIR/00b-glory-spine.md"
add_front "$INPUT_DIR/00c-revelation-order.md"

# Systematic reception — drop its 7-line YAML and its own H1, demote the rest one level.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +8 "$STUDY_FILE" | awk 'BEGIN{skip=1} skip && /^# /{skip=0; next} {print}' | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 六卷 · 34 段
# ============================================================
add_volume "卷一 · 榮耀臨到被擄之地 (The Glory Comes to the Exiles) · 1-3篇" \
    "榮耀在迦巴魯河邊、在沒有殿的地方向被擄的人顯現；先看見，才吃書卷，才受託守望。**啟示的次序**：第 1 步 · 神先顯現，人才受差——榮耀在被擄之地向人顯現（1:1, 1:28），先看見，才聽見說話的聲音，才被叫站起來（2:1），才受託作守望的人（3:17）；而先知的口被封住（3:26）。"
for n in 01 02 03; do add_unit $n; done

add_volume "卷二 · 榮耀離開 (The Glory Departs) · 4-8篇" \
    "先有不說話的記號，再有向山的話，再揭開殿裏的穢像；榮耀在城破之前，分階段離開殿。**啟示的次序**：第 2 步 · 榮耀在城破之前先離開——基路伯之上 → 殿的門檻（9:3; 10:4）→ 殿的東門口（10:18-19）→ 城東的山（11:23）；城的陷落，消息要到 33:21 才傳到。"
for n in 04 05 06 07 08; do add_unit $n; done

add_volume "卷三 · 審判的理由 (The Reasons for Judgment) · 9-18篇" \
    "假平安、偶像在心、棄嬰的身世、嫩枝、各人的罪、悖逆的歷史、刀、流血的城、兩姊妹、鍋——理由一項一項攤開。**啟示的次序**：第 3 步 · 審判的理由逐項攤開，為要「他們就知道我是耶和華」；到卷末，先知的妻子死去，他不得為她哀哭（24:15-18），口還封著。"
for n in 09 10 11 12 13 14 15 16 17 18; do add_unit $n; done

add_volume "卷四 · 列國也要知道 (The Nations Will Know) · 19-23篇" \
    "鄰邦、推羅、推羅王、埃及、陰間。**啟示的次序**：第 4 步 · 「知道我是耶和華」從以色列擴到萬邦——審判不只臨到神的子民，列國的榮華（船、香柏樹）都要下到坑裏。"
for n in 19 20 21 22 23; do add_unit $n; done

add_volume "卷五 · 口開了，神自己來 (The Mouth Opened; God Himself Comes) · 24-29篇" \
    "逃來的人未到的前一晚，先知的口先開了；然後神自己作牧人、賜新心新靈、使枯骨復活，最後是歌革。**啟示的次序**：第 5 步 · 消息之前，口先開（33:22）；心與靈的更新（36:26-27; 37:14; 39:29），排在殿的度量（40:1 起）之前。"
for n in 24 25 26 27 28 29; do add_unit $n; done

add_volume "卷六 · 榮耀回來 (The Glory Returns) · 30-34篇" \
    "度量、榮耀從東而來、君王與土地、殿中流出的水、耶和華的所在。**啟示的次序**：第 6 步 · 度量之後，榮耀才進來，進來的方向就是離開的方向（11:23 對 43:2-5）；殿中流出水（47:1），城的名字是「耶和華的所在」（48:35）。"
for n in 30 31 32 33 34; do add_unit $n; done

# ============================================================
# 卷末 · 榮耀先離開，也先回來
# ============================================================
add_volume "卷末 · 榮耀回來之後 (After the Glory Returns)" \
    "全書從榮耀在河邊顯現起頭，走過離開、審判、新心與枯骨，終於一個新的城名——歸回不是人的計劃的完成，是神自己「在那裏」。"
add_front "$INPUT_DIR/99-the-glory-returns.md"

# ============================================================
# 附錄 — every chapter's 體例說明 box points the reader at
# 《附錄：引用出處總表》; both appendices must be concatenated or those
# pointers dangle in the printed book.
# ============================================================
add_volume "附錄 (Appendices)" \
    "經文與主題索引、引用出處總表——各章「體例說明」所指的卷末附錄。"
add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with ezekiel.latex template..."

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

#!/bin/bash

# Judges PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 九卷 21 章 + 卷末 + 跋
# Uses templates/pdf/judges.latex (Iron/Torch/Dusk theme, matching the Gospel
# of John / Acts of the Apostles / Isaiah / Job series standard: cover art,
# frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/judges"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/judges-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/judges-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/judges.latex"

echo "=========================================="
echo "🔥  Judges Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "士師記研讀"
subtitle: "Judges Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **核心資源整合：**

  • **週四查經班** — 第一手屬靈教導（老弟兄查經法）

  • **John MacArthur** — gty.org 逐段講道（限於現存講章涵蓋之處）

  • **G. Campbell Morgan** — 《The Analyzed Bible》卷一（1907），士師記結構總覽

  • **Matthew Henry ／ Albert Barnes** 等公有領域注疏 — 補足前二者未涵蓋之章節
    （見卷末《附錄：引用出處總表》逐章說明）

  **一圈一圈往下墮落的循環，每一圈都喊著：以色列需要一位真正的王**

  導論：光景與循環 (1-2章) | 俄陀聶·以笏·珊迦 (3章) | 底波拉與巴拉 (4-5章) |
  基甸 (6-8章) | 亞比米勒與小士師 (9-10章) | 耶弗他 (11-12章) | 參孫 (13-16章) |
  米迦的偶像與但支派 (17-18章) | 利未人之妾與便雅憫的內戰 (19-21章)

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

# Volume divider: a part-title page carrying the volume's theme.
# Front/back matter and volume dividers: same as add_file but marks the H1
# {.unnumbered}. Without this LaTeX numbers EVERY chapter sequentially, so the
# preface, orientation chapters and the nine volume divider pages consume
# numbers ahead of the book's own 第一章 — the contents page would then read
# two conflicting numbers on one line. Marking these unnumbered lets the 21
# study units number 1-21, matching 第一章-第二十一章. Same approach as
# build-job-consolidated.sh / build-isaiah-consolidated.sh.
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
    # xelatex then dies on "Undefined control sequence \n". Same convention
    # as build-job-consolidated.sh.
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
# 卷首 · 定位 — orientation: overview, position, spine
# ============================================================
add_volume "卷首 · 定位 (Orientation)" \
    "讀正文之前先讀這幾章：總覽、位置、骨幹。"

add_front "$INPUT_DIR/00-overview.md"
add_front "$INPUT_DIR/00a-judges-position.md"
add_front "$INPUT_DIR/00b-cycle-spine.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 九卷 · 21 章
# ============================================================
add_volume "卷一 · 導論：光景與循環 (Orientation) · 1-2章" \
    "未趕盡的迦南人，波金使者的責備，循環公式本身的交代——全書的引擎在此先講一遍。\n>\n> **啟示的次序·序幕**：士師記不會直接回答「誰是王」，但整卷書的目的，正是逼你先問出這個問題。"
for f in 01-unfinished-conquest.md 02-angel-at-bochim.md; do
    add_chapter "$f"
done

add_volume "卷二 · 士師循環（一）：俄陀聶·以笏·珊迦 (First Cycle) · 3章" \
    "第一次沉淪、第一次哀求、第一次拯救——循環的公式第一次真正運轉起來。\n>\n> **啟示的次序·第一步**：「拯救者」（מוֹשִׁיעַ）這個字，第一次被安放進士師記的歷史敘事裏——這正是後來「耶和華拯救」（耶穌）這個名字的字根，第一次在這卷書裏預先響起。"
for f in 03-othniel-ehud-shamgar.md; do
    add_chapter "$f"
done

add_volume "卷三 · 士師循環（二）：底波拉與巴拉 (Deborah and Barak) · 4-5章" \
    "神藉一位女先知與一首戰歌，讓一支潰散的軍隊看見：得勝不在乎兵車九百輛，只在乎耶和華。\n>\n> **啟示的次序·第二步**：耶和華的使者第一次在士師記裏開口說話（5:23），親自宣判誰站在祂那邊；士師記開始讓最意外的人得著尊榮，預告路加福音「叫卑賤的升高」（路1:52）。"
for f in 04-deborah-and-barak.md 05-song-of-deborah.md; do
    add_chapter "$f"
done

add_volume "卷四 · 士師循環（三）：基甸 (Gideon) · 6-8章" \
    "神揀選一個躲在酒醡裡打麥子的膽小人，用三百人的得勝教會全以色列：免得他們向神誇口，說是自己的手救了自己。\n>\n> **啟示的次序·第三步**：耶和華的使者親自下到最軟弱之人的藏身之處，把他還未擁有的身分先賜給他；三百人的得勝，把「不容誇口」的十字架邏輯提前演練了一次（7:2；林前1:29）。"
for f in 06-gideons-call.md 07-three-hundred.md 08-gideons-ephod.md; do
    add_chapter "$f"
done

add_volume "卷五 · 士師循環（四）：亞比米勒與小士師 (Abimelech) · 9-10章" \
    "沒有外敵時，士師記的墮落轉向內部——一個篡位者用弟兄的血鋪自己的王座；約坦的寓言早已說盡結局。\n>\n> **啟示的次序·反面**：士師記唯一一次沒有基督的預表，只有基督的反面——一頂靠殺戮搶來、終必焚燒的冠冕，逼著讀者去問：誰才配戴那頂真正的冠冕？"
for f in 09-abimelechs-kingship.md 10-tola-jair-jephthah-rises.md; do
    add_chapter "$f"
done

add_volume "卷六 · 士師循環（五）：耶弗他 (Jephthah) · 11-12章" \
    "一個被趕出家門的私生子，成了以色列的拯救者；他得勝的代價，卻是一句永遠無法收回的誓言。\n>\n> **啟示的次序·第四步**：「獨生的」（יְחִידָה）這個字，第一次把讀者的目光從耶弗他的女兒，引向那位真正的獨生子——「神並不愛惜自己的兒子，為我們眾人捨了」（羅8:32）。"
for f in 11-jephthahs-vow.md 12-ephraim-and-minor-judges.md; do
    add_chapter "$f"
done

add_volume "卷七 · 士師循環（六）：參孫 (Samson) · 13-16章" \
    "力大無窮，卻管不住自己的眼目與情慾——最強的士師，敗在最私密的軟弱上；有恩賜，沒有聖潔。\n>\n> **啟示的次序·第五步（十字架的預演）**：「奇妙」這個名字第一次被說出口，卻沒有人知道是誰（13:18；賽9:6）；參孫的口渴、參孫的禱告、參孫的死，一步比一步更逼近各各他的畫面。"
for f in 13-samsons-birth.md 14-samsons-riddle.md 15-samsons-vengeance.md \
         16-samson-and-delilah.md; do
    add_chapter "$f"
done

add_volume "卷八 · 亂象（一）：米迦的偶像與但支派 (Micah and Dan) · 17-18章" \
    "沒有王的時代，宗教也任意而行——私設的神像、待價而沽的祭司、整支派的偶像崇拜。\n>\n> **啟示的次序·沉默**：沒有士師、沒有外敵，卻用五章篇幅寫盡黑暗；這片刻意的沉默，正是全書逼問「誰是真王」最尖銳的方式。"
for f in 17-micahs-idols.md 18-migration-of-dan.md; do
    add_chapter "$f"
done

add_volume "卷九 · 亂象（二）：利未人之妾與便雅憫的內戰 (Civil War) · 19-21章" \
    "全書最黑暗的一夜，引爆一場幾乎滅族的內戰——道德的崩潰，比任何外敵都更具毀滅性。\n>\n> **啟示的次序·終章**：全書最黑暗的一夜，換來的不是答案，是一個留給下一卷書的問題；「以色列中沒有王」要等到路加福音才等到回答——「他要作雅各家的王，直到永遠」（路1:32-33）。"
for f in 19-levites-concubine.md 20-war-against-benjamin.md \
         21-restoration-of-benjamin.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 沒有王，直到真王
# ============================================================
add_volume "卷末 · 沒有王，直到真王 (No King, Until the True King)" \
    "士師記從「沒有王」開篇的呼聲，走到「各人任意而行」的結局——這聲呼求，要等到那位萬王之王親自回答。"
add_front "$INPUT_DIR/99-no-king-but-you.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0} /^# /{ if(!done){ sub(/[[:space:]]*$/,""); $0=$0" {.unnumbered}" ; done=1 } } {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with judges.latex template..."

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

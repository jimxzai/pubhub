#!/bin/bash

# Numbers PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 五卷 24 章 + 卷末 + 跋
# Uses templates/pdf/numbers.latex (Camp/Wilderness/Promise theme, matching the
# Job / Acts of the Apostles / Isaiah series standard: cover art, frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/numbers"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/numbers-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/numbers-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/numbers.latex"

echo "=========================================="
echo "🏕️  Numbers Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "民數記研讀"
subtitle: "Numbers Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **週四查經班** — 第一手屬靈教導

  • **Matthew Henry** — 《Commentary on the Whole Bible》

  • **G. Campbell Morgan** — 《An Exposition of the Whole Bible: Numbers》

  **從西奈的次序到應許之地：曠野的管教、不信的倒斃、信實神的堅持**

  卷一‧在西奈的次序 (1-10:10章) | 卷二‧曠野的抱怨與審判 (10:11-20章) | 卷三‧從何珥山到摩押平原 (21-25章)
  卷四‧新一代的預備 (26-32章) | 卷五‧應許之地的產業 (33-36章)

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
# preface, orientation chapters and the five volume divider pages consume
# numbers 1-9 and the book's own 第一章 comes out as a much higher LaTeX
# chapter number — the contents page then reads two conflicting numbers on
# one line. Marking these unnumbered lets the 24 study units number 1-24,
# matching 第一章-第二十四章. Same approach as build-job-consolidated.sh.
# An unnumbered H1 becomes \chapter*, and \chapter* does NOT call
# \chaptermark — so every page of the preface, the orientation chapters and
# the appendices kept whatever running head was last set, which is the title
# of the last NUMBERED chapter (the appendix pages were headed "西羅非哈女兒
# 產業案的了結"). Nothing warns about this; it is visible only on the page.
# Emitting \markboth right after the heading sets the head explicitly.
add_front() {
    local f="$1"
    [ -f "$f" ] || return 0
    echo "  Adding (unnumbered): $(basename "$f")"
    tail -n +8 "$f" | sed 's/\^\([0-9][0-9:-]*\)\^/\\textsuperscript{\1}/g' \
      | awk 'BEGIN{done=0}
             /^# /{ if(!done){ sub(/[[:space:]]*$/,"");
                               t=substr($0,3);
                               # LaTeX specials must be escaped inside
                               # \markboth or the head breaks the build:
                               # "Appendix: Scripture & Theme Indices" threw
                               # "Misplaced alignment tab character &".
                               gsub(/&/,"\\\\&",t); gsub(/%/,"\\\\%",t);
                               gsub(/#/,"\\\\#",t); gsub(/_/,"\\\\_",t);
                               print $0" {.unnumbered}";
                               print "";
                               print "\\markboth{"t"}{"t"}";
                               done=1; next } }
             {print}' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
}

add_volume() {
    printf '# %s {.unnumbered}\n\n\\markboth{%s}{%s}\n\n> %s\n' "$1" "$1" "$1" "$2" >> "$COMBINED_MD"
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
add_front "$INPUT_DIR/00a-numbers-position.md"
add_front "$INPUT_DIR/00b-two-generations-spine.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 五卷 · 24 段
# ============================================================
add_volume "卷一 · 在西奈的次序 (Order at Sinai) · 1-10:10章" \
    "會幕已經立起，百姓已經受了律法——現在要做的，是把一群百姓編組成一支能為神爭戰、環繞會幕而行的軍隊。"
for f in 01-numbering-and-encamping.md 02-levites-and-tabernacle-service.md \
         03-purity-camp-and-nazirite-vow.md 04-offerings-and-lampstand.md \
         05-passover-cloud-and-trumpets.md; do
    add_chapter "$f"
done

add_volume "卷二 · 曠野的抱怨與審判 (Rebellion in the Wilderness) · 10:11-20章" \
    "雲彩一起行，抱怨也隨即開始——從貪慾的墳墓到可拉黨的叛變，第一代出埃及的人漸漸在不信中倒斃曠野。"
for f in 06-setting-out-and-complaining.md 07-miriam-aaron-and-the-spies.md \
         08-rebellion-and-the-forty-years.md 09-supplementary-laws-and-tassels.md \
         10-korahs-rebellion.md 11-aarons-staff-and-purification.md \
         12-miriam-moses-and-aarons-death.md; do
    add_chapter "$f"
done

add_volume "卷三 · 從何珥山到摩押平原 (From Mount Hor to the Plains of Moab) · 21-25章" \
    "銅蛇立起、外邦先知四次想咒詛卻只能祝福——神的信實在曠野盡頭比在西奈山下更加清楚。"
for f in 13-bronze-serpent-and-victory.md 14-balak-summons-balaam.md \
         15-balaams-four-oracles.md 16-baal-peor.md; do
    add_chapter "$f"
done

add_volume "卷四 · 新一代的預備 (Preparing the New Generation) · 26-32章" \
    "第一代人的名字已經從名冊上除去，第二次數點揭開了一個新的世代——他們要重新面對信心與次序的功課。"
for f in 17-second-census.md 18-zelophehads-daughters-and-succession.md \
         19-appointed-offerings-and-vows.md 20-war-with-midian.md \
         21-transjordan-tribes.md; do
    add_chapter "$f"
done

add_volume "卷五 · 應許之地的產業 (Inheriting the Promised Land) · 33-36章" \
    "回顧整條曠野路程，劃定迦南的境界，安排逃城與產業的條例——一切安排都指向即將進入的那地。"
for f in 22-wilderness-itinerary.md 23-borders-and-levite-cities.md \
         24-zelophehads-daughters-resolved.md; do
    add_chapter "$f"
done

# ============================================================
# 卷末 · 從曠野到應許
# ============================================================
add_volume "卷末 · 從曠野到應許 (From Wilderness to Promise)" \
    "全書從西奈山下的數點起頭，走過整整一代人的倒斃，最終停在摩押平原、約旦河的東岸——這條路沒有一步是繞過曠野走的。"
add_front "$INPUT_DIR/99-preparing-to-enter.md"

# 附錄 — indices (scripture/theme) and the citation ledger. Both carry
# machine-generated tables (gen-numbers-scripture-index.py,
# gen-numbers-citation-ledger.py); regenerate them before building if the
# chapters have changed.
add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0}
         /^# /{ if(!done){ sub(/[[:space:]]*$/,"");
                           t=substr($0,3);
                               # LaTeX specials must be escaped inside
                               # \markboth or the head breaks the build:
                               # "Appendix: Scripture & Theme Indices" threw
                               # "Misplaced alignment tab character &".
                               gsub(/&/,"\\\\&",t); gsub(/%/,"\\\\%",t);
                               gsub(/#/,"\\\\#",t); gsub(/_/,"\\\\_",t);
                           print $0" {.unnumbered}";
                           print "";
                           print "\\markboth{"t"}{"t"}";
                           done=1; next } }
         {print}' >> "$COMBINED_MD"
((chapter_count++))

echo ""
echo "✅ Combined markdown: $COMBINED_MD ($(wc -l < "$COMBINED_MD") lines, $chapter_count chapters)"
echo ""
echo "🔨 Generating PDF with numbers.latex template..."

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

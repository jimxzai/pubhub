#!/bin/bash

# 2 Chronicles PDF Builder - CONSOLIDATED 2026 EDITION
# = Preface + 卷首定位(overview/position/spine) + 全書領受總綱 + 八卷 36 章 + 卷末 + 跋
# Uses templates/pdf/chronicl2.latex (Purple/Gold/Ember theme, matching the
# Job / Numbers / Exodus series standard: cover art, frontispiece)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/chronicl2"
STUDY_FILE="$INPUT_DIR/elder-wong-systematic-study.md"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/chronicl2-consolidated.md"
OUTPUT_PDF="$OUTPUT_DIR/chronicl2-consolidated.pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/chronicl2.latex"

echo "=========================================="
echo "👑 2 Chronicles Deep Study PDF (CONSOLIDATED 2026)"
echo "=========================================="
echo ""

mkdir -p "$OUTPUT_DIR"

cat > "$COMBINED_MD" << 'HEADER'
---
title: "歷代志下研讀"
subtitle: "2 Chronicles Deep Study"
author: "PubHub 三書精讀系統"
date: "2026年9月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **注疏骨幹：兩位可逐字核對的解經者**

  • **G. Campbell Morgan** — 《Exposition on the Whole Bible》，歷代志下部分

  • **Matthew Henry** — 《Commentary on the Whole Bible》，歷代志下卷

  另有數章視實際查得的一手材料，收錄 John MacArthur 專題信息與教父時期的論述，均逐條標明出處。

  本卷沒有第一手的查經班教導筆記可依循，全書一處也沒有加引號歸給老弟兄；
  凡「老弟兄式」領受，均為編者依這系列查經方法所作的撮述。詳見〈前言〉
  與卷末〈附錄：參考資料與引文帳目〉。

  **從所羅門建殿的榮光，到二十一位王三百八十四年的起伏，到古列詔令重新打開的門**

  卷一‧所羅門時代 (1-9章) | 卷二‧王國分裂 (10章) | 卷三‧早期猶大王 (11-20章) |
  卷四‧中期猶大王 (21-28章) | 卷五‧希西家復興 (29-32章) | 卷六‧瑪拿西轉折 (33章) |
  卷七‧約西亞復興 (34-35章) | 卷八‧末代四王與尾聲 (36章)

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
# preface, orientation chapters and the eight volume divider pages consume
# numbers 1-9+ and the book's own 第一章 comes out as a much higher LaTeX
# chapter number — the contents page then reads two conflicting numbers on
# one line. Marking these unnumbered lets the 36 study units number 1-36,
# matching 第一章-第三十六章. Same approach as build-exodus-consolidated.sh.
# An unnumbered H1 becomes \chapter*, and \chapter* does NOT call
# \chaptermark — so every page of the preface, the orientation chapters and
# the appendices kept whatever running head was last set, which is the title
# of the last NUMBERED chapter. Nothing warns about this; it is visible only
# on the page. Emitting \markboth right after the heading sets the head
# explicitly.
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
    # %b (not %s) for the description: it carries \n\n to separate the volume's
    # theme line from its 「啟示的次序·第 N 步」 spine line. bash's printf does not
    # expand escapes inside a %s argument, so %s printed a literal \n\n on the page
    # while check-book-spine.py — which greps the source — still reported [ok].
    printf '# %s {.unnumbered}\n\n\\markboth{%s}{%s}\n\n> %b\n' "$1" "$1" "$1" "$2" >> "$COMBINED_MD"
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
add_front "$INPUT_DIR/00a-chronicles2-position.md"
add_front "$INPUT_DIR/00b-seeking-spine.md"

# Systematic reception — demote headings one level so it reads as one chapter.
if [ -f "$STUDY_FILE" ]; then
    echo "  Adding: elder-wong-systematic-study.md (as 全書領受總綱)"
    printf '# 全書領受總綱——查經領受 (Systematic Reception) {.unnumbered}\n\n' >> "$COMBINED_MD"
    tail -n +2 "$STUDY_FILE" | sed 's/^#/##/' >> "$COMBINED_MD"
    printf '\n\n\\newpage\n\n' >> "$COMBINED_MD"
    ((chapter_count++))
fi

# ============================================================
# 正文 · 八卷 · 36 章
# ============================================================
add_volume "卷一 · 所羅門時代 (Solomon's Temple) · 1-9章" \
    "所羅門登基第一件事是求智慧，不是求財富；聖殿建成、約櫃入殿，耶和華的榮光充滿了神的殿——這是全書唯一一段幾乎完美的巔峰。\n\n**啟示的次序·第一步（起點）**：右尋求的樣式，在全書一開始就被示範出來——尋求的對象是神的心意，不是自己的益處（1:11）。"
for f in 01-solomon-asks-for-wisdom.md 02-preparing-temple-materials.md \
         03-building-the-temple.md 04-temple-furnishings.md \
         05-glory-fills-the-temple.md 06-solomons-dedication-prayer.md \
         07-gods-response-if-my-people.md 08-solomons-building-projects.md \
         09-queen-of-sheba-glorys-peak.md; do
    add_chapter "$f"
done

add_volume "卷二 · 王國分裂 (The Kingdom Divided) · 10章" \
    "羅波安在示劍一句決定，統一的王國就此斷裂，且再未癒合——這是全書的骨折點。\n\n**啟示的次序·第二步（骨折）**：人的愚昧選擇，同時是神藉先知早已宣告的審判（10:15）——人的責任與神的主權並存。"
add_chapter "10-rehoboams-folly-kingdom-divided.md"

add_volume "卷三 · 早期猶大王 (Asa and Jehoshaphat) · 11-20章" \
    "羅波安、亞撒、約沙法輪流示範「尋求」與「不倚靠」如何在同一個人身上交替出現——起初倚靠神，中途動搖，晚年往往靠自己的智謀而非神的膀臂。\n\n**啟示的次序·第三步（拉鋸）**：先知把7:14的原則說成一條可驗證的公式——尋求就尋見，離棄就被離棄（15:2）。"
for f in 11-rehoboam-strengthens-kingdom.md 12-shishaks-invasion-rehoboam-humbled.md \
         13-abijahs-victory-over-jeroboam.md 14-asas-reforms-victory-over-cushites.md \
         15-asas-covenant-renewal.md 16-asas-later-failure.md \
         17-jehoshaphat-teaches-the-law.md 18-jehoshaphat-allies-with-ahab.md \
         19-jehoshaphats-judicial-reform.md 20-jehoshaphats-prayer-victory-through-worship.md; do
    add_chapter "$f"
done

add_volume "卷四 · 中期猶大王 (Darkness with a Few Lights) · 21-28章" \
    "這八章是全書最黑暗的一段——約蘭殺兄弟、亞他利雅殺王孫、亞哈斯獻兒女為祭——卻仍有約阿施早年、烏西雅前期、約坦一生這些短暫卻真實的光明。\n\n**啟示的次序·第四步（幾乎斷絕）**：大衛家的血脈幾乎在亞他利雅手中斷絕，神卻在危機最深處親自介入保守應許（22:10-12）。"
for f in 21-jehorams-wickedness.md 22-ahaziah-and-athaliahs-usurpation.md \
         23-joash-enthroned-athaliahs-death.md 24-joash-repairs-temple-then-falls.md \
         25-amaziahs-pride.md 26-uzziahs-strength-and-pride.md \
         27-jotham-walks-steadily.md 28-ahaz-great-evil.md; do
    add_chapter "$f"
done

add_volume "卷五 · 希西家復興 (Hezekiah's Revival) · 29-32章" \
    "先潔淨聖殿，再守逾越節，然後全面宗教改革——敬拜的次序被恢復，國家的復興才隨之而來。\n\n**啟示的次序·第五步（次序）**：改革不是從外交或軍事開始，是從恢復敬拜的通路開始（29:3）。"
for f in 29-hezekiah-cleanses-the-temple.md 30-hezekiahs-passover.md \
         31-hezekiahs-religious-reforms.md 32-hezekiah-repels-assyria-illness-pride.md; do
    add_chapter "$f"
done

add_volume "卷六 · 瑪拿西轉折 (Manasseh's Turn) · 33章" \
    "全書最惡的王，用上與7:14相同的動詞——自卑、懇求——悔改，神就應允了他。這是全書「尋求就尋見」這條線索最強、也最出人意外的證據。\n\n**啟示的次序·第六步（轉折）**：這條路沒有下限，無論一個人曾經惡到甚麼地步（33:12-13）。"
add_chapter "33-manassehs-evil-and-repentance.md"

add_volume "卷七 · 約西亞復興 (Josiah's Revival) · 34-35章" \
    "約西亞年幼就開始尋求神，律法書出土後全面加速改革，守了自撒母耳以來最隆重的逾越節——這是猶大滅亡之前最後一次燃燒到底的機會。\n\n**啟示的次序·第七步（最後的燃燒）**：律法書的發現不是尋求的起點，是既有尋求之心得著更清楚方向的加速器（34:3）。"
for f in 34-josiah-discovers-book-of-law.md 35-josiahs-passover-and-death.md; do
    add_chapter "$f"
done

add_volume "卷八 · 末代四王與尾聲 (The Last Kings and Cyrus's Decree) · 36章" \
    "約西亞死後23年內四位王一位比一位敗壞，聖殿終於被焚——但全書沒有停在灰燼裏，最後兩節是神藉外邦君王古列頒布的詔令：可以上去。\n\n**啟示的次序·第八步（終點）**：審判是神耐性用盡之後的最後一步，卻不是祂最後的心意——門，仍然開著（36:15-23）。"
add_chapter "36-last-four-kings-and-cyrus-decree.md"

# ============================================================
# 卷末 · 可以上去
# ============================================================
add_volume "卷末 · 可以上去 (Let Him Go Up)" \
    "全書從所羅門獻殿的榮光起頭，走過三百八十四年、二十一位王的興衰，最終停在聖殿的灰燼旁——卻在最後兩節，被一位外邦君王的詔令重新點燃盼望。"
add_front "$INPUT_DIR/99-open-door.md"

# 附錄 — indices (scripture/theme) and the citation ledger. Both carry
# machine-generated tables (gen-chronicl2-scripture-index.py,
# check-citation-ledger.py); regenerate them before building if the
# chapters have changed.
add_front "$INPUT_DIR/98-appendix-indices.md"
add_front "$INPUT_DIR/99-appendix-references.md"

# 跋 — afterword. Last content file: no trailing \newpage.
echo "  Adding (unnumbered): 999-afterword.md"
tail -n +8 "$INPUT_DIR/999-afterword.md" \
  | awk 'BEGIN{done=0}
         /^# /{ if(!done){ sub(/[[:space:]]*$/,"");
                           t=substr($0,3);
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
echo "🔨 Generating PDF with chronicl2.latex template..."

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

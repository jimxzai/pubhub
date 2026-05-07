# 約翰福音研讀 (Gospel of John Deep Study)

**Status**: ✅ COMPLETE - All 21 Chapters
**Template**: Original premium template (PRESERVED)
**Last Updated**: 2026-01-03

---

## 📖 Overview

Complete Gospel of John study integrating three core resources:
- **黃長老週四查經班** - Elder Wong's Thursday Bible study (first-hand teaching)
- **John MacArthur** - Verse-by-verse exposition (gty.org)
- **G. Campbell Morgan** - The Gospel According to John (1909)

**Core Framework**: 榮耀 = 恩典 + 真理 (Glory = Grace + Truth)

---

## 📚 Chapter Files (22 files)

```
00-overview.md                   # 約翰福音總覽
01-prologue.md                   # Ch 1:1-18   道成肉身
02-cana-wedding.md               # Ch 2        迦拿婚宴
03-nicodemus.md                  # Ch 3        重生之道
04-samaritan-woman.md            # Ch 4        活水泉源
05-bethesda.md                   # Ch 5        畢士大池
06-bread-of-life.md              # Ch 6        生命的糧
07-feast-tabernacles.md          # Ch 7        住棚節
08-light-of-world.md             # Ch 8        世界的光
09-blind-man.md                  # Ch 9        瞎子得醫
10-good-shepherd.md              # Ch 10       好牧人
11-lazarus.md                    # Ch 11       拉撒路復活
12-triumphal-entry.md            # Ch 12       榮入聖城
13-washing-feet.md               # Ch 13       洗腳與新命令
14-way-truth-life.md             # Ch 14       道路真理生命
15-true-vine.md                  # Ch 15       真葡萄樹
16-holy-spirit.md                # Ch 16       聖靈的工作
17-high-priestly-prayer.md       # Ch 17       大祭司禱告
18-arrest-trial.md               # Ch 18       被捕與審判
19-crucifixion.md                # Ch 19       十字架
20-resurrection.md               # Ch 20       復活
21-epilogue.md                   # Ch 21       尾聲與使命
complete-book.md                 # 完整書稿
```

**Total**: 21 chapters + overview + complete book

---

## 🎨 Template Structure (IMPORTANT - DO NOT CHANGE)

### Original Premium Template

**File**: `templates/pdf/gospel-of-john-original.latex` (568 lines)

**Critical Features** (must be preserved):

1. **Red Letter Bible** (Inspired by ai-eden.com) ⭐ NEW
   ```latex
   \definecolor{JesusRed}{RGB}{204,0,0}  % #CC0000
   \newcommand{\jesus}[1]{\textcolor{JesusRed}{#1}}
   ```
   - Jesus's words displayed in red (#CC0000)
   - Usage: `\jesus{"I am the way, and the truth, and the life"}`
   - See: `RED-LETTER-GUIDE.md` for complete usage

2. **TikZ Graphics Library**
   ```latex
   \usepackage{tikz}
   \usetikzlibrary{shapes,arrows,positioning,fit,backgrounds,calc,decorations.pathmorphing}
   ```

3. **Decorative Elements**
   - `\vinedecor{}` - Vine decoration for chapter headers
   - `\crosssymbol` - Cross symbol for passion narrative
   - Map support (Water, Land, Mountain colors)

3. **Colored Box Environments**
   ```latex
   ScriptureBg   RGB(252,250,245)  # Scripture quotations
   GreekBg       RGB(245,248,252)  # Greek word studies
   ApplicationBg RGB(248,252,248)  # Application sections
   ```

4. **Typography**
   - Main: Songti SC (宋體)
   - Sans: PingFang SC (蘋方)
   - Mono: Menlo (等寬)
   - Italic: Kaiti SC (楷體)

5. **Page Format**
   - Size: 7×10 inches (professional book format)
   - Margins: Conservative for binding
   - Line spacing: 1.1 (readable)

6. **CJK Line Breaking**
   ```latex
   \XeTeXlinebreaklocale "zh"
   \XeTeXlinebreakskip = 0pt plus 1pt minus 0.1pt
   ```
   **Note**: NO `xeCJK` package needed!

---

## 🔨 Build Instructions

### Primary Build Script

**Script**: `scripts/build-gospel-pdf-original.sh`

```bash
#!/bin/bash
# Builds Gospel of John with ORIGINAL premium template
# All 21 chapters + overview
./scripts/build-gospel-pdf-original.sh
```

**Output**: `output/gospel-of-john-original.pdf`
- Size: ~844K
- Pages: ~110 pages
- Chapters: All 21 ✅

### Build Process

1. **Combine markdown files**
   - Start with YAML frontmatter
   - Add 00-overview.md
   - Add chapters 01-21 in order
   - Insert `\newpage` between chapters

2. **Generate PDF with pandoc**
   ```bash
   pandoc "$COMBINED_MD" \
     -o "$OUTPUT_PDF" \
     --pdf-engine=xelatex \
     --template="templates/pdf/gospel-of-john-original.latex" \
     --toc \
     --toc-depth=2 \
     --number-sections
   ```

3. **Open result**
   ```bash
   open output/gospel-of-john-original.pdf
   ```

---

## 📋 Content Structure (Each Chapter)

### Standard Format

```markdown
---
title: 約翰福音研讀
subtitle: Gospel of John Deep Study
author: PubHub 三書精讀系統
date: 2025年12月
publisher: 三書精讀出版系統
---

# Chapter Title (Bilingual)

約翰福音 X:Y-Z

## 經文 (Scripture)

### 中文 — 和合本修訂版 (RCUV)
> [Chinese text]

### English — NIV (New International Version)
> [English text]

## 背景 (Context)
### 歷史背景
### 文學結構

## 原文研讀 (Word Study)
[Greek word analysis with tables]

## 神學要點 (Theological Points)
### 1. First Point
### 2. Second Point

## 三方整合 (Three Resources Integration)

### 黃長老教導
[Elder Wong's teaching]

### MacArthur 解經
[MacArthur's exposition]

### Campbell Morgan 洞見
[Morgan's insights]

## 生命應用 (Application)
### 個人層面
### 教會層面
### AI時代反思

## 結論 (Conclusion)
```

---

## 🔍 Three Core Resources

### 1. Elder Wong's Materials

**Location**: `daily-notes/drafts/thursday-wong/`

**Key files**:
- `Gospel of John.md` - Core framework
- `John-2-3-Study.md` through `John-18-21-Study.md` - Chapter studies
- `reports/FINAL-complete-report.md` - Complete study report

**Framework**: 榮耀 = 恩典 + 真理
- 七個神蹟 (Seven Signs) - Works manifesting Grace
- 七個「我是」(Seven "I AM") - Words manifesting Truth

### 2. John MacArthur

**Source**: https://www.gty.org/library/resources/sermon-series/324

**Series**: "The Gospel of John" (154 sermons)
- Verse-by-verse exposition
- MacArthur Study Bible notes
- Theological depth

### 3. G. Campbell Morgan

**Source**: https://archive.org/details/gospelaccordingto00morg

**Book**: "The Gospel According to John" (1909)
- Structural analysis
- Spiritual organization
- Classic commentary

---

## ⚠️ CRITICAL - TEMPLATE PRESERVATION RULES

### DO NOT

❌ **Remove TikZ support** - Required for diagrams
❌ **Change page size** - 7×10 is intentional for professional book format
❌ **Simplify to "basic" template** - Loses important visual elements
❌ **Add `xeCJK` package** - Not available in environment, use fontspec
❌ **Change font stack** - Carefully chosen for CJK + English
❌ **Remove colored boxes** - Critical for visual hierarchy
❌ **Change line breaking settings** - Optimized for Chinese text

### DO

✅ **Keep all TikZ decorations** - Part of original design
✅ **Preserve color scheme** - Bible study themed colors
✅ **Maintain CJK line breaking** - Essential for Chinese typography
✅ **Use fontspec only** - Works without xeCJK package
✅ **Keep 7×10 format** - Standard book size
✅ **Preserve all custom environments** - Scripture boxes, Greek studies

---

## 📊 Quality Metrics

### Current Status

- [x] All 21 chapters complete
- [x] Three resources integrated
- [x] Original template preserved
- [x] PDF builds successfully
- [x] ~110 pages (>100 pages requirement met)
- [x] TikZ diagrams working
- [x] CJK typography correct
- [x] Table of contents generated
- [x] Bilingual (繁中 + English)

### File Sizes

```
gospel-of-john-original.pdf    844K   (21 chapters, original template)
gospel-of-john-combined-full.md  ~180K  (source markdown)
```

---

## 🔄 Maintenance

### When Adding/Updating Chapters

1. **Follow naming convention**: `NN-chapter-name.md`
2. **Include YAML frontmatter** (lines 1-7)
3. **Start content at line 8**
4. **Use bilingual headings**
5. **Include all standard sections**
6. **Integrate three resources**

### When Rebuilding PDF

```bash
# Always use the original build script
./scripts/build-gospel-pdf-original.sh

# Verify chapter count (should be 21)
# Check PDF size (should be ~844K)
# Confirm page count (should be >100 pages)
```

### When Template Needs Update

1. **Backup current template first**
   ```bash
   cp templates/pdf/gospel-of-john-original.latex \
      templates/pdf/gospel-of-john-original-backup-$(date +%Y%m%d).latex
   ```

2. **Make minimal changes** - Only if absolutely necessary
3. **Test build immediately**
4. **Compare output carefully**
5. **Restore from backup if issues**

---

## 📝 Git History

**Original commit**: `d762581` ("john")
**Restored**: 2026-01-03
**Template preserved**: ✅

**Important commits**:
- `d762581` - Original Gospel of John with premium template
- `29446ee` - MVP focus declaration
- `d1f7472` - Book structure

---

## 📞 Support

**For questions about**:
- **Template structure**: See `templates/pdf/gospel-of-john-original.latex`
- **Build process**: See `scripts/build-gospel-pdf-original.sh`
- **Content**: See three core resources in `thursday-wong/`
- **Greek studies**: Refer to `docs/study-notes/john-1-1-logos-deep-dive.md`

---

## 🎯 Summary

**THE ORIGINAL GOSPEL OF JOHN STRUCTURE MUST BE PRESERVED**

- Template: `gospel-of-john-original.latex` ✅
- Build script: `build-gospel-pdf-original.sh` ✅
- All 21 chapters: ✅
- TikZ diagrams: ✅
- 7×10 format: ✅
- ~110 pages: ✅

**Default command**:
```bash
./scripts/build-gospel-pdf-original.sh
open output/gospel-of-john-original.pdf
```

---

**Last Updated**: 2026-01-03
**Maintained By**: PubHub 三書精讀系統
**Status**: COMPLETE & PRESERVED

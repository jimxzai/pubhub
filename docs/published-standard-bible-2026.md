# Published Standard Bible 2026

**三書精讀出版系統 — 聖經出版標準規範**

Version: 2.1
Date: 2026-01-04
Status: Official Standard

---

## Table of Contents

1. [Copyright & Attribution](#1-copyright--attribution)
2. [Bible Versions & Bilingual Format](#2-bible-versions--bilingual-format)
3. [Red Letter Bible Format](#3-red-letter-bible-format)
4. [Directory Structure](#4-directory-structure)
5. [YAML Frontmatter Standard](#5-yaml-frontmatter-standard)
6. [Key Scripture Translations](#6-key-scripture-translations)
7. [Build Scripts](#7-build-scripts)
8. [Gospel of John Structure](#8-gospel-of-john-structure)
9. [Output Files](#9-output-files)
10. [Quality Checklist](#10-quality-checklist)
11. [Theological Framework](#11-theological-framework)
12. [Future Expansion](#12-future-expansion)
13. [Professional Publishing Features](#13-professional-publishing-features) *(NEW)*
14. [LaTeX Templates](#14-latex-templates) *(NEW)*

---

## 1. Copyright & Attribution

### Standard Copyright Notice

```
版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神
```

### Three Core Resources Integration

All Gospel study publications must integrate these three authoritative sources:

| Resource | Description | Role |
|----------|-------------|------|
| **黃長老週四查經班** | Elder Wong's Thursday Bible Study | 第一手屬靈教導 |
| **John MacArthur** | Grace to You (gty.org) | 逐節解經 |
| **G. Campbell Morgan** | The Gospel According to John (1909) | 解經王子 |

### Bible Version Copyright Notices

| Version | Copyright Notice |
|---------|------------------|
| **NASB** | Scripture quotations are from the New American Standard Bible®, Copyright © 1960, 1971, 1977, 1995, 2020 by The Lockman Foundation. All rights reserved. |
| **NKJV** | Scripture taken from the New King James Version®. Copyright © 1982 by Thomas Nelson. Used by permission. All rights reserved. |
| **NIV** | Scripture quotations marked NIV are taken from the Holy Bible, New International Version®, NIV®. Copyright © 1973, 1978, 1984, 2011 by Biblica, Inc.™ Used by permission of Zondervan. All rights reserved worldwide. |
| **ESV** | Scripture quotations are from The ESV® Bible (The Holy Bible, English Standard Version®), copyright © 2001 by Crossway, a publishing ministry of Good News Publishers. Used by permission. All rights reserved. |

---

## 2. Bible Versions & Bilingual Format

### Primary Languages

| Language | Primary Version | Reference Versions |
|----------|-----------------|-------------------|
| **Chinese** | 和合本修訂版 (RCUV) | 新譯本 (CNV), 呂振中譯本 |
| **English** | Version-specific (NASB/NKJV/NIV/ESV) | As noted |
| **Greek** | NA28, UBS5 | For word studies |

### Available English Versions

| Version Code | Full Name | Characteristics |
|--------------|-----------|-----------------|
| `nasb` | New American Standard Bible | Literal translation, formal equivalence |
| `nkjv` | New King James Version | Modern KJV, traditional language |
| `niv` | New International Version | Dynamic equivalence, readable |
| `esv` | English Standard Version | Essentially literal, default |

### Bilingual Reference Format

```markdown
| 2 | 經文朗讀 | 中英對照 (RCUV + [VERSION]) |
```

Example for NKJV:
```markdown
| 2 | 經文朗讀 | 中英對照 (RCUV + NKJV) |
```

---

## 3. Red Letter Bible Format

### Jesus' Words Markup

Use `\jesus{}` LaTeX command to highlight Jesus' words in red:

```markdown
\jesus{I am the way, the truth, and the life. No one comes to the Father except through Me.}
```

### Verse Superscript Format

Use `^number^` in markdown, converted to `\textsuperscript{number}` for LaTeX:

```markdown
> ^14^And the Word became flesh and dwelt among us
```

Build script automatically converts:
```bash
sed 's/\^\\([0-9]*\\)\^/\\\\textsuperscript{\\1}/g'
```

---

## 4. Directory Structure

### Multi-Version Organization

```
books/bible/
├── gospel-of-john/           # Original ESV version
├── gospel-of-john-nasb/      # NASB version
├── gospel-of-john-nkjv/      # NKJV version
├── gospel-of-john-niv/       # NIV version
└── gospel-of-matthew/        # Future books
```

### Chapter File Naming Convention

| Pattern | Example | Content |
|---------|---------|---------|
| `00-overview.md` | `00-overview.md` | Book overview and structure |
| `01-[topic].md` | `01-prologue.md` | Chapter 1 main section |
| `01b-[topic].md` | `01b-first-disciples.md` | Chapter 1 subsection |
| `02-[topic].md` | `02-cana-wedding.md` | Chapter 2 |
| ... | ... | Continue through chapter 21 |

### Chapter Order for Gospel of John

```
01 01b 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
```

---

## 5. YAML Frontmatter Standard

### Chapter File Frontmatter (7 lines)

```yaml
---
title: Chapter Title
chapter: X
section: Section Name
theme: Main Theme
hymn: Associated Hymn
---
```

### Overview File Frontmatter

```yaml
---
title: 約翰福音研讀
subtitle: Gospel of John Deep Study
author: PubHub 三書精讀系統
date: 2026年1月
publisher: 三書精讀出版系統
---
```

---

## 6. Key Scripture Translations

### John 20:31 (Core Verse) — By Version

| Version | Translation |
|---------|-------------|
| **RCUV** | 但記這些事，是要叫你們信耶穌是基督，是神的兒子，並且叫你們信了祂，就可以因祂的名得生命。 |
| **NASB** | But these have been written so that you may believe that Jesus is the Christ, the Son of God; and that by believing you may have life in His name. |
| **NKJV** | but these are written that you may believe that Jesus is the Christ, the Son of God, and that believing you may have life in His name. |
| **NIV** | But these are written that you may believe that Jesus is the Messiah, the Son of God, and that by believing you may have life in his name. |
| **ESV** | But these are written so that you may believe that Jesus is the Christ, the Son of God, and that by believing you may have life in his name. |

### John 3:16 — By Version

| Version | Translation |
|---------|-------------|
| **NASB** | For God so loved the world, that He gave His only Son, so that everyone who believes in Him will not perish, but have eternal life. |
| **NKJV** | For God so loved the world that He gave His only begotten Son, that whoever believes in Him should not perish but have everlasting life. |
| **NIV** | For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life. |

### John 1:14 — By Version

| Version | Translation |
|---------|-------------|
| **NASB** | And the Word became flesh, and dwelt among us; and we saw His glory, glory as of the only Son from the Father, full of grace and truth. |
| **NKJV** | And the Word became flesh and dwelt among us, and we beheld His glory, the glory as of the only begotten of the Father, full of grace and truth. |
| **NIV** | The Word became flesh and made his dwelling among us. We have seen his glory, the glory of the one and only Son, who came from the Father, full of grace and truth. |

---

## 7. Build Scripts

### Script Naming Convention

```
build-gospel-[version].sh
```

Examples:
- `build-gospel-nasb.sh`
- `build-gospel-nkjv.sh`
- `build-gospel-niv.sh`
- `build-gospel-pdf-original.sh` (ESV default)

### Build Script Template

```bash
#!/bin/bash

# Gospel of John PDF Builder - [VERSION] Version
# Uses [VERSION] ([Full Name]) for English Scripture

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_ROOT/books/bible/gospel-of-john-[version]"
OUTPUT_DIR="$PROJECT_ROOT/output"
COMBINED_MD="$OUTPUT_DIR/gospel-of-john-[version]-combined.md"
OUTPUT_PDF="$OUTPUT_DIR/gospel-of-john-[version].pdf"
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-john-original.latex"
```

### YAML Header in Build Script

```bash
cat > "$COMBINED_MD" << 'HEADER'
---
title: "約翰福音研讀"
subtitle: "Gospel of John Deep Study ([VERSION])"
author: "PubHub 三書精讀系統"
date: "2026年1月"
publisher: "三書精讀出版系統"
copyright: |
  版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神

  **三大核心資源整合：**

  • **黃長老週四查經班** — 第一手屬靈教導

  • **John MacArthur** — 逐節解經 (gty.org)

  • **G. Campbell Morgan** — 解經王子 (1909)

  **English Scripture: [VERSION] ([Full Name])**

  **榮耀 = 恩典 + 真理**

  七個神蹟 (works) 彰顯恩典 | 七個「我是」(words) 彰顯真理

  [Copyright Notice for specific version]
---

HEADER
```

### Pandoc Command

```bash
pandoc "$COMBINED_MD" \
  -o "$OUTPUT_PDF" \
  --pdf-engine=xelatex \
  --template="$TEMPLATE" \
  --from=markdown-superscript-subscript \
  --toc \
  --toc-depth=1 \
  --top-level-division=chapter \
  -V tocdepth=0
```

---

## 8. Gospel of John Structure

### Four Parts

| Part | Chapters | Theme | Chinese |
|------|----------|-------|---------|
| **Prologue** | 1:1-18 | The Nature of the Word | 序言：道的本質 |
| **Public Ministry** | 1:19-12:50 | Signs and Discourses | 公開事工：神蹟與講論 |
| **Private Teaching** | 13:1-17:26 | Upper Room Discourse | 私下教導：馬可樓上講論 |
| **Passion & Resurrection** | 18:1-21:25 | Cross and Empty Tomb | 受難復活：十架與空墳 |

### Seven Signs (七個神蹟)

| # | Sign | Reference | Symbolism |
|---|------|-----------|-----------|
| 1 | Water to Wine | 2:1-11 | Glory of the New Covenant |
| 2 | Healing Official's Son | 4:46-54 | Power of Faith |
| 3 | Healing at Bethesda | 5:1-15 | Lord of the Sabbath |
| 4 | Feeding 5000 | 6:1-14 | Bread of Life |
| 5 | Walking on Water | 6:16-21 | Overcoming Storms |
| 6 | Healing Blind Man | 9:1-41 | Light of the World |
| 7 | Raising Lazarus | 11:1-44 | Resurrection and Life |

### Seven "I AM" Statements (七個「我是」)

| # | Statement | Reference | OT Echo |
|---|-----------|-----------|---------|
| 1 | I am the Bread of Life | 6:35 | Manna (Ex 16) |
| 2 | I am the Light of the World | 8:12 | Pillar of Fire (Ex 13) |
| 3 | I am the Door | 10:7 | Tabernacle Entrance |
| 4 | I am the Good Shepherd | 10:11 | David as Shepherd (Ps 23) |
| 5 | I am the Resurrection and Life | 11:25 | Tree of Life (Gen 2) |
| 6 | I am the Way, Truth, Life | 14:6 | Moses Leading |
| 7 | I am the True Vine | 15:1 | Israel Vineyard (Is 5) |

---

## 9. Output Files

### PDF Output Naming

```
gospel-of-john-[version].pdf
```

Examples:
- `gospel-of-john-nasb.pdf`
- `gospel-of-john-nkjv.pdf`
- `gospel-of-john-niv.pdf`
- `gospel-of-john-original.pdf` (ESV)

### Combined Markdown Naming

```
gospel-of-john-[version]-combined.md
```

### Output Directory

```
output/
├── gospel-of-john-nasb.pdf
├── gospel-of-john-nasb-combined.md
├── gospel-of-john-nkjv.pdf
├── gospel-of-john-nkjv-combined.md
├── gospel-of-john-niv.pdf
├── gospel-of-john-niv-combined.md
├── gospel-of-john-original.pdf
└── gospel-of-john-combined-full.md
```

---

## 10. Quality Checklist

Before publishing any Bible study PDF:

- [ ] Copyright notice: `版權所有 © 2026 Soli Deo Gloria — 唯獨榮耀神`
- [ ] Three core resources properly attributed
- [ ] Bible version copyright notice included
- [ ] All scripture references match the specified version
- [ ] Overview `00-overview.md` updated with correct version references
- [ ] Key verse (John 20:31) matches the version
- [ ] Daily rhythm table shows correct bilingual format (RCUV + VERSION)
- [ ] Red letter markup `\jesus{}` applied to Jesus' words
- [ ] Verse numbers using superscript format `^n^`
- [ ] All 22 chapters included (00 overview + 01 through 21)
- [ ] PDF generated successfully with correct file name

---

## 11. Theological Framework

### Core Principle

```
榮耀 = 恩典 + 真理
Glory = Grace + Truth
```

### Manifestation

| Aspect | Expression | Count |
|--------|------------|-------|
| **恩典 (Grace)** | 七個神蹟 (works) | 7 Signs |
| **真理 (Truth)** | 七個「我是」(words) | 7 "I AM" Statements |

---

## 12. Future Expansion

### Planned Books

| Priority | Book | Status |
|----------|------|--------|
| 1 | Gospel of John | Complete |
| 2 | Gospel of Matthew | In Progress |
| 3 | Gospel of Luke | Planned |
| 4 | Acts | Planned |
| 5 | Johannine Epistles | Planned |

### Version Expansion

Apply same multi-version standard (NASB, NKJV, NIV, ESV) to all future books.

---

## 13. Professional Publishing Features

### 13.1 Emoji Support

The professional template supports Apple Color Emoji for visual elements:

```latex
% In LaTeX template
\newfontfamily\emojifont{Apple Color Emoji}[Renderer=Harfbuzz]
\newcommand{\emoji}[1]{{\emojifont #1}}
```

**Usage in Markdown:**
```markdown
## 📖 經文研讀 Scripture Study
### 🔑 關鍵詞彙 Key Terms
```

**Common Emoji Usage:**

| Emoji | Usage | Context |
|-------|-------|---------|
| 📖 | Scripture section | 經文 |
| 🔑 | Key terms/keywords | 關鍵詞 |
| 💡 | Insights | 洞見 |
| ✝️ | Cross/Salvation | 十架/救恩 |
| 🕊️ | Holy Spirit | 聖靈 |
| 📝 | Notes | 筆記 |
| ⚠️ | Warning/Important | 注意 |
| 🎵 | Hymns | 聖詩 |

### 13.2 Numbered Figures

Figures are automatically numbered by chapter (e.g., Figure 3.1, Figure 3.2):

```markdown
![約翰福音地圖 Map of John's Gospel](images/john-map.png)

圖 Figure 3.1: 約翰福音重要地點 Key Locations in Gospel of John
```

**LaTeX Configuration:**
```latex
\renewcommand{\thefigure}{\thechapter.\arabic{figure}}
\captionsetup[figure]{name={圖 Figure}}
```

### 13.3 Numbered Tables

Tables are numbered similarly (e.g., Table 2.1):

```markdown
| 神蹟 | 經文 | 象徵意義 |
|------|------|----------|
| 水變酒 | 2:1-11 | 新約的榮耀 |

表 Table 2.1: 七個神蹟 Seven Signs
```

**LaTeX Configuration:**
```latex
\renewcommand{\thetable}{\thechapter.\arabic{table}}
\captionsetup[table]{name={表 Table}}
```

### 13.4 Numbered Notes

Study notes are numbered per chapter:

```latex
\begin{notebox}
This is an important observation about the text.
\end{notebox}
```

Output: **註 Note 3.1:** This is an important observation...

### 13.5 Glossary (詞彙表)

**Markdown Format:**
```markdown
## 詞彙表 Glossary

**λόγος (logos)** — *Word*
The Greek term for "Word" used in John 1:1. In Greek philosophy...

**σάρξ (sarx)** — *Flesh*
The Greek term for flesh, emphasizing human nature...
```

**LaTeX Environment:**
```latex
\begin{bibleglossary}
\glitem{λόγος}{logos}{The Greek term for "Word"...}
\glitem{σάρξ}{sarx}{The Greek term for flesh...}
\end{bibleglossary}
```

### 13.6 Scripture Index (經文索引)

Index entries for key verses:

```markdown
約翰福音 1:1 — 道的本性 \index{John 1:1}
約翰福音 3:16 — 神愛世人 \index{John 3:16}
約翰福音 14:6 — 道路真理生命 \index{John 14:6}
```

### 13.7 Bibliography/References (參考書目)

**Standard Reference Format:**

```markdown
## 參考書目 References

### 主要資源 Primary Sources

1. **黃長老** (2024-2026). 週四查經班約翰福音系列. 教會錄影.

2. **MacArthur, John** (1985-2007). *The MacArthur New Testament Commentary: John*. Moody Publishers.

3. **Morgan, G. Campbell** (1909). *The Gospel According to John*. Fleming H. Revell Company.

### 輔助資源 Secondary Sources

4. **Carson, D.A.** (1991). *The Gospel According to John*. Pillar New Testament Commentary. Eerdmans.

5. **Köstenberger, Andreas J.** (2004). *John*. Baker Exegetical Commentary. Baker Academic.
```

### 13.8 Appendix (附錄)

**Appendix Structure:**

```markdown
# 附錄 Appendices

## 附錄 A: 約翰福音年表 Chronology of John's Gospel

| 事件 | 經文 | 大約日期 |
|------|------|----------|
| 耶穌受洗 | 1:29-34 | AD 26 |
| 第一次潔淨聖殿 | 2:13-22 | AD 27 |
| ...

## 附錄 B: 希臘文詞彙表 Greek Vocabulary

| 希臘文 | 音譯 | 中文 | 英文 |
|--------|------|------|------|
| λόγος | logos | 道 | Word |
| ἀλήθεια | aletheia | 真理 | Truth |
| χάρις | charis | 恩典 | Grace |
| ...

## 附錄 C: 地圖集 Maps

[Include TikZ-generated maps or image files]

## 附錄 D: 聖詩索引 Hymn Index

| 聖詩 | 章節 | 主題 |
|------|------|------|
| Amazing Grace | Ch 3, 9 | 重生、醫治 |
| Abide with Me | Ch 15 | 葡萄樹 |
| ...
```

---

## 14. LaTeX Templates

### 14.1 Available Templates

| Template | File | Features | Size |
|----------|------|----------|------|
| **Original** | `gospel-of-john-original.latex` | Basic CJK, TikZ maps, Red Letter | 7×10" |
| **Devotional 2026** | `gospel-devotional-2026.latex` | Elegant memoir, TikZ maps, structure diagrams | 6×9" |
| **Professional 2026** | `gospel-professional-2026.latex` | Full features (emoji, glossary, index, appendix) | 7×10" |
| **Liturgical 2026** | `gospel-liturgical-2026.latex` | Large print, liturgical diagrams, lectern format | 8.5×11" |
| **Scholarly 2026** | `gospel-scholarly-2026.latex` | Apparatus criticus, manuscript diagrams, academic | 7×10" |
| **NIV Study 2026** | `gospel-niv-study-2026.latex` | Study notes, cross-refs, charts, two-column | 7×9.25" |
| **MacArthur 2026** | `gospel-macarthur-2026.latex` | Verse-by-verse, doctrinal notes, deity chart | 6.5×9.5" |

### 14.1a Liturgical Template (NEW - 2026)

The liturgical template (`gospel-liturgical-2026.latex`) provides a premium large-print edition designed for lectern and ceremonial use:

**Key Features:**
- `memoir` document class for elegant book layout
- **Large print (8.5×11" Letter)** designed for lectern reading
- 12pt font size for easy visibility
- Songti SC font for bilingual CJK/English
- **Liturgical Year Diagrams:**
  - Liturgical Year Wheel (seasons: Advent, Christmas, Lent, Easter, Ordinary Time)
  - Liturgical Colors Chart (Purple, White, Green, Red, Black, Rose)
  - Lectionary Cycle Diagram (3-year cycle: Year A/Matthew, Year B/Mark, Year C/Luke)
  - Daily Office Hours Diagram (Matins, Lauds, Vespers, Compline)
  - Eucharistic Prayer Structure
- **Gospel of John Diagrams:**
  - Holy Land Map with key locations
  - Gospel Structure Diagram
  - Seven Signs boxes
  - Seven "I AM" Statements boxes
- Red Letter Bible support (`\jesus{}`)
- Large verse numbers for easy reading
- Rubric commands for liturgical instructions

**Build Script:**
```bash
scripts/build-gospel-liturgical.sh [version]
# Examples:
./scripts/build-gospel-liturgical.sh esv
./scripts/build-gospel-liturgical.sh nasb
./scripts/build-gospel-liturgical.sh nkjv
./scripts/build-gospel-liturgical.sh niv
```

**Output Files:**
```
output/
└── gospel-of-john-liturgical-esv.pdf   (1.2M)
```

**Liturgical Template Custom Commands:**

| Command | Usage |
|---------|-------|
| `\vs{n}` | Large verse number for lectern reading |
| `\chnum{n}` | Extra large chapter number |
| `\jesus{text}` | Red letter for Jesus' words |
| `\rubric{text}` | Liturgical instruction in red |
| `\rubriczh{zh}{en}` | Bilingual rubric |
| `\response{text}` | Congregational response (R) |
| `\versicle{text}` | Versicle (V) |
| `\antiphon{text}` | Antiphon with cross symbols |
| `\antiphonzh{zh}{en}` | Bilingual antiphon |
| `\gloria` | Gloria Patri (bilingual) |
| `\liturgicaldiv` | Three crosses divider |
| `\ornamentdiv` | Diamond ornament divider |
| `\dropcap{letter}` | Red drop cap |

**Liturgical Diagrams:**

| Diagram | Command | Description |
|---------|---------|-------------|
| Liturgical Year | `\liturgicalwheel` | Circular wheel showing church seasons |
| Colors Chart | `\colorschart` | Visual guide to liturgical colors |
| Lectionary | `\lectionarycycle` | 3-year Sunday reading cycle |
| Daily Office | `\dailyoffice` | Hours of prayer throughout the day |
| Eucharist | `\eucharisticstructure` | Structure of the Eucharistic Prayer |
| Holy Land | `\holylandmap` | Map of Gospel locations |
| Structure | `\gospelstructure` | Gospel of John structure diagram |
| Seven Signs | `\sevensignsbox` | Seven miracles box |
| Seven I AM | `\seveniambox` | Seven "I AM" statements box |

**Color Palette (Liturgical Template):**

| Color Name | RGB | Usage |
|------------|-----|-------|
| LiturgicalRed | (165,30,30) | Ceremonial red, verse numbers |
| LiturgicalGold | (184,134,11) | Ornaments, borders |
| LiturgicalBlue | (40,60,100) | Headings, chapter titles |
| JesusRed | (180,0,0) | Jesus's words (Red Letter) |
| RubricRed | (180,40,40) | Liturgical instructions |
| AdventBlue | (75,0,130) | Advent season |
| LentPurple | (128,0,128) | Lent season |
| EasterWhite | (255,215,0) | Easter season |
| OrdinaryGreen | (0,128,0) | Ordinary Time |

---

### 14.1b Devotional Template (ENHANCED)

The devotional template (`gospel-devotional-2026.latex`) provides an elegant, intimate reading experience with full TikZ maps and diagrams:

**Key Features:**
- `memoir` document class for elegant book layout
- Trade paperback size (6×9 inches)
- Songti SC font for bilingual CJK/English
- **TikZ Maps & Diagrams (NEW):**
  - Gospel Locations Map (Sea of Galilee, Jordan River, Dead Sea, cities with verse refs)
  - Gospel Structure Diagram (Prologue → Public Ministry → Private Teaching → Passion)
  - Seven Signs visual (7 miracles with boxes)
  - Seven "I AM" Statements visual (with boxes)
- Simple TikZ ornaments (cross, diamond, vine decorations)
- Devotional reflection boxes
- Red Letter Bible support (`\jesus{}`)
- Scripture boxes with gold borders
- Greek word study environment
- Application boxes
- Hymn references
- Colophon with publishing information

**Build Script:**
```bash
scripts/build-gospel-devotional.sh [version]
# Examples:
./scripts/build-gospel-devotional.sh esv
./scripts/build-gospel-devotional.sh nasb
./scripts/build-gospel-devotional.sh nkjv
./scripts/build-gospel-devotional.sh niv
```

**Output Files:**
```
output/
├── gospel-of-john-devotional-esv.pdf   (1.0M)
├── gospel-of-john-devotional-nasb.pdf  (1.0M)
├── gospel-of-john-devotional-nkjv.pdf  (1.0M)
└── gospel-of-john-devotional-niv.pdf   (1.0M)
```

**Devotional Template Custom Commands:**

| Command | Usage |
|---------|-------|
| `\ornamentline` | Diamond separator with rules |
| `\ornamentbreak` | Three asterisks separator |
| `\ornamentcross` | Cross symbol with horizontal rules |
| `\jesus{text}` | Red letter for Jesus' words |
| `\devotion{text}` | English devotional reflection box |
| `\devotionzh{chinese}{english}` | Bilingual devotional box |
| `\crossref{ref}` | Margin cross reference |
| `\hymn{title}{details}` | Hymn reference with musical note |
| `\biblebook{name}` | Bible book name as chapter |
| `\chapternum{n}` | Decorative chapter number |
| `\versenum{n}` | Verse number superscript |
| `\dropcap{letter}` | Simple drop cap |

**Devotional Template Environments:**

```latex
% Scripture box with optional title
\begin{scripturebox}[約翰福音 1:1-5]
太初有道，道與神同在，道就是神。
\end{scripturebox}

% Greek word study
\begin{greekstudy}[}{λόγος}
希臘文 logos 的深刻含義...
\end{greekstudy}

% Application box
\begin{application}[今日應用]
這段經文如何影響我們的日常生活...
\end{application}
```

**Color Palette (Devotional Template):**

| Color Name | RGB | Usage |
|------------|-----|-------|
| biblered | (139,35,35) | Jesus' words, verse numbers |
| bibleblue | (35,60,100) | Headings, devotion titles |
| biblegold | (184,134,11) | Ornaments, borders |
| lightcream | (252,250,245) | Scripture box background |
| textbrown | (60,45,30) | Body text |
| lightgray | (120,120,120) | Secondary text, page numbers |

### 14.1c Scholarly/Critical Edition Template (NEW - 2026)

The scholarly template (`gospel-scholarly-2026.latex`) provides an academic critical edition designed for seminary and research use:

**Key Features:**
- `memoir` document class for academic book layout
- **Academic size (7×10 inches)** for scholarly publishing
- 11pt font size with wide margins for annotations
- Songti SC font for bilingual CJK/English
- **Greek/Hebrew auto-font switching** via `ucharclasses` package
- **Manuscript Diagrams:**
  - Manuscript Family Tree (Stemma) showing text-type relationships
  - Textual Transmission Timeline (1st-16th century)
  - Canon Formation Diagram (OT, NT, Deuterocanon)
  - Synoptic Problem Diagram (Q Source, Two-Source Theory)
  - Gospel of John Structure Diagram
- **Scholarly Apparatus:**
  - Apparatus criticus footnotes (`\apparatus{}`)
  - Manuscript sigla formatting (`\ms{}`)
  - Greek text inline (`\gk{}`)
  - Textual variant boxes (`\txtvar{}`)
  - Marginal notes
- **Gospel of John Diagrams:**
  - Holy Land Map with key locations
  - Gospel Structure Diagram
  - Seven Signs boxes
  - Seven "I AM" Statements boxes
- Red Letter Bible support (`\jesus{}`)

**Build Script:**
```bash
scripts/build-gospel-scholarly.sh [version]
# Examples:
./scripts/build-gospel-scholarly.sh esv
./scripts/build-gospel-scholarly.sh nasb
./scripts/build-gospel-scholarly.sh nkjv
./scripts/build-gospel-scholarly.sh niv
```

**Output Files:**
```
output/
└── gospel-of-john-scholarly-esv.pdf   (1.1M)
```

**Scholarly Template Custom Commands:**

| Command | Usage |
|---------|-------|
| `\ms{sigla}` | Manuscript sigla (e.g., `\ms{P66}`, `\ms{א}`) |
| `\gk{text}` | Inline Greek text with proper font |
| `\apparatus{text}` | Apparatus criticus footnote |
| `\txtvar{text}` | Textual variant discussion box |
| `\marginref{ref}` | Marginal cross-reference |
| `\jesus{text}` | Red letter for Jesus' words |
| `\vs{n}` | Verse number with proper styling |
| `\chnum{n}` | Chapter number with scholarly styling |
| `\dropcap{letter}` | Drop cap for chapter openings |

**Scholarly Diagrams:**

| Diagram | Command | Description |
|---------|---------|-------------|
| Stemma | `\stemmadiagram` | Manuscript family tree (Autograph → Text-types) |
| Timeline | `\transmissiontimeline` | Textual transmission from 1st-16th century |
| Canon | `\canondiagram` | Canon formation (OT, NT, Deuterocanon) |
| Synoptic | `\synopticdiagram` | Q Source and Two-Source Theory |
| Structure | `\johnstructure` | Gospel of John structure diagram |
| Holy Land | `\holylandmap` | Map of Gospel locations |
| Seven Signs | `\sevensignsbox` | Seven miracles box |
| Seven I AM | `\seveniambox` | Seven "I AM" statements box |

**Text-Type Color Coding:**

| Text-Type | Color | Manuscripts |
|-----------|-------|-------------|
| Alexandrian | Green (0,100,0) | P66, P75, א, B, C |
| Western | Red (180,0,0) | D, it, sy |
| Byzantine | Purple (128,0,128) | A, E, majority |
| Caesarean | Orange (255,140,0) | (mixed witnesses) |

**Color Palette (Scholarly Template):**

| Color Name | RGB | Usage |
|------------|-----|-------|
| ScholarBlue | (25,45,85) | Headings, chapter titles |
| ScholarGray | (80,80,80) | Body text |
| ScholarRed | (140,20,20) | Timeline markers |
| ApparatusGray | (100,100,100) | Footnote apparatus |
| JesusRed | (180,0,0) | Jesus's words (Red Letter) |
| PapyrusColor | (210,180,140) | Papyrus manuscript nodes |
| UncialColor | (139,90,43) | Uncial manuscript nodes |
| MinusculeColor | (85,107,47) | Minuscule manuscript nodes |

### 14.1d NIV Study Bible Template (NEW - 2026)

The NIV Study Bible template (`gospel-niv-study-2026.latex`) provides a comprehensive study edition inspired by the NIV Study Bible format:

**Key Features:**
- `memoir` document class for study Bible layout
- **Study Bible size (7×9.25 inches)** standard study format
- 10pt font for dense but readable text
- Songti SC font for bilingual CJK/English
- **Two-column layout** with column separator
- **Study Notes** (footnote style)
- **Cross-references** (margin and inline)
- **Book Introduction & Outline**
- **TikZ Charts & Diagrams:**
  - Gospel Structure Chart
  - Seven Signs Chart (bilingual)
  - I AM Statements Chart (bilingual)
  - Holy Land Map
  - Ministry Timeline
- **Special Boxes:**
  - Word Study boxes
  - Character Profile boxes
  - Theological Note boxes
  - Historical/Cultural Background boxes
- Red Letter Bible support (`\jesus{}`)
- Key verse highlighting

**Build Script:**
```bash
scripts/build-gospel-niv-study.sh [version]
# Examples:
./scripts/build-gospel-niv-study.sh esv
./scripts/build-gospel-niv-study.sh nasb
./scripts/build-gospel-niv-study.sh nkjv
./scripts/build-gospel-niv-study.sh niv
```

**Output Files:**
```
output/
└── gospel-of-john-niv-study-esv.pdf   (1.1M)
```

**NIV Study Template Custom Commands:**

| Command | Usage |
|---------|-------|
| `\vs{n}` | Verse number (superscript blue) |
| `\chnum{n}` | Large chapter drop cap |
| `\sectionhead{title}` | Section heading |
| `\sectionheadzh{zh}{en}` | Bilingual section heading |
| `\xref{refs}` | Margin cross-reference |
| `\inlinexref{refs}` | Inline cross-reference |
| `\studynote{ref}{text}` | Study note (footnote) |
| `\keyverse{text}` | Highlighted key verse |
| `\jesus{text}` | Red letter for Jesus' words |

**NIV Study Template Environments:**

| Environment | Usage |
|-------------|-------|
| `wordstudy` | Greek/Hebrew word analysis box |
| `characterbox{name}` | Character profile box |
| `theologybox` | Theological note box |
| `culturebox` | Historical/Cultural background box |
| `bookintro` | Book introduction box |

**NIV Study Diagrams:**

| Diagram | Command | Description |
|---------|---------|-------------|
| Structure | `\johnstructurechart` | Gospel structure (Prologue, Signs, Glory, Epilogue) |
| Signs | `\sevensignschart` | Seven miraculous signs with meanings |
| I AM | `\iamchart` | Seven I AM statements |
| Map | `\johnlocationsmap` | Key locations in John |
| Timeline | `\johntimeline` | Jesus' ministry timeline |

**Color Palette (NIV Study Template):**

| Color Name | RGB | Usage |
|------------|-----|-------|
| NIVBlue | (0,51,102) | Headings, chapter titles, verse numbers |
| NIVRed | (153,0,0) | Theological notes, emphasis |
| NIVGold | (184,134,11) | Character boxes, key verse highlight |
| JesusRed | (180,0,0) | Jesus's words (Red Letter) |
| CrossRefGray | (100,100,100) | Cross-references |
| HeaderGray | (60,60,60) | Page headers |

### 14.1e MacArthur Study Bible Template (NEW - 2026)

The MacArthur Study Bible template (`gospel-macarthur-2026.latex`) provides a verse-by-verse expository study edition inspired by the MacArthur Study Bible format:

**Key Features:**
- `memoir` document class for study Bible layout
- **Study Bible size (6.5×9.5 inches)** compact study format
- 10pt font for dense but readable text
- Songti SC font for bilingual CJK/English
- **Greek/Hebrew auto-font switching** via `ucharclasses` package
- **Single-column layout** with wide margins for notes
- **Verse-by-Verse Commentary** (MacArthur's distinctive feature)
- **Doctrinal Notes** (highlighted in red)
- **Word Studies** (Greek/Hebrew with transliteration)
- **Book Introduction & Outline**
- **TikZ Charts & Diagrams:**
  - Gospel of John Structure Chart (Prologue → Signs → Glory → Epilogue)
  - Deity of Christ Chart (10 evidence nodes)
  - Seven Signs Table (bilingual with significance)
  - I AM Statements Table (bilingual with meaning)
  - Passion Week Timeline (12-21章)
- **Special Boxes:**
  - Key Verse boxes (gold border)
  - Doctrine boxes (blue theme)
  - Historical/Cultural Background boxes
  - Word Study boxes
- Red Letter Bible support (`\jesus{}`)

**Build Script:**
```bash
scripts/build-gospel-macarthur.sh [version]
# Examples:
./scripts/build-gospel-macarthur.sh esv
./scripts/build-gospel-macarthur.sh nasb
./scripts/build-gospel-macarthur.sh nkjv
./scripts/build-gospel-macarthur.sh niv
```

**Output Files:**
```
output/
└── gospel-of-john-macarthur-esv.pdf   (1.1M)
```

**MacArthur Template Custom Commands:**

| Command | Usage |
|---------|-------|
| `\vs{n}` | Verse number (bold blue superscript) |
| `\chnum{n}` | Large chapter number |
| `\sectionhead{title}` | Section heading |
| `\sectionheadzh{zh}{en}` | Bilingual section heading |
| `\xref{refs}` | Inline cross-reference |
| `\versenote{ref}{text}` | Verse-by-verse commentary note |
| `\versenotezh{ref}{zh}{en}` | Bilingual verse note |
| `\doctrinenote{title}{text}` | Doctrinal note (highlighted red) |
| `\gkword{word}{greek}` | Greek word study |
| `\hbword{word}{hebrew}` | Hebrew word study |
| `\jesus{text}` | Red letter for Jesus' words |
| `\notesdivider` | Horizontal rule for notes sections |

**MacArthur Template Environments:**

| Environment | Usage |
|-------------|-------|
| `keyversebox` | Key verse highlight box (gold border) |
| `doctrinebox[title]` | Doctrinal exposition box (blue theme) |
| `historybox` | Historical/Cultural background box |
| `wordbox[word]` | Word study box (gold accent) |
| `bookintro` | Book introduction box |

**MacArthur Template Diagrams:**

| Diagram | Command | Description |
|---------|---------|-------------|
| Structure | `\johnoutlinechart` | Gospel structure (Prologue → Signs → Glory → Epilogue) |
| Deity | `\deitychart` | Deity of Christ evidence (10 proof nodes) |
| Signs | `\signstable` | Seven miraculous signs table |
| I AM | `\iamtable` | Seven I AM statements table |
| Passion | `\passionweek` | Passion Week timeline (chapters 12-20) |

**Color Palette (MacArthur Template):**

| Color Name | RGB | Usage |
|------------|-----|-------|
| MacBlue | (0,40,85) | Headings, chapter titles, verse numbers |
| MacRed | (139,0,0) | Doctrinal notes, emphasis |
| MacGold | (184,134,11) | Key verse borders, word study accents |
| JesusRed | (180,0,0) | Jesus's words (Red Letter) |
| DoctrineBlue | (20,60,100) | Doctrine box theme |
| VerseGray | (70,70,70) | Commentary text |
| RefGray | (100,100,100) | Cross-references |
| NoteBg | (252,250,245) | Note background |
| KeyVerseBg | (255,250,235) | Key verse box background |
| DoctrineBg | (240,245,255) | Doctrine box background |
| HistoryBg | (252,250,245) | History box background |
| WordBg | (255,252,240) | Word study background |

### 14.2 Template Selection in Build Script

```bash
# For basic builds
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-of-john-original.latex"

# For professional builds with all features
TEMPLATE="$PROJECT_ROOT/templates/pdf/gospel-professional-2026.latex"
```

### 14.3 Professional Template Features

| Feature | LaTeX Package | Status |
|---------|---------------|--------|
| Emoji support | `fontspec` + Apple Color Emoji | ✅ |
| Numbered figures | `caption`, `float` | ✅ |
| Numbered tables | `caption`, `longtable` | ✅ |
| Numbered notes | `tcolorbox` custom | ✅ |
| Glossary | `glossaries` | ✅ |
| Bibliography | `biblatex` | ✅ |
| Index | `makeidx` | ✅ |
| Appendix | `appendix` | ✅ |
| Red Letter Bible | `\jesus{}` command | ✅ |
| TikZ diagrams | `tikz` | ✅ |
| Greek/Hebrew fonts | `ucharclasses` | ✅ |

### 14.4 Custom LaTeX Environments

**Scripture Box:**
```latex
\begin{scripturebox}[約翰福音 1:1-5]
太初有道，道與神同在，道就是神。
\end{scripturebox}
```

**Greek Word Study Box:**
```latex
\begin{greekbox}[λόγος]
希臘文 logos 在約翰福音開篇的深刻含義...
\end{greekbox}
```

**Application Box:**
```latex
\begin{applicationbox}[今日應用]
這段經文如何影響我們的日常生活...
\end{applicationbox}
```

**Note Box (numbered):**
```latex
\begin{notebox}
重要觀察：約翰特別強調見證的主題...
\end{notebox}
```

### 14.5 Section Dividers

```latex
\sectiondivider[\emoji{✝️}]  % With emoji
\sectiondivider              % Plain divider
```

### 14.6 Color Scheme

| Color Name | RGB | Usage |
|------------|-----|-------|
| ChapterBlue | (25,55,95) | Chapter titles, sections |
| ScriptureGold | (165,125,55) | Decorations, rules |
| CommentaryBrown | (85,60,45) | Subsections, commentary |
| JesusRed | (204,0,0) | Jesus' words (Red Letter) |
| TextGray | (50,50,50) | Body text |
| ScriptureBg | (252,250,245) | Scripture box background |
| GreekBg | (245,248,252) | Greek study background |
| ApplicationBg | (248,252,248) | Application box background |

---

## 15. Extended Quality Checklist

### Pre-Publication Review

**Content Quality:**
- [ ] All scripture quotes verified against source version
- [ ] Chinese translations match RCUV
- [ ] Greek/Hebrew terms verified with lexicons
- [ ] Commentary citations are accurate and verifiable
- [ ] No fabricated quotes or references

**Professional Elements:**
- [ ] Figures numbered correctly (Chapter.Figure)
- [ ] Tables numbered correctly (Chapter.Table)
- [ ] Notes numbered correctly (Chapter.Note)
- [ ] Glossary entries complete and accurate
- [ ] Bibliography formatted consistently
- [ ] Index entries comprehensive
- [ ] Appendices properly structured

**Visual Quality:**
- [ ] Emoji render correctly (if using professional template)
- [ ] TikZ diagrams display properly
- [ ] Red Letter markup visible for Jesus' words
- [ ] Page breaks appropriate (no orphans/widows)
- [ ] Table of Contents accurate

**Technical Quality:**
- [ ] PDF file size reasonable (<5MB per book)
- [ ] Hyperlinks functional
- [ ] Bookmarks properly nested
- [ ] Fonts embedded correctly

---

*三書精讀出版系統 · Published Standard Bible 2026 v2.1 · Soli Deo Gloria*

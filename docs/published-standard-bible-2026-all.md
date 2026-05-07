# PubHub Bible Study Book Standard 2026

## 三書精讀聖經研讀標準 (Published Standard)

**Version**: 2026.01
**Effective Date**: January 2026
**Applies To**: All Bible study books in the PubHub system

---

## 1. Translation Standard

### Primary Translations (Bilingual Format)

| Order | Language | Translation | Usage |
|-------|----------|-------------|-------|
| 1 | **中文** | 和合本修訂版 (RCUV) | Primary Chinese text |
| 2 | **English** | ESV (English Standard Version) | Primary English text |

### Format in Markdown

```markdown
### 中文 — 和合本修訂版 (RCUV)

> ^1^經文內容...

### English — ESV

> ^1^Scripture content...
```

### Verse Number Format

- Use superscript: `^1^` → renders as superscript 1
- LaTeX conversion: `^1^` → `\textsuperscript{1}`

---

## 2. Chapter Structure Standard

Every chapter must follow this structure:

```markdown
---
title: 章節標題
subtitle: Chapter Title in English
chapter: [number]
scripture: [經文範圍]
---

# 章節標題 (Chapter Title)

經文範圍

## 經文 (Scripture)

### 中文 — 和合本修訂版 (RCUV)
> [Chinese text with verse numbers]

### English — ESV
> [English text with verse numbers]

---

## 背景 (Context)

[Historical and literary context]

---

## 原文研讀 (Word Study)

| 希臘文 | 音譯 | 意義 | 出現次數 |
|--------|------|------|----------|
| [Greek] | [transliteration] | [meaning] | [count] |

---

## 解經洞見 (Commentary)

### John MacArthur
> [Quote with citation]

### G. Campbell Morgan
> [Quote with citation]

---

## 神學要點 (Theological Points)

### 1. [Point Title]
[Explanation]

### 2. [Point Title]
[Explanation]

---

## 個人反思 (Personal Reflection)

1. [Reflection question]
2. [Reflection question]
3. [Reflection question]

---

## 配詩 (Hymns & Psalms)

**聖詩**: [Hymn name]
> [Lyrics]

**詩篇**: [Psalm reference]
> [Text]

---

*三書精讀項目 · [Book Name] · [Chapter]*
```

---

## 3. Core Resources (三方整合)

All Bible study content must integrate these three primary sources:

| Resource | Type | Usage |
|----------|------|-------|
| **黃長老 (Elder Wong)** | 第一手教導 | Primary spiritual teaching |
| **John MacArthur** | 逐節解經 | Verse-by-verse exposition |
| **G. Campbell Morgan** | 解經王子 | Devotional insight |

### Citation Format

```markdown
> "Quote text here."
> — Author Name, *Book Title*
```

---

## 4. File Naming Convention

### Chapter Files

```
[NN]-[topic-name].md

Examples:
00-overview.md
01-prologue.md
02-cana-wedding.md
03-nicodemus.md
```

### Special Files

```
00-overview.md       # Book overview (required)
complete-book.md     # Combined full text
README.md            # Book documentation
```

---

## 5. YAML Frontmatter Standard

```yaml
---
title: 中文標題
subtitle: English Subtitle
chapter: [number]
scripture: [經文範圍]
author: PubHub 三書精讀系統
date: 2026年[月]月
publisher: 三書精讀出版系統
---
```

---

## 6. LaTeX Template Standard

### Template Location

```
templates/pdf/[book-name].latex
```

### Required Features

- XeLaTeX for CJK support
- Greek/Hebrew font auto-switching (ucharclasses)
- Red Letter Bible support (`\jesus{}` command)
- Professional 7×10 inch format
- Table of contents
- Scripture boxes with backgrounds

### Core LaTeX Commands

```latex
% Red Letter Bible - Jesus's Words
\definecolor{JesusRed}{RGB}{204,0,0}
\newcommand{\jesus}[1]{\textcolor{JesusRed}{#1}}

% Verse superscript
\textsuperscript{1}
```

---

## 7. Build Script Standard

### Script Location

```
scripts/build-[book-name]-pdf.sh
```

### Required Functionality

1. Combine all chapter markdown files
2. Skip YAML frontmatter (lines 1-7)
3. Convert `^number^` to `\textsuperscript{number}`
4. Add `\newpage` between chapters
5. Generate PDF via pandoc + xelatex
6. Report success/failure with file size

---

## 8. Directory Structure

```
books/bible/[book-name]/
├── 00-overview.md           # Book overview
├── 00-prologue.md           # Prologue (if applicable)
├── 01-[chapter-name].md     # Chapter 1
├── 02-[chapter-name].md     # Chapter 2
├── ...
├── README.md                # Documentation
└── complete-book.md         # Combined text

templates/pdf/
├── [book-name].latex        # PDF template

scripts/
├── build-[book-name]-pdf.sh # Build script

output/
├── [book-name].pdf          # Generated PDF
├── [book-name]-combined.md  # Combined markdown
```

---

## 9. Quality Checklist

Before publishing any chapter:

- [ ] 聖經引文是否準確？(RCUV/ESV)
- [ ] 中英對照是否完整？
- [ ] 注疏引用是否可查證？
- [ ] 邏輯是否連貫？
- [ ] 是否有屬靈洞見（而非常識）？
- [ ] 格式是否符合規範？
- [ ] 希臘文/希伯來文是否正確顯示？

---

## 10. Core Formula

> **榮耀 = 恩典 + 真理**
> **Glory = Grace + Truth**

This formula from John 1:14 guides all Bible study content:

| 恩典 (Grace) | 真理 (Truth) |
|--------------|--------------|
| 七個神蹟 (works) | 七個「我是」(words) |
| 神白白的禮物 | 神啟示的本質 |
| 救恩的基礎 | 信仰的內容 |

---

## 11. Books Using This Standard

| Book | Status | Location |
|------|--------|----------|
| 約翰福音 (Gospel of John) | ✅ Complete | `books/bible/gospel-of-john/` |
| 馬太福音 (Gospel of Matthew) | ✅ Complete | `books/bible/gospel-of-matthew/` |
| 馬可福音 (Gospel of Mark) | 📝 In Progress | `books/bible/gospel-of-mark/` |
| 四福音合參 (Gospel Harmony) | 📝 In Progress | `books/bible/gospel-harmony/` |

---

## 12. Forbidden Practices

- ❌ Fabricated Scripture quotes (不杜撰經文)
- ❌ Unverifiable commentary (不編造注疏)
- ❌ Empty spiritual jargon (避免空洞套話)
- ❌ AI-generated filler content (避免AI腔調)
- ❌ Excessive emojis (避免過度使用emoji)
- ❌ Using translations other than RCUV/ESV as primary

---

## 13. Version History

| Version | Date | Changes |
|---------|------|---------|
| 2026.01 | 2026-01-04 | Initial published standard |

---

**Soli Deo Gloria — 唯獨榮耀神**

*三書精讀出版系統 · PubHub Publishing System · 2026*

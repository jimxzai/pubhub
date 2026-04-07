# Product Requirements Document (PRD)
## 生命之道 — 約翰福音研讀項目

**Version**: 1.0
**Date**: 2025-12-28
**Product Name**: Gospel of John Study System
**Document Status**: Draft

---

## 1. Product Overview

### 1.1 Vision
打造一個 AI 輔助的聖經研讀系統，讓信徒能夠深入、系統地研讀約翰福音，並產出高質量的雙語研讀材料。

### 1.2 Mission
透過「道」(Logos) 的主題框架，幫助使用者理解約翰福音的神學深度，同時保持實際的生命應用。

---

## 2. User Personas

### 2.1 Primary User: 研讀者
- **背景**: 有基本聖經知識的信徒
- **目標**: 深入研讀約翰福音，建立系統性筆記
- **痛點**:
  - 不知從何下手
  - 缺乏原文知識
  - 難以找到可靠注疏
- **需求**:
  - 結構化的研讀框架
  - AI 輔助查找注疏
  - 自動格式化輸出

### 2.2 Secondary User: 小組帶領者
- **背景**: 教會小組長或主日學老師
- **目標**: 準備查經材料
- **需求**:
  - 可分享的筆記格式
  - 討論問題生成
  - 周報摘要

---

## 3. Feature Specifications

### 3.1 核心功能

#### F1: 每日研讀筆記系統
**Priority**: P0 (Must Have)

| Attribute | Specification |
|-----------|---------------|
| Input | 當日經文範圍、個人心得 |
| Output | 格式化的研讀筆記 (Markdown) |
| Format | 經文、背景、原文、注疏、應用 |

**User Story**:
> 作為研讀者，我希望有一個標準化的筆記模板，以便我每天都能有系統地記錄研讀心得。

---

#### F2: AI 注疏師 (`/annotate`)
**Priority**: P0 (Must Have)

| Attribute | Specification |
|-----------|---------------|
| Input | 研讀筆記或經文段落 |
| Output | 添加歷代注疏的豐富版本 |
| Sources | 教父、改革宗、當代福音派 |

**Acceptance Criteria**:
- [ ] 每條注疏標明出處和作者
- [ ] 提供中英對照
- [ ] 希臘原文詞彙附音譯和解釋

---

#### F3: AI 校對神 (`/proofread`)
**Priority**: P0 (Must Have)

| Attribute | Specification |
|-----------|---------------|
| Input | 草稿筆記 |
| Output | 校對後的版本 |
| Checks | 聖經引文、邏輯、語法、格式 |

**Acceptance Criteria**:
- [ ] 聖經引文 100% 準確
- [ ] 邏輯連貫性檢查
- [ ] 中英雙語潤色

---

#### F4: 出版系統 (`/publish`)
**Priority**: P1 (Should Have)

| Attribute | Specification |
|-----------|---------------|
| Input | 累積的研讀筆記 |
| Output | 周報、月報、書稿 |
| Format | Markdown / PDF ready |

---

#### F5: 總編輯 (`/master-editor`)
**Priority**: P1 (Should Have)

| Attribute | Specification |
|-----------|---------------|
| Input | 每日筆記 |
| Output | 質量評估報告、分類建議 |
| Metrics | 完整度、深度、準確性 |

---

### 3.2 內容結構

#### 3.2.1 研讀筆記模板

```markdown
# 約翰福音 [Chapter]:[Verses]

## 經文 (Scripture)
> [RCUV 中文]

> [ESV English]

## 背景 (Context)
- 歷史背景
- 文學結構
- 上下文連接

## 原文研讀 (Word Study)
| 希臘文 | 音譯 | 意義 | 出現次數 |
|--------|------|------|----------|

## 神學要點 (Theological Points)
1. ...
2. ...

## 歷代注疏 (Historical Commentary)
- **[作者]**: "[引文]" — [出處]

## 生命應用 (Application)
- ...

## 反思問題 (Reflection Questions)
1. ...
```

---

#### 3.2.2 章節分類

**Part 1: 序言 (Prologue)** - Ch 1:1-18
- 道的本質與榮耀

**Part 2: 公開事工 (Public Ministry)** - Ch 1:19-12:50
- 神蹟與講論
- 接受與拒絕

**Part 3: 私下教導 (Private Teaching)** - Ch 13-17
- 馬可樓上講論
- 大祭司禱告

**Part 4: 受難與復活 (Passion & Resurrection)** - Ch 18-21
- 十架與空墳
- 復活顯現

---

## 4. Technical Specifications

### 4.1 File Structure

```
docs/
├── BRD-gospel-of-john.md      # 商業需求文檔
├── PRD-gospel-of-john.md      # 產品需求文檔 (本文件)
└── study-notes/
    ├── 00-overview.md         # 全書概覽
    ├── 01-prologue.md         # 1:1-18 序言
    ├── 02-ch1-witness.md      # 1:19-51 見證
    ├── 03-ch2-cana.md         # 2:1-25 迦拿婚宴
    └── ...
```

### 4.2 Naming Convention
- Files: `NN-short-description.md`
- Headers: 繁體中文 (英文備註)
- References: `約 1:1` or `John 1:1`

### 4.3 Quality Gates

| Stage | Check | Tool |
|-------|-------|------|
| Draft | 完整性 | `/master-editor` |
| Review | 注疏添加 | `/annotate` |
| Final | 校對潤色 | `/proofread` |
| Publish | 格式輸出 | `/publish` |

---

## 5. Content Roadmap

### 5.1 Current Progress

| Chapter | Status | Notes |
|---------|--------|-------|
| 1:1-18 | Draft | 序言已完成初稿 |
| 1:19-51 | Draft | 見證與呼召 |
| 2-3 | Planned | 下一步 |
| 4-6 | Planned | 神蹟系列 |
| 7-12 | Planned | 講論與衝突 |
| 13-17 | Planned | 馬可樓上 |
| 18-21 | Planned | 受難復活 |

### 5.2 Next Steps
1. 完成約翰福音第二章研讀
2. 建立神蹟 (Signs) 專題研讀
3. 添加歷代注疏

---

## 6. Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| 章節覆蓋率 | 100% (21 章) | ~5% |
| 注疏引用數 | 每章 3+ 條 | TBD |
| 校對通過率 | 100% | TBD |
| 用戶滿意度 | 4.5/5 | TBD |

---

## 7. Dependencies

### 7.1 External
- Bible Gateway API (經文查詢)
- Logos Bible Software (原文研究)
- Claude Code (AI 輔助)

### 7.2 Internal
- `/annotate` skill 正常運作
- `/proofread` skill 正常運作
- `/publish` skill 正常運作

---

## 8. Open Questions

1. **語言優先**: 以繁體中文為主，還是中英並重？
   - **決定**: 繁體中文為主，關鍵術語中英對照

2. **出版格式**: 最終輸出為 PDF 還是電子書？
   - **待定**: 根據使用需求決定

3. **更新頻率**: 每日更新還是每周批量更新？
   - **建議**: 每日研讀，每周整理

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-28 | Claude Code | Initial draft |

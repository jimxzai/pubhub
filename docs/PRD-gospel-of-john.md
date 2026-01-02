# Product Requirements Document (PRD)
## 生命之道 — 約翰福音研讀項目

**Version**: 3.0
**Date**: 2026-01-01
**Product Name**: Gospel of John Study System
**Document Status**: Active MVP

---

## 1. Product Overview

### 1.1 Vision

打造一個 AI 輔助的聖經研讀系統，讓信徒能夠深入、系統地研讀約翰福音，並產出高質量的雙語研讀材料。

### 1.2 Mission

透過「道」(Logos) 的主題框架，幫助使用者理解約翰福音的神學深度，同時保持實際的生命應用。

### 1.3 MVP 核心定義

> **"Truly Go Deeper"** — 寧深不廣，專注約翰福音一卷書

#### MVP 特色

| 要素 | 規格 |
|------|------|
| 經卷範圍 | 約翰福音 21 章 (唯一焦點) |
| 核心資源 | 黃長老 + gty.org + Campbell Morgan |
| 研讀節奏 | Day-to-day 每日靈修 |
| 產出形式 | 結構化筆記 + 周報 |

#### 核心資源詳述

**黃長老 (Elder Wong) — 第一手教導**

- 週四查經班現場教導
- Zoom 錄影存檔 (用戶提供)
- 原創筆記與大綱 (用戶提供)
- 華人教會處境應用

**Grace to You (gty.org)**

- John MacArthur 約翰福音講道系列
- 逐節解經，忠於原文
- 強調基督神性與救恩教義
- 網站: <https://www.gty.org>

**G. Campbell Morgan**

- *The Gospel According to John* (1909)
- "解經王子" (Prince of Expositors)
- 屬靈組織 (Spiritual Organization) 分析法
- 深刻的靈修洞見

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

**User Stories**:

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-1.1 | 作為研讀者，我希望有一個標準化的筆記模板，以便我每天都能有系統地記錄研讀心得。 | - 模板包含所有必要欄位<br>- 可快速複製使用<br>- 格式一致性 |
| US-1.2 | 作為研讀者，我希望能整合黃長老、MacArthur、Morgan三方資源，以便獲得全面的理解。 | - 每章引用至少1處gty.org<br>- 每章引用至少1處Morgan<br>- 整合華人處境應用 |
| US-1.3 | 作為研讀者，我希望能看到中英雙語經文對照，以便深入理解原意。 | - RCUV中文<br>- ESV英文<br>- 格式清晰可讀 |

---

#### F2: AI 注疏師 (`/annotate`)
**Priority**: P0 (Must Have)

| Attribute | Specification |
|-----------|---------------|
| Input | 研讀筆記或經文段落 |
| Output | 添加歷代注疏的豐富版本 |
| Sources | 教父、改革宗、當代福音派 |

**User Stories**:

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-2.1 | 作為研讀者，我希望能查看歷代教父的註解，以便理解教會傳統詮釋。 | - 引用來源清晰<br>- 標明作者年代<br>- 中英對照 |
| US-2.2 | 作為研讀者，我希望能學習希臘原文詞彙，以便深入理解經文原意。 | - 希臘文正確顯示<br>- 附音譯 (transliteration)<br>- 詞義解釋 |
| US-2.3 | 作為小組帶領者，我希望能獲得多元觀點的註解，以便豐富查經討論。 | - 至少3個來源<br>- 涵蓋不同時代<br>- 可作討論素材 |

---

#### F3: AI 校對神 (`/proofread`)
**Priority**: P0 (Must Have)

| Attribute | Specification |
|-----------|---------------|
| Input | 草稿筆記 |
| Output | 校對後的版本 |
| Checks | 聖經引文、邏輯、語法、格式 |

**User Stories**:

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-3.1 | 作為研讀者，我希望確保所有聖經引文100%準確，以免誤導讀者。 | - 經文與RCUV/ESV完全一致<br>- 章節引用正確<br>- 無遺漏或錯字 |
| US-3.2 | 作為研讀者，我希望文章邏輯清晰連貫，以便讀者容易跟隨。 | - 段落之間有連接<br>- 論點有支持<br>- 結構合理 |
| US-3.3 | 作為研讀者，我希望中英雙語表達都流暢自然，以提升可讀性。 | - 中文語法正確<br>- 英文表達地道<br>- 術語一致 |

---

#### F4: 出版系統 (`/publish`)
**Priority**: P1 (Should Have)

| Attribute | Specification |
|-----------|---------------|
| Input | 累積的研讀筆記 |
| Output | 周報、月報、書稿 |
| Format | Markdown / PDF ready |

**User Stories**:

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-4.1 | 作為研讀者，我希望每周自動生成周報摘要，以便回顧本週學習。 | - 自動整合當週內容<br>- 摘要精煉<br>- 包含反思問題 |
| US-4.2 | 作為研讀者，我希望累積內容能生成書稿格式，以便將來出版。 | - 章節結構完整<br>- 格式統一<br>- 可轉換為PDF |
| US-4.3 | 作為小組帶領者，我希望能分享整合好的查經材料，以便小組使用。 | - 可分享格式<br>- 內容完整<br>- 排版整齊 |

---

#### F5: 總編輯 (`/master-editor`)
**Priority**: P1 (Should Have)

| Attribute | Specification |
|-----------|---------------|
| Input | 每日筆記 |
| Output | 質量評估報告、分類建議 |
| Metrics | 完整度、深度、準確性 |

**User Stories**:

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-5.1 | 作為研讀者，我希望獲得筆記質量評估，以便知道改進方向。 | - 評估各維度分數<br>- 具體改進建議<br>- 優先順序排列 |
| US-5.2 | 作為研讀者，我希望筆記能自動分類歸檔，以便後續查找。 | - 按章節分類<br>- 按主題標籤<br>- 搜索友好 |

---

#### F6: AI 戰略家 (`/ai-parallels`)
**Priority**: P2 (Could Have)

| Attribute | Specification |
|-----------|---------------|
| Input | 研讀筆記或經文段落 |
| Output | 現代AI/科技案例對照 |
| Scope | 2025-2035 AI發展趨勢 |

**User Stories**:

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-6.1 | 作為科技業信徒，我希望看到聖經智慧與AI時代的對照，以便將信仰應用於工作。 | - 案例相關性高<br>- 類比合理<br>- 應用具體 |
| US-6.2 | 作為研讀者，我希望理解古代智慧如何應對現代挑戰，以增強信仰實踐。 | - 連結清晰<br>- 避免牽強附會<br>- 啟發思考 |

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

| Chapter | Status | Location |
|---------|--------|----------|
| 1:1-18 | ✅ Complete | `01-prologue.md` |
| 1:19-51 | ✅ Complete | `01-prologue.md` |
| 2 (迦拿婚宴) | ✅ Complete | `02-cana-wedding.md` |
| 3 (尼哥底母) | ✅ Complete | `03-nicodemus.md` |
| 4 (撒馬利亞婦人) | ✅ Complete | `04-samaritan-woman.md` |
| 5 (畢士大池) | ✅ Complete | `05-bethesda.md` |
| 6 (生命的糧) | ✅ Complete | `06-bread-of-life.md` |
| 7 (住棚節) | ✅ Complete | `07-feast-tabernacles.md` |
| 8 (世界的光) | ✅ Complete | `08-light-of-world.md` |
| 9 (生來瞎眼) | ✅ Complete | `09-blind-man.md` |
| 10 (好牧人) | ✅ Complete | `10-good-shepherd.md` |
| 11 (拉撒路) | ✅ Complete | `11-lazarus.md` |
| 12 (榮耀進城) | ✅ Complete | `12-triumphal-entry.md` |
| 13 (洗腳) | ✅ Complete | `13-washing-feet.md` |
| 14 (道路真理生命) | ✅ Complete | `14-way-truth-life.md` |
| 15 (真葡萄樹) | ✅ Complete | `15-true-vine.md` |
| 16 (聖靈) | ✅ Complete | `16-holy-spirit.md` |
| 17 (大祭司禱告) | ✅ Complete | `17-high-priestly-prayer.md` |
| 18 (被捕受審) | ✅ Complete | `18-arrest-trial.md` |
| 19 (十架) | ✅ Complete | `19-crucifixion.md` |
| 20 (復活) | ✅ Complete | `20-resurrection.md` |
| 21 (跋) | ✅ Complete | `21-epilogue.md` |

### 5.2 Next Steps

1. ✅ ~~完成約翰福音第二章研讀~~ (已完成)
2. ✅ ~~建立神蹟 (Signs) 專題研讀~~ (已完成)
3. ✅ ~~整合 gty.org 和 Campbell Morgan 資源~~ (已完成)
4. 🚧 擴展至約翰書信 (1-3 John)
5. 🚧 擴展至路加-使徒行傳
6. 📋 內容質量審核與修訂
7. 📋 PDF出版準備

### 5.3 每日靈修節奏 (Day-to-Day Rhythm)

#### 研讀流程

```text
📖 早晨 (45-60分鐘)
├── 1. 禱告預備 — 求聖靈開啟心眼
├── 2. 經文朗讀 — 中英對照 (RCUV + ESV)
├── 3. 黃長老教導 — Zoom 錄影 + 查經筆記
├── 4. MacArthur 資源 — gty.org 講道/注釋
├── 5. Morgan 洞見 — 屬靈結構分析
└── 6. 筆記記錄 — 整合三方洞見

🌙 晚間 (15分鐘)
├── 回顧經文
├── 反思應用
└── 禱告回應
```

#### 週間安排

| 日 | 活動 | 產出 |
|----|------|------|
| 週一-週六 | 每日靈修研讀 | 個人筆記 |
| 週日 | 本週整合回顧 | 周報摘要 |

#### 屬靈組織理解目標

- 掌握約翰福音四大部分結構
- 理解七個神蹟的屬靈意義
- 領會七個「我是」的神學深度
- 建立「道」的整全觀念

---

## 6. Success Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| 約翰福音章節覆蓋率 | 100% (21 章) | **100%** | ✅ 達標 |
| 注疏引用數 | 每章 3+ 條 | 審核中 | 🔍 驗證中 |
| 校對通過率 | 100% | 審核中 | 🔍 驗證中 |
| 用戶滿意度 | 4.5/5 | TBD | 📋 待評估 |
| 擴展書卷覆蓋 | 10 書卷 | 8 | 🚧 進行中 |

---

## 7. Dependencies

### 7.1 External — MVP 核心

- **黃長老 (Elder Wong)** — 查經筆記與 Zoom 錄影 (用戶提供，第一手教導)
- **gty.org** — John MacArthur 講道與注釋 (核心資源)
- **G. Campbell Morgan** — *The Gospel According to John* (核心資源)
- Bible Gateway (經文查詢)
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
| 2.0 | 2025-12-28 | Claude Code | MVP focus: gty.org + Campbell Morgan, daily rhythm |
| 3.0 | 2026-01-01 | Claude Code | 擴展用戶故事 (15個)、更新進度指標、新增F6 AI戰略家 |

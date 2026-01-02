# Business Requirements Document (BRD)
## 生命之道 — 約翰福音研讀項目

**Version**: 3.0
**Date**: 2026-01-01
**Project Name**: Thursday Wong Gospel of John Study
**Document Status**: Active MVP

---

## 1. Executive Summary

本項目旨在建立一個系統化的約翰福音研讀平台，以「道」(Logos) 為主題，透過 AI 輔助工具協助信徒深入理解耶穌基督的神性與救恩信息。項目將產出高質量的中英雙語研讀材料，可作為個人靈修、小組查經或出版之用。

---

## 1.5 MVP 定義：專注約翰福音

### MVP 核心原則
**"Truly Go Deeper"** — 寧深不廣，在約翰福音一卷書中扎根

### MVP 範圍
- **唯一經卷**: 約翰福音 21 章
- **核心資源**:
  - **黃長老 (Elder Wong)** 查經筆記與 Zoom 錄影 (第一手教導)
  - **gty.org** (Grace to You - John MacArthur 講道與注釋)
  - **G. Campbell Morgan** 約翰福音注釋
- **每日節奏**: Day-to-day 靈修與研讀

### MVP 目標
| 目標 | 指標 |
|------|------|
| 每日一段落深入研讀 | 21章/3個月 = 每2-3天一章 |
| 整合 MacArthur 講道精華 | 每章至少1篇 gty.org 參考 |
| Campbell Morgan 洞見 | 每章至少1處引用 |
| 屬靈組織與架構理解 | 掌握約翰福音整體結構 |

### 為何選擇這三個資源？

**黃長老 (Elder Wong) — 第一手教導**

- 週四查經班現場教導
- Zoom 錄影存檔供回顧
- 原創筆記與大綱
- 結合華人教會處境的應用

**John MacArthur (gty.org)**

- 逐節解經、忠於原文
- 強調基督的神性與救恩教義
- 實用的生命應用
- 豐富的免費資源 (sermons, study guides, Q&A)

**G. Campbell Morgan**

- 被譽為「解經王子」(Prince of Expositors)
- 著重約翰福音的屬靈結構
- 優美的文學表達
- 深刻的靈修洞見

---

## 2. Business Objectives

### 2.1 Primary Objectives
| ID | Objective | Success Criteria |
|----|-----------|------------------|
| BO-1 | 完成約翰福音系統性研讀筆記 | 21章經文全覆蓋 |
| BO-2 | 建立標準化研讀框架 | 可複製至其他書卷 |
| BO-3 | 產出可出版級別的內容 | 通過專業校對審核 |

### 2.2 Secondary Objectives
- 建立 AI 輔助研經工作流程
- 累積歷代注疏資料庫
- 培養系統性查經習慣

---

## 3. Scope

### 3.1 In Scope
- 約翰福音 1-21 章逐章研讀
- 七個神蹟 (Signs) 深度分析
- 七個「我是」(I AM) 宣告解析
- 中英雙語對照
- 歷代注疏整合
- 希臘原文關鍵詞分析

### 3.2 Out of Scope
- 約翰書信 (Phase 2)
- 啟示錄 (Phase 3)
- 視頻/音頻製作
- 印刷出版發行

---

## 4. Stakeholders

| Role | Name/Group | Responsibility |
|------|------------|----------------|
| Project Owner | Thursday Wong Study Group | 內容方向、最終審核 |
| Content Creator | 研讀者 | 每日筆記、經文查考 |
| AI Assistant | Claude Code | 注疏、校對、格式化 |
| Reviewer | 教會牧者/神學顧問 | 神學準確性審核 |

---

## 5. Requirements

### 5.1 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | 每日研讀筆記模板 | Must Have |
| FR-2 | 聖經經文自動引用格式化 | Must Have |
| FR-3 | 歷代注疏引用系統 | Should Have |
| FR-4 | 中英對照輸出 | Should Have |
| FR-5 | 希臘原文詞彙表 | Could Have |
| FR-6 | 周報/月報自動生成 | Could Have |

### 5.2 Non-Functional Requirements

| ID | Requirement | Specification |
|----|-------------|---------------|
| NFR-1 | 聖經引文準確性 | 100% |
| NFR-2 | 注疏可查證性 | 必須標明出處 |
| NFR-3 | 語言清晰度 | 高中以上閱讀水平 |
| NFR-4 | 內容可訪問性 | Markdown 格式 |

---

## 6. Content Structure

### 6.1 核心框架：榮耀 = 恩典 + 真理

基於約翰福音 1:14 的神學洞察：

```
道成肉身
    └── 榮耀
         ├── 恩典 (Grace) → 行動 (Works) → 七個神蹟
         └── 真理 (Truth) → 話語 (Words) → 七個「我是」
```

### 6.2 七個神蹟 (Signs)

| # | Sign | Passage | Theme |
|---|------|---------|-------|
| 1 | 水變酒 | 2:1-11 | 婚姻之約，喜樂的生命 |
| 2 | 醫治大臣之子 | 4:46-54 | 家庭生活，憑話語的信心 |
| 3 | 醫治瘸腿者 | 5:1-18 | 罪與受苦的釋放 |
| 4 | 五餅二魚 | 6:1-14 | 生命的維持 |
| 5 | 海面行走 | 6:16-21 | 生命的援助 |
| 6 | 醫治生來瞎眼者 | 9:1-41 | 雙重的看見 |
| 7 | 拉撒路復活 | 11:1-44 | 救贖：死亡的勝利 |

### 6.3 七個「我是」(I AM) 宣告

1. 我是生命的糧 (6:35)
2. 我是世界的光 (8:12)
3. 我是羊的門 (10:7)
4. 我是好牧人 (10:11)
5. 我是復活，我是生命 (11:25)
6. 我是道路、真理、生命 (14:6)
7. 我是真葡萄樹 (15:1)

---

## 6.5 每日靈修節奏 (Day-to-Day Spiritual Rhythm)

### 核心理念

> "叫人活著的乃是靈，肉體是無益的。我對你們所說的話就是靈，就是生命。" (約 6:63)

每日靈修不是完成任務，而是 **領受神的啟示** (God's Revelation)，**建立屬靈組織** (Spiritual Organization)。

### 每日研讀流程

```text
📖 早晨 (45-60分鐘)
├── 1. 禱告預備 (5分鐘)
│   └── 求聖靈開啟心眼
├── 2. 經文朗讀 (10分鐘)
│   ├── 中文：和合本修訂版
│   └── 英文：ESV
├── 3. 黃長老教導 (15分鐘)
│   ├── 回顧 Zoom 錄影片段
│   └── 參考查經筆記大綱
├── 4. MacArthur 講道/注釋 (10分鐘)
│   └── gty.org 對應經文資源
├── 5. Campbell Morgan 洞見 (10分鐘)
│   └── 注意屬靈結構分析
└── 6. 筆記記錄 (5分鐘)
    └── 整合三方洞見、應用

🌙 晚間 (15分鐘)
├── 回顧當日經文
├── 反思應用
└── 禱告回應
```

### 屬靈組織架構 (Campbell Morgan's Approach)

Morgan 強調理解約翰福音的 **屬靈邏輯**:

| 部分 | 章節 | 主題 | 屬靈組織 |
|------|------|------|----------|
| 序言 | 1:1-18 | 道的本質 | 神學根基 |
| 公開事工 | 1:19-12:50 | 神蹟與講論 | 接受與拒絕的試驗 |
| 私下教導 | 13-17 | 馬可樓上 | 門徒的裝備 |
| 受難復活 | 18-21 | 榮耀的高峰 | 救贖的完成 |

### 每周整合

- **週日**: 回顧本週經文，寫周報摘要
- **反思問題**:
  1. 本週看見基督什麼屬性？
  2. 如何將「道」活出來？
  3. 下週研讀的預備心態？

---

## 7. Deliverables

### 7.1 Phase 1: Foundation ✅ COMPLETE
- [x] 項目說明文件 (CLAUDE.md)
- [x] 主題簡介 (第一課)
- [x] 約翰福音 1:1-18 (序言)
- [x] 約翰福音 1:19-51
- [x] 約翰福音 2-3 章
- [x] BRD/PRD 文檔

### 7.2 Phase 2: Core Content ✅ COMPLETE
- [x] 七個神蹟深度研讀 (Ch 2, 4, 5, 6, 9, 11)
- [x] 七個「我是」宣告分析 (Ch 6, 8, 10, 11, 14, 15)
- [x] 馬可樓上講論 (13-17章)
- [x] 公開事工 (Ch 7-12 衝突與講論)

### 7.3 Phase 3: Completion ✅ COMPLETE
- [x] 受難與復活敘事 (18-21章)
- [x] 全書總結與索引 (complete-book.md)
- [x] 出版準備 (books/bible/gospel-of-john/)

### 7.4 Phase 4: Expansion (In Progress)
- [x] 約翰書信 (1-3 John)
- [x] 路加福音 (Gospel of Luke)
- [x] 使徒行傳 (Acts)
- [x] 雅各書 (James)
- [ ] 其他書卷 (Genesis, Matthew, Revelation - 部分完成)

---

## 8. Timeline

| Phase | Content | Status |
|-------|---------|--------|
| Phase 1 | Ch 1-4 + 框架 | ✅ 完成 |
| Phase 2 | Ch 5-12 (神蹟與講論) | ✅ 完成 |
| Phase 3 | Ch 13-21 (受難復活) | ✅ 完成 |
| Phase 4 | 約翰書信 + 其他書卷 | 🚧 進行中 |

---

## 9. Authoritative Sources

### 9.1 聖經版本

- **中文主要**: 和合本修訂版 (RCUV)
- **中文參考**: 新譯本 (CNV)、呂振中譯本
- **英文主要**: ESV (English Standard Version)
- **英文參考**: NIV、NASB、NET Bible
- **希臘文**: NA28、UBS5

### 9.2 MVP 核心資源 ⭐

#### 黃長老 (Elder Wong) — 第一手教導

- **來源**: 週四查經班
- **形式**:
  - 查經筆記與大綱 (用戶提供)
  - Zoom 錄影存檔 (用戶提供)
- **特色**:
  - 華人教會處境應用
  - 現場互動教導
  - 系統性約翰福音研讀
- **使用方式**:
  - 作為研讀的主要框架
  - 結合其他資源深化理解

#### Grace to You (gty.org) — John MacArthur

- **網站**: <https://www.gty.org>
- **約翰福音講道系列**: "The Gospel According to John" (完整逐章解經)
- **Study Bible**: *The MacArthur Study Bible* 約翰福音注釋
- **使用方式**:
  - 每章研讀前先聽/讀 MacArthur 講道
  - 記錄關鍵解經洞見
  - 注意希臘原文解釋

#### G. Campbell Morgan — 解經王子

- **核心著作**: *The Gospel According to John* (1909)
- **特色**:
  - 屬靈組織 (Spiritual Organization) 分析
  - 約翰福音結構性洞見
  - 優美的靈修風格
- **使用方式**:
  - 每章研讀後閱讀 Morgan 的分析
  - 注意他如何呈現經文的屬靈邏輯
  - 學習他的 "expository method"

### 9.3 補充注釋書

- Carson, D.A. *The Gospel According to John* (PNTC)
- Morris, Leon. *The Gospel According to John* (NICNT)
- Köstenberger, Andreas. *John* (BECNT)

### 9.4 原文工具

- Logos Bible Software
- Blue Letter Bible
- Bible Gateway

---

## 10. AI Workflow

### 10.1 Available Skills

| Skill | Function | Usage |
|-------|----------|-------|
| `/master-editor` | 總編輯：分析並分類每日筆記 | 質量評估 |
| `/annotate` | 注疏師：添加歷史注疏和中英對照 | 內容豐富 |
| `/proofread` | 校對神：中英雙語潤色、邏輯檢查 | 品質把關 |
| `/publish` | 出書總管：生成周報、月報和書稿 | 輸出整合 |
| `/ai-parallels` | AI戰略家：映射至AI博弈案例 | 現代應用 |

### 10.2 Quality Standards
- 聖經引文必須 100% 準確
- 歷代注疏必須可查證
- 神學論述必須有根據
- 語言表達必須清晰

---

## 11. Risks and Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| 神學偏差 | High | 多方參考、牧者審核 |
| 引文錯誤 | High | AI 交叉驗證、人工校對 |
| 進度延遲 | Medium | 靈活調整計劃 |
| 內容過於學術 | Medium | 平衡深度與可讀性 |

---

## 12. Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Owner | | | |
| Content Lead | | | |
| Reviewer | | | |

---

**Document History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-28 | Claude Code | Initial draft |
| 2.0 | 2025-12-28 | Claude Code | MVP focus: gty.org + Campbell Morgan, 每日靈修節奏 |
| 3.0 | 2026-01-01 | Claude Code | 更新進度：Gospel of John MVP 完成，Phase 4 擴展中 |

# Business Requirements Document (BRD)
## 生命之道 — 約翰福音研讀項目

**Version**: 1.0
**Date**: 2025-12-28
**Project Name**: Thursday Wong Gospel of John Study
**Document Status**: Draft

---

## 1. Executive Summary

本項目旨在建立一個系統化的約翰福音研讀平台，以「道」(Logos) 為主題，透過 AI 輔助工具協助信徒深入理解耶穌基督的神性與救恩信息。項目將產出高質量的中英雙語研讀材料，可作為個人靈修、小組查經或出版之用。

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

## 7. Deliverables

### 7.1 Phase 1: Foundation ✅ COMPLETED
- [x] 項目說明文件 (CLAUDE.md)
- [x] 主題簡介 (第一課)
- [x] 約翰福音 1:1-18 (序言)
- [x] 約翰福音 1:19-51
- [x] 約翰福音 2-3 章
- [x] BRD/PRD 文檔

### 7.2 Phase 2: Core Content ✅ COMPLETED
- [x] 七個神蹟深度研讀
- [x] 七個「我是」宣告分析
- [x] 馬可樓上講論 (13-17章)
- [x] 21 章研讀筆記 (`docs/study-notes/`)

### 7.3 Phase 3: Completion ✅ COMPLETED
- [x] 受難與復活敘事 (18-21章)
- [x] 全書總結與索引
- [x] Billy Graham 風格講道系列 (`docs/sermons/`) — 10篇

### 7.4 講道系列詳情

| # | 講題 | 經文 | 檔案 |
|---|------|------|------|
| 1 | 神愛世人 | 約 3:16 | `01-god-so-loved.md` |
| 2 | 你必須重生 | 約 3:1-7 | `02-you-must-be-born-again.md` |
| 3 | 活水的邀請 | 約 4:13-14 | `03-living-water.md` |
| 4 | 世界的光 | 約 8:12 | `04-light-of-the-world.md` |
| 5 | 生命的糧 | 約 6:35 | `05-bread-of-life.md` |
| 6 | 好牧人 | 約 10:11, 14 | `06-good-shepherd.md` |
| 7 | 復活與生命 | 約 11:25-26 | `07-resurrection-and-life.md` |
| 8 | 唯一的道路 | 約 14:6 | `08-the-only-way.md` |
| 9 | 常在基督裡 | 約 15:4-5 | `09-abiding-in-christ.md` |
| 10 | 十字架的愛 | 約 19:30 | `10-love-of-the-cross.md` |

---

## 8. Timeline

| Phase | Content | Status |
|-------|---------|--------|
| Phase 1 | Ch 1-4 + 框架 | ✅ 完成 |
| Phase 2 | Ch 5-12 (神蹟與講論) | ✅ 完成 |
| Phase 3 | Ch 13-21 (受難復活) | ✅ 完成 |
| Phase 4 | Billy Graham 講道系列 | ✅ 完成 (2025-01-04)

---

## 9. Authoritative Sources

### 9.1 聖經版本
- **中文主要**: 和合本修訂版 (RCUV)
- **中文參考**: 新譯本 (CNV)、呂振中譯本
- **英文主要**: ESV (English Standard Version)
- **英文參考**: NIV、NASB、NET Bible
- **希臘文**: NA28、UBS5

### 9.2 注釋書
- Carson, D.A. *The Gospel According to John* (PNTC)
- Morris, Leon. *The Gospel According to John* (NICNT)
- Köstenberger, Andreas. *John* (BECNT)

### 9.3 原文工具
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
| 1.1 | 2025-01-04 | Claude Code | Phase 1-3 completed, added sermon series |

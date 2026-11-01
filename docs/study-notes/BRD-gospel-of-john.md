# Business Requirements Document (BRD)
## 生命之道 — 從約翰福音到全本聖經研讀書庫

**Version**: 4.0
**Date**: 2026-10-31
**Project Name**: 三書精讀出版系統 · 聖經研讀書庫 (Bible Study Library)
**Document Status**: Active. MVP（約翰福音）已完成；系統已擴展為全本聖經書庫
**Companion documents**: `PRD-gospel-of-john.md`（使用者故事）、`../system-evaluation-2026-10-31.md`（系統評估與升級計劃）

> v4.0 的主要改動：本文件寫於 v3.0（2026-01）時，範圍仍是「約翰福音一卷」。到 2026-10，系統實際已產出 60 餘冊可建置的研讀書 PDF，經文版本、章節體例、驗證工具、品質評分都已改變。v4.0 把文件改成符合現況，並把尚未達成的需求列明，不寫成已完成。

---

## 1. Executive Summary

本項目以約翰福音為起點，建立一套 AI 輔助、可重複的聖經研讀書製作系統：每卷書有固定的章節體例、雙語經文（和合本 CUV + NASB 1995）、可查證的歷代注疏，以及一條貫穿全書的「骨幹」（神啟示的次序）。

截至 2026-10-31：

| 指標 | 現況 | 證據 |
|------|------|------|
| 有建置基準的書冊 | 65 冊 | `.claude/skills/eat-bible/baselines.tsv` |
| 骨幹檢查 4/4 通過的書目錄 | 49 個 | `scripts/check-book-spine.py`（2026-10-31 全庫執行） |
| 有評分表的書 | 約 50 卷 | `docs/scores/`（88 份） |
| 缺字 (missing glyphs) | 65 冊全部為 0 | baselines.tsv |
| 仍有溢出 (overfull boxes) | 9 冊 | genesis 138、ephesians 64、judges 48、ezekiel 32、exodus 24、1-samuel 22、proverb 8、joel 4、pastoral-epistles 4 |
| 讀者可取得的發佈版本 | 66 卷正典＋主題／替代版本，共 74 個 PDF | 2026-10-31 上線於 ai-eden.com `/resources`（ai-eden commit `729f36fa`）；須登入，但 PDF 本身在 storage.googleapis.com 公開可下載 |
| 人工（牧者）神學審核 | 未進行 | 所有評分皆為 AI 自評或 AI 獨立校對 |

這個專案的強項是書的內容與驗證紀律。弱項在書以外的部分：書目要從 pubhub 手動搬到 ai-eden（無清單、無完整性測試），讀經器沒有連到研讀書，每日靈修流程停擺，pubhub 自己的 `app/` 仍是約翰福音 MVP 的佔位頁。讀者端的整體評估見 ai-eden 的 `Docs/system-evaluation-2026-10-31.md`。

---

## 2. MVP 回顧：約翰福音（已完成）

### 2.1 MVP 原則（保留）

**"Truly Go Deeper"** — 寧深不廣。約翰福音一卷書建立的體例，已成為全書庫的標準（`gospel-of-john` 是範本書）。

### 2.2 MVP 目標達成情況

| 目標 | v3.0 指標 | 結果 |
|------|-----------|------|
| 21 章全覆蓋 | 100% | ✅ 完成（23 單元，含序言與骨幹章） |
| MacArthur 講道 | 每章 ≥1 篇 gty.org | ✅ 講道編號已逐條核對 |
| Campbell Morgan 洞見 | 每章 ≥1 處 | ✅ 15 條引文逐字核對 |
| 掌握全書結構 | 屬靈組織 | ✅ 骨幹章 `00a-revelation-order.md`，骨幹檢查 4/4 |
| 出版級成品 | 通過專業校對 | 🟡 AI 校對已完成（評分 9.6）；人工審核未做 |

### 2.3 約翰福音內容框架（保留）

```
道成肉身 (約 1:14)
    └── 榮耀
         ├── 恩典 → 行動 → 七個神蹟
         └── 真理 → 話語 → 七個「我是」
```

七個神蹟：水變酒 (2:1-11)、醫大臣之子 (4:46-54)、醫瘸腿者 (5:1-18)、五餅二魚 (6:1-14)、海面行走 (6:16-21)、醫生來瞎眼者 (9:1-41)、拉撒路復活 (11:1-44)。

七個「我是」：生命的糧 (6:35)、世界的光 (8:12)、羊的門 (10:7)、好牧人 (10:11)、復活和生命 (11:25)、道路真理生命 (14:6)、真葡萄樹 (15:1)。

---

## 3. Business Objectives

### 3.1 Primary Objectives

| ID | Objective | Success Criteria | 狀態 |
|----|-----------|------------------|------|
| BO-1 | 完成約翰福音系統性研讀 | 21 章全覆蓋 | ✅ |
| BO-2 | 建立可複製的研讀框架 | 其他書卷沿用同一體例 | ✅ 11 節章節模板 + 骨幹 + 評分表，已套用 49 卷 |
| BO-3 | 產出可出版級內容 | 通過專業校對審核 | 🟡 AI 層面已達成；缺人工神學審核 |
| BO-4 *(新)* | 全本聖經 66 卷書庫 | 每卷達到「骨幹」成熟度（第 5 階） | 🟡 約 49/66；撒母耳記上下、彼得前後書、希伯來書、以賽亞書、保羅書信多卷未達標 |
| BO-5 *(新)* | 讀者能取得、閱讀、分享 | 書目頁、可下載版本、手機可讀 | 🟡 已在 ai-eden.com 上線（須登入、PDF 檢視器）；手機友善的 HTML 章節與「研讀本章」連結未做 |
| BO-6 *(新)* | 服事教會查經 | 小組帶領者可直接使用的材料 | 🟡 書中有「老弟兄查經」與默想問題，但沒有帶領者版本 |

### 3.2 Secondary Objectives

- AI 輔助研經工作流程 — ✅ 已成形（`eat-bible`、`ask-elder-wong` 技能與 14 支驗證腳本）
- 歷代注疏資料庫 — ✅ 各書 `sources/` 存公有領域原文（Calvin、Henry、Morgan、教父等），供機器逐字核對
- 系統性查經習慣（每日靈修） — ❌ 每日筆記 2026-08 後僅 2 篇；週報停在 2026-W08

---

## 4. Scope

### 4.1 In Scope（v4.0）

- 舊約 39 卷、新約 27 卷研讀書（PDF，A5/書冊版面）
- 每卷：骨幹章、分卷扉頁、11 節章節模板、索引、引用出處總表
- 經文：中文和合本 (CUV) 為底本；英文 NASB 1995
- 注疏：MacArthur (gty.org)、G. Campbell Morgan，以及公有領域注疏家（Calvin、Matthew Henry、教父等）
- 品質：機器驗證 + AI 獨立校對 + 十項評分表
- *(新)* 書庫發佈：書目、下載、版本
- *(新)* 小組查經帶領者材料
- 每日靈修筆記與週報（恢復運作）

### 4.2 Out of Scope

- 視頻／音頻製作
- 實體印刷發行（PDF 須達印刷品質，但不負責印刷通路）
- 孫子兵法、資治通鑑（屬於三書計劃，但不在本 BRD 範圍）
- 版權詩歌歌詞（只用公有領域聖詩；版權歌詞也會觸發內容過濾）

---

## 5. Stakeholders

| Role | Name/Group | Responsibility |
|------|------------|----------------|
| Project Owner / Editor-in-chief | Jim Xiao | 方向、最終決定、提交 |
| Teaching source | 黃長老 / 週四查經班；書中以「老弟兄」呈現 | 查經風格與教導 |
| Church partner | CCIC Sunnyvale（哥林多後書 24 課，2026-03~08） | 課程使用者 |
| AI production team | Claude Code（eat-bible、ask-elder-wong、五個編輯 agent） | 建卷、校對、驗證、評分 |
| Theological reviewer | 教會牧者／神學顧問 | **尚未指派**，是 BO-3 的阻礙 |
| Readers | 個人讀者、小組帶領者、主日學老師 | **尚無取得管道** |

---

## 6. Requirements

### 6.1 Functional Requirements

| ID | Requirement | Priority | 狀態 |
|----|-------------|----------|------|
| FR-1 | 每日研讀筆記模板 | Must | 🔴 `pnpm new-note` 崩潰（`require` 在 ESM 中不可用） |
| FR-2 | 經文引用格式化與核對 | Must | ✅ `lint-scripture-text.py`、`check-prose-scripture-quotes.py`、`verify-prose-citations.py` |
| FR-3 | 注疏引用系統 | Must | ✅ 引文帳目 + `verify-citations.py` / `verify-sermon-quotes.py` / `check-citation-ledger.py` |
| FR-4 | 中英對照輸出 | Must | ✅ CUV + NASB 1995 並列 |
| FR-5 | 原文詞彙 | Should | ✅ 每章「原文研讀」表；希伯來文 NFD 檢查 |
| FR-6 | 週報／月報自動生成 | Could | 🔴 GitHub Action 最近 40 次全部失敗 |
| FR-7 *(新)* | 一鍵建書 | Must | 🟡 可行，但 104 支各書專屬 build script 各自複製 |
| FR-8 *(新)* | 書的骨幹檢查 | Must | ✅ `check-book-spine.py`（巢狀目錄與無 build script 的書看不到） |
| FR-9 *(新)* | 品質評分與成熟度階梯 | Must | ✅ 十項評分表，`docs/scores/` |
| FR-10 *(新)* | 書庫狀態總表 | Should | ❌ 無；狀態分散在 baselines、scores、記憶檔 |
| FR-11 *(新)* | 讀者書目與下載 | Must | 🟡 ai-eden.com `/resources`；書目 `lib/bible-study-library.ts` 手動維護，須改由 pubhub 產生清單（ai-eden US-32.4） |
| FR-12 *(新)* | 手機友善閱讀（HTML 或 EPUB） | Should | ❌ |
| FR-13 *(新)* | 小組帶領者版本 | Should | ❌ |
| FR-14 *(新)* | 勘誤與版本號 | Should | ❌ |

### 6.2 Non-Functional Requirements

| ID | Requirement | Specification | 狀態 |
|----|-------------|---------------|------|
| NFR-1 | 經文準確性 | 100%，雙來源逐節核對 | 🟡 機器可查的面已核；仍有檢查器看不到的面（見評估報告） |
| NFR-2 | 注疏可查證 | 有引號就必須能定位原文 | ✅ 規則已立；已逐卷執行 |
| NFR-3 | 不杜撰 | 不杜撰經文、注疏、黃長老語錄、數字 | ✅ 規則；校對輪仍會抓到違例 |
| NFR-4 | 排版 | 0 缺字、0 溢出 | 🟡 缺字全清；9 冊仍有溢出 |
| NFR-5 *(新)* | 評分誠實 | 評分表列出「仍未完成」；外部覆核 | 🟡 自評偏高：外部覆核後申命記 9.7→9.2，約伯記用出版社標準時 9.8→7.0 |
| NFR-6 *(新)* | 安全 | 不公開可寫入的儲存空間 | ⚠️ `app/storage` 在前端直接上傳／刪除，須確認 Firebase 規則 |
| NFR-7 *(新)* | 可維護 | 修一次 bug，全書庫生效 | 🔴 同一類 bug 已在不同書重複出現三次（`printf %s→%b`、`\@schapter` 頁眉、secnumdepth） |

---

## 7. Content Standard（全書庫統一，取代 v3.0 的版本設定）

| 項目 | 標準 |
|------|------|
| 中文經文 | 和合本 (CUV)，以 ai-eden.com 為準；cnbible / fhl 抓取核對 |
| 英文經文 | NASB 1995（biblehub 的 chapter 頁才是 1995 版） |
| 用字 | 裏／甚麼；和合本譯名；間隔號「·」 |
| 章節模板 | 11 節：基督焦點、配詩、經文、背景、原文研讀、領受要點、歷代注疏、詩篇與聖詩、老弟兄查經、生命應用、與其他經文的關聯 |
| 骨幹 | 骨幹章 + 分卷扉頁骨幹標記 + 各章座標行 + 章末回到基督 |
| 詩歌 | 只用公有領域聖詩 |

> **已知不一致**：`CLAUDE.md` 與 `.claude/CONTENT_RULES.md` 仍寫「RCUV + ESV」為主要版本，與上表不符。以本表為準，並在升級計劃第 0 階段修正。

---

## 8. Deliverables & Phases

| Phase | 內容 | 狀態 |
|-------|------|------|
| 1-3 | 約翰福音 MVP | ✅ 2026-01 |
| 4 | 新約擴展（路加、行傳、書信、啟示錄） | ✅ 大部分；彼得前後書、希伯來書、保羅書信多卷未到骨幹階 |
| 5 | 舊約建卷（創世記至瑪拉基書） | ✅ 大部分；撒母耳記上下未到標準 |
| 6 *(新)* | 系統升級：統一建置、品質閘、讀者發佈、靈修流程 | 📋 見 `docs/system-evaluation-2026-10-31.md` |

---

## 9. Risks and Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| 神學偏差，且無人工審核 | High | 第 3 階段指派牧者審核，先從約翰福音與兩卷試點書開始 |
| AI 自評分數偏高 | High | 評分一律由另一個代理覆核；分數旁註明「AI 評分」 |
| 檢查器看不到的缺陷（校對輪一再抓到） | High | 每卷保留人工式通讀校對；新缺陷類型寫成腳本 |
| 複製貼上的建置腳本重複出錯 | Medium | 共用建置函式庫（第 2 階段） |
| 書目與實際檔案不一致 | Medium | pubhub 產生 `library-manifest.json`，ai-eden 以 CI 驗證（第 4 階段） |
| 並行 session 互相覆寫 | Medium | 提交前 `git status` 與 `git diff --cached --stat` |
| 版權詩歌觸發內容過濾 | Low | 只用公有領域聖詩 |

---

## 10. Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Owner | Jim Xiao | | |
| Theological Reviewer | （待指派） | | |

---

**Document History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-28 | Claude Code | Initial draft |
| 2.0 | 2025-12-28 | Claude Code | MVP focus: gty.org + Campbell Morgan, 每日靈修節奏 |
| 3.0 | 2026-01-01 | Claude Code | Gospel of John MVP 完成，Phase 4 擴展中 |
| 4.0 | 2026-10-31 | Claude Code | 範圍改為全本聖經書庫；經文改 CUV + NASB 1995；新增 BO-4~6、FR-7~14、NFR-5~7；以實測數字標示狀態 |

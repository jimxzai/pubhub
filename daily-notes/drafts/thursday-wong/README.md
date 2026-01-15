# 約翰福音研讀項目

**Gospel of John Study Project**

---

## 項目概述

本項目是約翰福音全書的系統性研讀，以「榮耀 = 恩典 + 真理」(約 1:14) 為核心神學框架，深入分析七個神蹟與七個「我是」宣告。

### 核心框架

```
榮耀 = 恩典 + 真理

├── 恩典 (Grace) → 七個神蹟 (σημεῖον)
├── 真理 (Truth) → 七個「我是」(ἐγώ εἰμι)
└── 榮耀 (Glory) → 十字架與復活 (δόξα)
```

---

## 項目結構

```
thursday-wong/
│
├── CLAUDE.md                    # Claude Code 項目配置
├── README.md                    # 本文件
├── Gospel of John.md            # 原始研讀筆記
│
├── .claude/                     # Claude Code 配置
│   ├── settings.json
│   ├── README.md
│   └── commands/
│       ├── master-editor.md     # 總編輯 Agent
│       ├── annotate.md          # 注疏師 Agent
│       ├── proofread.md         # 校對神 Agent
│       └── publish.md           # 出書總管 Agent
│
├── 研讀筆記/
│   ├── John-2-3-Study.md        # 約翰福音 2-3 章
│   ├── John-4-5-Study.md        # 約翰福音 4-5 章
│   ├── John-6-7-Study.md        # 約翰福音 6-7 章
│   ├── John-8-10-Study.md       # 約翰福音 8-10 章
│   ├── John-11-12-Study.md      # 約翰福音 11-12 章
│   ├── John-13-17-Study.md      # 約翰福音 13-17 章
│   └── John-18-21-Study.md      # 約翰福音 18-21 章
│
├── reports/                     # 報告輸出
│   ├── FINAL-weekly-summary.md  # 周報 (~2,000 字)
│   ├── FINAL-monthly-report.md  # 月報 (~4,500 字)
│   └── FINAL-complete-report.md # 完整報告
│
└── book/                        # 書稿
    ├── 00-table-of-contents.md  # 目錄
    ├── 00-preface.md            # 序言
    ├── chapter-01-logos.md      # 第一章：太初有道
    ├── chapter-02-seven-signs.md    # 第二章：七個神蹟
    ├── chapter-03-seven-i-am.md     # 第三章：七個「我是」
    ├── chapter-04-farewell-discourse.md  # 第四章：臨別講論
    ├── chapter-05-passion-resurrection.md # 第五章：受難與復活
    ├── chapter-FINAL-complete.md    # 完整導讀
    ├── appendix-01-greek-vocabulary.md  # 附錄一：希臘文詞彙
    ├── appendix-02-structure-charts.md  # 附錄二：結構圖表
    └── appendix-03-commentary-excerpts.md # 附錄三：歷代註釋
```

---

## 內容統計

| 類別 | 檔案數 | 字數 |
|------|--------|------|
| 研讀筆記 | 7 | ~15,000 字 |
| 報告 | 3 | ~8,000 字 |
| 書稿正文 | 6 | ~28,000 字 |
| 前言與目錄 | 2 | ~2,500 字 |
| 附錄 | 3 | ~7,000 字 |
| **總計** | **21** | **~60,000 字** |

---

## 七個神蹟一覽

| # | 神蹟 | 經文 | 恩典主題 |
|---|------|------|----------|
| 1 | 水變酒 | 2:1-11 | 喜樂的生命 |
| 2 | 醫治大臣之子 | 4:46-54 | 話語的信心 |
| 3 | 醫治畢士大癱子 | 5:1-18 | 罪的釋放 |
| 4 | 五餅二魚 | 6:1-14 | 生命的維持 |
| 5 | 海面行走 | 6:16-21 | 患難中的同在 |
| 6 | 醫治生來瞎眼者 | 9:1-41 | 屬靈的光照 |
| 7 | 拉撒路復活 | 11:1-44 | 勝過死亡 |

---

## 七個「我是」宣告

| # | 宣告 | 經文 | 供應 |
|---|------|------|------|
| 1 | 生命的糧 | 6:35 | 飢餓的滿足 |
| 2 | 世界的光 | 8:12 | 黑暗的照亮 |
| 3 | 羊的門 | 10:7,9 | 進入的道路 |
| 4 | 好牧人 | 10:11,14 | 生命的保護 |
| 5 | 復活和生命 | 11:25 | 死亡的勝利 |
| 6 | 道路真理生命 | 14:6 | 到父的途徑 |
| 7 | 真葡萄樹 | 15:1 | 結果的能力 |

---

## Claude Code 指令

本項目配置了以下 Claude Code slash commands：

| 指令 | 功能 |
|------|------|
| `/master-editor` | 分析並分類每日筆記 |
| `/annotate` | 添加歷史注疏和中英對照 |
| `/proofread` | 中英雙語潤色、邏輯檢查、引文核對 |
| `/publish` | 生成周報、月報和書稿章節 |

### 使用 `/publish` 指令

```
/publish

選擇輸出模式：
1. 周報 (Weekly Summary) - 1000-2000 字
2. 月報 (Monthly Report) - 3000-5000 字
3. 書稿章節 (Book Chapter) - 5000-10000 字

輸入 "all" 生成所有三種模式
```

---

## 參考資源

### 主要參考註釋
- D.A. Carson, *The Gospel According to John* (PNTC)
- Leon Morris, *The Gospel According to John* (NICNT)
- Raymond Brown, *The Gospel According to John* (Anchor Bible)

### 教父著作
- Augustine, *Tractates on the Gospel of John*
- Chrysostom, *Homilies on the Gospel of John*
- Origen, *Commentary on the Gospel of John*

---

## 項目時間線

- **2025年12月**：項目啟動
- 完成約翰福音 1-21 章研讀筆記
- 完成三種報告模式
- 完成書稿全部章節與附錄

---

## 授權

本項目內容供個人研讀與教會使用。

---

*由 Claude Code 協助生成*
*2025年12月*

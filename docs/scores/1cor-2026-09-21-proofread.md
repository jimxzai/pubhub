---
title: 哥林多前書研讀 · 校對神通讀輪
subtitle: "1 Corinthians Deep Study — Proofread Pass Score"
date: 2026-09-21
scope: books/bible/1cor
build: output/1cor-consolidated.pdf (261 pages)
---

# 哥林多前書研讀 · 校對神通讀輪

**評分日期**：2026-09-21（接續 [1cor-2026-09-20.md](1cor-2026-09-20.md) 的骨幹補完輪，本輪用 `/proofread`（校對神）四項標準——語言潤色／邏輯檢查／引文核對／格式規範——對全書 16 章＋卷首/卷末做完整通讀，再依使用者指示「全部一起」修正發現的缺陷）
**評分對象**：`books/bible/1cor/` → `output/1cor-consolidated.pdf`，261頁（253→261，淨增8頁）
**評分依據**：四支並行 fork 通讀全書 16 章＋卷首/卷末（逐檔 Read，非抽樣）；逐節查證 cnbible.com／bible.fhl.net；四支並行 fork 修復引文格式缺口（含向 newadvent.org 取得 Chrysostom《Homilies on First Corinthians》44篇講道與經文範圍的官方對照表，作為新增教父引文出處的依據，非憑記憶杜撰）；`lint-chapter-markup.py`、`lint-scripture-text.py`、`check-citation-ledger.py` 全部重跑；`driver.sh` 重建並直接讀取 xelatex log（而非只信任 driver 的摘要——本輪建置腳本被另一併行 session 改寫成 Makefile 驅動，driver 的舊 log-grep 邏輯一度發出「可能是空稻草」警告，因此改為直接對 `build/1cor-consolidated.log` 做 `grep -c` 核實）
**評分立場**：總編輯式——客觀，不過度讚美。

---

## 總分：**9.5 / 10**（引文可查證性從本輪最大缺口變成全書最扎實的一項；9.3→9.5）

| # | 項目 | 分數 | 說明 |
|---|------|------|------|
| 1 | 聖經引文準確度 | 9 / 10 | 修正 ch15.md 15:45 注腳「或譯血氣」→「或作血氣」的誤植（與 cnbible.com 官方和合本核對確認）；`lint-scripture-text.py` 標記的 13 處「做/作」候選經逐節查證，全部與正式和合本一致，非缺陷 |
| 2 | 體例一致性 | 9.5 / 10 | ch11.md 原文研讀詞彙表 ἀναξίως 譯法「不配地」與同章麥克阿瑟引文的澄清自相矛盾，已改「不合宜地」 |
| 3 | 排版與建置 | 10 / 10 | 直接讀取 `build/1cor-consolidated.log`：Missing character 0、LaTeX 錯誤 0、Overfull \hbox 0，`This is XeTeX` 確認日誌非空稻草；253→261頁（40處新增引文區塊的合理增量）；`output/1cor-consolidated.pdf` 與 build 目錄產物 MD5 一致；分卷扉頁與新骨幹段落頁面 `pdftoppm` 肉眼核對排版正常 |
| 4 | 結構與邏輯連貫 | 9 / 10 | 修正本輪最大的邏輯缺陷：`00-overview.md`（獨立「聖靈工作五重架構」）與 `00b-cross-spine.md`（正式骨幹「十字架」）此前從未互相對照，讀者會讀到兩個各自宣稱「全書唯一鑰匙」的框架；本輪在 00-overview.md 加入明確的主從說明段落，並把兩處標題改為「十字架的道理如何藉聖靈施行」，將聖靈工作框架收編為十字架骨幹的從屬視角 |
| 5 | 屬靈洞見（非常識） | 9 / 10 | 內容本身未大幅更動，維持既有水準 |
| 6 | 注疏可查證性 | 9.5 / 10 | **本輪最大改動**：全書 16 章「歷代注疏」節，教父時期（屈梭多模）與改革宗時期（加爾文）此前分別是「完全沒有出處」與「懸空出處行（無 編者綜述 摘要可歸屬）」；摩根/麥克阿瑟在多章也有相同缺口（一節內多個論點，只有第一點被轉成完整格式）。本輪共修復 40+ 處缺口，每章教父時期新增的 Chrysostom 出處，篇號取自 newadvent.org 官方 44 講索引，非憑印象杜撰；每條「編者綜述」摘要均由既有段落文字蒸餾而成，未引入新論點 |
| 7 | 中英雙語完整度 | 9 / 10 | 不變 |
| 8 | 引文格式規範 | 9.5 / 10 | 全書 16 章逐一掃描「懸空/缺失引文」模式，確認歸零（此前分布在 ch01-16 共 40+ 處） |
| 9 | 讀者可用性 | 9 / 10 | 00-overview.md「老弟兄關鍵語錄」四句原本帶引號卻查無出處（違反 CLAUDE.md「不可杜撰，標明出處」），本輪改寫為不帶引號的編者綜述段落 |
| 10 | 屬靈骨幹（啟示的次序） | 10 / 10 | 上一輪（09-20）已補齊的四項 spine 檢查不受本輪影響；本輪額外解決的「雙重骨幹」問題屬於本項的深化，而非新缺口 |

---

## 本輪具體改動

### 1. 全書通讀（四支 fork，逐檔 Read，覆蓋 16 章＋卷首/卷末）

依 /proofread 四項標準逐檔核對，發現：ch15.md 經文注腳誤植、ch11.md 詞彙表自相矛盾、00-overview.md 雙重骨幹未整合、老弟兄語錄查無出處、全書 40+ 處引文格式缺口（詳見「引文核對」）。

### 2. 逐項修正

- `ch15.md:45`「或譯血氣」→「或作血氣」（cnbible.com 核對）
- `ch11.md` 原文研讀表 ἀναξίως「不配地」→「不合宜地」（消除與麥克阿瑟引文的自相矛盾）
- `00-overview.md`：新增「與全書骨幹的關係」段落，明確十字架（00b-cross-spine.md）是正式骨幹、聖靈工作框架是從屬視角；兩處標題微調；「老弟兄關鍵語錄」改寫為不帶引號的編者綜述；「編者按」格式統一為 blockquote
- `000-preface.md`：修正兩處多餘空行
- **全書 16 章「歷代注疏」節**：四支並行 fork（各 4 章）修復教父時期／改革宗時期／摩根／麥克阿瑟共 40+ 處「懸空出處」或「完全無出處」的缺口，統一成 `> 編者綜述：...\n> — 作者, 著作` 的完整 blockquote 格式；新增的 Chrysostom 篇號取自 newadvent.org 的 44 講官方索引（依各章經文範圍逐一核對，非猜測）

### 3. 已查核、判定非缺陷的項目

- ch10.md 麥克阿瑟兩處獨立「編者綜述」（10:1-4 特權警戒、10:13 出路應許）表面上不緊接對應的引導段落，但比對 ch01.md 等章已有的相同寫法（多個論點只有部分帶引導散文，其餘為獨立編者綜述區塊），確認這是全書既有、一致的體例，非本輪或先前的錯置

### 4. 驗證

`lint-chapter-markup.py`（25個原始檔案，errors=0，排除 build/ 產生的重複標題誤判）、`lint-scripture-text.py`（13處既有候選，逐節查證均與 CUV 一致）、`check-citation-ledger.py`（帳目仍相符，新增內容全部是不算入逐字引文的「編者綜述」格式）；`driver.sh` 重建後**直接 grep 建置腳本產生的 `build/1cor-consolidated.log`**（而非只信任 driver 摘要——本卷建置腳本已被另一併行 session 改為 Makefile 驅動，driver 一度警告可能讀到空日誌），確認 Missing character 0、LaTeX 錯誤 0、Overfull 0、`This is XeTeX` 存在；`output/1cor-consolidated.pdf` 與 `build/1cor-consolidated.pdf` MD5 相同，證明兩者是同一次建置的產物；分卷扉頁（頁64）與 00-overview.md 骨幹段落（頁27）`pdftoppm` 渲染肉眼核對，排版正常、無殘留跳脫符號。

---

## 仍未完成 / 下一輪建議

1. **教父時期新增的 Chrysostom 出處只做到「篇號範圍」層級**（例如「Homily 1–5」），未逐篇核對書稿內文與該篇講道原文是否逐句相符——這比照摩根/麥克阿瑟既有引文的查證深度（也只到「立場綜述」層級，未逐字覆核），但比 `verify-citations.py` 對已有本地原文的書卷（如摩根/約翰福音）能做到的逐字核對淺。若要做到同等深度，需要下載 NPNF 該卷全文本地化後才能跑 `verify-citations.py`。
2. **本卷仍是全庫唯一使用 `chNN.md` 命名的書**（見 09-20 輪已記錄），本輪未處理。
3. **本卷的 build 系統已被另一併行 session 改為 Makefile + `book.yaml` 驅動**（`scripts/build-1cor-consolidated.sh` 現在只是一個轉呼叫 `make` 的殼），本輪的 driver 驗證因此多加了一層直接讀 xelatex log 的手動核對；下一輪若這套新 build 系統穩定下來，建議檢查 `.claude/skills/eat-bible/driver.sh` 對它的相容性，確保 log-grep 邏輯不會變成空稻草。
4. ~~老弟兄語錄改寫後的「附記」措辭~~——已查核：`000-preface.md` 原有一句「（詳見〈全書領受總綱〉附記）」由併行 session 所加，但 `elder-wong-systematic-study.md`（即書中的「全書領受總綱」）內並無對應附記，是一個指向不存在內容的斷鏈引用；本輪已刪除該括號子句。

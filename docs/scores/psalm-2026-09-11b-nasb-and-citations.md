---
title: 詩篇研讀 · 出版品質評分（第二輪：中英雙語補齊與引文覆核）
subtitle: "Psalms Deep Study — Editorial Quality Score, Round 2 (NASB Bilingual Completion & Citation Re-verification)"
date: 2026-09-11
scope: books/bible/psalm
build: output/psalm-consolidated.pdf (110 pages) · output/psalm-liturgical-consolidated.pdf (339 pages, 原 305 頁)
---

# 詩篇研讀 · 出版品質評分（第二輪：中英雙語補齊與引文覆核）

**評分日期**：2026-09-11（同日第二輪，接續 `docs/scores/psalm-2026-09-11.md`）
**這一輪的來由**：第一輪評分表誠實列出兩項最大缺口——(1) 五冊逐篇領受（06-10，147篇個別詩篇，全書內容主體）沒有英文對照；(2) 摩根與麥克阿瑟引文本輪未重新機器核對。作者要求針對這兩項「fix and upgrade and optimize it to closer to 10」。本輪逐一處理。

---

## 總分：**9.1 / 10**（第一輪 8.3 → 本輪 9.1）

| # | 項目 | 第一輪 | 本輪 | 說明 |
|---|---|---|---|---|
| 1 | 聖經引文準確度 | 8.5 | 8.5 | 未變動 |
| 2 | 體例一致性 | 8.0 | 8.5 | 06-10 現在與 00-overview／01-05 使用同一套「CUV/NASB 核心經文方框」體例，全書英文對照格式統一 |
| 3 | 排版與建置 | 9.5 | 9.5 | 兩版重建仍 0 missing glyph、0 overfull；liturgical 版 305→339 頁（147 個新方框），已記錄新基準線 |
| 4 | 結構與邏輯連貫 | 8.5 | 8.5 | 未變動 |
| 5 | 屬靈洞見（非常識） | 9.0 | 9.0 | 未變動 |
| 6 | 注疏可查證性 | 7.5 | **9.0** | 摩根《話中之光》七則、MacArthur 導論一則，本輪皆以 `curl` 取得原始 HTML 逐字核對（非 AI 摘要），全數逐字相符；唯一一則未能逐字核對的摩根《默想詩篇》導論引文，由「加引號的引文」誠實降級為「不加引號的撮述」——寧可少宣稱，不可假宣稱 |
| 7 | 中英雙語完整度 | 5.0 | **8.5** | 06-10 全數147篇個別詩篇領受，逐篇補上 CUV/NASB1995 核心經文方框（與01-05既有體例一致，每篇一則錨點經文，非逐句全譯）；00-overview／01-05 原有的 ESV 對照全數換成 NASB 1995，與全書英文版本統一 |
| 8 | 引文格式規範 | 8.0 | 8.3 | MacArthur 導論引文改為房規「英文在前、中文在後」雙行體例（原為中文夾註英文的舊式） |
| 9 | 讀者可用性 | 7.5 | 7.5 | 未變動（見下方「仍未完成」第3項） |
| 10 | 屬靈骨幹（啟示的次序） | 10 | 10 | `check-book-spine.py` 仍 4/4；147 處新增內容未擾動既有座標／回到基督標記 |

---

## 這一輪做了甚麼

**1.（最大工程）06-10 全數147篇個別詩篇補上 CUV/NASB1995 核心經文方框。** 五支平行 agent 各負責一冊（39/30/17/17/44篇），逐篇：
   - 從該篇既有內容（精義一句話／背景與聖靈的編排／黃長老這樣帶你讀）判斷錨點經文，中文一律**複製既有已核對文字**、不重新輸入；
   - 逐章向 `biblehub.com/nasb/psalms/` 或 `ai-eden.com`（第一冊改用此更符合專案標準的來源，並交叉核對 biblehub）取得 NASB 1995 原文，以內容特徵（而非網址）確認版次；
   - 供給字斜體化（`*word*`）、舊約引文全大寫等房規細節逐一落實。

   事後機器抽驗：147個方框與147個標題一一對應（無錯位、無重複）、經文出處欄中英一致、格式零缺陷；另抽驗5節（詩16:10、59:9、71:18、93:4、99:4）直接對照 biblehub 原始頁面，逐字相符——其中詩59:9的「his strength」（NASB，第三人稱）與和合本「我的力量啊」（第一人稱）是已知的經文傳統（Ketiv/Qere）分歧，非誤譯，agent 正確地兩存而未強行統一。

   **一篇例外**：詩87（08-guide-book-three.md）因原文只以片段散落在各段落、無法在不臆造的情況下組出完整經文，agent 正確地拒絕捏造並跳過；本人隨後另行以 `curl` 向 cnbible.com 取得 87:4-6 完整經文、biblehub 取得對應 NASB，補上該篇方框。

**2. 摩根與麥克阿瑟引文重新機器核對（非 AI 摘要）。** 記取本項目既有教訓（WebFetch 摘要可能悄悄改寫經文），改用 `curl` 直接取得 `biblenotes.online/resources/searchlights/psalms.htm` 原始 HTML、`blueletterbible.org` MacArthur 導論原始 HTML，去標籤後逐句比對：
   - 摩根《話中之光》詩1、2、22、23、24、42、51 共七則短評，**全數逐字相符**（含此前未曾逐字覆核過的詩1「The man delighting in that law...is the man who is prosperous」、詩2「the comfort of all those who love righteousness」等）。
   - MacArthur 詩篇導論五句引文（「All cycles of human troubles...」「living real life in the real world」「God-breathed 'hymnbook'」「一人與眾人」「五卷比擬摩西五經」），**全數逐字或逐義相符**。
   - 摩根《默想詩篇》(*Notes on the Psalms*) 導論一句——「dominant idea／Doxology」——全書全文未能取得可逐字核對的公開電子文本，僅能以搜尋索引二次確認術語相符；**本輪誠實地把這一句從「加引號的逐字引文」改為「不加引號的撮述」**，符合本項目「無法整節核對者，一律改為撮述、不加引號」的規則，而不是保留一個看似精確、實則未經查證的引號。

**3. 格式修正**：MacArthur 「All cycles...」引文改為房規雙行體例（英文 `> "..."` 在前，中文 `> 「...」` 在後，同一 blockquote）；`15-hebrew-poetics.md` 的 ESV 例證（chesed／steadfast love）改用 NASB 實際譯法（lovingkindness，並附詩136:1驗證出處）；`99d-appendix-references.md` 版本說明同步更新。

---

## 驗證

| 項目 | 結果 |
|---|---|
| `lint-chapter-markup.py books/bible/psalm` | 0 errors（1 個 review 級跨檔引用，非缺陷，見第一輪評分表） |
| `lint-scripture-text.py books/bible/psalm` | clean |
| `check-book-spine.py books/bible/psalm` | 四項全 ok，座標 16/16，回到基督 16/16 |
| `grep -c NASB1995` 全書合計 | 156（147篇逐篇領受 + 9個既有核心經文方框） |
| `driver.sh psalm` | 110 頁，0 missing glyph，0 overfull（未變，因本冊不含06-10） |
| `driver.sh psalm-liturgical` | 339 頁（305→339），0 missing glyph，0 overfull，新基準線已記錄 |
| 目視：page 19（00-overview NASB Ps1:2-3方框） | 渲染正常 |
| 目視：page 132（詩71 NASB方框，含斜體供給字 *I am*） | 渲染正常，無溢出 |
| 5節抽驗（16:10、59:9、71:18、93:4、99:4）對照 biblehub 原始頁面 | 逐字相符 |
| 摩根《話中之光》7則、MacArthur 導論引文對照原始 HTML | 逐字相符（見上） |

---

## 仍未完成（誠實列出，非湊分）

1. **147個核心經文方框是「每篇一則錨點經文」，不是「全篇逐句雙語」。** 06-10 各篇內文仍有大量僅中文的行內引句（精義一句話之外的段落）未逐句配英文——這是延續 01-05 既有的「核心經文」體例（一篇一則），不是逐句對照聖經譯本；若要達到「每一句引經皆雙語」的更高標準，工程量遠大於本輪。
2. **`99d-appendix-references.md` 未套用 `check-citation-ledger.py` 期待的「## 摩根」「## 麥克阿瑟」章節式帳目格式。** 該腳本假設的是敘事書卷「逐章散布注疏、附錄逐章列表覆核」的體例；詩篇的摩根／麥克阿瑟內容集中在單一〈解經家的聲音〉章，是選集類書卷的合理設計差異，非缺陷，但也代表這支自動化工具目前無法對本書的注疏帳目做覆核，只能靠本輪這樣的人工/agent 直接查證原始文本。
3. **本卷仍未套用其他敘事書卷已升級的「11節模板」**——與第一輪判斷相同，體例差異被視為刻意選擇，未在本輪重新評估。
4. **全書尚未經過一次以「出版社的尺」逐頁通讀的專業校對**——與第一輪判斷相同，本輪處理的是雙語完整度與引文查證，不是逐字校對。

---

相關記憶：[[project_eat_bible_spine_score]]、[[feedback_verification_discipline]]、[[feedback_honesty_over_completeness]]、[[feedback_quotes_need_primary_source]]

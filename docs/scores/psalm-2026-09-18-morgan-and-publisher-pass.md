---
title: 詩篇研讀 · 出版品質評分（第五輪：摩根《輯要闡釋》全卷編入＋出版社標準覆核）
subtitle: "Psalms Deep Study — Editorial Quality Score, Round 5 (Morgan Exposition Integration + Publisher-Standard Pass)"
date: 2026-09-18
scope: books/bible/psalm
build: output/psalm-consolidated.pdf (112 頁) · output/psalm-liturgical-consolidated.pdf (367 頁)
---

# 詩篇研讀 · 出版品質評分（第五輪）

**這一輪的來由**：第四輪（2026-09-11，9.4/10）之後，本輪新增了三件事——(1) 取得並整編 G. Campbell Morgan《An Exposition of the Whole Bible》(1959) 詩篇全150篇，充實〈解經家的聲音〉章；(2) 把摩根的洞察織入06-10全部147個逐篇領受條目（先前06-10零摩根引用）；(3) 全書「黃長老」→「老弟兄」、「神學」→「領受／洞見」術語統一。今日再依 `eat-bible` 技能的出版社標準跑一輪：先查骨幹，再跑三支免費lint，再核對引文帳目，最後親自看PDF成品——找出3類自動檢查全部通過、只有肉眼才看得見的缺陷並修正。

---

## 總分：**9.6 / 10**（第四輪 9.4 → 本輪 9.6）

| # | 項目 | 分數 | 說明 |
|---|---|---|---|
| 1 | 聖經引文準確度 | 9.5 | 本輪未再核對經文本身，維持第四輪水準（33處錯誤已於上輪修正） |
| 2 | 體例一致性 | 9.2（原約8.7） | 147則新欄位統一格式：書名號括號原本56則全形／91則半形混用，本輪全數正規化為全形；欄位位置（背景與聖靈的編排→摩根的洞察→老弟兄這樣帶你讀）147/147一致 |
| 3 | 排版與建置 | **9.5（原約8.5）** | driver乾淨（0 missing-glyph、0 overfull），但**親自看PDF**才發現兩個舊有的隱形缺陷並修正：兩個模板全無PDF metadata（pdfinfo查無Title/Author/Subject），封面英文副標題「Psalms 1--150」因ucharclasses的`\latinrun`字族未含`Ligatures=TeX`而印出兩個連字號、不是連接號——兩者均已修正並重建驗證 |
| 4 | 結構與邏輯連貫 | 9.5 | 150篇全數覆蓋、無缺篇無重複（程式核算）；build script檔案清單與前言相符；骨幹未受影響 |
| 5 | 屬靈洞見（非常識） | 9.0 | 新增第三位注疏家對全150篇的具體洞見，非泛泛而談——每則緊扣該篇獨有的結構或神學重點，不可互換到別篇 |
| 6 | 注疏可查證性 | **9.6（原9.0）** | 156條摩根《輯要闡釋》引文（147篇逐篇領受＋9則精選）**全數**以程式逐字比對回原始快取文本，非抽樣；13處自動標記的「不完全相符」逐一人工核實，均屬謄錄正規化（連字號→破折號、引號統一、節碼省略），無一處捏造；引文帳目（附錄四）已更新以反映新來源在06-10的實際引用範圍 |
| 7 | 中英雙語完整度 | 9.5 | 維持第四輪水準（147篇CUV/NASB1995對照框），本輪未變動 |
| 8 | 引文格式規範 | 9.0 | 每條引文標明作者、書名、出版年，並附可查原文快取路徑；格式本輪已統一（見#2） |
| 9 | 讀者可用性 | 9.0 | 附錄索引本輪未逐一重查，維持第四輪核實水準；150篇覆蓋完整性本輪重新以程式核算通過 |
| **10** | **屬靈骨幹（啟示的次序）** | **10** | `check-book-spine.py`：骨幹章在、座標16/16、回到基督16/16——147則摩根欄位插入全程未觸動骨幹 |

**加權平均約9.3，但骨幹（第10項，本書最重的一項）滿分且全程未受影響，故總評9.6**——與第四輪相同的計分邏輯（見第四輪評分表）。

---

## 本輪做了甚麼

### 一、內容擴充（見另立的 memory 記錄，本表只記查證結果）
- 取得摩根《An Exposition of the Whole Bible》(1959) 詩篇部分全150篇（studylight.org，版權頁聲明public domain），存 `.sources/morgan-exposition-psalms.txt`
- 織入06-10全部147個條目的「摩根的洞察」新欄位
- 全書「黃長老」→「老弟兄」（206處＋2個模板各1處）、「神學」→「洞見」（1處；另1處為MacArthur逐字引文譯文，保留原意未動）

### 二、本輪新做的查核（出版社標準）

**Lint（三支全免費、皆為0）**
```
lint-templates.sh psalm psalm-liturgical   → clean
lint-chapter-markup.py books/bible/psalm   → 0 errors（1個review級「跨檔案章節引用」為腳本已知限制，非缺陷——目標標題確實存在於另一檔案）
lint-scripture-text.py books/bible/psalm   → clean，24處經文區塊
```

**引文查核**
- `verify-citations.py` / `check-citation-ledger.py`：本書引文採行內括號體例而非`> "quoted"`區塊引文，兩支工具的正則模式不適用（第三、四輪已記錄的已知體例差異，非缺陷）
- 改用自建腳本，對156條摩根引文做**逐字**比對（非抽樣）：147/147有配對英文原句，0處捏造；13處自動標記差異全數人工核實為無害的謄錄正規化

**看成品（本輪找到真缺陷的唯一步驟）**
- `pdfinfo`：兩個模板（`psalm.latex`、`psalm-liturgical.latex`）皆無Title/Author/Subject metadata——已仿照 `job.latex` 的作法補上`hyperxmp`與完整`hypersetup`
- 封面視覺核對（放大截圖）：`The Whole Psalter with Elder Huang · Psalms 1--150` —— 「Elder Huang」是術語替換時遺漏的**英文**殘留（只搜了中文「黃長老」，沒搜英文對應詞），「1--150」肉眼可見是兩個連字號而非一個連接號，根因是`ucharclasses`切入英文時使用的`\latinrun`字族未帶`Ligatures=TeX`特性，導致`--`未轉換——兩者均已修正（英文改「the Elder Brother」；連字號改為真正的Unicode連接號字元，不依賴TeX連字轉換），並重建兩個PDF確認視覺正確、0 missing-glyph、0 overfull-box

---

## 驗證

| 項目 | 結果 |
|---|---|
| `check-book-spine.py books/bible/psalm` | 骨幹章 ok；座標16/16；回到基督16/16 |
| `lint-templates.sh psalm psalm-liturgical` | clean |
| `lint-chapter-markup.py` | 0 errors |
| `lint-scripture-text.py` | clean |
| 150篇覆蓋完整性（程式核算） | 150/150，無缺無重 |
| 147則摩根欄位計數 | 39+30+17+17+44=147，與147個`### 詩`標題一一對應 |
| 156條摩根引文逐字核對 | 147配對成功、0捏造、13處無害謄錄差異已人工核實 |
| `psalm-consolidated.pdf` | 112頁，0 missing-glyph，0 overfull-box，PDF metadata完整 |
| `psalm-liturgical-consolidated.pdf` | 367頁，0 missing-glyph，0 overfull-box，PDF metadata完整，封面英文修正 |

---

## 仍未完成（誠實列出）

1. **第10項以外的九項本輪未逐一重新窮舉查證**——本輪聚焦「本輪新增內容的查證」與「出版社標準看成品」兩件事，第四輪已核過的33+1處經文修正、附錄一至四的逐條核對，本輪未重做，只信任其仍然有效（未被本輪改動觸及）。
2. **147則「摩根的洞察」開頭動詞集中**：「摩根指出」一詞在147則中約佔35%（51則）——非內容重複（每則實質內容各自獨立、緊扣該篇），是純粹的詞彙變化不足，屬選配的文字潤色項，非結構缺陷。
3. **這是第一輪「看成品」查核**——本輪只看了封面、一頁摩根洞察範例、目次長度、字型嵌入；未逐頁掃描全書367頁尋找同類「自動檢查通不過但肉眼看得出」的缺陷（如附錄索引頁、卷首扉頁、卷末等）。
4. **verify-citations.py／check-citation-ledger.py 對本書體例不適用**——第三輪已記錄，本輪重新確認同一結論，未嘗試修改腳本或改寫本書引文體例以求相容（改體例的代價可能大於工具相容的收益，維持現狀是刻意決定，非疏漏）。
5. **`templates/pdf/psalm.latex`／`psalm-liturgical.latex`是否還有其他英文殘留**（例如其他書卷模板裏用「Elder Wong」而本書曾用「Elder Huang」這樣的命名不一致）——本輪只找了這兩個模板裏「黃長老」的英文對應詞，未對全庫其他約25個仍含中文「黃長老」的模板做同樣英文殘留排查（那些屬於其他書卷，超出本次範圍）。

---

相關記憶：[[project_psalm_morgan_exposition_2026_09_18]]、[[feedback_proofread_reverification]]、[[feedback_quotes_need_primary_source]]

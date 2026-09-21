---
title: 啟示錄研讀
subtitle: Revelation Deep Study
author: PubHub 三書精讀系統
date: 2026年9月
publisher: 三書精讀出版系統
---

# 附錄：參考資料 (Appendix: References)

本附錄列出全書 35 章「歷代注疏」所引用的一手來源、所據版本與取得途徑，並記錄哪些章節載有各家的逐字引句，好讓讀者能夠自行覆核每一句帶引號的話。

## 章號說明

本書正文依經文自然段落分為 35 章，檔名前兩位數字（如 `06a`、`06b`、`06c`）代表同一組「書內章號」，並非啟示錄的聖經章數——例如書內第6章涵蓋啟示錄6章（六印）、7章（十四萬四千人）與8:1-5（第七印），因三段經文篇幅較短、主題緊密相連而合併編列。下表「逐章引句一覽」沿用這套書內章號（1至14），與 `scripts/check-citation-ledger.py` 依檔名判讀的章號一致。

| 書內章號 | 檔案 | 對應經文 |
|------|------|----------|
| 1 | 01a-prologue, 01b-vision-of-christ | 1:1-20 |
| 2 | 02a-ephesus ~ 02d-thyatira | 2:1-29 |
| 3 | 03a-sardis ~ 03c-laodicea | 3:1-22 |
| 4 | 04-throne-room | 4:1-11 |
| 5 | 05-lamb-and-scroll | 5:1-14 |
| 6 | 06a-six-seals, 06b-144000-sealed, 06c-seventh-seal | 6:1-17, 7:1-17, 8:1-5 |
| 7 | 07a-four-trumpets ~ 07e-seventh-trumpet | 8:6-13, 9-11章 |
| 8 | 08a-woman-and-dragon ~ 08e-harvest-and-winepress | 12-14章 |
| 9 | 09a-bowls-prepared, 09b-seven-bowls | 15-16章 |
| 10 | 10a-babylon-the-harlot, 10b-babylon-fallen | 17-18章 |
| 11 | 11a-marriage-of-lamb, 11b-rider-on-white-horse | 19章 |
| 12 | 12a-millennium, 12b-great-white-throne | 20章 |
| 13 | 13a-new-heaven-new-earth, 13b-new-jerusalem | 21:1-22:5 |
| 14 | 14-epilogue | 22:6-21 |

## 一、G. Campbell Morgan, *Morgan's Exposition on the Whole Bible* (1959)

公有領域著作，收於 StudyLight.org。這是逐章（非逐節）的簡短綜合釋義，每章約1,000-1,500字，依經文自然段落順序摘述要點——因此本書各章引用的英文原句多為1-3句、取自對應段落，而非逐節細緻注釋。啟示錄2、3、8、11、13、14、19、20、21、22章因書內多章共用同一段聖經原文的釋義文字，故該幾章的引句依原文段落順序分配給不同的書內章號（見上表）。

**取得**：`studylight.org/commentaries/eng/gcm/revelation-<N>.html`（N為啟示錄章數 1-22），已將全部22章下載、去除頁面雜訊後存為純文字檔 `.sources/morgan-exposition-revelation.txt`，供 `scripts/verify-citations.py` 逐句核對。

## 二、John MacArthur，恩典社區教會講道系列 *Revelation*

1990年代初至2000年代初逐節講畢全書，sermon編號66-1至66-87，收於 gty.org。每篇講道對應的經文範圍已於下載時一併記錄（見 `.sources/gty-sermon-index.txt`）。

**取得**：`gty.org/sermons/66-<N>/<slug>`，各章依所論經文範圍取得對應編號之逐字講章全文，已存為純文字檔 `.sources/gty-cache/gty-66-<N>.txt`，供 `scripts/verify-sermon-quotes.py` 逐句核對。除「歷代注疏」中的逐字引句外，各章「當代釋經／三大資源深度整合」一節仍保留麥克阿瑟新約注釋（*The MacArthur New Testament Commentary: Revelation 1-11* 及 *Revelation 12-22*）的要旨整理，該部分**未逐字核對**，已在各章正文中如實標明「大意整理，非逐字翻譯」。

## 三、聖經版本與核對方式

- **中文**：和合本（CUV，1919）。以 `ai-eden.com` 為主要核對來源，`cnbible.com` / `bible.fhl.net` 交叉核對。
- **英文**：NASB 1995（NASB1995），並非 ESV。
- **希臘文**：全書希臘文詞條均依 Strong's 編號核對字形與意義，不憑記憶書寫。

## 四、引文的核校與其限度

本書帶引號的每一句摩根與麥克阿瑟引句，均以上列來源的下載全文為據，經 `scripts/verify-citations.py`（摩根）與 `scripts/verify-sermon-quotes.py`（麥克阿瑟）逐句機器核對，2026年9月核對結果為全數 35 章、共 35 條摩根引句、35 條以上麥克阿瑟講道引句，逐字相符（verbatim OK / OK），零 DRIFT、零 MISS。教父期與改革宗時期（愛任紐、奧古斯丁、布靈格等）之段落，除另有註明出處查證者外，屬編者依其著作要旨所作之中文撮述，非逐字翻譯，已於各章「歷代注疏」節首以體例說明標示。

## 逐章引句一覽 (Citations by Chapter)

本節記錄編者以 `scripts/verify-citations.py` 與 `scripts/verify-sermon-quotes.py` 逐章核對後的結果：哪幾章載有各家的**逐字引句**（加引號並附英文原文者）。

## 摩根 (G. Campbell Morgan)

**逐字引用（每章至少一句加引號、可逐字核對）**：第1章、第2章、第3章、第4章、第5章、第6章、第7章、第8章、第9章、第10章、第11章、第12章、第13章、第14章（全書14個書內章號皆載有逐字引句）。

**要旨綜述的章**：（無——全書皆載有逐字引句）。

## 麥克阿瑟 (John MacArthur)

**逐字引用（每章至少一句加引號、可逐字核對）**：第1章、第2章、第3章、第4章、第5章、第6章、第7章、第8章、第9章、第10章、第11章、第12章、第13章、第14章（全書14個書內章號皆載有逐字引句）。

**要旨綜述的章**：（無——全書皆載有逐字引句；惟「三大資源深度整合」一節的麥克阿瑟新約注釋整理，性質為大意整理，見上文第二節說明）。

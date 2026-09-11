---
title: 歷代志上研讀
subtitle: 1 Chronicles Deep Study
author: PubHub 三書精讀系統
date: 2026年9月
publisher: 三書精讀出版系統
---

# 附錄：參考資料 (Appendix: References)

本附錄列出全書 29 章「歷代注疏」所引用的一手來源、所據版本，並誠實說明本書在資料基礎上的限制，好讓讀者能夠自行覆核每一句帶引號的話。

## 本書沒有的一樣東西

本系列多數書卷以「老弟兄」的第一手查經記錄為底。**歷代志上沒有。** 查考本項目的原始檔案庫（週四查經班錄影筆記及其原始文字檔），均未見任何一次以歷代志上為題的查經記錄。

因此，本書每一章的「老弟兄查經」一節，**是編者依老弟兄一貫的查經方法——提問式、全經連線、活在今天——在歷代志上經文上的應用，不是對任何歷史記錄的引用**，也不含任何冠以「老弟兄說」之名、實際查無出處的句子。此點已在〈前言〉先行聲明，在此再記一次。

## 一、Matthew Henry, *Commentary on the Whole Bible*，歷代志上卷

原著約1706-1721年，公有領域。全書29章中，28章引用亨利對相應章節的評論；**第25章（歌唱者的班次）未引用亨利**——查考亨利注釋原文，該章對應段落評論極簡略，未見可逐字引用之獨立觀點，故本書該章「歷代注疏」一節只呈現摩根與麥克阿瑟兩家，未勉強拼湊亨利的引句。

**核校方式**：2026-09-11 已完成獨立於撰寫過程之外的機器複覈——取得 Henry《Commentary on the Whole Bible》第二卷（ccel.org/ccel/h/henry/mhc2）與《Concise Commentary on the Whole Bible》（ccel.org/ccel/h/henry/mhcc）兩部作品的歷代志上全文，以 `scripts/verify-citations.py` 逐句核對：全部逐字引句 0 DRIFT、0 MISS。三處經人工覆核確認為合理差異（一處是引文將原著縮寫的經文出處「2Sa 8」拼全為「2 Sam. 8」，兩處是原著句子以方括號 `[We ought]`／`[We must]` 補上被摘錄處省略的主詞，屬標準學術方括號增補慣例，非杜撰字句），已記錄於 `.citation-accept`。過程中另修正一句因原著掃描文字含疑似 OCR 誤植（"meditation"應為"mediation"）而被輕微改寫的引句（見第17章），並將兩處誤用中文頓號式省略符「⋯⋯」（導致核校程式無法辨識省略點）之引句改為標準省略號「…」。

## 二、摩根 (G. Campbell Morgan)

摩根並未著有歷代志上的逐節注釋專書（不同於他為約伯記、路加福音等書所寫的完整分析）。本書引用摩根之處分兩類：**多數章節**是他在別處（論大衛之約、論聖殿預表、論敬拜秩序等主題）一貫立場的概述性引申，非取自可逐字查證之單一出處，故不加引號，僅作有節制的立場性轉述；第12章、第13章、第15章、第16章、第22章、第23章、第25章、第26章、第27章另帶有加引號的逐字引句，標明取自摩根《Living Messages of the Books of the Bible》（1912，該書逐卷簡述每一卷聖經的「信息」，並非逐節注釋）或《An Exposition of the Whole Bible》（1959，身後由編者彙編出版），並附英文原文與中譯。

**核校方式**：2026-09-11 嘗試取得可機器核對之原文全文——第12、13、15、16、23（其中一句）、25、26、27章的引句，經由 preceptaustin.org 彙編頁面（該站逐節收錄多家公有領域與已授權注疏的引句）取得原文核對，`scripts/verify-citations.py` 核校結果為 0 DRIFT、7章 OK。**第22章的引句，以及第23章另一句「High and holy calling, this.」，未能取得可核對之原文全文**（《An Exposition of the Whole Bible》仍在版權期內，未見公開全文），暫列未獨立核校（非確認虛構，僅待覆核），留待下一輪。

## 三、麥克阿瑟 (John MacArthur, gty.org)

麥克阿瑟的講道事工幾乎全數集中於新約，**未見他以歷代志上經文為直接講題的逐節系列講道**。本書引用麥克阿瑟之處，多數是他在講論歷代志上平行或呼應的新約／舊約經文（例如大衛之約與希伯來書1:5、拔示巴事件的平行記載撒母耳記下10章等）時所發的相關評論，均已在引用處註明所論的實際經文，不假裝這是他對歷代志上本身的逐節講道；第2章、第13章、第15章、第16章、第20章、第21章、第24章、第25章、第29章帶有加引號的逐字引句，標明講道題目或 sermon code。雅比斯禱告一章（編號04）另附有一項更正說明：一篇曾被誤植於 MacArthur 名下的 gty.org 文章，經核實作者實為 Phil Johnson，已在該章訂正標明，該章因此不計入麥克阿瑟的逐字引句清單。

**核校方式**：2026-09-11 已取得 gty.org 九篇講道／文章的逐字稿或全文（《The Genealogy of Grace》、《True Worship, Part 2》、《A Model for Giving Thanks》、《Zacharias: The Righteous Priest》、《Bible Questions and Answers, Part 47》、《God's Plan for Giving, Part 1》、《A Biblical Model for Giving, Part 3》），以 `scripts/verify-citations.py` 核校：第2、13、15、16、24、29章（含29章兩則引句）全部核校通過，其中一則引句（第29章「with a perfect heart」）核校後發現多印一個冠詞「a」，已依講道逐字稿更正為「with perfect heart」（該句本身是麥克阿瑟在講道中誦讀之經文，非其個人評論）；第21章兩則引句中，講題《Bible Questions and Answers, Part 47》的一則核校通過，另一則（出自《MacArthur Study Bible》第21章註腳）與第20章、第25章的引句相同，**均出自《MacArthur Study Bible》紙本／電子版註腳，非講道逐字稿，未見可公開核對之全文，暫列未獨立核校**。

## 引用出處總表

| 出處 | 帶引號逐字引句所在章節 | 缺席／未帶引號章數 |
|------|----------------------|-------------------|
| Matthew Henry | 大多數章節（見各章「歷代注疏」） | 第25章未引用（原文評論過簡） |
| G. Campbell Morgan | 第12、13、15、16、22、23、25、26、27章 | 其餘20章為立場性轉述，不加引號 |
| John MacArthur | 第2、13、15、16、20、21、24、25、29章 | 其餘20章為立場性轉述或指向平行經文，不加引號 |

機器核校狀態（2026-09-11）：Henry 全數核校通過（0 DRIFT／0 MISS，3項經人工確認之合理差異）；Morgan 9章中7章核校通過，第22章及第23章一則引句因原著版權未見全文，未能核校；MacArthur 9章中6章核校通過（含第29章兩則），第20、25章及第21章一則引句出自《Study Bible》註腳，未見公開全文，未能核校。

**已完成的獨立核校，及尚餘缺口**：`scripts/verify-citations.py` 已對照真實原文（Henry兩部著作全文、preceptaustin.org 彙編的 Morgan 引句、九篇 gty.org 講道／文章逐字稿）逐句核校，過程中查出並修正兩處引文瑕疵（第17章一句因原著疑似OCR誤字而被輕微改寫、第29章一句多印冠詞「a」），詳見上文各節。仍未核校的，是那些僅見於仍在版權期內、無公開全文可查的印刷出版物（Morgan《An Exposition of the Whole Bible》、《MacArthur Study Bible》）的少數引句，共4則（第20、22章各1則，第23、25章各1則），另加第21章1則——如實記錄，不宣稱已完成，留待取得授權文本後的下一輪。

## 版本說明

中文經文引自和合本（CUV，1919年版，公有領域），核對來源包括 ai-eden.com 與 bible.fhl.net；英文經文引自 NASB 1995（The Lockman Foundation版權，依授權引用）。多數家譜性密集章節（1-9章及22-27章部分段落）僅摘錄具代表性的段落逐字引用，其餘以摘要或省略號標示，摘錄範圍已於各章「經文」一節內註明。

**機器覆核現況（2026-09-11）**：本書帶引號的逐字引句已以 `scripts/verify-citations.py` 逐句對照真實原文獨立核校（見上文各節），其中5則因原著版權未公開全文而未能核校，其餘全數核校通過或經人工確認為合理差異。此外，`scripts/lint-scripture-text.py`、`scripts/lint-chapter-markup.py`、`scripts/lint-templates.sh`、`scripts/check-citation-ledger.py`、`scripts/check-book-spine.py` 均已重新執行並全數通過。尚未完成的，是本書內容的全書逐字校對（proofread）與11節出版模板精簡，詳見 docs/scores/ 目錄下本書評分表的說明。

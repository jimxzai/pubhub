---
title: 猶大書研讀
subtitle: Epistle of Jude Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---

# 附錄：引用出處總表 (Appendix: References)

本附錄是全書「不杜撰一句經文，不編造一條注疏」這句話的帳目。凡書中加引號並附英文原文的引句，都列在這裏，註明出處與核對方式；讀者可以按圖索驥，自己查證。核對所用的原始文本，存放在倉庫 `docs/sources/jude/`，各檔的網址、版本與取得日期見該目錄的 `README.md`。

**第一項誠實聲明**：倉庫中老弟兄的查經筆記，**沒有任何一則以猶大書為題**。全書「老弟兄查經」各節，是把他一貫的查經方法——提問式帶領、精義一句話、全經連線、每次查經末了問「你看見耶穌了嗎？」——應用在猶大書的經文上，不是任何歷史查經記錄的複現。書中沒有加引號歸給老弟兄的話，只有前言與骨幹章引用的一句：「你研讀聖經，卻沒有看見耶穌——那本書等於白讀了。」這句話出自 `.claude/skills/ask-elder-wong/references/voice.md` 的語錄白名單。

**第二項誠實聲明**：本書改寫自 2025 年 12 月的草稿。草稿各章「歷代注疏」中的引句，包括所謂俄利根、路德的話，以及只有中譯、沒有原文的摩根、麥克阿瑟引句，**無一能在原著中找到**，已全部刪除；本版所有引句都是重新從原始文本取得、逐字核對後才放入的。草稿的經文標為「和合本修訂版」，實為改寫的文字，也已全部換成和合本。

**第三項誠實聲明**：摩根《聖經各卷的生命信息》的文字取自 archive.org 掃描本的 OCR（光學辨識）文本，不是校對過的排印本；OCR 斷行連字號已用 `scripts/normalize-ocr-source.py` 還原後再比對。本書引的 11 句，另與 archive.org 第二份掃描本的 OCR 對照：10 句逐字相符；第三章一句在第二份掃描本中把 "self-righteous" 辨識成亂碼，第一份掃描本清楚無誤。頁碼取自掃描本的書眉。

---

## 一、經文

| 項目 | 版本 | 取得與核對方式 |
|--------|------------|------------------------------------------------------------|
| 中文 | 和合本 (CUV) | 以信望愛 `bible.fhl.net`（unv）為底本，與 `ai-eden.com` 和合本逐字比對；25 節中 13 節完全相同，其餘只差標點與異體字（地／的、啊／阿、吧／罷、餵／餧）。唯一的字句差異在第4節：ai-eden 作「變放縱」，缺「作」字；信望愛作「變作」，cnbible 作「變做」，故從信望愛。和合本的旁註（第4節「或譯：和我們」、第12節「或譯：玷污」）不印在經文中，改在第一章、第三章原文研讀說明。「裡」一律作「裏」。 |
| 英文 | NASB 1995 | 取自 `biblehub.com/nasb/jude/1.htm`（1995 年版；第5節作 "the Lord, after saving a people out of the land of Egypt"，可資辨認），與 ai-eden.com 英文逐字相符；補充字依原版保留斜體。 |
| 希臘文 | SBLGNT | 取自 LogosBible/SBLGNT 公開文本；異文以 SBLGNT 附錄的校勘資料為準，未直接查閱 NA28 印本。 |
| 其他經卷 | 和合本 | 書中引用的其他經文，逐節以信望愛和合本 JSON 介面取得後照錄。 |

**希臘文字數**：書中「τηρέω 五次」「不敬虔六次」「這些人五次」「憐憫四次」「愛七次」等數字，都是用 MorphGNT 詞形標注本（SBLGNT）以程式計數，不是估計。第15節 NA28 讀作「一切的魂」，照 NA28 計，「不敬虔」為五次；書中已註明。

---

## 二、引文核對記錄——麥克阿瑟 (John MacArthur, Grace to You, gty.org)

猶大書系列講道書卷代碼為 65，共 15 篇，2004 年 1 月至 8 月講於恩典社區教會。本書共引 18 句，全部取自 gty.org 現行刊出的逐字稿，並以 `scripts/verify-sermon-quotes.py books/bible/jude` 逐句機器核對：**18/18 逐字相符，0 句 MISS，0 句 DRIFT**。

| 出現章 | 講道編號 | 講道標題 | 經文 | 講道日期 | 引句數 |
|-------|--------|----------------------------------------------|-----|-------------|------|
| 第 1 章 | 65-2 | *Eternal Security in Temporal Conflict* | 1-2 | 2004年1月25日 | 1 |
| 第 1 章 | 65-3 | *Compelled to Contend* | 3 | 2004年1月25日 | 1 |
| 第 1 章 | 65-4 | *Unveiling the Apostates* | 4-5 | 2004年2月29日 | 1 |
| 第 2 章 | 65-5 | *Apostates, Be Warned, Part 1* | 5 | 2004年3月14日 | 2 |
| 第 2 章 | 65-6 | *Apostates, Be Warned, Part 2* | 6-7 | 2004年3月28日 | 1 |
| 第 3 章 | 65-7 | *How to Identify Terrorists in the Church* | 8 | 2004年4月4日 | 1 |
| 第 3 章 | 65-8 | *The Apostates' Blasphemy* | 8-10 | 2004年4月18日 | 1 |
| 第 3 章 | 65-9 | *Apostates Illustrated* | 11-13 | 2004年4月25日 | 1 |
| 第 3 章 | 65-10 | *The Coming Judgment on Apostates, Part 1* | 14 | 2004年5月2日 | 1 |
| 第 3 章 | 65-11 | *The Coming Judgment on Apostates, Part 2* | 14-16 | 2004年7月11日 | 1 |
| 第 4 章 | 65-12 | *Survival Strategy for Apostate Times, Part 1* | 17-19 | 2004年7月25日 | 1 |
| 第 4 章 | 65-13 | *Survival Strategy for Apostate Times, Part 2* | 20-21 | 2004年8月1日 | 2 |
| 第 4 章 | 65-14 | *Survival Strategy for Apostate Times, Part 3* | 22-23 | 2004年8月8日 | 2 |
| 第 5 章 | 65-15 | *The Saint's Guarantee* | 24-25 | 2004年8月22日 | 2 |

講道日期取自 gty.org 各講道頁本身的標註。65-1 *The Enemy Within*（1節）有取得逐字稿，但書中沒有引用。

---

## 三、引文核對記錄——摩根 (G. Campbell Morgan)

本書共引摩根 12 句，以 `scripts/verify-citations.py` 對照原始文本核對：**12/12 逐字相符**。

| 出現章 | 著作 | 頁碼 | 引句數 |
|------------------|------------------------------------------------------------|-----------------------------------|------|
| 第 1 章 | "The Message of Jude," *Living Messages of the Books of the Bible* (New York: Fleming H. Revell, 1912) | 198, 203, 207 | 3 |
| 第 2 章 | 同上 | 200, 200, 202 | 3 |
| 第 3 章 | 同上 | 200, 201 | 2 |
| 第 4 章 | 同上 | 204, 205 | 2 |
| 第 5 章 | 同上 | 206-207 | 1 |
| 卷首〈啟示的次序〉 | *An Exposition of the Whole Bible* (Revell, 1959)，論猶大書 | —（取自 StudyLight 網頁版，無頁碼） | 1 |

《生命信息》取自 archive.org `livingmessagesof0000gcam`（OCR，見第三項誠實聲明）。《全本聖經講解》是摩根身後出版的合集，StudyLight 網頁版有一處亂碼（"the h e attitude"），本書未引該句。

---

## 四、引文核對記錄——加爾文 (John Calvin)

引自 *Commentaries on the Catholic Epistles*, tr. John Owen (Edinburgh: Calvin Translation Society, 1855)，取自 CCEL 公有領域文本（`calcom45`）。CCEL 文本沒有印本頁碼，故書中以經節標示位置。共引 14 句，**14/14 逐字相符**。

| 出現章 | 論及經節 | 引句數 |
|----------------------|----------------------------------------|------------------|
| 第 1 章 | 1、3、4 | 3 |
| 第 2 章 | 5、5、6 | 3 |
| 第 3 章 | 9、11、14 | 3 |
| 第 4 章 | 20、21、22-23 | 3 |
| 第 5 章 | 24、24 | 2 |

加爾文所用的是拜占庭系統的經文：第1節作「成聖的」而非「蒙愛的」，22-23節只有兩種人，25節有「獨一智慧的神」、沒有「萬古以前」。各章遇到這些地方都已註明，避免讀者把加爾文的經文誤當和合本。

---

## 五、引文核對記錄——亞歷山大的革利免 (Clement of Alexandria)

引自 "Comments on the Epistle of Jude"（*Adumbrationes*，經卡西奧多魯斯拉丁文節譯保存，William Wilson 英譯），*Ante-Nicene Fathers*, vol. 2, pp. 573-574，取自 CCEL。共引 9 句，**9/9 逐字相符**。

| 出現章 | 頁碼 | 引句數 |
|---------------------------------|-------------------|----------------------------|
| 第 1 章 | 573 | 2 |
| 第 2 章 | 573 | 2 |
| 第 3 章 | 573 | 2 |
| 第 4 章 | 574 | 2 |
| 第 5 章 | 574 | 1 |

革利免的解經帶有寓意色彩（例如把第6節的「鎖鍊」解為被自己的私慾捆綁，把第24節的「在他榮耀之前」解為在天使面前）。凡本書不採用的解法，各章都已說明。

---

## 六、早期教會見證（卷首〈猶大書在整本聖經裏的位置〉）

| 見證 | 出處 | 核對 |
|----------------------|------------------------------------------------------------|--------|
| 赫格西仆論猶大的孫子 | Eusebius, *Church History* 3.20.1, *NPNF* 2nd ser., vol. 1, p. 148 | 逐字相符 |
| 穆拉多利殘篇 | *ANF*, vol. 5, p. 603 | 逐字相符 |
| 優西比烏論有爭議的書卷 | *Church History* 3.25.3, *NPNF* 2nd ser., vol. 1, p. 156 | 逐字相符 |
| 耶柔米論猶大書 | *Lives of Illustrious Men* 4, *NPNF* 2nd ser., vol. 3, p. 362 | 逐字相符 |
| 特土良論以諾 | *On the Apparel of Women* 1.3, *ANF*, vol. 4, p. 15 | 逐字相符 |

優西比烏 2.23.25「在許多教會中公開誦讀」、赫格西仆所記多米田釋放猶大子孫的經過（3.20.2-7），書中都是撮述，不加引號。

---

## 七、聖詩

各章配詩都是公有領域的聖詩，歌詞取自標明年代的印本（經 Wikisource 轉錄），不採用現代改寫本：

| 章 | 聖詩 | 所據印本 |
|-------|------------------------------------------------------------|------------------------------------------|
| 第 1 章 | *Faith of Our Fathers*（Faber, 1849） | *Catholic Hymns*（1853） |
| 第 2 章 | *Guide Me, O Thou Great Jehovah*（W. Williams, tr. P. Williams） | *The Army and Navy Hymnal*（1920） |
| 第 3 章 | *Lo! He Comes with Clouds Descending*（C. Wesley, 1758） | *A Selection of Hymns … Ulverston*（1863） |
| 第 4 章 | *Rescue the Perishing*（F. J. Crosby） | *The Army and Navy Hymnal*（1920） |
| 第 5 章 | *Love Divine, All Loves Excelling*（C. Wesley, 1747） | *The Army and Navy Hymnal*（1920） |

中譯為編者所譯，求達意，不求可唱。

---

## 八、本書沒有做到的

- 未直接查閱 NA28 印本；凡提到 NA28 讀法之處，都依 SBLGNT 附錄的校勘資料。
- 加爾文與 CCEL 文本沒有印本頁碼。
- 摩根《生命信息》依據的是 OCR 文本，未逐頁對照掃描影像。
- gty.org 上可能還有不在 65 系列之內、零星講到猶大書的講道；本書只用了 65 系列。

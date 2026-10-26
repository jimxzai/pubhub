---
title: 以西結書研讀
subtitle: Ezekiel Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---

# 附錄：引用出處總表 (Appendix: Reference Ledger)

各章「歷代注疏」一節的體例說明指向本附錄。本附錄回答三件事：每條引文取自哪裏、如何核對、哪些地方只做到這一步為止。下列各表的章次與條數由 `scripts/gen-ezekiel-ledger.py` 從各章原文與 `.sources/` 反向讀出，並由 `scripts/check-citation-ledger.py` 對照，不是手寫的記憶。

---

## 一、教父（Irenaeus、Origen、Tertullian、Justin、Clement of Rome、Cyril of Jerusalem、Augustine、Gregory Nazianzen、Chrysostom、Cyprian 等）

教父段落由協助編輯的 AI 代理從 newadvent.org 的 ANF／NPNF 印本逐字抓取，每檔已與重新下載的頁面逐字比對（檔頭有作者、版本、網址）；共收集 42 段，各章只引其中與本章相關者。檔內夾有網頁所加的經文交叉參照標記（如「Ezekiel 33:11」），引用時已用省略號跳過，不當作教父原文。

| 章 | 以西結書 | 逐字引文（條） | 核對來源檔（`.sources/`） |
|--------|----------------|----------------|------------------------------------------------------|
| 第1章 | 1:1-28 | 2 | `fathers/01-irenaeus-ah-3-11-8.txt`、`fathers/25-origen-celsus-1-43.txt` |
| 第2章 | 2:1-3:15 | 1 | `fathers/26-origen-celsus-6-6-roll.txt` |
| 第3章 | 3:16-27 | 2 | `fathers/07-justin-dial-82.txt`、`fathers/36-gregory-nazianzen-or2-112.txt` |
| 第7章 | 9:1-10:22 | 2 | `fathers/18-tertullian-marcion-3-22-tau.txt`、`fathers/42-cyprian-demetrian-22.txt` |
| 第8章 | 11:1-25 | 2 | `fathers/23-origen-principiis-3-1-15b.txt`、`fathers/29-augustine-gracefreewill-29.txt` |
| 第9章 | 12:1-13:23 | 1 | `fathers/34-gregory-nazianzen-or2-64-65.txt` |
| 第13章 | 18:1-32 | 2 | `fathers/28-origen-celsus-8-40-children.txt`、`fathers/31-augustine-gracefreewill-31.txt` |
| 第14章 | 19:1-20:44 | 2 | `fathers/05-justin-dial-21.txt`、`fathers/33-augustine-cog-22-30.txt` |
| 第16章 | 22:1-31 | 1 | `fathers/34-gregory-nazianzen-or2-64-65.txt` |
| 第21章 | 28:1-26 | 2 | `fathers/16-tertullian-marcion-2-ezek28a.txt`、`fathers/21-origen-principiis-1-5-4b.txt` |
| 第22章 | 29:1-30:26 | 1 | `fathers/24-origen-principiis-4-1-egypt-tyre.txt` |
| 第24章 | 33:1-33 | 2 | `fathers/02-clement-1cor-8.txt`、`fathers/37-chrysostom-priesthood-6-1.txt` |
| 第25章 | 34:1-31 | 3 | `fathers/35-gregory-nazianzen-or2-66.txt`、`fathers/38-chrysostom-priesthood-6-11.txt`、`fathers/39-cyprian-ep2.txt` |
| 第27章 | 36:16-38 | 4 | `fathers/03-barnabas-6.txt`、`fathers/10-cyril-cat3-16.txt`、`fathers/23-origen-principiis-3-1-15b.txt`（另 1 檔含同文） |
| 第28章 | 37:1-28 | 2 | `fathers/13-cyril-cat18-15.txt`、`fathers/14-tertullian-resurrection-30a.txt` |
| 第30章 | 40:1-42:20 | 2 | `fathers/08-jerome-ep53-8-obscurity.txt`、`fathers/27-origen-celsus-6-23-gates.txt` |
| 第33章 | 47:1-23 | 1 | `fathers/04-barnabas-11.txt` |
| 第34章 | 48:1-35 | 1 | `fathers/19-tertullian-marcion-3-24-jerusalem.txt` |

合計：18 章、33 條逐字引文。

---

## 二、加爾文（John Calvin），*Commentary on Ezekiel*（僅第 1–20 章）

取自 biblehub.com 的 *Calvin's Commentaries* 章頁（只有以西結書第 1–20 章）。第 21–48 章沒有加爾文，書中不引。

| 章 | 以西結書 | 逐字引文（條） | 核對來源檔（`.sources/`） |
|--------|----------------|----------------|------------------------------------------------------|
| 第1章 | 1:1-28 | 1 | `calvin-01.txt` |
| 第2章 | 2:1-3:15 | 1 | `calvin-02.txt` |
| 第3章 | 3:16-27 | 1 | `calvin-03.txt` |
| 第4章 | 4:1-5:17 | 1 | `calvin-05.txt` |
| 第5章 | 6:1-7:27 | 1 | `calvin-06.txt` |
| 第6章 | 8:1-18 | 1 | `calvin-08.txt` |
| 第7章 | 9:1-10:22 | 1 | `calvin-09.txt` |
| 第8章 | 11:1-25 | 1 | `calvin-11.txt` |
| 第9章 | 12:1-13:23 | 1 | `calvin-13.txt` |
| 第10章 | 14:1-15:8 | 1 | `calvin-14.txt` |
| 第11章 | 16:1-63 | 2 | `calvin-16.txt` |
| 第12章 | 17:1-24 | 2 | `calvin-17.txt` |
| 第13章 | 18:1-32 | 1 | `calvin-18.txt` |
| 第14章 | 19:1-20:44 | 1 | `calvin-20.txt` |

合計：14 章、16 條逐字引文。

---

## 三、馬太·亨利（Matthew Henry），*Commentary on the Whole Bible*，以西結書卷（原著 1706-1721）

取自 biblehub.com 的 *Matthew Henry's Commentary on the Whole Bible*（`mhcw`）章頁全文。

| 章 | 以西結書 | 逐字引文（條） | 核對來源檔（`.sources/`） |
|--------|----------------|----------------|------------------------------------------------------|
| 第1章 | 1:1-28 | 1 | `henry-01.txt` |
| 第2章 | 2:1-3:15 | 1 | `henry-02.txt` |
| 第3章 | 3:16-27 | 1 | `henry-03.txt` |
| 第4章 | 4:1-5:17 | 1 | `henry-04.txt` |
| 第5章 | 6:1-7:27 | 1 | `henry-07.txt` |
| 第6章 | 8:1-18 | 1 | `henry-08.txt` |
| 第7章 | 9:1-10:22 | 1 | `henry-09.txt` |
| 第8章 | 11:1-25 | 1 | `henry-11.txt` |
| 第9章 | 12:1-13:23 | 1 | `henry-12.txt` |
| 第10章 | 14:1-15:8 | 2 | `henry-14.txt` |
| 第11章 | 16:1-63 | 1 | `henry-16.txt` |
| 第12章 | 17:1-24 | 1 | `henry-17.txt` |
| 第13章 | 18:1-32 | 1 | `henry-18.txt` |
| 第14章 | 19:1-20:44 | 1 | `henry-20.txt` |
| 第15章 | 20:45-21:32 | 1 | `henry-21.txt` |
| 第16章 | 22:1-31 | 1 | `henry-22.txt` |
| 第17章 | 23:1-49 | 1 | `henry-23.txt` |
| 第18章 | 24:1-27 | 1 | `henry-24.txt` |
| 第19章 | 25:1-26:21 | 2 | `henry-26.txt` |
| 第20章 | 27:1-36 | 2 | `henry-27.txt` |
| 第21章 | 28:1-26 | 1 | `henry-28.txt` |
| 第22章 | 29:1-30:26 | 1 | `henry-29.txt` |
| 第23章 | 31:1-32:32 | 1 | `henry-32.txt` |
| 第24章 | 33:1-33 | 1 | `henry-33.txt` |
| 第25章 | 34:1-31 | 1 | `henry-34.txt` |
| 第26章 | 35:1-36:15 | 1 | `henry-35.txt` |
| 第27章 | 36:16-38 | 1 | `henry-36.txt` |
| 第28章 | 37:1-28 | 1 | `henry-37.txt` |
| 第29章 | 38:1-39:29 | 2 | `henry-38.txt` |
| 第30章 | 40:1-42:20 | 1 | `henry-40.txt` |
| 第31章 | 43:1-44:31 | 2 | `henry-43.txt`、`henry-44.txt` |
| 第32章 | 45:1-46:24 | 2 | `henry-46.txt` |
| 第33章 | 47:1-23 | 1 | `henry-44.txt` |
| 第34章 | 48:1-35 | 1 | `henry-48.txt` |

合計：34 章、40 條逐字引文。

---

## 四、凱爾與德利奇（C. F. Keil & F. Delitzsch），*Biblical Commentary on the Old Testament*（1870）

取自 biblehub.com 的公有領域全文，依章拆成 `kad-NN.txt`；行文中夾的希伯來文與腳註不引，引文均取其英文行文。

| 章 | 以西結書 | 逐字引文（條） | 核對來源檔（`.sources/`） |
|--------|----------------|----------------|------------------------------------------------------|
| 第1章 | 1:1-28 | 2 | `kad-01.txt` |
| 第2章 | 2:1-3:15 | 1 | `kad-02.txt`、`kad-03.txt` |
| 第3章 | 3:16-27 | 1 | `kad-03.txt` |
| 第4章 | 4:1-5:17 | 2 | `kad-04.txt` |
| 第5章 | 6:1-7:27 | 1 | `kad-07.txt` |
| 第6章 | 8:1-18 | 2 | `kad-08.txt` |
| 第7章 | 9:1-10:22 | 2 | `kad-09.txt` |
| 第8章 | 11:1-25 | 1 | `kad-11.txt` |
| 第9章 | 12:1-13:23 | 1 | `kad-12.txt` |
| 第10章 | 14:1-15:8 | 2 | `kad-14.txt` |
| 第11章 | 16:1-63 | 3 | `kad-16.txt` |
| 第12章 | 17:1-24 | 2 | `kad-17.txt` |
| 第13章 | 18:1-32 | 1 | `kad-18.txt` |
| 第14章 | 19:1-20:44 | 1 | `kad-20.txt` |
| 第15章 | 20:45-21:32 | 1 | `kad-21.txt` |
| 第16章 | 22:1-31 | 1 | `kad-22.txt` |
| 第17章 | 23:1-49 | 1 | `kad-23.txt` |
| 第18章 | 24:1-27 | 1 | `kad-24.txt` |
| 第19章 | 25:1-26:21 | 1 | `kad-26.txt` |
| 第20章 | 27:1-36 | 2 | `kad-27.txt` |
| 第21章 | 28:1-26 | 1 | `kad-28.txt` |
| 第22章 | 29:1-30:26 | 3 | `kad-29.txt` |
| 第23章 | 31:1-32:32 | 2 | `kad-31.txt`、`kad-32.txt` |
| 第24章 | 33:1-33 | 2 | `kad-33.txt` |
| 第25章 | 34:1-31 | 1 | `kad-34.txt` |
| 第26章 | 35:1-36:15 | 3 | `kad-35.txt` |
| 第27章 | 36:16-38 | 1 | `kad-36.txt` |
| 第28章 | 37:1-28 | 2 | `kad-37.txt` |
| 第29章 | 38:1-39:29 | 1 | `kad-38.txt` |
| 第30章 | 40:1-42:20 | 1 | `kad-40.txt` |
| 第31章 | 43:1-44:31 | 2 | `kad-43.txt` |
| 第32章 | 45:1-46:24 | 1 | `kad-45.txt` |
| 第33章 | 47:1-23 | 2 | `kad-47.txt` |
| 第34章 | 48:1-35 | 1 | `kad-48.txt` |

合計：34 章、52 條逐字引文。

---

## 五、司金納（J. Skinner），*Ezekiel*（*The Expositor's Bible*，1895）

司金納的《解經者聖經》以專題文章寫成，biblehub 把同一篇文章放在相鄰幾章的檔裏（例如 `expositors-12`／`-17`／`-19`），所以「含同文」的檔不止一個；本表列出前三個。

| 章 | 以西結書 | 逐字引文（條） | 核對來源檔（`.sources/`） |
|--------|----------------|----------------|------------------------------------------------------|
| 第1章 | 1:1-28 | 1 | `expositors-01.txt` |
| 第2章 | 2:1-3:15 | 1 | `expositors-02.txt`、`expositors-03.txt` |
| 第3章 | 3:16-27 | 1 | `expositors-02.txt`、`expositors-03.txt` |
| 第4章 | 4:1-5:17 | 1 | `expositors-04.txt`、`expositors-05.txt`、`expositors-06.txt`（另 1 檔含同文） |
| 第5章 | 6:1-7:27 | 1 | `expositors-04.txt`、`expositors-05.txt`、`expositors-06.txt`（另 1 檔含同文） |
| 第6章 | 8:1-18 | 3 | `expositors-08.txt`、`expositors-09.txt`、`expositors-10.txt`（另 1 檔含同文） |
| 第7章 | 9:1-10:22 | 1 | `expositors-08.txt`、`expositors-09.txt`、`expositors-10.txt`（另 1 檔含同文） |
| 第9章 | 12:1-13:23 | 1 | `expositors-12.txt`、`expositors-13.txt`、`expositors-14.txt` |
| 第10章 | 14:1-15:8 | 1 | `expositors-12.txt`、`expositors-13.txt`、`expositors-14.txt` |
| 第11章 | 16:1-63 | 1 | `expositors-16.txt` |
| 第12章 | 17:1-24 | 2 | `expositors-12.txt`、`expositors-17.txt`、`expositors-19.txt` |
| 第13章 | 18:1-32 | 1 | `expositors-18.txt` |
| 第14章 | 19:1-20:44 | 1 | `expositors-12.txt`、`expositors-17.txt`、`expositors-19.txt` |
| 第15章 | 20:45-21:32 | 1 | `expositors-21.txt` |
| 第16章 | 22:1-31 | 1 | `expositors-22.txt`、`expositors-24.txt` |
| 第17章 | 23:1-49 | 1 | `expositors-23.txt` |
| 第18章 | 24:1-27 | 2 | `expositors-22.txt`、`expositors-24.txt` |
| 第19章 | 25:1-26:21 | 1 | `expositors-26.txt`、`expositors-29.txt` |
| 第20章 | 27:1-36 | 1 | `expositors-27.txt`、`expositors-28.txt` |
| 第21章 | 28:1-26 | 1 | `expositors-27.txt`、`expositors-28.txt` |
| 第22章 | 29:1-30:26 | 1 | `expositors-29.txt`、`expositors-30.txt`、`expositors-31.txt`（另 1 檔含同文） |
| 第23章 | 31:1-32:32 | 1 | `expositors-29.txt`、`expositors-30.txt`、`expositors-31.txt`（另 1 檔含同文） |
| 第24章 | 33:1-33 | 1 | `expositors-33.txt` |
| 第25章 | 34:1-31 | 2 | `expositors-34.txt` |
| 第26章 | 35:1-36:15 | 1 | `expositors-35.txt`、`expositors-36.txt` |
| 第27章 | 36:16-38 | 1 | `expositors-35.txt`、`expositors-36.txt` |
| 第28章 | 37:1-28 | 1 | `expositors-37.txt` |
| 第29章 | 38:1-39:29 | 2 | `expositors-38.txt`、`expositors-39.txt` |
| 第30章 | 40:1-42:20 | 2 | `expositors-40.txt`、`expositors-41.txt`、`expositors-42.txt`（另 1 檔含同文） |
| 第31章 | 43:1-44:31 | 1 | `expositors-40.txt`、`expositors-41.txt`、`expositors-42.txt`（另 2 檔含同文） |
| 第32章 | 45:1-46:24 | 1 | `expositors-44.txt`、`expositors-45.txt`、`expositors-46.txt` |
| 第33章 | 47:1-23 | 1 | `expositors-47.txt`、`expositors-48.txt` |
| 第34章 | 48:1-35 | 2 | `expositors-47.txt`、`expositors-48.txt` |

合計：33 章、41 條逐字引文。

---

## 六、戴維森（A. B. Davidson），*The Cambridge Bible for Schools and Colleges: Ezekiel*（1892）

取自 biblehub.com 的 *Cambridge Bible for Schools and Colleges* 章頁全文。

| 章 | 以西結書 | 逐字引文（條） | 核對來源檔（`.sources/`） |
|--------|----------------|----------------|------------------------------------------------------|
| 第1章 | 1:1-28 | 1 | `cambridge-01.txt` |
| 第2章 | 2:1-3:15 | 1 | `cambridge-03.txt` |
| 第3章 | 3:16-27 | 1 | `cambridge-03.txt` |
| 第4章 | 4:1-5:17 | 2 | `cambridge-04.txt` |
| 第5章 | 6:1-7:27 | 2 | `cambridge-07.txt` |
| 第6章 | 8:1-18 | 1 | `cambridge-08.txt` |
| 第7章 | 9:1-10:22 | 1 | `cambridge-10.txt` |
| 第8章 | 11:1-25 | 1 | `cambridge-11.txt` |
| 第9章 | 12:1-13:23 | 2 | `cambridge-12.txt`、`cambridge-13.txt` |
| 第10章 | 14:1-15:8 | 1 | `cambridge-14.txt` |
| 第11章 | 16:1-63 | 1 | `cambridge-16.txt` |
| 第12章 | 17:1-24 | 1 | `cambridge-17.txt` |
| 第13章 | 18:1-32 | 1 | `cambridge-18.txt` |
| 第14章 | 19:1-20:44 | 1 | `cambridge-20.txt` |
| 第15章 | 20:45-21:32 | 1 | `cambridge-21.txt` |
| 第16章 | 22:1-31 | 2 | `cambridge-22.txt` |
| 第17章 | 23:1-49 | 2 | `cambridge-23.txt` |
| 第18章 | 24:1-27 | 1 | `cambridge-24.txt` |
| 第19章 | 25:1-26:21 | 1 | `cambridge-26.txt` |
| 第20章 | 27:1-36 | 2 | `cambridge-27.txt` |
| 第21章 | 28:1-26 | 1 | `cambridge-28.txt` |
| 第22章 | 29:1-30:26 | 1 | `cambridge-29.txt` |
| 第23章 | 31:1-32:32 | 2 | `cambridge-31.txt` |
| 第24章 | 33:1-33 | 2 | `cambridge-33.txt` |
| 第25章 | 34:1-31 | 1 | `cambridge-34.txt` |
| 第26章 | 35:1-36:15 | 1 | `cambridge-35.txt` |
| 第27章 | 36:16-38 | 2 | `cambridge-36.txt` |
| 第28章 | 37:1-28 | 1 | `cambridge-37.txt` |
| 第29章 | 38:1-39:29 | 2 | `cambridge-38.txt` |
| 第30章 | 40:1-42:20 | 1 | `cambridge-40.txt` |
| 第31章 | 43:1-44:31 | 1 | `cambridge-43.txt` |
| 第32章 | 45:1-46:24 | 1 | `cambridge-40.txt` |
| 第33章 | 47:1-23 | 1 | `cambridge-47.txt` |
| 第34章 | 48:1-35 | 1 | `cambridge-48.txt` |

合計：34 章、44 條逐字引文。

---

## 七、《講壇釋經》（*The Pulpit Commentary*）

`pulpit-NN.txt` 多為 biblehub 章頁上的逐節「摘錄」，部分在句子中間被截斷；本書只引完整出現在摘錄內、有頭有尾的句子。

| 章 | 以西結書 | 逐字引文（條） | 核對來源檔（`.sources/`） |
|--------|----------------|----------------|------------------------------------------------------|
| 第2章 | 2:1-3:15 | 1 | `pulpit-02.txt` |
| 第3章 | 3:16-27 | 1 | `pulpit-03.txt` |
| 第4章 | 4:1-5:17 | 1 | `pulpit-04.txt` |
| 第6章 | 8:1-18 | 1 | `pulpit-08.txt` |
| 第7章 | 9:1-10:22 | 1 | `pulpit-09.txt` |
| 第8章 | 11:1-25 | 1 | `pulpit-11.txt` |
| 第9章 | 12:1-13:23 | 1 | `pulpit-12.txt` |
| 第10章 | 14:1-15:8 | 1 | `pulpit-14.txt` |
| 第13章 | 18:1-32 | 1 | `pulpit-18.txt` |
| 第14章 | 19:1-20:44 | 1 | `pulpit-20.txt` |
| 第15章 | 20:45-21:32 | 2 | `pulpit-20.txt`、`pulpit-21.txt` |
| 第16章 | 22:1-31 | 1 | `pulpit-22.txt` |
| 第17章 | 23:1-49 | 1 | `pulpit-23.txt` |
| 第18章 | 24:1-27 | 3 | `pulpit-24.txt` |
| 第19章 | 25:1-26:21 | 1 | `pulpit-26.txt` |
| 第20章 | 27:1-36 | 1 | `pulpit-27.txt` |
| 第21章 | 28:1-26 | 1 | `pulpit-28.txt` |
| 第22章 | 29:1-30:26 | 1 | `pulpit-29.txt` |
| 第24章 | 33:1-33 | 1 | `pulpit-33.txt` |
| 第25章 | 34:1-31 | 1 | `pulpit-34.txt` |
| 第29章 | 38:1-39:29 | 1 | `pulpit-38.txt` |
| 第30章 | 40:1-42:20 | 1 | `pulpit-40.txt` |
| 第31章 | 43:1-44:31 | 1 | `pulpit-44.txt` |

合計：23 章、26 條逐字引文。

---

## 八、JFB（Jamieson, Fausset & Brown），*Commentary Critical and Explanatory*

取自 biblehub.com 的 JFB 章頁全文。

| 章 | 以西結書 | 逐字引文（條） | 核對來源檔（`.sources/`） |
|--------|----------------|----------------|------------------------------------------------------|
| 第2章 | 2:1-3:15 | 1 | `jfb-02.txt` |
| 第3章 | 3:16-27 | 1 | `jfb-03.txt` |
| 第4章 | 4:1-5:17 | 1 | `jfb-04.txt` |
| 第5章 | 6:1-7:27 | 1 | `jfb-07.txt` |
| 第6章 | 8:1-18 | 2 | `jfb-08.txt` |
| 第7章 | 9:1-10:22 | 1 | `jfb-09.txt` |
| 第8章 | 11:1-25 | 1 | `jfb-11.txt` |
| 第11章 | 16:1-63 | 1 | `jfb-16.txt` |
| 第15章 | 20:45-21:32 | 1 | `jfb-20.txt` |
| 第16章 | 22:1-31 | 1 | `jfb-22.txt` |
| 第17章 | 23:1-49 | 1 | `jfb-23.txt` |
| 第18章 | 24:1-27 | 1 | `jfb-24.txt` |
| 第19章 | 25:1-26:21 | 2 | `jfb-26.txt` |
| 第21章 | 28:1-26 | 1 | `jfb-28.txt` |
| 第23章 | 31:1-32:32 | 1 | `jfb-31.txt` |
| 第24章 | 33:1-33 | 1 | `jfb-33.txt` |
| 第25章 | 34:1-31 | 1 | `jfb-34.txt` |
| 第26章 | 35:1-36:15 | 1 | `jfb-36.txt` |
| 第27章 | 36:16-38 | 2 | `jfb-36.txt` |
| 第28章 | 37:1-28 | 1 | `jfb-37.txt` |
| 第29章 | 38:1-39:29 | 1 | `jfb-38.txt` |
| 第30章 | 40:1-42:20 | 1 | `jfb-41.txt` |
| 第31章 | 43:1-44:31 | 2 | `jfb-43.txt` |
| 第32章 | 45:1-46:24 | 2 | `jfb-40.txt`、`jfb-44.txt` |
| 第33章 | 47:1-23 | 1 | `jfb-47.txt` |

合計：25 章、30 條逐字引文。

---

## 九、吉爾（John Gill），*Exposition of the Entire Bible*

`gill-NN.txt` 為 biblehub 章頁上的逐節摘錄，部分在句子中間被截斷；本書只引完整的句子，多數處只以釋義方式提及並註明檔名。

| 章 | 以西結書 | 逐字引文（條） | 核對來源檔（`.sources/`） |
|--------|----------------|----------------|------------------------------------------------------|
| 第4章 | 4:1-5:17 | 1 | `gill-04.txt` |
| 第29章 | 38:1-39:29 | 1 | `gill-38.txt` |
| 第30章 | 40:1-42:20 | 1 | `gill-40.txt` |
| 第32章 | 45:1-46:24 | 1 | `gill-45.txt` |

合計：4 章、4 條逐字引文。

---

## 十、摩根（G. Campbell Morgan），*The Analyzed Bible*，以西結書分段大綱

《分析聖經》（archive.org `bwb_T3-BNU-740` 的 OCR）是**分段大綱與短評，不是逐章講章**；檔內有頁碼與頁眉夾雜。本書只引描述本章的短句，標「分析聖經·以西結書」，不寫成論某節。

| 章 | 以西結書 | 逐字引文（條） | 核對來源檔（`.sources/`） |
|--------|----------------|----------------|------------------------------------------------------|
| 第2章 | 2:1-3:15 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第3章 | 3:16-27 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第4章 | 4:1-5:17 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第5章 | 6:1-7:27 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第7章 | 9:1-10:22 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第12章 | 17:1-24 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第13章 | 18:1-32 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第15章 | 20:45-21:32 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第16章 | 22:1-31 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第17章 | 23:1-49 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第18章 | 24:1-27 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第19章 | 25:1-26:21 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第23章 | 31:1-32:32 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第24章 | 33:1-33 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第25章 | 34:1-31 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第26章 | 35:1-36:15 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第27章 | 36:16-38 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第28章 | 37:1-28 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第29章 | 38:1-39:29 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第30章 | 40:1-42:20 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |
| 第31章 | 43:1-44:31 | 1 | `morgan-analyzed-bible-ezekiel.txt`、`morgan-job-malachi.txt` |

合計：21 章、21 條逐字引文。

---

## 十一、麥克阿瑟——本書沒有逐字引文

麥克阿瑟沒有以西結書的逐節講道系列（gty.org 的站點地圖與 Monergism 的麥克阿瑟系列清單都查無）。本書沒有任何一條麥克阿瑟的逐字引文，也不以他人冒充，更不憑記憶引他。

---

## 十二、老弟兄——本書沒有第一手引文

本項目沒有老弟兄講以西結書的第一手錄影或筆記。各章「老弟兄查經」一節是依 ask-elder-wong 方法所作的**方法性撮述**，不加引號、不宣稱是逐字語錄；加引號的老弟兄語句只有 `.claude/skills/ask-elder-wong/references/voice.md` 白名單內的句子。倉庫中老弟兄約翰福音材料裏確實出現的以西結連結，各處已註明路徑與行數，並標示為倉庫材料，而不是他講過以西結書。

---

## 十三、配詩的出處

每章一節配詩，歌詞由協助編輯的 AI 代理從印本或公有領域歌詞網站逐字抓取（一節）；中譯由撰寫各章的 AI 代理所作。作者與年份依來源所印，因此與一般通行的說法偶有出入（如 Kelly 1804、Watts 1709、Bernard of Morlaix），以下表為準。

- 第1章 · Holy, Holy, Holy；Reginald Heber, 1826。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/h/o/l/y/h/holyholy.htm>
- 第2章 · Break Thou the Bread of Life；Mary Lathbury, 1877, and Alexander Groves, 1913 (Cyber credit; stanza 1 is Lathbury)。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/b/t/t/b/bttblife.htm>
- 第3章 · Watchman, Tell Us of the Night；John Bowring, 1825。取自 The Army and Navy Hymnal (1920), ed. Henry Augustine Smith, via English Wikisource (rev 13830100)：<https://en.wikisource.org/wiki/The_Army_and_Navy_Hymnal/Hymns/Watchman,_Tell_Us_of_the_Night>
- 第4章 · Stricken, Smitten, and Afflicted；Thomas Kelly, 1804。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/s/t/r/i/stricken.htm>
- 第5章 · Dies Iræ (Irons translation)；Tommaso da Celano, tr. William Josiah Irons, 1849。取自 The Seven Great Hymns of the Mediaeval Church, ed. Charles Cooper Nott (1902), ch. VII "Dr. Irons", via English Wikisource (rev 14350882)：<https://en.wikisource.org/wiki/The_seven_great_hymns_of_the_mediaeval_church/Dies_Ir%C3%A6/Irons>
- 第6章 · Come, Thou Fount of Every Blessing；Robert Robinson, 1758。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/c/o/m/e/t/comethou.htm>
- 第7章 · Rock of Ages；Augustus Toplady, 1776。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/r/o/c/k/rockages.htm>
- 第8章 · O for a Heart to Praise My God；Charles Wesley, 1742。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/o/f/o/r/oforhear.htm>
- 第9章 · Be Still, My Soul；Katharina von Schlegel, 1752; tr. Jane L. Borthwick, 1855 (Hymns from the Land of Luther)。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/b/e/s/t/bestmyso.htm>
- 第10章 · Dear Lord and Father of Mankind (from "The Brewing of Soma")；John Greenleaf Whittier, 1872。取自 The Complete Poetical Works of John Greenleaf Whittier, "The Brewing of Soma", via English Wikisource (rev 13881891)：<https://en.wikisource.org/wiki/The_Complete_Poetical_Works_of_John_Greenleaf_Whittier/The_Brewing_of_Soma>
- 第11章 · Jesus, Lover of My Soul；Charles Wesley, 1740。取自 The Army and Navy Hymnal (1920), ed. Henry Augustine Smith, via English Wikisource (rev 13800152)：<https://en.wikisource.org/wiki/The_Army_and_Navy_Hymnal/Hymns/Jesus,_Lover_of_My_Soul>
- 第12章 · O God, Our Help in Ages Past；Isaac Watts, 1719。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/o/g/o/h/ogohiap.htm>
- 第13章 · Just as I Am, Without One Plea；Charlotte Elliott, 1835。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/j/u/s/t/justasam.htm>
- 第14章 · O Love That Wilt Not Let Me Go；George Matheson, 1882。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/o/l/t/w/oltwnlmg.htm>
- 第15章 · Judge Eternal, Throned in Splendor；Henry Holland, 1902。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/j/u/d/g/judgeter.htm>
- 第16章 · Where Cross the Crowded Ways of Life；Frank Mason North, 1903。取自 The Army and Navy Hymnal (1920), ed. Henry Augustine Smith, via English Wikisource (rev 13800286)：<https://en.wikisource.org/wiki/The_Army_and_Navy_Hymnal/Hymns/Where_Cross_the_Crowded_Ways_of_Life>
- 第17章 · Come, Ye Sinners, Poor and Needy；Joseph Hart, 1759。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/c/o/m/e/y/comeyspn.htm>
- 第18章 · Abide with Me (Lyte)；Henry Lyte, 1847。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/a/b/i/d/abidewme.htm>
- 第19章 · Eternal Father, Strong to Save；William Whiting, 1860。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/e/t/e/r/eternalf.htm>
- 第20章 · Jesus, Savior, Pilot Me；Edward Hopper, 1871。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/j/s/p/i/jspilotm.htm>
- 第21章 · A Mighty Fortress Is Our God；Martin Luther, 1529; tr. Frederic H. Hedge, 1853。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/m/i/g/h/mightyfo.htm>
- 第22章 · Guide Me, O Thou Great Jehovah；William Williams, 1745; tr. Peter Williams, 1771。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/g/u/i/d/guideme.htm>
- 第23章 · My Faith Looks Up to Thee；Ray Palmer, 1830。取自 The Army and Navy Hymnal (1920), ed. Henry Augustine Smith, via English Wikisource (rev 13800182)：<https://en.wikisource.org/wiki/The_Army_and_Navy_Hymnal/Hymns/My_Faith_Looks_Up_to_Thee>
- 第24章 · Rescue the Perishing；Fanny Crosby, 1869。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/r/e/s/c/rescuetp.htm>
- 第25章 · The King of Love My Shepherd Is；Henry Baker, 1868。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/k/i/n/g/kinglove.htm>
- 第26章 · I to the Hills Will Lift Mine Eyes (Psalm 121)；Scottish Psalter, 1650。取自 1650 Scottish Psalter, Psalm 121, SermonAudio Hymnal & Psalter：<https://web.sermonaudio.com/psalter/psalm121>
- 第27章 · Breathe on Me, Breath of God；Edwin Hatch, 1878。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/b/o/m/b/bombog.htm>
- 第28章 · Come, Holy Spirit, Heavenly Dove；Isaac Watts, 1709 (Cyber; list said 1707)。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/c/o/m/e/h/comehshd.htm>
- 第29章 · Fight the Good Fight with All Thy Might；John Monsell, 1863。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/f/i/g/h/fightthe.htm>
- 第30章 · Glorious Things of Thee Are Spoken；John Newton, 1779。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/g/l/o/r/i/glorious.htm>
- 第31章 · Come, Thou Long Expected Jesus；Charles Wesley, 1745。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/c/o/m/t/comtlong.htm>
- 第32章 · Crown Him with Many Crowns；Matthew Bridges, 1852, and Godfrey Thring, 1874 (Cyber credit; stanza 1 is Bridges)。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/c/r/o/w/crownhim.htm>
- 第33章 · Shall We Gather at the River?；Robert Lowry, 1864。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/s/h/a/l/shalwega.htm>
- 第34章 · Jerusalem the Golden；Bernard of Morlaix, 1146; tr. John M. Neale, 1858 (The Rhythm of Bernard of Morlaix)。取自 The Cyber Hymnal (hymntime.com), public-domain hymn text archive：<http://www.hymntime.com/tch/htm/j/e/r/u/jerugold.htm>

---

## 十四、教父段落清單

- `01-irenaeus-ah-3-11-8.txt` · Irenaeus, Against Heresies 3.11.8（以西結書 1:5-10 (four-faced cherubim; Ezekiel not named in the passage)）：<https://www.newadvent.org/fathers/0103311.htm>
- `02-clement-1cor-8.txt` · Clement of Rome, First Epistle to the Corinthians, ch. 8（以西結書 33:11; 18:30）：<https://www.newadvent.org/fathers/1010.htm>
- `03-barnabas-6.txt` · Barnabas, Epistle of Barnabas, ch. 6（以西結書 11:19; 36:26）：<https://www.newadvent.org/fathers/0124.htm>
- `04-barnabas-11.txt` · Barnabas, Epistle of Barnabas, ch. 11（以西結書 47:1-12）：<https://www.newadvent.org/fathers/0124.htm>
- `05-justin-dial-21.txt` · Justin Martyr, Dialogue with Trypho, ch. 21（以西結書 20:19-26）：<https://www.newadvent.org/fathers/01282.htm>
- `06-justin-dial-47.txt` · Justin Martyr, Dialogue with Trypho, ch. 47（以西結書 18:21-24; 33:12-16 (repentance, as Ezekiel tells)）：<https://www.newadvent.org/fathers/01283.htm>
- `07-justin-dial-82.txt` · Justin Martyr, Dialogue with Trypho, ch. 82（以西結書 3:17-21; 33:7-9 (watchman)）：<https://www.newadvent.org/fathers/01286.htm>
- `08-jerome-ep53-8-obscurity.txt` · Jerome, Letter 53 (to Paulinus), section 8（以西結書 1; 40-48 (beginning and end of the book)）：<https://www.newadvent.org/fathers/3001053.htm>
- `09-jerome-ep53-9-cherubim.txt` · Jerome, Letter 53 (to Paulinus), section 9（以西結書 1:7-20 (cherubim, wheels)）：<https://www.newadvent.org/fathers/3001053.htm>
- `10-cyril-cat3-16.txt` · Cyril of Jerusalem, Catechetical Lecture 3 (On Baptism), section 15-16（以西結書 36:25）：<https://www.newadvent.org/fathers/310103.htm>
- `11-cyril-cat16-14.txt` · Cyril of Jerusalem, Catechetical Lecture 16 (On the Holy Ghost), section 14（以西結書 11:5）：<https://www.newadvent.org/fathers/310116.htm>
- `12-cyril-cat18-1.txt` · Cyril of Jerusalem, Catechetical Lecture 18 (On the Resurrection), heading and section 1（以西結書 37:1）：<https://www.newadvent.org/fathers/310118.htm>
- `13-cyril-cat18-15.txt` · Cyril of Jerusalem, Catechetical Lecture 18 (On the Resurrection), section 15（以西結書 37:12）：<https://www.newadvent.org/fathers/310118.htm>
- `14-tertullian-resurrection-30a.txt` · Tertullian, On the Resurrection of the Flesh, ch. 30 (first part)（以西結書 37:1-14）：<https://www.newadvent.org/fathers/0316.htm>
- `15-tertullian-resurrection-30b.txt` · Tertullian, On the Resurrection of the Flesh, ch. 30 (second part)（以西結書 37:1-14）：<https://www.newadvent.org/fathers/0316.htm>
- `16-tertullian-marcion-2-ezek28a.txt` · Tertullian, Against Marcion, Book 2, ch. 10 (first part)（以西結書 28:11-19）：<https://www.newadvent.org/fathers/03122.htm>
- `17-tertullian-marcion-2-ezek28b.txt` · Tertullian, Against Marcion, Book 2, ch. 10 (second part)（以西結書 28:15-19）：<https://www.newadvent.org/fathers/03122.htm>
- `18-tertullian-marcion-3-22-tau.txt` · Tertullian, Against Marcion, Book 3, ch. 22（以西結書 9:4）：<https://www.newadvent.org/fathers/03123.htm>
- `19-tertullian-marcion-3-24-jerusalem.txt` · Tertullian, Against Marcion, Book 3, ch. 24（以西結書 48:30-35）：<https://www.newadvent.org/fathers/03123.htm>
- `20-origen-principiis-1-5-4a.txt` · Origen, De Principiis, Book 1, ch. 5, section 4 (first part)（以西結書 28:11-19）：<https://www.newadvent.org/fathers/04121.htm>
- `21-origen-principiis-1-5-4b.txt` · Origen, De Principiis, Book 1, ch. 5, section 4 (second part)（以西結書 28:11-19）：<https://www.newadvent.org/fathers/04121.htm>
- `22-origen-principiis-3-1-15a.txt` · Origen, De Principiis, Book 3, ch. 1, section 15 (first part)（以西結書 11:19-20; 36:26-27）：<https://www.newadvent.org/fathers/04123.htm>
- `23-origen-principiis-3-1-15b.txt` · Origen, De Principiis, Book 3, ch. 1, section 15 (second part)（以西結書 11:19-20; 36:26-27）：<https://www.newadvent.org/fathers/04123.htm>
- `24-origen-principiis-4-1-egypt-tyre.txt` · Origen, De Principiis, Book 4, section 22 (numbering as printed on the page)（以西結書 26-32 (oracles on Tyre and Egypt)）：<https://www.newadvent.org/fathers/04124.htm>
- `25-origen-celsus-1-43.txt` · Origen, Against Celsus, Book 1, ch. 43（以西結書 1:1）：<https://www.newadvent.org/fathers/04161.htm>
- `26-origen-celsus-6-6-roll.txt` · Origen, Against Celsus, Book 6, ch. 6（以西結書 2:8-3:3）：<https://www.newadvent.org/fathers/04166.htm>
- `27-origen-celsus-6-23-gates.txt` · Origen, Against Celsus, Book 6, ch. 23（以西結書 40-48 (the gates)）：<https://www.newadvent.org/fathers/04166.htm>
- `28-origen-celsus-8-40-children.txt` · Origen, Against Celsus, Book 8, ch. 40（以西結書 18:2-4）：<https://www.newadvent.org/fathers/04168.htm>
- `29-augustine-gracefreewill-29.txt` · Augustine, On Grace and Free Will, ch. 29（以西結書 11:19-20）：<https://www.newadvent.org/fathers/1510.htm>
- `30-augustine-gracefreewill-30.txt` · Augustine, On Grace and Free Will, ch. 30（以西結書 36:22-27）：<https://www.newadvent.org/fathers/1510.htm>
- `31-augustine-gracefreewill-31.txt` · Augustine, On Grace and Free Will, ch. 31（以西結書 18:31-32; 36:26）：<https://www.newadvent.org/fathers/1510.htm>
- `32-augustine-gracefreewill-32.txt` · Augustine, On Grace and Free Will, ch. 32（以西結書 36:26-27）：<https://www.newadvent.org/fathers/1510.htm>
- `33-augustine-cog-22-30.txt` · Augustine, City of God, Book 22, ch. 30（以西結書 20:12）：<https://www.newadvent.org/fathers/120122.htm>
- `34-gregory-nazianzen-or2-64-65.txt` · Gregory Nazianzen, Oration 2 (In Defence of His Flight), sections 64-65（以西結書 33:2; 14:5; 22）：<https://www.newadvent.org/fathers/310202.htm>
- `35-gregory-nazianzen-or2-66.txt` · Gregory Nazianzen, Oration 2 (In Defence of His Flight), section 66（以西結書 34:2-16）：<https://www.newadvent.org/fathers/310202.htm>
- `36-gregory-nazianzen-or2-112.txt` · Gregory Nazianzen, Oration 2 (In Defence of His Flight), section 112（以西結書 3:18）：<https://www.newadvent.org/fathers/310202.htm>
- `37-chrysostom-priesthood-6-1.txt` · John Chrysostom, On the Priesthood, Book 6, ch. 1（以西結書 33:2-6）：<https://www.newadvent.org/fathers/19226.htm>
- `38-chrysostom-priesthood-6-11.txt` · John Chrysostom, On the Priesthood, Book 6, ch. 11（以西結書 34:17）：<https://www.newadvent.org/fathers/19226.htm>
- `39-cyprian-ep2.txt` · Cyprian (Roman clergy letter among his epistles), Epistle 2 (From the Roman Clergy to the Carthaginian Clergy), section 1（以西結書 34:3-4）：<https://www.newadvent.org/fathers/050602.htm>
- `40-cyprian-ep51-27.txt` · Cyprian, Epistle 51 (To Antonianus), section 27（以西結書 18:20）：<https://www.newadvent.org/fathers/050651.htm>
- `41-cyprian-lapsed-36.txt` · Cyprian, Treatise 3 (On the Lapsed), section 36（以西結書 33:11）：<https://www.newadvent.org/fathers/050703.htm>
- `42-cyprian-demetrian-22.txt` · Cyprian, Treatise 5 (To Demetrian), section 22（以西結書 9:4-6）：<https://www.newadvent.org/fathers/050705.htm>

---

## 十五、聖經版本與核對方式

- **中文：**和合本（1919）。以 fhl（bible.fhl.net，`unv`）為底，專有名詞與字形在 ai-eden 與 cnbible 兩者一致處從舊形（推羅、撒瑪利亞、利巴嫩、大馬色、毗、呂彼亞、亞拉伯、約但、燒燬、火燄、可作）；經文區由 `scripts/gen-ezekiel-scripture.py` 自來源檔印出，章內經文與 `.sources/units/` 逐字一致，由 `.sources/check_chapter.py` 逐章核對。
- **一個刻意的字形例外：**47:3-5 的「蹚」字。ai-eden 與 cnbible 的和合本欄都作一個罕見字形，本書印刷字體沒有它，故取 fhl 的「蹚」。
- **三節來源缺陷：**16:57、18:11、39:27 三節，和合本在 fhl、ai-eden、cnbible 三個來源裏都只有一個字母 `a`，內容已併入上一節；經文區在這三節印出一行說明，不自行補寫和合本字句。NASB 這三節俱全。
- **英文：**NASB 1995。取自 biblehub.com 的 NASB 章頁，因為 ai-eden 的 NASB 檔在兩處與 1995 版不符（11:3 為 1977 措辭，13:15 字串錯亂）。
- **希伯來文：**Sefaria 的 JPS 希伯來底本（Miqra according to the Masorah），去掉讀經符號、保留母音；原文研讀表的字形須能在 `.sources/hebrew/ezekiel-he.tsv` 中找到。希伯來文 21:1-37 的節號與和合本不同（希伯來 21:1-5 = 和合本 20:45-49），表內以和合本節號為準。
- **跨卷經文：**一律由 `.sources/xref.py`（ai-eden，有快取）逐節印出，只做「裡」→「裏」一項改動。
- **注疏引文：**每條英文引文都是 `.sources/commentary/` 或 `.sources/fathers/` 內檔案的逐字子字串（忽略大小寫與標點），由 `.sources/check_quotes.py` 逐條核對；同一句全書只引一次，由 `QUOTE-LEDGER.tsv` 與全書掃描雙重把關。

---

## 十六、機器核對現況

- 逐章驗證：`.sources/check_chapter.py` 對 34 章的結果為 0 errors（YAML、十一節順序、經文區、引文子字串、座標與鑰詞、「你看見…了嗎」等）。**通過它只證明形式正確，不證明內容為真。**
- 全書掃描：同一句注疏跨章重複者 0 處（對 `> "…"` 引文的前 60 個字元逐條比對）。
- 本表的條數由腳本自各章讀出；分類無法歸屬者 0 條，在來源檔中找不到者 0 條。
- 歷代注疏中文譯文是編者所譯，沒有另行校對。
- 配詩中，第 4、8、9、15、17、26、27、28 章只有單一來源可對；第 31 章另有一頁底本不明的同文；其餘已與第二來源比對。

---

## 十七、仍未完成

以下各項是誠實的缺口，不是已完成事項：

1. 已執行一輪獨立校對：九位沒有看過本書的 AI 校對者各自向原始來源重新取證，共提出 A 級（錯誤）24 條、B 級（無法查證或過度斷言）76 條、C 級（錯字、文風等）116 條；修訂者逐條向原始來源重新查證後才修改，個別條目經查證不成立者未改。**尚未有人類校對者通讀全書**，這是仍未完成的最重要一項。
2. 已做一輪精簡（各章約減 12–27%，全書約 19%，刪除重複的論述與部分重複的注疏引文，各章仍保留至少 8 條逐字引文，個別章原本即不足）；精簡後的文字未再經獨立校對，仍有重複之處未處理。
3. 配詩第 16 章第四行「Son of man」前是否有「O」，兩個來源不一致，待查 1903 年原版。
4. 40–48 章的解釋傳統（字面、象徵、基督裏應驗）、28:11-19 的所指、38–39 章的歌革，本書一律並陳而不定案；這是刻意的，需要作者決定的只是是否在日後的版本加上本書自己的立場。
5. 老弟兄對以西結書沒有第一手材料；「老弟兄查經」各節是方法性撮述。

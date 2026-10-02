---
title: 約翰三書研讀
subtitle: 3 John Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---

# 附錄：引用出處總表 (Appendix: References)

本附錄記錄全書九章「歷代注疏」與卷首卷末各章所引用的全部來源，並如實說明本書的資料基礎。每一條加引號的英文引句，都已用 `scripts/verify-citations.py` 與下列下載的原文逐字比對；講道引句另以 `scripts/verify-sermon-quotes.py` 對照所屬講章逐字稿。原文抽段存於本書資料夾 `books/bible/john3/.sources/`（附 README 列出網址）。

---

## 一、資料基礎的誠實說明

**老弟兄**：本項目沒有老弟兄講約翰三書的第一手材料。以「約翰三書」「丟特腓」「低米丟」檢索全部書稿、每日筆記與文件，只找到舊稿《約翰書信》第七章（`books/bible/johannine-epistles/07-3john.md`），其頁尾雖寫「整合三方資源：黃長老查經教導……」，正文卻沒有任何老弟兄的教導內容。本書各章「老弟兄查經」一節因此全部是**方法性撮述**，沒有一句加引號歸給老弟兄。

**加爾文**：加爾文《大公書信注釋》（CCEL calcom45）注了約翰一書，沒有注約翰二、三書；全文檢索不見 Gaius、Diotrephes。本書不引加爾文論約翰三書之語。

**教父**：約翰三書沒有留下教父的逐節注釋。本書只在〈約翰三書概覽〉引用優西比烏與耶柔米論正典的兩段話（見第七節）。

**舊稿的引文**：上述舊稿第七章曾以中文列出耶柔米、加爾文、麥克阿瑟、司托德四條「引言」，均無原文、無可定位的出處；其中加爾文一條所歸屬的注釋並不存在。本書一條也沒有沿用。

---

## 二、聖經版本與核對方式

- **中文**：和合本（CUV），以 `https://www.ai-eden.com/api/bible/3-john/1?t=CUV` 為底本，逐節以 `bible.fhl.net`（和合本 unv）覆核。兩者差異：ai-eden 作「兄弟阿」，fhl 作「兄弟啊」——本書依全系列體例作「啊」；ai-eden 把第 14、15 節併在一處，本書依 fhl 分節。第 8 節「做工」與詩 15:2「做事」經 fhl 確認和合本本作「做」。全書正文引用的每一處交叉經文，均在寫作時用 fhl 和合本重新取得原句，並以 `scripts/verify-prose-citations.py` 機器覆核（99 處，0 不符）。
- **English**：NASB 1995，ai-eden 同一 API 取得，以 `https://biblehub.com/nasb/3_john/1.htm`（頁尾標明 NASB 1995 版權）逐節核對一致。
- **希臘文**：SBL Greek New Testament，MorphGNT 詞法標記版（`github.com/morphgnt/sblgnt`）。書中一切希臘字形與出現次數（如 ἀλήθεια 六次、φιλοπρωτεύω 與 πρωτεύω 新約各一次、προπέμπω 新約九次、κατ᾽ ὄνομα 新約兩次、新約只有約翰三書不見 Ἰησοῦς 與 Χριστός）均以程式逐字檢索全部 27 卷得出，不憑記憶。

---

## 三、引文核對記錄——雷諾茲（亨利《聖經全註》續）

**來源**：Matthew Henry, *Commentary on the Whole Bible*, vol. VI (Acts to Revelation)，CCEL 純文字版 `https://ccel.org/ccel/h/henry/mhc6/cache/mhc6.txt`。約翰三書部分自「OF THE THIRD EPISTLE OF JOHN」標題起，至「Jude」標題止。

**作者說明**：馬太·亨利寫完新約歷史書後去世；該卷序言所附續作者名單（引自 J. B. Williams 所著亨利傳記）記載：「1, 2, and 3 John — Mr. John Reynolds, of Shrewsbury」。本書因此一律標明「John Reynolds of Shrewsbury, in Matthew Henry」。

**逐字引用的章**：

| 章 | 經文 | 引句數 |
|----------------------------|----------------------------|----------------------------|
| 第1章 | 1-2 | 3 |
| 第2章 | 3-4 | 2 |
| 第3章 | 5-6 | 2 |
| 第4章 | 7-8 | 2 |
| 第5章 | 9 | 2 |
| 第6章 | 10 | 1 |
| 第7章 | 11 | 2 |
| 第8章 | 12 | 1 |
| 第9章 | 13-15 | 2 |

---

## 四、引文核對記錄——韋斯科特

**來源**：B. F. Westcott, *The Epistles of St John: The Greek Text with Notes and Essays*, 3rd ed. (Macmillan, 1892)，archive.org 識別碼 `cu31924074296629`（康乃爾大學藏本 OCR）。約翰三書注釋部分自「ΙΩΑΝΝΟΥ Γ」標題起，至其後「The Two Empires」附論前止；另抽取導論「The Second and Third Epistles」一節。另有兩份掃描本（`epistlesofstjohn00westuoft`、`TheEpistlesOfStJohnTheGreekText`）OCR 為希臘字型亂碼，未採用。

**逐字引用的章**（〈歷代注疏〉設有韋斯科特一節者）：第2章、第3章、第4章、第6章、第7章、第8章、第9章。另在〈好為首的丟特腓〉一章的〈背景〉小節引用一句（論丟特腓並無錯誤見解）。

**說明**：第 4 章引用的是韋斯科特為第 7 節所寫的附註〈神的名〉（Additional Note on v. 7, "The Divine Name"）。第 8 章原擬引用「低米丟可能是送信人」一句，因掃描本把 "It is" 黏成 "Itis"，改引同段另一句完整的話，該論點則改為不加引號的綜述。

---

## 五、引文核對記錄——普盧默

**來源**：A. Plummer, *The Epistles of S. John, with Notes, Introduction and Appendices* (Cambridge Bible for Schools and Colleges, 1887)，archive.org 識別碼 `epistlessjohnwi00plumgoog`（Google 掃描本 OCR）。抽取約翰三書注釋（pp. 186-195）與導論第四章「The Third Epistle」（pp. 59-61）。

**逐字引用的章**（〈歷代注疏〉設有普盧默一節者）：第1章、第3章、第4章、第5章、第6章、第7章、第9章。另在〈真理也給他作見證〉一章的〈原文研讀〉小節引用一句（論「真理本身作見證」）；第 1、3、9 章在〈背景〉或〈原文研讀〉另有引句。

**說明**：第 1 章原擬引用普盧默論「above all things」的一句，因掃描本把 "prosperity" 印成 "ipiosgenty"，改引同一注釋的結論句。〈約翰三書在正典中的位置〉一章所引「亞歷山大主教」論異端與分裂的話，是普盧默在導論中的引文，本書標明為「普盧默引亞歷山大」。

---

## 六、引文核對記錄——摩根

**來源**：G. Campbell Morgan, *Living Messages of the Books of the Bible* (Fleming H. Revell, 1912)，archive.org 識別碼 `livingmessagesof0000gcam_o4l5`，「The Message of the Letters of John」一篇（pp. 177-190）。摩根沒有逐節注釋約翰三書，此篇是他對約翰三封書信的整體信息分析，其中直接論到二書與三書的只有幾句。

**逐字引用的章**：第2章（p. 180）。另在卷首〈約翰三書在正典中的位置〉引用一句（p. 177）。

要旨綜述的章：無。第 1、3-9 章不設摩根一節，因摩根原著沒有論及這些經文的材料，本書不以他人的話填補。

---

## 七、引文核對記錄——麥克阿瑟

**來源**：John MacArthur 講約翰三書的兩篇講道，gty.org 逐字稿（由 gty.org `sitemap.xml` 確認約翰三書只有這兩篇）：

- "Friends and Foes in the Church, Part 1"，sermon 64-1，`https://www.gty.org/sermons/64-1/friends-and-foes-in-the-church-part-1`（講 1-8 節）
- "Friends and Foes in the Church, Part 2"，sermon 64-2，`https://www.gty.org/sermons/64-2/friends-and-foes-in-the-church-part-2`（講 9-15 節）

**逐字引用的章**：第1章、第2章、第3章、第4章、第5章、第6章、第7章、第8章、第9章。

**說明**：第 1-4 章出自 sermon 64-1，第 5-9 章出自 sermon 64-2。第 7 章所引麥克阿瑟論「許多教會被丟特腓式人物把持，他們其實不是基督徒」一句，判斷甚重，本書在引文後註明：約翰本人在第 11 節說的是原則，並未直接宣判丟特腓沒有得救。64-1 中另有一段論及某神學院與伊斯蘭的時事評論，與經文解釋無直接關係，本書未引。

---

## 八、其他引用

- **優西比烏**，*Church History* III.25.3，McGiffert 英譯（NPNF² vol. 1），`https://www.newadvent.org/fathers/250103.htm`——〈約翰三書概覽〉。
- **耶柔米**，*De Viris Illustribus* 9，Richardson 英譯（NPNF² vol. 3），`https://www.newadvent.org/fathers/2708.htm`——〈約翰三書概覽〉。
- **聖詩**：九首配詩全部取自 Wikisource 所錄的有年代印本（八首出自 *The Army and Navy Hymnal*, ed. H. A. Smith, 1920；〈Walk in the Light〉出自 J. C. Hutchieson 編 *Fugitive Poetry, 1600–1878*），均屬公有領域；中譯為編者所譯。〈Blest Be the Tie That Binds〉所錄印本第一、三節有 "Christan""mutal" 兩處排印錯字，本書所引第四、五節不受影響。原擬採用的 Bonar、Elliott、Chisholm、Breck、Wilson 五首，因未能取得可核對的印本全文而改換。

---

## 九、機器逐字核對現況（2026-10-01）

| 檢查 | 結果 |
|------------------------------------------|------------------------------------------|
| `verify-citations.py`（全部英文引句，對照五種來源） | 九章 62 條：逐字相符 59、OCR 正規化後相符 3、DRIFT 0、MISS 0 |
| `verify-sermon-quotes.py`（麥克阿瑟講道引句，對照所屬講章） | 10 條全部在所屬講章中找到 |
| `verify-prose-citations.py`（正文中加引號並附出處的和合本經文） | 99 處，0 不符 |
| `check-prose-scripture-quotes.py`（正文中未附他卷出處的經文引句） | 0 不符 |
| `lint-scripture-text.py`（和合本異體字） | 2 處「做」待查，均經 fhl 確認和合本本作「做」 |

卷首卷末各章的英文引句（優西比烏、耶柔米、摩根、普盧默引亞歷山大）另行核對，結果見本書評分表（`docs/scores/john3-2026-10-01.md`）。

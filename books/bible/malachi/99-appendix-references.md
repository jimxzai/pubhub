---
title: 瑪拉基書研讀
subtitle: The Book of Malachi Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---

# 附錄：引用出處總表 (Appendix: References)

本附錄是全書「不杜撰一句經文，不編造一條注疏」這句話的帳目。凡書中加引號並附英文原文的引句，都列在這裏，註明出處與核對方式；讀者可以按圖索驥，自己查證。核對所用的原始文本，存放在 `books/bible/malachi/sources/`（各檔的取得方式與版本見該目錄的 `BOOK-SPEC.md` 與各檔本身）。另有兩類核對用的網路資料沒有存檔：gty.org 網站地圖已存檔（`gty-sitemap-2026-10-31.xml`）；另一類沒有存檔的是各章聖詩部分的 Wikisource 頁面（已存 JSON 回傳檔於 `sources/hymns/`）；讀者需要時請自行重新下載。

**第一項誠實聲明**：倉庫中老弟兄的查經筆記，**沒有任何一則以瑪拉基書為題**。全書「老弟兄查經」各節，是把他一貫的查經方法——提問式帶領、精義一句話、全經連線、每次查經末了問「你看見耶穌了嗎？」——應用在瑪拉基書的經文上，不是任何歷史查經記錄的複現。書中加引號歸給老弟兄的話，只有前言與少數幾章引用的幾句語錄（「你研讀聖經，卻沒有看見耶穌——那本書等於白讀了。」「字句叫人死，精義叫人活。」「我們照著神的意思去做，神就負責；照著我的意思去做，我要負責。」「有什麼讓你心裏有感動？不是你想出來的，是聖靈光照的。」「看弟兄們怎麼讀報紙（看股票），就知道他們怎麼讀聖經了。」），都出自 `.claude/skills/ask-elder-wong/references/voice.md` 的語錄白名單（「心裡」依全庫體例寫作「心裏」）。

**第二項誠實聲明**：麥克阿瑟（John MacArthur）**沒有瑪拉基書的逐節講道系列**：gty.org 的網站地圖（2026-10-31 下載）裏沒有書卷代碼 39 的講道網址。本書引用的，是另一種東西：他在別篇講道裏**解釋瑪拉基書某一節**的句子。取得方式是掃描網站地圖所列的講道逐字稿：第一輪 2,506 篇（NN-NN 編號），其中 201 頁含 "Malachi"，128 篇確實引到或解釋瑪拉基書的具體經節，存檔於 `sources/commentary/macarthur/`（`INDEX.md` 與 `QUOTES.md`）；第二輪補掃另外 777 篇舊編號（純數字）講道，78 頁出現 "Malachi"，結果見 `LEGACY-SCAN.md`（沒有加進書裏）；777 頁的逐字稿沒有存檔，只存了網址清單 `legacy-urls.txt` 與命中表，需要時可重抓。網站地圖本身存檔為 `gty-sitemap-2026-10-31.xml`。**這 128 與 78 篇沒有逐篇細讀**，節號標註依上下文判斷；書中只引 `QUOTES.md` 裏經逐字比對的句子。這些講道是針對別的經文（羅馬書、馬太福音、路加福音等）而講，所以他解釋瑪拉基書的句子多半是順帶援引，不能當作他對全書的系統解經。

**第三項誠實聲明**：摩根《聖經各卷的生命信息》的文字取自 archive.org 兩份不同掃描本的 OCR（光學辨識）文本，不是校對過的排印本。書中所引摩根各句，已與存檔的 OCR 文字逐字比對；**頁碼依 OCR 文字中的頁眉（"THE MESSAGE OF MALACHI 3NN"）判定，沒有另外對照整本掃描 PDF，也沒有人工逐頁看圖。**

**第四項誠實聲明**：教父引文（《十二使徒遺訓》、猶斯丁、愛任紐、奧古斯丁）取自十九世紀英譯本（ANF、NPNF），不是希臘文或拉丁文原文，引文的措辭是譯本的措辭。加爾文英譯本裏歐文（John Owen）的編者註腳不是加爾文的話，書中凡提到註腳之處都明寫「編者」。

---

## 一、經文

| 項目 | 版本 | 取得與核對方式 |
|--------|------------|------------------------------------------------------------|
| 中文 | 和合本 (CUV) | 以 `ai-eden.com` 和合本（API `/api/bible/malachi/N?t=CUV`）為底本，與信望愛 `bible.fhl.net`（unv）比對：55 節中的差異都只在標點、「麼／嗎」「他／她」「牠／他」與空格（逐條見 `sources/scripture/two-source-diff.txt`），沒有字句的實質差異。依全庫政策以 ai-eden 為準；「裡」一律作「裏」。2:14 的「他／她」：和合本原文作「他」。 |
| 英文 | NASB 1995 | 取自 `biblehub.com/nasb/malachi/N.htm`（頁首標 NASB 1995），剔除段落小標題後，與 ai-eden 的 NASB 系文本逐字（不計標點與大小寫）比對，55 節全部一致；補充字依 biblehub 版本保留斜體。**未另與 biblegateway 比對。** |
| 希伯來文 | WLC（OSHB） | 取自 openscriptures/morphhb 公開文本（`wlc/Mal.xml`），含詞性標注；書中所有字數都用程式從這個文本計數。節號換算為英文（和合本）節號：希伯來文 3:19-24 = 4:1-6。 |
| 其他經卷 | 和合本 | 書中引用的其他經文，逐節以 `sources/cuv.py`（ai-eden）取得後照錄；並用 `scripts/verify-prose-citations.py books/bible/malachi --self 瑪` 逐條機器核對。該腳本讀的是信望愛版，所以殘留的不符都是「麼／嗎」「挂／掛」「裏／裡」「阿／啊」一類的底本用字差異（保留 ai-eden 的字），沒有字句上的不符。 |
| 經文區塊 | 兩版對照 | 每章「經文」小節由 `sources/gen_scripture_blocks.py` 自動生成，`--check` 比對各章與生成檔逐字相同。 |

**希伯來文字數**（用 `sources/count_hebrew.py` 重現，完整表見 `sources/keyword-counts.md`）：

| 字 | 次數 | 位置 |
|----------------|------|--------------------------------------|
| צְבָאוֹת 萬軍 | 24 | 1:4、6、8、9、10、11、13、14；2:2、4、7、8、12、16；3:1、5、7、10、11、12、14、17；4:1、3 |
| אָמַר 說 | 40 | 見 `keyword-counts.md` |
| וַאֲמַרְתֶּם 你們卻說 | 9 | 1:2、6、7、13；2:14、17；3:7、8、13（另 3:14 אֲמַרְתֶּם 一次） |
| 人的問題 | 8 | 1:2、6、7；2:14、17；3:7、8、13 |
| שָׁלַח 差遣 | 5 | 2:2、4、16；3:1；4:5（神作主詞 4 次，2:16 是人休妻） |
| שֵׁם 名 | 10 | 1:6（2）、11（3）、14；2:2、5；3:16；4:2 |
| בְּרִית 約 | 6 | 2:4、5、8、10、14；3:1 |
| בָּגַד 詭詐 | 5 | 2:10、11、14、15、16 |
| שׁוּב 轉向 | 7 | 1:4；2:6；3:7（3）、18；4:6 |
| יוֹם 日子 | 8 | 3:2、4、7、17；4:1（2）、3、5 |
| שֶׁמֶשׁ 日頭 | 2 | 1:11；4:2 |
| 咒詛類字 | 7 | 1:14；2:2（3）；3:9（2）；4:6 |
| דָּבַר（Niphal） | 2 | 3:13、3:16 |

和合本把原文的某些詞合併或略譯，所以中文讀者看到的次數不一定與上表相同（例：1:4 的「回去」和合本略去）。「全書最後一個詞是咒詛」一說，只對希伯來文原文成立；和合本 4:6 中文句末是「遍地」。各章原文研讀表的字義說明，是編者對照希伯來文本與 NASB／和合本／加爾文與亨利的英文引文所寫，**沒有逐條細讀 BDB 全文詞條，也未對照 HALOT**；第八章 חֵרֶם 的釋義取自 biblehub 轉錄的 BDB 詞條（`sources/commentary/biblehub-h2764.html`）。

---

## 二、引文核對記錄——麥克阿瑟 (John MacArthur, Grace to You, gty.org)

本書共引麥克阿瑟 19 句，用 `scripts/verify-sermon-quotes.py` 逐句對照各自講章的 gty.org 逐字稿（先取得逐字稿快取，再比對字串）：**19/19 逐字相符**。逐字引文出現在第1章、第2章、第3章、第4章、第5章、第6章、第7章、第8章。第3章的兩句取自 60-18（講題是信徒的祭司身分，他借瑪拉基書二章對照真假祭司，不是逐節解經；書中已如實說明）。

| 章 | 講章（Grace to You 編號） | 論及經節 |
|------|------------------------------------------------------------|------------------|
| 第1章 | 45-71 *Is Israel's Unbelief Inconsistent with God's Plan? Part 1*；42-195 *The Extreme Nature of True Discipleship, Part 1* | 1:2-3 |
| 第2章 | 42-147 *When You Pray Say*；62-4 *The Certainty of Sin, Part 1*；49-11 *The Mystery of Christian Unity, Part 2* | 1:6-14 |
| 第3章 | 60-18 *The Believer's Privileges, Part 2: Access Part 1*（2 句） | 2:1-9；2:5 |
| 第4章 | 41-48 *The Truth About Divorce, Part 1*（2 句）；80-383 *Husbands, Love Your Wives* | 2:10-16 |
| 第5章 | 41-2 *The Herald of the New King*；42-98 *The Greatest Man Who Ever Lived, Part 2* | 3:1 |
| 第6章 | 45-102 *Paying Your Taxes, Part 1*；80-365 *The Christian and Taxes*；90-72 *Biblical Principles for Handling Money, Part 2* | 3:8-10 |
| 第7章 | 81-183 *The Final Mystery Revealed*；49-21 *What's Wrong with Everybody?* | 3:16-18 |
| 第8章 | 41-44 *When Does Elijah Come?*；42-40 *A Voice Crying in the Wilderness, Part 2* | 4:5-6 |

（上表以各章實際出現的來源行為準；若表與章內來源行不同，以章內為準，並請以 `verify-sermon-quotes.py` 重新核對。）逐字稿的引號與撇號有直、彎兩種，比對時已正規化。

---

## 三、引文核對記錄——摩根 (G. Campbell Morgan)

引自 "The Message of Malachi," *Living Messages of the Books of the Bible* (New York: Fleming H. Revell, 1912), pp. 335-349，取自 archive.org `livingmessagesof0000gcam_p4q1`（OCR，存檔於 `sources/commentary/morgan-living-messages-malachi-ocr1.txt`）。本書共引摩根 15 句，用 `sources/check_quotes.py` 逐句比對（忽略大小寫、標點、換行與斷行連字號）：**15/15 逐字相符**。逐字引文出現在第1章、第2章、第3章、第4章、第5章、第6章、第7章、第8章與卷首〈啟示的次序與神的計劃〉。

| 出現處 | 頁碼 | 引句數 |
|------------------------|--------------------|------|
| 卷首〈啟示的次序與神的計劃〉 | 341 | 1 |
| 第1章 | 341、342 | 2 |
| 第2章 | 339、344 | 2 |
| 第3章 | 335、337 | 2 |
| 第4章 | 337 | 1 |
| 第5章 | 343、343 | 2 |
| 第6章 | 337 | 1 |
| 第7章 | 345、346、347 | 3 |
| 第8章 | 347 | 1 |

第7章如實標明：摩根在 p.345 說 3:16「思念他名」的希臘字與腓 4:8 同字、意為「點算清單」，本書查證七十士譯本（Rahlfs 1935，存檔於 `sources/commentary/lxx-malachi-3-13-18.txt`）瑪 3:16 實際用字為 εὐλαβουμένοις，腓 4:8 為 λογίζεσθε，整卷瑪拉基書搜不到 λογιζ- 詞幹，**他這一點本書未能核實**。只查了 Rahlfs，其他七十士譯本版本是否有異文沒有查。

---

## 四、引文核對記錄——加爾文 (John Calvin)

引自 *Commentaries on the Twelve Minor Prophets*, vol. 5 (Zechariah, Malachi), tr. John Owen (Edinburgh: Calvin Translation Society)，取自 CCEL 公有領域文本（`calcom30`，存檔於 `sources/commentary/calvin-malachi.txt`）。CCEL 文本沒有印本頁碼，故書中以經節標示位置。共引 22 句，**22/22 逐字相符**。書中所引都是加爾文正文；Owen 的編者註腳（Ed.）不是加爾文的話，凡提到編者註腳之處（〈瑪拉基書的位置〉的年代表、第3章 2:3、第5章），都明寫「編者」，並不加引號。

| 出現處 | 引句數 |
|--------------------|------|
| 卷首（位置、骨幹） | 2 |
| 第1章 | 2 |
| 第2章 | 2 |
| 第3章 | 3 |
| 第4章 | 2 |
| 第5章 | 3 |
| 第6章 | 3 |
| 第7章 | 3 |
| 第8章 | 2 |

---

## 四之二、引文核對記錄——Keil (C. F. Keil)

引自 *Biblical Commentary on the Old Testament: The Twelve Minor Prophets*, vol. 2, tr. James Martin (Edinburgh: T. & T. Clark, 1878)，取自 archive.org `thetwelveminorpr02keiluoft`（OCR，存檔於 `sources/commentary/keil-minor-prophets-vol2.txt`；瑪拉基書在該卷 pp.430 起）。本書只在第2章 1:11 引了他 2 句，作為十九世紀近代注釋的讀法（他本人讀為預言，並列出現在式與將來式兩派的名單），用 `sources/check_quotes.py` 逐句比對：**2/2 逐字相符**。這是本書唯一的近代注釋；二十世紀以後的注釋書沒有取得原文。

---

## 五、引文核對記錄——亨利 (Matthew Henry)

引自 *An Exposition of the Old and New Testament*，瑪拉基書一卷（亨利本人所撰），取自 CCEL `mhc4` 公有領域文本，無印本頁碼（存檔於 `sources/commentary/henry-malachi.txt`）。共引 22 句，**22/22 逐字相符**。

| 出現處 | 引句數 |
|--------------------------|------|
| 卷首（位置、骨幹） | 2 |
| 第1章 | 2 |
| 第2章 | 2 |
| 第3章 | 3 |
| 第4章 | 3 |
| 第5章 | 3 |
| 第6章 | 2 |
| 第7章 | 3 |
| 第8章 | 2 |

---

## 六、教父

第2章引《十二使徒遺訓》第14章（Roberts–Donaldson 譯，earlychristianwritings.com）、猶斯丁《與特里弗對話》第41章（ANF vol. 1）、愛任紐《駁異端》4.17.5（ANF vol. 1）、奧古斯丁《上帝之城》18.35（NPNF 1st ser. vol. 2，Marcus Dods 譯）各一句；第3章再引奧古斯丁《上帝之城》18.35 一句。共 5 句，原文存檔於 `sources/fathers/`，逐字比對（比對用腳本寫在寫作者的暫存區，未留存於專案內；可依存檔文字重做）。《十二使徒遺訓》的年代學者有爭議，本書不下定論。

---

## 七、聖詩

各章配詩都是公有領域的聖詩，歌詞多數取自標明年代的印本（經 Wikisource 轉錄；第5章取自 *The English Hymnal* 1906 的 archive.org OCR），第3章、第6章的 Wikisource 頁未標明所據印本；一律不採用現代改寫本：

| 章 | 聖詩 | 所據印本 |
|-------|------------------------------------------------------------|------------------------------------------|
| 第1章 | *O Love That Will Not Let Me Go*（George Matheson, 1882） | *The Army and Navy Hymnal*（1920）no. 110 |
| 第2章 | *Take My Life, and Let It Be*（Frances R. Havergal, 1874） | *The Army and Navy Hymnal*（1920）no. 116 |
| 第3章 | *O Thou Who Camest from Above*（Charles Wesley, 1762） | Wikisource（未標示所據版本） |
| 第4章 | *How Firm a Foundation*（"K—", John Rippon, 1787） | *The Army and Navy Hymnal*（1920） |
| 第5章 | *On Jordan's Bank the Baptist's Cry*（Charles Coffin / J. Chandler） | *The English Hymnal*（1906）OCR |
| 第6章 | *Softly and Tenderly Jesus Is Calling*（Will L. Thompson, 1880） | Wikisource（該頁註明歌詞轉自 Timeless Truths 圖書館） |
| 第7章 | *Blest Be the Tie That Binds*（John Fawcett） | *The Army and Navy Hymnal*（1920）no. 170 |
| 第8章 | *Hark! The Herald Angels Sing*（Charles Wesley, altered by later hands） | *The Army and Navy Hymnal*（1920） |

各章的校註交代了各首與印本的出入（誤植、略去的副歌、行首大寫等）。第7章的作者年份：Wikisource 該頁印作 1772，通行說法是 1782，本書不寫年份。中譯為編者所譯，求達意，不求可唱。

---

## 八、核對方法

- `sources/check_quotes.py`：逐句核對加爾文、亨利、摩根的 `> "引句"`；61 句（含 Keil 2 句）全部通過。
- `scripts/verify-sermon-quotes.py books/bible/malachi`：麥克阿瑟 19/19。
- `scripts/verify-prose-citations.py books/bible/malachi --self 瑪`：行文中的經文引用，不符項全為底本用字差異（見第一項）。
- `sources/gen_scripture_blocks.py --check`：八章經文區塊與生成檔同步。
- `scripts/gen-malachi-indices.py --check`：索引與各章同步。

---

## 九、本書沒有做到的

- **已做兩輪獨立校對，但沒有人類通讀。**本書由一位主線作者與四位並行寫作者完成；各章逐句機器核對後，第一輪由三位唯讀代理分三組向原始來源重新取證（無杜撰，抓出約 40 項過度或不逐字的說法，已修）；精簡與修正之後，第二輪由另一位代理比對改動前後的差異、重驗被改寫的句子與本附錄各項計數（抓出附錄過時聲明、1 處計數矛盾、數處經文用語，已修）。沒有第二位人類校對者通讀，所以本書的自評分數不能當作定論。
- **精簡輪只做了一輪。**第3至第8章各刪約 8–12%（重複的論點、過細的表格列、牽強的「活在今天·AI時代」整節；第5、7章基督焦點各刪一句，第5章 3:1 讀法表合併了列）；第2章先因新增 Keil 一家與 1:11 表格一列略增，之後另做一輪精簡（31.6→27.3 KB，約 -14%；整張「這十四節的結構」表、「祭物的線」、נשא פנים 一列與幾條重複引文被刪），仍是最長一章。經文、注疏引文、配詩與各家並排立場均未改字。
- 麥克阿瑟的 128 篇涉及瑪拉基經節的講章沒有逐篇細讀；他對 3:8-10 的立場（神權國度的稅）、對以利亞的「若以色列接受」與「尚有未來應驗」兩種說法，書中如實並排，未裁決。
- 教父引文只取英譯本；近代學者對 1:11 的讀法只有 Keil（十九世紀）一家，二十世紀以後的注釋書沒有取得原文，所以第2章 1:11 的讀法並排仍不完整（正文已說明）。
- 摩根頁碼只依 OCR 頁眉，未對照掃描 PDF。
- 原文研讀的字義說明：2026-10-31 事後以 openscriptures/HebrewLexicon 的 BDB 詞條索引（公有領域，簡短釋義，以 Strong 號對應 WLC 詞元；全書 306 個詞元的對照表存檔於 `sources/hebrew/bdb-glosses-malachi.md`）由一位唯讀代理逐列核對各章〈原文研讀〉表與正文的字義、字根、語態與「全書N次」：沒有與 BDB／WLC 衝突之處，修了 12 處措辭（例如「哥哥」不是 אָח 的字義、יִגְדַּל 是 Qal 假設語氣不是被動、וָאֹהַב 是 waw 連續式、「煉金」「廢棄」「之下」是和合本譯法）。**這只核對了簡短釋義，沒有讀 BDB 全文詞條，也未對照 HALOT。**
- 2:12（עֵר וְעֹנֶה）、2:15、2:16、3:17 的 סְגֻלָּה，各家讀法並排，沒有裁決。
- 「老弟兄查經」各節是方法的應用，不是筆記（見第一項誠實聲明）。

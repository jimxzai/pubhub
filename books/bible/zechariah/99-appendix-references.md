---
title: 撒迦利亞書研讀
subtitle: The Book of Zechariah Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---

# 附錄：引用出處總表 (Appendix: References)

本附錄是全書「不杜撰一句經文，不編造一條注疏」這句話的帳目。各家注疏引句的數量、出處與核對方式列在這裏；逐句的出處，見各章引文下方的出處行，讀者可以據以自己查證。核對所用的原始文本，存放在 `books/bible/zechariah/.sources/`（經文、希伯來文與計數程式）與 `.sources/commentary/`（注疏原文與講道逐字稿），各檔的網址、版本與取得日期見檔頭。

**第一項誠實聲明**：倉庫中老弟兄的查經筆記，**沒有任何一則以撒迦利亞書為題**。全書「老弟兄查經」各節，是把他一貫的查經方法——提問式帶領、精義一句話、全經連線、每次查經末了問「你看見耶穌了嗎？」——應用在撒迦利亞書的經文上，不是任何歷史查經記錄的複現。書中加引號歸給老弟兄的話，只有〈撒迦利亞書深度領受〉卷首的一句語錄（「你研讀聖經，卻沒有看見耶穌——那本書等於白讀了。」），出自 `.claude/skills/ask-elder-wong/references/voice.md` 的語錄白名單。

**第二項誠實聲明**：麥克阿瑟（John MacArthur）的引文，取自 gty.org 公開的講道逐字稿（19 篇，代碼 2153-2171），是口語講稿，保留講員原話與轉錄錯字；本書沒有核對講道的錄音。他對第9至14章的讀法屬分別主義、前千禧年；書中凡引用，都標明是他的讀法。摩根《聖經全本講解》（*An Exposition of the Whole Bible*, 1959）的網頁轉錄沒有印本頁碼，其版權狀態本書未查清（已引的 19 句，均為單句或短段）。

**第三項誠實聲明**：書中的注疏出處行，與 `.sources/commentary/` 下的檔案逐一對應。加爾文英譯本裏的編者註腳（標「-- Ed.」與括號數字）不是加爾文的話，本書不引為加爾文。普西（E. B. Pusey）轉譯教父處，本書寫「普西轉述 X」，並說明教父的名字是依普西自己的註腳；書中沒有把普西轉譯的句子當作教父原文。

---

## 一、經文

| 項目 | 版本 | 取得與核對方式 |
|--------|------------|------------------------------------------------------------|
| 中文 | 和合本 (CUV) | 以 ai-eden.com 的和合本（CUV）逐章資料為底本，與信望愛 `bible.fhl.net`（unv）逐節比對，二百一十一節中有二十五節兩者字形不同（fhl 較現代：嗎／她／它／牠／泰爾／黎巴嫩／約旦／大馬士革／希臘等），逐節比對 cnbible.com 的原版和合本欄，與 ai-eden 相符；全書依 ai-eden 的字形，標點（「」）依 fhl。記錄見 `.sources/cuv-crosscheck.md`。「裡」一律作「裏」。 |
| 英文 | NASB 1995 | 取自 `biblehub.com/nasb/zechariah/N.htm`（以 9:9 "just and endowed with salvation" 確認是 1995 版），斜體（補充字）依 ai-eden 標示。 |
| 希伯來文 | WLC（OSHB） | 取自 openscriptures/morphhb 公開文本（`wlc/Zech.xml`），含詞性標注；書中所有字數都用程式從這個文本計數（`.sources/count_hebrew.py`，兩次執行結果相同）。全書詞元 3128 個，OSHB 原文 `<w>` 元素 3134 個，其中 6 個 ketiv 由其 qere 取代。 |
| 其他經卷 | 和合本 | 書中引用的其他經文，逐節以信望愛和合本 JSON 介面取得後照錄，並用 `scripts/verify-prose-citations.py --self 亞` 逐條機器核對。該腳本讀的是 fhl 的字形，所以凡 ai-eden 與 fhl 字形不同的撒迦利亞書本身的經文，腳本會報「MISS」；這些是已知的字形差異，不是書稿錯誤（見下〈核對方法〉）。 |

**三處需要說明的經文決定**

- **14:12**：ai-eden 的和合本、cnbible 與 biblegateway 的和合本作「吞在口中潰爛」；fhl、和合本修訂版（CUVMPT）與希伯來文（לָשׁוֹן「舌」）作「舌在口中潰爛」。本書用「舌」，並視「吞」為輾轉抄錄的異文。
- **11:15**：四個和合本來源都作「愚昧人的器具」，沒有「牧」字；希伯來文與 NASB 是「牧人／shepherd」。本書照和合本，並在第15章說明。
- **12:10**：和合本作「所扎的」（不是「刺」），並附注「或譯：他；本節同」。

**希伯來文字數**（用 `.sources/count_hebrew.py` 重現；完整逐節清單見 `.sources/keyword-counts.md`）：

| 字 | 次數 | 位置 |
|----------------|------|--------------------------------------|
| יְהוָה צְבָאוֹת 萬軍之耶和華 | 53 | 第1章9；第2章3；第3章3；第4章2；第5章1；第6章2；第7章6；第8章18；9:15；10:3；12:5；13:2、7；14:16、17、21（2） |
| בַּיּוֹם הַהוּא 在那日 | 22 | 2:11；3:10；6:10；9:16；11:11；12:3、4、6、8（2）、9、11；13:1、2、4；14:4、6、8、9、13、20、21 |
| שׁוּב 轉向 | 18 | 1:3（2）、4、6、16；4:1；5:1；6:1；7:14；8:3、15；9:8、12（2）；10:6、9、10；13:7 |
| שָׁכַן 住 | 4 | 2:10、11；8:3、8 |
| 「你們就知道萬軍之耶和華差遣了我」 | 4 | 2:9、11；4:9；6:15 |
| מַשָּׂא 擔子 | 2 | 9:1；12:1 |
| זָמַם 定意 | 3 | 1:6；8:14、15 |
| צֶמַח 苗 | 2 | 3:8；6:12 |
| רוּחַ 靈／風 | 9 | 2:6；4:6；5:9；6:5、8；7:12；12:1、10；13:2 |
| רָעָה 牧養／牧人（含 רֹעִי「我的牧人」） | 14 | 10:2、3；11:3、4、5、7（2）、8、9、15、16、17；13:7（2）；（11:17 與 13:7 的 רֹעִי，OSHB 標為另一詞元 7473，按詞形補入） |

「萬軍之耶和華」的算法：原文 יהוה 緊接 צבאות 才算一次，全書 צבאות 一共 53 次，與此相同。1:16 與 8:3 的 שַׁבְתִּי 是第一人稱完成式「我回到」；8:15 也有同形 שַׁבְתִּי，但那裏是副詞用法（「再」，緊接 זָמַמְתִּי「我定意」），不是「回到」。各章另有若干章內計數（如某個詞在第13章只出現一次），按 OSHB 詞元逐節查得，寫在該章原文研讀表裏；逐節清單見 `keyword-counts.md` 末節〈章內計數〉。上表的「定意」與「擔子」兩列不在 `keyword-counts.md` 裏，是另以同一份 OSHB 文本重新計數（3 次與 2 次）。原文研讀各表的字義說明，是編者對照希伯來文本、NASB／和合本與各注疏家的英文引文所寫；**沒有逐條對照 BDB 或 HALOT 全文詞條**。

---

## 二、引文核對記錄——麥克阿瑟 (John MacArthur, Grace to You, gty.org)

引自 gty.org 講道逐字稿（SSR 網頁取得，2026-10-31），代碼為四位數。共引 38 句，用 `scripts/verify-sermon-quotes.py` 以本地逐字稿檔（`--cache`）比對：**38/38 逐字相符**。

| 章 | 講道代碼 | 講道標題 |
|-------|--------|----------------------------------------|
| 第1章 | 2153 | The Prerequisite for Blessing |
| 第2章 | 2154 | The Divine Plan for Jerusalem, Part 1 |
| 第3章 | 2156 | The Conquest of Israel's Enemy |
| 第4章 | 2157 | The Future Glory of Jerusalem |
| 第5章 | 2158 | The Cleansing of the Nation of Israel |
| 第6章 | 2159 | Israel: The Light of the World |
| 第7章 | 2160 | The End of Sinners and Sin |
| 第8、9章 | 2161 | Establishing God's Kingdom on Earth |
| 第10章 | 2162 | Ritual vs. Reality |
| 第11章 | 2163 | Turning the Fast into a Feast |
| 第12章 | 2164 | The Saga of Two Conquerers, Part 1 |
| 第13章 | 2165 | The Saga of Two Conquerers, Part 2 |
| 第14章 | 2166 | The Redemption of Israel |
| 第15章 | 2167、2168 | 2167：The Rejection of the True Shepherd；2168：The False Shepherd |
| 第16章 | 2169 | Israel's Final Deliverance |
| 第17章 | 2170 | The Cleansing of Israel |
| 第18、19章 | 2171 | The Day of the Lord |

2155（The Divine Plan for Jerusalem, Part 2）本書沒有引用。麥克阿瑟逐字稿的轉錄錯字（如 "Conquerers"）照原樣保留在講道標題裏。逐字引文的章：第1章、第2章、第3章、第4章、第5章、第6章、第7章、第8章、第9章、第10章、第11章、第12章、第13章、第14章、第15章、第16章、第17章、第18章、第19章。

---

## 三、引文核對記錄——摩根 (G. Campbell Morgan)

兩個出處：(1) "The Message of Zechariah," *Living Messages of the Books of the Bible*, Old Testament (New York: Fleming H. Revell, 1912), pp. 317-331，取自 archive.org 兩份掃描本的 OCR（`livingmessagesof0000gcam_p4q1`、`livingmessagesof0000unse`），**有頁碼**；(2) *An Exposition of the Whole Bible* (New York: Fleming H. Revell, 1959)，Zechariah 1-14，網頁轉錄（truthaccordingtoscripture.com），**沒有頁碼**。書中共引摩根 34 句：Living Messages 15 句、Exposition 19 句；用 `scripts/verify-citations.py` 加上 `.sources/tools/check_frontmatter_quotes.py`（核對卷首各章）比對：**全部逐字相符**，其中 4 句以 OCR 容錯比對（OCR 斷行連字號）。Living Messages 的 OCR 有錯字（如 "peculias"、"Jehovab"），書中所引句都不含這些錯字。

逐字引文的章：第1章、第2章、第3章、第4章、第5章、第6章、第7章、第8章、第9章、第10章、第11章、第12章、第13章、第14章、第15章、第16章、第17章、第18章、第19章。

---

## 四、引文核對記錄——加爾文 (John Calvin)

引自 *Commentaries on the Twelve Minor Prophets*, vol. 5 (Zechariah and Malachi), tr. John Owen (Edinburgh: Calvin Translation Society, 1849)，取自 CCEL 公有領域文本（`calcom30`）。共引 59 句：各章「歷代注疏」小節 58 句，加上卷首〈位置〉1 句；**59/59 逐字相符**（核對腳本只掃各章注疏小節，卷首那一句另以 `check_frontmatter_quotes.py` 逐字核對）。書中所引都是加爾文正文；Owen 的編者註腳（Ed.）不是加爾文的話，凡提到編者註腳之處，都明寫「編者」，並不加引號。

逐字引文的章：第1章、第2章、第3章、第4章、第5章、第6章、第7章、第8章、第9章、第10章、第11章、第12章、第13章、第14章、第15章、第16章、第17章、第18章、第19章。

---

## 五、引文核對記錄——亨利 (Matthew Henry)

引自 *Commentary on the Whole Bible*, vol. 4 (Isaiah to Malachi)，撒迦利亞書一卷（亨利本人所撰），取自 CCEL `mhc4` 公有領域文本，無印本頁碼。共引 49 句，**49/49 逐字相符**；卷首另有 2 句（〈位置〉〈啟示的次序〉各 1 句），一併逐字核對。

逐字引文的章：第1章、第2章、第3章、第4章、第5章、第6章、第7章、第8章、第9章、第10章、第11章、第12章、第13章、第14章、第15章、第16章、第17章、第18章、第19章。

---

## 六、其他注疏：普西與教父

| 章 | 作者與出處 | 取得 |
|-------|------------------------------------------------------------|----------------------------|
| 第4章 | Justin Martyr, *Dialogue with Trypho*, ch. 115 | New Advent，ANF 1，tr. Dods & Reith |
| 第5章 | Justin Martyr, *Dialogue with Trypho*, ch. 116 | New Advent，ANF 1，tr. Dods & Reith |
| 第9章 | Justin Martyr, *Dialogue with Trypho*, ch. 121 | New Advent，ANF 1，tr. Dods & Reith |
| 第10章 | E. B. Pusey, *The Minor Prophets*, vol. 8 (Zechariah) | archive.org `minorprophetswit0003reve` |
| 第13章 | John Chrysostom, *Homilies on Matthew*, Hom. 66 | New Advent，NPNF 1/10，tr. Prevost & Riddle |
| 第13章 | Cyril of Jerusalem, *Catechetical Lecture* 13, §34 | New Advent，NPNF 2/7，tr. Gifford |
| 第15章 | Cyril of Jerusalem, Lecture 13, §10；Augustine, *Harmony of the Gospels* III.7 §31；Pusey（11:1-3 綜述，無引號） | New Advent，NPNF 2/7；NPNF 1/6，tr. Salmond |
| 第16章 | Cyril of Jerusalem, Lecture 13, §41；Pusey（轉譯註明 "S. Jer." 的一段） | New Advent；Pusey, *The Minor Prophets*, vol. 8（Nisbet, 1907 reprint） |
| 第17章 | Justin Martyr, *Dialogue with Trypho*, ch. 53 | New Advent，ANF 1，tr. Dods & Reith |
| 第18章 | Cyril of Jerusalem, Lecture 13, §24 | New Advent |

普西的文本有希伯來文與希臘文亂碼，本書只引純英文句。第16章那一句，普西轉譯的是註腳標為 "S. Jer." 的一段，本書寫「耶柔米，經普西譯引」；**這個識別只依普西自己的註腳，沒有對照耶柔米的拉丁原文。**

---

## 七、聖詩

各章配詩都是公有領域的聖詩（作者卒於1930年之前），歌詞取自標明年代的印本（經 Wikisource 轉錄），或 Wikisource 的聖詩頁面（未註明印本者，在各章配詩的出處行如實註明）。

| 章 | 聖詩 | 所據 |
|-------|------------------------------------------------------------|------------------------------------------|
| 第1章 | *Come, Sinners, to the Gospel Feast*（Charles Wesley） | Wikisource 聖詩頁面（未註明印本） |
| 第2章 | *God Moves in a Mysterious Way*（William Cowper） | *Olney Hymns*（1840 ed.） |
| 第3章 | *A Mighty Fortress Is Our God*（Luther／Hedge） | *The Army and Navy Hymnal*（1920） |
| 第4章 | *Glorious Things of Thee Are Spoken*（John Newton） | 同上 |
| 第5章 | *Arise, My Soul, Arise*（Charles Wesley） | 同上 |
| 第6章 | *Spirit of God, Descend upon My Heart*（George Croly） | 同上 |
| 第7章 | *Rock of Ages, Cleft for Me*（A. M. Toplady） | 同上 |
| 第8章 | *This Is My Father's World*（M. D. Babcock） | Wikisource 聖詩頁面（未註明印本） |
| 第9章 | *Crown Him with Many Crowns*（Matthew Bridges） | *The Army and Navy Hymnal*（1920） |
| 第10章 | *Take My Life, and Let It Be*（F. R. Havergal） | 同上 |
| 第11章 | *Jerusalem the Golden*（Bernard of Cluny／Neale） | 同上 |
| 第12章 | *Lead On, O King Eternal*（E. W. Shurtleff） | 同上 |
| 第13章 | *All Glory, Laud, and Honor*（Theodulf／Neale） | 同上 |
| 第14章 | *The King of Love My Shepherd Is*（H. W. Baker） | 同上 |
| 第15章 | *Beneath the Cross of Jesus*（E. C. Clephane） | 同上 |
| 第16章 | *When I Survey the Wondrous Cross*（Isaac Watts） | 同上 |
| 第17章 | *There Is a Fountain Filled with Blood*（William Cowper） | 同上 |
| 第18章 | *Lo, He Comes with Clouds Descending*（Wesley／Cennick） | Wikisource 聖詩頁面（未註明印本） |
| 第19章 | *Holy, Holy, Holy! Lord God Almighty*（Reginald Heber） | *The Army and Navy Hymnal*（1920） |

第1、8、18章所據不是標明年代的印本，與通行本逐字相符與否，沒有另行核對。中譯為編者所譯，求達意，不求可唱。

---

## 八、核對方法

- `scripts/verify-citations.py`：逐段核對加爾文、亨利、摩根（含普西）各小節下的 `> "引句"`（含 OCR 容錯）。
- `scripts/verify-sermon-quotes.py --cache`：核對麥克阿瑟的引句，對象是本地存檔的逐字稿。
- `.sources/tools/check_frontmatter_quotes.py`：核對卷首各章與未放在「歷代注疏」小節之下的引句，對象是全部注疏來源檔。
- `scripts/verify-prose-citations.py books/bible/zechariah --self 亞`：行文中的經文引用。該腳本讀 fhl 的字形，ai-eden 與 fhl 字形不同處（嗎／麼等）會報 MISS，這些已逐條看過，屬字形差異。
- `scripts/check-book-spine.py`：四項骨幹檢查。
- `scripts/gen-zechariah-indices.py --check`：索引與生成器的解析結果同步（生成器不認某些前字與頓號後的連續節式，偶有漏列，見索引頁）。

---

## 九、本書沒有做到的

- **校對由唯讀的 AI 校對者擔任，沒有人類校對者通讀。**全書經三輪獨立校對，每輪的校對者彼此獨立，且不讀前面各輪的報告：第一輪四位，共提出嚴重錯誤（事實錯誤、語意倒反、歸屬錯誤）27 項、次要錯誤（無據絕對語、計數、出處地址、規則違反）90 項；第二輪五位，嚴重錯誤 19 項、次要錯誤 96 項；第三輪五位（在精簡輪之後，專查修訂與精簡所帶進的錯誤），嚴重錯誤 3 項、次要錯誤 41 項。凡經核對屬實者都已修正，報告存於 `.sources/review/`。三輪的嚴重錯誤數遞減，但**第三輪修訂之後的文字，沒有再交給另一位校對者整體重讀**；修訂本身可能帶進新的錯誤，所以本書不敢說已經沒有錯。
- **精簡只做了一輪。**這一輪刪去各章重複的命題，縮減約一成多；現在各章約 22–28 KB，最長的是第15章（約 28 KB），其次是第11、5、19章（約 26–27 KB）。同一點仍可能分散在領受要點、提問式對話、默想問題與禱告之間，沒有逐句量測是否已全部清除。
- **原文研讀的字義說明只經代理逐項對照希伯來文本與注疏，沒有對照 BDB 或 HALOT 全文詞條。**
- **麥克阿瑟的引句只對照 gty.org 的逐字稿文字，沒有對照錄音**；他的逐字稿有轉錄錯字。摩根《聖經全本講解》（1959）網頁轉錄的版權狀態未查清。
- **普西轉譯的「耶柔米」一段**，識別依普西自己的註腳，沒有對照耶柔米的拉丁原文；加爾文英譯本裏的編者註腳不是加爾文，書中引到處都已標明「編者」。
- **聖詩**：第1、8、18章所據不是標明年代的印本，與通行本是否逐字相符沒有另行核對；中譯為編者所譯。
- **經文版本決定**：14:12「舌」、11:15「愚昧人」兩處和合本來源不一致，本書的選擇已在〈一、經文〉說明；這是本書的取捨，不是定論，讀者可對照手邊的和合本印本。
- **歷來爭論不下判斷**：第9至14章的時間（已成就／末日／象徵）、「耶和華的使者」與「差遣我的萬軍之耶和華」的關係、約書亞與「苗」、12:10 的「我」與「他」、太27:9 歸給耶利米、三個牧人、14:21 的「迦南人」，本書都只並排列出各家讀法。
- **章號歧義**：本書的「第N章」是十九個單元，不等於聖經的章；經文範圍行與全書座標行負責對應，書中已在〈概覽〉說明，沒有另行改標題。
- **版面只看過部分頁面**：封面、封底、書名頁相關頁、目錄、概覽、〈啟示的次序〉的表、第1章的開頭與原文研讀表、一頁注疏；沒有逐頁看全書。
- **NASB 的授權**：版權頁依 Lockman Foundation 的通行格式註明 NASB 版權，本書沒有保存授權往來的紀錄；全卷經文的英文並列引用，是否在該基金會的免申請範圍內，本書沒有查清，公開發行前須由出版者另行確認。
- **8:3 的時態**：NASB 1995 作 *I will return to Zion*（未來式）；希伯來文 שַׁבְתִּי 是完成式，本書的書名頁與第11章標題取完成式（*I Have Returned to Zion*），經文區塊仍照 NASB 原文。

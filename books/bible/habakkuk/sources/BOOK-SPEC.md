# 哈巴谷書研讀 — BOOK-SPEC（給寫章節的代理）

範例章：`books/bible/habakkuk/01-how-long.md`（先完整讀一遍；格式、語氣、密度都照它；它已通過 verify-citations、verify-prose-citations、lint）。
全書工作目錄：`/Users/jimxiao/dev/pubhub`。書稿目錄：`books/bible/habakkuk/`。來源目錄：`books/bible/habakkuk/sources/`（以下簡稱 `$S`）。

## 0. 硬規則（違反任何一條整章作廢）

1. **不杜撰經文。** 中文只用和合本（CUV），英文只用 NASB 1995。`## 經文` 區塊已為你生成：`$S/scripture/units/NN.md`（NN＝你的章號），**原樣貼入**，不得改字。任何其他經文引用（交叉經文、詩篇、新約），**每一處**都先用 `python3 books/bible/habakkuk/sources/cuv.py '書 章:節'` 查出和合本再引；查不到就改述不引號。書卷簡稱用 fhl 的：創 出 利 民 申 書 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 詩 箴 傳 歌 賽 耶 哀 結 但 何 珥 摩 俄 拿 彌 鴻 哈 番 該 亞 瑪 太 可 路 約 徒 羅 林前 林後 加 弗 腓 西 帖前 帖後 提前 提後 多 門 來 雅 彼前 彼後 約壹 約貳 約參 猶 啟。（和合本的措辭常與記憶中不同——例如啟6:10 是「要等到幾時呢」不是「要到幾時呢」——所以一定要查。）
2. **不杜撰注疏。** 凡加引號並歸給某人的英文句子，必須是 `$S/commentary/` 下來源檔裏的逐字句子（空白／大小寫／標點不拘，用字必須一字不差）。**只從來源檔複製，不憑記憶寫。** 寫完立刻跑第 5 節的驗證指令。不能驗證的，改成不加引號的綜述。**中文句子若是你自己翻的注疏，不加「」**（用不加引號的轉述，或放在英文引文下方的「中譯：」行）。
3. **不杜撰老弟兄的話。** 倉庫裏沒有老弟兄論哈巴谷書的記錄。「老弟兄查經」一節是把他的**方法**（提問式帶領、精義一句話、全經連線、今天的祭壇、「你看見耶穌了嗎」）應用在本章。可以加引號歸給他的，**只有**以下白名單（`.claude/skills/ask-elder-wong/references/voice.md`），且中文一律寫「裏」不寫「裡」：
   - 「你研讀聖經，卻沒有看見耶穌——那本書等於白讀了。」
   - 「字句叫人死，精義叫人活。」
   - 「知識叫人自高。屬靈的人，聖經懂得很多的人，往往是相當自高的人。」
   - 「先把這章一口氣讀完，不要停。」
   - 「躺在青草地上，是羊在反芻——你的讀經是反芻嗎？」
   - 「有什麼讓你心裏有感動？不是你想出來的，是聖靈光照的。」
   - 「哪裏有信，哪裏就有聖靈的工作；哪裏有不信，哪裏就有撒旦的工作。」
   - 「我們照著神的意思去做，神就負責；照著我的意思去做，我要負責。」
   - 「不是我們去建立教會，是你手上有沒有釘痕的手。」
   - 「人能創造的只有在腦袋裏面。我們今天不是創造了AI，而是製造了AI。創造，唯有神能。」
   - 「創世記——道創造萬物。約翰福音——道成了肉身。啟示錄——那騎白馬的，名字叫神之道。整本聖經從頭到尾，主角只有一位。」
   - 範例章已用：「有什麼讓你心裏有感動」（第1章）。**每句語錄全書最多用一次**；每章用 0-1 句，用在真正貼切處，不要硬塞。
4. **不替哈巴谷書補上經文沒有的細節。** 先知的年代、身世、他當時的處境、迦勒底人入侵的日期，經文沒說的，就說「經文沒有說」，並如範例章那樣把注釋家的主張標為「讀法」。
5. **不把經文寫成預表來湊結論。** 新約**明引**哈巴谷書的只有四處：徒13:41（引哈1:5）、羅1:17／加3:11（引哈2:4）、來10:37-38（引哈2:3-4）。其他對應（如啟示錄）若寫，必須標明是「並讀」或「教會歷來的一種讀法」，並說明經文本身沒有明說。
6. **繁體中文；用「裏／那裏／甚麼」，不用「裡／那裡／什麼」；專名依和合本（迦勒底、利巴嫩、提幔、巴蘭山、古珊、米甸）；間隔號用「·」；避免 AI 腔、空洞套話、emoji。**
7. 你**只能**寫你被指派的章節檔。不要碰其他檔案、不要跑 build、不要 git commit／add、不要改 `$S` 裏的任何檔案。（暫存檔放 `/tmp/`）
8. **同一個點全章只講一次。** 各小節各司其職，不重複（見 `.claude/skills/eat-bible/references/chapter-template.md`）。
9. **全書去重：** 每一句注疏引文在全書只能出現一次。你只用你這章**專屬**的引文（見第 4 節分配），不要用別章分配到的。
10. **字數、次數、位置只用 `$S/keyword-counts.txt`（`python3 books/bible/habakkuk/sources/count_hebrew.py` 可重現）與 `$S/hebrew.tsv`**，不要自己重數。凡寫「全書N次」「唯一」「只有」「最後」這類絕對語，必須是你剛用工具證實的；證實不了就改成「在這卷書裏出現於 X、Y」。
11. **字義說明**（原文研讀表）：只寫詞的基本意義、字根、出現處；**不要寫「BDB 說…」「辭典說…」**（本書字義尚未對照辭書，附錄如實交代）。

## 1. 全書骨幹（每章都要與它對上）

**書名**：哈巴谷書研讀。**全書一句話**：先知對神提出三項控告——不聽、不救、使我看見（1:2-3）；神用兩次回答和一個異象，把這三個動詞在第3章一個一個還給他：我聽見了（3:2、3:16）、神的拯救（3:8、3:13、3:18）、我看見了（3:6-7、3:10）。問題沒有被解釋掉，先知被帶到另一個地方站著：然而，我要因耶和華歡欣。

**人的軌跡**：控告（1:2-4）→ 神的回答超過他所求（1:5-11）→ 再問，然後上守望所（1:12-2:1）→ 神說：寫下、等候、義人因信得生（2:2-5）→ 五個「禍哉」，一個肅靜（2:6-20）→ 先知聽見、禱告、看見神來（3:1-15）→ 身體戰兢，嘴唇顫動，仍說「然而」（3:16-19）。

**神的次序（五步）**——每個「卷首扉頁」與「座標」行用的結構：

| 步 | 經文 | 章 | 神在做甚麼 |
|---|---|---|---|
| 第一步 | 1:1-4 | 第1章 | 神讓先知先開口：三項控告被收進正典，沒有刪，沒有責備 |
| 第二步 | 1:5-11 | 第2章 | 神的回答比問題更大：「我行一件事」，興起迦勒底人；你們總是不信 |
| 第三步 | 1:12-2:1 | 第3章 | 先知再問（你眼目清潔，為何看著不理），然後不再追問，上守望所等候 |
| 第四步 | 2:2-20 | 第4-5章 | 神再次開口：寫下異象、等候、義人因信得生；然後是五個禍哉，與「全地都當在他面前肅敬靜默」 |
| 第五步 | 3:1-19 | 第6-7章 | 先知聽見了：禱告、神來了、然而歡欣——三項控告都被回答，問題仍在，人站在高處 |

**經文數字（WLC＋OSHB 詞元計算；全表見 `$S/keyword-counts.txt`，可重現）**：
- 聽見 שָׁמַע（動詞）三次：1:2（你不聽）、3:2（我聽見了）、3:16（我聽見了）。另名詞 שֵׁמַע「名聲／所聽見的」3:2。
- 拯救：動詞 יָשַׁע 1:2（你還不拯救）；名詞 יֵשַׁע 3:13（兩次）、3:18（我的拯救）；יְשׁוּעָה 3:8。**一次在控告裏，四次在第3章。**
- 看見：רָאָה 七次：1:3、1:5、1:13、2:1、3:6、3:7、3:10；נָבַט（看、觀望）五次：1:3、1:5、1:13（兩次）、2:15；צָפָה（守望）2:1；חָזָה（所得的異象）1:1、חָזוֹן 2:2-3。
- 強暴 חָמָס 六次：1:2、1:3、1:9、2:8、2:17（兩次）。（創6:11「地上滿了強暴」也是這個字。）
- 禍哉 הוֹי 五次：2:6、2:9、2:12、2:15、2:19。
- 義人 צַדִּיק 三次：1:4（被圍困）、1:13（被吞滅）、2:4（必因信得生）；惡人 רָשָׁע 三次：1:4、1:13、3:13。
- 「出來」 יָצָא 五次：1:4（兩次：公理不出來／顛倒的公理出來）、1:7（迦勒底人的判斷勢力都從自己發出）、3:5（熱症發出）、3:13（你出來要拯救你的百姓）。
- 「來」 בּוֹא 六次：1:8、1:9（迦勒底人）、2:3（兩次：必然臨到）、3:3（神從提幔而來）、3:16（戰兢入我的骨）。
- 「行事／工作」 פָּעַל：1:5（我行一件事）、3:2（求你復興你的作為）。
- 「活／復興」 חָיָה：2:4（義人必活）、3:2（求你復興）。אֱמוּנָה 只在 2:4。
- 「地」 אֶרֶץ 十次：1:6、2:8、2:14、2:17、2:20、3:3、3:6、3:7、3:9、3:12。
- 「細拉」 三次：3:3、3:9、3:13。「列國」 גּוֹי 七次；「眾民」 עַם 六次。
- 耶和華 יהוה 十二次（詞元計）；「我的神」「我的拯救」3:18。
- **希伯來文的節號與和合本一致**（哈巴谷書沒有節號差）。

**不可壓平的張力（遇到就保留，不要為了整齊抹平）**：
1. 先知在1:2-4 控告的是誰——猶大內部的強暴（加爾文、亨利的讀法）還是迦勒底人（另一些讀法）；經文本身以第6節為界，列為「讀法」，不替先知決定。
2. 神用不義的迦勒底人去審判神的百姓（1:6、1:12），先知的第二問（1:13）正是從這裏來；神**沒有**直接回答這一問，而是說寫下、等候（2:2-3）。不要替神補一個神義論的答案。
3. 2:4「因信」：אֱמוּנָה 的基本意思是穩固、信實（摩根：faithfulness）；保羅把它用在稱義（羅1:17；加3:11），希伯來書用在忍耐（來10:38）。三處用法各取一個面向，不要壓成一個。
4. 3:2 希伯來文「在這些年間」（בְּקֶרֶב שָׁנִים），與奧古斯丁所用拉丁譯本「在兩個活物之間」不同；引奧古斯丁時要標明他用的是另一個讀法。
5. 3:13「受膏者」（מְשִׁיחֶךָ）指誰，注釋家看法不同（百姓？大衛家的王？）；寫「彌賽亞」讀法時必須標明是並讀。
6. 先知最後沒有得到解釋：猶大仍要入俘擄（3:16「等候患難之日」）；歡欣不是因為處境改變。這是全書的誠實處，不要抹掉。
7. 3:17 的農作物失收，是約中咒詛的形象（申28:38-42），也可以是真實的飢荒；不要定於一種。

## 2. 章節計畫

| 檔案 | 經文 | 負責 | 標題（H1）| 配詩（公有領域，須自查原文）|
|---|---|---|---|---|
| 01-how-long.md | 1:1-4 | 主編（已完成）| 你不應允，要到幾時呢？ (How Long, and You Will Not Hear?) | Come, Ye Disconsolate |
| 02-a-work-you-would-not-believe.md | 1:5-11 | 代理A | 我行一件事，你們總是不信 (A Work You Would Not Believe) | A Mighty Fortress Is Our God（Luther／Hedge 1853）|
| 03-i-will-stand-at-my-watch.md | 1:12-2:1 | 代理A | 我要站在守望所 (I Will Stand at My Watch) | Rock of Ages, Cleft for Me（Toplady 1776）|
| 04-the-righteous-shall-live.md | 2:2-5 | 代理B | 義人必因信得生 (The Righteous Shall Live by His Faith) | I Know Not Why God's Wondrous Grace（Whittle 1883）|
| 05-woe-and-the-silence.md | 2:6-20 | 代理B | 禍哉！惟耶和華在他的聖殿中 (Woe, and the LORD in His Holy Temple) | Holy, Holy, Holy, Lord God Almighty（Heber 1826）|
| 06-i-have-heard-your-report.md | 3:1-15 | 代理C | 耶和華啊，我聽見了你的名聲 (I Have Heard the Report of You) | Mine Eyes Have Seen the Glory（Howe 1861）|
| 07-yet-i-will-rejoice.md | 3:16-19 | 代理C | 然而，我要因耶和華歡欣 (Yet I Will Rejoice in the LORD) | Cowper, "Sometimes a Light Surprises"（1779，從 Wikisource 取原文；取不到可核對的全文就改用 Peace, Perfect Peace，並在回報裏說明）|

**配詩查證：** 只用公有領域聖詩。取原文：`curl -sL -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36' 'https://en.wikisource.org/w/index.php?title=The_Army_and_Navy_Hymnal/Hymns/<詩名>&action=raw'`（詩名用底線代空格；頁面內有 `<pages index="The Army and Navy Hymnal.djvu" from=N to=N />`，再取 `https://en.wikisource.org/w/index.php?title=Page:The_Army_and_Navy_Hymnal.djvu/N&action=raw`，歌詞在 `<poem>` 內）。**Wikisource 會限流：每次請求間隔 6-8 秒。** 印本有錯字時，核對通行本，發現就在作者行註明。取 1-2 節即可，每節附你自己的中譯（中譯不加來源聲明，只在詩末作者行寫 text from …）。**不得**使用仍受版權保護的詩歌歌詞（會觸發內容過濾器）。

## 3. 每章格式（11 節，順序固定；範例章即格式）

```
YAML 7 行（原樣，與範例章相同）
# 中文標題 (English)
哈巴谷書 N:x-y                    ← 經文範圍行（用和合本節號；跨章寫 1:12-2:1）
**經文核對**：[ai-eden.com/bible/habakkuk/N](https://www.ai-eden.com/bible/habakkuk/N?t=CUV,NASB&cols=2)
## 基督焦點 (Christ at the Center)   > 鑰詞 + 全書座標 box（座標行必須有，且標明這章在「五步」的哪一步、與三個動詞的關係）+ 1-2 段
## 配詩 (Opening Hymn)
## 經文 (Scripture)               貼入 $S/scripture/units/NN.md；版本說明那一行照範例章
## 背景 (Context)                 2-3 個 ### 小節
## 原文研讀 (Word Study)          表（原文｜節｜意義），希伯來文用 `python3 books/bible/habakkuk/sources/heb.py 章:節` 取得（已去音調符號、保留母音點）
## 領受要點 (Truths Received)     3-4 條編號，每條必須是這一章專屬的，不能搬到別章
## 歷代注疏 (Historical Commentary)  > 體例說明 box（照範例章原文，保留「本卷沒有麥克阿瑟…」那句）+ 各家小標題
## 詩篇與聖詩 (Psalm & Hymn)
## 老弟兄查經 (Reading with the Elder Brother)  精義一句話 / ### 全經連線（2-4 條）/ ### 提問式對話（先問・再問・追問・落到自己）/ ### 活在今天·AI時代 / ### 今天的祭壇（早晨・晚上・一個行動）/ **你看見耶穌了嗎**（最後一段，必須含這五個字）
## 生命應用 (Application)         ### 默想問題（≤3，與提問式對話不重複）/ ### 禱告回應
## 與其他經文的關聯              表
*本章研讀整合：…*（尾行，格式照範例章，列出本章實際用到的來源）
```
- 經文區塊的 `^n^` 標記、斜體 `*word*` 不動。
- 原文研讀表分隔列要夠寬（原文欄 ≥20 個 dash）。表裏凡放希伯來文，意義欄不要貼著不換行的長拉丁字。
- 行文中引用經文，加引號的和合本句子一律與 `cuv.py` 輸出逐字相同（可截取其中連續的一段，不可改字；非經文的詞組用『』，不用「」）。
- 英文標題 H1 用括號英文；希伯來文用在表格與行文，音譯用拉丁字母時給中文釋義。
- 長度：每章 18,000–23,000 bytes（範例章 19,900）。第4、5、6章可到 26,000。不要灌水。
- 「領受要點」「提問式對話」「默想問題」三處不得重複同一個問題或同一個結論。
- 「活在今天·AI時代」寫具體觀察，不空談；不說沒有根據的事實（例如不編造某公司、某事件、某統計）。

## 4. 注疏來源與每章專屬配給（`$S/commentary/`）

| 來源檔 | 作者／出處（引文出處行照寫）|
|---|---|
| `calvin-habakkuk.txt` | John Calvin, *Commentaries on the Twelve Minor Prophets*, vol. 4 (Habakkuk, Zephaniah, Haggai), tr. John Owen (Edinburgh: Calvin Translation Society, 1848), on Habakkuk N:v。**索引 `calvin-index.txt`（行號＝本檔行號）。檔裏有 `[數字]` 編號的譯者／編者註腳（常以 `--Ed.` 結尾），那不是加爾文，不得引為加爾文。** 出版年份我們未核對原書，引文出處行**不寫年份**（照範例章：只寫書名、卷、譯者、經節）。 |
| `henry-habakkuk.txt` | Matthew Henry, *An Exposition of the Old and New Testament*, on Habakkuk N:v（亨利親撰）。檔內 `##### FILE i`＝導論（行1-151，**留給主編**）、`ii`＝第1章（行152-340）、`iii`＝第2章（行341-543）、`iv`＝第3章（行544起）。 |
| `morgan-living-messages-habakkuk-ocr1.txt`／`ocr2.txt` | G. Campbell Morgan, "The Message of Habakkuk," *Living Messages of the Books of the Bible* (New York: Fleming H. Revell, 1912), p. N。兩份是同書不同掃描的 OCR；頁碼見檔內「THE MESSAGE OF HABAKKUK 2NN」頁眉（頁眉在左或右，數字就是頁碼；273 起，286 止）。OCR 有錯字，引文必須以掃描為準，逐字核對（驗證指令會先做 OCR 正規化）。摩根這章只到第286頁，只講到 2:4 與等候，**對 1:5-11 與 3:1-15 幾乎沒有逐節解經**，所以那些章可以不引摩根（在體例說明裏照實寫「本章沒有摩根逐節論述」即可，不要硬湊）。 |
| `augustine-cityofgod-18-32-33.txt` | Augustine, *The City of God*, Book 18, ch. 32 ("Of the Prophecy that is Contained in the Prayer and Song of Habakkuk"), tr. Marcus Dods（New Advent 電子版；只引到章號，不編頁碼）。**他用的是拉丁（七十士譯本系統）的讀法，不是希伯來文**，引用時必須標明。供第6、7章。 |

**每章專屬（不得越界）**
- **第2章（1:5-11）**：加爾文行 384-975（1:5-11）；亨利第1章「I. The preamble…」「II. The sentence…」兩段（檔行175-190）；摩根：不引。
- **第3章（1:12-2:1）**：加爾文行 976-1949；亨利第1章「The prophet, having received…」至結尾（檔行191-210）；摩根 p.283-284（「Habakkuk might have started out as a lecturer…」「He poured out his heart…」「The best place to speak of the secret problem is the Secret Place」「Men do not listen to-day as they listened of old. If men will listen, God will speak」）與 p.285-286（「How shall I wait? On the watch-tower, telling God everything, and listening to God.」）。**第1章已用 p.284「Oh, the comfort…」不得重複。**
- **第4章（2:2-5）**：加爾文行 1950-2962；亨利第2章 2:1-5 段（檔行341-372）；摩根 p.275-281（含 p.277 faithfulness 的翻譯討論、p.278「what is fidelity other than fullness of faith?」、p.280「He shall live」、p.281「Faith is the principle of life in spite of all appearances. Pride is destructive in spite of all appearances.」）與 p.285「Have you never discovered that waiting is the hardest of all work?」（跨頁到 286）。**p.273-275 的敘述留給主編。**
- **第5章（2:6-20）**：加爾文行 2963-4657；亨利第2章「I. The charge… II. The sentence…」之後的各禍（檔行372-420）；摩根 p.282（「The keen satire of Habakkuk is poured upon idolatry…」「Violence issues in self-destruction.」等）。
- **第6章（3:1-15）**：加爾文行 4658-6150；亨利第3章（檔行544-600，到「V./VI.」六項為止）；摩根 p.283（「He who had thought God was doing nothing to punish evil, now prays that in the midst of wrath He will remember mercy.」「Then he illustrates the life of faith. There is first the vision of God coming from Teman.」）；奧古斯丁 18.32 中論 3:2-15 的句子（約從「In his prayer, with a song」至「You have sent into the sea Your horses」）。
- **第7章（3:16-19）**：加爾文行 6151-6556；亨利第3章末段（檔行601-612，「I. The prophet had foreseen… II. He had looked back…」）；摩根 p.275（「Habakkuk does not end with a wail; he ends with a song.」「That is faith's agnosticism, belief's problem.」）與 p.283（「The living message is perfectly patent. Faith has still its problems.」）；奧古斯丁 18.32 中論 3:16-19 的句子（約從「I gave heed, and my belly trembled」到結尾，含「some copies have, I will joy in God my Jesus」）。
- **留給主編（卷首與附錄）**：亨利導論（檔 `FILE i`）、摩根 p.273-275 的「That is the story of Habakkuk」「Opening in mystery and questioning, it closes in certainty and affirmation」、加爾文 Preface（檔行 1-55）。

## 5. 驗證（你寫完、回報前必須全跑，把結果貼在回報裏）

```
cd /Users/jimxiao/dev/pubhub
S=books/bible/habakkuk/sources/commentary
python3 scripts/verify-citations.py books/bible/habakkuk --source $S/calvin-habakkuk.txt --heading 加爾文
python3 scripts/verify-citations.py books/bible/habakkuk --source $S/henry-habakkuk.txt --heading 亨利
python3 scripts/normalize-ocr-source.py $S/morgan-living-messages-habakkuk-ocr1.txt /tmp/mh1-$$.txt >/dev/null
python3 scripts/normalize-ocr-source.py $S/morgan-living-messages-habakkuk-ocr2.txt /tmp/mh2-$$.txt >/dev/null
cat /tmp/mh1-$$.txt /tmp/mh2-$$.txt > /tmp/morgan-$$.txt
python3 scripts/verify-citations.py books/bible/habakkuk --source /tmp/morgan-$$.txt --heading 摩根
python3 scripts/verify-citations.py books/bible/habakkuk --source $S/augustine-cityofgod-18-32-33.txt --heading 奧古斯丁
python3 scripts/verify-prose-citations.py books/bible/habakkuk --self 哈
python3 scripts/lint-chapter-markup.py books/bible/habakkuk
python3 scripts/lint-scripture-text.py books/bible/habakkuk
```
（腳本會掃整個目錄，別人的章節出現 MISS 與你無關；只看你的檔。）每條 `MISS`／`DRIFT` 都必須修成 `OK`，或改成不加引號的綜述。`verify-prose-citations` 把「引號＋出處」配對，行文中非經文的詞組請用『』；跨節引句出處寫成範圍。再用 `diff <(sed -n '/^## 經文/,/^## 背景/p' 你的檔) ...` 確認經文區塊與 `$S/scripture/units/NN.md` 一致（你的檔多了 `## 經文`、版本說明與 `---` 等包裝行，只比經文兩段即可）。

另外，**交叉比對全書去重**：你每一句注疏英文引文，用 `grep -rl "那句的前八個字" books/bible/habakkuk/*.md` 確認只出現在你自己的檔。

## 6. 回報格式（≤250 字）

1. 檔名與 bytes；2. 驗證腳本輸出的 OK/MISS/DRIFT 計數；3. 你引用了哪些交叉經文（書章節清單，每條都已用 cuv.py 查過）；4. 配詩出處與核對方式；5. **旗標**：你不確定、或來源與預期不符、或你認為需要主編裁決的地方（最重要）。不要貼整章內容。

## 7. 工作方式

- 先讀範例章與本檔，再讀你的來源檔對應段落（用 `grep -n` 找行號，用 Read 的 offset/limit 讀），**分段寫入**：先 Write 前半（到「歷代注疏」），再用 Edit 接後半。不要單次寫入整章（會停滯）。
- 希伯來文詞：先 `python3 books/bible/habakkuk/sources/heb.py N:v` 看原文，再選詞；次數只用第1節 `keyword-counts.txt`。
- 寫之前先想「這段經文在整卷書裏做的那一件事」，章的精義一句話、基督焦點、全經連線要對上它。下面是主編讀完來源後對各章的重點提示（**是方向，不是結論**；每一條仍須你自己從經文與來源檔核對，核對不了就不寫）。

### 各章重點提示

**第2章（1:5-11）**：神對控告的回答，第一個動作是叫人「觀看」（רְאוּ 複數命令，1:5）；「我行一件事」（פֹּעֵל פֹּעַל，分詞，正在進行）——同一字根到 3:2 變成先知的祈求「求你復興你的作為」。「你們總是不信」（1:5）→ 徒13:40-41 保羅引用（用 cuv.py 查徒13:38-41）。迦勒底人的描寫（1:6-11）：殘忍暴躁、馬比豹快、為行強暴而來（חָמָס，1:9 同一字）、以自己的勢力為神（1:11，伏筆到1:16 向網獻祭）。1:7「判斷和勢力都任意發出」用的是「出來」（יצא），與1:4 公理不出來對看。賽10:5-7（亞述是神怒氣的杖）、耶25:9（尼布甲尼撒是神的僕人）可並讀（先查和合本）。這一章要處理的難處：神用不義之民審判自己的民；加爾文、亨利怎樣處理「神的工具自己仍要負責」（1:11 的「顯為有罪」）。

**第3章（1:12-2:1）**：先知在發問之前先背信條（1:12：你不是從亙古而有嗎？我的神，我的聖者）；然後才問（1:13：你眼目清潔，為何看著不理——נבט 再現，呼應1:3）。1:14-17 的「網」：人如海中的魚，迦勒底人向網獻祭——倚靠自己工具與成果的偶像（AI 時代可具體寫：人把自己造出來的工具當成神，但不編造事實）。2:1 的守望：三個動詞站、立、觀看（עמד、יצב、צפה），「看耶和華對我說甚麼話」，以及「我可用甚麼話向他訴冤」的歧義（תּוֹכַחְתִּי，和合本小字「或譯回答所疑問的」；NASB "when I am reproved"）——保留兩讀。呼應彌7:7（用 cuv.py 查，字面結構近似：守望、等候、救我的神、必應允我）、賽21:8、結3:17、詩130:5-6。基督：來1:1-2（神在這末世藉著兒子曉諭我們）。

**第4章（2:2-5）**：寫下異象（2:2「使讀的人容易讀」，和合本小字「或譯：隨跑隨讀」）；異象「快要應驗，並不虛謊；雖然遲延，還要等候；必然臨到，不再遲延」（2:3），來10:37 把「必然臨到」讀成「那要來的」。2:4 是全書的鑰節：驕傲的人「心不正直」vs 義人「因信（אֱמוּנָה，信實）得生」；摩根整段討論翻譯。1:4（惡人圍困義人）與 2:4（義人必活）用同一個字「義人」：同一個人，從被圍困到必活。三處新約引用各取不同面向（羅1:17、加3:11、來10:38），查 cuv.py。老弟兄白名單「哪裏有信，哪裏就有聖靈的工作」可用在這章。「義者」是基督的稱號：徒3:14、7:52、22:14（查和合本）。

**第5章（2:6-20）**：五個「禍哉」：2:6-8 擄掠與債；2:9-11 不義之財與高處的窩，牆裏的石頭必呼叫；2:12-14 以人血建城；2:15-17 使鄰舍喝醉，耶和華右手的杯必傳到你；2:18-19 對木偶說「醒起」。2:8 與 2:17 的副歌近乎相同（「因你殺人流血，向國內的城並城中一切居民施行強暴」）。**2:14 在五禍正中：「認識耶和華榮耀的知識要充滿遍地，好像水充滿洋海」——和創6:11「地上滿了強暴」用同一個動詞「充滿」，是對強暴的答案。**2:20「惟耶和華在他的聖殿中，全地都當在他面前肅敬靜默」——對照木偶「沒有氣息」（2:19）；啟8:1、番1:7、亞2:13 可並讀。「杯」：賽51:17、太26:39、啟14:10 並讀。老弟兄白名單「人能創造的只有在腦袋裏面……」用在這章（2:18-19，製造偶像者倚靠自己所造的）最貼切。巴比倫的結局（但5章、賽21:9、啟18:2）。

**第6章（3:1-15）**：整章是祈禱（תְּפִלָּה，3:1），歌的標記（על שגינות、細拉三次、3:19 的伶長）。3:2 的轉折：「我聽見了你的名聲就懼怕」，所求的是「求你復興你的作為」——就是1:5 那件他不信的事；「在忿怒中以憐憫為念」（רַחֵם）。3:3-15 的神顯現沿用出埃及、西乃、約書亞的意象：提幔與巴蘭山（申33:2；士5:4）、瘟疫在前頭（出）、日月停住（書10:12-13）、紅海（出15）。3:8「你乘在馬上，坐在得勝（יְשׁוּעָה）的車上」→ 啟19:11（騎白馬者稱為誠信真實）；老弟兄白名單「創世記——道創造萬物……那騎白馬的，名字叫神之道……」可用。3:13「你出來要拯救你的百姓」——「出來」（יצא）與1:4 公理不出來、神自己出來對看。奧古斯丁對3:2-15 的逐句基督論解讀要標明用的是拉丁讀法；他說「在兩個活物之間」與希伯來文「在這些年間」不同。

**第7章（3:16-19）**：先知的身體：肚腹戰兢、嘴唇顫動、骨中朽爛、我在所站之處發抖（3:16）；仍「安然等候」（אָנוּחַ）患難之日。3:17 六件失去；3:18「然而我要……」。「救我的神」אֱלֹהֵי יִשְׁעִי 與「耶穌」同字根（太1:21：你要給他起名叫耶穌）；奧古斯丁18.32 的「God my Jesus」那句要用上，並標明是他所用的拉丁抄本讀法，與和合本、NASB 不同。3:19「使我穩行在高處」。1:2 的「你還不拯救」→ 3:18 的「救我的神」，全書的回答是一個名字。處境沒有變（猶大仍要入俘擄）。基督：來12:2（為那擺在前面的喜樂，忍受了十字架的苦難）、羅5:3（查和合本措辭）。這一章同時是全書的結尾：結尾行要把五步收到「你看見耶穌了嗎」。

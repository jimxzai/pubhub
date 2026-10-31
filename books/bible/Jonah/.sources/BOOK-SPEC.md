# 約拿書研讀 — BOOK-SPEC（給寫章節的代理）

範例章：`books/bible/Jonah/01-arise-and-flee.md`（先完整讀一遍；你的章節格式、語氣、密度都照它）。
已通過 verify-citations（加爾文／亨利／摩根）、lint-chapter-markup。

## 0. 硬規則（違反任何一條整章作廢）

1. **不杜撰經文。** 中文只用和合本（CUV），英文只用 NASB 1995。`## 經文` 區塊已為你生成：`.sources/scripture/NN.md`（NN＝你的章號），**原樣貼入**，不得改字。任何其他經文引用（交叉經文、詩篇、新約），**每一處**都先用 `python3 .sources/cuv.py '書 章:節'` 查出和合本再引；查不到就改述不引號。書卷簡稱用 fhl 的：創 出 利 民 申 書 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 詩 箴 傳 歌 賽 耶 哀 結 但 何 珥 摩 俄 拿 彌 鴻 哈 番 該 亞 瑪 太 可 路 約 徒 羅 林前 林後 加 弗 腓 西 帖前 帖後 提前 提後 多 門 來 雅 彼前 彼後 約壹 約貳 約參 猶 啟。
2. **不杜撰注疏。** 凡加引號並歸給某人的英文句子，必須是下列來源檔裏的逐字句子（空白／大小寫／標點不拘，用字必須一字不差）。**只從來源檔複製，不憑記憶寫。** 寫完立刻跑第 5 節的驗證指令。不能驗證的，改成不加引號的綜述。
3. **不杜撰老弟兄的話。** 倉庫裏沒有老弟兄論約拿書的記錄。「老弟兄查經」一節是把他的**方法**（提問式帶領、精義一句話、全經連線、今天的祭壇、「你看見耶穌了嗎」）應用在本章，**不得**把任何句子加引號歸給他。
4. **不替約拿書補上經文沒有的細節。** 魚的種類、約拿得救後的心情、尼尼微王的名字、尼尼微悔改的歷史證據——經文沒說的，就說「經文沒有說」。
5. **不把約拿寫成基督的預表來湊結論。** 新約**明說**的對應只有太12:39-41／路11:29-32（三日三夜、尼尼微人悔改、「有一人比約拿更大」）。其他對應（例如1:12投海代替船上的人）若寫，必須標明是「教會歷來的一種讀法」並說明經文本身沒有明說；加爾文（來源檔 Lecture 72）就主張約拿作預表只在「從死裏回來」這一點。
6. **繁體中文；用「裏／那裏／甚麼」，不用「裡／那裡／什麼」；專名依和合本（約帕、他施、尼尼微、亞米太）；間隔號用「·」；避免 AI 腔、空洞套話、emoji。**
7. 你**只能**寫你被指派的章節檔。不要碰其他檔案、不要跑 build、不要 git commit／add、不要改 `.sources/` 裏的任何檔案。
8. **同一個點全章只講一次。** 各小節各司其職，不重複（見 `.claude/skills/eat-bible/references/chapter-template.md`）。
9. **全書去重：** 每一句注疏引文在全書只能出現一次。你只用你這章**專屬**的引文（見第 4 節分配），不要用別章分配到的。

## 1. 全書骨幹（每章都要與它對上）

**書名**：約拿書研讀。**全書一句話**：神的話兩次臨到一個逃跑的先知；神用風、籤、魚、蓖麻、蟲、東風，一件一件「安排」；書的最後一句，不是約拿的回答，是神的問題——「我豈能不愛惜呢？」

**人的軌跡**：起來逃（קוּם，1:3）→ 一路往下（ירד×4：1:3 兩次、1:5、2:6）→ 魚腹中才第一次禱告（2:1-2）→ 照話起來去（3:3）→ 發怒、求死（4:1-3、8-9）→ 沒有回答（4:11 後）。

**神的次序（四步）**——這是每個「卷首扉頁」與「座標」行用的結構：
| 步 | 經文 | 章 | 神在做甚麼 |
|---|---|---|---|
| 第一步 | 1:1-16 | 第1-3章 | 神先開口，也先動手：話臨到；風、籤、海都聽從，只有先知不聽；連水手都認識了耶和華 |
| 第二步 | 1:17-2:10 | 第4章 | 預備在先，禱告在後：魚是「安排」的（1:17），然後才有禱告（2:1）；「救恩出於耶和華」（2:9） |
| 第三步 | 3:1-10 | 第5-6章 | 話第二次臨到，重新差遣不加責備；尼尼微悔改，神「後悔」（3:10） |
| 第四步 | 4:1-11 | 第7-8章 | 神以問題收尾：約拿引出神的恩慈作為自己逃的理由；神安排蓖麻、蟲、東風，最後問「我豈能不愛惜呢？」 |

**經文數字（OSHB 詞元計算，節號為和合本節號；全表見 `.sources/keyword-counts.md`）**：
- 神說話（直接向約拿）：兩次命令（1:2、3:2），其餘都是問句（4:4、4:9、4:11）。
- 「安排」מנה 四次：魚（1:17）、蓖麻（4:6）、蟲（4:7）、東風（4:8）。（CUV 全用「安排」；NASB 全用 appointed。）
- 「下去」ירד 四次：1:3（兩次）、1:5、2:6。「拋／投」טול 四次：1:4（神）、1:5（水手拋貨）、1:12（約拿請求）、1:15（水手）。
- 「大」גדול 十四次：1:2、1:4（兩次）、1:10、1:12、1:16、1:17、3:2、3:3、3:5、3:7、4:1、4:6、4:11。
- 「惡／災」רעה 九次：1:2、1:7、1:8、3:8、3:10（兩次）、4:1、4:2、4:6。
- 「起來」קום 六次：1:2、1:3、1:6、3:2、3:3、3:6。「逃」ברח 三次：1:3、1:10、4:2。
- 「懼怕」ירא（動詞）三次：1:5、1:10、1:16；加上1:9形容詞「敬畏」共四處。
- 「愛惜／憐惜」חוס（CUV「愛惜」，NASB compassion）兩次：4:10（約拿對蓖麻）、4:11（神對尼尼微）。
- 「發怒」חרה 四次：4:1、4:4、4:9（兩次）。「後悔／轉意」נחם 三次：3:9、3:10、4:2。「回轉／回頭」שוב 五次：1:13（水手想划回岸）、3:8、3:9（兩次）、3:10。
- 神的名：יהוה 二十六次、אלהים 十六次；第四章 4:6 是全書唯一的「耶和華神」（יהוה אלהים），4:7-9 是「神」。
- 尼尼微的警告只有五個希伯來字：עוֹד אַרְבָּעִים יוֹם וְנִינְוֵה נֶהְפָּכֶת（3:4）。נֶהְפָּכֶת「傾覆」可指毀滅，也可指翻轉改變；經文沒有明說作者要的是哪一個，寫的時候只能說「這個字兩面都能讀」。
- 希伯來文版本第2章節號和合本差一節（和合本1:17＝希伯來文2:1；和合本2:1-10＝希伯來文2:2-11）。`.sources/hebrew.tsv` 有雙節號。

**不可壓平的張力（遇到就保留，不要為了整齊抹平）**：
1. 歷史性：本書依聖經本身與耶穌的用法（太12:40-41）讀為歷史敘事；現代有「寓言／諷刺」讀法，列為他人的主張，不駁斥也不採用，只點出耶穌自己怎麼用。
2. 尼尼微的悔改有多深：耶穌說他們「悔改了」（太12:41）；加爾文（來源 Lecture 72）說他不知道那是不是「真正的悔改」，因為後來尼尼微對以色列「十分敵對」。兩者並存，不調和。鴻3:1 是後來的審判。
3. 神「後悔」（נחם 3:10）與神不後悔（民23:19；撒上15:29）：兩種說法都在經上。加爾文處理過（Lecture 78-79），可引。
4. 約拿2章的禱告是不是悔改：禱告裏沒有認罪，也沒有承諾去尼尼微；只有感謝與還願（2:9）。不要替他補。
5. 約拿書結尾不給答案——4:11 之後沒有約拿的回應。不要替他寫回應。

## 2. 章節計畫

| 檔案 | 經文 | 負責 | 標題（H1）| 配詩（公有領域，須自查原文）|
|---|---|---|---|---|
| 01-arise-and-flee.md | 1:1-3 | 主編（已完成）| 起來去，他卻起來逃 | Come, Thou Fount（Robinson 1758）|
| 02-the-lord-hurled-a-wind.md | 1:4-10 | 代理A | 耶和華使海中起大風 (The LORD Hurled a Great Wind) | Eternal Father, Strong to Save（Whiting 1860）|
| 03-throw-me-into-the-sea.md | 1:11-16 | 代理A | 將我拋在海中 (Throw Me Into the Sea) | Master, the Tempest Is Raging（Mary A. Baker 1874）或 Jesus, Savior, Pilot Me（Hopper 1871）|
| 04-the-appointed-fish.md | 1:17-2:10 | 代理B | 耶和華安排一條大魚 (The LORD Appointed a Great Fish) | Jesus, Lover of My Soul（C. Wesley 1740，取 Other refuge 一段）|
| 05-the-second-time.md | 3:1-4 | 代理C | 話二次臨到約拿 (The Word Came the Second Time) | Amazing Grace（Newton 1779）|
| 06-nineveh-turns.md | 3:5-10 | 代理C | 他們離開惡道，神就後悔 (They Turned, and God Relented) | Depth of Mercy（C. Wesley 1740）|
| 07-is-it-right-to-be-angry.md | 4:1-4 | 代理D | 你這樣發怒合乎理嗎 (Do You Have Good Reason to Be Angry?) | Dear Lord and Father of Mankind（Whittier 1872，取 Drop thy still dews 段）|
| 08-the-last-question.md | 4:5-11 | 代理D | 我豈能不愛惜呢 (Should I Not Have Compassion?) | There's a Wideness in God's Mercy（Faber 1862）|

**配詩查證：** 只用公有領域聖詩。取原文：`curl -sL -A 'Mozilla/5.0 …' 'https://en.wikisource.org/w/index.php?title=Page:The_Army_and_Navy_Hymnal.djvu/<頁>&action=raw'`（目錄在 `https://en.wikisource.org/w/index.php?title=The_Army_and_Navy_Hymnal/Hymns/<詩名>&action=raw`，內有頁號）。印本有錯字（如範例章末行 from→for），引用前核對通行本，發現就在作者行註明。詩題不在 Army & Navy Hymnal 裏的，改選別的公有領域詩（作者卒於 1930 年前、明確公有）並寫明出處。**不得**使用仍受版權保護的詩歌歌詞（會觸發內容過濾器）。

## 3. 每章格式（11 節，順序固定；範例章即格式）

```
YAML 7 行（原樣，與範例章相同）
# 中文標題 (English)
約拿書 N:x-y                     ← 經文範圍行（用和合本節號）
**經文核對**：[ai-eden.com/bible/jonah/N](https://www.ai-eden.com/bible/jonah/N?t=CUV,NASB&cols=2)
## 基督焦點 (Christ at the Center)   > 鑰詞 + 全書座標 box（座標行必須有，且標明這章在「四步」的哪一步）+ 1-2 段
## 配詩 (Opening Hymn)
## 經文 (Scripture)               貼入 .sources/scripture/NN.md；版本說明那一行照範例章
## 背景 (Context)                 2-3 個 ### 小節
## 原文研讀 (Word Study)          表（原文｜節｜意義），希伯來文用 `python3 .sources/heb.py 章:節` 取得（已去音調符號、保留母音點），可附一小段 **粗體標題。**說明
## 領受要點 (Truths Received)     3-4 條編號，每條必須是這一章專屬的，不能搬到別章
## 歷代注疏 (Historical Commentary)  > 體例說明 box（範例章原文，保留「本書沒有麥克阿瑟…」那句）+ 各家小標題
## 詩篇與聖詩 (Psalm & Hymn)
## 老弟兄查經 (Reading with the Elder Brother)  精義一句話 / ### 全經連線（2-4 條）/ ### 提問式對話（先問・再問・追問・落到自己）/ ### 活在今天·AI時代 / ### 今天的祭壇（早晨・晚上・一個行動）/ **你看見耶穌了嗎**（最後一段，必須含這五個字）
## 生命應用 (Application)         ### 默想問題（≤3，與提問式對話不重複）/ ### 禱告回應
## 與其他經文的關聯              表
*本章研讀整合：…*
```
- 經文區塊的 `^n^` 標記、斜體 `*word*` 不動。
- 原文研讀表分隔列要夠寬（原文欄 ≥20 個 dash）。表裏凡放希臘／希伯來字，意義欄不要貼著不換行的長拉丁字。
- 行文中引用經文，加引號的和合本句子一律與 `cuv.py` 輸出逐字相同。
- 英文標題 H1 用括號英文；Hebrew 用在表格與行文，音譯用拉丁字母（chesed 之類）時給中文釋義。
- 長度：每章 18,000–23,000 bytes（範例章 18,973）。第4章可到 27,000。不要灌水。

## 4. 注疏來源與每章專屬配給（`.sources/`）

| 來源檔 | 作者／出處（引文出處行照寫）|
|---|---|
| `calvin-jonah.txt` | John Calvin, *Commentaries on the Twelve Minor Prophets*, vol. 3 (Jonah, Micah, Nahum), tr. John Owen (Edinburgh: Calvin Translation Society, 1847), on Jonah N:v。Lecture 72（1:1-2 前）… Lecture 78（3:6-8）… 4:1 起在檔案約 4259 行。**檔裏有編者 Ed. 註腳與譯者序（John Owen 自己的話），那不是加爾文，不得引為加爾文。**|
| `henry-mhc-jonah.txt` | Matthew Henry, "An Exposition, with Practical Observations, of the Book of the Prophet Jonah," in *Commentary on the Whole Bible*, vol. 4, on Jonah N:v（約拿書是亨利親撰）|
| `morgan-exposition-jonah-N.txt`（N＝1-4）| G. Campbell Morgan, *An Exposition of the Whole Bible* (New York: Fleming H. Revell, 1959), on Jonah N。每章只有 1-3 段；只引正文段落（有 20+ 字的句子），不引網頁選單雜訊 |
| `morgan-message-of-jonah.txt` | G. Campbell Morgan, "The Message of Jonah"（SermonIndex 收錄講稿；大綱體，來源為轉錄稿，出處行加注「轉錄稿，未見原書頁碼」）— 只供第7、8章 |
| `augustine-letter102-jonah.txt` | Augustine, Letter 102 (To Deogratias), Question VI, §§30-37, tr. J. G. Cunningham, *NPNF* 1st series, vol. 1（New Advent 電子版；只引到節號，不編頁碼）— 供第4、6章 |

**每章專屬（不得越界）**
- 第2-3章（代理A）：加爾文 Lecture 72（1:3 之後）-73-74；亨利 1:4-16；摩根 exp-1 第二段（"Jehovah sent out a wind…"那段）。**沒有教父可引，不列「教父時期」小節**。
- 第4章（代理B）：加爾文 Lecture 75-76（2章）與他論太12:39 的那段（Lecture 72 內，只有**一處**，歸第4章不歸第1章）；亨利 1:17-2:10；摩根 exp-2；奧古斯丁 Letter 102 §§30-35。需要「教父時期」小節。
- 第5-6章（代理C）：加爾文 Lecture 77-79；亨利 3章；摩根 exp-3；奧古斯丁 §§36-37（若有關於尼尼微悔改的句子，歸第6章）。第5章不引教父。
- 第7-8章（代理D）：加爾文 Lecture 80-81（4章）；亨利 4章；摩根 exp-4 與 message-of-jonah。第7、8章不引教父。

## 5. 驗證（你寫完、回報前必須全跑，把結果貼在回報裏）

```
cd /Users/jimxiao/dev/pubhub
S=books/bible/Jonah/.sources
python3 scripts/verify-citations.py books/bible/Jonah --source $S/calvin-jonah.txt --heading 加爾文
python3 scripts/verify-citations.py books/bible/Jonah --source $S/henry-mhc-jonah.txt --heading 亨利
cat $S/morgan-exposition-jonah-[1-4].txt $S/morgan-message-of-jonah.txt > /tmp/morgan-$$.txt
python3 scripts/verify-citations.py books/bible/Jonah --source /tmp/morgan-$$.txt --heading 摩根
python3 scripts/verify-citations.py books/bible/Jonah --source $S/augustine-letter102-jonah.txt --heading 奧古斯丁
python3 scripts/lint-chapter-markup.py books/bible/Jonah
python3 scripts/lint-scripture-text.py books/bible/Jonah
```
（腳本會掃整個目錄，別人的章節出現 MISS 與你無關；只看你的檔。）每條 `MISS`／`DRIFT` 都必須修成 `OK`，或改成不加引號的綜述。再用 `diff <(sed -n '/^## 經文/,/^## 背景/p' 你的檔) ...` 確認經文區塊與 `.sources/scripture/NN.md` 一致。

## 6. 回報格式（≤250 字）

1. 檔名與 bytes；2. 驗證腳本輸出的 OK/MISS/DRIFT 計數；3. 你引用了哪些交叉經文（書章節清單，每條都已用 cuv.py 查過）；4. **旗標**：你不確定、或來源與預期不符、或你認為需要主編裁決的地方（最重要）。不要貼整章內容。

## 7. 工作方式

- 先讀範例章與本檔，再讀你的來源檔對應段落（用 `grep -n` 找行號，用 Read 的 offset/limit 讀），**分段寫入**：先 Write 前半（到「歷代注疏」），再用 Edit 接後半。不要單次寫入整章（會停滯）。
- 希伯來文詞：先 `python3 .sources/heb.py N:v` 看原文，再選詞；次數只用第1節 `keyword-counts.md` 與 `hebrew.tsv`，不要自己重數。

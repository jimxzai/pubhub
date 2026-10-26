# 傳道書研讀 — 建卷計劃（2026-10-26）

slug `ecclesiastes`；目錄 `books/bible/ecclesiastes/`；build `scripts/build-ecclesiastes-consolidated.sh`；模板 `templates/pdf/ecclesiastes.latex`（由 nehemiah.latex 派生改色）。
12 章，H1 序號即真實章號（1–12），不會與經卷章號錯位。體例：11 節房規（見 .claude/skills/eat-bible/references/chapter-template.md）；範本＝尼希米記 / 路得記。

## 狀態（隨做隨記）
- [x] 經文源：sources/scripture/（FHL 和合本 → cuv.tsv；ai-eden 對校；cnbible 現代標點；biblehub NASB 1995）。222 節全到齊。`python3 extract.py && python3 apply_fixes.py` 重建；`inject_scripture.py <章> <檔>` 注入 `@@SCRIPTURE@@`。
- [x] 希伯來文：sources/hebrew/hebrew.tsv（Sefaria；已對齊英文節號：希 4:17＝英 5:1，希 5:n＝英 5:n+1）；`count.py` 可重跑計數。
- [x] 注疏源已下載：commentary/henry/henry-chNN.txt（CCEL mhc3.Ec；ch12 取 xiii 頁，導論取 i 頁）、commentary/bridges/bridges.txt（Bridges 1860，monergism PDF，已 normalize，章界見 "CHAPTER N"）、commentary/morgan-message-of-ecclesiastes.txt（Living Messages OT pp.57-69，頁碼取自頁眉）、commentary/fathers/gregory.txt（Gregory Thaumaturgus Metaphrase，ANF 6）、commentary/gty/*.txt（麥克阿瑟）
- [x] 聖詩 sources/hymns/*.txt（Wikisource，12 首；顯示頁面雜訊，寫書時手取詩節）
- [ ] 章檔 01–12、前置檔、模板、build、gen 腳本、評分

## 經文版本決定（已披露於版本說明）
- 底本 FHL unv；2:10「不給它的」→「不給他的」、7:26「她」→「他」（ai-eden 1919 讀法，同路得記 2:14 先例）。
- 7:1 ai-eden 自身有「美好的的膏油」重字，採 FHL。
- **7:27–28：FHL、ai-eden、cnbible 三源皆把兩節併在 7:27 下、7:28 為占位符；無來源可拆，書中標 ^27-28^，NASB 欄仍分 27／28。**

## 已實算的數字（count.py，Leningrad via Sefaria；請勿憑印象改）
| 項目 | 次數 | 備註 |
|---|---|---|
| הֶבֶל 虛空（所有詞形） | **38** | 1:2 有 5 次、12:8 有 3 次＝首尾框架 8 次，書體 30 次。（麥克阿瑟導論稱 37，計法不同，見附錄註明） |
| תַּחַת הַשָּׁמֶשׁ 日光之下 | **29** | 全落在 1:3–**10:5**；10:6–12:14 一次都沒有 |
| רְעוּת/רַעְיוֹן רוּחַ 捕風 | **9** | 1:14 1:17 2:11 2:17 2:26 4:4 4:6 4:16 6:9；第 6 章之後不再出現 |
| אֱלֹהִים | **40**（帶冠詞 32） | |
| יהוה | **0** | 約的名字全卷從未出現（需再以 `count.py 'יהו'` 確認後才可寫進書） |
| עָמָל 勞碌（含 עמל 的詞） | 35 | |
| יִתְרוֹן 益處 | 10 | 「有甚麼益處」1:3、3:9 |
| חֵלֶק 分 | 8 | |
| רָאִיתִי 我見 | 18 | |
| הַכֹּל הָבֶל 凡事都是虛空 | 6 | 1:2 1:14 2:11 2:17 3:19 12:8 |
| קֹהֶלֶת | 6 | 1:1 1:2 1:12 7:27 12:9 12:10 |
| שְׁאוֹל | 1 | 9:10 |
| עוֹלָם | 4 | 1:4 2:16 3:14 9:6（3:11 的「永生」原文 הָעֹלָם，帶冠詞，count 的前綴規則未計入——寫書前須另核） |

## 骨幹草案（待章檔逐節驗證；原則：發現而非強加）
人的軌跡：我試（1–2）→ 我見（3–6）→ 我查（7–10）→ 我歸（11–12）。
神的次序：神給（1:13、2:24-26）→ 神把永生放在人心（3:11）→ 神所作的人不能參透（3:11、8:17、11:5）→ 神使人敬畏（3:14）→ 神必審問（3:17、11:9、12:14）→ 一個牧者所賜（12:11）。
全經弧線：創 3 咒詛與勞苦 → 傳道書（咒詛底下誠實的人生）→ 羅 8:20-21（屈服在虛空之下，仍有指望）→ 啟 21–22（不再有日頭、不再有咒詛、「看哪，我將一切都更新了」對 傳 1:10「看哪，這是新的」）。
可驗證的連結：LXX 12:11 與約 10:16「一個牧人」；彌賽亞對「所羅門更大的」太 12:42；雅 4:14 氣息；提前 6:17 神厚賜百物給我們享受；約 4:13 對傳 1:8。
必須保持開放的張力：Qohelet 與 12:9-14 編者聲音的關係；3:21 vs 12:7；7:16-17；7:26-28；9:5,10；11:9 vs 民 15:39；b.Shabbat 30b 猶太傳統曾想藏起此書（須自 Sefaria 取原文再引）。

## 注疏來源（狀態待補）
- 摩根：*The Message of Ecclesiastes*，載 Living Messages of the Books of the Bible, OT（1912），OCR 已在 books/bible/nehemiah/sources/commentary/m-livingmessagesof0000unse.txt（約第 12128 行起，頁 57–）。
- 麥克阿瑟：無逐節系列（gty sitemap 4085 筆講道無傳道書系列）。可用：GTY 書卷導論 MSB21、blog B210118、講道 90-482、70-2、53-15、60-33、90-42（逐字核對前不得加引號）。
- 亨利：CCEL mhc3.Ec.*（可抓）。其餘公有領域（Bridges、Delitzsch、Ginsburg、Spurgeon、Gregory Thaumaturgus Metaphrase）待查可得性。
- 老弟兄：倉庫與 daily-notes 無傳道書第一手材料；**只用方法，不引語錄**（voice.md 白名單通則除外）。

## 聖詩（公有領域，Wikisource 取文；版權詩歌會觸發內容過濾器）
待選。

## 四卷（定）與「神的次序」步驟（每卷扉頁 add_volume 描述用）
- 卷一 · 試 (1–2)：第 1 步——神第一次出場是一份沉重的差事（1:13），第二次是一隻手（2:24）；人用智慧與享樂試遍日光之下，找不到益處。
- 卷二 · 時 (3–6)：第 2 步——神定了時候，又把永遠放在人心裏，卻不讓人看全（3:1, 3:11）；冤屈、孤單、敬拜、財富四章的見聞都在這條界線內。
- 卷三 · 問 (7–10)：第 3 步——神使這兩樣並列（7:14）：智慧到了極限，義人遭難、惡人享壽，人查不出（7:15; 8:14, 17）；然而 8:12 敬畏神的終久必得福樂。
- 卷四 · 歸 (11–12)：第 4 步——神必審問（11:9; 12:14），也賜下一個牧者（12:11）；人所當盡的本分是敬畏。
人的軌跡：我專心尋求（1:13）→ 我見（18 次，最後 10:7）→ 你當（11:1 起改命令句；12:1 當記念）。

## 章檔（H1 序號＝真實章號）
| 檔 | 標題 | 鑰詞 | 配詩 |
|---|---|---|---|
| 01-vanity-of-vanities | 虛空的虛空 | הֶבֶל 1:2 | 01 Abide with Me（Change and decay） |
| 02-the-kings-experiment | 王的試驗 | מִיַּד הָאֱלֹהִים 2:24 | 02 Jesus, Thou Joy of Loving Hearts |
| 03-a-time-for-everything | 凡事都有定期 | עֵת 3:1 / הָעֹלָם 3:11 | 03 O God, Our Help in Ages Past |
| 04-two-are-better-than-one | 兩個人總比一個人好 | אֵין מְנַחֵם 4:1 | 04 Blest Be the Tie |
| 05-guard-your-steps | 謹慎腳步 | 5:2 神在天上你在地下 | 05 Holy, Holy, Holy |
| 06-the-appetite-never-filled | 不知足的口 | 6:7 | 06 Jesus, Lover of My Soul |
| 07-the-house-of-mourning | 往遭喪的家去 | טוֹב 7:1-12 | 07 It Is Well（When Peace Like a River） |
| 08-who-knows-the-interpretation | 誰知道事情的解釋 | 8:12-13 / 8:17 | 08 God Moves in a Mysterious Way |
| 09-one-event-for-all | 臨到眾人的事都是一樣 | מִקְרֶה 9:2-3 | 09 Work, for the Night Is Coming |
| 10-dead-flies | 死蒼蠅 | 10:1 | 10 O God of Earth and Altar |
| 11-cast-your-bread | 將糧食撒在水面 | 11:5 / 11:9 | 11 Sowing in the Morning |
| 12-remember-your-creator | 當記念造你的主 | זְכֹר 12:1 / 12:11 | 12 Saviour, Like a Shepherd Lead Us |
前置：000-preface、00-overview、00a-ecclesiastes-position、00b-vanity-spine、00c-revelation-order、elder-wong-systematic-study；卷末：98-appendix-indices、99-appendix-references、99-remember-your-creator、999-afterword。

## 誠實記錄（寫進書的附錄）
- 麥克阿瑟導論稱 hebel 37 次，亨利稱「日光之下」28 次；本書以 Leningrad 逐字實算 38 與 29，計法差異須註明。
- 詮釋張力兩派並存不調和：Bridges / 亨利（悔改的所羅門，全書是神的話）vs 摩根 / 麥克阿瑟（1–11 章是沒有神的人生觀的「愚昧的啟示」，12 章才是智慧的陳述）。12:9-10 編者說這是「憑正直寫的誠實話」。
- 亨利主張「傳道者」陰性詞尾是所羅門自責其「柔弱」——這是亨利的推測；書中只陳述 7:27 動詞為陰性（待核 Hebrew）。


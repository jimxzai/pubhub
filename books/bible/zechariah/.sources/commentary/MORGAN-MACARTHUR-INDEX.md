# Morgan & MacArthur on Zechariah — 來源索引（單元 01–19）

產生日期：2026-10-31。所有引句皆由程式自來源檔逐字取出或逐字比對（見各節標註）。

## 來源與可查證性（必讀）

### Morgan（摩根）
| 檔案 | 出處 | 可否定位 | 備註 |
|---|---|---|---|
| `morgan-living-messages-zechariah-ocr1.txt` | G. Campbell Morgan, "The Message of Zechariah," *Living Messages of the Books of the Bible*, Old Testament (New York: Fleming H. Revell, 1912), pp. 317-331 | **有頁碼**（OCR 的頁首/頁尾保留 317-331）| archive.org `livingmessagesof0000gcam_p4q1` 第一掃描；OCR 有錯字（如 peculias, apocalvpse, Jehovab），以 ocr2 裁決。1912 年版權，美國公有領域。**這是摩根論本書最完整的一篇（約 21 KB，一整章）** |
| `morgan-living-messages-zechariah-ocr2.txt` | 同上第二掃描（`livingmessagesof0000unse`） | 有頁碼（部分頁碼 OCR 亦有誤，如 "32"、"=327"）| 用於裁決 OCR1 錯字；頁眉格式與 ocr1 不同 |
| `morgan-exposition-zechariah-1.txt` … `-14.txt` | G. Campbell Morgan, *An Exposition of the Whole Bible* (New York: Fleming H. Revell, 1959), Zechariah 1-14 | **無頁碼**（網頁轉錄，每章 1-6 小段，全書合計約 18,000 字元）| truthaccordingtoscripture.com；1959 合集版權狀態未查清（Jonah 書亦同，待確認）。第 1 章頁（"Verses 1-21"）實際概述前兩個異象，不是只談 1:1-21 |
**摩根沒有逐節講解**：Exposition 每章只有概述；Living Messages 是整卷總論。凡摩根引句，單元對應多半只能到「異象層級」。studylight 403，biblenotes.online 無 Zechariah 檔（404）。未找到可核對的摩根 Zechariah 講章單獨轉錄（SermonIndex/archive.org 未再搜）。

### MacArthur（麥克阿瑟）
gty.org 有**完整的 Zechariah 逐章系列**：series 6071「Zechariah, Vol. 01」(sermons 2153-2162, 10 篇) 與 series 6072「Zechariah, Vol. 02」(2163-2171, 9 篇)。共 19 篇，早年講道系列（2157 第 69 段提到 "America in 1977"，故約為 1977 年前後；gty.org 頁面未列日期與場合，書中只寫「早年晚間查經系列」），**編號是舊式 4 位數代碼，不是 NN-NNN**。
- 檔案：`gty-2153.txt` … `gty-2171.txt`（標頭 6 行：TITLE/CODE/URL/SOURCE/STRUCTURE/空行；之後**每段一行**；下表「段」＝標頭後第幾段，**檔案行號＝段號＋6**）。
- 取得方式：`curl -A '<瀏覽器UA>' https://www.gty.org/sermons/<CODE>`，取第一個 `div.expand--content` 內的 `<p>`（SSR，curl 直接可得，無需 DevTools）。
- **逐字稿 caveat**：gty.org 的轉錄稿保留口語、有轉錄錯字（如 "Conquerers"、"Megiddon"、"fee and toes"、"Moslems"），引用時須原樣逐字。講道多為**前千禧年、分別主義**立場（教會被提之後以色列得救），書中須註明這是講者的讀法。
- `scripts/verify-sermon-quotes.py` 的 `CODE_RE` 可接受 4 位數字碼（`sermon 2153`）；其 `fetch()` 走舊網址 `library/sermons-library/<code>/`，**未必可用**；以 `--cache books/bible/zechariah/.sources/commentary` 使用本目錄 `gty-<CODE>.txt`（檔名格式相符）即可直接比對本地檔，不必連網。引句出處行請寫成 `sermon 2153`（含「sermon」字樣）。
- 否定斷言：本系列**是**逐章系列，不存在「麥克阿瑟沒講過撒迦利亞」的問題。但：無單獨講 1:18-21 的完整一篇（2156 以但以理書與四國夢開場，1:18-21 約在 28-145 段，匠人僅 146 段一句）；無單獨講 7:1-14 的完整一篇（2162 先講路 18:9-14 法利賽人與稅吏，7 章在 14-59 段）；8:1-23 與 9:1-8 均有，但 2163 前 27 段是申命記談神愛以色列。

## 單元覆蓋總表

| 單元 | 經文 | Morgan Exp.（章/段）| Morgan LM（頁）| MacArthur 講道 | 段範圍 |
|---|---|---|---|---|---|
| 01 | 1:1-6 | Y ch1 (概述) | 317-321 | 2153 Prerequisite | 44-137 |
| 02 | 1:7-17 | Y ch1 | 318,327 | 2154 + 2155 | 2154:6-30；2155:38-92 |
| 03 | 1:18-21 | Y ch1（一段專談角與匠人） | 325,331 | 2156（1:18 在 28；匠人僅 146） | 2156:28-146；2157:46 回顧 |
| 04 | 2:1-13 | Y ch2 | 325 | 2157 Future Glory | 44-114 |
| 05 | 3:1-10 | Y ch3 | 326 | 2158 | 26-94 |
| 06 | 4:1-14 | Y ch4 | 326 | 2159 | 21-118 |
| 07 | 5:1-11 | Y ch5 | —（LM 僅列第六、七異象 p.326） | 2160 | 31-79 |
| 08 | 6:1-8 | Y ch6 前段 | 326-327 | 2161（symbols 36-3，4 靈 47-55） | 36-65 |
| 09 | 6:9-15 | Y ch6 後段 | 324 | 2161（Joshua crown 66-94） | 66-94 |
| 10 | 7:1-14 | Y ch7 | 329-330（abolish fasts） | 2162（路18 開場；Zech 7 在 14-59） | 14-59 |
| 11 | 8:1-23 | Y ch8 | 329-330 | 2163（8 章在 28-80；前 27 段講申 7 神愛以色列） | 28-80 |
| 12 | 9:1-8 | Y ch9 前段 | — | 2164 Saga 1 | 25-64 |
| 13 | 9:9-17 | Y ch9 後段 | 327,329 | 2165 Saga 2（9:9 在 23-31） | 17-70 |
| 14 | 10:1-12 | Y ch10（僅兩小段） | — | 2166 | 9-53 |
| 15 | 11:1-17 | Y ch11 | 329 | 2167（v1-14）＋2168（v4-14 回顧、v15-17） | 2167:16-58；2168:31-57 |
| 16 | 12:1-14 | Y ch12 | 327,329 | 2169 | 12-55 |
| 17 | 13:1-9 | Y ch13（僅一小段） | 329 | 2170 | 26-64 |
| 18 | 14:1-11 | Y ch14 前段 | 329 | 2171 | 16-55 |
| 19 | 14:12-21 | Y ch14 後段 | 330 | 2171 | 55-76 |

**無缺口單元**：19 個單元皆有麥克阿瑟與摩根可引。**較弱處**（引用時須誠實說明）：單元 03（匠人只有 2156 第 146 段一句）、07（LM 無第五異象專節；Exposition ch5 有）、10（講道先走路 18）、12/14/17（摩根 Exposition 僅 1-2 小段）。

## 單元 00 · 撒迦利亞書 全書 · 卷首／骨幹（Spine）

**摩根《Living Messages》（有頁碼，OCR1 行號為 `morgan-living-messages-zechariah-ocr1.txt` 檔案行）**

- (p.318; ocr1 L178; OCR1 有 OCR 錯字；OCR2 逐字相符；亦可用於單元 02、03、04、05、06、07、08) "The burden of Zechariah was that of the pervasive power and the persistent purpose of Jehovah. The book has been accurately described as the apocalypse of the Old Testament. An apocalypse is the removal of something that hides; an unveiling."
- (p.319; ocr1 L196; OCR1 有 OCR 錯字；OCR2 逐字相符；亦可用於單元 01、02、03) "Our observation is limited to the sight of the eyes and the hearing of the ears. The peculiar peril of the day of adversity is that therein men are in danger of seeing only the things that are near."
- (p.319; ocr1 L203; OCR1 逐字相符；亦可用於單元 03、04) "These men were looking at the near; Zechariah bade them look through to the things beyond. They were looking at the narrow circumstances; Zechariah called them to the wider circumstances of the Divine government and activity."

## 單元 01 · 撒迦利亞書 1:1-6 · 你們要轉向我

**摩根《Living Messages》（有頁碼，OCR1 行號為 `morgan-living-messages-zechariah-ocr1.txt` 檔案行）**

- (p.322; ocr1 L303; OCR1 逐字相符) "The threefold use of the title in the opening paragraph of Zechariah speaks of that fact of sovereignty to the conditions in the midst of which the people found themselves."
- (p.321; ocr1 L274; OCR1 逐字相符；亦可用於單元 11) "Zechariah used it more frequently than any other prophet. Fifty-three times at least does this majestic and wonderful title appear upon the pages of this brief prophecy of fourteen chapters."
- (p.324; ocr1 L394; OCR1 逐字相符；亦可用於單元 09) "Jehovah of hosts declares that if men will return to Him, He will return to them, and this He does by the coming of the Spirit."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2153 〈The Prerequisite for Blessing〉，段 53／檔案行 59) "It is God comforting His people through the prophet in a time of hardship while they were rebuilding their country and their temple."
- (sermon 2153 〈The Prerequisite for Blessing〉，段 86／檔案行 92) "God is not a sort of a senile Santa Claus figure; God is not some kind of passive grandfather character, who sits up there stroking His beard and just hoping everybody will be real nice, because He likes it if they have are."
- (sermon 2153 〈The Prerequisite for Blessing〉，段 87／檔案行 93) "Whether God is dealing with Israel, or God is dealing with society today or society in general, whether God is dealing with a believer in the Church – whoever and whenever God deals with sin, He is angry."
- (sermon 2153 〈The Prerequisite for Blessing〉，段 92／檔案行 98) "So, you see, Zechariah introduces the fact that even though this is God remembers and God blesses and God comforts, there’s always – there’s always a circle in which that happens, outside of which is wrath."
- (sermon 2153 〈The Prerequisite for Blessing〉，段 118／檔案行 124) "The graves of the world are filled with people who fall into this classification, who have walked out of the presence of God, who have not been willing to turn from their sin and have forfeited blessing for time and eternity."

## 單元 02 · 撒迦利亞書 1:7-17 · 香桃木中間的騎士

**摩根《Living Messages》（有頁碼，OCR1 行號為 `morgan-living-messages-zechariah-ocr1.txt` 檔案行）**

- (p.325; ocr1 L415; OCR1 逐字相符；亦可用於單元 03) "The people were conscious of the shady place; but they were not conscious of the Watcher. He was unveiled."

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 1, 段 3; 檔 morgan-exposition-zechariah-1.txt) "Under the figure of the myrtle trees Israel is described as "in the bottom," or, far better, as the margin reads, "in the shady place." It is the day of her overshadowing, but she is still watched."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2154 〈The Divine Plan for Jerusalem, Part 1〉，段 6／檔案行 12) "And so along comes Zechariah and he just again and again and again encourages the people that God is in their midst, that God is at work, that God has a plan, that wonderful things are going to happen no matter what it looks like."
- (sermon 2154 〈The Divine Plan for Jerusalem, Part 1〉，段 16／檔案行 22) "So when they were going into captivity, inevitable because of sin, but there is, and this is the beauty of it, there is a tolerance within God's judgment that turns to compassion, see."
- (sermon 2154 〈The Divine Plan for Jerusalem, Part 1〉，段 28／檔案行 34) "The Angel of the Lord, none other than Jesus Christ, none other than God himself the second person of the Trinity taking on an angelic form."
- (sermon 2155 〈The Divine Plan for Jerusalem, Part 2〉，段 51／檔案行 57) "And now, all of a sudden, the Angel of the Lord is back, and all the while of those 200 years, while Israel was in wretchedness, and Israel was in sinfulness, their protector and advocate and defender was not around."
- (sermon 2155 〈The Divine Plan for Jerusalem, Part 2〉，段 69／檔案行 75) "Here is Christ the Intercessor; here is Christ the Advocate, Christ the Defender, Christ the Protector, Christ taking up the cause of His people."

## 單元 03 · 撒迦利亞書 1:18-21 · 四角與四個匠人

**摩根《Living Messages》（有頁碼，OCR1 行號為 `morgan-living-messages-zechariah-ocr1.txt` 檔案行）**

- (p.331; ocr1 L623; OCR1 逐字相符；亦可用於單元 08) "See the shady place if you will, but see also the angel of Jehovah watching. See clearly the horns that are being prepared for the destruction of the purposes of God, but see also the smiths that will destroy the horns. See the unseen."

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 1, 段 5; 檔 morgan-exposition-zechariah-1.txt) "The horn is a symbol of power, and the four stand for the powers which have scattered the chosen people. The smiths are the symbol of that which destroys power, and stand for those who are to break the power of the horns."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2156 〈The Conquest of Israel's Enemy〉，段 42／檔案行 48) "Now, the horn can express the power of an individual or the power of a nation, as in the case of the horn of Moab, or the horn of Israel."
- (sermon 2156 〈The Conquest of Israel's Enemy〉，段 52／檔案行 58) "And there is a second view, and that is that the four horns which scatter have scattered, are scattering, and will scatter, using the fullness of that possible Hebrew tense are the four great world empires that make up the times of the Gentiles."
- (sermon 2156 〈The Conquest of Israel's Enemy〉，段 146／檔案行 152) "Verse 20, “And then the Lord showed me four” – and you’ve got an interesting word in the Hebrew, four artisans, four workmen, four – some people say carpenters – four smiths."
- (sermon 2156 〈The Conquest of Israel's Enemy〉，段 67／檔案行 73) "And God gave him an amazing dream of a picture of the whole thing, the way it would be all the way to the end when Christ would come."
- (sermon 2157 〈The Future Glory of Jerusalem〉，段 46／檔案行 52) "The second vision presented, of the horns and the smiths, presented the fact that the nations who had triumphed over Israel would be crushed."

## 單元 04 · 撒迦利亞書 2:1-13 · 手拿準繩的人

**摩根《Living Messages》（有頁碼，OCR1 行號為 `morgan-living-messages-zechariah-ocr1.txt` 檔案行）**

- (p.326; ocr1 L428; OCR1 有 OCR 錯字；OCR2 逐字相符) "The third vision is that of a city, and a young man so interested therein that he desired to measure it; and also of the fact that the new city had no walls, for two reasons; first, because it is too great to be included by walls, and secondly, because it does not need the defense of walls by reason of the defense of Jehovah."

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 2, 段 2; 檔 morgan-exposition-zechariah-2.txt) "The nature of that prosperity is indicated in the statement that Jehovah's presence will make walls unnecessary, and its extent be so vast as to make walls impossible."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2157 〈The Future Glory of Jerusalem〉，段 60／檔案行 66) "But if you were to visit Jerusalem, you would realize that from one wall of Jerusalem to the other wall is about a ten-minute walk right across the middle."
- (sermon 2157 〈The Future Glory of Jerusalem〉，段 65／檔案行 71) "And the millennial Jerusalem, the Jerusalem of the King, the Jerusalem yet, when Jesus returns, will be so big and so populated with people and animals that it will go way past its walls."
- (sermon 2157 〈The Future Glory of Jerusalem〉，段 82／檔案行 88) "During the day the cloud appeared, and the glory of God dwelt and came down and entered the Holy of the Holies in the tabernacle and dwelt in the midst of the land of Israel."
- (sermon 2157 〈The Future Glory of Jerusalem〉，段 89／檔案行 95) "And as the shepherd in the field would light a fire to keep the marauding wolf from coming to get his sheep, so the Lord will be the fire to protect His nation Israel."
- (sermon 2157 〈The Future Glory of Jerusalem〉，段 113／檔案行 119) "And finally, finally, finally Israel will be the channel of salvation to the world that God chose them to be in the first place."

## 單元 05 · 撒迦利亞書 3:1-10 · 約書亞與骯髒的衣服

**摩根《Living Messages》（有頁碼，OCR1 行號為 `morgan-living-messages-zechariah-ocr1.txt` 檔案行）**

- (p.326; ocr1 L445; OCR1 逐字相符) "The fourth vision is that of the adversary, and also of the Advocate. The people were conscious of the adversary; but they were not conscious of the Advocate. He was unveiled."

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 3, 段 3; 檔 morgan-exposition-zechariah-3.txt) "it preeminently set forth that the nation which had failed through sin would be restored by moral cleansing to the priestly position and function of access to God and mediation."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2158 〈The Cleansing of the Nation of Israel〉，段 36／檔案行 42) "Satan, the once great archangel of God, who fell through pride, amazingly still permitted to enter God’s presence and make his accusation."
- (sermon 2158 〈The Cleansing of the Nation of Israel〉，段 37／檔案行 43) "Here is Joshua, and he’s ministering to the Lord, and he represents his people, and his people are bowing even though they’re sinful."
- (sermon 2158 〈The Cleansing of the Nation of Israel〉，段 52／檔案行 58) "And so, as Joshua was brought back, when neither his father or grandfather was so fortunate, so he represents the nation brought back, a small remnant indicating that God is not finished with Israel, that there is yet a plan, an ultimate purpose."
- (sermon 2158 〈The Cleansing of the Nation of Israel〉，段 83／檔案行 89) "God will keep His promise Israel will be fully reinstated as His priestly nation to serve His house and keep His courts and have free access to His presence like the angels do forever."
- (sermon 2158 〈The Cleansing of the Nation of Israel〉，段 85／檔案行 91) "So, the divine choice, the divine condemnation, the divine cleansing, the divine covenant – and listen, the one who makes it all possible – the divine Christ."

## 單元 06 · 撒迦利亞書 4:1-14 · 不是倚靠勢力

**摩根《Living Messages》（有頁碼，OCR1 行號為 `morgan-living-messages-zechariah-ocr1.txt` 檔案行）**

- (p.326; ocr1 L451; OCR1 逐字相符) "The fifth vision is that of responsibility, the candlestick and the light shining in the dark places; and also a vision of resource, the oil and the perpetual supply. The people were conscious of the responsibility, but not of the resource."
- (p.330; ocr1 L609; OCR1 逐字相符；亦可用於單元 19) "Zechariah said, You will only be strong as you see the things that are not seen, the heavenly visions, and hear the things that are never heard, the heavenly voices."

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 4, 段 2; 檔 morgan-exposition-zechariah-4.txt) "The two olive trees, as Zechariah described them, referred immediately and locally to Zerubbabel and Joshua, the governor and the priest under whom the Temple had been rebuilt and its worship restored, but ultimately to the offices of king and priest as they would be realized and fulfilled in the person of the Messiah."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2159 〈Israel: The Light of the World〉，段 63／檔案行 69) "Human strength, human power of every description – physical, mental, moral, whatever – combined or individual will never bring about the salvation of the nation Israel."
- (sermon 2159 〈Israel: The Light of the World〉，段 82／檔案行 88) "What this is is a defiant challenge against all opposition that tries to stop God from accomplishing His work in the power of His Spirit."
- (sermon 2159 〈Israel: The Light of the World〉，段 74／檔案行 80) "So, the oil, then, is the picture of the Spirit, and it’s the flow of the Spirit in profuse quantity that’s going to make that kingdom such a fantastic time."
- (sermon 2159 〈Israel: The Light of the World〉，段 50／檔案行 56) "The Church is gone; he has no witness in the world, and Israel will be reborn and regenerated and redeemed and placed in the position of being the light that God intended them to be all along."

## 單元 07 · 撒迦利亞書 5:1-11 · 飛行的書卷與量器

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 5, 段 2; 檔 morgan-exposition-zechariah-5.txt) "The ephah is the symbol of commerce, and, according to the distinct prophecy, the woman sitting in the midst of the ephah is the personification of wickedness."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2160 〈The End of Sinners and Sin〉，段 39／檔案行 45) "This is a symbol of the Word of God, and it is the Word of God that is alive and powerful and sharper than any two-edged sword, that pierces and divides asunder."
- (sermon 2160 〈The End of Sinners and Sin〉，段 41／檔案行 47) "God will judge you not on the basis of works, not on the basis of your good deeds, but on the basis of truth."
- (sermon 2160 〈The End of Sinners and Sin〉，段 46／檔案行 52) "There will no long – longer be God’s silence, there will be no longer be God’s long suffering, there will no longer be this period of patience, there will be instantaneous judgment."
- (sermon 2160 〈The End of Sinners and Sin〉，段 49／檔案行 55) "The criterion is the word of God, the completeness means everyone who sins will be totally wiped out of any possible blessing."
- (sermon 2160 〈The End of Sinners and Sin〉，段 54／檔案行 60) "The spirit of self-centered materialism that had been so foreign to Israel when they were shepherd people, had overtaken them since the spell of Babylon had been cast on them."

## 單元 08 · 撒迦利亞書 6:1-8 · 四輛戰車

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 6, 段 2; 檔 morgan-exposition-zechariah-6.txt) "the prophet was instructed that the chariots symbolized the four spirits of heaven going forth from the presence of the Lord to walk to and fro in the earth."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2161 〈Establishing God's Kingdom on Earth〉，段 54／檔案行 60) "And it was four of those angels that were dispatched by God to this vision to show Zechariah the final picture of judgment."
- (sermon 2161 〈Establishing God's Kingdom on Earth〉，段 55／檔案行 61) "Now, that phrase at the end of verse 5, as a footnote, is a millennial title for the Lord, the Lord of the whole earth."
- (sermon 2161 〈Establishing God's Kingdom on Earth〉，段 57／檔案行 63) "Angelic judgment agents, just like you have in Revelation, where you have seven angels blowing seven trumpets, seven angels pouring out seven bowls of judgment."
- (sermon 2161 〈Establishing God's Kingdom on Earth〉，段 59／檔案行 65) "And so, you find here that God is then bringing about a final judgment of vengeance, particularly upon the nations that have mistreated Israel."
- (sermon 2161 〈Establishing God's Kingdom on Earth〉，段 65／檔案行 71) "And so, when God at the end comes and goes with His host against Babylon, the final system, and wipes it out, then God’s spirit is at rest."

## 單元 09 · 撒迦利亞書 6:9-15 · 冠冕與「苗」

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 6, 段 3; 檔 morgan-exposition-zechariah-6.txt) "His office would be dual: He would be both Priest and King; and it was promised that the "counsel of peace shall be between them both," that is to say, the resulting peace would accrue from the union of the kingly and priestly functions in the one Person."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2161 〈Establishing God's Kingdom on Earth〉，段 66／檔案行 72) "And there is a beautiful act that takes place on that next day that actually did happen historically, no doubt, to symbolize the coronation of the Lord Jesus Christ."
- (sermon 2161 〈Establishing God's Kingdom on Earth〉，段 78／檔案行 84) "But there’s coming a day, beloved, in the future when God is going to send the Messiah back to rebuild the temple."
- (sermon 2161 〈Establishing God's Kingdom on Earth〉，段 85／檔案行 91) "Not in the kingdom because the same One who rules with the role of King is the same One who intercedes and makes the worship of the true God the measure of every man, the Lord Jesus Christ."
- (sermon 2161 〈Establishing God's Kingdom on Earth〉，段 89／檔案行 95) "When Jesus comes to set up His kingdom, there isn’t going to be any question about the fact that this is an absolutely accurate fulfillment of God’s prophecy."
- (sermon 2161 〈Establishing God's Kingdom on Earth〉，段 92／檔案行 98) "What He’s saying here is, this is going to come to pass for you if you will diligently obey the voice of the Lord your God."

## 單元 10 · 撒迦利亞書 7:1-14 · 禁食的問題

**摩根《Living Messages》（有頁碼，OCR1 行號為 `morgan-living-messages-zechariah-ocr1.txt` 檔案行）**

- (pp.329-330; ocr1 L570; OCR1 逐字相符；亦可用於單元 11) "the prophet to the men of his own age was that they were to build the house of God even though it was a day of darkness and disappointment; that they were to abolish their fasts by removing the cause for them, to have done with them by getting rid of the sin which occasioned them"

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 7, 段 4; 檔 morgan-exposition-zechariah-7.txt) "The second answer reminded them that God sought justice and mercy rather than the observance of self-appointed fasts."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2162 〈Ritual vs. Reality〉，段 16／檔案行 22) "And so now, two years later, while Israel is greatly comforted in what has happened in the meantime, God comes back to them with a tremendous message of warning."
- (sermon 2162 〈Ritual vs. Reality〉，段 25／檔案行 31) "When the Babylonians had come in and wiped out Jerusalem and the temple, that was a devastating thing in the history of Israel."
- (sermon 2162 〈Ritual vs. Reality〉，段 32／檔案行 38) "The point is, you can worship and you can celebrate with a fast or you can celebrate with a feast any time you want, if it’s truly done to the honor and glory of the Lord, you see?"
- (sermon 2162 〈Ritual vs. Reality〉，段 17／檔案行 23) "And then, God moved in and comforted their hearts by giving them these visions through Zechariah to tell them that God would rebuild their city and God would rebuild their temple."

## 單元 11 · 撒迦利亞書 8:1-23 · 我要住在耶路撒冷當中

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 8, 段 1; 檔 morgan-exposition-zechariah-8.txt) "The third answer was full of grace. It declared that God was jealous for Zion, that He had returned to it, and that therefore its prosperity was assured, notwithstanding that these people saw only the devastation which caused their lamentation."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2163 〈Turning the Fast into a Feast〉，段 34／檔案行 40) "Now, when the Bible speaks of the jealousy of God, it doesn’t mean envy, but it is the boundless zeal that comes from a God who loves holiness and hates sin, who loves His own people who are godly and hates the ungodly."
- (sermon 2163 〈Turning the Fast into a Feast〉，段 35／檔案行 41) "There was a sense in which this was a great message for Israel, not that they were desirous that people be punished, but they were desirous that God be justified."
- (sermon 2163 〈Turning the Fast into a Feast〉，段 42／檔案行 48) "And in Zechariah’s time, the presence of God was nothing more than a memory, because Israel had long ago forfeited the presence of God."
- (sermon 2163 〈Turning the Fast into a Feast〉，段 44／檔案行 50) "And Ezekiel saw it leave in his vision and later, he saw it coming back, and this was a great, great hope for Israel that the Shekinah of God would come back to His temple."

## 單元 12 · 撒迦利亞書 9:1-8 · 主要奪取

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 9, 段 2; 檔 morgan-exposition-zechariah-9.txt) "In the course of this campaign he passed Jerusalem more than once, but never attacked it, Thus, according to the prophecy of Zechariah, the city was preserved for the coming of the true King."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2164 〈The Saga of Two Conquerers, Part 1〉，段 35／檔案行 41) "And you remember how Cyrus, Cyrus who was an ungodly pagan, was used by God to open the door to lead Israel back to its land."
- (sermon 2164 〈The Saga of Two Conquerers, Part 1〉，段 36／檔案行 42) "Alexander the Great, before you want to give him all the credit, was a tool of God to accomplish God’s judgment against pagan nations."
- (sermon 2164 〈The Saga of Two Conquerers, Part 1〉，段 42／檔案行 48) "All of a sudden there’s a dramatic change and the Spirit of God goes behind the human prince to the real power."
- (sermon 2164 〈The Saga of Two Conquerers, Part 1〉，段 55／檔案行 61) "These Philistines, as pagan as they were, once they spit out their idols and come to God, they will be in Israel like a ruler, see."
- (sermon 2164 〈The Saga of Two Conquerers, Part 1〉，段 56／檔案行 62) "So, literally, there would be a revival there and there would be those who would be a part of Israel’s life because they worshiped Israel’s God."

## 單元 13 · 撒迦利亞書 9:9-17 · 你的王來到你這裏

**摩根《Living Messages》（有頁碼，OCR1 行號為 `morgan-living-messages-zechariah-ocr1.txt` 檔案行）**

- (p.329; ocr1 L549; OCR1 逐字相符；亦可用於單元 16、17、18) "The Advent of rejection prepares for the Advent of coronation. The Advent of coronation perfects the Advent of rejection."

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 9, 段 2; 檔 morgan-exposition-zechariah-9.txt) "That coming he then foretold, calling on Zion and Jerusalem to rejoice, declaring the character of the King, and announcing His complete victory."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2165 〈The Saga of Two Conquerers, Part 2〉，段 26／檔案行 32) "You know, it’s amazing as you look at the text because against the background of the invincible marching army of Alexander comes one who doesn’t inspire fear and He doesn’t inspire dread and nobody’s shaking and nobody’s quaking."
- (sermon 2165 〈The Saga of Two Conquerers, Part 2〉，段 27／檔案行 33) "“Thy King.” Israel’s King, Israel’s redeemer, the promised seed of David, the Messiah, the One who is to reign, the One of whom Isaiah said, “Unto us a child is born and the government shall be upon His shoulders.” He’s the King.”"
- (sermon 2165 〈The Saga of Two Conquerers, Part 2〉，段 23／檔案行 29) "So He jumps into the future and He says there’s coming a time when the other conqueror, the divine conqueror not the human one, comes."
- (sermon 2165 〈The Saga of Two Conquerers, Part 2〉，段 49／檔案行 55) "When the King comes, Israel will be freed from the pit of trouble, the pit of war, the pit of suffering to know the liberty of the Kingdom of peace and the reign of the Prince of Peace Himself."
- (sermon 2165 〈The Saga of Two Conquerers, Part 2〉，段 66／檔案行 72) "So you have the salvation on the one hand, and the peace and the Kingdom and this terrible judgment of the godless on the other hand."

## 單元 14 · 撒迦利亞書 10:1-12 · 耶和華眷顧羣羊

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 10, 段 2; 檔 morgan-exposition-zechariah-10.txt) "Finally, speaking in the name of Jehovah, the prophet described Jehovah's regathering of the people."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2166 〈The Redemption of Israel〉，段 9／檔案行 15) "And the Spirit, as always, poured out will do initially the work of conviction, and they’ll look on Christ and they’ll mourn for what they did to Him."
- (sermon 2166 〈The Redemption of Israel〉，段 31／檔案行 37) "Because while the Bible always promises a literal kingdom with literal rain and literal water and literal fields growing with literal crops, it also speaks of spiritual blessing outpoured on the people of God."
- (sermon 2166 〈The Redemption of Israel〉，段 43／檔案行 49) "You know, if you study Israel’s history, the only time they ever won a battle was when the Lord was in it."
- (sermon 2166 〈The Redemption of Israel〉，段 43／檔案行 49) "The world is going to go into a state of shock in the day when the King of Kings comes with His mighty people from Israel to win the great and final battle before the kingdom."
- (sermon 2166 〈The Redemption of Israel〉，段 16／檔案行 22) "In fact, Daniel calls Him a stone cut out without hands, and He is the crushing stone that comes in judgment to destroy the Gentile world powers."

## 單元 15 · 撒迦利亞書 11:1-17 · 兩根杖與三十塊錢

**摩根《Living Messages》（有頁碼，OCR1 行號為 `morgan-living-messages-zechariah-ocr1.txt` 檔案行）**

- (p.327; ocr1 L502; OCR1 逐字相符；亦可用於單元 13、16) "The oracles teach the same lesson. The anointed King is rejected, but the book does not end with that story. The rejected King is enthroned by the pervasive power of Jehovah."

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 11, 段 3; 檔 morgan-exposition-zechariah-11.txt) "This King is portrayed as having two staves, one called Beauty, which signified grace, and the other, Bands, which signified union. This true Shepherd rejected the false, and then was Himself rejected of the people."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2167 〈The Rejection of the True Shepherd〉，段 55／檔案行 61) "That was worse than no price at all because thirty pieces of silver was compensation paid for a slave that had been gored by an ox, Exodus 21:32."
- (sermon 2167 〈The Rejection of the True Shepherd〉，段 55／檔案行 61) "And they didn’t want to just ignore Him and give Him no price, so they said You’re worth thirty pieces of silver."
- (sermon 2167 〈The Rejection of the True Shepherd〉，段 41／檔案行 47) "And the very thing they feared and killed their Messiah to avoid was the sentence of God that took place on their nation."
- (sermon 2167 〈The Rejection of the True Shepherd〉，段 34／檔案行 40) "God may have designed Israel for judgment, but that doesn’t mean when the nations superseded reasonable judgment and acted cruelly that they are without guilt."
- (sermon 2168 〈The False Shepherd〉，段 31／檔案行 37) "Somehow he played the part of the coming shepherd and dramatized for the people what they were going to do to the Christ."

## 單元 16 · 撒迦利亞書 12:1-14 · 他們必仰望我

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 12, 段 4; 檔 morgan-exposition-zechariah-12.txt) "This victory over the nations will issue in the restoration of the spiritual Israel to supremacy under the government of One whom they had pierced."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2169 〈Israel's Final Deliverance〉，段 14／檔案行 20) "And before there can ever be conversion in Israel and before there can ever be repentance in Israel and before there will ever be salvation in Israel and before God will ever set up His kingdom, there’s going to be grief – there’s grief."
- (sermon 2169 〈Israel's Final Deliverance〉，段 51／檔案行 57) "Because they recognize that the very one who came back as their deliverer was the same one they killed and they pierced when He came the first time."
- (sermon 2169 〈Israel's Final Deliverance〉，段 52／檔案行 58) "Anybody to be saved must turn from the ultimate sin which is the sin of rejecting Jesus Christ, not believing in Him."
- (sermon 2169 〈Israel's Final Deliverance〉，段 44／檔案行 50) "God wants no human glory, no human magnification, and so just to make sure it won’t happen He starts by giving the victory first to the little folks in the countryside."
- (sermon 2169 〈Israel's Final Deliverance〉，段 54／檔案行 60) "Sure they will, because they’ll know that it was in their very line that the Messiah came and was rejected."

## 單元 17 · 撒迦利亞書 13:1-9 · 擊打牧人

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 13, 段 1; 檔 morgan-exposition-zechariah-13.txt) "In that day, by way of a fountain opened to them, they will be cleansed from all the things which have defiled and degraded them."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2170 〈The Cleansing of Israel〉，段 27／檔案行 33) "And so the point is this, Israel will be cleansed of its own moral defilement and of its tendency to behave and go in the wrong direction."
- (sermon 2170 〈The Cleansing of Israel〉，段 62／檔案行 68) "Christ returns, the one third or however many it is, those remaining, that remnant remaining are going to see Christ; they’re going to repent; they’re going to mourn; they’re going to weep; they’re going to look on Him who was pierced; they’re going to be saved."
- (sermon 2170 〈The Cleansing of Israel〉，段 60／檔案行 66) "And so we see that they’ll be cleansed from the defilement, from the deception, from the dispersion all through the death of the Savior."
- (sermon 2170 〈The Cleansing of Israel〉，段 63／檔案行 69) "And so they’re going to be smelted, as it were, and refined and purified, leaving only the precious silver, only the precious gold, all the other rebels purged out."
- (sermon 2170 〈The Cleansing of Israel〉，段 26／檔案行 32) "And when they come in repentance and that fountain opens on a national basis to them, notice the end of verse 1, it will be for sin and uncleanness."

## 單元 18 · 撒迦利亞書 14:1-11 · 腳站在橄欖山上

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 14, 段 1; 檔 morgan-exposition-zechariah-14.txt) "The prophet finally described the ultimate victories of the King, commencing with a description of the smiting of the Shepherd and the scattering of the sheep."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2171 〈The Day of the Lord〉，段 21／檔案行 27) "And so God has gathered these nations with a Jewish purpose in mind and that is to act in judgment against unbelieving persons in Israel."
- (sermon 2171 〈The Day of the Lord〉，段 40／檔案行 46) "So in order to facilitate a hasty exit for the depressed people who are undergoing the siege, the Lord Jesus hits the mountain, splits the thing wide open, creates a valley and God’s people Israel can flee right through that open pass."
- (sermon 2171 〈The Day of the Lord〉，段 49／檔案行 55) "And it is precisely at this moment that the events of chapter 12 take place, when they look on Him whom they’ve pierced, when a fountain of blessing is opened, when they repent."
- (sermon 2171 〈The Day of the Lord〉，段 51／檔案行 57) "And at that moment Israel is going to turn and look and they’re going to believe and they’re going to turn to their Messiah and they’re going to be wonderfully saved and spared judgment and gathered into the kingdom."
- (sermon 2171 〈The Day of the Lord〉，段 17／檔案行 23) "In other words, man’s day is ended and the Lord begins to take back His earth – the day of the Lord."

## 單元 19 · 撒迦利亞書 14:12-21 · 歸耶和華為聖

**摩根《Exposition of the Whole Bible》（無頁碼，章/段號）**

- (Zech 14, 段 2; 檔 morgan-exposition-zechariah-14.txt) "This advent would initiate the new processes of the settlement of the land, and the cleansing of Jerusalem by judgment, to be followed by the establishment of the Kingdom, in which all nations would gather to Jerusalem as a center of worship, those refusing being punished, while all life would be consecrated."

**麥克阿瑟（gty.org，出處行寫 `sermon CODE`）**

- (sermon 2171 〈The Day of the Lord〉，段 59／檔案行 65) "Not only is the Lord crowned, but the city is crowned, and it becomes the jewel of the earth, and Christ is crowned King and sits on the throne in that city."
- (sermon 2171 〈The Day of the Lord〉，段 64／檔案行 70) "Beloved, ultimately all the wealth of the world will come to the hands of the Lord and His people in His kingdom."
- (sermon 2171 〈The Day of the Lord〉，段 67／檔案行 73) "But these people from the nations will go up from year to year to worship the King, the Lord of host, and keep the Feast of Tabernacles."
- (sermon 2171 〈The Day of the Lord〉，段 70／檔案行 76) "But he says in that day every single thing that exists is going to be just as holy as the high priest."

## 引用格式與使用規則（給寫作者）

- **摩根 Living Messages**：`G. Campbell Morgan, "The Message of Zechariah," *Living Messages of the Books of the Bible*, Old Testament (New York: Fleming H. Revell, 1912), p. 321.` 頁碼已由 OCR 頁眉/頁尾核對（317-331）。標「OCR1 有 OCR 錯字；OCR2 逐字相符」者，引句在 ocr2 逐字成立；兩掃描皆讀成錯字的句子（"Jehovab"、"writter"、"necd"、"heisthe"）已全部避開。`verify-citations.py --source` 請傳 `cat ocr1 ocr2 > /tmp/morgan.txt`；OCR 跨行斷詞（"pro-/phetic"）可能讓工具報 DRIFT，須人工對 ocr2 對應行，必要時加 `.citation-accept`。
- **摩根 Exposition**：`G. Campbell Morgan, *An Exposition of the Whole Bible* (New York: Fleming H. Revell, 1959), on Zechariah N`（網頁轉錄，無頁碼）。檔內段落號是本檔案的段序，不是書頁。
- **麥克阿瑟**：出處行寫 `> — John MacArthur, "<Title>," sermon 2157, Grace to You (gty.org).`（務必含 `sermon CODE` 字樣）；驗證：`python3 scripts/verify-sermon-quotes.py books/bible/zechariah --heading 麥克阿瑟 --cache books/bible/zechariah/.sources/commentary`。
- **分別主義前千禧年讀法**：本系列把 9-14 章讀為以色列民族的末世得救（Armageddon、教會被提、千禧年國度），並把 1:18 四角讀為但以理書四國。這是講者立場，書中須寫成「麥克阿瑟的讀法」，不可寫成經文本身所說。摩根在 LM p.328 也自認「touch upon controversial ground」，視香桃木異象為現在、其餘未應驗；同樣須標為摩根的讀法。
- **摩根的數字**：LM p.321 說 "Fifty-three times at least"（萬軍之耶和華）——這是摩根的計數，書中若當事實引須以 WLC 自行重數。
- **全書去重**：每一句只出現一次；「亦可用於單元」只是備選。單元 00 為卷首／骨幹章用。
- **逐字稿特性**：MacArthur 逐字稿含口語與轉錄錯字（例如 2153 第 86 段 "if they have are"）。引用須原樣逐字，不得「修好」；嫌雜就改選別句。

# 耶利米書研讀 — 建卷計劃（2026-10-26）

slug `jeremiah`；目錄 `books/bible/jeremeiah/`（目錄拼字沿用使用者所建，build script 的 INPUT_DIR 指向它）；
build `scripts/build-jeremiah-consolidated.sh`；模板 `templates/pdf/jeremiah.latex`（由 nehemiah.latex 改色派生）。
體例＝約翰福音 11 節章節模板（`.claude/skills/eat-bible/references/chapter-template.md`），卷首/卷末骨架照約翰卷
（00-overview、000-preface、00a/00b/00c、領受總綱、四至六卷、99-to-revelation、98/99 附錄、999-afterword）。
H1 序號＝本書章序 1–27（unnumbered 卷首／卷末），**真實章節範圍只寫在參照行與座標行**，不併入 H1。

## 已核事實（皆機器數過，來源 sources/scripture/aieden-N.json，1364 節全齊）

- 「耶和華的話臨到」(CUV) 31 節（1:2, 1:4, 2:1, 7:1, 11:1, 13:8, 18:1, 21:1, 24:4, 25:3 …）；「耶和華如此說」87 節；「萬軍之耶和華」76 節。
- 六個動詞「拔出、拆毀、毀壞、傾覆、建立、栽植」(1:10)；其後 12:14-17、18:7-9、24:6、31:28、42:10、45:4 重提（待逐處核）。
- 「新約」一詞全書僅 31:31 一節；「七十年」僅 25:11-12、29:10。
- 「背道」12 節（2:19; 3:6, 8, 11, 12, 14, 22; 5:6; 8:5; 14:7; 31:22; 49:4）。
- 「我要作他們的神」24:7、31:33、32:38 三處。
- 待查：שׁוב 全書次數（Sefaria 逐字）；היה דבר־יהוה 次數；「不聽」43 節。
- 禁止代求：7:16、11:14、14:11（15:1 摩西撒母耳也不能）。

## 骨幹（啟示的次序）——初稿，待總綱章再核

核心觀察：耶利米書是一本**神先開口、先哀哭、先留後路**的書；審判有宣告、有控訴、有呼籲，在毀滅的同時，新約的應許種在圍城裏。

五步（神的次序）：
1. **話先於人**（1）——「我未將你造在腹中，我已曉得你」(1:5)；話臨到、手按口 (1:9)，先知是話的口，不是話的作者。
2. **先控訴、後審判；先呼喚、後定罪**（2–6）——「背道的以色列啊，回來」(3:12,22)；一再給回頭的門，直到 6:30「被棄的銀渣」。
3. **代求被關上，眼淚卻沒有關**（7–20）——「不要為這百姓祈求」(7:16)，而先知仍哀哭 (9:1)、仍控告 (20:7-18)：神禁止代求的時候，自己先流淚。
4. **審判藉巴比倫、盼望種在審判裏**（21–29, 30–33）——「我僕人尼布甲尼撒」(25:9)；七十年 (29:10)；圍城中買田 (32)；新約 (31:31-34)。
5. **話語勝過刀與火**（34–45）→**審判者亦受審**（46–51）→**燈未熄滅**（52）——書卷被小刀割、被火燒，神使它再寫、再添 (36:32)；巴比倫的書卷被扔進幼發拉底 (51:63-64)；全書以約雅斤在巴比倫王席上得飯食收束 (52:31-34)。

人的軌跡：1:6「我不知怎樣說」→ 15:16「你的言語是我心中的歡喜」→ 20:9「我心裏覺得似乎有燒著的火」→ 20:14「願我生的那日受咒詛」→ 38:6 淤泥坑 → 43:6 被帶往埃及。

跨約連結（只用有經文的線，不硬說預表）：太16:14（人說耶穌是耶利米）、太2:17-18（拉結哭）、太21:13（賊窩，引耶7:11）、
太26:28／路22:20／林前11:25（新約）、林後3:6、來8:8-12、來10:16-17（引耶31）、羅11:27、啟18:21（巴比倫如磨石沉沒，回扣耶51:63）。
**禁止**：「耶利米是基督的預表」之類無經文依據的斷語。

## 六卷 27 章

卷一 呼召與控訴 (1–6)
1 `01-before-i-formed-you` — 耶1　　2 `02-broken-cisterns` — 耶2:1-3:5
3 `03-return-faithless-israel` — 耶3:6-4:4　　4 `04-peace-peace` — 耶4:5-6:30

卷二 殿與不聽 (7–20)
5 `05-den-of-robbers` — 耶7-8　　6 `06-weeping-prophet-living-god` — 耶9-10
7 `07-covenant-belt-jar` — 耶11-13　　8 `08-drought-and-closed-intercession` — 耶14-15
9 `09-deceitful-heart` — 耶16-17　　10 `10-potter-and-flask` — 耶18-19
11 `11-fire-in-my-bones` — 耶20

卷三 君王與假先知 (21–29)
12 `12-kings-before-the-fall` — 耶21-22　　13 `13-righteous-branch` — 耶23
14 `14-two-baskets-seventy-years` — 耶24-25　　15 `15-trial-and-yoke` — 耶26-27
16 `16-hananiah-and-the-letter` — 耶28-29

卷四 安慰之書 (30–33)
17 `17-book-of-consolation` — 耶30-31:30　　18 `18-new-covenant` — 耶31:31-40
19 `19-field-at-anathoth` — 耶32-33

卷五 話語與焚燒 (34–45)
20 `20-broken-covenant-rechabites` — 耶34-35　　21 `21-scroll-and-penknife` — 耶36
22 `22-cistern-and-courtyard` — 耶37-38　　23 `23-fall-of-the-city` — 耶39-41
24 `24-egypt-and-baruch` — 耶42-45

卷六 列國與終局 (46–52)
25 `25-oracles-against-nations` — 耶46-49　　26 `26-fall-of-babylon` — 耶50-51
27 `27-jehoiachins-table` — 耶52

## 注疏來源（sources/commentary/，待下載；不可編造）
- 亨利 CCEL `mhc4.Jer`（HTTP 200 已確認）
- 加爾文《耶利米書注釋》CCEL calcom19/20（HTTP 200 已確認；改革宗）
- Keil & Delitzsch《耶利米書》（CCEL URL 302，另尋來源）
- 摩根《The Message of Jeremiah》——已在 `nehemiah/sources/commentary/m-livingmessagesof01morgiala.txt`（Living Messages OT, 1912, 約 pp.109-117）。Studies in the Prophecy of Jeremiah (1931) 美國尚未入公有領域，不用。
- 麥克阿瑟 gty.org：先用 sitemap 找耶利米講章，**找不到的章不立該節**，不補位。
- 教父：奧古斯丁《上帝之城》引耶31、愛任紐、耶柔米；僅用可在 NPNF 查到者。
- Sefaria 希伯來文：`/api/texts/Jeremiah.N?context=0&lang=he` 已確認可用。
- 老弟兄：倉庫無耶利米書第一手材料（待 grep 確認）；只用方法，不引語錄。

## 驗證路線
check-book-spine → lint-templates → lint-chapter-markup → lint-scripture-text → verify-citations/verify-sermon-quotes →
check-citation-ledger → driver.sh jeremiah → 看 PDF 頁面 → 評分表 docs/scores/jeremiah-2026-10-26.md

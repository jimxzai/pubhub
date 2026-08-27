# 馬可福音深度修訂規格 (REVISION SPEC) — 2026-08

目標：把 `books/bible/gospel-of-mark/` 各章書稿修訂到與《約翰福音研讀》整編版（2026-08 定稿）**完全相同的體例與深度**。

**範本章**（動筆前必讀）：`books/bible/gospel-of-john/06-bread-of-life.md`
**語氣範本**：`.claude/skills/ask-elder-wong/references/voice.md`（語錄白名單）、`references/seven-keys.md`

---

## 三條紅線（違反任何一條整章作廢）

1. **不杜撰經文**。中文經文只能取自本次已核驗的本地檔案（見下）；英文 ESV 保留各章現有文字，不新增未核對的 ESV 段落。
2. **不杜撰語錄**。加「」歸給老弟兄的句子，只能出自 voice.md 白名單或倉庫實際檔案。其餘用他的語氣寫，不加引號。**馬可卷不是週四查經班的第一手筆記**——不得出現「出處：老弟兄馬可福音查經筆記」這類虛構出處；一律以「老弟兄查經法」（方法進路）署名。
3. **不杜撰注疏**。歷代注疏（Chrysostom/Calvin/MacArthur/Morgan）：**保留各章現有引文及其出處，可重排、可精簡，不得新增帶引號的新引文，不得更改或補造出處**。需要補充處，用不帶引號的立場綜述。

## 全書統一改名與版本

- 全文「黃長老」→「老弟兄」（出版匿名，同約翰卷；準則：約 3:30「他必興旺，我必衰微」）。
  - 「黃長老查經：…」小節 →「老弟兄查經法 (Reading with the Method)」
  - 「黃長老查經 · 深讀」→「老弟兄查經 · 深讀 (Going Deeper)」
  - 「黃長老精義」→「老弟兄精義 (The Distilled Key)」
- 經文版本：「和合本修訂版 (RCUV)」→「和合本 (CUV)」。所有 RCUV 字樣（含每日節奏表）改為 CUV。

## 中文經文替換程序（最重要的機械步驟）

已核驗的和合本文本（bolls.life CUV，繁體，與約翰卷同一文本底本）在：

```
/private/tmp/claude-501/-Users-jimxiao-Documents-GitHub-pubhub-books-bible-gospel-of-mark/607c1188-c6b8-4472-b293-451306d44673/scratchpad/cuv/mark-<章>.txt   （每行：節號 + 經文）
.../cuv/psalm-<篇>.txt
```

1. 保留本章現選的節段範圍（可微調增刪，以服事講解為準）。
2. **逐節以檔案文字替換現有 RCUV 文字**，一字不改，只允許：
   - 加直接引語的引號「」（原檔無引號）；
   - 句末語氣字「阿」→「啊」（同約翰卷慣例）；
   - 保留/添加 `^節號^` 上標與 `\jesus{...}`（耶穌親口的話）標記；本章核心金句可用 `\jesus{\textbf{「…」}}`；
   - 段內省略用 ⋯⋯。
3. 章首「經文核對」連結保留並改為：`[ai-eden.com/bible/mark/N](https://www.ai-eden.com/bible/mark/N?t=CUV,ESV&cols=2)`。

## 每章目標結構（依約翰卷第六章，節次與名稱照抄）

```
# 第N章：標題 (English)            ← 保留現有標題
馬可福音 N:x-y
**經文核對**：[…]

## 基督焦點 (Christ at the Center)
> **本章鑰詞：X Y** \
> **僕人座標**：一行，把本章放在全書骨幹上（三次預言受難／10:45／彌賽亞的隱秘／「立刻」），
>   並註明（全書骨幹見卷首《僕人的道路——全書的骨幹》）
（保留並打磨現有基督焦點段落）

## 配詩 (Opening Hymn)             ← 新增；用書卷概覽表該章聖詩，第一節原文 + 中文意譯
## 經文 (Scripture)
### 中文 — 和合本 (CUV)            ← 按上述程序替換
### English — ESV                  ← 保留現有
## 背景 (Context)                  ← 保留、可深化；至少一個表格
## 原文研讀 (Word Study)           ← 保留；希臘文列改用希臘字母（如 εὐθύς），照約翰卷表頭：希臘文|音譯|意義|經文|註解
## 神學要點 (Theological Points)   ← 由「領受與亮光」改名；保留五點，酌加對照表（約翰卷風格）
## 歷代注疏 (Historical Commentary)
> **體例說明**：本節是歷代解經者立場的綜述；帶引號引文均為編者自英文原著的中譯，並標明出處，
> 不應作為原文逐字引用轉引。
### 教父時期 / ### 改革宗時期 / ### 當代釋經（MacArthur 留此；Morgan 移出至「摩根深讀」）
## 詩篇回應 (Psalm Response)       ← 新增；1-2 段詩篇（取自 psalm-*.txt，關鍵句加粗）
## 聖詩默想 (Hymn Meditation)      ← 新增；另一首相配聖詩的一節（僅用著名聖詩第一節，不確定歌詞就換一首確定的）
## 三大資源深度整合 (Deep Integration: Three Core Resources)
### 摩根深讀 (G. Campbell Morgan)  ← 把本章現有 Morgan 材料移入並組織成 3-5 個小標題段（**關鍵句加粗**），
                                     末行「> 出處：G. Campbell Morgan, *The Gospel According to Mark*（本章相關講章）」
### 老弟兄查經法 (Reading with the Method) ← 由「黃長老查經」改名；保留精義句/帶你讀/連結；
                                     「華人教會處境應用」內容併入此節或深讀
## 配詩 (Hymns & Psalms)           ← 保留現有
## 老弟兄查經 · 深讀 (Going Deeper)
### 全經連線 (Tracing It Through Scripture)   ← 深化：舊約預表→本章成就→書信/啟示錄收尾，2-3 條線
### 提問式對話 (Let the Reader Speak)         ← 4 層遞進提問（先問/再問/追問/落到自己），照 voice.md 句法
### 活在今天 · AI時代 (Living It Today)
### 今天的祭壇 (Today's Altar)               ← 早晨/晚上/一個行動 三行（照約翰卷）
## 老弟兄精義 (The Distilled Key)
**一句話精義**：… / **貫通全經**：… / **無法迴避的問題**：…
（末尾 blockquote 金句只可用白名單語錄，或乾脆不加）
## 生命應用 (Application)
### 默想問題                        ← 現有默想問題 + 反思問題合併去重，5-6 題，每題加粗小標
### 禱告回應
## 與其他經文的關聯                 ← 新增；主題|本章經文|相關經文 對照表（含符類福音平行經文）
（刪除獨立的「## 反思問題」節）
*本章研讀整合三方資源：老弟兄查經法、John MacArthur (gty.org)、G. Campbell Morgan*
```

## 各章鑰詞（統一指定，概覽表與各章鑰詞框必須一致）

| 檔 | 章 | 鑰詞 |
|----|----|------|
| 01a | 1:1-8 | 預備 Prepare |
| 01b | 1:9-11 | 愛子 Beloved |
| 01c | 1:12-13 | 曠野 Wilderness |
| 01d | 1:14-45 | 權柄 Authority |
| 02 | 2:1-3:6 | 人子 Son of Man |
| 03 | 3:7-35 | 同在 With Him |
| 04 | 4:1-41 | 聽 Listen |
| 05 | 5:1-43 | 信 Believe |
| 06 | 6:1-56 | 牧人 Shepherd |
| 07 | 7:1-37 | 心 Heart |
| 08a | 8:1-26 | 餅 Bread |
| 08b | 8:27-38 | 基督 Christ |
| 09 | 9:1-50 | 聽他 Hear Him |
| 10 | 10:1-52 | 贖價 Ransom |
| 11 | 11:1-33 | 殿 Temple |
| 12 | 12:1-44 | 房角石 Cornerstone |
| 13 | 13:1-37 | 儆醒 Watch |
| 14 | 14:1-72 | 杯 Cup |
| 15 | 15:1-47 | 幔子 Veil |
| 16 | 16:1-20 | 復活 Risen |

## 文風校準

- 繁體中文為主，關鍵術語附原文（εὐθύς / immediately）。
- 老弟兄語氣：不急著給答案、提問帶著走、不迴避批判、落點是每日的活祭；禁空洞套話、禁 AI 腔、禁 emoji。
- 每章結尾的屬靈追問回到：「透過這段，你看見耶穌是誰？」
- Markdown 與 LaTeX 標記慣例照舊（`\jesus{}`、`^n^`、表格、`>` 引文塊）。

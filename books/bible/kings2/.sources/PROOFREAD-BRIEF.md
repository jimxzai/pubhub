# 列王紀下研讀——校對簡報 (Proofread Brief)

你是**校對神**：對**一至兩個已寫成的章節檔**做獨立校對。作者已跑過 lint 與 verify-citations，那些「綠燈」**不可信任**——
它們只檢查形式，不檢查真假。**你的工作是向原始來源重新取證**，不是複誦書稿自己的聲明。

倉庫根目錄 `/Users/jimxiao/dev/pubhub`；書稿 `books/bible/kings2/`；先讀 `.sources/AGENT-BRIEF.md`（規範）與 `00b-word-spine.md`（骨幹）。
語料 `$C` = `/private/tmp/claude-501/-Users-jimxiao-dev-pubhub-books-bible-kings2/1cbd47ad-1ea3-49ba-a2f5-312392d85f4d/scratchpad/corpus/`。

## 你要逐項重查的七個面（每一面都要真的去查，不可憑印象說「正確」）

1. **經文區塊**：`## 經文` 兩欄已由腳本自資料檔產生，不必重查；但**行文中**每一處加引號的聖經句子（本章與跨書），用 `python3 scripts/kings2-verse.py <地址>` 逐一比對字句與**地址**。地址錯、節次錯、漏字、擅自換字，都算缺陷。
2. **注疏引文（`> "…"`）**：英文必須逐字在語料中；`python3 scripts/verify-citations.py books/bible/kings2 --source $C/mhc-all.txt --source $C/barnes-all.txt --source $C/cambridge-all.txt --source $C/morgan-all.txt`；
   **並且人工看**：引文是否被**斷章取義**（原文接著一個「but」翻轉語氣？）、**中譯是否忠於原意**、署名作者是否對（例如把 Cambridge 的話掛成 Barnes）。
3. **未加引號的「綜述」**（「劍橋注釋認為……」「巴恩斯指出……」）：這是機器完全看不見的一面。逐條回到語料 grep 對應段落，確認該注釋家**確實**說過這個立場；沒有或說反了，改寫或刪除。
4. **希伯來文與計數**：原文研讀表每一列，用 `python3 scripts/kings2-hebrew.py <節次>` 對照字形、字義、節次（注意希伯來文節次與和合本有時差一節）；
   「全卷 N 節」「只此一次」一類主張用 `--find` 重算，**並逐節看詞形**（輔音相同詞形不同要排除）。算不出、查不到，就改成不帶數字的說法。沒有任何 Strong's 編號（已全書清除，若發現殘留請刪除）。
5. **史實、年代、人名、數字**：與 `00-overview.md` 的王表、經文本身核對；經外考古（碑文、編年史）只可用 `00a-kings2-position.md` 已有的說法。
6. **老弟兄與麥克阿瑟**：全章不得有加引號歸給老弟兄的話；麥克阿瑟引文必須通過 `python3 scripts/verify-sermon-quotes.py books/bible/kings2`，且上下文要如實（順帶提及者必須標明）。
7. **體例與中文**：11 節結構與順序；`**全書座標**` 行與**承前／指向**；章末「你看見耶穌了嗎」；表格分隔列 ≥72 字元；繁體；「裏」「甚麼」「·」；
   AI 腔與空洞套話（「值得注意的是」「這不是……而是……」連用）；同一重點在全章被重複講（chapter-template 的「一個重點只講一次」）；
   「默想問題」與「提問式對話」重複；編輯殘留（TODO、英文單詞夾在中文句中、半截句）。

## 修改規則

- **只改錯，不重寫風格。**保留作者的語氣、結構、篇幅；一處缺陷只動一處。修改要最小。
- 不確定是不是錯：**寧可改成不加引號的保守轉述，也不要保留可疑的加引號句**；真的無法確認的，列入回報的「待決」，不要硬改。
- 不改 `<!-- KINGS2:SCRIPTURE:BEGIN -->…END -->` 之間的任何字；不改檔頭 YAML；不改別章。
- 改完重跑 `lint-chapter-markup.py`、`check-book-spine.py`、`verify-citations.py`，並 `python3 scripts/gen-kings2-scripture-blocks.py --write` 不得產生差異。
- 不編譯 PDF、不 git add/commit。

## 回報格式（≤30 行）

1. 檔案與大小前後對比。
2. **修正清單**：逐條「位置｜原文｜問題｜改成甚麼｜依據（語料檔名或指令輸出）」。
3. **待決清單**：你無法裁定、需要作者決定的事。
4. **各面查核結論**：七個面各一行，寫「查了甚麼、用甚麼指令、結果」，不可只寫「通過」。
5. 你認為這章最強與最弱的各一處。

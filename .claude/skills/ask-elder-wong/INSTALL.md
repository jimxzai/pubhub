# 安裝與移植說明

## 安裝

```bash
# 全域安裝（任何專案可用）
unzip ask-elder-wong.zip -d ~/.claude/skills/

# 或安裝到某個專案
unzip ask-elder-wong.zip -d <專案>/.claude/skills/
```

安裝後以 `/ask-elder-wong <經文｜主題｜問題>` 呼叫，或讓它依 description 自動觸發。

## 移植到 pubhub 以外的環境時，請注意

`SKILL.md` 的「第一步：先查倉庫，再開口」假設存在 pubhub 倉庫的語料：

- `books/bible/john-thursday-wong/`
- `books/bible/*/elder-wong-systematic-study.md`
- `books/bible/psalter-elder-huang.pdf`
- 各書卷逐章書稿中的 `## 黃長老精義`、`## 黃長老查經 · 深讀`

**沒有這些檔案時，第一步會查無所獲**——這不影響其餘流程，技能仍可正常帶領查經，
只是失去「站在既有書稿上往前走」的優勢。若要在別的語料庫使用，請改寫第一步的
路徑表，指向該環境實際的查經材料。

## 語錄白名單的邊界

`references/voice.md` 是可直接引用的黃長老語錄**白名單**。SKILL.md 的第一條硬規則
規定：凡加「」歸給黃長老的句子必須有出處。在沒有 pubhub 語料的環境中，可引用的
範圍就只剩 `voice.md` 這一份——不可因為查不到倉庫檔案就自行擴充。

## 經文查證

引用經文以和合本為準，查證來源 `ai-eden.com`，備援 `cnbible.com`。
新環境需自行將這些網域加入 WebFetch 白名單。

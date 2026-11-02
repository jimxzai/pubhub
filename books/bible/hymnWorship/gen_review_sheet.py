#!/usr/bin/env python3
"""Generate docs/review-checklists/hymnworship.md — the pastoral review sheet for the Worship Book.

Everything an editor wrote (as opposed to Scripture and hymn text read from sources) is listed once, with the
claim it makes, and boxes for the reviewer.  Regenerated from build_book.py's own data, so it cannot drift."""
import re, runpy, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.argv = ["x", "/dev/null"]
g = runpy.run_path(str(HERE / "build_book.py"))
BOX = "☐ 通過　☐ 修改　☐ 刪除"
o = ["---", "title: 敬拜與禱告手冊 · 牧者審閱表", "date: 2026-11-01", "scope: books/bible/hymnWorship", "---", "",
     "# 敬拜與禱告手冊 · 牧者審閱表", "",
     "**用途**：本書的經文（和合本、NASB 1995）與聖詩歌詞都由來源讀出並做過機器核對；**下面這些是編者寫的**，沒有神學審閱。審閱一輪約一小時。",
     "**怎麼用**：每項選一個：通過／修改（在意見欄寫新句）／刪除。審閱人與日期填在最後。把填好的表交回，由編者改入 `build_book.py` 並重建。", ""]
o += ["## 一、詩篇「看見耶穌」（36 項）", "",
      "標示：**新約引用**＝新約經文自己引用或點名這篇詩；**主題呼應**＝編者列出的對照，新約沒有引用本篇；**傳統**＝教會傳統說法。請特別留意「主題呼應」是否有過度發揮的疑慮。", "",
      "| 詩篇 | 標示 | 句子 | 對照經文 | 審閱 | 意見 |", "|---|---|---|---|---|---|"]
for n in sorted(g["SEE_JESUS"]):
    line, refs = g["SEE_JESUS"][n]
    kind = "新約引用" if n in g["CITED"] else ("傳統" if n in g["TRADITION"] else "主題呼應")
    o.append(f"| {n} | {kind} | {line} | {'；'.join(g['label'](r) for r in refs)} | {BOX} | |")
o += ["", "## 二、聖詩「默想」問題（46 項）", "",
      "每個問題都應該扣住那首歌詞，換到別首詩就不成立。請把泛泛的、說教味重的、或對歌詞有誤解的標出來。", "",
      "| 編號 | 曲名 | 問題 | 審閱 | 意見 |", "|---|---|---|---|---|"]
for k, zh, ref in g["ALL"]:
    o.append(f"| {g['NUM'][k]} | {g['TITLE'][k]} | {g['HQ'][k]} | {BOX} | |")
o += ["", "## 三、每日短禱（14 項）與認罪禱告", "",
      "這些禱詞是編者寫的，用詞是否合宜、有無神學偏差、是否有「空洞套話」？", "",
      "| 日 | 時段 | 禱詞 | 審閱 | 意見 |", "|---|---|---|---|---|"]
src = (HERE / "build_book.py").read_text(encoding="utf-8")
days = re.findall(r'\("([^"]+)", (\d+), "(\w+)", (\d+), "(\w+)",\n\s+"([^"]+)",\n\s+"([^"]+)"\)', src)
for d, am, ah, pm, ph, am_pr, pm_pr in days:
    o.append(f"| {d} | 早晨（詩 {am}） | {am_pr} | {BOX} | |")
    o.append(f"| {d} | 晚間（詩 {pm}） | {pm_pr} | {BOX} | |")
conf = re.search(r"同聲認罪禱告[^\n]*\n\n> ([^\n]+)", (ROOT / "output/hymnworship-body.md").read_text(encoding="utf-8"))
if conf:
    o.append(f"| 主日 | 認罪禱告（卷三） | {conf.group(1)} | {BOX} | |")
o += ["", "## 四、骨幹章與其他編者論斷", "", "| 位置 | 論斷 | 審閱 | 意見 |", "|---|---|---|---|",
      f"| 骨幹章 | 以賽亞 6 的次序「看見→承認→領受→回應→被差遣」對應「顯現→照出人的真相→潔淨→發問→差遣」 | {BOX} | |",
      f"| 骨幹章 | 敬拜的第一個動詞是「父要」（約 4:23），不是人要 | {BOX} | |",
      f"| 骨幹章 | 詩篇 95：召、神是誰、跪、聽神說話（8-11 神開口） | {BOX} | |",
      f"| 骨幹章 | 三種偏差：以感覺為中心／只有熱情或只有真理／只剩一個鐘頭 | {BOX} | |",
      f"| 前言 | 「詩章、頌詞、靈歌」的對應：詩篇／聖詩／聖靈感動的歌唱與禱告 | {BOX} | |",
      f"| 卷三 | 十一個環節的次序與用詞 | {BOX} | |",
      f"| 卷三 | 七種特別場合的選讀經文是否合宜 | {BOX} | |",
      f"| 卷六 | 主禱文逐句的「可以這樣禱告」 | {BOX} | |",
      f"| 附錄四 | 處境索引的詩篇與聖詩配對（特別是病痛配詩 91，是否有成功神學的風險） | {BOX} | |", "",
      "---", "", "**審閱人**：＿＿＿＿＿＿＿＿　**日期**：＿＿＿＿＿＿＿＿　**整體意見**：", ""]
out = ROOT / "docs/review-checklists/hymnworship.md"
out.write_text("\n".join(o), encoding="utf-8")
print("wrote", out.relative_to(ROOT), "—", sum(1 for l in o if "☐" in l), "review items")

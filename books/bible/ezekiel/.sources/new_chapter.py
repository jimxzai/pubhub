#!/usr/bin/env python3
"""Create a chapter skeleton: YAML, H1, reference line, 經文核對, the 11 sections, and the
## 經文 block pasted VERBATIM from units/NN-*.scripture.md. Every other section holds a
<!-- TODO:name --> marker; fill them one at a time with the Edit tool (small edits, never one giant write).

  python3 .sources/new_chapter.py 05          # writes books/bible/ezekiel/05-<stem>.md (refuses to overwrite)
"""
import sys, re, pathlib, importlib.util
ROOT = pathlib.Path(__file__).resolve().parents[4]
BOOK = ROOT / "books/bible/ezekiel"
spec = importlib.util.spec_from_file_location("g", ROOT / "scripts/gen-ezekiel-scripture.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

TITLES = {
 "01":"迦巴魯河邊 (By the River Chebar)","02":"人子啊，你要吃這書卷 (Son of Man, Eat This Scroll)","03":"守望的人與封住的口 (The Watchman and the Sealed Mouth)",
 "04":"不說話的講道 (Preaching Without Words)","05":"向以色列的山說話 (Speak to the Mountains of Israel)","06":"殿裏的穢像 (Abominations in the Temple)",
 "07":"額上的記號與門檻上的榮耀 (The Mark and the Glory at the Threshold)","08":"榮耀離開這城 (The Glory Leaves the City)","09":"行李與假平安 (Baggage and False Peace)",
 "10":"偶像在心與無用的葡萄樹 (Idols in the Heart and the Useless Vine)","11":"被丟棄在田野的嬰孩 (The Foundling)","12":"兩隻大鷹與一根嫩枝 (Two Eagles and a Tender Twig)",
 "13":"惟有犯罪的，他必死亡 (The Soul That Sins Shall Die)","14":"輓歌與悖逆的歷史 (Lament and the History of Rebellion)","15":"刀劍之歌 (The Song of the Sword)",
 "16":"流人血的城 (The City of Blood)","17":"兩個姊妹 (Two Sisters)","18":"鍋與妻子之死 (The Pot and the Death of a Wife)","19":"鄰邦與推羅 (The Neighbors and Tyre)",
 "20":"為那隻船的哀歌 (Lament for the Ship)","21":"推羅王 (The Prince of Tyre)","22":"法老與尼羅河 (Pharaoh and the Nile)","23":"香柏樹與死亡坑 (The Cedar and the Pit)",
 "24":"逃來的人與開了的口 (The Fugitive and the Opened Mouth)","25":"以色列的牧人 (The Shepherds of Israel)","26":"兩座山 (Two Mountains)","27":"新心與新靈 (A New Heart and a New Spirit)",
 "28":"枯骨復活 (The Valley of Dry Bones)","29":"歌革與瑪各 (Gog of Magog)","30":"度量 (The Measuring)","31":"榮耀從東而來 (The Glory Returns from the East)",
 "32":"君王與土地 (The Prince and the Land)","33":"殿中流出的水 (The River from the Temple)","34":"耶和華的所在 (The LORD Is There)"}
YAML = "---\ntitle: 以西結書研讀\nsubtitle: Ezekiel Deep Study\nauthor: PubHub 三書精讀系統\ndate: 2026年10月\npublisher: 三書精讀出版系統\n---\n"
def main():
    nn = sys.argv[1].zfill(2)
    stem = next(s for s in g.UNITS if s.startswith(nn + "-"))
    c1, v1, c2, v2 = g.UNITS[stem]
    ref = f"以西結書 {c1}:{v1}-{v2}" if c1 == c2 else f"以西結書 {c1}:{v1}-{c2}:{v2}"
    out = BOOK / f"{stem}.md"
    if out.exists(): sys.exit(f"{out.name} exists; edit it instead")
    scripture = (BOOK / ".sources/units" / f"{stem}.scripture.md").read_text(encoding="utf8")
    t = lambda name: f"<!-- TODO:{name} -->"
    body = f"""{YAML}
# {TITLES[nn]}

{ref}

**經文核對**：[ai-eden.com/bible/ezekiel/{c1}](https://www.ai-eden.com/bible/ezekiel/{c1}?t=CUV,NASB&cols=2)

## 基督焦點 (Christ at the Center)

{t("基督焦點")}

---

## 配詩 (Opening Hymn)

{t("配詩")}

---

## 經文 (Scripture)

{scripture}
---

## 背景 (Context)

{t("背景")}

---

## 原文研讀 (Word Study)

{t("原文研讀")}

---

## 領受要點 (Truths Received)

{t("領受要點")}

---

## 歷代注疏 (Historical Commentary)

{t("歷代注疏")}

---

## 詩篇與聖詩 (Psalm & Hymn)

{t("詩篇與聖詩")}

---

## 老弟兄查經 (Reading with the Elder Brother)

{t("老弟兄查經")}

---

## 生命應用 (Application)

{t("生命應用")}

---

## 與其他經文的關聯

{t("關聯表")}

{t("結尾行")}
"""
    out.write_text(body, encoding="utf8"); print("wrote", out)
main()

#!/usr/bin/env python3
"""Create a chapter skeleton: YAML, H1, reference line, 經文核對, the 11 sections, and the
## 經文 block expanded VERBATIM from cuv.tsv / nasb1995.tsv by scripture/inject_scripture.py.
Every other section holds a <!-- TODO:name --> marker; fill them one at a time with the Edit
tool (small edits, never one giant write).

  python3 books/bible/lamentation/sources/new_chapter.py 02     # writes 02-<stem>.md (refuses to overwrite)
"""
import sys, pathlib, importlib.util

ROOT = pathlib.Path(__file__).resolve().parents[4]
BOOK = ROOT / "books/bible/lamentation"
spec = importlib.util.spec_from_file_location("inj", BOOK / "sources/scripture/inject_scripture.py")
inj = importlib.util.module_from_spec(spec); spec.loader.exec_module(inj)

# stem -> (chapter, first verse, last verse, H1)
UNITS = {
 "01-how-lonely-sits-the-city":        (1, 1, 11, "錫安獨坐 (How Lonely Sits the City)"),
 "02-is-it-nothing-to-you":            (1, 12, 22, "這事你們不介意嗎 (Is It Nothing to You?)"),
 "03-the-lord-as-an-enemy":            (2, 1, 10, "主如仇敵 (The Lord Has Become Like an Enemy)"),
 "04-pour-out-your-heart-like-water":  (2, 11, 22, "在主面前傾心如水 (Pour Out Your Heart Like Water)"),
 "05-the-man-who-has-seen-affliction": (3, 1, 20, "我是困苦人 (I Am the Man Who Has Seen Affliction)"),
 "06-new-every-morning":               (3, 21, 39, "每早晨都是新的 (New Every Morning)"),
 "07-let-us-examine-our-ways":         (3, 40, 66, "我們當查驗己行 (Let Us Examine Our Ways)"),
 "08-how-the-gold-has-grown-dim":      (4, 1, 11, "精金變色 (How the Gold Has Grown Dim)"),
 "09-the-lords-anointed":              (4, 12, 22, "耶和華的受膏者 (The LORD's Anointed)"),
 "10-restore-us-to-yourself":          (5, 1, 22, "求你使我們回轉 (Restore Us to Yourself)"),
}
YAML = "---\ntitle: 耶利米哀歌研讀\nsubtitle: Lamentations Deep Study\nauthor: PubHub 三書精讀系統\ndate: 2026年10月\npublisher: 三書精讀出版系統\n---\n"


def main():
    nn = sys.argv[1].zfill(2)
    stem = next(s for s in UNITS if s.startswith(nn + "-"))
    ch, v1, v2, title = UNITS[stem]
    out = BOOK / f"{stem}.md"
    if out.exists():
        sys.exit(f"{out.name} exists; edit it instead")
    t = lambda name: f"<!-- TODO:{name} -->"
    body = f"""{YAML}
# {title}

耶利米哀歌 {ch}:{v1}-{v2}

**經文核對**：[ai-eden.com/bible/lamentations/{ch}](https://www.ai-eden.com/bible/lamentations/{ch}?t=CUV,NASB&cols=2)

## 基督焦點 (Christ at the Center)

{t("基督焦點")}

---

## 配詩 (Opening Hymn)

{t("配詩")}

---

{inj.block(f"{ch}:{v1}-{v2}").rstrip()}

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

---

{t("結尾行")}
"""
    out.write_text(body, encoding="utf8")
    print("wrote", out)


main()

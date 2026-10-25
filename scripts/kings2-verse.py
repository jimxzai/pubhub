#!/usr/bin/env python3
"""Print 和合本 verses for quoting in the 2 Kings chapters (no memory quoting).

    python3 scripts/kings2-verse.py 太3:4 賽8:19-20 王上13:2 [--eden]

Source: bible.fhl.net (和合本 `unv`, modern punctuation — the same base the
chapters' 經文 blocks use), with the project's proper-noun normalisation
(撒瑪利亞、大馬色、約但、瑪代、伯拉、利巴嫩 … per ai-eden.com, the project's
standard source) and 裡→裏, 「．」→「·」. `--eden` additionally prints the
ai-eden.com text (rate-limited: one request per 4 s; use sparingly).

Chapter JSON is cached in $KINGS2_VERSE_CACHE (default /tmp/kings2-verse-cache),
shared by anyone running this concurrently.
"""
import json, os, pathlib, re, sys, time, urllib.parse, urllib.request

CACHE = pathlib.Path(os.environ.get("KINGS2_VERSE_CACHE", "/tmp/kings2-verse-cache"))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"}
REP = [("撒馬利亞", "撒瑪利亞"), ("大馬士革", "大馬色"), ("約旦", "約但"), ("米底亞", "瑪代"),
       ("幼發拉底", "伯拉"), ("黎巴嫩", "利巴嫩"), ("安派", "安排"), ("裡", "裏"), ("癒", "愈"),
       ("．", "·"), ("‧", "·"), ("\u3000神", "神")]
ALIAS = {"約壹": "約一", "約貳": "約二", "約參": "約三", "約一": "約一", "約二": "約二", "約三": "約三"}
EDEN = ["genesis exodus leviticus numbers deuteronomy joshua judges ruth 1-samuel 2-samuel 1-kings 2-kings 1-chronicles 2-chronicles ezra nehemiah esther job psalms proverbs ecclesiastes song-of-solomon isaiah jeremiah lamentations ezekiel daniel hosea joel amos obadiah jonah micah nahum habakkuk zephaniah haggai zechariah malachi matthew mark luke john acts romans 1-corinthians 2-corinthians galatians ephesians philippians colossians 1-thessalonians 2-thessalonians 1-timothy 2-timothy titus philemon hebrews james 1-peter 2-peter 1-john 2-john 3-john jude revelation".split()]
BOOKS = "創 出 利 民 申 書 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 詩 箴 傳 歌 賽 耶 哀 結 但 何 珥 摩 俄 拿 彌 鴻 哈 番 該 亞 瑪 太 可 路 約 徒 羅 林前 林後 加 弗 腓 西 帖前 帖後 提前 提後 多 門 來 雅 彼前 彼後 約一 約二 約三 猶 啟".split()
EDEN = EDEN[0] if isinstance(EDEN[0], list) else EDEN


def get(url):
    for i in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode("utf8")
        except Exception:
            time.sleep(2 * (i + 1))
    raise SystemExit("fetch failed: " + url)


def chapter(book, ch):
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"{book}-{ch}.json"
    if f.exists():
        return {int(k): v for k, v in json.loads(f.read_text(encoding="utf8")).items()}
    d = json.loads(get(f"https://bible.fhl.net/json/qb.php?chineses={urllib.parse.quote(book)}&chap={ch}&version=unv&strong=0"))
    out = {}
    for r in d.get("record", []):
        t = r["bible_text"]
        for a, b in REP:
            t = t.replace(a, b)
        out[int(r["sec"])] = t
    f.write_text(json.dumps(out, ensure_ascii=False), encoding="utf8")
    return out


def eden(book, ch):
    slug = EDEN[BOOKS.index(book)]
    time.sleep(4)
    d = json.loads(get(f"https://www.ai-eden.com/api/bible/{slug}/{ch}?t=CUV"))
    return {v["verse"]: v["textZh"] for v in d["data"]["verses"]}


def main(argv):
    show_eden = "--eden" in argv
    for ref in [a for a in argv if not a.startswith("--")]:
        m = re.match(r"^(.+?)(\d+):(\d+)(?:-(\d+))?$", ref)
        if not m:
            print(f"?? cannot parse {ref}")
            continue
        book = ALIAS.get(m[1], m[1])
        if book not in BOOKS:
            print(f"?? unknown book {m[1]} (use: {' '.join(BOOKS)})")
            continue
        ch, a = int(m[2]), int(m[3]); b = int(m[4] or a)
        d = chapter(book, ch)
        miss = [v for v in range(a, b + 1) if v not in d]
        if miss:
            print(f"?? {ref}: verses {miss} not found")
        print(f"[{ref}] " + "".join(f"^{v}^{d[v]}" for v in range(a, b + 1) if v in d))
        if show_eden:
            e = eden(book, ch)
            print(f"[{ref} · ai-eden] " + "".join(f"^{v}^{e.get(v, '')}" for v in range(a, b + 1)))


if __name__ == "__main__":
    main(sys.argv[1:])

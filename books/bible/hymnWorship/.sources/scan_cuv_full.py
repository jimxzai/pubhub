#!/usr/bin/env python3
"""Whole-Bible diff: ai-eden data/cuv.json vs FHL 和合本 (unv). Known 1919-vs-modernised orthography pairs are
filtered out; what is left is written to cuv-full-scan.json for review. One request per chapter, 1 s apart, cached."""
import difflib, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
HERE = Path(__file__).parent; OUT = HERE / "fhl_full"; OUT.mkdir(exist_ok=True)
cuv = json.load(open("/Users/jimxiao/dev/ai-eden/data/cuv.json", encoding="utf-8"))
ZH = {"genesis":"創","exodus":"出","leviticus":"利","numbers":"民","deuteronomy":"申","joshua":"書","judges":"士","ruth":"得","1-samuel":"撒上","2-samuel":"撒下","1-kings":"王上","2-kings":"王下","1-chronicles":"代上","2-chronicles":"代下","ezra":"拉","nehemiah":"尼","esther":"斯","job":"伯","psalms":"詩","proverbs":"箴","ecclesiastes":"傳","song-of-solomon":"歌","isaiah":"賽","jeremiah":"耶","lamentations":"哀","ezekiel":"結","daniel":"但","hosea":"何","joel":"珥","amos":"摩","obadiah":"俄","jonah":"拿","micah":"彌","nahum":"鴻","habakkuk":"哈","zephaniah":"番","haggai":"該","zechariah":"亞","malachi":"瑪","matthew":"太","mark":"可","luke":"路","john":"約","acts":"徒","romans":"羅","1-corinthians":"林前","2-corinthians":"林後","galatians":"加","ephesians":"弗","philippians":"腓","colossians":"西","1-thessalonians":"帖前","2-thessalonians":"帖後","1-timothy":"提前","2-timothy":"提後","titus":"多","philemon":"門","hebrews":"來","james":"雅","1-peter":"彼前","2-peter":"彼後","1-john":"約一","2-john":"約二","3-john":"約三","jude":"猶","revelation":"啟"}
punct = re.compile(r"[\s　、，。；：！？「」『』（）．·—…─\-,.;:!?\"'()\[\]]")
PAIRS = {("的","地"),("他","它"),("他","牠"),("他","她"),("麼","嗎"),("罷","吧"),("那","哪"),("阿","啊"),("燄","焰"),("罣","掛"),("但","旦"),("着","著"),("裏","裡"),("裡","裏"),("纔","才"),("甚","什"),("麼","么")}
def get(book, ch):
    f = OUT / f"{book}-{ch}.json"
    if f.exists(): return json.load(open(f, encoding="utf-8"))
    u = "https://bible.fhl.net/json/qb.php?" + urllib.parse.urlencode({"chineses": ZH[book], "chap": ch, "sec": "1-180", "version": "unv", "gb": 0})
    for _ in range(3):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40))
            if d["status"] == "success" and d["record_count"] > 0:
                f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8"); time.sleep(1); return d
        except Exception as e: time.sleep(3)
    return None
res, miss, n = [], [], 0
for key in cuv:
    book, ch = key.rsplit("-", 1)
    d = get(book, int(ch))
    if not d: miss.append(key); continue
    fh = {r["sec"]: r["bible_text"] for r in d["record"]}
    for v, a in cuv[key].items():
        n += 1; b = fh.get(int(v))
        if b is None: res.append((key, v, "FHL-MISSING-VERSE", a[:40], "")); continue
        A, B = punct.sub("", a), punct.sub("", b)
        if A == B: continue
        ops = [(t, A[i1:i2], B[j1:j2]) for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B).get_opcodes() if t != "equal"]
        rest = [o for o in ops if not (o[0] == "replace" and (o[1], o[2]) in PAIRS) and not (o[0] == "replace" and o[1] in ("作","做","是","譯","或") )]
        if rest: res.append((key, v, "DIFF", a[:60], rest))
    if len(res) % 1 == 0 and ch == "1": json.dump({"n": n, "res": res, "miss": miss}, open(HERE / "cuv-full-scan.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump({"n": n, "res": res, "miss": miss, "done": True}, open(HERE / "cuv-full-scan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("DONE verses", n, "residual", len(res), "missing chapters", len(miss))

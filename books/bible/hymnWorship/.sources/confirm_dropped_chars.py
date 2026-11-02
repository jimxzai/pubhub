#!/usr/bin/env python3
"""For every verse where FHL has ONE extra Chinese character that ai-eden's cuv.json lacks, ask a third source
(cnbible.com, CUVMPT) whether the local context (3 chars before + the char + 3 chars after, FHL spelling) occurs in that
chapter. Output: ai-eden-cuv-dropped-chars.md (candidates, with how many independent sources agree)."""
import difflib, html, json, re, time, urllib.request
from pathlib import Path
HERE = Path(__file__).parent; OUT = HERE / "cnbible"; OUT.mkdir(exist_ok=True)
cuv = json.load(open("/Users/jimxiao/dev/ai-eden/data/cuv.json", encoding="utf-8"))
scan = json.load(open(HERE / "cuv-full-scan.json", encoding="utf-8"))
punct = re.compile(r"[\s　、，。；：！？「」『』（）．·‧•—…─\-,.;:!?\"'()\[\]【】〈〉《》－]")
cjk = re.compile(r"[一-鿿]")
SLUG = lambda b: b.replace("-", "") if b[0].isdigit() else b
def cn(book, ch):
    f = OUT / f"{book}-{ch}.txt"
    if f.exists(): return f.read_text(encoding="utf-8")
    for slug in (book, SLUG(book)):
        try:
            h = urllib.request.urlopen(urllib.request.Request(f"https://www.cnbible.com/{slug}/{ch}.htm", headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read().decode("utf-8", "ignore")
            t = punct.sub("", html.unescape(re.sub(r"<[^>]+>", " ", h)))
            f.write_text(t, encoding="utf-8"); time.sleep(1); return t
        except Exception: continue
    return ""
cands = []
for key, v, kind, ctx, ops in scan["res"]:
    ins = [o for o in ops if o[0] == "insert" and len(o[2]) == 1 and cjk.match(o[2])]
    rest = [o for o in ops if o not in ins and (o[1] or o[2]) and cjk.search(o[1] + o[2])]
    if len(ins) == 1 and not rest: cands.append((key, v))
print("candidates", len(cands))
rows = []
for key, v in cands:
    book, ch = key.rsplit("-", 1)
    a = cuv[key][v]
    fh = {r["sec"]: r["bible_text"] for r in json.load(open(HERE / "fhl_full" / f"{key}.json", encoding="utf-8"))["record"]}[int(v)]
    A, B = punct.sub("", a), punct.sub("", fh)
    op = [o for o in difflib.SequenceMatcher(None, A, B).get_opcodes() if o[0] == "insert"][0]
    j = op[3]; win = B[max(0, j - 3): j + 4]
    c = cn(book, ch)
    rows.append((key, v, B[j], win, bool(c) and win in c, a, fh))
conf = [r for r in rows if r[4]]
md = ["# ai-eden `data/cuv.json` — 疑似漏字（FHL 多一字，且 cnbible.com 同處也有）\n",
      f"掃描範圍：全部 {scan['n']} 節。條件：FHL 和合本比 ai-eden 恰好多一個漢字，其餘差異只屬已知的現代化字形；第三來源 cnbible.com 同一章裡出現「前三字＋該字＋後三字」。\n",
      f"候選 {len(rows)} 節，三來源一致 {len(conf)} 節，其餘 {len(rows) - len(conf)} 節只有 FHL 一家（需人工判斷，不列為已確認）。\n",
      "| 章節 | 漏的字 | ai-eden 現況 | 應為（FHL） | 三源 |", "|---|---|---|---|---|"]
for key, v, ch_, win, ok, a, fh in sorted(rows, key=lambda r: (not r[4], r[0], int(r[1]))):
    md.append(f"| {key}:{v} | {ch_} | {a[:44]} | {fh[:44]} | {'✔' if ok else '—'} |")
(HERE / "ai-eden-cuv-dropped-chars.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("confirmed by 3 sources:", len(conf), "of", len(rows))

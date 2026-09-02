#!/usr/bin/env python3
"""
Regenerate the Philemon book's two indexes FROM THE BUILT PDF.

Why from the PDF: an index maintained by hand drifts from the text the moment
anything is edited. This reads the typeset artifact, so the page numbers are
true by construction.

  1. books/bible/1philimon/appendix-12-scripture-index.md  (generated whole)
  2. books/bible/1philimon/index.md                        (page column rewritten
                                                            in place; terms kept)

Run AFTER a build, then build once more so the indexes land in the PDF:

    bash scripts/build-philemon-consolidated.sh
    python3 scripts/gen-philemon-indexes.py
    bash scripts/build-philemon-consolidated.sh

Page numbers stay valid across that second build because both indexes sit at
the very end of the book, so their own length cannot move anything they cite.
"""
import subprocess, re, sys, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF  = os.path.join(ROOT, 'output', 'philemon-consolidated.pdf')
BOOK = os.path.join(ROOT, 'books', 'bible', '1philimon')

def pages_of(pdf):
    txt = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
    return txt.split('\f')

def folio_offset(pages):
    """printed folio = pdf page - offset, in main matter. Derived, not assumed."""
    c = collections.Counter()
    for i, p in enumerate(pages, start=1):
        lines = [l.strip() for l in p.split('\n') if l.strip()]
        if not lines:
            continue
        for cand in (lines[-1], lines[0]):
            m = (re.fullmatch(r'(\d{1,3})', cand) or re.match(r'^(\d{1,3})\s', cand)
                 or re.search(r'\s(\d{1,3})$', cand))
            if m:
                c[i - int(m.group(1))] += 1
                break
    off, n = c.most_common(1)[0]
    if n < 100:
        sys.exit('could not derive a stable folio offset (best %r seen %d times)' % (off, n))
    return off

# The two index appendices must not index themselves: a reference pointing at
# the index is noise, and because the index sits at the end of the book its own
# growth shifts those self-references on every pass, so the numbers never settle.
# Match only the RUNNING HEAD, not body text: an earlier version scanned the
# first 400 characters and swallowed ordinary content pages that merely
# mentioned an index, silently dropping four real terms.
INDEX_HEAD = re.compile(r'(附錄十二：經文索引|索引\s*$|^\s*索引\b)')

def is_index_page(page):
    lines = [l.strip() for l in page.split("\n") if l.strip()]
    if not lines:
        return False
    for cand in (lines[0], lines[-1]):
        if INDEX_HEAD.search(cand):
            return True
    return False

def rng(nums):
    nums = sorted(set(nums)); out = []; s = p = nums[0]
    for n in nums[1:]:
        if n == p + 1:
            p = n; continue
        out.append(str(s) if s == p else '%d-%d' % (s, p)); s = p = n
    out.append(str(s) if s == p else '%d-%d' % (s, p))
    return ', '.join(out)

BOOKS = [
 ("創世記",["創世記","創"]),("出埃及記",["出埃及記","出"]),("利未記",["利未記","利"]),
 ("民數記",["民數記","民"]),("申命記",["申命記","申"]),("路得記",["路得記","得"]),
 ("撒母耳記上",["撒上"]),("約伯記",["約伯記","伯"]),("詩篇",["詩篇","詩"]),
 ("箴言",["箴言","箴"]),("以賽亞書",["以賽亞書","賽"]),("耶利米書",["耶利米書","耶"]),
 ("阿摩司書",["阿摩司書","摩"]),
 ("馬太福音",["馬太福音","太"]),("馬可福音",["馬可福音","可"]),("路加福音",["路加福音","路"]),
 ("約翰福音",["約翰福音","約"]),("使徒行傳",["使徒行傳","徒"]),("羅馬書",["羅馬書","羅"]),
 ("哥林多前書",["哥林多前書","林前"]),("哥林多後書",["哥林多後書","林後"]),
 ("加拉太書",["加拉太書","加"]),("以弗所書",["以弗所書","弗"]),("腓立比書",["腓立比書","腓"]),
 ("歌羅西書",["歌羅西書","西"]),("帖撒羅尼迦前書",["帖前"]),
 ("提摩太前書",["提摩太前書","提前"]),("提摩太後書",["提摩太後書","提後"]),
 ("提多書",["提多書","多"]),("腓利門書",["腓利門書","門"]),
 ("希伯來書",["希伯來書","來"]),("雅各書",["雅各書","雅"]),
 ("彼得前書",["彼得前書","彼前"]),("彼得後書",["彼得後書","彼後"]),
 ("約翰一書",["約翰一書","約壹"]),("啟示錄",["啟示錄","啟"]),
]
ORDER = {b: i for i, (b, _) in enumerate(BOOKS)}
PAIRS = sorted(((a, full) for full, abs_ in BOOKS for a in abs_), key=lambda x: -len(x[0]))
TO_FULL = dict(PAIRS)
ALT = "|".join(re.escape(a) for a, _ in PAIRS)
PAT_CV   = re.compile(r'(' + ALT + r')\s?(\d{1,3}):(\d{1,3})(?:[-–](\d{1,3}))?')
PAT_PHLM = re.compile(r'(門|腓利門書)\s?(\d{1,2})(?:[-–](\d{1,2}))?(?![:\d])')

def scripture_index(pages, off):
    hits = collections.defaultdict(set)
    for i, page in enumerate(pages, start=1):
        if i <= off or is_index_page(page):
            continue
        f = i - off
        for m in PAT_CV.finditer(page):
            b = TO_FULL[m.group(1)]
            if b == "腓利門書":
                continue
            hits[(b, int(m.group(2)), int(m.group(3)))].add(f)
        for m in PAT_PHLM.finditer(page):
            v = int(m.group(2))
            if 1 <= v <= 25:
                hits[("腓利門書", 1, v)].add(f)
    phlm  = sorted([k for k in hits if k[0] == "腓利門書"], key=lambda k: k[2])
    other = sorted([k for k in hits if k[0] != "腓利門書"],
                   key=lambda k: (ORDER[k[0]], k[1], k[2]))
    L = ["---", "title: 附錄十二：經文索引", 'subtitle: "Scripture Index"', "---", "",
         "# 附錄十二：經文索引", "**Scripture Index**", "",
         "> 頁碼為本書正文頁碼。本索引由排版後的成品自動編製（`scripts/gen-philemon-indexes.py`），",
         "> 逐頁掃描全書的經文引用，因此不會與內文脫節。", "", "---", "",
         "## 一、腓利門書（逐節）", "", "| 節 | 頁碼 |", "|---|---|"]
    for k in phlm:
        L.append("| 門 %d | %s |" % (k[2], rng(hits[k])))
    L += ["", "---", "", "## 二、其他經文", ""]
    cur = None
    for k in other:
        if k[0] != cur:
            cur = k[0]
            L += ["", "### " + cur, "", "| 章節 | 頁碼 |", "|---|---|"]
        L.append("| %s %d:%d | %s |" % (k[0], k[1], k[2], rng(hits[k])))
    L.append("")
    open(os.path.join(BOOK, 'appendix-12-scripture-index.md'), 'w',
         encoding='utf-8').write("\n".join(L))
    return len(phlm), len(other), len({k[0] for k in other})

def topical_index(pages, off):
    main  = [(i, p) for i, p in enumerate(pages, start=1)
             if i > off and not is_index_page(p)]
    total = len(main)
    def find(term):
        if not term:
            return None
        fs = [i - off for i, p in main if term in p]
        if not fs:
            return None
        return "全書" if len(fs) > 0.40 * total else rng(fs)

    path = os.path.join(BOOK, 'index.md')
    out, col, changed, missed = [], None, 0, []
    for ln in open(path, encoding='utf-8').read().split('\n'):
        if not ln.startswith('|'):
            out.append(ln); continue
        cells = ln.split('|')
        stripped = [c.strip() for c in cells]
        if any(s.startswith('頁碼') for s in stripped):          # header row
            col = next(k for k, s in enumerate(stripped) if s.startswith('頁碼'))
            out.append(ln); continue
        if set(''.join(stripped)) <= set('-: '):                 # separator row
            out.append(ln); continue
        if col is None or col >= len(cells):
            out.append(ln); continue
        term = stripped[1]
        pl = find(term)
        if pl is None and len(stripped) > 2:
            m = re.match(r'^([Ͱ-Ͽἀ-῿]+)', stripped[2])
            if m:
                pl = find(m.group(1))
        if pl is None:
            missed.append(term); out.append(ln); continue
        cells[col] = ' ' + pl + ' '
        out.append('|'.join(cells)); changed += 1
    open(path, 'w', encoding='utf-8').write('\n'.join(out))
    return changed, missed

if __name__ == '__main__':
    if not os.path.exists(PDF):
        sys.exit('build the PDF first: bash scripts/build-philemon-consolidated.sh')
    pages = pages_of(PDF)
    off = folio_offset(pages)
    print('folio offset: printed page = pdf page - %d' % off)
    a, b, c = scripture_index(pages, off)
    print('scripture index: %d Philemon verses, %d other references, %d books' % (a, b, c))
    ch, missed = topical_index(pages, off)
    print('topical index: %d rows repaginated, %d terms not found' % (ch, len(missed)))
    if missed:
        print('  not found:', ', '.join(missed[:8]))

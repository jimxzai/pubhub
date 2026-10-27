#!/usr/bin/env python3
"""Revise the user-designated PDF in place.

Pages 1-FRONT_PAGES are the immutable original baseline, patched but never
reflowed (per the 2026-09-21 decision recorded in SOURCE-RECONCILIATION.md).
Chapter 12 onward is a fresh xelatex render of the current markdown sources,
spliced on — see the FRONT_PAGES comment below and PUBLISHER-FIX-REPORT.md's
2026-09-24 entry for why.
"""
from pathlib import Path
import os
import hashlib
import json
import re
import fitz
from cover_design import front_cover, back_cover
from editorial_upgrade import upgrade, unchanged_outside
from patch_fonts import load_songti_regular, load_times_italic

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'sources/archive/romans-original-baseline.pdf'
OUTPUT = Path(os.environ.get('ROMANS_CANONICAL_PDF', ROOT.parents[2] / 'output/romans-consolidated.pdf'))
EXPECTED_HASH = 'abed9a6294db5db9a9da7fc96a5e482d36013103ce74783048434339a515524b'
CHAPTER_PAGES = [52,68,83,100,115,132,147,162,181,198,212,229,244,261,277,294]
CHAPTER_IDS = [8,9,10,12,13,15,16,17,19,20,21,23,24,25,26,27]
CHANGED = {1,9,10,27,30,48,69,148}
# 2026-09-24: pages 1-FRONT_PAGES stay the patched original baseline
# (pixel-frozen); chapter 12 onward is replaced by a fresh xelatex render of
# the current markdown sources (build_fresh_pdf.py), so a content addition
# too large to fit the frozen page's whitespace (the 背景-section
# doctrine-to-ethic table) can actually ship. See PUBLISHER-FIX-REPORT.md's
# 2026-09-24 entry for the full rationale.
FRONT_PAGES = 228
CHAPTER_12_MARKER = '活祭與身體的恩賜'
# font-family names the real Songti SC face registered below — naming a
# system font here instead ("serif" or "Songti SC") silently renders in
# insert_htmlbox's own bundled Droid Sans Fallback fallback (see
# patch_fonts.py); every put()/replace() page must go through this face.
CSS = '''
body {font-family:"RomansPatch"; font-size:10.3pt; line-height:1.36; color:#172238; margin:0;}
p {margin:0 0 9pt 0;} h1 {font-family:"RomansPatch"; font-size:19pt; font-weight:normal; color:#223c64; margin:0 0 13pt 0;}
h2 {font-family:"RomansPatch"; font-size:12pt; color:#8a641c; font-weight:normal; margin:12pt 0 6pt 0;}
table {border-collapse:collapse; width:100%;} td,th {padding:3pt 5pt; border-bottom:0.4pt solid #d8d4ca; font-weight:normal; text-align:left;}
.small {font-size:9pt;} .rule {border-top:0.7pt solid #8a641c; padding-top:10pt;}
'''
_PATCH_ARCHIVE = None

def _patch_archive():
    # The italic face matches the original baseline's treatment of inline
    # Greek/Hebrew transliterations (e.g. oiktirmōn on p.229), which render
    # in Times New Roman Italic — confirmed via get_text('dict') span flags
    # on the unpatched page, not assumed.
    global _PATCH_ARCHIVE
    if _PATCH_ARCHIVE is None:
        songti = load_songti_regular()
        italic = load_times_italic()
        _PATCH_ARCHIVE = (
            '@font-face { font-family: "RomansPatch"; src: url("songti-regular.ttf"); font-style: normal; }\n'
            '@font-face { font-family: "RomansPatch"; src: url("romans-patch-italic.ttf"); font-style: italic; }\n',
            fitz.Archive([(songti, 'songti-regular.ttf'), (italic, 'romans-patch-italic.ttf')]),
        )
    return _PATCH_ARCHIVE

def put(page, rect, html, size=None):
    font_face, archive = _patch_archive()
    css = font_face + CSS + (f'body {{font-size:{size}pt;}}' if size else '')
    spare, scale = page.insert_htmlbox(rect, html, css=css, archive=archive, scale_low=1)
    if spare < 0 or scale < 1:
        raise RuntimeError(f'Text does not fit on source page {page.number+1}: {rect}')

def replace(page, rect, html, size=10.3):
    page.add_redact_annot(rect, fill=(1,1,1))
    page.apply_redactions(images=0, graphics=0)
    put(page, rect, html, size)

# Single-character word-choice fixes (below) are mid-sentence and must sit
# flush against untouched neighboring glyphs on the same line, so the
# `insert_htmlbox`/`put()` route above (fine for the whole-paragraph
# rewrites) is unusable here: its CJK metrics run ~20% wider per character
# than this book's actual body font. Instead this draws the replacement with
# insert_text() using the exact same font, size, color and baseline origin
# as the original glyphs (extracted via get_text('rawdict') at each target),
# which is pixel-exact rather than approximate.
def patch_word(page, rect, origin, text, fontsize, color, fontbuffer):
    page.add_redact_annot(rect, fill=(1,1,1))
    page.apply_redactions(images=0, graphics=0)
    page.insert_font(fontname='SongtiPatch', fontbuffer=fontbuffer)
    page.insert_text(origin, text, fontsize=fontsize, fontname='SongtiPatch', color=color)

def main():
    if hashlib.sha256(BASE.read_bytes()).hexdigest() != EXPECTED_HASH:
        raise SystemExit('Baseline differs from the designated original; stop rather than edit another edition')
    original = fitz.open(BASE)
    doc = fitz.open(BASE)
    assert len(doc) == 348 and tuple(doc[0].rect) == (0,0,504,720)
    front_cover(doc[0])
    # The original copyright page is rewritten in its original front-matter slot.
    replace(doc[8], fitz.Rect(47,340,457,674), '''
      <h1>出版與引用說明</h1>
      <p>羅馬書研讀 · 因信得生<br>PubHub 三書精讀系統 · 三書精讀出版系統<br>Soli Deo Gloria — 唯獨榮耀神</p>
      <p>整合老弟兄查經方法論、John MacArthur 逐節解經與 G. Campbell Morgan 的結構分析。老弟兄部分是方法論的應用，並非羅馬書原始查經筆記的逐字記錄。</p>
      <h2>版本與引用</h2>
      <p>本次校訂保留原版內容與版式，併入編輯修正及查閱功能。中文經文標示為和合本，英文為 NASB 1995。原稿的歷史核對記錄不等於本版已重做全部查證。</p>
      <p class="small">NASB 1995 copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. All rights reserved. lockman.org</p>
      <p class="small">本版供出版者審閱；經文、引文及詩歌的使用許可仍待核定。原版「Used by permission」文字尚無隨附授權證據，因此不沿用為本版授權保證。ISBN 待出版者決定。</p>
    ''', 10)
    # Use an existing blank verso. No pages are inserted, so printed pagination
    # and every existing contents destination remain valid.
    assert not doc[9].get_text().strip()
    put(doc[9], fitz.Rect(47,52,457,673), '''
      <h1>本次校訂與查閱指引</h1>
      <p>本書保留原版圖表、五卷分段與完整研讀文字；封面沿用書名，提升系列設計。本次吸收編輯修正；原有印刷頁碼不變。</p>
      <h2>閱讀次序</h2>
      <p>先讀卷首定位與概覽，再讀「全書骨幹」及完整的「全書領受總綱」。按五卷次序進入十六章；卷末、索引、參考資料與跋仍在原位。</p>
      <h2>十六章快速查閱</h2>
      <table>
      <tr><th>章</th><th>印刷頁</th><th>章</th><th>印刷頁</th></tr>
    ''' + ''.join(f'<tr><td>第 {i+1} 章</td><td>{CHAPTER_PAGES[i]-20}</td><td>第 {i+9} 章</td><td>{CHAPTER_PAGES[i+8]-20}</td></tr>' for i in range(8)) + '''
      </table>
      <p class="small">點選章號可跳至正文。電子書籤與經文索引的章號亦提供跳轉。</p>
      <h2>本次編輯修正</h2>
      <p>印刷第 7、10、28 頁：撤去未附確切出處的摩根具名引句，改作編者比較；不再以此推定兩封書信的直接寫作次序。</p>
      <p class="small rule">引文、譯文、神學審查與使用許可仍須各自核定。電子導覽和排版檢查不代表這些審查已完成。</p>
    ''')
    replacement = '編者比較：加拉太書與羅馬書都論及信心、律法與稱義，但論述方式與牧養處境各有重點。因未取得摩根原話的確切書目與頁碼，本版不沿用具名引句，也不以此核定兩封信的直接寫作次序。'
    replace(doc[26], fitz.Rect(61,301,457,354), '<p>'+replacement+'</p>', 9.5)
    replace(doc[29], fitz.Rect(45,417,448,508), '<p>羅馬書與加拉太書可互相參照。以下為編者的主題比較：</p><p>'+replacement+'</p>', 10)
    # Preserve the cross-page sentence: this paragraph still ends with 羅馬,
    # followed by 書 on the next page, as in the original text.
    replace(doc[47], fitz.Rect(45,595,448,669), '<p>編者比較：加拉太書與羅馬書都論及信心、律法與稱義；本版未取得支持原摩根引句的確切出處，故不以它斷定兩封信的直接寫作次序。以下仍從主題作比較：加拉太書與羅馬書像兩支軍隊從不同方向攻打同一座城：加拉太書駁斥外邦信徒被說服要靠割禮與律法「補足」因信稱義的軟弱，羅馬</p>', 10.1)
    # Scripture-wording corrections (2026-09-21 校對神 pass), frozen-region
    # entries only (chapters 2 and 8; pages 69/148). The remaining entries
    # this list used to carry (chapters 13-16 and back matter) targeted pages
    # now replaced by the 2026-09-24 from-source re-layout below — their
    # corrected wording is confirmed present in the chapter/appendix source
    # files instead (verified by grep before removal), so the fresh render
    # already carries them and the pixel patches would be dead code.
    songti = load_songti_regular()
    BODY, BODY_COLOR = 9.925399780273438, (50/255, 50/255, 50/255)
    fixes = [
        (68, (182.5965576171875,267.96014404296875,222.41726684570312,277.88555908203125), (182.5965576171875,276.4960021972656), '積蓄忿怒', BODY, BODY_COLOR),
        (68, (309.82110595703125,319.5091552734375,350.21746826171875,329.4345703125), (309.82110595703125,328.0450134277344), '就以忿怒', BODY, BODY_COLOR),
        (147, (151.87522888183594,563.0291137695312,181.7308349609375,572.9544677734375), (151.87522888183594,571.56494140625), '服事主', BODY, BODY_COLOR),
    ]
    for page_index, rect, origin, text, fontsize, color in fixes:
        patch_word(doc[page_index], fitz.Rect(*rect), origin, text, fontsize, color, songti)
    regions, numbering = upgrade(doc, replace, put)
    changed = CHANGED | set(regions)
    # Preserve the original outline, but expose Romans chapter numbers directly.
    # (Chapters 1-11 only here -- this id_to_number remap is a quirk of how
    # the original baseline's own LaTeX numbered its front matter; the fresh
    # chapter-12-onward render below never had that problem, see
    # build_fresh_pdf.py / build_book.py's mark_unnumbered().)
    toc = doc.get_toc()
    id_to_number = dict(zip(CHAPTER_IDS, range(1,17)))
    for item in toc:
        if item[0] == 1:
            match = re.match(r'^(\d+) (.*)', item[1])
            if match and int(match[1]) in id_to_number:
                item[1] = f'羅馬書第 {id_to_number[int(match[1])]} 章 · {match[2]}'

    # --- 2026-09-24 splice: rebuild chapter 12 onward from current markdown
    # sources and replace the frozen document's tail with it. build_fresh_pdf
    # always rebuilds (never reuses stale output), so this can never drift
    # from the chapter/appendix source files.
    import build_fresh_pdf
    if build_fresh_pdf.main() != 0:
        raise RuntimeError(f'fresh xelatex build failed; see {build_fresh_pdf.LOG}')
    fresh = fitz.open(build_fresh_pdf.OUTPUT_PDF)
    fresh_ch12 = next(
        i for i, page in enumerate(fresh)
        if CHAPTER_12_MARKER in page.get_text() and '羅馬書12:1-21' in page.get_text().replace(' ', '')
    )
    # Splice by trimming and prepending INTO the fresh document, not by
    # inserting both sources into a brand-new empty one: pandoc/hyperref
    # links chapters via named PDF destinations (e.g. "chapter.12"), and
    # PyMuPDF's insert_pdf() silently drops those (renders as 0 links, no
    # error) when the target is a fresh empty document with no destination
    # tree of its own -- confirmed by a direct A/B page-link count, not
    # assumed. Keeping `fresh` as the live document object preserves its own
    # destination tree; only the frozen front is copied in.
    fresh_toc = fresh.get_toc()  # page numbers below are pre-trim, absolute in `fresh`
    fresh.select(list(range(fresh_ch12, len(fresh))))
    fresh.insert_pdf(doc, from_page=0, to_page=FRONT_PAGES-1, start_at=0)
    spliced = fresh
    back_cover(spliced[-1])
    offset = FRONT_PAGES - fresh_ch12  # fresh (pre-trim) 0-indexed page -> spliced 0-indexed page

    fresh_split = next(i for i, e in enumerate(fresh_toc) if '第 12 章' in e[1])
    old_split = next(i for i, e in enumerate(toc) if '第 12 章' in e[1])
    new_tail_toc = []
    for level, title, page in fresh_toc[fresh_split:]:
        # Strip hyperref's bookmarksnumbered auto-prefix ("12 羅馬書第..."):
        # the frozen region's own chapter titles carry no such prefix, so a
        # single bookmark tree shouldn't switch style partway through.
        title = re.sub(r'^\d+ (?=羅馬書第)', '', title)
        new_tail_toc.append([level, title, page + offset])
    spliced.set_toc(
        [[1,'讀經、辨別、回應',6], [1,'經文與引文：怎樣核對',8], [1,'本次校訂與查閱指引',10]]
        + toc[:old_split] + new_tail_toc
    )

    # Chapters 12-16's new absolute positions, read back from the fresh
    # build's own TOC rather than assumed, since the fresh layout's exact
    # page count depends on the current chapter source text.
    chapter_pages = list(CHAPTER_PAGES[:11])
    for n in range(12, 17):
        entry = next(e for e in fresh_toc if f'第 {n} 章' in e[1])
        chapter_pages.append(entry[2] + offset)
    assert len(chapter_pages) == 16

    # Links on the new guide use the exact text rectangles found after rendering.
    for chapter, page_number in enumerate(chapter_pages, 1):
        for rect in spliced[9].search_for(f'第 {chapter} 章'):
            spliced[9].insert_link({'kind':fitz.LINK_GOTO,'from':rect,'page':page_number-1})
    # The appendix Scripture index's "第N章" cells are already live links in
    # the spliced-in region: pandoc/hyperref links every `[第N章](#romans-N)`
    # in the source markdown (build_book.py) to a named PDF destination, so
    # unlike the old frozen baseline (which needed this project's own
    # word-position-matching pass to retrofit navigation onto plain text),
    # nothing further is required here. Counted for the report below.
    index_start = next(e[2] for e in new_tail_toc if e[0] == 1 and '經文與主題索引' in e[1])
    index_stop = next(e[2] for e in new_tail_toc if e[0] == 1 and '參考資料' in e[1])
    index_links = sum(len(spliced[i].get_links()) for i in range(index_start - 1, index_stop - 1))

    meta = spliced.metadata.copy()
    meta['subject'] = 'Romans Deep Study — original edition with editorial corrections'
    from datetime import datetime, timezone
    meta['modDate'] = datetime.now(timezone.utc).strftime('D:%Y%m%d%H%M%SZ')
    spliced.set_metadata(meta)
    spliced.set_language('zh-Hant')
    # Same two-range scheme as the original (roman numerals for pages 1-20,
    # then Arabic from page 21 with no declared end) applies unchanged to a
    # longer or shorter tail -- verified against the actual printed footer
    # numbers on the spliced-in pages, not assumed.
    spliced.set_page_labels(original.get_page_labels())
    spliced.subset_fonts()
    OUTPUT.parent.mkdir(exist_ok=True)
    temporary = OUTPUT.with_name('.romans-consolidated-merge.pdf')
    spliced.save(temporary, garbage=3, deflate=True)
    doc.close()
    spliced.close()  # spliced is fresh (see splice comment above); one object, one close
    # Compare every retained frozen-region page, not merely the number of pages.
    result = fitz.open(temporary)
    preserved = []
    for n in range(FRONT_PAGES):
        assert result[n].rect == original[n].rect
        if n+1 in regions and n+1 not in CHANGED:
            assert unchanged_outside(original[n], result[n], regions[n+1]), f'Unintended change outside approved regions on page {n+1}'
        if n+1 not in changed:
            a = original[n].get_pixmap(matrix=fitz.Matrix(.5,.5), alpha=False).samples
            b = result[n].get_pixmap(matrix=fitz.Matrix(.5,.5), alpha=False).samples
            if a != b:
                raise RuntimeError(f'Unexpected appearance change on original page {n+1}')
            assert result[n].get_text() == original[n].get_text(), f'Unexpected text change on page {n+1}'
            preserved.append(n+1)
    assert len(preserved) == FRONT_PAGES-len(changed)
    for page in result:
        for link in page.get_links():
            if link['kind'] == fitz.LINK_GOTO:
                assert 0 <= link['page'] < len(result), (page.number, link)
    front_text = result[0].get_text()
    assert '因信得生' in front_text and '羅馬書研讀' in front_text
    assert 'Edition 1.1' in front_text and 'NASB 1995' in front_text and '2026-09-20' in front_text
    assert '�' not in front_text
    back_text = result[-1].get_text()
    assert '因信得生' in back_text and '羅馬書研讀' in back_text
    assert '�' not in back_text
    # Verify frozen-region links still resolve, including the old printed contents.
    for n in range(FRONT_PAGES):
        before = [l for l in original[n].get_links() if l['kind']==fitz.LINK_GOTO]
        after = [l for l in result[n].get_links() if l['kind']==fitz.LINK_GOTO]
        for link in before:
            if link['page'] >= FRONT_PAGES:
                continue  # target moved with the splice; page-10/index links above already point correctly
            assert any(l['page']==link['page'] and l['from']==link['from'] for l in after), (n+1,link)
    report = {'baseline_sha256': EXPECTED_HASH, 'pages':len(result), 'front_pages':FRONT_PAGES, 'unchanged_pages':len(preserved), 'chapter_pages':chapter_pages, 'added_index_links':index_links, 'guide_links':len(result[9].get_links()), 'bookmarks':len(result.get_toc()), 'source_layout':'7 x 10 inches', 'cover_metadata':'Edition 1.1 · CUV · NASB 1995 · 2026-09-20', 'result_sha256':hashlib.sha256(temporary.read_bytes()).hexdigest()}
    report.update(corrected_pages=sorted(changed), numbering_repairs=numbering,
                  region_checked_pages=len(set(regions)-CHANGED),
                  approved_regions={str(n):[list(r) for r in rs] for n,rs in regions.items()})
    result.close()
    original.close()
    temporary.replace(OUTPUT)
    (ROOT/'sources/audits/baseline-merge.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('approved_regions','corrected_pages')},indent=2))

if __name__ == '__main__':
    main()

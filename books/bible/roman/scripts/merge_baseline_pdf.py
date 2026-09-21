#!/usr/bin/env python3
"""Revise the user-designated PDF in place, never reflow its 348-page body.

The immutable input is archived before cleanup. Editorial and numbering
corrections occupy explicit rectangles; untouched pages and pixels outside
new repair regions must compare against the original.
"""
from pathlib import Path
import os
import hashlib
import json
import re
import fitz
from cover_design import covers
from editorial_upgrade import upgrade, unchanged_outside

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'sources/archive/romans-original-baseline.pdf'
OUTPUT = Path(os.environ.get('ROMANS_CANONICAL_PDF', ROOT.parents[2] / 'output/romans-consolidated.pdf'))
EXPECTED_HASH = 'abed9a6294db5db9a9da7fc96a5e482d36013103ce74783048434339a515524b'
CHAPTER_PAGES = [52,68,83,100,115,132,147,162,181,198,212,229,244,261,277,294]
CHAPTER_IDS = [8,9,10,12,13,15,16,17,19,20,21,23,24,25,26,27]
CHANGED = {1,9,10,27,30,48,69,148,245,246,263,279,295,296,313,333,346,348}
CSS = '''
body {font-family:serif; font-size:10.3pt; line-height:1.36; color:#172238; margin:0;}
p {margin:0 0 9pt 0;} h1 {font-family:serif; font-size:19pt; font-weight:normal; color:#223c64; margin:0 0 13pt 0;}
h2 {font-family:serif; font-size:12pt; color:#8a641c; font-weight:normal; margin:12pt 0 6pt 0;}
table {border-collapse:collapse; width:100%;} td,th {padding:3pt 5pt; border-bottom:0.4pt solid #d8d4ca; font-weight:normal; text-align:left;}
.small {font-size:9pt;} .rule {border-top:0.7pt solid #8a641c; padding-top:10pt;}
'''

def put(page, rect, html, size=None):
    css = CSS + (f'body {{font-size:{size}pt;}}' if size else '')
    spare, scale = page.insert_htmlbox(rect, html, css=css, scale_low=1)
    if spare < 0 or scale < 1:
        raise RuntimeError(f'Text does not fit on source page {page.number+1}: {rect}')

def replace(page, rect, html, size=10.3):
    page.add_redact_annot(rect, fill=(1,1,1))
    page.apply_redactions(images=0, graphics=0)
    put(page, rect, html, size)

# Single-character word-choice fixes (below) are mid-sentence and must sit
# flush against untouched neighboring glyphs on the same line, so the
# generic `insert_htmlbox`/CSS "serif" fallback (used for the whole-paragraph
# rewrites above) is unusable here: its CJK metrics run ~20% wider per
# character than this book's actual body font, and font-family in CSS does
# not resolve to a different font in this MuPDF build regardless of the
# name given, so there is no way to ask insert_htmlbox for the real font.
# Instead this draws the replacement with insert_text() using the exact
# same font, size, color and baseline origin as the original glyphs
# (extracted via get_text('rawdict') at each target), which is pixel-exact
# rather than approximate. The font is read live from the local macOS
# install (Songti.ttc face 6, "Songti SC"/"Regular") each run — same
# dependency already required to view or print this book's Chinese pages
# (see eat-bible SKILL.md, "Fonts are a hard macOS dependency") — and is
# never written to disk or committed; only fontTools' in-memory extraction
# is a new requirement (`pip install fonttools`).
def _load_songti_regular():
    from fontTools.ttLib import TTCollection
    import io
    path = '/System/Library/Fonts/Supplemental/Songti.ttc'
    if not Path(path).is_file():
        raise SystemExit('Songti.ttc not found; the Scripture-wording patch requires macOS with Songti SC installed')
    tc = TTCollection(path)
    for face in tc.fonts:
        if face['name'].getDebugName(1) == 'Songti SC' and face['name'].getDebugName(2) == 'Regular':
            buf = io.BytesIO()
            face.save(buf)
            return buf.getvalue()
    raise SystemExit('Songti SC Regular face not found in Songti.ttc')

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
    covers(doc)
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
      <p>印刷第 313 頁：舊版「108 條引句零漂移、零查無」記錄尚無可重現的來源檔與報告；本版不把它列作完成驗證的保證。</p>
      <p class="small rule">引文、譯文、神學審查與使用許可仍須各自核定。電子導覽和排版檢查不代表這些審查已完成。</p>
    ''')
    replacement = '編者比較：加拉太書與羅馬書都論及信心、律法與稱義，但論述方式與牧養處境各有重點。因未取得摩根原話的確切書目與頁碼，本版不沿用具名引句，也不以此核定兩封信的直接寫作次序。'
    replace(doc[26], fitz.Rect(61,301,457,354), '<p>'+replacement+'</p>', 9.5)
    replace(doc[29], fitz.Rect(45,417,448,508), '<p>羅馬書與加拉太書可互相參照。以下為編者的主題比較：</p><p>'+replacement+'</p>', 10)
    # Preserve the cross-page sentence: this paragraph still ends with 羅馬,
    # followed by 書 on the next page, as in the original text.
    replace(doc[47], fitz.Rect(45,595,448,669), '<p>編者比較：加拉太書與羅馬書都論及信心、律法與稱義；本版未取得支持原摩根引句的確切出處，故不以它斷定兩封信的直接寫作次序。以下仍從主題作比較：加拉太書與羅馬書像兩支軍隊從不同方向攻打同一座城：加拉太書駁斥外邦信徒被說服要靠割禮與律法「補足」因信稱義的軟弱，羅馬</p>', 10.1)
    # Scripture-wording corrections (2026-09-21 校對神 pass): verse-by-verse
    # checked against cnbible.com's labeled "繁體中文和合本 (CUV Traditional)"
    # column. rect/origin/fontsize/color are all read from the original via
    # get_text('rawdict') at each location; see patch_word() above.
    songti = _load_songti_regular()
    BODY, BODY_COLOR = 9.925399780273438, (50/255, 50/255, 50/255)
    REFLECT, REFLECT_COLOR = 10.868300437927246, (0, 0, 0)
    fixes = [
        (68, (182.5965576171875,267.96014404296875,222.41726684570312,277.88555908203125), (182.5965576171875,276.4960021972656), '積蓄忿怒', BODY, BODY_COLOR),
        (68, (309.82110595703125,319.5091552734375,350.21746826171875,329.4345703125), (309.82110595703125,328.0450134277344), '就以忿怒', BODY, BODY_COLOR),
        (147, (151.87522888183594,563.0291137695312,181.7308349609375,572.9544677734375), (151.87522888183594,571.56494140625), '服事主', BODY, BODY_COLOR),
        (244, (236.0268096923828,572.9581909179688,285.76300048828125,582.883544921875), (236.0268096923828,581.4940185546875), '是與你有益', BODY, BODY_COLOR),
        (244, (192.44253540039062,586.109130859375,232.2235107421875,596.0344848632812), (192.44253540039062,594.6449584960938), '是伸冤的', BODY, BODY_COLOR),
        (245, (148.95230102539062,82.72415161132812,198.7281951904297,92.64955139160156), (148.95230102539062,91.25999450683594), '不加害與人', BODY, BODY_COLOR),
        (262, (395.3214416503906,306.06414794921875,435.0726318359375,315.98956298828125), (395.3214416503906,314.6000061035156), '服事基督', BODY, BODY_COLOR),
        (278, (320.0308837890625,56.42315673828125,350.263671875,66.34855651855469), (320.0308837890625,64.95899963378906), '歸與神', BODY, BODY_COLOR),
        (278, (358.4367370605469,185.07215881347656,398.18792724609375,194.99755859375), (358.4367370605469,193.60800170898438), '彼此勸戒', BODY, BODY_COLOR),
        (278, (364.6679992675781,379.4751281738281,414.731689453125,389.4005432128906), (364.6679992675781,388.010986328125), '有分，就當', BODY, BODY_COLOR),
        (294, (107.37918090820312,457.0511169433594,178.1373748779297,466.9765319824219), (107.37918090820312,465.58697509765625), '舉薦我們的姊妹', BODY, BODY_COLOR),
        (294, (232.07342529296875,644.313232421875,302.96063232421875,654.2385864257812), (232.07342529296875,652.8490600585938), '尼利亞和他姊妹', BODY, BODY_COLOR),
        (295, (140.14109802246094,69.57415771484375,231.305908203125,79.49955749511719), (140.14109802246094,78.11000061035156), '不服事我們的主基督', BODY, BODY_COLOR),
        (295, (241.49929809570312,69.57415771484375,292.04937744140625,79.49955749511719), (241.49929809570312,78.11000061035156), '只服事自己', BODY, BODY_COLOR),
        (295, (188.7980499267578,245.29214477539062,268.46923828125,255.21754455566406), (188.7980499267578,253.82798767089844), '歸與獨一全智的神', BODY, BODY_COLOR),
        (312, (79.41268157958984,110.86825561523438,166.64166259765625,121.73655700683594), (79.41268157958984,120.21499633789062), '歸與獨一全智的神', REFLECT, REFLECT_COLOR),
        (345, (279.7076416015625,95.96426391601562,368.7190246582031,106.83256530761719), (279.7076416015625,105.31100463867188), '歸與獨一全智的神', REFLECT, REFLECT_COLOR),
        (345, (188.60958862304688,192.70025634765625,275.83856201171875,203.5685577392578), (188.60958862304688,202.0469970703125), '歸與獨一全智的神', REFLECT, REFLECT_COLOR),
    ]
    for page_index, rect, origin, text, fontsize, color in fixes:
        patch_word(doc[page_index], fitz.Rect(*rect), origin, text, fontsize, color, songti)
    replace(doc[332], fitz.Rect(56,273,459,391), '''<p>查核範圍說明：舊版記錄曾稱 2026 年 9 月 2 日逐條核對教父與改教家資料，並報稱 108 條英文引句「零漂移、零查無」。本版尚未取得能重現該結果的逐條來源存檔與比對報告，因此撤回把上述數字視為完成驗證的保證。</p><p>下列作者、文本與來源表仍供讀者追溯。原有日期及查核分類屬編輯歷程記錄；引文逐字相符、譯文準確與使用許可仍須分別核定。凡未附可重現證據者，均列入待覆核。</p>''',10.2)
    regions, numbering = upgrade(doc, replace, put)
    changed = CHANGED | set(regions)
    # Preserve the original outline, but expose Romans chapter numbers directly.
    toc = doc.get_toc()
    id_to_number = dict(zip(CHAPTER_IDS, range(1,17)))
    for item in toc:
        if item[0] == 1:
            match = re.match(r'^(\d+) (.*)', item[1])
            if match and int(match[1]) in id_to_number:
                item[1] = f'羅馬書第 {id_to_number[int(match[1])]} 章 · {match[2]}'
    doc.set_toc([[1,'讀經、辨別、回應',6], [1,'經文與引文：怎樣核對',8], [1,'本次校訂與查閱指引',10]] + toc)
    # Links on the new guide use the exact text rectangles found after rendering.
    for chapter, page_number in enumerate(CHAPTER_PAGES, 1):
        for rect in doc[9].search_for(f'第 {chapter} 章'):
            doc[9].insert_link({'kind':fitz.LINK_GOTO,'from':rect,'page':page_number-1})
    index_links = 0
    for index in range(314,327):
        page = doc[index]
        for x0,y0,x1,y1,word,*_ in page.get_text('words'):
            if re.fullmatch(r'0[1-9]|1[0-6]', word) and 210 < x0 < 250 and y0 > 45:
                page.insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(x0,y0,x1,y1),'page':CHAPTER_PAGES[int(word)-1]-1})
                index_links += 1
    meta = doc.metadata.copy()
    meta['subject'] = 'Romans Deep Study — original edition with editorial corrections'
    from datetime import datetime, timezone
    meta['modDate'] = datetime.now(timezone.utc).strftime('D:%Y%m%d%H%M%SZ')
    doc.set_metadata(meta)
    doc.set_language('zh-Hant')
    doc.set_page_labels(original.get_page_labels())
    doc.subset_fonts()
    OUTPUT.parent.mkdir(exist_ok=True)
    temporary = OUTPUT.with_name('.romans-consolidated-merge.pdf')
    doc.save(temporary, garbage=3, deflate=True)
    doc.close()
    # Compare every retained source page, not merely the number of pages.
    result = fitz.open(temporary)
    preserved = []
    for n in range(348):
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
    assert len(result) == 348 and len(preserved) == 348-len(changed)
    assert result.get_page_labels() == original.get_page_labels()
    for page in result:
        for link in page.get_links():
            if link['kind'] == fitz.LINK_GOTO:
                assert 0 <= link['page'] < len(result), (page.number, link)
    for number in (0,347):
        cover_text = result[number].get_text()
        assert '因信得生' in cover_text and '羅馬書研讀' in cover_text
        if number == 0:
            assert 'Edition 1.1' in cover_text and 'NASB 1995' in cover_text and '2026-09-20' in cover_text
        assert '\ufffd' not in cover_text
    # Verify original links still resolve, including the old printed contents.
    for n in range(348):
        before = [l for l in original[n].get_links() if l['kind']==fitz.LINK_GOTO]
        after = [l for l in result[n].get_links() if l['kind']==fitz.LINK_GOTO]
        for link in before:
            assert any(l['page']==link['page'] and l['from']==link['from'] for l in after), (n+1,link)
    report = {'baseline_sha256': EXPECTED_HASH, 'pages':len(result), 'unchanged_pages':len(preserved), 'corrected_pages':sorted(CHANGED), 'added_index_links':index_links, 'guide_links':len(result[9].get_links()), 'bookmarks':len(result.get_toc()), 'source_layout':'7 x 10 inches', 'cover_metadata':'Edition 1.1 · CUV · NASB 1995 · 2026-09-20', 'result_sha256':hashlib.sha256(temporary.read_bytes()).hexdigest()}
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

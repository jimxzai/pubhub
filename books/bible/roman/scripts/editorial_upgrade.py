"""Measured editorial repairs; no global re-typesetting of the source PDF."""
import re
import os
from pathlib import Path
import fitz

CHAPTER_PAGES = [52,68,83,100,115,132,147,162,181,198,212,229,244,261,277,294]
CHAPTER_IDS = [8,9,10,12,13,15,16,17,19,20,21,23,24,25,26,27]

def upgrade(doc, replace, put):
    regions={}
    latin_path=Path(os.environ.get('ROMANS_LABEL_FONT','/System/Library/Fonts/Supplemental/Times New Roman.ttf'))
    if not latin_path.is_file():
        raise RuntimeError('Times New Roman.ttf is required for embedded numbering labels')
    latin_buffer=latin_path.read_bytes()
    def repair(number,rect,content,size=10.3):
        rect=fitz.Rect(rect)
        replace(doc[number-1],rect,content,size)
        regions.setdefault(number,[]).append(rect)

    repair(152,(45,327,448,535),'''
      <p>nomos 在本章須按上下文分辨，不能只憑冠詞有無判定意思。7:21 的 ton nomon 有冠詞，卻仍可譯作「規律」；冠詞不是區分摩西律法與運作原則的開關。</p>
      <p>1. 摩西的律法：7:1-14 多處討論律法的約束、誡命及其良善。<br>
      2. 支配人的規律或力量：7:21-23 談及行善的意願、肢體中爭戰的律與罪的律；須連同修飾語理解。<br>
      3. 神的律：7:22-25 指向人所喜悅、願意順服的神的旨意。</p>
      <p>這些用法彼此關聯，並非三個互不相干的定義。保羅的問題不是律法邪惡，而是罪如何挾制人；7:25 至 8:4 把答案引向基督與聖靈。</p>
      <p class="small">原文核對：羅馬書 7:21，Nestle 1904／Westcott–Hort 文本均見 ton nomon。釋義仍須按整段論證判斷。</p>''',10.2)
    # Remove unsupported prevalence claim without flattening the debate.
    repair(154,(320,77,447,136),'奧古斯丁晚期立場、路德、加爾文及部分當代福音派釋經家',10.3)
    p=doc[153]
    block=next(b for b in p.get_text('blocks') if '兩種讀法都同意' in b[4])
    repair(154,(45,block[1]-.8,448,block[3]+.8),'''
      <p>7:25 的感謝把盼望指向耶穌基督，但兩種讀法對25節下半的定位不同。信徒爭戰的讀法，把它視為得救確據與持續爭戰並存；律法之下者的讀法，則把它視為8:1-4展開釋放之前的總結。</p>
      <p>也有人把「我」理解為代表性發言。閱讀時應比較6:6、7:14、7:22與8:2-4，不因第一人稱或現在式便斷定發言者的身分，也不把其中一種解釋寫成各方共同結論。</p>''',10.1)
    for number in (244,259):
        page=doc[number-1]
        block=next(b for b in page.get_text('blocks') if '沒有直接提耶穌' in b[4])
        original=''.join(block[4].splitlines())
        revised=original.replace('保羅在這一章沒有直接提耶穌的名字，然而',
                                  '保羅在13:14明確提到主耶穌基督，')
        repair(number,(block[0]-.5,block[1]-.5,block[2]+.5,block[3]+1),'<p>'+revised+'</p>',10)
    repair(331,(55,54,459,143),'''
      <p>歷史統計待覆核：所報46段，與「維持19、修正14、查無3」合計36段不符；「其中10段」是子集，不能重複加總。本版不把此數字列為完整核驗保證。</p>
      <p>以下保留來源線索；逐字相符、撮述公允、譯文準確與使用許可仍須分別查核。</p>''',10)
    # Existing blank versos become useful front matter without changing pagination.
    assert not doc[5].get_text().strip() and not doc[7].get_text().strip()
    for number in (6,8): regions[number]=[doc[number-1].rect]
    put(doc[5],fitz.Rect(47,54,457,673),'''
      <h1>讀經、辨別、回應</h1>
      <p>本書是研讀工具，不取代聖經本身。先細讀經文，再讀注疏；把經文所說、作者推論與個人應用分開記錄。</p>
      <h2>每次研讀的四步</h2>
      <table><tr><td>觀察</td><td>誰在說話？向誰說？圈出「所以」「但如今」「因為」等轉折。</td></tr>
      <tr><td>理解</td><td>本段如何承接上一段？它在全信的論證中回答甚麼問題？</td></tr>
      <tr><td>比較</td><td>先比經文，再比注疏。記下不同解釋各自的依據與未解難題。</td></tr>
      <tr><td>回應</td><td>用一句話寫下領受；選一項可實踐的回應，下次研讀時回顧。</td></tr></table>
      <h2>跟隨全信的推進</h2>
      <p>1–3章：普世的需要，與神在基督裏顯明的義。<br>
      4–5章：亞伯拉罕的信、和好與盼望。<br>
      6–8章：與基督聯合、律法與罪、聖靈中的生命。<br>
      9–11章：以色列、神的信實與人的回應。<br>
      12–16章：憐憫所生的敬拜、彼此接納與共同使命。</p>
      <p class="small">以上是讀者論證路線，不另立印刷分卷。目錄的 R1–R16 與正文 Romans 1–16 指聖經章號；卷首及附錄仍沿用原編排序號。印刷頁碼維持不變。</p>
      <h2>讀爭議段落時</h2>
      <p>7:14–25：比較「我」的各種讀法，避免只靠時態決定。<br>
      9–11章：同時留意保羅的哀痛、神的憐憫與不可誇口的勸告。<br>
      13:1–7：連同13:10的愛與徒5:29閱讀，不把順服當作縱容傷害。<br>
      14–15章：分辨良心差異與實際傷害；接納不是放棄辨別。</p>
      <p class="small rule">小組帶領：先讓每人說出經文觀察，再比較解釋；不以贊同某位注疏家代替論證，也不以不同意見羞辱他人。</p>''',10.3)
    put(doc[7],fitz.Rect(47,54,457,673),'''
      <h1>經文與引文：怎樣核對</h1>
      <h2>兩種語言，不混淆版本</h2>
      <p>正文中文標示為和合本，英文為 NASB 1995。不同和合本電子文本可有字形、譯名及括註差異；本版保留指定原版，沒有把它靜默改成修訂版，也不宣稱與某個現代電子排印逐字相同。</p>
      <p>本次以 FHL 的 unv 繁體文本及 Bible Hub 的 NASB 1995 章頁作比較線索。差異須分清是版本用字、省略括註、排印錯誤，還是擷取造成；找到差異不等於已判定哪一方有錯。</p>
      <h2>分清三種聲音</h2>
      <table><tr><td>原文引句</td><td>核對作者、著作、譯者、講道編號或頁碼；省略符號前後也須連同上下文閱讀。</td></tr>
      <tr><td>編者中譯</td><td>是英文引句的譯文，不是作者寫成的中文；關鍵詞仍須回查原文。</td></tr>
      <tr><td>綜述／應用</td><td>屬編者的理解與應用，不應去掉說明、加上引號，再當作作者逐字言論轉引。</td></tr></table>
      <h2>可追溯，不等於已核准</h2>
      <p>引用出處、文字相符、上下文公允與使用許可，是四項不同判斷。本版不以歷史「已核實」字樣代替現有證據；仍待覆核的項目保留為待辦。</p>
      <p>全书資料核對使用實際 PDF 擷取文字與封存參考檔；忽略標點及排版差異的相符，只能稱「正規化文字相符」，不可稱逐字、逐標點核實。</p>
      <h2>查閱與勘誤</h2>
      <p>用電子書籤進入羅馬書第1–16章；按原印刷頁碼引用。回報問題時請提供章節、印刷頁碼、原句、所用版本及可查閱來源。</p>
      <p class="small rule">原始來源、修訂區域與核對結果均保留在本書專案的 sources 目錄。權利、神學、雙語校對、無障礙及紙樣審核尚未因此完成。</p>'''.replace('全书','全書'),10.2)
    # Repair chapter numbering in printed labels and running heads, not just bookmarks.
    numbering=0
    for chapter,(start,old) in enumerate(zip(CHAPTER_PAGES,CHAPTER_IDS),1):
        stop=CHAPTER_PAGES[chapter] if chapter<16 else 310
        for n in range(start-1,stop-1):
            page=doc[n]
            for rect in page.search_for(f'Chapter {old}'):
                if rect.y1>110: continue
                label=f'Romans {chapter}'
                # Native Latin font keeps the compact running-head baseline.
                page.add_redact_annot(rect,fill=(1,1,1))
                page.apply_redactions(images=0,graphics=0)
                size=10 if rect.y0<43 else 11
                page.insert_font(fontname='RomansLabel',fontbuffer=latin_buffer)
                page.insert_text((rect.x0,rect.y1-2),label,fontsize=size,fontname='RomansLabel',color=(.12,.18,.27))
                regions.setdefault(n+1,[]).append(rect+(-1,-1,1,1))
                numbering+=1
    toc_repairs=0
    mapping=dict(zip(CHAPTER_IDS,range(1,17)))
    for n in range(10,20):
        page=doc[n]
        links=page.get_links()
        for x0,y0,x1,y1,word,*_ in page.get_text('words'):
            if not (word.isdigit() and int(word) in mapping and x0<60 and y0>43): continue
            rect=fitz.Rect(x0-.4,y0-.4,x1+.4,y1+.4)
            page.add_redact_annot(rect,fill=(1,1,1))
            page.apply_redactions(images=0,graphics=0)
            page.insert_font(fontname='RomansLabel',fontbuffer=latin_buffer)
            page.insert_text((x0,y1-2),f'R{mapping[int(word)]}',fontname='RomansLabel',fontsize=8,color=(.12,.18,.27))
            regions.setdefault(n+1,[]).append(fitz.Rect(x0-.4,y0-.4,x0+15,y1+.4))
            toc_repairs+=1
        current=page.get_links()
        for link in links:
            if link['kind']==fitz.LINK_GOTO and not any(l['kind']==link['kind'] and l['from']==link['from'] and l['page']==link['page'] for l in current):
                page.insert_link({k:link[k] for k in ('kind','from','page','to','zoom') if k in link})
    assert toc_repairs==16, f'Unexpected contents repair count: {toc_repairs}'
    return regions,numbering

def unchanged_outside(a,b,regions):
    """Compare all rendered pixels outside explicitly approved edit rectangles."""
    matrix=fitz.Matrix(.75,.75)
    first=a.get_pixmap(matrix=matrix,alpha=False)
    second=b.get_pixmap(matrix=matrix,alpha=False)
    for rect in regions:
        mask=(fitz.Rect(rect)*matrix+(-2,-2,2,2)).irect
        first.set_rect(mask,(255,255,255))
        second.set_rect(mask,(255,255,255))
    return first.samples==second.samples

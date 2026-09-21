"""Vector series packaging inspired by John's design, with Romans' identity."""
import math
import fitz

GOLD = (216/255, 183/255, 109/255)

def text(page, top, bottom, html, size=12, color='#f9f6ec', align='center'):
    css = f'''body {{font-family:serif; font-size:{size}pt; line-height:1.45;
        color:{color}; margin:0; text-align:{align};}}
        p {{margin:0 0 9pt;}} i {{color:#d8b76d;}}'''
    spare, scale = page.insert_htmlbox(fitz.Rect(62,top,442,bottom), html,
                                      css=css, scale_low=1)
    if spare < 0 or scale != 1:
        raise ValueError(f'Cover text overflow at {top}')

def ground(page):
    # Remove old content, not merely hide it from sight or text extraction.
    page.add_redact_annot(page.rect, fill=False)
    page.apply_redactions(images=2, graphics=2)
    for y in range(0,720,3):
        t = y/720
        color = tuple((a+(b-a)*t)/255 for a,b in zip((7,18,32),(20,47,65)))
        page.draw_rect(fitz.Rect(0,y,504,y+3), color=None, fill=color)
    for inset,width in ((23,0.9),(29,0.3)):
        page.draw_rect(fitz.Rect(inset,inset,504-inset,720-inset), color=GOLD,width=width)
    for x in (23,481):
        for y in (23,697):
            page.draw_circle((x,y),1.8,color=None,fill=GOLD)

def rule(page, y, left=98, right=406):
    page.draw_line((left,y),(right,y),color=GOLD,width=.5)

def covers(doc):
    front, back = doc[0], doc[-1]
    ground(front)
    text(front,62,103,'Three Books Deep Reading · Romans<br>三書精讀 · 羅馬書深度研讀',10,'#bfced3')
    rule(front,119,175,329)
    text(front,139,169,'從福音所顯的義，走向信心的順服',11,'#bfced3')
    for radius in (24,28):
        front.draw_circle((252,209),radius,color=GOLD,width=.5)
    for angle in range(0,360,15):
        a = math.radians(angle)
        front.draw_line((252+31*math.cos(a),209+31*math.sin(a)),
                        (252+35*math.cos(a),209+35*math.sin(a)),color=GOLD,width=.4)
    text(front,193,226,'義',20)
    text(front,266,325,'因信得生',38)
    text(front,322,354,'<i>Justified to Live by Faith</i>',19)
    text(front,371,413,'羅馬書研讀',24)
    text(front,415,441,'A Study of the Epistle to the Romans',12,'#bfced3')
    text(front,463,491,'神的義 · The Righteousness of God',13,'#d8b76d')
    rule(front,511)
    text(front,529,577,'義人必因信得生。<br><span style="font-size:9pt;color:#bfced3">羅馬書 1:17 · 和合本</span>',15)
    rule(front,583)
    text(front,604,633,'因信稱義　與主同活　獻上活祭',11,'#d8b76d')
    text(front,648,688,'PubHub · 三書精讀出版系統<br><span style="font-size:8.2pt;color:#bfced3">研讀指南 · Edition 1.1</span><br><span style="font-size:8.2pt;color:#bfced3">CUV / NASB 1995 · 2026-09-20</span>',8.8)

    ground(back)
    text(back,64,91,'神的義 · The Righteousness of God',15,'#d8b76d')
    text(back,111,152,'從因信稱義，到獻上自己',22)
    text(back,159,189,'From justification by faith to a life offered to God',11,'#bfced3')
    rule(back,204)
    text(back,227,344,'<p>逐章研讀羅馬書十六章，沿着定罪、稱義、成聖、揀選與活祭的次序，看見福音如何塑造生命與群體。</p><p>本書結合經文研讀、歷代注疏、原文觀察與生命應用，並保留完整的全書領受總綱、經文索引及參考資料。</p>',12,align='left')
    text(back,351,434,'A chapter-by-chapter study of Romans: from humanity’s need and justification by faith to life in the Spirit, God’s faithfulness to Israel, and worship expressed in daily life. Includes commentary, reflection, Scripture indexes, and references.',11,'#bfced3',align='left')
    rule(back,449)
    text(back,468,536,'<span style="color:#d8b76d">讀經 · 理解 · 回應</span><br>細讀經文，分辨注疏與編者觀察；<br>帶着問題默想，以禱告與行動回應。',12)
    text(back,553,625,'老弟兄部分為查經方法論的應用，非羅馬書原始課堂逐字稿。<br>研讀指南與經文引用，不宣稱完整逐節中英平行排印。<br>引用來源與使用許可仍待出版核定。',9,'#bfced3')
    rule(back,640)
    text(back,655,685,'因信得生 · 羅馬書研讀<br>PubHub · 三書精讀出版系統',10)

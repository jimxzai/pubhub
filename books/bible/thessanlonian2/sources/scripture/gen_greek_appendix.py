#!/usr/bin/env python3
"""Generate 97-appendix-greek-vocabulary.md from SBLGNT (MorphGNT) counts.

Every number in the appendix is computed here; nothing is typed by hand
except the Chinese glosses. Re-run after any change:
    python3 sources/scripture/gen_greek_appendix.py [--sblgnt DIR]
DIR defaults to sources/scripture/sblgnt-nt (MorphGNT files 61-Mt … 87-Re).
"""
import argparse, collections, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK_DIR = os.path.dirname(os.path.dirname(HERE))
ABBR = {61: '太', 62: '可', 63: '路', 64: '約', 65: '徒', 66: '羅', 67: '林前', 68: '林後',
        69: '加', 70: '弗', 71: '腓', 72: '西', 73: '帖前', 74: '帖後', 75: '提前', 76: '提後',
        77: '多', 78: '門', 79: '來', 80: '雅', 81: '彼前', 82: '彼後', 83: '約壹', 84: '約貳',
        85: '約參', 86: '猶', 87: '啟'}

# Theme words: (lemma, 和合本 rendering, why it matters)
THEMES = [
    ('κύριος', '主', '全書最常見的實詞；這是一封以主為中心的信'),
    ('θεός', '神', ''),
    ('πᾶς', '一切、眾人', '「一切逼迫患難」「隨時隨事」「你們眾人」'),
    ('πίστις', '信心', '信心增長（1:3）對照「人不都是有信心」（3:2）'),
    ('πιστεύω', '信', '「一切信的人」（1:10）對照「信從虛謊」（2:11）'),
    ('ἀλήθεια', '真理、真道', '不領受愛真理的心（2:10）；信真道（2:13）'),
    ('ἀποκαλύπτω', '顯露', '全用於那不法的人'),
    ('ἀποκάλυψις', '顯現', '用於主耶穌'),
    ('παρουσία', '降臨、來', '主（2:1, 8）與那不法的人（2:9）'),
    ('ἐνέργεια', '運動', '撒但的運動（2:9）；神差遣迷惑的運行（2:11）'),
    ('ἐπιστολή', '書信', '冒名的信、寫的信、這信、親筆'),
    ('παραγγέλλω', '吩咐', '全在第三章'),
    ('ἐργάζομαι', '做工', '全在第三章'),
    ('ἀτάκτως', '不按規矩', '失序；見下表'),
    ('εἰρήνη', '平安', '首（1:2）尾（3:16）'),
    ('χάρις', '恩', '首（1:2）尾（3:18）'),
]
# Hapax glosses (CUV wording) — the list itself is computed, not typed
GLOSS = {
    'ὑπεραυξάνω': '格外增長', 'ἐγκαυχάομαι': '誇口', 'ἔνδειγμα': '明證',
    'τίνω': '受（刑罰）', 'ἐνδοξάζομαι': '得榮耀', 'ἀτάκτως': '不按規矩',
    'ἀτακτέω': '不按規矩而行', 'περιεργάζομαι': '專管閒事', 'καλοποιέω': '行善',
    'σημειόομαι': '記下',
}
# Spine words: NT-wide distribution
SPINE = [
    ('ἐνέργεια', '運動、運行的能力'),
    ('ἀποστασία', '離道反教'),
    ('ἐπισυναγωγή', '聚集'),
    ('ἐπιφάνεια', '（降臨的）榮光、顯現'),
    ('ἀπαρχή', '初熟的果子（帖後2:13 異文，見第5章）'),
    ('ἄτακτος', '不守規矩的'),
    ('τάξις', '次序'),
    ('σαλεύω', '動心、搖動'),
    ('κατέχω', '攔阻；持守'),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sblgnt', default=os.path.join(HERE, 'sblgnt-nt'))
    a = ap.parse_args()
    nt = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(a.sblgnt, '*.txt'))):
        for line in open(f, encoding='utf-8'):
            p = line.split()
            b = int(p[0][:2]) + 60
            nt[p[6]].append((b, int(p[0][2:4]), int(p[0][4:6])))
    th = {w: [r for r in refs if r[0] == 74] for w, refs in nt.items()}
    total_words = sum(len(v) for v in th.values())
    assert total_words > 800, 'SBLGNT files not found'

    def where(refs, book=True):
        return '、'.join(f'{ABBR[b] if book else ""}{c}:{v}' for b, c, v in refs)

    out = ['---', 'title: 帖撒羅尼迦後書研讀', 'subtitle: 2 Thessalonians Deep Study',
           'author: PubHub 三書精讀系統', 'date: 2026年10月', 'publisher: 三書精讀出版系統', '---', '',
           '# 附錄：希臘文字彙 (Appendix: Greek Vocabulary) {.unnumbered}', '',
           '> 本附錄由腳本 `sources/scripture/gen_greek_appendix.py` 依 SBLGNT 希臘文新約（MorphGNT 詞元標註）'
           '自動產生，書中凡說「出現 N 次」「全新約僅見於此」者，皆以此為據。'
           f'帖撒羅尼迦後書在此底本共 {total_words} 字。詞元計數不分詞形（如 κύριος 含 κυρίου、κύριε 等）；'
           '不同底本的個別異文可能使計數略有出入。', '',
           '## 一、全書主題詞', '',
           '| 詞元 | 和合本 | 本書次數 | 出處 | 份量 |',
           '|----------------------|--------------|--------|------------------------------------------|----------------------------------|']
    for lem, zh, note in THEMES:
        refs = th.get(lem, [])
        out.append(f'| `{{\\greekfont {lem}}}`{{=latex}} | {zh} | {len(refs)} | {where(refs, False)} | {note} |')
    hapax = sorted((w for w, refs in th.items() if refs and len(nt[w]) == len(refs)),
                   key=lambda w: th[w][0])
    out += ['', '## 二、全新約僅見於本書的字', '',
            f'以下 {len(hapax)} 個詞元在全新約只出現在帖撒羅尼迦後書。其中一半落在第三章論「不按規矩而行」的段落，'
            '保羅為這個失序的光景用了別處沒有用過的字。', '',
            '| 詞元 | 和合本 | 出處 |',
            '|----------------------|--------------------|----------------------|']
    for w in hapax:
        out.append(f'| `{{\\greekfont {w}}}`{{=latex}} | {GLOSS.get(w, "")} | {where(th[w], False)} |')
    out += ['', '## 三、骨幹相關字在全新約的分佈', '',
            '| 詞元 | 意義 | 全新約次數 | 出處 |',
            '|----------------------|----------------------------|--------|--------------------------------------------------|']
    for w, zh in SPINE:
        out.append(f'| `{{\\greekfont {w}}}`{{=latex}} | {zh} | {len(nt[w])} | {where(nt[w])} |')
    out += ['', '**資料來源**：SBLGNT（Society of Biblical Literature Greek New Testament，Michael W. Holmes 編，2010）；'
            '詞元與詞性標註取自 MorphGNT 專案（github.com/morphgnt/sblgnt）。和合本對譯取自各節經文本身。', '']
    path = os.path.join(BOOK_DIR, '97-appendix-greek-vocabulary.md')
    open(path, 'w', encoding='utf-8').write('\n'.join(out))
    print(f'wrote {path}: {len(hapax)} hapax, {total_words} words')

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Fill the HYMN-PENDING markers in chapters 01-10.

For each chapter NN: builds the 配詩 block (English stanzas copied verbatim from
sources/hymns/NN-*.txt, plus the Chinese rendering below) and replaces the first
<!-- HYMN-PENDING --> marker; the second marker (in 詩篇與聖詩) is replaced with the
一段「配詩（見上）」說明 held in NOTES.  A chapter whose NOTES entry is empty is skipped.

  python3 books/bible/lamentation/sources/place_hymns.py            # all chapters with notes
  python3 books/bible/lamentation/sources/place_hymns.py 03         # one chapter
"""
import pathlib, re, sys

BOOK = pathlib.Path(__file__).resolve().parents[1]
HYMNS = BOOK / "sources/hymns"

# 中文意譯：每節為與英文逐行對照的行（英文節內換行與此一一對應）
ZH = {
 "01": ["來吧，一切悲傷的人，無論你在哪裏衰殘，\n來到施恩座前，懇切跪下；\n把你受傷的心帶到這裏，在這裏訴說你的痛楚；\n地上沒有一種憂傷，是天上不能醫治的。",
        "荒涼者的喜樂，迷途者的光，\n悔改者的盼望，永不褪色，也純全，\n在這裏，那位安慰者開口，溫柔地說：\n『地上沒有一種憂傷，是天上不能痊癒的。』"],
 "02": ["哦，神聖的頭，如今受了傷，\n滿載憂傷與羞辱，\n如今被人譏誚地圍住，\n荊棘是你唯一的冠冕；\n哦，神聖的頭，何等榮耀！\n直到如今，你曾享何等福樂！\n然而，雖然被人輕看、滿是血污，\n我仍歡喜稱你為我的。",
        "哦，最尊貴、最可愛的容顏！\n從前，世人一見你顯現，都心存敬畏，\n如今，羞辱竟丟在你身上！\n你因痛苦，何等蒼白，\n因沉重的凌辱與嗤笑；\n那曾如晨光明亮的面容，\n如今何等憔悴。"],
 "03": ["神行事，奧妙難測，\n要施行祂的奇事；\n祂的腳蹤立在海中，\n又乘駕風暴。",
        "不要憑淺薄的感官斷定主，\n只要為祂的恩典信靠祂：\n在嚴厲的天意背後，\n祂藏著一張微笑的臉。"],
 "04": ["我們有一位何等的朋友耶穌，\n擔當我們一切的罪與憂；\n何等的特權，能把一切\n都帶到神面前禱告。\n哦，我們常常丟失多少平安，\n哦，我們白受多少不必受的痛，\n都因我們不把一切\n帶到神面前禱告，",
        "我們有試煉與試探嗎？\n有任何地方有煩惱嗎？\n我們絕不該灰心，\n要帶到主面前禱告。\n能找到這樣信實的朋友嗎，\n肯分擔我們一切的憂傷？\n耶穌知道我們每一個軟弱，\n要帶到主面前禱告，"],
 "05": ["引導我吧，仁慈的光，在四面圍繞的黑暗裏，\n引導我前行；\n夜是黑的，我離家甚遠，\n引導我前行。\n保守我的腳步；我不求看見\n遠處的景象；一步，對我已經足夠。",
        "我從前並不如此，也沒有祈求你\n引導我前行；\n我喜歡自己選擇、自己看清我的路；但如今\n引導我前行。\n我愛過那炫目的白晝；縱然有懼怕，\n驕傲仍轄制我的意志：求你不要記念過去的年日。"],
 "06": ["每一個早晨，都有新的愛，\n我們醒來、起身便是見證；\n經過睡眠與黑暗，平安被帶過，\n重得生命、力量與思想。",
        "新的憐憫，隨每一個回來的日子，\n在我們禱告時環繞我們；\n新的危險已過，新的罪已蒙赦免，\n新的對神的思念，新的對天的盼望。"],
 "07": ["憐憫的深處啊！還能有\n憐憫為我存留嗎？\n我的神能收回祂的怒氣，\n饒恕我這罪人中的罪魁嗎？",
        "我抗拒祂的恩典已經很久，\n很久當面惹動祂，\n不肯聽祂的呼召，\n千次的跌倒使祂憂傷。"],
 "08": ["萬古磐石，為我裂開，\n讓我藏身在你裏面；\n願那水與血，\n從你被刺的肋旁流出，\n作罪的雙重療法，\n潔淨我的罪咎，也潔淨罪的權勢。",
        "縱使我的熱心沒有止息，\n縱使我的眼淚永遠流下，\n這一切都不能為罪贖罪；\n你必拯救，惟有你；\n我手中一無所有，\n只緊緊抓住你的十字架。"],
 "09": ["為主的受膏者歡呼！\n大衛更大的子孫！\n在所定的時候歡呼，\n祂的王權在地上開始；\n祂來破除壓迫，\n釋放被擄的人，\n除去罪過，\n並以公平掌權。",
        "祂帶著迅速的救助而來，\n臨到受冤屈的人；\n幫助貧窮與有需要的，\n叫軟弱的得剛強；\n賜他們歌唱代替嘆息，\n使他們的黑暗轉為光明；\n他們被定罪、將死的靈魂，\n在祂眼中是寶貴的。"],
 "10": ["我們的神，是過去世世代代的幫助，\n是我們將來歲月的盼望，\n是我們避風暴的遮蔽，\n也是我們永遠的家！",
        "在你寶座的蔭庇下，\n你的聖徒安然居住；\n你的膀臂單獨已足夠，\n我們的保障是穩固的。"],
}

# 配詩（見上）說明：撰寫者讀過該章後填寫；必須誠實，不可說經文與聖詩互相引用
NOTES = {}
NOTES_FILE = BOOK / "sources/hymn-notes.py"
if NOTES_FILE.exists():
    exec(NOTES_FILE.read_text(encoding="utf8"))


def header(path):
    h = {}
    for line in path.read_text(encoding="utf8").split("\n"):
        if not line.strip():
            break
        k, _, v = line.partition(": ")
        h[k] = v
    return h


def stanzas(path):
    body = path.read_text(encoding="utf8").split("\n\n", 1)[1]
    return [s.strip("\n") for s in body.split("\n\n")]


def block(nn):
    path = next(HYMNS.glob(f"{nn}-*.txt"))
    h = header(path)
    y = h.get("YEAR", "")
    credit = h["AUTHOR"] if y.startswith("not stated") else f"{h['AUTHOR']}，{y.split(' (')[0]}"
    out = [f"> **{h['TITLE']}** \\", f"> *{credit}*", ">"]
    st = stanzas(path)
    for s in st:
        out.append("> " + " \\\n> ".join(s.split("\n")))
        out.append(">")
    for z in ZH[nn]:
        out.append("> " + " \\\n> ".join(z.split("\n")))
        out.append(">")
    return "\n".join(out[:-1])


def main():
    only = sys.argv[1].zfill(2) if len(sys.argv) > 1 else None
    for f in sorted(BOOK.glob("[0-9][0-9]-*.md")):
        nn = f.name[:2]
        if only and nn != only:
            continue
        if nn not in NOTES:
            print(nn, "skipped (no note yet)")
            continue
        t = f.read_text(encoding="utf8")
        if "<!-- HYMN-PENDING" not in t:
            print(nn, "no marker")
            continue
        markers = list(re.finditer(r"<!-- HYMN-PENDING[^>]*-->", t))
        assert len(markers) == 2, (nn, len(markers))
        t = t[:markers[1].start()] + NOTES[nn].strip() + t[markers[1].end():]
        t = t[:markers[0].start()] + block(nn) + t[markers[0].end():]
        f.write_text(t, encoding="utf8")
        print(nn, "placed")


main()

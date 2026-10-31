#!/usr/bin/env python3
"""Expand @@HYMN NN@@ and @@HYMNNOTE NN@@ markers in chapter files from sources/hymns/NN-*.txt.
English lines are copied from the fetched files; the Chinese lines are the editor's own rendering.
usage: python3 expand_hymns.py <chapter.md> [...]"""
import re, sys, glob
from pathlib import Path
HERE = Path(__file__).resolve().parent

H = {
 "01": dict(title="God Moves in a Mysterious Way", credit="William Cowper; text from *Olney Hymns* (1840 edition, Wikisource), stanzas 1, 4", st=[0, 3],
  zh=[["神行事奇妙，", "要行祂的奇事；", "祂的腳蹤踏在海裏，", "乘著風暴而行。"],
      ["不要憑微弱的感覺論斷主，", "只要因祂的恩典信靠祂；", "在嚴厲的天意背後，", "祂藏著一張微笑的臉。"]],
  note="第四節說「不要憑微弱的感覺論斷主」，在嚴厲的天意背後「祂藏著一張微笑的臉」。這首詩與本章經文沒有互相引用；放在這裏，是因為它與本章一樣，先不替神的作為下結論。"),
 "02": dict(title="Be Still, My Soul", credit="Katharina von Schlegel, tr. Jane Borthwick; text from hymntime.com (Cyber Hymnal), stanzas 1, 2", st=[0, 1],
  zh=[["安靜吧，我的靈魂：主站在你這一邊。", "耐心背起十字架，無論是憂傷或痛苦。", "交託你的神去安排、去供應；", "在每一次變遷中，祂必信實不變。", "安靜吧，我的靈魂：你最好的、屬天的朋友，", "要領你走過荊棘的路，到歡喜的終點。"],
      ["安靜吧，我的靈魂：你的神必親自擔當，", "引導未來，如同祂引導過去。", "你的盼望、你的信靠，不要讓任何事動搖；", "如今奧祕的一切，終必明亮。", "安靜吧，我的靈魂：風與浪仍然認得", "祂的聲音——祂住在世上時，曾向風浪發命令。"]],
  note="這首詩一再重複「安靜吧」，並說風和浪仍然認得祂的聲音。它與1:7 的「靜默無聲」沒有互相引用；兩處的「安靜」，一處是在日子之前，一處是在盼望之中。"),
 "03": dict(title="Day of Wrath! O Day of Mourning", credit="Dies Irae, attributed to Thomas of Celano, tr. William Josiah Irons; text from Wikisource (Irons), stanzas 1, 2", st=[0, 1],
  zh=[["忿怒的日子！悲痛的日子！", "看哪，先知的警告得了應驗，", "天與地都在灰燼中焚燒！"],
      ["哦，何等的恐懼撕裂人的胸膛，", "當審判者從天降臨，", "一切都繫於祂的判決。"]],
  note="第一節說「先知的警告」得了應驗，但沒有點名是哪一位先知，也沒有引用西番雅書；本書採用這首詩，只因它的第一行與1:15 的「忿怒的日子」同一個畫面。"),
 "04": dict(title="Come, Ye Sinners, Poor and Needy", credit="Joseph Hart; text from hymntime.com (Cyber Hymnal), stanzas 1, 2", st=[0, 1],
  zh=[["來吧，罪人，困苦可憐的，", "軟弱受傷、病痛的人，", "耶穌預備好站著要拯救你們，", "滿有憐憫，又有能力。", "祂能，祂能；", "祂願意：不要再懷疑。"],
      ["嗬，貧乏的人，來吧，歡迎！", "讚美神白白的豐富。", "真實的信，真實的悔改，", "每一樣領我們靠近的恩典——", "不用錢，不用錢，", "來到耶穌基督面前，來買。"]],
  note="第二節說「每一樣領我們靠近的恩典」（brings us nigh）。這首詩沒有引用2:3；它與本章的相同處是：邀請在先，而且邀請的人是「預備好站著」的那一位。"),
 "05": dict(title="Jesus Shall Reign Where'er the Sun", credit="Isaac Watts; text from hymntime.com (Cyber Hymnal), stanzas 1, 2", st=[0, 1],
  zh=[["耶穌必作王，太陽所到之處，", "日日運行的路途之上；", "祂的國度從海岸伸到海岸，", "直到月亮不再盈虧。"],
      ["看哪，眾海島連同她們的君王，", "歐羅巴也獻上她最好的貢物；", "從北到南，眾王相聚，", "在祂腳前呈上敬意。"]],
  note="詩中有「海島」「從北到南」的列國向祂呈上敬意。這首詩沒有引用西番雅書；2:11 說列國海島的居民各在自己的地方敬拜祂，兩處的畫面相近，是編者的對照。"),
 "06": dict(title="Come, Thou Fount of Every Blessing", credit="Robert Robinson; text from hymntime.com (Cyber Hymnal), stanzas 1, 4", st=[0, 3],
  zh=[["來吧，一切恩福的源頭，", "調準我的心歌頌你的恩；", "憐憫的溪流永不止息，", "呼喚最響亮的讚美。", "教我一首悅耳的歌，", "是天上火焰般的舌頭所唱。", "讚美那山！我已站定在其上，", "那是你救贖之愛的山。"],
      ["哦，我對恩典何等虧欠，", "天天不得不如此！", "願你的恩慈，像一條鎖鏈，", "把我流浪的心繫在你身上。", "我容易漂流，主啊，我感覺得到，", "容易離開我所愛的神；", "我的心在這裏，求你收下並蓋印，", "為你天上的院宇蓋印。"]],
  note="第四節說「我容易漂流……容易離開我所愛的神」，並求恩慈像鎖鏈把心繫住。這首詩與3:2 的「不親近他的神」沒有互相引用；詩中的人承認自己會離開，而且求神把他繫住。"),
 "07": dict(title="Dear Lord and Father of Mankind", credit="John Greenleaf Whittier, adapted by Garrett Horder; text from Wikisource (*The Canadian Soldiers' Song Book*), stanzas 1, 4", st=[0, 3],
  zh=[["親愛的主，人類的父，", "求你饒恕我們狂熱的作為！", "把我們合宜的心思重新給我們穿上；", "在更純淨的生活中尋見事奉你，", "在更深的敬畏中尋見讚美。"],
      ["在那深沉的肅靜之中，", "我們壓過你呼召的細微聲音的", "一切言語與工作都歸於平息，", "願你的祝福如此無聲地降下，", "像你的嗎哪降下一樣。"]],
  note="詩中求主饒恕「狂熱的作為」，並在肅靜裏等候祂的祝福像嗎哪一樣無聲降下。這首詩沒有引用西番雅書；它與本章的相同處是「等候」：祝福不是人搶來的，是降下來的。"),
 "08": dict(title="Rejoice, the Lord Is King", credit="Charles Wesley; text from *Hymns for our Lord's Resurrection* (1746, Wikisource), stanzas 1, 2", st=[0, 1],
  zh=[["歡喜吧，主是王！", "敬拜你們的主、你們的王，", "世人哪，獻上感謝，歌唱，", "永遠得勝；", "舉起你的心，舉起你的聲音，", "我再說，要歡喜。"],
      ["耶穌，救主作王，", "是真理與慈愛的神，", "祂洗淨了我們的污點，", "就升上高處坐下；", "舉起你的心，舉起你的聲音，", "我再說，要歡喜。"]],
  note="全詩的重複句是「我再說，要歡喜」。這首詩與3:14 的四個歡呼命令沒有互相引用；兩處都先下命令，再說理由：理由是那位王。"),
}

def stanzas(path):
    t = Path(path).read_text(encoding="utf-8").split("\n\n", 1)[1].strip()
    return [s.split("\n") for s in re.split(r"\n\s*\n", t)]

def block(nn):
    h = H[nn]; f = glob.glob(str(HERE / "hymns" / f"{nn}-*.txt"))[0]
    st = stanzas(f); out = [f"> **{h['title']}** \\", f"> {h['credit']}", ">"]
    for k, i in enumerate(h["st"]):
        en = st[i]; zh = h["zh"][k]
        assert len(en) == len(zh), (nn, i, len(en), len(zh))
        out.append("> " + " \\\n> ".join(en)); out.append(">")
        out.append("> " + " \\\n> ".join(zh))
        if k < len(h["st"]) - 1: out.append(">")
    return "\n".join(out)

def note(nn):
    h = H[nn]
    return f"### {h['title']}（見上「配詩」）\n\n{h['note']}"

for p in sys.argv[1:]:
    t = Path(p).read_text(encoding="utf-8")
    t = re.sub(r"^@@HYMN (\d\d)@@[ \t]*$", lambda m: block(m[1]), t, flags=re.M)
    t = re.sub(r"^@@HYMNNOTE (\d\d)@@[ \t]*$", lambda m: note(m[1]), t, flags=re.M)
    Path(p).write_text(t, encoding="utf-8"); print("expanded", p)

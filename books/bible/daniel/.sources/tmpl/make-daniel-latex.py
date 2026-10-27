#!/usr/bin/env python3
"""Derive templates/pdf/daniel.latex from templates/pdf/ezra.latex: same page machinery, new cover / frontispiece /
title page / closing page / metadata. Re-run after editing the blocks below."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
src = (ROOT / "templates/pdf/ezra.latex").read_text().split("\n")

def find(s, start=0):
    for i in range(start, len(src)):
        if s in src[i]: return i
    raise SystemExit("marker not found: " + s)

COVER = r'''%% ============================================
%% COVER ART PAGE - three concentric zones: the Most High at the centre, the kingdom
%% given around Him, the empires of the nations at the rim.
%% ============================================
\thispagestyle{empty}
\begin{tikzpicture}[remember picture, overlay]
  \fill[ScriptureBg] (current page.south west) rectangle (current page.north east);
  \draw[ScriptureGold, line width=2.8pt]
    ([xshift=0.42in,yshift=0.42in]current page.south west)
    rectangle
    ([xshift=-0.42in,yshift=-0.42in]current page.north east);
  \draw[ScriptureGold, line width=0.5pt]
    ([xshift=0.50in,yshift=0.50in]current page.south west)
    rectangle
    ([xshift=-0.50in,yshift=-0.50in]current page.north east);
  \draw[ChapterStone, line width=0.3pt, opacity=0.55]
    ([xshift=0.58in,yshift=0.58in]current page.south west)
    rectangle
    ([xshift=-0.58in,yshift=-0.58in]current page.north east);
  \foreach \cnr in {south west, south east, north west, north east} {
    \fill[ScriptureGold] ([xshift=0.42in,yshift=0.50in]current page.\cnr) circle (0.045in);
    \fill[ScriptureGold] ([xshift=0.58in,yshift=0.50in]current page.\cnr) circle (0.045in);
    \fill[ScriptureGold] ([xshift=0.50in,yshift=0.42in]current page.\cnr) circle (0.045in);
    \fill[ScriptureGold] ([xshift=0.50in,yshift=0.58in]current page.\cnr) circle (0.045in);
    \fill[HandClay]  ([xshift=0.50in,yshift=0.50in]current page.\cnr) circle (0.040in);
    \fill[ScriptureGold] ([xshift=0.50in,yshift=0.50in]current page.\cnr) circle (0.012in);
  }
\end{tikzpicture}

\begin{center}
\vspace*{0.42in}

{\footnotesize\scshape\color{ChapterStone} Three Books Deep Reading \textbullet\ Daniel}\\[0.08cm]
{\footnotesize\color{TextGray} 三書精讀 \textbullet\ 但以理書深度研讀}

\vspace{0.16cm}
\begin{tikzpicture}
  \draw[ScriptureGold, line width=0.8pt] (-2.6,0) -- (-0.5,0);
  \fill[ScriptureGold] (-0.35,0) circle (0.04);
  \fill[ScriptureGold] (0,0) circle (0.06);
  \fill[ScriptureGold] (0.35,0) circle (0.04);
  \draw[ScriptureGold, line width=0.8pt] (0.5,0) -- (2.6,0);
\end{tikzpicture}
\vspace{0.22cm}

{\fontsize{13}{15}\selectfont\itshape\color{TextGray} 國度是被賜的，不是被奪的 \textperiodcentered\ The Kingdom Is Given, Not Seized}

\vspace{0.30cm}

% ===== THREE CONCENTRIC ZONES: THE MOST HIGH / THE KINGDOM / THE EMPIRES =====
\begin{tikzpicture}[scale=0.85, transform shape]
  % Outer zone - the empires of the nations (2, 7, 8)
  \fill[HandClay, opacity=0.16] (0,0.1) circle (1.65);
  \draw[HandClay, line width=0.9pt, opacity=0.75] (0,0.1) circle (1.65);
  % Middle zone - the kingdom given (2:44, 7:14, 7:27)
  \fill[ReturnAmber, opacity=0.14] (0,0.1) circle (1.15);
  \draw[ReturnAmber, line width=1.0pt, opacity=0.85] (0,0.1) circle (1.15);
  % Inner zone - the Most High
  \fill[ChapterStone, opacity=0.22] (0,0.1) circle (0.55);
  \draw[ChapterStone, line width=1.0pt, opacity=0.9] (0,0.1) circle (0.55);
  \node[font=\tiny,color=ChapterStone] at (0,-0.65) {至高者};
  \node[font=\tiny,color=ReturnAmber!80!black] at (0,-1.28) {國度};
  \node[font=\tiny,color=HandClay!80!black]  at (0,-1.9) {列國};
\end{tikzpicture}

\vspace{0.10cm}
\textcolor{ScriptureGold}{\rule{2.8in}{0.8pt}}
\vspace{0.24cm}

{\fontsize{34}{40}\selectfont\bfseries\color{ChapterStone}\kaiti\selectfont 至高者掌權}\\[0.10cm]
{\fontsize{16}{20}\selectfont\scshape\color{CommentaryBrown} The Most High Rules}

\vspace{0.20cm}
{\fontsize{22}{26}\selectfont\bfseries\kaiti\selectfont 但以理書研讀}\\[0.08cm]
{\fontsize{13}{16}\selectfont\itshape\color{TextGray} A Study of the Book of Daniel}

\vspace{0.24cm}
% One Aramaic word only: XeTeX lays out a maqaf- or space-joined RTL phrase as
% separate runs in LTR order (word order and maqaf come out scrambled).
{\fontsize{15}{18}\selectfont\itshape\color{ChapterStone} שַׁלִּיט }\quad
{\footnotesize\scshape\color{CommentaryBrown} “shallit”}\quad
{\footnotesize\bfseries\color{ReturnAmber!80!black} 掌權 \textperiodcentered\ 至高者掌權（但 4:17）}

\vfill

\fcolorbox{ScriptureGold}{white}{%
\begin{minipage}{4.3in}
\centering\vspace{0.15cm}
{\footnotesize\color{ReturnAmber!70!black}\kaiti\selectfont
「……好叫世人知道至高者在人的國中掌權，要將國賜與誰就賜與誰，或立極卑微的人執掌國權。」}\\[0.10em]
{\scriptsize\itshape\color{TextGray}
“\ldots In order that the living may know / That the Most High is ruler over the realm of mankind, / And bestows it on whom He wishes / And sets over it the lowliest of men.”}\\[0.10em]
{\scriptsize\color{ChapterStone} 但以理書 4:17 \textperiodcentered\ Daniel 4:17}
\vspace{0.15cm}
\end{minipage}}

\vspace{0.3in}
\end{center}
\cleardoublepage
'''

FRONT = r'''%% ============================================
%% FRONTISPIECE - "全書一句話" built on Daniel 7:13-14: the kingdom is given.
%% ============================================
\thispagestyle{empty}
\begin{center}
\vspace*{0.1in}

\begin{tikzpicture}
  \draw[ScriptureGold, line width=0.8pt] (-2.8,0) -- (-0.55,0);
  \fill[ScriptureGold] (0,0) circle (0.055);
  \draw[ScriptureGold, line width=0.8pt] (0.55,0) -- (2.8,0);
\end{tikzpicture}

\vspace{0.12cm}
{\Large\bfseries\color{ChapterStone} 全書一句話 \textperiodcentered\ The Whole Book in One Verse}

\vspace{0.30cm}
\fcolorbox{ScriptureGold}{ScriptureBg}{%
\begin{minipage}{4.6in}
\centering\vspace{0.2cm}
\normalsize\color{CommentaryBrown}
……見有一位像人子的，駕著天雲而來，被領到亙古常在者面前，\textbf{\color{HandClay!80!black}得了}權柄、榮耀、國度，
使各方、各國、各族的人都事奉他。他的權柄是永遠的，不能廢去；他的國必不敗壞。\\[0.5em]
\footnotesize\itshape
\ldots One like a Son of Man was coming, / And He came up to the Ancient of Days / And was presented before Him. / And to Him \textbf{was given} dominion, / Glory and a kingdom, / That all the peoples, nations and men of every language / Might serve Him. / His dominion is an everlasting dominion / Which will not pass away; / And His kingdom is one / Which will not be destroyed.\\[0.4em]
\small\color{ChapterStone} 但以理書 7:13-14 \textperiodcentered\ Daniel 7:13-14
\vspace{0.2cm}
\end{minipage}}

\vspace{0.35cm}
{\small\color{TextGray} 十二章經文 \textperiodcentered\ 十六篇研讀 \textperiodcentered\ 五卷 \textperiodcentered\ 國度是賜的，不是奪的\\
\textit{Twelve chapters of Daniel in sixteen studies \textperiodcentered\ five volumes \textperiodcentered\ the kingdom is given, not seized}}

\vspace{0.30cm}
{\small
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{@{}p{2.8cm}p{2.4cm}p{6.9cm}@{}}
\toprule
\textbf{卷} & \textbf{研讀篇} & \textbf{在全書的展開} \\
\midrule
卷一：在巴比倫立志 & 1篇 & 被擄本身是「主將……交付他手」；神先交付，人才立志 \\
卷二：列國之王與天上的神 & 2-7篇 & 天上的神廢王、立王；至高者在人的國中掌權；金像、火窯、牆上的字、獅子坑 \\
卷三：四獸與人子 & 8-10篇 & 列國的權柄是借來的；開庭在先；國賜給像人子的，也賜給至高者的聖民 \\
卷四：禱告與七十個七 & 11-12篇 & 先讀書、後禱告；答覆在懇求之初就發出；歷史的時間表交給禱告的人 \\
卷五：看不見的爭戰與結局 & 13-16篇 & 結局寫在真確書上；名錄在冊上的必得拯救；人只要去等候，到了末期，必起來 \\
\bottomrule
\end{tabular}
}

\vspace{0.2cm}
\textcolor{ScriptureGold}{\rule{2.5in}{0.7pt}}
\vspace{0.15cm}

{\bfseries\color{ChapterStone} 讀經之鑰 \textperiodcentered\ How to Read This Book}

\vspace{0.12cm}
\begin{minipage}{4.6in}
\footnotesize\color{TextGray}
不是來讀一張末世時間表，是來看一位神怎樣在巴比倫掌權：「至高者在人的國中掌權，要將國賜與誰就賜與誰」（4:17, 25, 32）。列國的權柄是被賜的，所以也是被收的；最後賜給人子，並賜給至高者的聖民。\\[0.3em]
\textit{\scriptsize
You are watching one God rule in Babylon. Three times the book says, in the same words, that the Most High rules over the realm of mankind and gives it to whom He wishes (4:17, 25, 32). Empires hold power on a lease; at the last it is given to the Son of Man and to the saints of the Highest.}
\end{minipage}

\vfill
{\scriptsize\color{LightGray} PubHub 三書精讀系統 \textperiodcentered\ Soli Deo Gloria}

\vspace{0.3in}
\end{center}
\cleardoublepage
'''

TITLE = r'''% Title page
\begin{titlepage}
\thispagestyle{empty}
\begin{center}
\vspace*{0.5cm}

\crosssymbol\hspace{0.3cm}{\color{ScriptureGold}\rule{2.5in}{1pt}}\hspace{0.3cm}\crosssymbol

\vspace{0.4cm}

{\fontsize{36}{42}\selectfont\bfseries\color{ChapterStone}\kaiti\selectfont 至高者掌權}\\[0.2cm]
{\large\itshape\color{LightGray} The Most High Rules}

\vspace{0.6cm}

{\fontsize{22}{28}\selectfont\bfseries 但以理書研讀}\\[0.15cm]
{\normalsize A Study of the Book of Daniel}

\vspace{0.5cm}

\fcolorbox{ScriptureGold}{ScriptureBg}{%
\begin{minipage}{3.8in}
\centering
\vspace{0.3cm}
\small\itshape\color{CommentaryBrown}
……至高者在人的國中掌權，\\
要將國賜與誰就賜與誰……\\[0.15em]
\footnotesize \ldots the Most High is ruler over the realm of mankind, / And bestows it on whom He wishes\ldots\ — Daniel 4:17
\vspace{0.3cm}
\end{minipage}
}

\vspace{0.4cm}

% Five-volume structure diagram. Plain centimetre coordinates, no picture-level
% `scale` (node sizes ignore it while positions obey it).
\begin{tikzpicture}[every node/.style={align=center}]
  \node[font=\footnotesize\bfseries,color=ChapterStone] at (0,1.9) {全書五卷 Five Volumes, 16 Studies};

  \node[draw=ChapterStone,fill=ScriptureBg,rounded corners,minimum width=2.3cm,minimum height=0.9cm,font=\tiny,text width=2.1cm] (v1) at (-5.6,0.8) {卷一 \textperiodcentered\ 在巴比倫立志};
  \node[font=\tiny,color=LightGray] at (-5.6,0.05) {1};

  \node[draw=ReturnAmber,fill=ScriptureBg,rounded corners,minimum width=2.3cm,minimum height=0.9cm,font=\tiny,text width=2.1cm] (v2) at (-2.8,0.8) {卷二 \textperiodcentered\ 列國之王與天上的神};
  \node[font=\tiny,color=LightGray] at (-2.8,0.05) {2-7};

  \node[draw=ReturnAmber,fill=ScriptureBg,rounded corners,minimum width=2.3cm,minimum height=0.9cm,font=\tiny,text width=2.1cm] (v3) at (0,0.8) {卷三 \textperiodcentered\ 四獸與人子};
  \node[font=\tiny,color=LightGray] at (0,0.05) {8-10};

  \node[draw=HandClay,fill=ScriptureBg,rounded corners,minimum width=2.3cm,minimum height=0.9cm,font=\tiny,text width=2.1cm] (v4) at (2.8,0.8) {卷四 \textperiodcentered\ 禱告與七十個七};
  \node[font=\tiny,color=LightGray] at (2.8,0.05) {11-12};

  \node[draw=HandClay,fill=ScriptureBg,rounded corners,minimum width=2.3cm,minimum height=0.9cm,font=\tiny,text width=2.1cm] (v5) at (5.6,0.8) {卷五 \textperiodcentered\ 看不見的爭戰與結局};
  \node[font=\tiny,color=LightGray] at (5.6,0.05) {13-16};

  \draw[->,color=ScriptureGold,thick] (v1.east) -- (v2.west);
  \draw[->,color=ScriptureGold,thick] (v2.east) -- (v3.west);
  \draw[->,color=ScriptureGold,thick] (v3.east) -- (v4.west);
  \draw[->,color=ScriptureGold,thick] (v4.east) -- (v5.west);
\end{tikzpicture}

\vspace{0.2cm}

{\footnotesize\color{TextGray} 「主將猶大王約雅敬……交付他手」（但 1:2）}

\vfill

{\normalsize\color{ScriptureGold}\bfseries 國度是被賜的，不是被奪的；列國如此，聖民亦如此}\\[0.1cm]
{\footnotesize\color{LightGray} The kingdom is given, not seized: to the nations on a lease, at the last to the Son of Man and the saints (Daniel 2:21; 4:17; 7:14, 27)}

\vspace{0.5cm}

$if(author)$
{\normalsize $author$}\\[0.3cm]
$endif$

$if(publisher)$
{\small $publisher$}\\[0.15cm]
$endif$

$if(date)$
{\small $date$}
$else$
{\small \today}
$endif$

\vspace{0.3cm}
\crosssymbol\hspace{0.3cm}{\color{ScriptureGold}\rule{2.5in}{1pt}}\hspace{0.3cm}\crosssymbol

\end{center}
\end{titlepage}
'''

COPY = r'''\textbf{但以理書研讀 / Daniel Deep Study}\\[0.8em]

Copyright \copyright\ \the\year\ $if(author)$$author$$endif$\\
All rights reserved.\\[0.8em]

\textbf{聖經版本 / Bible Versions}\\
中文：和合本 (CUV)，公有領域\\
English: New American Standard Bible 1995 (NASB)\\[0.8em]

\textbf{主要參考資料 / Primary Sources}\\
\textbullet\ John Calvin - Commentaries on the Book of the Prophet Daniel (CCEL, public domain)\\
\textbullet\ Matthew Henry - Commentary on the Whole Bible\\
\textbullet\ John MacArthur - Daniel sermon series, gty.org (27-01 to 27-31)\\
\textbullet\ G. Campbell Morgan - Living Messages of the Books of the Bible, overview only\\
\textbullet\ Hippolytus; Flavius Josephus (public domain)\\
\textbullet\ Sefaria - Miqra according to the Masorah (Hebrew and Aramaic text)\\[0.8em]

本書為七年三書精讀項目成果之一。\\
Part of the 7-Year Three Books Deep Reading Project.
'''

CLOSE = r'''\vspace{0.3cm}
{\fontsize{22}{26}\selectfont\bfseries\kaiti\selectfont 國度是賜的}\\[0.1cm]
{\normalsize\itshape\color{LightGray} The Kingdom Is Given}

\vspace{0.35cm}

\fcolorbox{ScriptureGold}{white}{%
\begin{minipage}{4.7in}
\centering\vspace{0.18cm}
{\footnotesize\bfseries\color{ChapterStone} 全書五卷 \;\; Five Volumes}\\[0.3em]
{\footnotesize\color{TextGray}
在巴比倫立志 (1) \textbullet\ 列國之王與天上的神 (2-7) \textbullet\ 四獸與人子 (8-10)\\
禱告與七十個七 (11-12) \textbullet\ 看不見的爭戰與結局 (13-16)}
\vspace{0.18cm}
\end{minipage}}

\vspace{0.35cm}
\textcolor{ScriptureGold}{\rule{2.5in}{0.7pt}}
\vspace{0.3cm}

{\footnotesize\itshape\color{CommentaryBrown}
「你且去等候結局，因為你必安歇。到了末期，你必起來，享受你的福分。」}\\[0.15cm]
{\scriptsize\color{ChapterStone} — 但以理書 12:13}
'''

def seg(a_marker, b_marker, start=0):
    a = find(a_marker, start); b = find(b_marker, a + 1); return a, b

out = list(src)
# work from the bottom up so earlier indices stay valid
a = find("{\\fontsize{22}{26}\\selectfont\\bfseries\\kaiti\\selectfont 我們神的手}") - 1   # the \vspace line above it
b = find("— 以斯拉記 8:22")
out[a:b + 1] = CLOSE.rstrip("\n").split("\n")
a = find("\\textbf{以斯拉記研讀 / Ezra Deep Study}")
b = find("Part of the 7-Year Three Books Deep Reading Project.")
out[a:b + 1] = COPY.rstrip("\n").split("\n")
a = find("% Title page"); b = find("\\end{titlepage}")
out[a:b + 1] = TITLE.rstrip("\n").split("\n")
a = find("%% FRONTISPIECE") - 1; b = find("\\cleardoublepage", a)
out[a:b + 1] = FRONT.rstrip("\n").split("\n")
a = find("%% COVER ART PAGE") - 1; b = find("\\cleardoublepage", a)
out[a:b + 1] = COVER.rstrip("\n").split("\n")
text = "\n".join(out)
rep = [
 ("% PubHub Ezra Deep Study Template", "% PubHub Daniel Deep Study Template"),
 ("% Series identity: Stone/Amber/Clay palette - the return from Babylon, the temple\n% rebuilt stone by stone, and the hand of God that goes before. Deliberately\n% distinct from Joshua's Jordan blue and Job's Ash/Storm/Dawn.",
  "% Series identity: Stone/Amber/Clay palette (shared with the Ezra volume) - the stone cut\n% without hands, the amber of the lion's-den dusk, the clay of the image's feet.\n% Derived from templates/pdf/ezra.latex by books/bible/daniel/.sources/tmpl/make-daniel-latex.py."),
 ("Ezra's Word Study\n%% sections use pointed Hebrew AND Aramaic (Hebrew-block characters; Aramaic\n%% runs at 4:8-6:18 and 7:12-26)", "Daniel's Word Study\n%% sections use pointed Hebrew AND Aramaic (Hebrew-block characters; Aramaic\n%% runs at 2:4b-7:28)"),
 ("COLOR SCHEME - Ezra identity: the stone of the rebuilt temple, the amber\n%% of the lamp-lit road, the clay of the register", "COLOR SCHEME - Daniel: the stone of 2:34, the amber of the furnace and the\n%% lamp, the clay of the image's feet"),
 ("% Ezra is not a Gospel", "% Daniel is not a Gospel"),
 ("                                                 % for the temple foundation laid in 3章", "                                                 % for the stone cut without hands (2:34)"),
 ("% Warm accent - the return and the road (1-3章, 7-8章): amber", "% Warm accent - the furnace and the lamp: amber"),
 ("% Earth accent - the register and the confession (2章, 10章): clay", "% Earth accent - the image's feet of clay: clay"),
 ("pdfsubject={以斯拉記逐章研讀：歸回、重建聖殿、神施恩的手在先——十章經文，十四篇研讀}", "pdfsubject={但以理書逐章研讀：至高者在人的國中掌權、國度是賜的不是奪的——十二章經文，十六篇研讀}"),
 ("pdfkeywords={以斯拉記, Ezra, 歸回, 重建聖殿, 神的手, 聖經研讀, Bible Study, 和合本, NASB, 查經}", "pdfkeywords={但以理書, Daniel, 至高者, 國度, 人子, 七十個七, 聖經研讀, Bible Study, 和合本, NASB, 查經}"),
]
for a_, b_ in rep:
    if a_ not in text: print("WARN: not found:", a_[:50])
    text = text.replace(a_, b_)
(ROOT / "templates/pdf/daniel.latex").write_text(text)
print("wrote templates/pdf/daniel.latex")

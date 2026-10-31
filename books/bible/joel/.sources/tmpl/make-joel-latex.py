#!/usr/bin/env python3
"""Derive templates/pdf/joel.latex from templates/pdf/jude.latex.

Same page machinery as Jude (which follows templates/pdf/revelation.latex's full-bleed cover convention, i.e.
the Gospel of John / Revelation house cover: dark gradient, double gold hairline border, corner ornaments,
cross emblem, fleurons, Baskerville/Didot). New here: the ember palette, cover / title page / frame page /
colophon / back cover text and diagrams, PDF metadata. Verse texts printed on the covers are read from
.sources/scripture-all.tsv and asserted, never hand-typed.

Re-run after editing the blocks below:  python3 books/bible/joel/.sources/tmpl/make-joel-latex.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = (ROOT / "templates/pdf/jude.latex").read_text()
TSV = {}
for l in (ROOT / "books/bible/joel/.sources/scripture-all.tsv").read_text().splitlines():
    if l.startswith("#") or not l:
        continue
    k, zh, en = l.split("\t")
    TSV[k] = (zh, en)


def must_contain(ref, fragment, col):
    assert fragment in TSV[ref][col], f"{ref}: {fragment!r} not in scripture-all.tsv"


# ---- header (preamble) -------------------------------------------------------------------------------------------
head, rest = SRC.split("%% --------------------------------------------\n%% FRONT MATTER", 1)
rest = "%% --------------------------------------------\n%% FRONT MATTER" + rest

for a, b in [
    ("% PubHub Epistle of Jude Template", "% PubHub Book of Joel Template"),
    ("Bilingual Chinese/English with Greek word studies", "Bilingual Chinese/English with Hebrew word studies"),
    ("ChapterPurple", "ChapterEmber"),
    ("PurpleDark", "EmberDark"),
    ("PurpleLight", "EmberLight"),
    ("% Primary colors - Deep purple for Jude (contending, kept)", "% Primary colors - ember / rust for Joel (the day of the LORD; fire, locust, then rain)"),
    ("{65,35,95}        % Deep purple for chapters", "{118,42,24}        % Rust-ember for chapters"),
    ("{248,245,252}           % Light purple for Greek", "{251,245,238}           % Light ember tint for Greek/Hebrew"),
    ("{16,8,24}", "{26,10,6}"),
    ("{65,35,95}", "{104,40,22}"),
    ("{188,178,198}", "{204,186,170}"),
    ("Matches templates/pdf/revelation.latex's cover convention, retoned to\n%% this book's deep-purple/gold palette instead of Revelation's navy.",
     "Matches templates/pdf/revelation.latex's cover convention (as Jude does), retoned to\n%% this book's ember/gold palette."),
    ("% Cover gradient (near-black purple at top to the book's own\n% ChapterEmber at bottom)", "% Cover gradient (near-black umber at top to the book's own ember at bottom)"),
    ("\\PackageWarning{jude}", "\\PackageWarning{joel}"),
    ("pdftitle={猶大書研讀 — Epistle of Jude Deep Study}", "pdftitle={約珥書研讀 — The Book of Joel Deep Study}"),
    ("pdfsubject={猶大書逐段研讀：蒙保守的人，為真道竭力爭辯}", "pdfsubject={約珥書逐段研讀：雖然如此，一心歸向我——耶和華的日子與那扇開著的門}"),
    ("pdfkeywords={猶大書, Jude, 聖經研讀, Bible study, 和合本, NASB, 保守, 爭辯, 背道, 頌榮, 查經}",
     "pdfkeywords={約珥書, Joel, 聖經研讀, Bible study, 和合本, NASB, 耶和華的日子, 蝗災, 歸向, 聖靈澆灌, 錫安, 查經}"),
]:
    assert a in head, f"header marker missing: {a[:50]!r}"
    head = head.replace(a, b)

# ---- front matter: cover, title page, frame page ------------------------------------------------------------------
for ref, frag, col in [("2:12", "一心歸向我", 0), ("2:12", "Return to Me with all your heart", 1),
                       ("2:32", "凡求告耶和華名的就必得救", 0), ("2:32", "whoever calls on the name of the LORD", 1),
                       ("3:21", "耶和華住在錫安", 0), ("3:21", "the LORD dwells in Zion", 1),
                       ("2:11", "他軍旅", 0), ("2:25", "我打發到你們中間的大軍隊", 0), ("2:14", "也未可知", 0), ("2:26", "你們必多吃而得飽足", 0), ("2:27", "你們必知道我是在以色列中間，又知道我是耶和華─你們的神", 0), ("2:32", "Will be delivered", 1)]:
    must_contain(ref, frag, col)

FRONT = r'''%% --------------------------------------------
%% FRONT MATTER
%% --------------------------------------------
\frontmatter
\pagestyle{empty}

% Front cover — full-bleed, light-on-dark — the true first page of the book
\CoverBackground
\CoverBorder
\begin{titlepage}
\thispagestyle{empty}
\color{CoverCream}
\begin{center}
\vspace*{0.9cm}

\coveremblem[CoverGoldBright]

\vspace{0.4cm}

\publishersmark[CoverGoldBright]

\vspace{0.5cm}

\fleuron[CoverGoldBright]\hspace{0.3cm}{\color{CoverGoldBright}\rule{1.6in}{0.4pt}}\hspace{0.3cm}\fleuron[CoverGoldBright]

\vspace{0.5cm}

% Main title
{\fontsize{30}{36}\selectfont\bfseries\color{CoverCream} 雖然如此，一心歸向我}\\[0.25cm]
{\didotfont\large\itshape\color{CoverGoldBright} Yet Even Now — The Book of Joel}

\vspace{0.7cm}

% Book title
{\fontsize{22}{28}\selectfont\bfseries\color{CoverCream} 約珥書研讀}\\[0.2cm]
{\baskervillefont\itshape\normalsize\color{CoverGoldBright} A Study of the Book of Joel}

\vspace{0.8cm}

% Key verse — thin gold rule frame, reading light on dark
\begin{minipage}{4.3in}
\centering
{\color{CoverGoldBright}\rule{4.3in}{0.6pt}}
\vspace{0.35cm}
\small\itshape\color{CoverCream}
耶和華說：雖然如此，你們應當禁食、哭泣、悲哀，一心歸向我。\\[0.2em]
{\baskervillefont\footnotesize\color{CoverCream} “Yet even now,” declares the LORD,\\
“Return to Me with all your heart, And with fasting, weeping and mourning . . .” — Joel 2:12}
\vspace{0.35cm}
{\color{CoverGoldBright}\rule{4.3in}{0.6pt}}
\end{minipage}

\vspace{0.75cm}

% Core theme
{\normalsize\color{CoverGoldBright}\bfseries 災是祂的軍隊，日子是祂的日子，門也在祂手裏}\\[0.12cm]
{\baskervillefont\itshape\footnotesize\color{CoverCream} The army is His, the Day is His — and so is the open door}

\vfill

$if(author)$
{\normalsize\color{CoverCream} $author$}\\[0.3cm]
$endif$

$if(publisher)$
{\small\color{CoverCream} $publisher$}\\[0.15cm]
$endif$

$if(date)$
{\small\color{CoverCream} $date$}
$else$
{\small\color{CoverCream} \today}
$endif$

\vspace{0.4cm}
\fleuron[CoverGoldBright]\hspace{0.35cm}{\color{CoverGoldBright}\rule{1.8in}{0.4pt}}\hspace{0.35cm}\fleuron[CoverGoldBright]

\end{center}
\end{titlepage}
\cleardoublepage

% Title page
\begin{titlepage}
\thispagestyle{empty}
\begin{center}
\vspace*{0.8cm}

% Decorative cross and line
\crosssymbol\hspace{0.3cm}{\color{ScriptureGold}\rule{2.5in}{1pt}}\hspace{0.3cm}\crosssymbol

\vspace{0.5cm}

% Main title
{\fontsize{32}{40}\selectfont\bfseries\color{ChapterEmber} 雖然如此，一心歸向我}\\[0.2cm]
{\large\itshape\color{LightGray} Yet Even Now}

\vspace{0.7cm}

% Book title
{\fontsize{22}{28}\selectfont\bfseries 約珥書研讀}\\[0.15cm]
{\normalsize A Study of the Book of Joel}

\vspace{0.6cm}

% Key verse in box
\fcolorbox{ScriptureGold}{ScriptureBg}{%
\begin{minipage}{4in}
\centering
\vspace{0.3cm}
\small\itshape\color{CommentaryBrown}
凡求告耶和華名的就必得救。\\[0.2em]
\footnotesize . . . whoever calls on the name of the LORD Will be delivered. — Joel 2:32
\vspace{0.3cm}
\end{minipage}
}

\vspace{0.8cm}

% Book Structure diagram — five steps of the order of revelation
\begin{tikzpicture}[scale=0.7]
  \node[font=\footnotesize\bfseries,color=ChapterEmber] at (0,3.5) {Book Structure 書卷結構};

  % (node width is NOT scaled by [scale=0.7] but coordinates are, so centers
  % need real spacing >= box width; 2.9 units * 0.7 = 2.03cm clears 1.9cm boxes)
  \node[draw=ChapterEmber,fill=ScriptureBg,rounded corners,minimum width=1.9cm,minimum height=0.6cm,font=\tiny] at (-5.8,2) {1:1-20 Word};
  \node[font=\tiny,color=LightGray] at (-5.8,1.32) {話臨到};

  \node[draw=ChapterEmber,fill=ScriptureBg,rounded corners,minimum width=1.9cm,minimum height=0.6cm,font=\tiny] at (-2.9,2) {2:1-11 Day};
  \node[font=\tiny,color=LightGray] at (-2.9,1.32) {耶和華的日子};

  \node[draw=ChapterEmber,fill=ScriptureBg,rounded corners,minimum width=1.9cm,minimum height=0.6cm,font=\tiny] at (0,2) {2:12-17 Return};
  \node[font=\tiny,color=LightGray] at (0,1.32) {雖然如此};

  \node[draw=ChapterEmber,fill=ScriptureBg,rounded corners,minimum width=1.9cm,minimum height=0.6cm,font=\tiny] at (2.9,2) {2:18-32 Answer};
  \node[font=\tiny,color=LightGray] at (2.9,1.32) {補還·澆灌};

  \node[draw=ChapterEmber,fill=ScriptureBg,rounded corners,minimum width=1.9cm,minimum height=0.6cm,font=\tiny] at (5.8,2) {3:1-21 Zion};
  \node[font=\tiny,color=LightGray] at (5.8,1.32) {列國·錫安};

  % Arrows
  \draw[->,color=ScriptureGold,thick] (-4.4,2) -- (-4.2,2);
  \draw[->,color=ScriptureGold,thick] (-1.45,2) -- (-1.25,2);
  \draw[->,color=ScriptureGold,thick] (1.45,2) -- (1.65,2);
  \draw[->,color=ScriptureGold,thick] (4.2,2) -- (4.4,2);

  % Core thread at bottom
  \node[draw=ScriptureGold,fill=ScriptureBg,rounded corners,minimum width=5cm,minimum height=0.6cm,font=\small\bfseries,text=CommentaryBrown] at (0,0.3) {His army (2:11) \ensuremath{\rightarrow} Even now (2:12) \ensuremath{\rightarrow} My army (2:25) \ensuremath{\rightarrow} Dwells in Zion (3:21)};
  \node[font=\tiny,color=LightGray] at (0,-0.2) {祂的軍隊 \ensuremath{\rightarrow} 雖然如此 \ensuremath{\rightarrow} 我的大軍隊 \ensuremath{\rightarrow} 耶和華住在錫安};
\end{tikzpicture}

\vfill

% Author info
{\normalsize\color{ScriptureGold}\bfseries 作者：約珥，毗土珥的兒子}\\[0.1cm]
{\footnotesize\color{LightGray} Author: Joel son of Pethuel (1:1); the book names no king and gives no date}

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

% Frame page — from "who knows?" to "you shall know"
\thispagestyle{empty}
\begin{center}
\vspace*{0.5cm}
{\Large\bfseries\color{ChapterEmber} 從「也未可知」到「你們必知道」}\\[0.1cm]
{\normalsize From “Who Knows?” to “You Will Know”}

\vspace{0.6cm}

\begin{tikzpicture}[scale=0.9]
  \draw[ChapterEmber,line width=1.6pt,rounded corners] (-5.6,-4.4) rectangle (5.6,3.8);
  \node[font=\small\bfseries,text=ChapterEmber,align=center] at (0,3.1) {2:14 \ 他轉意後悔……也未可知\\\textit{Who knows whether He will turn and relent?}};

  \draw[ScriptureGold,line width=0.8pt,rounded corners,dashed] (-4.9,-0.6) rectangle (4.9,2.2);
  \node[font=\footnotesize,text=CommentaryBrown,align=center] at (0,1.65) {1:4 \ 蝗蟲吃了，又吃，又吃 \ \textit{has eaten \ldots\ has eaten \ldots\ has eaten}};
  \node[font=\footnotesize,text=CommentaryBrown,align=center] at (0,0.95) {2:25 \ 我打發的大軍隊所吃的年歲，我要補還 \ \textit{I will make up the years}};
  \node[font=\footnotesize,text=CommentaryBrown,align=center] at (0,0.25) {2:26 \ 你們必多吃而得飽足 \ \textit{you will have plenty to eat}};

  \node[draw=ScriptureGold,fill=ScriptureBg,rounded corners,font=\small\bfseries,text=ChapterEmber,align=center] at (0,-1.7) {2:27 \ 你們必知道我是在以色列中間\\\textit{you will know that I am in the midst of Israel}};
  \node[font=\small\bfseries,text=ChapterEmber,align=center] at (0,-3.6) {3:17 \ 你們就知道……且又住在錫安\\\textit{you will know \ldots\ dwelling in Zion}};
\end{tikzpicture}

\vspace{0.8cm}

\begin{minipage}{4.6in}
\small\color{TextGray}
約珥書的動詞「知道」（ידע）只出現三次：第一次是一個問句，希伯來文「誰知道」（מִי יוֹדֵעַ）祂會不會回心轉意，和合本譯作「也未可知」（2:14）；後兩次是應許，「你們必知道」（2:27；3:17）。在問句與應許之間，是蝗蟲吃了又吃，然後是祂補還，是祂自己說：我是在以色列中間。災是祂的軍旅（2:11）、是祂打發的大軍隊（2:25），日子是祂的日子，所以「雖然如此」（2:12）的門也在祂手裏；全書最後一個詞組，是「耶和華住在錫安」（3:21）。
\end{minipage}

\vspace{0.5cm}
{\footnotesize\color{LightGray} 「你們必知道我是在以色列中間，又知道我是耶和華─你們的神」— 約珥書 2:27}
\end{center}
\cleardoublepage

'''

# ---- middle: copyright page, TOC, main matter up to $body$ (keep Jude's, with names changed) ----------------------
mid_start = rest.index("% Copyright page")
mid_end = rest.index("%% --------------------------------------------\n%% CLOSING COLOPHON")
mid = rest[mid_start:mid_end]
for a, b in [
    ("ChapterPurple", "ChapterEmber"),
    ("\\textbf{猶大書研讀 / Epistle of Jude Study}", "\\textbf{約珥書研讀 / The Book of Joel Study}"),
]:
    assert a in mid, a
    mid = mid.replace(a, b)

BACK = r'''%% --------------------------------------------
%% CLOSING COLOPHON — kept separate and short on purpose; appears
%% before the back cover so the back cover is the true final page
%% --------------------------------------------
\backmatter
\thispagestyle{empty}
\pagestyle{empty}
\vspace*{\fill}
\begin{center}
\coveremblem[ScriptureGold]

\vspace{0.5cm}

\fleuron\hspace{0.3cm}{\color{ScriptureGold}\rule{1.3in}{0.4pt}}\hspace{0.3cm}\fleuron

\vspace{1cm}

{\small\itshape\color{CommentaryBrown} ……因為耶和華住在錫安。}\\[0.4em]
{\baskervillefont\footnotesize\itshape\color{LightGray} “. . . for the LORD dwells in Zion.” — Joel 3:21}

\vspace{1.2cm}

{\itshape\normalsize\color{CommentaryBrown} 你看見耶穌了嗎？}\\[0.3em]
{\baskervillefont\itshape\small\color{LightGray} Have you seen Jesus?}

\vspace{1.4cm}

{\color{ScriptureGold}\rule{0.9in}{0.4pt}}

\vspace{0.5cm}

{\footnotesize\color{LightGray} Three Books Deep Reading \& Publishing}\\
{\footnotesize\color{LightGray} 三書精讀出版系統}

\vspace{0.3cm}

{\footnotesize\color{LightGray} Soli Deo Gloria — 唯獨榮耀神}
\end{center}
\vspace*{\fill}
\clearpage

%% --------------------------------------------
%% BACK COVER — full-bleed, light-on-dark, mirrors the front cover;
%% the true final page of the book
%% --------------------------------------------
\CoverBackground
\CoverBorder
\thispagestyle{empty}
\pagestyle{empty}
\color{CoverCream}
\vspace*{0.4cm}
\begin{center}
% One Hebrew word only: XeTeX scrambles space- or maqaf-joined RTL phrases.
{\Large\itshape\color{CoverGoldBright} שֹׁכֵן}\quad{\itshape\small\color{CoverMuted} {\baskervillefont “shokhen” — dwells} · 全書最後的動詞（3:17；3:21）}

\vspace{0.4cm}

\fleuron[CoverGoldBright]\hspace{0.25cm}{\color{CoverGoldBright}\rule{1.8in}{0.4pt}}\hspace{0.25cm}\fleuron[CoverGoldBright]

\vspace{0.4cm}

{\large\bfseries\color{CoverCream} 關於本書}\qquad{\baskervillefont\itshape\large\color{CoverGoldBright} About This Book}

\vspace{0.4cm}

\begin{minipage}{5in}
\small\color{CoverCream}
約珥書只有七十三節，卻把一場蝗災、一個軍隊、一個日子，全放在耶和華的手裏：蝗蟲是耶和華的「軍旅」（2:11），也是祂親口說「我打發到你們中間的大軍隊」（2:25）；「耶和華的日子」五次出現；而在審判還在行進的時候，祂說：「雖然如此」，一心歸向我（2:12）。本書分十章逐段研讀全卷，以「啟示的次序」為骨幹，整合老弟兄的查經方法、加爾文與馬太·亨利的歷代注疏、四位教父的引述、G. Campbell Morgan 的解經，以及 John MacArthur 論到約珥書的講道（gty.org）。每一句歸給注疏家的引文都附英文原文與出處，可以按圖索驥核對。

\vspace{0.3cm}

{\baskervillefont\color{CoverCream}\lettrine[lines=3,findent=2pt,nindent=2pt]{\color{CoverGoldBright}J}{}oel is seventy-three verses long, and it puts a locust plague, an army and a Day entirely in the hand of the LORD: the locusts are “His army” (2:11) and “My great army” (2:25); “the day of the LORD” occurs five times; and while the judgment is still on the march He says, “Yet even now,” return to Me with all your heart (2:12). This study reads the whole book in ten chapters built on the order of revelation, with Elder Wong's way of reading Scripture, the commentary of John Calvin and Matthew Henry, four of the Church Fathers, G. Campbell Morgan's exposition, and John MacArthur's preaching where he speaks of Joel (gty.org). Every quotation attributed to a commentator is given in its original English with a source a reader can check.}
\end{minipage}

\vspace{0.4cm}

{\small\bfseries\color{CoverCream} 五步：從話臨到到住在錫安}\qquad{\baskervillefont\itshape\small\color{CoverGoldBright} Five Movements}

\vspace{0.3cm}

\begin{minipage}{4.7in}
\small\color{CoverCream}
\begin{tabular}{@{}cp{3.4in}l@{}}
第一步 & 話先臨到，然後才有解釋 \textit{\baskervillefont\color{CoverCream} The Word comes first} & {\tiny\color{CoverMuted} 1:1-20}\\[0.25em]
第二步 & 日子臨近，軍隊是祂的 \textit{\baskervillefont\color{CoverCream} The Day is near; the army is His} & {\tiny\color{CoverMuted} 2:1-11}\\[0.25em]
第三步 & 雖然如此，祂先開口邀請 \textit{\baskervillefont\color{CoverCream} Yet even now, He invites first} & {\tiny\color{CoverMuted} 2:12-17}\\[0.25em]
第四步 & 祂回答：先補還，再澆灌 \textit{\baskervillefont\color{CoverCream} He answers: repays, then pours out} & {\tiny\color{CoverMuted} 2:18-32}\\[0.25em]
第五步 & 審判列國，住在錫安 \textit{\baskervillefont\color{CoverCream} The nations judged; the LORD dwells in Zion} & {\tiny\color{CoverMuted} 3:1-21}\\
\end{tabular}
\end{minipage}

\vspace{0.4cm}

{\color{CoverGoldBright}\rule{2.3in}{0.6pt}}

\vspace{0.25cm}

{\normalsize\itshape\color{CoverCream} 凡求告耶和華名的就必得救。}\\
{\baskervillefont\footnotesize\itshape\color{CoverMuted} “. . . whoever calls on the name of the LORD Will be delivered.” — Joel 2:32}

\vspace{0.25cm}

{\color{CoverGoldBright}\rule{2.3in}{0.6pt}}

\vspace{0.35cm}

{\footnotesize\color{CoverMuted} \S\ Joel Edition v1.0 \S\ 2026 \S}
\end{center}

\end{document}
'''

out = head + FRONT + mid + BACK
(ROOT / "templates/pdf/joel.latex").write_text(out)
print("wrote templates/pdf/joel.latex", len(out), "bytes;",
      "jude/Jude leftovers:", len(re.findall(r"Jude|猶大|ChapterPurple|PurpleDark", out)))

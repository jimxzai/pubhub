# 字體配置說明 / Font Configuration Reference

## macOS (使用此 PDF 推薦)

The macOS template uses **classical Chinese calligraphy fonts** built into the system:

| 字體 | 用途 | LaTeX 命令 |
|---|---|---|
| **宋體** Songti SC | 主要正文 (Body text) | `\rmfamily` (default) |
| **楷體** Kaiti SC | 強調、引文、紅字部分 (Emphasis, quotes, red letter Bible) | `\textit{...}` or `\textkai{...}` |
| **黑體** PingFang SC | 標題、無襯線 (Headers, sans-serif) | `\sffamily` |
| **行楷** STXingkai | 装飾性引文 (Decorative running script) | `\textxing{...}` |
| **仿宋** STFangsong | 詩歌、文學引文 (Poetry, literary quotes) | `\textfs{...}` |
| **黑體** Heiti SC | 強烈的章節標題 (Strong titles) | `\texthei{...}` |
| **華文楷體** STKaiti | 替代書法 (Alternative calligraphy) | `\stkaiti{...}` |

### 使用範例

```latex
正文用宋體：神愛世人。
\textkai{楷體強調：這就是永生。}
\textxing{行楷裝飾：認識主就是永生。}
\textfs{仿宋引用：道成了肉身，住在我們中間。}
\texthei{黑體標題：成了！}
```

### 紅字聖經 (Red Letter Bible)
耶穌的話語自動使用**楷體 + 紅色**，營造書法氣質：
```latex
\jesus{我就是道路、真理、生命。}
% Renders: 我就是道路、真理、生命。 (in Kaiti SC red italic)
```

---

## Linux / 其他系統

If `Songti SC` is not available (not on macOS), the build script automatically uses the Linux template with these substitutes:

| Font | Substitute |
|---|---|
| Songti SC → | DejaVu Serif (Latin) + Droid Sans Fallback (CJK) |
| Kaiti SC → | Droid Sans Fallback (no calligraphy variant available) |
| Menlo → | DejaVu Sans Mono |

To add proper calligraphy on Linux, install:
- **Noto Sans CJK** / **Noto Serif CJK** — modern Adobe/Google CJK fonts
- **AR PL UKai** (文鼎楷書 — 楷體)
- **AR PL UMing** (文鼎明體 — 宋體)
- **WenQuanYi** fonts (文泉驛)

```bash
# Ubuntu/Debian
sudo apt-get install fonts-noto-cjk fonts-arphic-ukai fonts-arphic-uming

# Then update the Linux template's \cjkfont, \kaiti definitions:
\setmainfont{Noto Serif CJK SC}
\newfontfamily\kaiti{AR PL UKai TW}
```

---

## 推薦的中文書法字體 / Recommended Chinese Calligraphy Fonts

| 字體 | 風格 | 適用 |
|---|---|---|
| **楷體** Kaiti | 端正書法 (Standard brush) | 引文、強調 |
| **顏體** Yan style (顏真卿) | 厚重 | 標題（少用）|
| **柳體** Liu style (柳公權) | 瘦勁 | 標題（少用）|
| **歐體** Ou style (歐陽詢) | 嚴謹 | 正式文件 |
| **趙體** Zhao style (趙孟頫) | 流暢 | 詩歌 |
| **行書** Xingshu | 流動的行書 | 装飾、書名 |
| **草書** Caoshu | 草書 | 极少使用 |

> 顏體、柳體 等古代書法家風格的字體在現代字庫中通常以「楷體」為基礎做變體，
> 如：方正顏體、漢儀柳楷、華文行楷等。

### 商業/免費字體建議

- **方正字庫** (FZ Type) — 商業字庫，含楷體、隸書、行書、草書
- **漢儀字庫** (HanYi) — 商業字庫，書法字體豐富
- **華文字庫** (STFonts) — macOS 內建，包含 STKaiti, STXingkai, STSong, STFangsong
- **思源宋體** (Source Han Serif / Noto Serif CJK) — Adobe/Google 開源
- **思源黑體** (Source Han Sans / Noto Sans CJK) — Adobe/Google 開源
- **文泉驛** (WenQuanYi) — 開源 GPL，含楷書

---

## 本卷的設計選擇

本卷《耶穌基督完整生平》(*The Complete Life of Jesus Christ*) 的字體設計：

**正文 (Body)**：使用**宋體** (Songti SC) — 端正、易讀、適合長時間閱讀經文。

**耶穌的話 (Red Letter)**：使用**楷體** (Kaiti SC) + 紅色 — 楷書如毛筆書寫，賦予基督的話語**書法氣質**和**神聖感**。

**標題 (Headers)**：使用**Songti Bold** + 禮儀色 — 經典而莊嚴。

**裝飾 (Decoration)**：適度使用**金色** (LiturgicalGold) 和**禮儀色彩**，呼應禮儀年的傳統色。

> "字體是讀者與經文之間的呼吸。好的字體讓神的話語自由地在心中流動。"

---

*版本：v2 · 日期：2026 年 5 月*

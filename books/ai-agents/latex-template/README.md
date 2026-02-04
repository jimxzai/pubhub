# The AI-Powered One-Person Company
## O'Reilly Style LaTeX Book Template

This template is based on [princefishthrower/dev-book-template](https://github.com/princefishthrower/dev-book-template), adapted for the book "The AI-Powered One-Person Company".

## Directory Structure

```
latex-template/
├── Book/
│   └── book.tex          # Main book content
├── Cover/
│   └── cover.tex         # Separate cover page
├── images/
│   └── cover-animal.png  # O'Reilly style animal illustration
├── output/               # Generated PDFs (gitignored)
├── scripts/
│   └── build-book.sh     # Build automation
├── Makefile              # Alternative build system
└── README.md             # This file
```

## Prerequisites

### macOS

```bash
# Install MacTeX (full LaTeX distribution)
brew install --cask mactex

# Install Ghostscript (for PDF merging)
brew install ghostscript

# Optional: Install Fira Code font for code listings
brew install --cask font-fira-code
```

### Ubuntu/Debian

```bash
# Install TeX Live
sudo apt-get install texlive-full

# Install Ghostscript
sudo apt-get install ghostscript
```

### Windows

1. Install [MiKTeX](https://miktex.org/download)
2. Install [Ghostscript](https://ghostscript.com/releases/gsdnld.html)

## Building the Book

### Using the build script (recommended)

```bash
./scripts/build-book.sh
```

This will:
1. Compile the main book (two passes for TOC)
2. Compile the cover (if image exists)
3. Merge them into a complete PDF
4. Clean up auxiliary files

### Using Make

```bash
# Build book only
make

# Full build with bibliography and index
make full

# Quick single-pass build
make quick

# Clean auxiliary files
make clean

# Open the PDF (macOS)
make open
```

### Manual build

```bash
cd Book
pdflatex book.tex
pdflatex book.tex  # Run twice for TOC
```

## Adding Content

### Chapter Structure

Each chapter follows this pattern:

```latex
\chapter{Chapter Title}

Introduction paragraph...

\section{First Section}

Content with code examples:

\begin{lstlisting}[style=python,caption={Description}]
def example():
    return "Hello, World!"
\end{lstlisting}

\section{Chapter Summary}

\begin{itemize}
    \item Key point 1
    \item Key point 2
\end{itemize}
```

### Callout Boxes

```latex
% Tip (green)
\begin{tip}
Pro tip content here.
\end{tip}

% Note (blue)
\begin{note}
Additional information here.
\end{note}

% Warning (orange)
\begin{warning}
Caution content here.
\end{warning}

% Agent Profile (red)
\begin{agentprofile}{EMMA --- Email Agent}
Agent description here.
\end{agentprofile}
```

### Code Listings

```latex
% Python (default)
\begin{lstlisting}[style=python,caption={Python example}]
import anthropic
client = anthropic.Anthropic()
\end{lstlisting}

% Bash (dark background)
\begin{lstlisting}[style=bash,caption={Shell command}]
pip install anthropic
\end{lstlisting}

% JSON
\begin{lstlisting}[style=json,caption={Configuration}]
{"model": "claude-sonnet-4-20250514"}
\end{lstlisting}
```

### Tables

```latex
\begin{table}[h]
\centering
\begin{tabular}{@{}lll@{}}
\toprule
\textbf{Column 1} & \textbf{Column 2} & \textbf{Column 3} \\
\midrule
Row 1 & Data & Data \\
Row 2 & Data & Data \\
\bottomrule
\end{tabular}
\caption{Table caption}
\end{table}
```

## Cover Image

Place your O'Reilly-style animal illustration at:

```
images/cover-animal.png
```

Recommended size: 1200x1600 pixels (3:4 ratio)

For generating an animal illustration, consider:
- [Midjourney](https://midjourney.com) with prompt like "detailed pencil sketch of a [animal], scientific illustration style, white background"
- Commission from an illustrator
- Use placeholder for development

## Customization

### Colors

Edit the color definitions in `Book/book.tex`:

```latex
\definecolor{oreilly-red}{HTML}{C1272D}
\definecolor{oreilly-dark}{HTML}{333333}
```

### Fonts

For XeLaTeX/LuaLaTeX users, uncomment the font section:

```latex
\setmainfont{Linux Libertine O}
\setsansfont{Linux Biolinum O}
\setmonofont{Fira Code}[Scale=0.85]
```

### Page Size

Default is US Letter. For A4, change:

```latex
\geometry{
    a4paper,
    ...
}
```

## Output Files

After building:

- `output/book.pdf` - Main book without cover
- `output/cover.pdf` - Cover page only
- `output/ai-one-person-company-complete.pdf` - Complete book with cover

## Troubleshooting

### "Package not found" errors

Install missing packages via your TeX distribution's package manager:
- macOS/MiKTeX: Usually auto-installs
- TeX Live: `tlmgr install <package-name>`

### TOC shows wrong page numbers

Run `pdflatex` twice (the build script does this automatically).

### Fonts not rendering correctly

Ensure you're using pdflatex (default) or install the required fonts for XeLaTeX/LuaLaTeX.

### Cover not building

Ensure `images/cover-animal.png` exists. The build script skips cover generation if the image is missing.

## Publishing to O'Reilly

If working with O'Reilly directly, they may prefer:
- **AsciiDoc** format (can convert from LaTeX)
- **HTMLBook** format
- Submission through **Atlas** platform

This LaTeX template is ideal for:
- Self-publishing
- Draft review
- Print-ready PDF generation

## Resources

- [O'Reilly Author Guidelines](https://www.oreilly.com/work-with-us.html)
- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)
- [TikZ Manual](https://tikz.dev/)
- [Original dev-book-template](https://github.com/princefishthrower/dev-book-template)

## License

Template structure based on dev-book-template. Content is copyright of the author.

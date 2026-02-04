# How to Compile "The AI Workforce" to PDF

## Option 1: Install MacTeX (Recommended)

Run these commands in Terminal:

```bash
# Install MacTeX (full version, ~4GB download)
brew install --cask mactex

# OR install BasicTeX (smaller, ~100MB)
brew install --cask basictex

# Restart terminal or run:
eval "$(/usr/libexec/path_helper)"

# Install required packages (if using BasicTeX)
sudo tlmgr update --self
sudo tlmgr install tcolorbox environ trimspaces collection-fontsrecommended parskip etoolbox

# Navigate to the template directory
cd /Users/jimxiao/Documents/GitHub/pubhub/books/ai-agents/latex-template

# Build the PDF
make
```

## Option 2: Use Overleaf (Online, No Installation)

1. Go to [Overleaf](https://www.overleaf.com)
2. Create a new project → "Upload Project"
3. Upload the entire `latex-template` folder as a ZIP
4. Click "Recompile" to generate PDF
5. Download the PDF

### To create the ZIP file:

```bash
cd /Users/jimxiao/Documents/GitHub/pubhub/books/ai-agents
zip -r ai-workforce-latex.zip latex-template/
```

## Option 3: Use Docker

```bash
# Pull TeXLive Docker image
docker pull texlive/texlive

# Build the book
cd /Users/jimxiao/Documents/GitHub/pubhub/books/ai-agents/latex-template
docker run --rm -v "$(pwd)":/workdir -w /workdir texlive/texlive \
    pdflatex -output-directory=output Book/book.tex
docker run --rm -v "$(pwd)":/workdir -w /workdir texlive/texlive \
    pdflatex -output-directory=output Book/book.tex
```

## After Building

The PDF will be at:
- `output/book.pdf` - Main book

## Current Status

✅ Title: **The AI Workforce**
✅ Subtitle: **Building Intelligent Agents for the One-Person Company**
✅ Author: **Jim Xiao**
✅ Template: O'Reilly style (dev-book-template)
⏳ Cover image: Add octopus illustration to `images/cover-animal.png`

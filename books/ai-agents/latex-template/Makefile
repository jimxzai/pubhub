# Makefile for The AI-Powered One-Person Company
# O'Reilly Style Book
# ============================================================

BOOK_DIR = Book
COVER_DIR = Cover
OUTPUT_DIR = output
MAIN = book

# Use pdflatex by default (change to xelatex or lualatex if needed)
LATEX = pdflatex
LATEX_FLAGS = -interaction=nonstopmode -output-directory=$(OUTPUT_DIR)

# Ghostscript for PDF merging
GS = gs
GS_FLAGS = -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite

.PHONY: all book cover complete quick clean distclean open help

# Default target
all: book

# Create output directory
$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

# Build main book (two passes for TOC)
book: $(OUTPUT_DIR)
	@echo "Building main book..."
	cd $(BOOK_DIR) && $(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	cd $(BOOK_DIR) && $(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	@echo "✓ Book compiled: $(OUTPUT_DIR)/$(MAIN).pdf"

# Build cover
cover: $(OUTPUT_DIR)
	@echo "Building cover..."
	cd $(COVER_DIR) && $(LATEX) $(LATEX_FLAGS) cover.tex
	cd $(COVER_DIR) && $(LATEX) $(LATEX_FLAGS) cover.tex
	@echo "✓ Cover compiled: $(OUTPUT_DIR)/cover.pdf"

# Complete book with cover merged
complete: book cover
	@echo "Merging cover and book..."
	$(GS) $(GS_FLAGS) \
		-sOutputFile=$(OUTPUT_DIR)/ai-one-person-company-complete.pdf \
		$(OUTPUT_DIR)/cover.pdf \
		$(OUTPUT_DIR)/$(MAIN).pdf
	@echo "✓ Complete book: $(OUTPUT_DIR)/ai-one-person-company-complete.pdf"

# Quick single-pass build (for iteration)
quick: $(OUTPUT_DIR)
	cd $(BOOK_DIR) && $(LATEX) $(LATEX_FLAGS) $(MAIN).tex

# Clean auxiliary files
clean:
	rm -f $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.toc
	rm -f $(OUTPUT_DIR)/*.out $(OUTPUT_DIR)/*.lof $(OUTPUT_DIR)/*.lot
	rm -f $(OUTPUT_DIR)/*.bbl $(OUTPUT_DIR)/*.blg
	rm -f $(OUTPUT_DIR)/*.idx $(OUTPUT_DIR)/*.ind $(OUTPUT_DIR)/*.ilg

# Clean everything including PDFs
distclean: clean
	rm -f $(OUTPUT_DIR)/*.pdf
	rmdir $(OUTPUT_DIR) 2>/dev/null || true

# Open PDF (macOS)
open: book
	open $(OUTPUT_DIR)/$(MAIN).pdf

# Watch for changes (requires fswatch)
watch:
	@echo "Watching for changes... (Ctrl+C to stop)"
	fswatch -o $(BOOK_DIR)/*.tex | xargs -n1 -I{} make quick

# Help
help:
	@echo "Available targets:"
	@echo "  make          - Build main book (default)"
	@echo "  make book     - Build main book"
	@echo "  make cover    - Build cover page"
	@echo "  make complete - Build and merge book with cover"
	@echo "  make quick    - Single-pass build (faster, for iteration)"
	@echo "  make clean    - Remove auxiliary files"
	@echo "  make distclean- Remove all generated files"
	@echo "  make open     - Build and open PDF (macOS)"
	@echo "  make watch    - Watch for changes and rebuild"
	@echo "  make help     - Show this help"

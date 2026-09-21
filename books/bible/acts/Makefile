SHELL := /bin/zsh

PYTHON ?= python3
PANDOC ?= pandoc
PDF_ENGINE ?= xelatex
CJK_FONT ?= STSong
MAIN_FONT ?= Arial Unicode MS

.PHONY: check release-check rights-audit pdf clean

check:
	$(PYTHON) scripts/validate_book.py

release-check:
	$(PYTHON) scripts/validate_book.py --strict

rights-audit:
	$(PYTHON) scripts/audit_rights.py

pdf:
	PANDOC="$(PANDOC)" PDF_ENGINE="$(PDF_ENGINE)" CJK_FONT="$(CJK_FONT)" MAIN_FONT="$(MAIN_FONT)" bash scripts/build_pdf.sh

clean:
	rm -rf .build dist

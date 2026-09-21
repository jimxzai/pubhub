PYTHON ?= python3

.PHONY: check citations scripture pdf pdf-audit epub html all clean release-check test

check:
	$(PYTHON) scripts/check_book.py
	$(PYTHON) scripts/lint-scripture-text.py
	$(PYTHON) scripts/gen-romans-scripture-index.py

citations:
	$(PYTHON) scripts/verify-citations.py
	$(PYTHON) scripts/quote_audit.py

test:
	$(PYTHON) -m unittest discover -s scripts -p 'test_*.py'

release-check: check citations test
	$(PYTHON) scripts/quote_audit.py --strict
	$(PYTHON) scripts/release_gate.py

scripture: check

pdf:
	$(PYTHON) scripts/build_book.py pdf

pdf-audit:
	$(PYTHON) scripts/audit_actual_pdf.py

epub: check
	$(PYTHON) scripts/build_book.py epub

html: check
	$(PYTHON) scripts/build_book.py html

all: pdf

clean:
	rm -rf build dist

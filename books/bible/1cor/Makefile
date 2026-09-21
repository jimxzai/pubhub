BUILD_DIR = build

.NOTPARALLEL:

.PHONY: verify html pdf epub clean all audit

verify:
	./scripts/verify_book.sh
	python3 scripts/validate_publication.py

html: verify
	python3 scripts/build_consolidated.py html

pdf: verify
	python3 scripts/build_consolidated.py pdf

epub: verify
	python3 scripts/build_consolidated.py epub

all: pdf html epub audit

audit:
	python3 scripts/audit_outputs.py

clean:
	rm -rf $(BUILD_DIR)

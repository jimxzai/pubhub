SHELL := /bin/zsh

ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
CONSOLIDATED_BUILDER := $(ROOT)../../../scripts/build-cor2-consolidated.sh

.PHONY: all validate links consolidated pdf epub release-check test clean

all: validate links test consolidated

test:
	python3 scripts/test_publishing.py

validate:
	./scripts/validate_book.sh

links:
	./scripts/check_links.sh

consolidated:
	$(CONSOLIDATED_BUILDER)

pdf epub: consolidated

release-check:
	./scripts/release_gate.sh

clean:
	rm -rf build dist

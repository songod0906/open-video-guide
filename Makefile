.PHONY: setup lint test check validate web context handoff

setup:
	python -m pip install -e ".[dev]"
	git config core.hooksPath .githooks
	python scripts/project_context.py

lint:
	python -m ruff check .
	python scripts/check_ste.py

test:
	python -m pytest

check: lint test validate

validate:
	ovg validate examples/example-guide.json
	python scripts/validate_benchmark.py

web:
	ovg-web

context:
	python scripts/project_context.py --print

handoff:
	python scripts/project_context.py --verify --print

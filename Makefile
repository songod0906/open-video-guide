.PHONY: setup lint test check validate

setup:
	python -m pip install -e ".[dev]"

lint:
	python -m ruff check .
	python scripts/check_ste.py

test:
	python -m pytest

check: lint test validate

validate:
	ovg validate examples/example-guide.json

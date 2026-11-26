.PHONY: check test lint format typecheck scripts

check: lint typecheck test scripts

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .

typecheck:
	uv run mypy

test:
	uv run pytest

scripts:
	uv run python scripts/check_file_length.py
	uv run python scripts/check_nested_loops.py src scripts
	uv run python scripts/check_gitignore_kiro.py

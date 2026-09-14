.PHONY: check

check:
	uv run --locked ruff format --check src tests
	uv run --locked ruff check src tests
	uv run --locked basedpyright
	uv run --locked mypy
	uv run --locked basedpyright --verifytypes reservations
	uv run --locked nasa lint src
	uv run --locked dddlint lint src
	uv run --locked testdesiderata tests
	uv run --locked mockbuster tests --strict
	uv run --locked lint-imports
	uv run --locked pytest --cov=reservations --cov-branch --cov-report=term-missing

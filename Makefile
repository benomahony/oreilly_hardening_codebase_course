.DEFAULT_GOAL := help
UV ?= uv
RUN = $(UV) run --locked

.PHONY: help setup check format lint types nasa ddd desiderata mocks architecture test docs demo solutions property mutation optimized

help:
	@echo 'make check       Run every passing quality gate'
	@echo 'make demo        Show and verify the deliberately broken examples'
	@echo 'make solutions   Check and execute the completed solutions'
	@echo 'make property    Run the Hypothesis properties'
	@echo 'make mutation    Run mutmut and reject unreviewed survivors'

setup:
	$(UV) sync --locked

check: lint types nasa ddd desiderata mocks architecture test optimized

format:
	$(RUN) ruff format src tests scripts solutions 
	$(RUN) ruff check src tests scripts solutions --fix

lint:
	$(RUN) ruff format --check src tests scripts solutions
	$(RUN) ruff check src tests scripts solutions

types:
	$(RUN) basedpyright
	$(RUN) mypy
	$(RUN) basedpyright --verifytypes reservations

nasa:
	$(RUN) nasa lint src

ddd:
	$(RUN) dddlint lint src

desiderata:
	$(RUN) testdesiderata tests

mocks:
	$(RUN) mockbuster tests --strict

architecture:
	$(RUN) lint-imports
	$(RUN) pytest tests/test_architecture.py -q

test:
	$(RUN) pytest --cov=reservations --cov-branch --cov-report=term-missing

docs:
	$(RUN) pytest tests/test_docs.py -q

demo:
	$(RUN) python -m scripts.demo

solutions:
	$(RUN) ruff check solutions
	$(RUN) ruff format --check solutions
	$(RUN) basedpyright
	$(RUN) nasa lint solutions/strict.py solutions/defensive.py solutions/ddd/reservations.py
	$(RUN) dddlint lint solutions/ddd --config solutions/ddd/dddlint.yaml
	$(RUN) testdesiderata solutions
	$(RUN) mockbuster solutions --strict
	$(RUN) pytest solutions tests/test_docs.py tests/test_architecture.py -q

property:
	$(RUN) pytest tests/test_properties.py -q

mutation:
	$(RUN) python -m scripts.mutation

optimized:
	$(RUN) python -O -m scripts.optimized_boundary

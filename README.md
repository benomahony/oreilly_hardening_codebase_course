# ChatOps: a worked example of hardening a codebase for agentic coding

A small, real command-parsing bot (`/task add`, `/task done <id>`, ...) —
the running example for every technique in
[Hardening Codebases for Agentic Coding](https://benomahony.com/blog/hardening-codebases-for-agentic-coding/).
Its error messages are built on Google's
[actionable Chat error messages](https://developers.google.com/workspace/chat/write-error-messages)
guidance, with a hands-on exercise for it in `exercises/`.

## Python-specific tools, language-agnostic ideas

Every tool named below is Python's implementation of a general idea. If
you're hardening a codebase in another language, port the idea, not the
tool:

| Idea | This codebase's tool (Python) |
|---|---|
| Static type checking at boundaries | Pydantic |
| Property-based fuzzing | Hypothesis |
| Dead-code / import / dependency hygiene | vulture, deptry |
| Assertion-density linting | nasa-lsp |
| Mock-usage banning | mockbuster |
| Format + lint | ruff |
| Static type checker | basedpyright |
| Security scanning | bandit |
| CLI guideline checking | cliqa |

## Quickstart

```bash
uv sync
uv run pytest                      # 85 tests, ~95% coverage
uv run chatops seed                # populate tasks.json with examples
uv run chatops list
uv run chatops handle "/task add Buy milk due 2026-08-20"
uv run chatops parse "/task frobnicate"   # see an actionable error
uv run pre-commit run --all-files  # the full static-analysis stack
```

## Technique → code map

| Technique | Where |
|---|---|
| Actionable error messages (Google Chat guidance) | `commons/errors.py` |
| Error collection pattern | `commons/errors.py::ErrorCollector` |
| Type safety with Pydantic models | `commons/models.py` |
| TypedDict for structured state (+ its tradeoff) | `commons/state.py` |
| Protocol classes for DI | `commons/protocols.py` |
| Defensive assertions (≥2 per function) | `engines/task_engine.py`, `engines/command_parser.py`, `engines/store.py` |
| Property-based fuzzing (Hypothesis) | `tests/property/` |
| Hypothesis testing profiles (`ci`/`dev`/`debug`/`fast`) | `tests/conftest.py` |
| pytest-examples for doc testing | `tests/doc/test_docs.py` |
| Architecture tests (AST-based) | `tests/architecture/test_layer_boundaries.py` |
| Test markers (unit/integration/architecture/property/doc) | `pyproject.toml` `[tool.pytest.ini_options]` |
| Pre-commit hook stack (ruff, basedpyright, vulture, bandit, deptry, mockbuster, cliqa, nasa-lsp) | `.pre-commit-config.yaml` |
| Fakes instead of mocks | `tests/fakes.py` |
| Modular layer architecture (`commons`/`engines`) | `src/oreilly_hardening_codebase_course/` |
| Dependency injection | `engines/task_engine.py::TaskEngine.__init__` |
| Contract specifications | `docs/contracts/task_command_contract.md` |
| Executable runbooks | `docs/runbooks/recover_corrupted_store.md` |
| Rich console logging | `cli.py` |
| Structured metrics collection | `commons/metrics.py` |
| CLI as a debug interface | `cli.py` (`parse`, `handle`, `list`, `seed`, `reset`) |
| Configuration loading with schema validation | `commons/config.py` |
| Coverage enforcement (80% floor) | `pyproject.toml` `[tool.coverage.report]` |

## Findings and exercises

Every technique has a real finding attached to it — a bug it caught, or a
constructed-and-verified before/after. `docs/workshop.md` has all of them,
each one reproducible yourself (break it, run the tool, observe, revert),
starting with actionable error messages.

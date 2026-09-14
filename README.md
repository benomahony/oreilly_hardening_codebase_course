# Hardening a Python codebase

One tiny stock counter. Every quality gate demonstrated with a broken example
and a checked solution. The application is three functions, about 40 executable
lines: parse a bounded request, reserve units, and reserve a batch.

## Start here

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```sh
uv sync --locked
make check
make demo
make solutions
```

`check` proves the finished application passes. `demo` verifies the broken
examples fail for the expected reason. `solutions` checks and runs the answers.
No database, web server, credentials, or paid AI service is required.

**[Presenter walkthrough](docs/demo.md)** · **[Exercises](exercises/README.md)** ·
**[Solutions](solutions/README.md)**

## What is demonstrated

| Topic | Tool | Focus |
|---|---|---|
| Formatting and linting | Ruff, all rules selected | Consistent code; zero findings |
| Strict types | basedpyright `all`, mypy `strict` | No Any escapes; 100% known public types |
| Defensive coding | NASA-LSP | All 12 shipped diagnostics; meaningful runtime assertions |
| Domain language | dddlint | Forbidden names, canonical terms, duplicates |
| Test quality | testdesiderata | All ten static categories; discussion of the two AI categories |
| Mock detection | mockbuster `--strict` | Real behavior in tests |
| Property-based testing | Hypothesis | Generated inputs, invariants, shrinking a real assertion failure |
| Fuzzing | Portable corpus mutation; Atheris on Linux | Untrusted bytes; assertion failures remain visible |
| Architecture tests | import-linter and pytest/grimp | Dependencies point toward the domain |
| Documentation tests | pytest-examples | Execute code blocks and verify printed output |
| Executable ADRs | pytest-examples | Architecture decisions expressed as tested examples |
| Mutation testing | mutmut | Expose a missed boundary despite 100% coverage |

## Individual lessons

```sh
uv run python -m scripts.demo NASA05-isinstance --verbose
uv run python -m scripts.demo hypothesis --verbose
make property
make fuzz
make mutation
```

All Python dependencies are locked in `uv.lock`; use Python 3.12, which uv installs
if needed. The first dddlint run downloads its Python parser. The pinned Atheris
wheel runs on Linux x86_64 via `make fuzz-atheris` and GitHub Actions; `make fuzz`
works on macOS and Linux. The portable fuzzer is seeded mutation, not coverage-guided.

Strict type checking and 100% type completeness measure static type coverage,
not proof of runtime correctness. Boundary exceptions, assertions, and tests
provide separate checks. See [scope and limits](docs/scope.md), including the
original NASA rules and every intentional lint exception.

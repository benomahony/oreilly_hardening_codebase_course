# Hardening a Python codebase

One stock counter: reserve three units from ten and seven remain.
Each lesson follows the same loop: **open a broken example → run the tool →
compare with the working code**.

## Set up

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run
these commands from the repository root:

```sh
uv sync --locked
make check
```

`make check` runs the checks on the finished code and tests. It should pass.
Python 3.12 and the tools are pinned in `uv.lock`; the first dddlint run also
downloads its Python parser. No services or credentials are needed.

## Start with one failure

Open [the broken reservation](examples/assertions/test_off_by_one.py).
It subtracts the requested stock but mistakenly adds one back. Run:

```sh
uv run pytest examples/assertions/test_off_by_one.py -q
```

Watch Hypothesis find the smallest counterexample: one unit requested from one
unit available. The conservation assertion fails. Compare the calculation with
[the working version](src/reservations/domain/stock.py), then run its properties:

```sh
uv run pytest tests/test_properties.py -q
```

The same property now passes. To make this an exercise, fix a scratch copy of the
broken example and rerun it. Keep the original so the demonstration is repeatable.

## Show the other ideas

Run each command separately from the repository root. These examples are
deliberately broken: read the diagnostic shown in the last column.

| Idea | Command | What it catches |
|---|---|---|
| Formatting | `uv run ruff format --check examples/quality/formatting.py` | Inconsistent formatting |
| Linting | `uv run ruff check examples/quality/linting.py` | Unused import, bare exception, missing types |
| Types | `uv run basedpyright --project examples/types` | Wrong arguments and unsafe type escapes |
| Meaningful assertions | `uv run nasa lint examples/nasa/NASA05-isinstance.py` | An assertion that only repeats a type |
| Domain language | `(cd examples/ddd && uv run dddlint lint .)` | Vague names, aliases, duplicate definitions |
| Test quality | `uv run testdesiderata examples/desiderata/test_bhv001.py` | A test that checks an invented mock result |
| Mocks | `uv run mockbuster examples/mocks --strict` | Mocked behavior in tests |
| Architecture | `PYTHONPATH=examples/architecture uv run lint-imports --config examples/architecture/pyproject.toml` | A domain import from infrastructure |
| Documentation | `uv run pytest examples/docs/test_stale_docs.py -q` | A code example claiming ten minus three is eight |

Compare code fixes with [the domain](src/reservations/domain/stock.py) and
[batch calculation](src/reservations/application/reservations.py); test fixes with
[domain tests](tests/test_domain.py) and [real request tests](tests/test_infrastructure.py).
The other NASA and test-quality snippets can be run with the same tools.

The [usage guide](docs/usage.md) and [design decisions](docs/adr/) are executable
examples too: `uv run pytest tests/test_docs.py -q` checks them. Change the valid
batch in ADR 002 from 32 items to 33 to see its boundary check fail, then restore it.

## Show why coverage is not enough

The [mutation example](examples/mutation/test_weak_suite.py) changes a valid-stock
guard from `>= 0` to `> 0`. A test using positive stock misses it; zero exposes it:

```sh
uv run pytest examples/mutation/test_weak_suite.py -k positive -q
uv run pytest examples/mutation/test_weak_suite.py -k zero -q
```

The first passes and the second fails. The regression belongs in
[the application tests](tests/test_application.py), alongside the other boundaries.
To have a tool make these changes automatically:

```sh
uv run mutmut run
uv run mutmut results
```

Inspect surviving changes with `uv run mutmut browse`. Some reveal missing tests;
others are equivalent, such as changes to unreachable assertion messages.
Mutation results are for discussion and review, outside `make check`.

## Where things live

- `src/`: the working application and code answers.
- `tests/`: the passing tests and test-writing answers.
- `examples/`: small, deliberately broken snippets.
- `docs/`: executable usage and design decisions, plus [tool scope and limits](docs/scope.md).

# Presenter walkthrough

The audience only needs to understand `10 - 3 = 7`. Show
`src/reservations/domain/stock.py` first. This is also the answer to the broken
examples; the application and tests are checked together with `make check`.

## 1. Establish green

Run `make check`. Show strict configuration in `pyproject.toml`: Ruff `ALL`,
basedpyright `all`, mypy `strict`, warnings as errors, 100% branch coverage,
and no disabled NASA or Test Desiderata rules.

## 2. Show the static gates

Use the direct tool commands in the [README](../README.md). Start with
formatting, linting, and types, then `NASA05-isinstance`, `NASA05-constant-assert`,
`NASA02`, and domain language. The README links to the working answers.
The [exercise guide](exercises.md) maps every lesson to its example and fix.

Every NASA diagnostic has its own small example. Run one with
`uv run nasa lint examples/nasa/NASA02.py` and read the reported diagnostic.

## 3. Show test quality

Run Mockbuster on `examples/mocks` and Test Desiderata on the `BHV001`,
`STR001`, and `SPC003` examples, using the commands in the README. The mocked test invents the answer;
`tests/test_infrastructure.py` exercises the real request path and checks remaining
stock. Each of the ten static Test Desiderata categories has an example;
`tests/test_domain.py` demonstrates the corrected testing practices.

## 4. Generate a counterexample

Run `uv run pytest examples/assertions/test_off_by_one.py -q`. A deliberate `+ 1` bug
trips the stock conservation assertion. Hypothesis shrinks the failure to one
requested unit. Show the correct calculation in `src/reservations/domain/stock.py`
and the minimal regression in `tests/test_domain.py`, then run `uv run pytest tests/test_properties.py -q`.
The properties cover conservation, invalid internal states, and arbitrary bytes
at the input boundary.

## 5. Test architecture and the explanations

Run the architecture command from the README: an import from the domain to infrastructure violates
the layer contract. `uv run lint-imports` checks the corrected source.

Run `uv run pytest examples/docs/test_stale_docs.py -q`: the prose claims eight units remain, and pytest-examples
shows the actual seven. `uv run pytest tests/test_docs.py -q` checks `docs/usage.md` and executes both ADRs
in `docs/adr/` using the same library.

## 6. Challenge the tests themselves

Run the two mutation-example tests from the README, then `uv run mutmut run`. The first development run had full
line and branch coverage but missed `reserve_batch(0, ())`. Mutmut changed `>= 0`
to `> 0` and the mutation survived. The answer is the explicit zero-stock test in
`tests/test_application.py`. See [the mutation lesson](mutation.md) for the measured
results and individual survivor reviews.

## Reset and offline use

The demo never edits the passing application. Broken files are isolated under
`examples/`. Commands print their diagnostics directly. Re-running an example is
the reset. Before going offline, run `uv sync --locked` and `make check`
once to populate package and parser caches.

For editor diagnostics, start `uv run nasa serve` and `uv run dddlint lsp` using
your editor's generic LSP client; Ruff and basedpyright have their own clients.
The terminal demo uses the same NASA analyzer and requires no editor extension.

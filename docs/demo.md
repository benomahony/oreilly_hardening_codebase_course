# Presenter walkthrough

The audience only needs to understand `10 - 3 = 7`. Show `src/reservations/domain/stock.py`
first. The extra folders hold the lessons, not a larger application.

## 1. Establish green (2 minutes)

Run `make check`. Show strict configuration in `pyproject.toml`: Ruff `ALL`,
basedpyright `all`, mypy `strict`, warnings as errors, 100% branch coverage,
and no disabled NASA or Test Desiderata rules.

## 2. Show the static gates (5 minutes)

Run each scene with `uv run python -m scripts.demo NAME --verbose`:

| NAME | What to show | Answer |
|---|---|---|
| `format` | Inconsistent formatting | `solutions/strict.py` |
| `lint` | Unused import, bare except, missing annotations | `solutions/strict.py` |
| `types` | Wrong arguments, Optional, wrong return, Any, missing annotations | `solutions/strict.py` |
| `NASA05-isinstance` | An assertion that only repeats a type | `solutions/defensive.py` |
| `NASA05-constant-assert` | Padding the assertion count | `solutions/defensive.py` |
| `NASA02` | Open-ended work | `solutions/defensive.py::reserve_batch` |
| `ddd` | StockManager, booking, duplicate reservation | `solutions/ddd/reservations.py` |

Every NASA diagnostic has its own named scene. `make demo` runs them all and
checks the exact diagnostic code, so a tool crash cannot masquerade as a success.

## 3. Show test quality (3 minutes)

Run `mocks`, `BHV001`, `STR001`, and `SPC003`. The mocked test invents the answer;
the solution exercises the real request path and checks remaining stock. Each
of the ten static Test Desiderata categories has a scene. The answers live in
`solutions/test_desiderata.py` and `solutions/test_mock_free.py`.

## 4. Generate a counterexample (3 minutes)

Run `hypothesis --verbose`. A deliberate `+ 1` bug trips the stock conservation
assertion. Hypothesis shrinks the failure to one requested unit. Show the actual
implementation fix in `solutions/defensive.py`, then run `make solutions`.

Run `make property` to exercise valid conservation laws and generated invalid
states. Run `fuzz --verbose` to show bytes reaching a failing invariant, then
`make fuzz` to exercise the corrected implementation with 10,008 inputs.
`make fuzz-atheris` adds coverage guidance on Linux.

## 5. Test architecture and the explanations (3 minutes)

Run `architecture --verbose`: an import from the domain to infrastructure violates
the layer contract. `make architecture` checks the corrected source.

Run `docs --verbose`: the prose claims eight units remain, and pytest-examples
shows the actual seven. `make docs` checks the corrected example and executes both
ADRs in `docs/adr/` using that same library. These are living design decisions,
not another documentation mechanism.

## 6. Challenge the tests themselves (3 minutes)

Run `make mutation`. The first development run had full line and branch coverage
but missed `reserve_batch(0, ())`. Mutmut changed `>= 0` to `> 0` and the mutation
survived. The solution is the explicit zero-stock test in `tests/test_application.py`.
See `docs/mutation.md` for the measured results and the individual survivor reviews.

## Reset and offline use

The demo never edits the passing application. Broken files are isolated under
`examples/broken/`, and each command logs its output in `reports/demo/`. Re-running
a scene is the reset. Before going offline, run `uv sync --locked` and `make check`
once to populate package and parser caches.

For editor diagnostics, start `uv run nasa serve` and `uv run dddlint lsp` using
your editor's generic LSP client; Ruff and basedpyright have their own clients.
The terminal demo uses the same NASA analyzer and requires no editor extension.

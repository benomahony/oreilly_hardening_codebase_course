# Hardening a Python codebase

**Run a file → see the failure → fix that file → run it again → green.**
Each teaching example contains its own checks and launches pytest when run.

## Start presenting

From the repository root, install the tools once:

```sh
uv sync --locked
```

Then open and run [the reservation example](examples/assertions/test_off_by_one.py):

```sh
uv run examples/assertions/test_off_by_one.py
```

An accidental `+ 1` makes the conservation assertion fail. Hypothesis finds the
smallest counterexample: one unit requested from one unit available. Remove the
`+ 1` and run **the same command** again. The test turns green. If the file is
already fixed, add `+ 1` to set up the demonstration. Undo your live edit to reset.

## Pick the next example

Every row uses the same command: `uv run FILE`. The instruction at the top of the
file says what to fix. Edit the indicated code or test; leave its checker and
launcher intact.

| Idea | File | Live fix |
|---|---|---|
| Formatting | `examples/quality/formatting.py` | Correct spacing and indentation |
| Linting | `examples/quality/linting.py` | Remove the unused import; add types and a docstring; fix exception handling |
| Types | `examples/types/violations.py` | Change the stock from a string to an integer |
| Meaningful assertions | `examples/nasa/NASA05-isinstance.py` | Replace the type check with meaningful business invariants |
| Domain language | `examples/ddd/vocabulary.py` | Use reservation names and remove duplicate definitions |
| Test quality | `examples/desiderata/test_bhv001.py` | Check real behavior instead of an invented mock result |
| Mocks | `examples/mocks/test_mocks.py` | Replace the mock with the real function and remove its import |
| Architecture | `examples/architecture/bad_reservations/domain.py` | Remove the infrastructure import and print call |
| Documentation | `examples/docs/test_stale_docs.py` | Change the expected output in the docstring from eight to seven |
| Mutation | `examples/mutation/test_weak_suite.py` | Change the stock guard from `> 0` to `>= 0` |

The other NASA and Test Desiderata files work the same way. Checks about code
quality call the real analyzer from a test inside the file. Test-quality checks
run first, so deliberately slow or interactive tests stop before executing.

For example, the mutation lesson shows a weak test passing and a boundary test
failing in one run. Fix the guard, rerun the file, and both pass.

## The finished application

`src/` and `tests/` hold the complete working stock counter. `make check` runs its
strict quality checks and tests; CI runs the same command. This is separate from
the deliberately broken teaching examples.

For a deeper mutation demonstration, run `uv run mutmut run`, then
`uv run mutmut results`. Review survivors with `uv run mutmut browse`.

Python 3.12 and the tools are locked. The first dddlint run downloads its parser.
No services or credentials are needed. [Scope and limits](docs/scope.md) explain
what the checks establish; [usage](docs/usage.md) and [design decisions](docs/adr/)
are also tested as part of the finished application.

# Exercises

Read a broken example, predict the failure, run its scene, then implement the fix
in a scratch copy. The completed answers are under `solutions/`; use `make solutions`
to check them. Keep the original failure fixtures intact so the live demo remains repeatable.

| Exercise | Broken example | Run | Passing solution |
|---|---|---|---|
| 1. Format and lint | `examples/broken/quality/` | `format`, `lint` | `solutions/strict.py` |
| 2. Close type escapes | `examples/broken/types/violations.py` | `types` | `solutions/strict.py` |
| 3. Meaningful contracts | `examples/broken/nasa/` | Any NASA rule code | `solutions/defensive.py` |
| 4. Use the domain language | `examples/broken/ddd/vocabulary.py` | `ddd` | `solutions/ddd/reservations.py` |
| 5. Improve the tests | `examples/broken/desiderata/` | The rule ID in each filename | `solutions/test_desiderata.py` |
| 6. Remove invented behavior | `examples/broken/mocks/test_mocks.py` | `mocks` | `solutions/test_mock_free.py` |
| 7. Find and shrink a bug | `examples/broken/assertions/test_off_by_one.py` | `hypothesis` | `solutions/defensive.py`, `solutions/test_properties.py` |
| 8. Fuzz into an invariant | `examples/broken/fuzz/off_by_one.py` | `fuzz` | `solutions/defensive.py`; passing `make fuzz` |
| 9. Enforce dependencies | `examples/broken/architecture/` | `architecture` | `solutions/architecture.md`, `src/reservations/` |
| 10. Repair stale docs | `examples/broken/docs/stale.md` | `docs` | `solutions/docs/updated.md` |
| 11. Make an ADR executable | `docs/adr/002-bounded-validated-input.md` | `make docs` | Change its valid boundary from 32 to 33 and observe failure, then restore it |
| 12. Strengthen a weak suite | `docs/mutation.md` | `make mutation` | `tests/test_application.py::test_empty_batch_accepts_zero_stock` |

For a named scene use `uv run python -m scripts.demo NAME --verbose`.

Discussion: which tests would keep passing after a harmless internal refactor?
Which invariants are meaningful at runtime? Which surviving mutations are
equivalent, and which expose missing tests? Why is a complete type annotation
score insufficient to establish correctness?

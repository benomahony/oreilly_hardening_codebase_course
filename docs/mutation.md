# What mutation testing found

The initial suite executed every production statement and branch, yet mutmut
found a missed boundary: `reserve_batch(0, ())`. Changing `available >= 0` to
`available > 0` survived because the empty-batch test only used positive stock.

Run the reconstructed weak test:

```sh
uv run pytest examples/mutation/test_weak_suite.py::test_positive_stock_misses_the_boundary -q
uv run pytest examples/mutation/test_weak_suite.py::test_zero_stock_exposes_the_survivor -q
```

The first test passes against the bad guard; the second exposes it. The regression
in `tests/test_application.py::test_empty_batch_accepts_zero_stock` is the answer;
mutmut checks the production implementation against that same test.

## Run the tool directly

`uv run mutmut run` mutates all three production modules. Read the results with
`uv run mutmut results` and inspect survivors with `uv run mutmut browse`.
This is a teaching exercise with manual review, outside `make check` and CI.

The earlier survivor reviews are retained in `mutation-survivors.tsv`. The hashes
identify the exact diffs reviewed at that time; they no longer drive a custom
approval gate. Review current survivors on their behavior. No production line is
excluded from mutation.

The remaining equivalent cases alter postcondition messages that cannot be
reached while the computation is unchanged, or relax a positivity assertion to
allow zero after a grammar that has already rejected zero. We keep those
postconditions because they detect future implementation bugs. We do not mock
internal operations or invent impossible inputs to inflate the mutation score.

Run `uv run mutmut results` to inspect survivors, `uv run mutmut show IDENTIFIER`
for a diff, and `uv run mutmut browse` for the interactive view. Do not call reviewed equivalents “killed.”
The [verification note](verification.md) records the last local checks.

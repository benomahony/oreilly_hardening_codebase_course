# What mutation testing found

The initial suite executed every production statement and branch, yet mutmut
found a missed boundary: `reserve_batch(0, ())`. Changing `available >= 0` to
`available > 0` survived because the empty-batch test only used positive stock.

Run the reconstructed weak test:

```sh
uv run pytest examples/broken/mutation/test_weak_suite.py::test_positive_stock_misses_the_boundary -q
uv run python -m scripts.demo mutation --verbose
```

The first test passes against the bad guard; the second exposes it. The completed
solution is `solutions/test_mutation.py`. The same regression is included in
`tests/test_application.py::test_empty_batch_accepts_zero_stock` so mutmut tests
the production implementation against it.

## The gate

`make mutation` runs the real mutmut tool against all three production modules.
It starts with a fresh disposable `mutants/` directory so added tests cannot be
hidden by stale mutation results. It requires a nonempty result set and rejects
unreviewed survivors, timeouts, missing tests, and incomplete results.

Survivors are reviewed individually in `mutation-survivors.tsv`. Each exemption
contains the SHA-256 of the **exact mutation diff**, its identifier, and its
reason. A different behavior change cannot pass merely because it reuses a
previously reviewed mutant number. No production line is excluded from mutation.

The remaining equivalent cases alter postcondition messages that cannot be
reached while the computation is unchanged, or relax a positivity assertion to
allow zero after a grammar that has already rejected zero. We keep those
postconditions because they detect future implementation bugs. We do not mock
internal operations or invent impossible inputs to inflate the mutation score.

Run `uv run mutmut results` to inspect survivors, `uv run mutmut show IDENTIFIER`
for a diff, and `uv run mutmut browse` for the interactive view. The measured
raw score is in `mutants/mutmut-cicd-stats.json`; do not call reviewed equivalents
“killed.” `docs/verification.md` records the final checked result.

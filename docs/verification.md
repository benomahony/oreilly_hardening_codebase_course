# Verification

Checked locally on macOS on 14 September 2026 with Python 3.12.1 and `uv.lock`.

| Check | Result |
|---|---|
| Direct example execution | All 31 teaching files execute their embedded checks with `uv run FILE` |
| Before and after the fix | Every intended failure was observed; all 31 corrected copies passed without changing their tests |
| `make check` | All application quality checks passed |
| Main pytest suite | 54 passed, including five executable documentation examples |
| Production coverage | 100% statements and branches: 41 statements, 8 branches |
| Public type completeness | 100%: 7 known exported symbols |

Corrected examples were checked in disposable copies outside the course, preserving
live edits in the repository. The old NASA filename-index test was removed after
its type-stub dependency was removed; each NASA lesson now checks its actual code.

The preceding mutation run found 77 mutants: 64 killed and 13 survived, a raw score
of 83.1%. Production source and application tests are unchanged by this update.
The prior reviews remain in [the mutation notes](mutation.md) and
[review list](mutation-survivors.tsv); review new survivors on their behavior.

CI runs `make check`. Teaching examples run directly using the
[README instructions](../README.md). The Linux workflow has not been rerun for
these local changes; remote history is in
[GitHub Actions](https://github.com/benomahony/oreilly_hardening_codebase_course/actions).

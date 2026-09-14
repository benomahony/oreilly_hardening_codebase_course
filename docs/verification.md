# Verification

Checked locally on macOS on 14 September 2026 with Python 3.12.1 and `uv.lock`.
The course now uses native tool commands, with `make check` as its single shortcut.

| Check | Result |
|---|---|
| `make check` | All formatting, linting, typing, NASA, DDD, test-quality, mock, architecture, and test checks passed |
| Main pytest suite | 55 passed, including five executable documentation examples |
| Production coverage | 100% statements and branches: 41 statements, 8 branches |
| Public type completeness | 100%: 7 known exported symbols |
| `uv run mutmut run` | 77 mutants: 64 killed, 13 survived |

The eight removed test cases checked the old runner's answer-path map. The
application tests, properties, and architecture tests remain in the suite.

The raw mutation score is **83.1%**. The prior equivalent-survivor reviews remain
in [the mutation notes](mutation.md) and [review list](mutation-survivors.tsv).
Review current survivors manually; no custom runner approves them automatically.

CI runs `make check`. Failure demonstrations and mutation review are run directly
using the [README commands](../README.md). The Linux workflow has not been rerun
for these local changes; remote history is in
[GitHub Actions](https://github.com/benomahony/oreilly_hardening_codebase_course/actions).

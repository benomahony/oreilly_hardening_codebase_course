# Verified results

Checked on 14 September 2026 with the committed lockfile, Python 3.12, and the
commands shown in the README.

| Command / check | Result |
|---|---|
| `make check` | Passed all formatting, linting, typing, NASA, DDD, test-quality, mock, architecture, and runtime-validation gates |
| Main pytest suite | 64 passed |
| Production coverage | 100% statements and branches: 41 statements, 8 branches |
| Public type completeness | 100%: 7 known exported symbols, none unknown or ambiguous |
| `make demo` | 32 of 32 intended failure demonstrations verified |
| `make solutions` | All solution checks passed; 15 selected tests passed |
| `make fuzz` | 10,008 inputs; 236 accepted, 9,772 rejected; no crashes |
| `make mutation` | 77 mutants: 64 killed, 13 individually reviewed equivalents; no missing tests or timeouts |

The raw mutation score is **83.1%**, not 100%. Twelve survivors change unreachable
postcondition error text, and one relaxes a guard behind stricter input validation.
See `mutation.md` and `mutation-survivors.tsv` for the review and the missing
boundary test found during development.

The Linux workflow runs the same course commands, an independent mutation job,
and the optional Atheris smoke test. Current run evidence is in
[GitHub Actions](https://github.com/benomahony/oreilly_hardening_codebase_course/actions).

Generated diagnostic logs live in `reports/demo/`; mutation statistics are in
`mutants/mutmut-cicd-stats.json`. Both are CI artifacts and deliberately excluded
from the source tree.

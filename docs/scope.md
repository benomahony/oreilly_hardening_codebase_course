# Scope, strictness, and limits

## What “strict” means here

Ruff selects `ALL`. The exceptions are `S101` (this lesson deliberately uses
assertions), formatter conflicts `COM812`/`ISC001`, and the mutually exclusive
docstring conventions `D203`/`D213`. Tests may use literal expected values
(`PLR2004`). Two command runners have local subprocess annotations explaining
their fixed repository-owned argument lists; the seeded portable fuzzer has a
local `S311` annotation because its randomness is for reproducibility.

basedpyright uses `all` on production, tests, solutions, and command scripts.
Mypy checks production with `strict` plus all-Any prohibitions and unreachable
code diagnostics. The installed package has a `py.typed` marker and must pass
`basedpyright --verifytypes reservations` with all public symbols known.
These checks do not prove program correctness or prevent an untyped Python
caller from violating an internal contract.

The optional Atheris entry point receives the same strict type check in its
Linux job, where Atheris is installed. `typings/` describes only the small API
surface used from Atheris and NASA-LSP, which lack complete package type markers.

NASA checks every production function with all rules enabled. Tests and the
course's command harness have different concerns, so the NASA invocation targets
`src/`. Each production assertion describes an internal precondition or a
postcondition. Input validation raises `ValueError` explicitly and remains active
under `python -O`, verified by `make optimized`. The normal application and test
runs require assertions enabled.

All ten static Test Desiderata categories are active; WRT/INS require the tool's
optional AI service and remain a discussion rather than an undisclosed dependency.
Mockbuster uses every detection category and `--strict`, with no baseline.

The broken examples are deliberately excluded from the passing static pipeline.
The demo invokes their tools explicitly and requires exit code 1 **and** the
expected diagnostic. Syntax errors, missing commands, and unrelated crashes
cannot count as successful demonstrations. Ruff, basedpyright and the solution
tests still check the completed answers.

## All ten NASA rules, honestly mapped

The [original Power of Ten](https://spinroot.com/gerard/pdf/P10.pdf) targets C.
[NASA-LSP](https://github.com/benomahony/NASA-LSP) is a Python adaptation, not a
proof of all ten original rules or NASA certification.

| Original rule | Demonstration and limitation |
|---|---|
| 1. Simple control flow, no recursion | NASA01 detects direct recursion and named dynamic APIs. It does not prove absence of indirect recursion. |
| 2. Fixed loop bounds | NASA02 catches `while True`; the application separately caps a tuple at 32. NASA-LSP does not prove all loop bounds. |
| 3. No post-initialization allocation | Not implemented by NASA-LSP; Python allocates dynamically. Input and batch bounds limit this example's work, not its entire heap. |
| 4. Short functions | NASA04 has an explicit 61-line failure fixture and small corrected functions. |
| 5. Meaningful assertions | NASA05 plus seven assertion-quality diagnostics; Hypothesis and fuzzing reach invariant failures. |
| 6. Minimal scope | Local variables, immutable inputs, no shared mutable application state; no general NASA-LSP scope proof. |
| 7. Check parameters and results | Boundary validation and meaningful use of returned values; basedpyright reports discarded non-None calls. Ruff B018 alone does not enforce this rule. |
| 8. Restrict preprocessor | Python has no C preprocessor; NASA01 restricts certain dynamic APIs. |
| 9. Restrict pointers | No direct C-pointer equivalent in this pure Python example; not an automated pointer proof. |
| 10. All warnings and analysis | Strict type/lint pipeline and pytest warnings as errors in CI. |

## Primary tool references

- [Ruff configuration](https://docs.astral.sh/ruff/configuration/)
- [Basedpyright typed libraries](https://docs.basedpyright.com/latest/usage/typed-libraries/)
- [NASA-LSP rules](https://github.com/benomahony/NASA-LSP/blob/main/docs/rules.md)
- [DDD lint](https://github.com/benomahony/dddlint)
- [Test Desiderata rule reference](https://github.com/benomahony/testdesiderata/blob/main/docs/rules.md)
- [Mockbuster](https://github.com/benomahony/mockbuster)
- [Hypothesis](https://hypothesis.readthedocs.io/en/latest/)
- [Atheris](https://github.com/google/atheris)
- [Import-linter](https://import-linter.readthedocs.io/)
- [pytest-examples](https://github.com/pydantic/pytest-examples)
- [mutmut](https://mutmut.readthedocs.io/en/latest/)

# Scope and limits

`make check` runs strict checks on the working application and tests. Ruff selects
`ALL`; exceptions are assertions (`S101`), formatter conflicts (`COM812`/`ISC001`),
docstring convention conflicts (`D203`/`D213`), and literal test values (`PLR2004`).
basedpyright uses `all`; mypy uses `strict` plus the explicit Any prohibitions.
Public type completeness and statement/branch coverage must both reach 100%.
Neither proves runtime correctness.

NASA-LSP uses all its rules on `src/`. The assertions express internal contracts;
external input is validated with explicit exceptions. To see validation remain
active when Python removes assertions, run this from the repository root:

```sh
uv run python -O -c "from reservations.infrastructure.wire import parse_reservations; parse_reservations(b'0')"
```

It raises `ValueError`. Run the regular application tests without `-O` so internal
assertions remain active too.

All ten static Test Desiderata categories and all Mockbuster detection categories
are active. Writable and Inspiring remain discussion topics; their optional AI
review is outside the credential-free checks. Ask whether tests are easy to write,
suggest useful cases, and survive harmless refactors.

The deliberately broken snippets run directly through each tool, as shown in the
[README](../README.md). Their failures are demonstrations, outside the passing CI
checks. Compare the actual diagnostic with the lesson; an unrelated crash does
not demonstrate the intended idea.

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
| 5. Meaningful assertions | NASA05 plus seven assertion-quality diagnostics; Hypothesis reaches invariant failures. |
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
- [Import-linter](https://import-linter.readthedocs.io/)
- [pytest-examples](https://github.com/pydantic/pytest-examples)
- [mutmut](https://mutmut.readthedocs.io/en/latest/)

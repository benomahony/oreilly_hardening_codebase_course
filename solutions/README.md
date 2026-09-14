# Completed solutions

Run **`make solutions`**. These are real runnable answers; none of the checks are
disabled to make them pass. The complete corrected application is in `src/reservations/`.

| Failure | Correction |
|---|---|
| Formatting, imports, broad exception, missing types | `strict.py`: format the code, use concrete types, and propagate a specific business error |
| NASA01 forbidden API | `defensive.py`: call known functions directly instead of evaluating code |
| NASA01 recursion | `defensive.py::reserve_batch`: iterate over a bounded tuple |
| NASA02 unbounded loop | Validate the 32-item maximum before starting work |
| NASA04 long function | Split the unit calculation from batch orchestration |
| NASA05 too few meaningful assertions | Check positive units, nonnegative stock, and conservation |
| NASA05-message | Give each invariant a useful failure message |
| NASA05-single-condition | Give each invariant its own assertion |
| NASA05-constant-assert | Assert properties of inputs and calculated outputs, not just-assigned literals |
| NASA05-redundant-none | Remove a redundant type-shaped check; assert a business property |
| NASA05-total-op | Do not count string-conversion truthiness as a stock invariant |
| NASA05-guaranteed-len | Check a business upper bound instead of `len(x) >= 0` |
| NASA05-isinstance | Type-check statically and validate external input explicitly |
| DDD vocabulary | `ddd/reservations.py`: one `create_reservation`, no manager/booking/duplicate definition |
| Ten static Test Desiderata categories | `test_desiderata.py`: fixed local inputs, real behavior, specific errors, short active tests |
| Mocks | `test_mock_free.py`: use the real parser, application, and domain |
| Hypothesis counterexample and fuzz crash | `defensive.py`: remove the erroneous `+ 1`; `test_properties.py`: retain the property and minimal regression |
| Architecture | `architecture.md`: correct layer direction; passing source and architecture tests |
| Stale documentation | `docs/updated.md`: seven units remain |
| Executable ADR | `../docs/adr/`: decisions expressed as runnable assertions with consequences documented |
| Mutation survivor | `../tests/test_application.py`: explicitly test an empty batch with zero stock |

Writable and Inspiring are reviewed by reading these short tests: setup is cheap,
the names express intent, and boundary properties suggest further examples. The
tool's optional AI review can support this discussion, but is not part of the
deterministic, credential-free gate.

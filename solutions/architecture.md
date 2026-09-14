# Architecture solution

Remove the `domain → infrastructure` import. Put orchestration in the application
layer and input handling in infrastructure. The complete passing implementation is
in `src/reservations/`. This is checked by `make architecture` and
`tests/test_architecture.py`; it is the same contract as the deliberately broken
mini-package. Renaming a layer or disabling the contract is not a solution.

Allowed direction:

```text
infrastructure → application → domain
```

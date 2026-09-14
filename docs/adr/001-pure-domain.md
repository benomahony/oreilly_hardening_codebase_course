# ADR 001: Keep reservation calculation pure

Status: accepted.

Context: a failed batch must not leave a partial stock update. Decision: compute
the outcome before any future persistence operation; use immutable inputs and a
domain free of framework dependencies. Consequence: a persistence adapter would
still need its own concurrency and transaction guarantees. This demo has no database.

This executable decision protects the observable failure behavior. The import
contracts separately protect dependency direction.

```python
from reservations.application.reservations import reserve_batch
from reservations.domain.stock import InsufficientStockError

quantities = (2, 9)
try:
    reserve_batch(10, quantities)
except InsufficientStockError:
    pass
else:
    raise AssertionError("an overcommitted batch must fail")
assert quantities == (2, 9)
assert reserve_batch(10, (2, 3)) == 5
```

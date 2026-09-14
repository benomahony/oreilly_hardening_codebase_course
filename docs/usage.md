# Using the reservation service

The wire boundary accepts positive ASCII decimal quantities. The service then
reserves them as a single pure calculation.

A single reservation consumes exactly the requested quantity. This is the
corrected output for the stale-documentation exercise.

```python
from reservations.domain.stock import reserve

print(reserve(10, 3))
#> 7
```

```python
from reservations.application.reservations import reserve_batch
from reservations.infrastructure.wire import parse_reservations

quantities = parse_reservations(b"2,3")
print(reserve_batch(10, quantities))
#> 5
```

Expected business failures have a specific exception type.

```python
from reservations.domain.stock import InsufficientStockError, reserve

try:
    reserve(2, 3)
except InsufficientStockError as error:
    print(str(error))
    #> requested units exceed available stock
```

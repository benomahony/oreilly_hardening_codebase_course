# Using the reservation service

The wire boundary accepts positive ASCII decimal quantities. The service then
reserves them as a single pure calculation.

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

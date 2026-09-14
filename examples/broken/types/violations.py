from typing import Any
from reservations.domain.stock import reserve

wrong_argument = reserve("10", 1)
wrong_return: str = reserve(10, 1)
optional_stock: int | None = None
unsafe_optional = reserve(optional_stock, 1)
unchecked: Any = "ten"
escaped_check = reserve(unchecked, 1)

def untyped_reservation(stock, units):
    return stock - units

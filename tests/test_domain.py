# Copyright (c) 2026 Ben O'Mahony
"""Business outcomes and exact contract failures for stock reservations."""

import pytest

from reservations.domain.stock import InsufficientStockError, reserve


@pytest.mark.parametrize(
    ("available", "requested", "expected"), [(10, 3, 7), (1, 1, 0), (100, 99, 1)]
)
def test_reservation_reduces_available_stock(available: int, requested: int, expected: int) -> None:
    """A reservation consumes exactly the requested quantity."""
    assert reserve(available, requested) == expected


@pytest.mark.parametrize(("available", "requested"), [(0, 1), (3, 4), (1, 9999)])
def test_reservation_rejects_overselling(available: int, requested: int) -> None:
    """Insufficient stock is an expected business rejection."""
    with pytest.raises(InsufficientStockError, match=r"^requested units exceed available stock$"):
        _ = reserve(available, requested)


def test_negative_stock_trips_the_programmer_contract() -> None:
    """Corrupt internal state is different from an expected business rejection."""
    with pytest.raises(AssertionError, match=r"^available stock must never be negative$"):
        _ = reserve(-1, 1)


@pytest.mark.parametrize("requested", [0, -1, -9999])
def test_nonpositive_request_trips_the_programmer_contract(requested: int) -> None:
    """A caller bypassing the input boundary receives a specific contract failure."""
    with pytest.raises(AssertionError, match=r"^a reservation must request positive units$"):
        _ = reserve(10, requested)

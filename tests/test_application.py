# Copyright (c) 2026 Ben O'Mahony
"""Batch reservations exercise the real domain implementation without mocks."""

import pytest

from reservations.application.reservations import reserve_batch
from reservations.domain.stock import InsufficientStockError


def test_batch_returns_remaining_stock() -> None:
    """The outcome is observable without assertions about internal call order."""
    assert reserve_batch(10, (2, 3)) == 5


def test_empty_batch_preserves_stock() -> None:
    """An internal empty batch is a no-op."""
    assert reserve_batch(5, ()) == 5


def test_empty_batch_accepts_zero_stock() -> None:
    """Mutation testing exposed this missing zero boundary despite full coverage."""
    assert reserve_batch(0, ()) == 0


def test_largest_batch_can_exhaust_stock() -> None:
    """The maximum is inclusive."""
    assert reserve_batch(32, (1,) * 32) == 0


def test_batch_failure_exposes_no_partial_result() -> None:
    """The service is a pure calculation, so a failure cannot partially commit state."""
    quantities = (2, 9)
    with pytest.raises(InsufficientStockError, match=r"^requested units exceed available stock$"):
        _ = reserve_batch(10, quantities)
    assert quantities == (2, 9)


def test_batch_rejects_negative_initial_stock() -> None:
    """Even an empty batch must not allow corrupt stock through."""
    with pytest.raises(AssertionError, match=r"^initial stock must never be negative$"):
        _ = reserve_batch(-1, ())


def test_batch_rejects_too_many_reservations() -> None:
    """The bound prevents a caller from introducing unbounded work."""
    with pytest.raises(AssertionError, match=r"^reservation batches must be bounded$"):
        _ = reserve_batch(100, (1,) * 33)


@pytest.mark.parametrize("quantity", [0, -1])
def test_batch_rejects_nonpositive_reservations(quantity: int) -> None:
    """Validate the complete batch before applying a reservation."""
    with pytest.raises(AssertionError, match=r"^every reservation must be positive$"):
        _ = reserve_batch(100, (1, quantity))

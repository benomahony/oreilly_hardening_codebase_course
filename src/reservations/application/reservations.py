# Copyright (c) 2026 Ben O'Mahony
"""Reserve a complete batch without exposing partial results."""

from typing import Final

from reservations.domain.stock import reserve

MAX_RESERVATIONS: Final = 32


def reserve_batch(available: int, quantities: tuple[int, ...]) -> int:
    """Reserve at most 32 requests; reject the whole calculation on failure."""
    assert available >= 0, "initial stock must never be negative"
    assert len(quantities) <= MAX_RESERVATIONS, "reservation batches must be bounded"
    assert all(quantity > 0 for quantity in quantities), "every reservation must be positive"
    remaining = available
    for quantity in quantities:
        remaining = reserve(remaining, quantity)
    assert remaining + sum(quantities) == available, "the batch must conserve stock"
    return remaining

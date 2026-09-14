# Copyright (c) 2026 Ben O'Mahony
"""Formatting, linting, and type-safety solution: typed real behavior, no Any escape."""

from reservations.domain.stock import reserve


def remaining_stock(available: int, requested: int) -> int:
    """Use concrete types, narrow contracts, and the correct return type."""
    assert available >= 0, "available stock must never be negative"
    assert requested > 0, "a reservation must request positive units"
    return reserve(available, requested)

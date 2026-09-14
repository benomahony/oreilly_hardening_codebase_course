# Copyright (c) 2026 Ben O'Mahony
"""Replace StockManager and create_booking with one unambiguous domain name."""

from reservations.domain.stock import reserve


def create_reservation(available: int, requested: int) -> int:
    """Name the operation in the canonical ubiquitous language."""
    assert available >= 0, "available stock must never be negative"
    assert requested > 0, "a reservation must request positive units"
    return reserve(available, requested)

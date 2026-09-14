# Copyright (c) 2026 Ben O'Mahony
"""The missing boundary case that kills the real surviving mutant."""

from reservations.application.reservations import reserve_batch


def test_an_empty_batch_accepts_zero_available_stock() -> None:
    """Zero is valid; a guard changing from >= 0 to > 0 must fail the test."""
    assert reserve_batch(0, ()) == 0

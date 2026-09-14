# Copyright (c) 2026 Ben O'Mahony
"""Replace the mock's invented result with the real end-to-end behavior."""

from reservations.application.reservations import reserve_batch
from reservations.infrastructure.wire import parse_reservations


def test_two_real_reservations_leave_five_units() -> None:
    """Behavior remains meaningful after internal implementation refactors."""
    assert reserve_batch(10, parse_reservations(b"2,3")) == 5

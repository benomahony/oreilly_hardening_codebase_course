# Copyright (c) 2026 Ben O'Mahony
"""Verify the formatting, typing, and vocabulary solutions execute correctly."""

from solutions.ddd.reservations import create_reservation
from solutions.strict import remaining_stock


def test_typed_reservation_has_the_correct_result() -> None:
    """Formatting and type fixes retain the real domain operation."""
    assert remaining_stock(10, 3) == 7


def test_canonical_vocabulary_identifies_a_real_operation() -> None:
    """A domain name denotes one business concept with real behavior."""
    assert create_reservation(10, 3) == 7

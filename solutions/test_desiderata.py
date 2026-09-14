# Copyright (c) 2026 Ben O'Mahony
"""Solutions for all ten static Test Desiderata categories.

DET/ISO: explicit local inputs. FST/AUT: synchronous behavior without waiting or
input. BHV/STR: real results, no mocks or call assertions. SPC: precise exception.
PRD: active tests. CMP/RDL: short tests named after one observable behavior.
Writable and Inspiring remain a human discussion; see README.md.
"""

import pytest

from reservations.domain.stock import InsufficientStockError, reserve


def test_reservation_consumes_exactly_three_units() -> None:
    """A fast, deterministic, isolated test of real behavior."""
    assert reserve(10, 3) == 7


def test_overcommitted_reservation_reports_insufficient_stock() -> None:
    """A specific exception prevents unrelated failures from making this pass."""
    with pytest.raises(InsufficientStockError, match=r"^requested units exceed available stock$"):
        _ = reserve(2, 3)

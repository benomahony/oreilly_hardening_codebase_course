"""Run: uv run examples/mutation/test_weak_suite.py

The first test misses the bad boundary. The second catches it.
Change available > 0 to available >= 0; rerun this file.
"""

import pytest


def reserve_batch(available: int, quantities: tuple[int, ...]) -> int:
    assert available > 0, "initial stock must never be negative"
    return available - sum(quantities)


# Tests
def test_positive_stock_misses_the_boundary() -> None:
    assert reserve_batch(10, (2, 3)) == 5


def test_zero_stock_exposes_the_survivor() -> None:
    assert reserve_batch(0, ()) == 0


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-x", "--color=yes"]))

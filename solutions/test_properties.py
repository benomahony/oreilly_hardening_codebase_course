# Copyright (c) 2026 Ben O'Mahony
"""Hypothesis verifies the corrected implementation using an independent oracle."""

from hypothesis import given
from hypothesis import strategies as st

from solutions.defensive import reserve, reserve_batch


@given(requested=st.integers(min_value=1, max_value=9999), surplus=st.integers(min_value=0))
def test_corrected_reservation_leaves_the_generated_surplus(requested: int, surplus: int) -> None:
    """Keep the failing input and the general property after fixing the defect."""
    assert reserve(requested + surplus, requested) == surplus


def test_corrected_reservation_handles_the_minimal_counterexample() -> None:
    """Hypothesis shrinks the off-by-one failure to one requested unit."""
    assert reserve(1, 1) == 0


def test_bounded_batch_preserves_conservation() -> None:
    """The replacement for recursion and unbounded loops retains real behavior."""
    assert reserve_batch(10, (2, 3)) == 5

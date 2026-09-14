"""Run: uv run examples/assertions/test_off_by_one.py

Add + 1 to the remaining-stock calculation to demonstrate a failure.
Remove it to fix the bug. Hypothesis finds the smallest counterexample.
"""

if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-q", "-x", "--color=yes"]))


import pytest
from hypothesis import given, settings, strategies as st

def broken_reserve(available: int, requested: int) -> int:
    assert available >= 0, "available stock must never be negative"
    assert requested > 0, "a reservation must request positive units"
    remaining = available - requested + 1
    assert remaining + requested == available, "a reservation must conserve stock"
    return remaining

@settings(max_examples=30, derandomize=True, deadline=None)
@given(requested=st.integers(min_value=1, max_value=9999))
def test_generated_requests_expose_off_by_one(requested: int) -> None:
    assert broken_reserve(requested, requested) == 0

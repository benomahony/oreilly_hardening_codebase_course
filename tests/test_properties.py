# Copyright (c) 2026 Ben O'Mahony
"""Generated inputs exercise conservation, boundary conditions, and assertion failures."""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from reservations.application.reservations import reserve_batch
from reservations.domain.stock import InsufficientStockError, reserve
from reservations.infrastructure.wire import parse_reservations

settings.register_profile("demo", max_examples=300, derandomize=True, deadline=None)
settings.load_profile("demo")


@pytest.mark.property
@given(requested=st.integers(min_value=1, max_value=9999), surplus=st.integers(min_value=0))
def test_reservation_conserves_stock(requested: int, surplus: int) -> None:
    """Generate stock from a request and known surplus: the surplus is the oracle."""
    assert reserve(requested + surplus, requested) == surplus


@pytest.mark.property
@given(available=st.integers(min_value=0), excess=st.integers(min_value=1))
def test_every_oversized_request_is_rejected(available: int, excess: int) -> None:
    """The business error must hold for every generated excess."""
    with pytest.raises(InsufficientStockError, match=r"^requested units exceed available stock$"):
        _ = reserve(available, available + excess)


@pytest.mark.property
@given(available=st.integers(max_value=-1))
def test_generated_corrupt_stock_hits_the_assertion(available: int) -> None:
    """Drive an actual programmer invariant to failure with generated invalid state."""
    with pytest.raises(AssertionError, match=r"^available stock must never be negative$"):
        _ = reserve(available, 1)


@pytest.mark.property
@given(requested=st.integers(max_value=0))
def test_generated_nonpositive_requests_hit_the_assertion(requested: int) -> None:
    """Generate counterexamples to the positive-quantity precondition."""
    with pytest.raises(AssertionError, match=r"^a reservation must request positive units$"):
        _ = reserve(10, requested)


@pytest.mark.property
@given(quantities=st.lists(st.integers(min_value=1, max_value=9999), min_size=1, max_size=32))
def test_generated_wire_requests_round_trip_and_exhaust_stock(quantities: list[int]) -> None:
    """Build valid requests independently of the parser's regular expression."""
    payload = ",".join(str(quantity) for quantity in quantities).encode("ascii")
    parsed = parse_reservations(payload)
    assert parsed == tuple(quantities)
    assert reserve_batch(sum(quantities), parsed) == 0


@pytest.mark.property
@given(payload=st.binary(max_size=200))
def test_arbitrary_bytes_never_escape_as_assertion_failures(payload: bytes) -> None:
    """Only validation errors are expected; assertion failures remain visible."""
    try:
        quantities = parse_reservations(payload)
    except ValueError:
        return
    assert 1 <= len(quantities) <= 32
    assert all(1 <= quantity <= 9999 for quantity in quantities)
    assert reserve_batch(sum(quantities), quantities) == 0

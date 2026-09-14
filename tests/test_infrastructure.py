# Copyright (c) 2026 Ben O'Mahony
"""Boundary validation rejects bad bytes with explicit, optimization-safe errors."""

import pytest

from reservations.application.reservations import reserve_batch
from reservations.infrastructure.wire import parse_reservations


@pytest.mark.parametrize(
    ("payload", "expected"),
    [(b"1", (1,)), (b"2,3", (2, 3)), (b"9999", (9999,)), (b"10,100,1000", (10, 100, 1000))],
)
def test_valid_wire_quantities_are_parsed(payload: bytes, expected: tuple[int, ...]) -> None:
    """All decimal widths and multi-item batches retain their values."""
    assert parse_reservations(payload) == expected


@pytest.mark.parametrize(
    "payload",
    [
        b"",
        b"0",
        b"-1",
        b"01",
        b"+1",
        b"1.0",
        b" 1",
        b"1 ",
        b"1\n",
        b"1,",
        b",1",
        b"1,,2",
        b"10000",
        b"\xff",
        b"1\x00",
        b",".join([b"1"] * 33),
    ],
)
def test_malformed_wire_quantities_are_rejected(payload: bytes) -> None:
    """Malformed input is a validation error, never a programmer assertion."""
    with pytest.raises(
        ValueError, match=r"^expected 1 to 32 comma-separated quantities between 1 and 9999$"
    ):
        _ = parse_reservations(payload)


def test_maximum_payload_and_batch_are_accepted() -> None:
    """Thirty-two four-digit quantities occupy exactly 159 bytes."""
    assert parse_reservations(b",".join([b"9999"] * 32)) == (9999,) * 32


def test_oversized_payload_is_rejected_before_parsing() -> None:
    """Bounding input also bounds parser work and allocations."""
    with pytest.raises(ValueError, match=r"^reservation payload exceeds 159 bytes$"):
        _ = parse_reservations(b"1" * 160)


def test_wire_request_reaches_the_real_application() -> None:
    """The complete path uses real parsing, orchestration, and business logic."""
    assert reserve_batch(10, parse_reservations(b"2,3")) == 5

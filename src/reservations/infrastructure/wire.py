# Copyright (c) 2026 Ben O'Mahony
"""A bounded ASCII wire format: comma-separated positive decimal quantities."""

import re
from typing import Final

from reservations.application.reservations import MAX_RESERVATIONS

MAX_PAYLOAD_BYTES: Final = 159
MAX_QUANTITY: Final = 9999
_REQUEST: Final = rb"[1-9][0-9]{0,3}(?:,[1-9][0-9]{0,3}){0,31}"


def parse_reservations(payload: bytes) -> tuple[int, ...]:
    """Validate external input with exceptions, then verify parser postconditions."""
    if len(payload) > MAX_PAYLOAD_BYTES:
        msg = "reservation payload exceeds 159 bytes"
        raise ValueError(msg)
    if re.fullmatch(_REQUEST, payload) is None:
        msg = "expected 1 to 32 comma-separated quantities between 1 and 9999"
        raise ValueError(msg)
    quantities = tuple(int(token) for token in payload.split(b","))
    assert len(quantities) <= MAX_RESERVATIONS, "the parser must enforce the batch limit"
    assert all(quantity > 0 for quantity in quantities), "the parser must reject nonpositive units"
    assert all(quantity <= MAX_QUANTITY for quantity in quantities), (
        "parsed quantities must be bounded"
    )
    return quantities

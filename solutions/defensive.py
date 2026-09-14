# Copyright (c) 2026 Ben O'Mahony
"""Solution to every NASA fixture: simple bounded work and meaningful contracts.

No recursion or dynamic APIs; functions fit on a page; assertions each express
one business invariant with a message. They neither restate types nor pad the
count with facts guaranteed by the language. See README.md for each rule's fix.
"""

from reservations.domain.stock import InsufficientStockError

MAX_RESERVATIONS = 32


def reserve(available: int, requested: int) -> int:
    """Fix the arithmetic bug while preserving a conservation assertion."""
    assert available >= 0, "available stock must never be negative"
    assert requested > 0, "a reservation must request positive units"
    if requested > available:
        msg = "requested units exceed available stock"
        raise InsufficientStockError(msg)
    remaining = available - requested
    assert remaining >= 0, "a reservation must never oversell stock"
    assert remaining + requested == available, "a reservation must conserve stock"
    return remaining


def reserve_batch(available: int, quantities: tuple[int, ...]) -> int:
    """Replace recursive or open-ended work with an explicitly bounded batch."""
    assert available >= 0, "initial stock must never be negative"
    assert len(quantities) <= MAX_RESERVATIONS, "reservation batches must be bounded"
    assert all(quantity > 0 for quantity in quantities), "every reservation must be positive"
    remaining = available
    for quantity in quantities:
        remaining = reserve(remaining, quantity)
    assert remaining + sum(quantities) == available, "the batch must conserve stock"
    return remaining

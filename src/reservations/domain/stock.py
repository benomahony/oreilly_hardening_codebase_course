# Copyright (c) 2026 Ben O'Mahony
"""Stock conservation is the invariant at the heart of a reservation."""


class InsufficientStockError(ValueError):
    """The requested quantity exceeds the stock that is available."""


def reserve(available: int, requested: int) -> int:
    """Return remaining stock, or reject a reservation that cannot be fulfilled.

    Preconditions are programmer contracts. Untrusted input must go through the
    infrastructure parser; assertion failures indicate an internal defect.
    """
    assert available >= 0, "available stock must never be negative"
    assert requested > 0, "a reservation must request positive units"
    if requested > available:
        msg = "requested units exceed available stock"
        raise InsufficientStockError(msg)
    remaining = available - requested
    assert remaining >= 0, "a reservation must never oversell stock"
    assert remaining + requested == available, "a reservation must conserve stock"
    return remaining

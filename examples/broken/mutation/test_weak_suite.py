from reservations.application.reservations import reserve_batch

def surviving_mutant(available: int, quantities: tuple[int, ...]) -> int:
    # The actual mutmut change that survived the original suite: >= 0 became > 0.
    assert available > 0, "initial stock must never be negative"
    return reserve_batch(available, quantities)

def test_positive_stock_misses_the_boundary() -> None:
    assert surviving_mutant(10, (2, 3)) == 5

def test_zero_stock_exposes_the_survivor() -> None:
    assert surviving_mutant(0, ()) == 0

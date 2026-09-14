from reservations.infrastructure.wire import parse_reservations

def exercise(payload: bytes) -> None:
    quantities = parse_reservations(payload)
    available = sum(quantities)
    remaining = available - sum(quantities) + 1  # Deliberate bug.
    assert remaining + sum(quantities) == available, "fuzzing found a stock conservation failure"

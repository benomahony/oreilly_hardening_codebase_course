# Copyright (c) 2026 Ben O'Mahony
"""Prove boundary validation still rejects bad bytes when Python removes asserts."""

from reservations.infrastructure.wire import parse_reservations


def main() -> None:
    """Use explicit checks because this command intentionally runs with python -O."""
    for payload in (b"0", b"-1", b"01", b"1\n", b"1" * 160, b",".join([b"1"] * 33)):
        try:
            _ = parse_reservations(payload)
        except ValueError:
            continue
        msg = f"optimized validation accepted invalid input: {payload!r}"
        raise RuntimeError(msg)
    if parse_reservations(b"2,3") != (2, 3):
        msg = "optimized validation changed valid input"
        raise RuntimeError(msg)


if __name__ == "__main__":
    main()

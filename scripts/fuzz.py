# Copyright (c) 2026 Ben O'Mahony
"""Portable, deterministic corpus mutation; Atheris provides coverage guidance on Linux."""

from __future__ import annotations

import argparse
import random
import sys

from reservations.application.reservations import reserve_batch
from reservations.infrastructure.wire import parse_reservations

CORPUS = (b"1", b"2,3", b"9999", b",".join([b"9999"] * 32), b"0", b"-1", b"", b"1" * 160)
MAX_BATCH = 32
MAX_UNITS = 9999


class FuzzOptions(argparse.Namespace):
    """Typed options for reproducible fuzzing."""

    runs: int = 10000
    exercise_bug: bool = False


def exercise(payload: bytes) -> bool:
    """Let unexpected exceptions and domain assertions crash the fuzzer."""
    try:
        quantities = parse_reservations(payload)
    except ValueError:
        return False
    assert 1 <= len(quantities) <= MAX_BATCH, "accepted batch must respect its bound"
    assert all(1 <= quantity <= MAX_UNITS for quantity in quantities), (
        "accepted units must be valid"
    )
    remaining = reserve_batch(sum(quantities), quantities)
    assert remaining == 0, "reserving every unit must exhaust stock"
    return True


def main() -> int:
    """Mutate valid and invalid seeds and retain reproducibility for a live demo."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--runs", type=int, default=10000)
    _ = parser.add_argument("--exercise-bug", action="store_true")
    args = parser.parse_args(namespace=FuzzOptions())
    if args.runs < 1:
        parser.error("--runs must be positive")
    if args.exercise_bug:
        from examples.broken.fuzz.off_by_one import exercise as exercise_bug  # noqa: PLC0415

        for payload in CORPUS[:4]:
            exercise_bug(payload)
        return 1
    rng = random.Random(2026)  # noqa: S311 -- Reproducible input mutation, no security use.
    accepted = sum(exercise(payload) for payload in CORPUS)
    for _ in range(args.runs):
        payload = bytearray(rng.choice(CORPUS))
        if payload and rng.randrange(2):
            payload[rng.randrange(len(payload))] = rng.randrange(256)
        else:
            payload.insert(rng.randrange(len(payload) + 1), rng.randrange(256))
        accepted += exercise(bytes(payload))
    count = args.runs + len(CORPUS)
    _ = sys.stdout.write(
        f"Fuzzed {count} inputs: {accepted} accepted, {count - accepted} rejected, no crashes.\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

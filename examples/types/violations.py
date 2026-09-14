"""Run: uv run examples/types/violations.py

The stock is a string. Change its annotation and value to an integer.
"""


from pathlib import Path
import subprocess

import pytest


def reserve(stock: int, units: int) -> int:
    return stock - units


def request_reservation() -> int:
    stock: str = "10"
    return reserve(stock, 3)


# Tests
def test_types_are_correct() -> None:
    result = subprocess.run(
        ["basedpyright", "--project", str(Path(__file__).parent)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_reservation_leaves_seven_units() -> None:
    assert request_reservation() == 7


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-x", "--color=yes"]))

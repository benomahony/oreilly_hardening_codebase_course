"""Run: uv run examples/mocks/test_mocks.py

Replace the mocked call with reserve(10, 3), and remove the Mock import.
"""

import subprocess
from unittest.mock import Mock

import pytest


def reserve(stock: int, units: int) -> int:
    return stock - units


# Tests
def test_example_uses_real_behavior() -> None:
    result = subprocess.run(
        ["mockbuster", __file__, "--strict"], capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_reservation_leaves_seven_units() -> None:
    reservation = Mock(return_value=7)
    assert reservation(10, 3) == 7


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-x", "--color=yes"]))

"""Run: uv run examples/architecture/bad_reservations/domain.py

Remove the infrastructure import and print call from reserve.
The domain calculation should not depend on an outer layer.
"""

def reserve(stock: int, units: int) -> int:
    from bad_reservations.infrastructure import DATABASE_NAME

    print(DATABASE_NAME)
    return stock - units


# Tests
import os
from pathlib import Path
import subprocess

import pytest


def test_domain_does_not_depend_on_infrastructure() -> None:
    directory = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["lint-imports", "--config", str(directory / "pyproject.toml")],
        cwd=directory, env=dict(os.environ, PYTHONPATH=str(directory)),
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_reservation_leaves_seven_units() -> None:
    assert reserve(10, 3) == 7


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-x", "--color=yes"]))

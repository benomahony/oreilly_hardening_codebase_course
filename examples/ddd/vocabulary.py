"""Run: uv run examples/ddd/vocabulary.py

Use stock and reservation names; remove the duplicate definition.
"""

class StockManager:
    pass

def create_booking():
    pass

def create_reservation():
    pass

def create_reservation():
    pass


# Tests
from pathlib import Path
import subprocess

import pytest


def test_domain_vocabulary_is_consistent() -> None:
    directory = Path(__file__).parent
    result = subprocess.run(
        ["dddlint", "lint", str(directory), "--config", str(directory / "dddlint.yaml")],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-x", "--color=yes"]))

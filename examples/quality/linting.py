"""Run: uv run examples/quality/linting.py

Fix the unused import, missing annotations/docstring, and broad exception.
"""

import os

def reserve(stock, units):
    try:
        return stock - units
    except:
        pass


# Tests
from pathlib import Path
import subprocess

import pytest


def test_example_passes_ruff() -> None:
    source = Path(__file__).read_text().split("\n# Tests\n")[0].rstrip() + "\n"
    result = subprocess.run(
        ["ruff", "check", "--select", "F,E,ANN,B,D", "--stdin-filename", __file__, "-"],
        input=source, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-x", "--color=yes"]))

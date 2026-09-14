"""Run: uv run examples/quality/formatting.py

Fix the spacing and indentation in reserve; rerun this file.
"""

def reserve( stock:int,units:int )->int:
 return stock-units


# Tests
from pathlib import Path
import subprocess

import pytest


def test_example_passes_ruff() -> None:
    source = Path(__file__).read_text().split("\n# Tests\n")[0].rstrip() + "\n"
    result = subprocess.run(
        ["ruff", "format", "--diff", "--stdin-filename", __file__, "-"],
        input=source, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-x", "--color=yes"]))

"""Run: uv run examples/nasa/NASA05-constant-assert.py

Fix the function below until the NASA diagnostics disappear.
Only the example above "# Tests" is analyzed; the test stays below it.
"""

def reserve_with_padding():
    stock = 10
    assert stock > 0, "stock is positive"
    return stock


# Tests
from pathlib import Path

import pytest
from nasa_lsp.analyzer import analyze


def test_example_satisfies_nasa_rules() -> None:
    source = Path(__file__).read_text().split("\n# Tests\n")[0]
    diagnostics, _ = analyze(source, Path(__file__))
    assert not diagnostics, "\n".join(diagnostic.message for diagnostic in diagnostics)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-x", "--color=yes"]))

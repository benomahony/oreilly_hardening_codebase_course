"""Run: uv run examples/desiderata/test_cmp001.py

Fix the test below until the quality check passes, then the test runs.
The quality check runs first so broken input/sleep/randomness examples do not execute.
"""

import ast
from pathlib import Path

from testdesiderata.linter import Linter

import pytest


def test_example_meets_test_desiderata() -> None:
    source = Path(__file__).read_text().split("\n# Example to fix\n")[1]
    source = source.split('\nif __name__ == "__main__":')[0]
    diagnostics = Linter().lint_tree(ast.parse("import pytest\n" + source), __file__)
    assert not diagnostics, "\n".join(
        f"{diagnostic.rule_id}: {diagnostic.message}" for diagnostic in diagnostics
    )


# Example to fix
def test_every_stock_value():
    assert 0 >= 0
    assert 1 >= 0
    assert 2 >= 0
    assert 3 >= 0
    assert 4 >= 0
    assert 5 >= 0
    assert 6 >= 0
    assert 7 >= 0
    assert 8 >= 0
    assert 9 >= 0
    assert 10 >= 0

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-x", "--color=yes"]))

"""Run: uv run examples/desiderata/test_prd003.py

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

@pytest.mark.xfail
def test_hidden_failure():
    assert False

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-x", "--color=yes"]))

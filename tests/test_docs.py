# Copyright (c) 2026 Ben O'Mahony
"""Execute Markdown documentation and ADR code blocks against the real package."""

import pytest
from pytest_examples import CodeExample, EvalExample, find_examples


@pytest.mark.docs
@pytest.mark.parametrize(
    "example", list(find_examples("docs/usage.md", "docs/adr", "solutions/docs")), ids=str
)
def test_documentation_and_decisions_remain_true(
    example: CodeExample, eval_example: EvalExample
) -> None:
    """An outdated expected result in a document must break the test suite."""
    _ = eval_example.run_print_check(example)

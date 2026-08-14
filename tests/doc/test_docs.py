"""Technique 7: pytest-examples validates every fenced python block in our
docstrings and markdown docs actually runs. Without this, a docstring
example is just a comment nobody checks — it rots the moment the API it
demonstrates changes, and nothing tells you.
"""

from __future__ import annotations

import pytest
from pytest_examples import CodeExample, EvalExample, find_examples

pytestmark = pytest.mark.doc

EXAMPLES = [
    *find_examples("src"),
    *find_examples("docs"),
    *find_examples("exercises"),
]


@pytest.mark.parametrize("example", EXAMPLES, ids=str)
def test_documentation_examples_run(example: CodeExample, eval_example: EvalExample) -> None:
    eval_example.run(example)

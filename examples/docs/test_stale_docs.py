import pytest
from pytest_examples import find_examples, CodeExample, EvalExample

@pytest.mark.parametrize("example", list(find_examples("examples/docs/stale.md")), ids=str)
def test_outdated_documentation(example: CodeExample, eval_example: EvalExample):
    eval_example.run_print_check(example)

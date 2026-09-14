"""Run: uv run examples/docs/test_stale_docs.py

Correct the expected output in this example: ten minus three is seven.

```python
def reserve(stock: int, units: int) -> int:
    return stock - units

print(reserve(10, 3))
#> 8
```
"""

if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-q", "-x", "--color=yes"]))


import pytest
from pytest_examples import CodeExample, EvalExample, find_examples


# Tests
@pytest.mark.parametrize("example", list(find_examples(__file__)), ids=str)
def test_documentation_matches_behavior(example: CodeExample, eval_example: EvalExample) -> None:
    eval_example.run_print_check(example)

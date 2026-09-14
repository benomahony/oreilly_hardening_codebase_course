"""The Atheris 3.1 API subset used by the Linux smoke test."""

from collections.abc import Callable
from contextlib import AbstractContextManager

def instrument_imports() -> AbstractContextManager[None]: ...
def instrument_func(function: Callable[[bytes], None]) -> Callable[[bytes], None]: ...
def Setup(
    argv: list[str],
    test_one_input: Callable[[bytes], None],
    *,
    enable_python_coverage: bool = ...,
) -> None: ...
def Fuzz() -> None: ...

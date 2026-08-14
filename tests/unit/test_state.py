import pytest

from oreilly_hardening_codebase_course.commons.state import ParseContext

pytestmark = pytest.mark.unit


def test_typed_dict_accepts_bad_data() -> None:
    """Pins the tradeoff documented in commons/state.py: TypedDict enforces
    nothing at runtime. A negative token_count is nonsense, but nothing
    raises — that's the cost of skipping Pydantic here. If this ever starts
    mattering, promote ParseContext to a BaseModel with Field(ge=0)."""
    ctx: ParseContext = {"raw_text": "/task add", "tokens": [], "token_count": -1}
    assert ctx["token_count"] == -1

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from oreilly_hardening_codebase_course.commons.models import MAX_TITLE_LENGTH, Task

pytestmark = pytest.mark.property


@given(st.text(min_size=1, max_size=MAX_TITLE_LENGTH))
def test_task_round_trips_through_json_for_any_valid_title(title: str) -> None:
    task = Task(id=1, title=title)
    restored = Task.model_validate_json(task.model_dump_json())
    assert restored == task


@given(st.text(min_size=MAX_TITLE_LENGTH + 1, max_size=MAX_TITLE_LENGTH + 50))
def test_task_rejects_any_title_over_the_length_limit(title: str) -> None:
    with pytest.raises(ValidationError):
        Task(id=1, title=title)


@given(st.integers(max_value=0))
def test_task_rejects_any_non_positive_id(bad_id: int) -> None:
    with pytest.raises(ValidationError):
        Task(id=bad_id, title="Buy milk")

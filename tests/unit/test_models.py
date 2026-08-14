import pytest
from pydantic import ValidationError

from oreilly_hardening_codebase_course.commons.models import CommandResult, Task, TaskCommand

pytestmark = pytest.mark.unit


def test_task_accepts_valid_data() -> None:
    task = Task(id=1, title="Buy milk")
    assert task.done is False
    assert task.due is None


def test_task_rejects_empty_title() -> None:
    with pytest.raises(ValidationError, match="title"):
        Task(id=1, title="")


def test_task_rejects_non_positive_id() -> None:
    with pytest.raises(ValidationError, match="id"):
        Task(id=0, title="Buy milk")


def test_task_command_rejects_unknown_action() -> None:
    with pytest.raises(ValidationError):
        TaskCommand(action="delete_everything", raw_text="/task delete_everything")  # type: ignore[arg-type]


def test_command_result_allows_missing_task() -> None:
    result = CommandResult(ok=True, message="No tasks yet.")
    assert result.task is None

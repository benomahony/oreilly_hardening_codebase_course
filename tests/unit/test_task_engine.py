import pytest

from oreilly_hardening_codebase_course.commons.models import CommandResult, TaskCommand
from oreilly_hardening_codebase_course.engines.task_engine import TaskEngine
from tests.fakes import FailingTaskStore, InMemoryTaskStore, StoreUnavailableError

pytestmark = pytest.mark.unit


@pytest.fixture
def engine() -> TaskEngine:
    return TaskEngine(store=InMemoryTaskStore())


def _add(engine: TaskEngine, title: str) -> CommandResult:
    return engine.handle(TaskCommand(action="add", title=title, raw_text=f"/task add {title}"))


def _done(engine: TaskEngine, task_id: int) -> CommandResult:
    return engine.handle(
        TaskCommand(action="done", task_id=task_id, raw_text=f"/task done {task_id}")
    )


def test_add_creates_a_task_and_updates_metrics(engine: TaskEngine) -> None:
    result = _add(engine, "Buy milk")

    assert result.ok
    assert result.task is not None
    assert result.task.title == "Buy milk"
    assert engine.metrics.tasks_created == 1
    assert engine.metrics.commands_processed == 1


def test_done_on_missing_task_returns_actionable_error_and_does_not_raise(
    engine: TaskEngine,
) -> None:
    result = _done(engine, 999)

    assert not result.ok
    assert "999" in result.message
    assert engine.metrics.commands_failed == 1


def test_remove_on_missing_task_returns_actionable_error(engine: TaskEngine) -> None:
    result = engine.handle(TaskCommand(action="remove", task_id=999, raw_text="/task remove 999"))
    assert not result.ok
    assert "999" in result.message


def test_list_reports_no_tasks_yet_when_store_is_empty(engine: TaskEngine) -> None:
    result = engine.handle(TaskCommand(action="list", raw_text="/task list"))
    assert result.ok
    assert "No tasks yet" in result.message


def test_marking_an_already_done_task_done_again_says_so_instead_of_pretending(
    engine: TaskEngine,
) -> None:
    task_id = _add(engine, "Ship it").task.id  # type: ignore[union-attr]
    _done(engine, task_id)

    result = _done(engine, task_id)

    assert result.ok
    assert "already marked done" in result.message


def test_full_lifecycle_add_list_done_remove(engine: TaskEngine) -> None:
    task_id = _add(engine, "Ship it").task.id  # type: ignore[union-attr]

    assert "Ship it" in engine.handle(TaskCommand(action="list", raw_text="/task list")).message

    done = _done(engine, task_id)
    assert done.ok
    assert done.task is not None
    assert done.task.done is True

    removed = engine.handle(
        TaskCommand(action="remove", task_id=task_id, raw_text=f"/task remove {task_id}")
    )
    assert removed.ok


def test_engine_propagates_store_outage_instead_of_hiding_it() -> None:
    """FailingTaskStore stands in for "the database is down" — a real fake
    misbehaving on purpose, not a Mock with a canned side_effect."""
    engine = TaskEngine(store=FailingTaskStore())
    with pytest.raises(StoreUnavailableError):
        _add(engine, "Buy milk")

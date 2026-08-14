import pytest

from oreilly_hardening_codebase_course.commons.errors import (
    ActionableError,
    ErrorCollector,
    is_actionable,
    missing_title,
    unknown_command,
    unknown_task_id,
    unrecognized_date,
)

pytestmark = pytest.mark.unit


def test_unrecognized_date_names_the_bad_value_and_the_fix() -> None:
    message = unrecognized_date("13/40/2026").render()
    assert "13/40/2026" in message
    assert "yyyy-mm-dd" in message
    assert "help" in message.lower()


def test_unrecognized_date_handles_missing_value() -> None:
    message = unrecognized_date("").render()
    assert "I need a date" in message


def test_vague_message_fails_the_actionability_check() -> None:
    assert not is_actionable("An error occurred.")


def test_actionable_messages_pass_the_check() -> None:
    assert is_actionable(unrecognized_date("nope").render())
    assert is_actionable(missing_title().render())
    assert is_actionable(unknown_command("/task frobnicate").render())
    assert is_actionable(unknown_task_id(7).render())


def test_error_collector_renders_every_collected_error() -> None:
    collector = ErrorCollector()
    collector.add(missing_title())
    collector.add(unrecognized_date("13/40/2026"))

    rendered = collector.render()

    assert "title" in rendered
    assert "13/40/2026" in rendered


def test_error_collector_render_without_errors_raises() -> None:
    with pytest.raises(AssertionError):
        ErrorCollector().render()


def test_actionable_error_render_requires_problem_and_solution() -> None:
    with pytest.raises(AssertionError):
        ActionableError(problem="", solution="do something").render()

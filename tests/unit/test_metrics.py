import pytest

from oreilly_hardening_codebase_course.commons.metrics import BotMetrics

pytestmark = pytest.mark.unit


def test_failure_rate_is_zero_with_no_commands() -> None:
    assert BotMetrics().failure_rate == 0.0


def test_record_command_tracks_totals_and_failures() -> None:
    metrics = BotMetrics()
    metrics.record_command(failed=False)
    metrics.record_command(failed=True)

    assert metrics.commands_processed == 2
    assert metrics.commands_failed == 1
    assert metrics.failure_rate == 0.5


def test_record_command_rejects_non_bool_failed_flag() -> None:
    """Defensive assertion: a caller passing something other than bool is a
    programming error, and should fail loudly right where it happened."""
    metrics = BotMetrics()
    with pytest.raises(AssertionError):
        metrics.record_command(failed="yes")  # type: ignore[arg-type]


def test_record_task_created_and_completed() -> None:
    metrics = BotMetrics()
    metrics.record_task_created()
    metrics.record_task_completed()

    assert metrics.tasks_created == 1
    assert metrics.tasks_completed == 1

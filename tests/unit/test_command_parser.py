from datetime import date

import pytest

from oreilly_hardening_codebase_course.engines.command_parser import (
    CommandParseError,
    parse_command,
)

pytestmark = pytest.mark.unit


def test_parses_add_with_due_date() -> None:
    command = parse_command("/task add Buy milk due 2026-08-20")
    assert command.action == "add"
    assert command.title == "Buy milk"
    assert command.due == date(2026, 8, 20)


def test_parses_add_without_due_date() -> None:
    assert parse_command("/task add Buy milk").due is None


def test_parses_list_and_help_with_no_arguments() -> None:
    assert parse_command("/task list").action == "list"
    assert parse_command("/task help").action == "help"


def test_parses_done_and_remove_with_id() -> None:
    assert parse_command("/task done 3").task_id == 3
    assert parse_command("/task remove 3").task_id == 3


@pytest.mark.parametrize(
    ("raw_text", "expected_in_message"),
    [
        ("/task frobnicate", "frobnicate"),
        ("", "understand"),
        ("/task add", "title"),
        ("/task add Buy milk due not-a-date", "yyyy-mm-dd"),
        ("/task add " + "x" * 201, "too long"),
        ("/task done", "task id"),
        ("/task done not-a-number", "not-a-number"),
        ("/task done 0", "0"),  # "0" passes isdigit() but violates task_id's ge=1
    ],
)
def test_rejected_commands_report_an_actionable_message(
    raw_text: str, expected_in_message: str
) -> None:
    with pytest.raises(CommandParseError, match=expected_in_message):
        parse_command(raw_text)


def test_add_missing_title_and_bad_date_reports_both_at_once() -> None:
    """The error collection pattern: two problems, one report."""
    with pytest.raises(CommandParseError) as exc_info:
        parse_command("/task add due 13/45/2026")
    message = str(exc_info.value)
    assert "title" in message
    assert "date format" in message

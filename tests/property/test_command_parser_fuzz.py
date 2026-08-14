"""Technique 5: property-based fuzzing. The property under test: `parse_command`
must never crash with anything other than `CommandParseError` on arbitrary
text — inputs a human writing examples by hand wouldn't think to try."""

from __future__ import annotations

import contextlib

import pytest
from hypothesis import given
from hypothesis import strategies as st

from oreilly_hardening_codebase_course.engines.command_parser import (
    CommandParseError,
    parse_command,
)

pytestmark = pytest.mark.property


@given(st.text())
def test_parse_command_only_ever_raises_command_parse_error(raw_text: str) -> None:
    with contextlib.suppress(CommandParseError):
        parse_command(raw_text)


@given(st.text(min_size=1).filter(lambda s: s.strip()))
def test_add_with_arbitrary_title_round_trips_or_is_rejected(title: str) -> None:
    raw_text = f"/task add {title}"
    try:
        command = parse_command(raw_text)
    except CommandParseError:
        return
    assert command.action == "add"
    assert command.title


@given(st.integers(min_value=1, max_value=10_000_000))
def test_done_with_any_positive_integer_id_parses_that_id(task_id: int) -> None:
    command = parse_command(f"/task done {task_id}")
    assert command.task_id == task_id


@given(st.integers(min_value=-1_000, max_value=0))
def test_done_with_zero_or_negative_id_is_rejected_not_crashed(task_id: int) -> None:
    with pytest.raises(CommandParseError):
        parse_command(f"/task done {task_id}")

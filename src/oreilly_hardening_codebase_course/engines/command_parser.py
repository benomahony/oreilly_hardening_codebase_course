"""Turns raw chat text into a validated `TaskCommand`, or an actionable
error via the error collection pattern (commons/errors.py) — every problem
in a command is reported at once, not just the first. See
tests/unit/test_command_parser.py."""

from __future__ import annotations

from datetime import date

from oreilly_hardening_codebase_course.commons.errors import (
    ErrorCollector,
    invalid_task_id,
    missing_title,
    title_too_long,
    unknown_action,
    unknown_command,
    unrecognized_date,
)
from oreilly_hardening_codebase_course.commons.models import MAX_TITLE_LENGTH, TaskCommand
from oreilly_hardening_codebase_course.commons.state import ParseContext

SUPPORTED_ACTIONS = frozenset({"add", "done", "list", "remove", "help"})


class CommandParseError(Exception):
    """Raised with an already-rendered, actionable message (see commons/errors.py)."""


def _tokenize(raw_text: str) -> ParseContext:
    assert isinstance(raw_text, str), "raw_text must be a string"
    assert raw_text is not None, "raw_text must not be None"
    tokens = raw_text.strip().split()
    return {"raw_text": raw_text, "tokens": tokens, "token_count": len(tokens)}


def parse_command(raw_text: str) -> TaskCommand:
    assert isinstance(raw_text, str), "raw_text must be a string"
    ctx = _tokenize(raw_text)
    assert ctx["token_count"] == len(ctx["tokens"]), "token_count out of sync with tokens"

    collector = ErrorCollector()
    tokens = ctx["tokens"]

    if not tokens or tokens[0] != "/task":
        collector.add(unknown_command(raw_text))
        raise CommandParseError(collector.render())

    if len(tokens) < 2 or tokens[1] not in SUPPORTED_ACTIONS:
        action_word = tokens[1] if len(tokens) >= 2 else ""
        collector.add(unknown_action(action_word))
        raise CommandParseError(collector.render())

    action = tokens[1]
    remainder = tokens[2:]

    if action in ("list", "help"):
        return TaskCommand(action=action, raw_text=raw_text)

    if action in ("done", "remove"):
        return _parse_id_command(action, remainder, raw_text, collector)

    assert action == "add", f"unexpected action after validation: {action}"
    return _parse_add_command(remainder, raw_text, collector)


def _parse_id_command(
    action: str, remainder: list[str], raw_text: str, collector: ErrorCollector
) -> TaskCommand:
    assert action in ("done", "remove"), f"_parse_id_command called with wrong action: {action}"
    assert isinstance(remainder, list), "remainder must be a list of tokens"
    raw_id = remainder[0] if remainder else ""
    # `isdigit()` alone lets "0" through, which violates task_id's ge=1.
    if not raw_id.isdigit() or int(raw_id) < 1:
        collector.add(invalid_task_id(raw_id))
        raise CommandParseError(collector.render())
    return TaskCommand(action=action, task_id=int(raw_id), raw_text=raw_text)


def _parse_add_command(
    remainder: list[str], raw_text: str, collector: ErrorCollector
) -> TaskCommand:
    assert isinstance(remainder, list), "remainder must be a list of tokens"
    assert isinstance(collector, ErrorCollector), "collector must be an ErrorCollector"

    if "due" in remainder:
        due_index = remainder.index("due")
        title_tokens = remainder[:due_index]
        due_tokens = remainder[due_index + 1 :]
    else:
        title_tokens = remainder
        due_tokens = []

    title = " ".join(title_tokens).strip()
    if not title:
        collector.add(missing_title())
    elif len(title) > MAX_TITLE_LENGTH:
        collector.add(title_too_long(title, MAX_TITLE_LENGTH))

    due_value: date | None = None
    if "due" in remainder:
        raw_due = due_tokens[0] if due_tokens else ""
        try:
            due_value = date.fromisoformat(raw_due) if raw_due else None
            if due_value is None:
                collector.add(unrecognized_date(raw_due))
        except ValueError:
            collector.add(unrecognized_date(raw_due))

    if collector.has_errors:
        raise CommandParseError(collector.render())

    return TaskCommand(action="add", title=title, due=due_value, raw_text=raw_text)

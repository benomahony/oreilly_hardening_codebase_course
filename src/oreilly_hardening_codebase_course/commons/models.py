"""Technique 1: type safety with Pydantic models. Every boundary of the bot
(parsed commands, stored tasks, results) is a `BaseModel` — bad data is
rejected at construction, not three functions later as a `KeyError`. See
tests/unit/test_models.py."""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

CommandAction = Literal["add", "done", "list", "remove", "help"]

MAX_TITLE_LENGTH = 200
"""Shared by Task/TaskCommand's Field constraint and the parser's
pre-check in engines/command_parser.py, so the two can't drift apart."""


class Task(BaseModel):
    id: int = Field(ge=1)
    title: str = Field(min_length=1, max_length=MAX_TITLE_LENGTH)
    done: bool = False
    due: date | None = None


class TaskCommand(BaseModel):
    """Contract between `engines.command_parser` and `engines.task_engine`
    — see docs/contracts/task_command_contract.md."""

    action: CommandAction
    title: str | None = Field(default=None, max_length=MAX_TITLE_LENGTH)
    due: date | None = None
    task_id: int | None = Field(default=None, ge=1)
    raw_text: str


class CommandResult(BaseModel):
    ok: bool
    message: str
    task: Task | None = None

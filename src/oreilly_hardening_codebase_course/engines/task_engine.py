"""Technique 4 (defensive assertions) + technique 13 (dependency injection):
`TaskEngine` depends on the `TaskStore` Protocol, never a concrete store —
constructor injection, no framework required. See
tests/unit/test_task_engine.py."""

from __future__ import annotations

from oreilly_hardening_codebase_course.commons.errors import already_done, unknown_task_id
from oreilly_hardening_codebase_course.commons.metrics import BotMetrics
from oreilly_hardening_codebase_course.commons.models import CommandResult, TaskCommand
from oreilly_hardening_codebase_course.commons.protocols import TaskStore


class TaskEngine:
    def __init__(self, store: TaskStore, metrics: BotMetrics | None = None) -> None:
        assert store is not None, "store must not be None"
        assert hasattr(store, "add") and hasattr(store, "list_all"), (
            "store must implement the TaskStore protocol"
        )
        self.store = store
        self.metrics = metrics if metrics is not None else BotMetrics()

    def handle(self, command: TaskCommand) -> CommandResult:
        assert isinstance(command, TaskCommand), "command must be a TaskCommand"
        assert command.action in ("add", "done", "list", "remove", "help"), (
            f"unknown action reached the engine: {command.action}"
        )

        handler = {
            "add": self._handle_add,
            "done": self._handle_done,
            "list": self._handle_list,
            "remove": self._handle_remove,
            "help": self._handle_help,
        }[command.action]
        result = handler(command)
        self.metrics.record_command(failed=not result.ok)
        return result

    def _handle_add(self, command: TaskCommand) -> CommandResult:
        assert command.title, "add command reached the engine without a title"
        assert command.action == "add", "wrong handler dispatched"
        task = self.store.add(title=command.title, due=command.due)
        self.metrics.record_task_created()
        return CommandResult(ok=True, message=f"Added task #{task.id}: {task.title}", task=task)

    def _handle_done(self, command: TaskCommand) -> CommandResult:
        assert command.task_id is not None, "done command reached the engine without a task_id"
        assert command.action == "done", "wrong handler dispatched"
        existing = self.store.get(command.task_id)
        if existing is None:
            return CommandResult(ok=False, message=unknown_task_id(command.task_id).render())
        if existing.done:
            return CommandResult(
                ok=True, message=already_done(command.task_id).render(), task=existing
            )
        task = self.store.mark_done(command.task_id)
        assert task is not None, "mark_done returned None right after store.get() found the task"
        self.metrics.record_task_completed()
        return CommandResult(ok=True, message=f"Marked task #{task.id} done.", task=task)

    def _handle_list(self, command: TaskCommand) -> CommandResult:
        assert command.action == "list", "wrong handler dispatched"
        tasks = self.store.list_all()
        assert isinstance(tasks, list), "store.list_all() must return a list"
        if not tasks:
            return CommandResult(ok=True, message="No tasks yet. Try /task add <title>.")
        summary = "; ".join(f"#{t.id} {'[x]' if t.done else '[ ]'} {t.title}" for t in tasks)
        return CommandResult(ok=True, message=summary)

    def _handle_remove(self, command: TaskCommand) -> CommandResult:
        assert command.task_id is not None, "remove command reached the engine without a task_id"
        assert command.action == "remove", "wrong handler dispatched"
        removed = self.store.remove(command.task_id)
        if not removed:
            return CommandResult(ok=False, message=unknown_task_id(command.task_id).render())
        return CommandResult(ok=True, message=f"Removed task #{command.task_id}.")

    def _handle_help(self, command: TaskCommand) -> CommandResult:
        assert command.action == "help", "wrong handler dispatched"
        result = CommandResult(
            ok=True,
            message=(
                "Commands: /task add <title> [due yyyy-mm-dd], /task list, "
                "/task done <id>, /task remove <id>."
            ),
        )
        assert result.ok, "_handle_help must always report ok=True"
        return result

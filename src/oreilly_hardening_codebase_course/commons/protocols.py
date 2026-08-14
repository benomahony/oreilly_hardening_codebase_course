"""Technique 3: Protocol classes for DI. `TaskEngine` depends on this
interface, not a concrete store — production wires up
`engines.store.JsonFileTaskStore`, tests wire up
`tests.fakes.InMemoryTaskStore` (technique 11: a fake, not a Mock).
Structural typing means a fake never inherits from this — it just needs
matching methods, checked statically by basedpyright."""

from __future__ import annotations

from datetime import date
from typing import Protocol

from oreilly_hardening_codebase_course.commons.models import Task


class TaskStore(Protocol):
    """Persistence boundary for tasks. See engines/store.py and tests/fakes.py."""

    def add(self, title: str, due: date | None) -> Task:
        """Create and persist a new task, returning it with an assigned id."""
        ...

    def get(self, task_id: int) -> Task | None:
        """Return the task with `task_id`, or None if it doesn't exist."""
        ...

    def list_all(self) -> list[Task]:
        """Return every stored task, in creation order."""
        ...

    def mark_done(self, task_id: int) -> Task | None:
        """Mark a task done and return it, or None if it doesn't exist."""
        ...

    def remove(self, task_id: int) -> bool:
        """Delete a task. Returns whether a task was actually removed."""
        ...

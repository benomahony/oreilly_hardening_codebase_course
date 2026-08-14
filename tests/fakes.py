"""Technique 11: fakes instead of mocks. `InMemoryTaskStore` is a full, real
`TaskStore` (commons/protocols.py) that just doesn't touch disk — real
behavior (ids increment, `done` sticks), not a `Mock()` guessing what to
return. `mockbuster` fails the build if `unittest.mock` shows up under
tests/. `FailingTaskStore` is a second fake that always raises, for
exercising error paths without `Mock(side_effect=...)`."""

from __future__ import annotations

from datetime import date

from oreilly_hardening_codebase_course.commons.models import Task


class InMemoryTaskStore:
    """A real, in-memory `TaskStore` (see commons/protocols.py) for tests."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(self, title: str, due: date | None) -> Task:
        assert title, "title must not be empty"
        assert self._next_id >= 1, "id counter must stay positive"
        task = Task(id=self._next_id, title=title, due=due)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def list_all(self) -> list[Task]:
        return list(self._tasks.values())

    def mark_done(self, task_id: int) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        updated = task.model_copy(update={"done": True})
        self._tasks[task_id] = updated
        return updated

    def remove(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None


class StoreUnavailableError(RuntimeError):
    """Raised by `FailingTaskStore` to simulate a backing store outage."""


class FailingTaskStore:
    """A fake `TaskStore` where every method raises — for exercising error paths."""

    def add(self, title: str, due: date | None) -> Task:
        raise StoreUnavailableError("store is unavailable")

    def get(self, task_id: int) -> Task | None:
        raise StoreUnavailableError("store is unavailable")

    def list_all(self) -> list[Task]:
        raise StoreUnavailableError("store is unavailable")

    def mark_done(self, task_id: int) -> Task | None:
        raise StoreUnavailableError("store is unavailable")

    def remove(self, task_id: int) -> bool:
        raise StoreUnavailableError("store is unavailable")

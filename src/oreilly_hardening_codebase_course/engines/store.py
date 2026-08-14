"""The production `TaskStore`: a JSON file on disk, deliberately simple
(no locking, no migrations). Tests use `tests.fakes.InMemoryTaskStore`
instead (technique 11: a fake, not a mock)."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from oreilly_hardening_codebase_course.commons.models import Task


class StoreCorruptedError(Exception):
    """Raised when the backing JSON file can't be parsed as a task list.

    See docs/runbooks/recover_corrupted_store.md for how to recover from
    this in practice.
    """


class StoreUnavailableError(Exception):
    """Raised when the store file can't be read or written for filesystem
    reasons (permissions, missing parent directory, disk full, ...).
    """


class JsonFileTaskStore:
    """A `TaskStore` (commons/protocols.py), satisfied structurally —
    no inheritance, just matching methods."""

    def __init__(self, path: Path) -> None:
        assert isinstance(path, Path), "path must be a Path"
        assert not path.is_dir(), "path must not be an existing directory"
        self._path = path

    def _read(self) -> list[Task]:
        if not self._path.exists():
            return []
        try:
            raw = json.loads(self._path.read_text())
        except json.JSONDecodeError as exc:
            raise StoreCorruptedError(
                f"{self._path} is not valid JSON. See docs/runbooks/recover_corrupted_store.md."
            ) from exc
        except OSError as exc:
            raise StoreUnavailableError(f"Couldn't read {self._path}: {exc}.") from exc
        assert isinstance(raw, list), f"{self._path} must contain a JSON array"
        tasks = [Task.model_validate(item) for item in raw]
        assert all(isinstance(t, Task) for t in tasks), "model_validate must produce Task instances"
        return tasks

    def _write(self, tasks: list[Task]) -> None:
        assert isinstance(tasks, list), "tasks must be a list"
        payload = [task.model_dump(mode="json") for task in tasks]
        try:
            self._path.write_text(json.dumps(payload, indent=2))
        except OSError as exc:
            raise StoreUnavailableError(
                f"Couldn't write to {self._path}: {exc}. "
                "Check the directory exists and is writable."
            ) from exc
        assert self._path.exists(), "write did not create the store file"

    def add(self, title: str, due: date | None) -> Task:
        assert title, "title must not be empty"
        assert len(title) <= 200, "title must be at most 200 characters"
        tasks = self._read()
        next_id = max((t.id for t in tasks), default=0) + 1
        task = Task(id=next_id, title=title, due=due)
        tasks.append(task)
        self._write(tasks)
        return task

    def get(self, task_id: int) -> Task | None:
        assert task_id >= 1, "task_id must be positive"
        result = next((t for t in self._read() if t.id == task_id), None)
        assert result is None or result.id == task_id, "get() returned a task with the wrong id"
        return result

    def list_all(self) -> list[Task]:
        tasks = self._read()
        assert isinstance(tasks, list), "_read() must return a list"
        ids = [t.id for t in tasks]
        assert len(ids) == len(set(ids)), "store contains duplicate task ids"
        return tasks

    def mark_done(self, task_id: int) -> Task | None:
        assert task_id >= 1, "task_id must be positive"
        tasks = self._read()
        for index, task in enumerate(tasks):
            if task.id == task_id:
                updated = task.model_copy(update={"done": True})
                assert updated.done is True, "mark_done must set done=True"
                tasks[index] = updated
                self._write(tasks)
                return updated
        return None

    def remove(self, task_id: int) -> bool:
        assert task_id >= 1, "task_id must be positive"
        tasks = self._read()
        remaining = [t for t in tasks if t.id != task_id]
        assert len(remaining) <= len(tasks), "remove must not increase the task count"
        removed = len(remaining) != len(tasks)
        if removed:
            self._write(remaining)
        return removed

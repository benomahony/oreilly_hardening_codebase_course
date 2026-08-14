import os
import platform
from datetime import date
from pathlib import Path

import pytest

from oreilly_hardening_codebase_course.engines.store import (
    JsonFileTaskStore,
    StoreCorruptedError,
    StoreUnavailableError,
)

pytestmark = pytest.mark.unit

_root_bypasses_permissions = platform.system() != "Windows" and os.geteuid() == 0


@pytest.fixture
def store(tmp_path: Path) -> JsonFileTaskStore:
    return JsonFileTaskStore(tmp_path / "tasks.json")


def test_add_then_list_round_trips_through_disk(store: JsonFileTaskStore) -> None:
    added = store.add(title="Buy milk", due=date(2026, 8, 20))
    assert store.list_all() == [added]


def test_ids_increment_across_writes(store: JsonFileTaskStore) -> None:
    first = store.add(title="First", due=None)
    second = store.add(title="Second", due=None)
    assert second.id == first.id + 1


def test_mark_done_persists(store: JsonFileTaskStore) -> None:
    task = store.add(title="Buy milk", due=None)
    store.mark_done(task.id)
    assert store.get(task.id).done is True  # type: ignore[union-attr]


def test_mark_done_on_missing_id_returns_none(store: JsonFileTaskStore) -> None:
    assert store.mark_done(999) is None


def test_remove_deletes_the_task(store: JsonFileTaskStore) -> None:
    task = store.add(title="Buy milk", due=None)
    assert store.remove(task.id) is True
    assert store.list_all() == []


def test_remove_on_missing_id_returns_false(store: JsonFileTaskStore) -> None:
    assert store.remove(999) is False


def test_corrupted_store_file_raises_with_a_pointer_to_the_runbook(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"
    path.write_text("{not valid json at all")
    with pytest.raises(StoreCorruptedError, match="runbook"):
        JsonFileTaskStore(path).list_all()


@pytest.mark.skipif(_root_bypasses_permissions, reason="root ignores file permission bits")
def test_write_failure_raises_store_unavailable_error(tmp_path: Path) -> None:
    """A read-only store directory must raise StoreUnavailableError, not a
    raw PermissionError. Uses a real read-only directory, not a mock."""
    readonly_dir = tmp_path / "readonly"
    readonly_dir.mkdir()
    readonly_dir.chmod(0o555)
    try:
        with pytest.raises(StoreUnavailableError, match="Couldn't write"):
            JsonFileTaskStore(readonly_dir / "tasks.json").add(title="Buy milk", due=None)
    finally:
        readonly_dir.chmod(0o755)

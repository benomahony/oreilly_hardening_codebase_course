# Runbook: recover a corrupted task store

**When:** any `chatops` command exits with a `store error` panel
mentioning `StoreCorruptedError` — the store's JSON file is malformed
(killed mid-write, bad hand-edit).

Technique 15: this runbook *is* the test — every step runs for real via
pytest-examples, so it can't quietly go stale.

## Step 1 — reproduce the failure

```python
import tempfile
from pathlib import Path

from oreilly_hardening_codebase_course.engines.store import JsonFileTaskStore, StoreCorruptedError

with tempfile.TemporaryDirectory() as tmp_dir:
    store_path = Path(tmp_dir) / "tasks.json"
    store_path.write_text("{not valid json at all")  # simulates a killed mid-write
    store = JsonFileTaskStore(store_path)

    try:
        store.list_all()
    except StoreCorruptedError as exc:
        assert "not valid JSON" in str(exc)
    else:
        raise AssertionError("expected StoreCorruptedError")
```

## Step 2 — check whether it's salvageable

Before discarding the file, check whether the damage is small enough to
hand-fix (a truncated last record) rather than losing every task:

```python
import json
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp_dir:
    store_path = Path(tmp_dir) / "tasks.json"
    store_path.write_text('[{"id": 1, "title": "Buy milk", "done": false, "due": null}')
    raw = store_path.read_text()

    try:
        json.loads(raw)
        recoverable = False
    except json.JSONDecodeError:
        recoverable = json.loads(raw + "]") is not None  # a truncated array closes cleanly

    assert recoverable
```

## Step 3 — reset and replay if unsalvageable

Reset the store and replay any commands you have a record of through
`chatops handle` — each `add`/`done`/`remove` is idempotent enough to
replay by hand. Resetting is deliberate, never automatic:

```python
import tempfile
from pathlib import Path

from oreilly_hardening_codebase_course.engines.store import JsonFileTaskStore

with tempfile.TemporaryDirectory() as tmp_dir:
    store_path = Path(tmp_dir) / "tasks.json"
    store_path.write_text("{not valid json at all")

    store_path.unlink()  # equivalent to `chatops reset --config ...`
    store = JsonFileTaskStore(store_path)

    assert store.list_all() == []  # fresh store, ready to replay commands into
```

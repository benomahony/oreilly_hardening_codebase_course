# Contract: `TaskCommand`

**Producer:** `engines.command_parser.parse_command`
**Consumer:** `engines.task_engine.TaskEngine.handle`

Enforced by `commons.models.TaskCommand` and checked by the executable
examples below — pytest-examples runs them in CI, so this doc can't drift
from the code without a test failing.

## Fields

| field      | type                | rule                                              |
| ---------- | ------------------- | -------------------------------------------------- |
| `action`   | one of the 5 actions | `add`, `done`, `list`, `remove`, `help`            |
| `title`    | `str \| None`        | required for `add`; ≤ 200 characters                |
| `due`      | `date \| None`       | optional, ISO 8601 (`yyyy-mm-dd`)                   |
| `task_id`  | `int \| None`        | required for `done`/`remove`; ≥ 1                    |
| `raw_text` | `str`                | always set — the original message, for audit/replay |

The "≤ 200" cell above is prose, unlike every other rule here — tied to
the real constant so it can't drift silently:

```python
from oreilly_hardening_codebase_course.commons.models import MAX_TITLE_LENGTH

assert MAX_TITLE_LENGTH == 200, "update the table above if this changes"
```

## Rule: `add` requires a non-empty title, ≤ `MAX_TITLE_LENGTH`

The parser rejects a missing title before constructing the model (an
actionable error, not a validation exception); the model itself is the
second line of defense against an overlong one:

```python
import pydantic
from oreilly_hardening_codebase_course.commons.models import MAX_TITLE_LENGTH, TaskCommand

command = TaskCommand(action="add", title="Buy milk", raw_text="/task add Buy milk")
assert command.title == "Buy milk"

try:
    TaskCommand(action="add", title="x" * (MAX_TITLE_LENGTH + 1), raw_text="/task add ...")
except pydantic.ValidationError as exc:
    assert "title" in str(exc)
else:
    raise AssertionError("expected a ValidationError for an overlong title")
```

## Rule: `done`/`remove` require a positive `task_id`

```python
import pydantic
from oreilly_hardening_codebase_course.commons.models import TaskCommand

try:
    TaskCommand(action="done", task_id=0, raw_text="/task done 0")
except pydantic.ValidationError as exc:
    assert "task_id" in str(exc)
else:
    raise AssertionError("expected a ValidationError for task_id=0")
```

## Rule: `list`/`help` ignore `title`, `due`, and `task_id`

```python
from oreilly_hardening_codebase_course.commons.models import TaskCommand

command = TaskCommand(action="list", raw_text="/task list")
assert command.title is None
assert command.task_id is None
```

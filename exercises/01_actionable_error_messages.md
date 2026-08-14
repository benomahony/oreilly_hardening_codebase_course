# Exercise: writing actionable error messages (Google Chat guidance)

Source: [Write error messages for Google Chat apps](https://developers.google.com/workspace/chat/write-error-messages)

## The guidance

Google's rule, in three parts: (1) name the problem, (2) give a concrete
next step, ideally with an example, (3) point to more help.

- Bad: *"Enter the correct date format."* — assumes the user knows what
  "correct" means.
- Good: *"I don't recognize the date format you entered. Write dates as
  yyyy-mm-dd; for example, 2000-01-31. For help, type /help."*

Checked mechanically, not just by eye:

```python
from oreilly_hardening_codebase_course.commons.errors import is_actionable

bad = "Enter the correct date format."
good = (
    "I don't recognize the date format you entered. "
    "Write dates as yyyy-mm-dd; for example, 2000-01-31. "
    "For help, type /help."
)

assert not is_actionable(bad)
assert is_actionable(good)
```

`is_actionable` is a heuristic (length + terminal punctuation), not real
NLP — enough to catch a regression to "An error occurred" in CI, not
enough to certify a message is actually helpful. That's why
`commons/errors.py` has one factory per distinct problem instead of one
generic `error(msg)`: each forces a separate problem and solution.

## Worked example: "you already did that"

Without a check, `/task done <id>` on an already-completed task would
silently "succeed" a second time with no signal that nothing changed — the
same ambiguity Google's guidance warns about, for a no-op instead of a
failure. Three pieces close that gap:

1. `commons/errors.py::already_done` — a new `ActionableError` factory.
2. `engines/task_engine.py::TaskEngine._handle_done` — calls `store.get()`
   first to tell "already done" apart from "just completed."
3. `tests/unit/test_task_engine.py::test_marking_an_already_done_task_done_again_says_so_instead_of_pretending`
   — the regression test.

```python
from oreilly_hardening_codebase_course.commons.models import TaskCommand
from oreilly_hardening_codebase_course.engines.task_engine import TaskEngine
from tests.fakes import InMemoryTaskStore

engine = TaskEngine(store=InMemoryTaskStore())
added = engine.handle(TaskCommand(action="add", title="Ship it", raw_text="/task add Ship it"))
task_id = added.task.id
engine.handle(TaskCommand(action="done", task_id=task_id, raw_text=f"/task done {task_id}"))

result = engine.handle(
    TaskCommand(action="done", task_id=task_id, raw_text=f"/task done {task_id}")
)
assert result.ok
assert "already marked done" in result.message
```

## Try it yourself

`/task add <title> due <date>` accepts a past date without comment —
`"due 2020-01-01"` today "succeeds" with the same message as any other
add. Using the same three-piece pattern:

1. Add an `ActionableError` factory to `commons/errors.py` — is a past due
   date an error (reject, like `unrecognized_date`) or a warning (accept,
   but say something, like `already_done`)? Justify your choice.
2. Wire it into `engines/command_parser.py` (rejecting) or
   `engines/task_engine.py` (warning-and-accepting).
3. Write the regression test first — it should fail against current code,
   then pass once your change lands.

No answer key checked in — compare notes with a partner, or check your
solution against `already_done` once you're done.

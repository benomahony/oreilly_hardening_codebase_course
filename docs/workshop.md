# Workshop: hardening a codebase for agentic coding

Self-paced, independent of each other and of anyone else's state. Each
one: break something small on purpose, run the tool that catches it,
revert, confirm green.

Every tool used below is Python's implementation of a language-agnostic
idea — see the table in `README.md` for the mapping.

```bash
uv sync && uv run pytest -q   # should say 85 passed before you touch anything
```

## If this were a real legacy codebase

The sections below are ordered for teaching — one idea at a time. Applying
this to an actual legacy codebase, the order is different:

1. **Get tests working.** A baseline suite, however thin, before anything
   else changes.
2. **Strip out mocks.** Replace with fakes so the suite you just got
   working is actually trustworthy, not just green.
3. **Add the pre-commit hook stack.** Not to fix everything today — to
   guarantee every file gets brought up to spec the next time anyone
   touches it.
4. **For any new feature: types and assertions from the start.** New code
   doesn't get the opportunistic treatment above — it's written to the
   full standard immediately, not retrofitted later.

Everything else here (architecture tests, fuzzing, contracts, runbooks)
layers on top once those four are in place.

---

## Actionable error messages

`commons/errors.py` is what every rejected command in this bot renders
through — Google's three-part rule: name the problem, give the fix, point
to help. `exercises/01_actionable_error_messages.md` has the worked
example (`already_done`) and an open half: past-due dates are currently
accepted with no comment. Decide error vs. warning, add an
`ActionableError` factory, wire it into `engines/command_parser.py` or
`engines/task_engine.py`, and write the regression test *before* the fix.

---

## Architecture tests

1. Append to `src/oreilly_hardening_codebase_course/commons/errors.py`:
   ```diff
   from oreilly_hardening_codebase_course.engines.task_engine import TaskEngine
   ```
2. `uv run pytest tests/architecture/ -q` → fails, naming the exact file and
   forbidden import.
3. Delete the line. Confirm: `uv run pytest tests/architecture/ -q` → 8 passed.

**Why:** nothing stops an agent adding a "helpful" import like this by
accident — an AST-based test does, a comment doesn't.

---

## pytest-examples catches doc drift, not just syntax

1. In `commons/errors.py::already_done`, change
   `f"Task #{task_id} is already marked done."` to `"... is done already."`
2. `uv run pytest -m doc -q` → `exercises/01_actionable_error_messages.md`
   fails: its worked example asserts the exact original phrase.
3. Revert the wording. Confirm: `uv run pytest -m doc -q` → all pass.

**Why:** pytest-examples *runs* doc code against the real implementation —
changing behavior without updating docs breaks CI, not just the docs. Try
the same trick on `docs/runbooks/recover_corrupted_store.md` by rewording
`StoreCorruptedError`'s message in `engines/store.py` instead.

---

## Hypothesis profiles: `dev` vs `ci`

1. In `engines/command_parser.py::_parse_add_command`, delete the
   `elif len(title) > MAX_TITLE_LENGTH: collector.add(title_too_long(...))`
   branch, leaving only the `if not title` check.
2. `uv run pytest tests/property/test_command_parser_fuzz.py::test_add_with_arbitrary_title_round_trips_or_is_rejected -q`
   — with the default `dev` profile (100 examples), this probably **passes**.
3. `HYPOTHESIS_PROFILE=ci uv run pytest tests/property/test_command_parser_fuzz.py::test_add_with_arbitrary_title_round_trips_or_is_rejected -q`
   — with `ci` (1000 examples), this **fails reliably**, shrunk to a
   201-character minimal counterexample.
4. Restore the `elif` block. Confirm: `uv run pytest tests/property/ -q` → 7 passed.

**Why:** `dev` is fast enough for the inner loop; only `ci`'s example count
has the statistical power to reliably catch a bug like this one. Run purely
on `dev`, this class of bug can sit in the codebase indefinitely.

---

## nasa-lsp and assertion density

1. In `engines/store.py::list_all`, delete both `assert` lines, leaving
   just `tasks = self._read()` / `return tasks`.
2. `uv run nasa lint src/oreilly_hardening_codebase_course/engines` →
   `NASA05 Function 'list_all' has only 0 assert(s) ... expected at least 2`.
3. Restore both asserts. Confirm: `4 files checked, no violations`.

**Why:** NASA Rule 5 is assertion *density* as a defect-catching strategy,
genuinely tool-enforceable. This check is scoped to `engines/` only — try
`nasa lint src` unscoped and see how many one-line Protocol stubs and CLI
commands light up. Padding those with never-failing asserts would itself
violate the rule. Where would you draw that line in your own codebase?

---

## mockbuster

1. Add to `tests/unit/test_metrics.py`:
   ```diff
   from unittest.mock import Mock

   def test_demo_mock():
       Mock().record_command(failed=True)
   ```
2. `uv run mockbuster --strict tests` → names the file and line:
   `Mock() instantiation detected - Use real objects, dependency injection,
   or integration tests`.
3. Delete what you added. Confirm: `No mocking usage detected`.

**Why:** compare to `tests/fakes.py::FailingTaskStore` and
`test_engine_propagates_store_outage_instead_of_hiding_it`. A `Mock()`
never raises unless told to; the real fake reproduces the actual failure
mode. That's what mockbuster protects.

---

## Store errors reaching the CLI as a raw traceback

1. Point the CLI at a store it can't write to:
   ```bash
   mkdir -p /tmp/readonly-demo && chmod 555 /tmp/readonly-demo
   echo '{"store_path": "/tmp/readonly-demo/tasks.json"}' > /tmp/readonly-config.json
   uv run chatops handle "/task add test" --config /tmp/readonly-config.json
   ```
   You get a clean red `store error` panel — `_run_store_op` in `cli.py`
   converts the exception into it.
2. In `cli.py::handle`, temporarily replace
   `result = _run_store_op(lambda: engine.handle(command))` with
   `result = engine.handle(command)`, then rerun the same command — this
   time a raw `StoreUnavailableError` traceback, not a panel.
3. Restore the line. Clean up:
   ```bash
   chmod 755 /tmp/readonly-demo && rm -rf /tmp/readonly-demo /tmp/readonly-config.json
   uv run pytest -q   # 85 passed
   ```

**Why:** `_run_store_op` only wraps calls that go through it — every CLI
command touching the store has to opt in. "We handle errors" and "we
handle the specific errors we routed through the helper" are different
claims; pointing the CLI at a broken filesystem checks this directly
instead of trusting that every command remembered to opt in.

---

## deptry and a config gap that looks like a code bug

1. Comment out `known_first_party = [...]` in `pyproject.toml`.
2. `uv run deptry .` → 13 `DEP003` findings, all claiming the project's own
   modules are "transitive dependencies."
3. Uncomment it. Confirm: `Success! No dependency issues found.`

**Why:** not every finding is a source bug — this one was deptry failing
to map the hyphenated project name to the underscored module name. Fixed
with one config line, not a code change.

---

## Run the whole stack

```bash
uv run pytest -q --cov && uv run ruff check . && uv run ruff format --check .
uv run basedpyright && uv run vulture && uv run bandit -c pyproject.toml -r src
uv run deptry . && uv run mockbuster --strict tests
uv run nasa lint src/oreilly_hardening_codebase_course/engines
uv run cliqa analyze chatops
```

Everything clean except cliqa's 2 expected warnings (`no_color`,
`subcommand_discovery` — see `cli.py`'s docstring for why those stay).
Bonus: argue for or against fixing one of them anyway.

## Other findings, not worth a full lab

- **basedpyright**: `CommandResult.task: Task | None` is flagged even on
  the success path (`reportOptionalMemberAccess`) — suppressed with
  `type: ignore`, not fixed. Documented debt.
- **Test markers**: a test with no `pytestmark` is invisible to every
  `-m <marker>` run. Comparing marker-count totals against
  `pytest --collect-only`'s full count exposes untagged tests directly.
- **Layer architecture**: `tests/architecture/` checks `commons` never
  imports `engines`, but nothing currently checks `src` never imports
  `tests` — a real gap, not just a hypothetical one.
- **cliqa**: also flags `-h`, `--version`, and `--help` examples support —
  all present in `cli.py`.
- **Structured metrics**: `record_command(failed="yes")` raises
  `AssertionError` instead of silently corrupting the counter.
- **Error collection pattern**: `/task add due 13/45/2026` reports both
  the missing title and the bad date in one message, not just the first.
- **Config loading**: a malformed-JSON file and a schema violation both
  collapse into the same `ConfigError`, not two exception types callers
  must know about separately.

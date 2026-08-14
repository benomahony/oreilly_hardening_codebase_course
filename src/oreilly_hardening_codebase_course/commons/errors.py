from __future__ import annotations

from pydantic import BaseModel

DEFAULT_HELP_HINT = "Type /help to see all commands."
_TRY_COMMANDS = "Try /task add, /task list, /task done <id>, or /task remove <id>."


class ActionableError(BaseModel):
    """An error message shaped for a human to act on, not just a log line."""

    problem: str
    solution: str
    help_hint: str = DEFAULT_HELP_HINT

    def render(self) -> str:
        assert self.problem, "problem must be set before rendering"
        assert self.solution, "solution must be set before rendering"
        return f"{self.problem} {self.solution} {self.help_hint}"


def unrecognized_date(raw_value: str) -> ActionableError:
    problem = (
        f"I don't recognize the date format '{raw_value}'."
        if raw_value
        else "I need a date after 'due'."
    )
    return ActionableError(
        problem=problem, solution="Write dates as yyyy-mm-dd; for example, 2026-08-20."
    )


def invalid_task_id(raw_value: str) -> ActionableError:
    problem = (
        f"'{raw_value}' isn't a valid task id." if raw_value else "I need a task id to do that."
    )
    return ActionableError(
        problem=problem,
        solution="Run /task list to see valid task ids, then try again, e.g. /task done 3.",
    )


def missing_title() -> ActionableError:
    return ActionableError(
        problem="I can't add a task without a title.",
        solution="Send /task add <title>, for example /task add Buy milk.",
    )


def unknown_command(raw_text: str) -> ActionableError:
    """`raw_text` is the whole chat message, not a single token — it can
    contain newlines or run long, so it's normalized rather than asserted
    clean."""
    normalized = " ".join(raw_text.split()) or "(empty message)"
    if len(normalized) > 120:
        normalized = normalized[:117] + "..."
    return ActionableError(problem=f"I don't understand '{normalized}'.", solution=_TRY_COMMANDS)


def unknown_action(action: str) -> ActionableError:
    problem = (
        f"I don't understand the action '{action}'." if action else "I need an action after /task."
    )
    return ActionableError(problem=problem, solution=_TRY_COMMANDS)


def title_too_long(raw_title: str, max_length: int) -> ActionableError:
    return ActionableError(
        problem=f"That title is {len(raw_title)} characters, which is too long.",
        solution=f"Keep task titles to {max_length} characters or fewer.",
    )


def unknown_task_id(task_id: int) -> ActionableError:
    return ActionableError(
        problem=f"I couldn't find task #{task_id}.",
        solution="Run /task list to see valid task ids.",
    )


def already_done(task_id: int) -> ActionableError:
    return ActionableError(
        problem=f"Task #{task_id} is already marked done.",
        solution="Nothing to do — run /task list if you want to double-check.",
    )


def is_actionable(message: str) -> bool:
    """Heuristic: actionable messages name a problem and a fix, so they
    tend to run longer than a bare sentence and end with punctuation."""
    stripped = message.strip()
    return bool(stripped) and stripped.endswith((".", "?", "!")) and len(stripped.split()) >= 6


class ErrorCollector:
    """Accumulates ActionableErrors instead of failing on the first one."""

    def __init__(self) -> None:
        self._errors: list[ActionableError] = []

    def add(self, error: ActionableError) -> None:
        assert isinstance(error, ActionableError), "add() expects an ActionableError"
        self._errors.append(error)

    @property
    def has_errors(self) -> bool:
        return bool(self._errors)

    def render(self) -> str:
        assert self._errors, "render() called with nothing collected"
        return "\n".join(error.render() for error in self._errors)

"""Technique 18: the CLI as a debug interface (technique 16: Rich console).
`parse` exercises the parser alone; `handle`/`list`/`seed`/`reset` touch the
store. `cliqa` (.pre-commit-config.yaml) flags Rich's boxed "Commands" panel
as unparseable like a plain list — a deliberate trade-off, not a bug."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from typing import NoReturn

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from oreilly_hardening_codebase_course.commons.config import BotSettings, ConfigError, load_settings
from oreilly_hardening_codebase_course.engines.command_parser import (
    CommandParseError,
    parse_command,
)
from oreilly_hardening_codebase_course.engines.store import (
    JsonFileTaskStore,
    StoreCorruptedError,
    StoreUnavailableError,
)
from oreilly_hardening_codebase_course.engines.task_engine import TaskEngine

__version__ = "0.1.0"

app = typer.Typer(
    name="chatops",
    help="Debug CLI for the ChatOps task bot: parse, run, and inspect commands.",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    epilog=(
        "Examples:\n\n"
        "  chatops parse '/task add Buy milk due 2026-08-20'\n\n"
        "  chatops handle '/task add Buy milk'\n\n"
        "  chatops seed && chatops list"
    ),
)
console = Console(no_color=bool(os.environ.get("NO_COLOR")))

_config_option = typer.Option(None, "--config", help="Path to a JSON config file.")


def _version_callback(value: bool) -> bool:
    # Click replaces the option's value with this callback's return.
    if value:
        console.print(f"chatops {__version__}")
        raise typer.Exit()
    return value


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
) -> None:
    """Debug CLI for the ChatOps task bot: parse, run, and inspect commands."""
    assert isinstance(version, bool), "version must be a bool"  # eager callback does the real work


def _fail(title: str, message: str) -> NoReturn:
    assert isinstance(title, str) and title, "title must be a non-empty string"
    assert isinstance(message, str) and message, "message must be a non-empty string"
    console.print(Panel(message, title=title, border_style="red"))
    raise typer.Exit(code=1)


def _load_settings_or_exit(config: Path | None) -> BotSettings:
    try:
        return load_settings(config)
    except ConfigError as exc:
        _fail("config error", str(exc))


def _store_for(settings: BotSettings) -> JsonFileTaskStore:
    return JsonFileTaskStore(settings.store_path)


def _run_store_op[T](operation: Callable[[], T]) -> T:
    """Convert store failures into an actionable panel, not a raw traceback."""
    try:
        return operation()
    except (StoreCorruptedError, StoreUnavailableError) as exc:
        _fail("store error", str(exc))


@app.command()
def parse(text: str) -> None:
    """Run only the parser on TEXT — debug it without touching any store."""
    try:
        command = parse_command(text)
    except CommandParseError as exc:
        _fail("parse error", str(exc))
    console.print(
        Panel(command.model_dump_json(indent=2), title="parsed command", border_style="green")
    )


@app.command()
def handle(text: str, config: Path | None = _config_option) -> None:
    """Parse TEXT and run it end-to-end against the configured store."""
    settings = _load_settings_or_exit(config)
    try:
        command = parse_command(text)
    except CommandParseError as exc:
        _fail("rejected", str(exc))

    engine = TaskEngine(store=_store_for(settings))
    result = _run_store_op(lambda: engine.handle(command))

    style = "green" if result.ok else "red"
    console.print(Panel(result.message, title="ok" if result.ok else "failed", border_style=style))
    if not result.ok:
        raise typer.Exit(code=1)


@app.command(name="list")
def list_tasks(config: Path | None = _config_option) -> None:
    """Print every task in the store as a table."""
    settings = _load_settings_or_exit(config)
    tasks = _run_store_op(_store_for(settings).list_all)

    table = Table(title=f"Tasks ({settings.store_path})")
    table.add_column("id", justify="right")
    table.add_column("done")
    table.add_column("title")
    table.add_column("due")
    for task in tasks:
        table.add_row(str(task.id), "x" if task.done else " ", task.title, str(task.due or ""))
    console.print(table)


@app.command()
def seed(config: Path | None = _config_option) -> None:
    """Populate the store with a few example tasks, for exploring the CLI."""
    settings = _load_settings_or_exit(config)
    store = _store_for(settings)

    def _seed() -> None:
        for title in ("Write the hardening exercise", "Review PR #42", "Buy milk"):
            store.add(title=title, due=None)

    _run_store_op(_seed)
    console.print(f"[green]Seeded 3 example tasks into {settings.store_path}[/green]")


@app.command()
def reset(config: Path | None = _config_option) -> None:
    """Delete the store file, starting fresh."""
    settings = _load_settings_or_exit(config)
    try:
        settings.store_path.unlink(missing_ok=True)
    except OSError as exc:
        _fail("store error", str(exc))
    console.print(f"[yellow]Reset {settings.store_path}[/yellow]")


if __name__ == "__main__":
    app()

import os
import platform
from collections.abc import Iterator
from pathlib import Path

import pytest
from typer.testing import CliRunner

from oreilly_hardening_codebase_course.cli import app

pytestmark = pytest.mark.unit
runner = CliRunner()

_root_bypasses_permissions = platform.system() != "Windows" and os.geteuid() == 0


@pytest.fixture
def store_args(tmp_path: Path) -> list[str]:
    config_path = tmp_path / "config.json"
    config_path.write_text(f'{{"store_path": "{tmp_path / "tasks.json"}"}}')
    return ["--config", str(config_path)]


@pytest.fixture
def readonly_store_args(tmp_path: Path) -> Iterator[list[str]]:
    readonly_dir = tmp_path / "readonly"
    readonly_dir.mkdir()
    readonly_dir.chmod(0o555)
    config_path = tmp_path / "config.json"
    config_path.write_text(f'{{"store_path": "{readonly_dir / "tasks.json"}"}}')
    try:
        yield ["--config", str(config_path)]
    finally:
        readonly_dir.chmod(0o755)


def test_version_flag_prints_the_version_and_exits_zero() -> None:
    """`--version`'s eager Click callback must return the bool it was
    handed, not implicitly return None."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "chatops" in result.stdout


@pytest.mark.parametrize(
    ("text", "exit_code", "expected_in_stdout"),
    [
        ("/task add Buy milk", 0, "Buy milk"),
        ("/task frobnicate", 1, "frobnicate"),
    ],
)
def test_parse(text: str, exit_code: int, expected_in_stdout: str) -> None:
    result = runner.invoke(app, ["parse", text])
    assert result.exit_code == exit_code
    assert expected_in_stdout in result.stdout


def test_handle_add_then_list_round_trips(store_args: list[str]) -> None:
    assert runner.invoke(app, ["handle", "/task add Buy milk", *store_args]).exit_code == 0

    result = runner.invoke(app, ["list", *store_args])
    assert result.exit_code == 0
    assert "Buy milk" in result.stdout


def test_handle_unknown_task_id_exits_nonzero_with_actionable_message(
    store_args: list[str],
) -> None:
    result = runner.invoke(app, ["handle", "/task done 999", *store_args])
    assert result.exit_code == 1
    assert "999" in result.stdout


def test_seed_populates_three_tasks(store_args: list[str]) -> None:
    runner.invoke(app, ["seed", *store_args])
    result = runner.invoke(app, ["list", *store_args])
    assert result.exit_code == 0
    assert "Buy milk" in result.stdout


def test_reset_clears_the_store(store_args: list[str]) -> None:
    runner.invoke(app, ["seed", *store_args])
    assert runner.invoke(app, ["reset", *store_args]).exit_code == 0

    result = runner.invoke(app, ["list", *store_args])
    assert result.exit_code == 0
    assert "Buy milk" not in result.stdout


def test_handle_reports_config_error_for_malformed_config(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text("{not valid json")

    result = runner.invoke(app, ["handle", "/task list", "--config", str(config_path)])

    assert result.exit_code == 1
    assert "config error" in result.stdout


@pytest.mark.skipif(_root_bypasses_permissions, reason="root ignores file permission bits")
def test_handle_reports_store_error_instead_of_crashing_on_permission_denied(
    readonly_store_args: list[str],
) -> None:
    """A read-only store directory must produce a `store error` panel, not
    a raw traceback. Uses a real read-only directory, not a mock."""
    result = runner.invoke(app, ["handle", "/task add Buy milk", *readonly_store_args])
    assert result.exit_code == 1
    assert "store error" in result.stdout
    assert "Permission denied" in result.stdout


@pytest.mark.skipif(_root_bypasses_permissions, reason="root ignores file permission bits")
def test_seed_reports_store_error_instead_of_crashing_on_permission_denied(
    readonly_store_args: list[str],
) -> None:
    """`seed` must also report store failures as a panel, not crash."""
    result = runner.invoke(app, ["seed", *readonly_store_args])
    assert result.exit_code == 1
    assert "store error" in result.stdout

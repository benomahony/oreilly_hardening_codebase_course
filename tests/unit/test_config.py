import json
from pathlib import Path

import pytest

from oreilly_hardening_codebase_course.commons.config import BotSettings, ConfigError, load_settings

pytestmark = pytest.mark.unit


def test_load_settings_defaults_when_no_path_given() -> None:
    settings = load_settings(None)
    assert settings.store_path == Path("tasks.json")


def test_load_settings_defaults_when_file_missing(tmp_path: Path) -> None:
    settings = load_settings(tmp_path / "does-not-exist.json")
    assert settings.max_title_length == 200


def test_load_settings_reads_valid_config(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"max_title_length": 50}))

    settings = load_settings(config_path)

    assert settings.max_title_length == 50


@pytest.mark.parametrize(
    ("contents", "expected_in_message"),
    [
        ("{not valid json", "not valid JSON"),
        (json.dumps({"max_title_length": -5}), "failed validation"),
    ],
)
def test_load_settings_rejects_bad_config(
    tmp_path: Path, contents: str, expected_in_message: str
) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(contents)

    with pytest.raises(ConfigError, match=expected_in_message):
        load_settings(config_path)


def test_bot_settings_rejects_negative_max_title_length() -> None:
    with pytest.raises(ValueError, match="max_title_length"):
        BotSettings(max_title_length=-5)

"""Centralized configuration loading with schema validation: bad config is
rejected at the boundary (`BotSettings`), not three calls deep in the
engine. See tests/unit/test_config.py."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError


class BotSettings(BaseModel):
    store_path: Path = Path("tasks.json")
    max_title_length: int = Field(default=200, ge=1, le=1000)
    help_url: str = "https://developers.google.com/workspace/chat/write-error-messages"


class ConfigError(Exception):
    """Raised when on-disk config can't be loaded: bad JSON or a schema violation."""


def load_settings(path: Path | None = None) -> BotSettings:
    """Load `BotSettings` from `path` (defaults if None/missing), raising
    `ConfigError` for any failure so callers handle one exception type."""
    assert path is None or isinstance(path, Path), "path must be a Path or None"
    if path is None or not path.exists():
        return BotSettings()
    try:
        raw = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Config at {path} is not valid JSON: {exc}") from exc
    assert isinstance(raw, dict), f"Config at {path} must be a JSON object"
    try:
        return BotSettings.model_validate(raw)
    except ValidationError as exc:
        raise ConfigError(f"Config at {path} failed validation: {exc}") from exc

"""Technique 2: TypedDict for structured state that doesn't need
validation. `ParseContext` is internal scratch state inside
`engines.command_parser` — checked statically (typos in key names), but
unlike `Task` it's a plain `dict` at runtime and enforces nothing. See
tests/unit/test_state.py."""

from __future__ import annotations

from typing import TypedDict


class ParseContext(TypedDict):
    raw_text: str
    tokens: list[str]
    token_count: int

# Copyright (c) 2026 Ben O'Mahony
"""Keep a teaching example for every shipped NASA diagnostic."""

from pathlib import Path

from nasa_lsp.analyzer import ALL_RULES


def test_every_nasa_diagnostic_has_a_broken_example() -> None:
    """A new diagnostic should have an example students can run directly."""
    examples = {path.stem for path in Path("examples/nasa").glob("*.py")}
    assert examples == ALL_RULES

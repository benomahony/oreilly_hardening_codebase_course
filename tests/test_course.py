# Copyright (c) 2026 Ben O'Mahony
"""Keep the course's executable scene-to-solution map intact."""

from pathlib import Path

import pytest
from nasa_lsp.analyzer import ALL_RULES

from scripts.demo import CASES, NASA_CODES


def test_every_nasa_diagnostic_has_a_failure_scene() -> None:
    """A tool upgrade adding a rule must not silently leave the course incomplete."""
    assert set(NASA_CODES) == ALL_RULES


@pytest.mark.parametrize("solution", sorted({case.solution for case in CASES}))
def test_every_failure_scene_has_a_completed_solution(solution: str) -> None:
    """Do not leave placeholder answers or broken solution links in the walkthrough."""
    assert Path(solution).is_file()

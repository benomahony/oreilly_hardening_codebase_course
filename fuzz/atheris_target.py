# Copyright (c) 2026 Ben O'Mahony
"""Instrument Python branches before loading the application under test."""

import sys
from pathlib import Path

import atheris

with atheris.instrument_imports():
    from scripts.fuzz import CORPUS, exercise


@atheris.instrument_func
def test_one_input(data: bytes) -> None:
    """Keep assertion failures visible to libFuzzer as crash findings."""
    _ = exercise(data)


def main() -> None:
    """Replay boundary seeds and then explore new inputs with coverage guidance."""
    corpus = Path("reports/fuzz-corpus")
    corpus.mkdir(parents=True, exist_ok=True)
    for index, seed in enumerate(CORPUS):
        _ = (corpus / f"seed-{index}").write_bytes(seed)
    atheris.Setup([*sys.argv, str(corpus)], test_one_input, enable_python_coverage=True)
    atheris.Fuzz()


if __name__ == "__main__":
    main()

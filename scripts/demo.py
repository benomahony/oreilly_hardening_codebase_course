# Copyright (c) 2026 Ben O'Mahony
"""Verify that each deliberately broken example fails for its intended reason."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DemoOptions(argparse.Namespace):
    """Typed arguments prevent the command-line boundary from spreading Any."""

    scene: str = "all"
    verbose: bool = False


@dataclass(frozen=True)
class FailureCase:
    """A command with a specific, reviewable expected failure."""

    name: str
    command: tuple[str, ...]
    expected: tuple[str, ...]
    solution: str
    cwd: str = "."


NASA_CODES = (
    "NASA01-forbidden-api",
    "NASA01-recursion",
    "NASA02",
    "NASA04",
    "NASA05",
    "NASA05-message",
    "NASA05-single-condition",
    "NASA05-constant-assert",
    "NASA05-redundant-none",
    "NASA05-total-op",
    "NASA05-guaranteed-len",
    "NASA05-isinstance",
)
DESIDERATA_CODES = (
    "DET001",
    "ISO001",
    "FST001",
    "AUT001",
    "BHV001",
    "STR001",
    "SPC003",
    "PRD003",
    "CMP001",
    "RDL001",
)
CASES = (
    FailureCase(
        "mutation",
        (
            "pytest",
            "examples/broken/mutation/test_weak_suite.py::test_zero_stock_exposes_the_survivor",
            "-q",
        ),
        ("initial stock must never be negative", "1 failed"),
        "solutions/test_mutation.py",
    ),
    FailureCase(
        "format",
        (
            "ruff",
            "format",
            "--check",
            "--no-force-exclude",
            "examples/broken/quality/formatting.py",
        ),
        ("would be reformatted",),
        "solutions/strict.py",
    ),
    FailureCase(
        "lint",
        ("ruff", "check", "--no-force-exclude", "examples/broken/quality/linting.py"),
        ("F401", "E722", "ANN"),
        "solutions/strict.py",
    ),
    FailureCase(
        "types",
        ("basedpyright", "--project", "examples/broken/types"),
        ("reportArgumentType", "reportExplicitAny", "reportUnknownParameterType"),
        "solutions/strict.py",
    ),
    *(
        FailureCase(
            code,
            ("nasa", "lint", f"{code}.py"),
            (code,),
            "solutions/defensive.py",
            "examples/broken/nasa",
        )
        for code in NASA_CODES
    ),
    FailureCase(
        "ddd",
        ("dddlint", "lint", "."),
        ("forbidden", "alias", "duplicate"),
        "solutions/ddd/reservations.py",
        "examples/broken/ddd",
    ),
    *(
        FailureCase(
            code,
            ("testdesiderata", f"examples/broken/desiderata/test_{code.lower()}.py"),
            (code,),
            "solutions/test_desiderata.py",
        )
        for code in DESIDERATA_CODES
    ),
    FailureCase(
        "mocks",
        ("mockbuster", "examples/broken/mocks", "--strict"),
        ("mock",),
        "solutions/test_mock_free.py",
    ),
    FailureCase(
        "architecture",
        ("lint-imports",),
        ("BROKEN", "bad_reservations.domain"),
        "solutions/architecture.md",
        "examples/broken/architecture",
    ),
    FailureCase(
        "docs",
        ("pytest", "examples/broken/docs/test_stale_docs.py", "-q"),
        ("Print output changed code", "1 failed"),
        "solutions/docs/updated.md",
    ),
    FailureCase(
        "hypothesis",
        ("pytest", "examples/broken/assertions/test_off_by_one.py", "-q"),
        ("Failing test case", "a reservation must conserve stock"),
        "solutions/test_properties.py",
    ),
    FailureCase(
        "fuzz",
        ("python", "-m", "scripts.fuzz", "--exercise-bug"),
        ("fuzzing found a stock conservation failure",),
        "solutions/defensive.py",
    ),
)


def run_case(case: FailureCase, *, verbose: bool) -> bool:
    """Reject a missing executable, timeout, unexpected success, or wrong diagnostic."""
    environment = dict(os.environ, COLUMNS="240", NO_COLOR="1", TERM="dumb")
    environment["PYTHONPATH"] = str(ROOT / case.cwd)
    # The command tuple is maintained in this repository, never supplied as shell text.
    result = subprocess.run(  # noqa: S603
        case.command,
        cwd=ROOT / case.cwd,
        env=environment,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    output = result.stdout + result.stderr
    report = ROOT / "reports" / "demo" / f"{case.name}.log"
    report.parent.mkdir(parents=True, exist_ok=True)
    _ = report.write_text(output)
    passed = result.returncode == 1 and all(token in output for token in case.expected)
    status = "EXPECTED FAILURE" if passed else "DEMO FAILED"
    _ = sys.stdout.write(f"{status}: {case.name} → {case.solution}\n")
    if verbose or not passed:
        _ = sys.stdout.write(output + "\n")
    return passed


def main() -> int:
    """Run all scenes, or a single scene for a live presentation."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "scene", nargs="?", default="all", choices=["all", *(case.name for case in CASES)]
    )
    _ = parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(namespace=DemoOptions())
    selected = [case for case in CASES if args.scene in ("all", case.name)]
    outcomes = [run_case(case, verbose=args.verbose) for case in selected]
    _ = sys.stdout.write(f"\n{sum(outcomes)}/{len(outcomes)} failure demonstrations verified.\n")
    return 0 if all(outcomes) else 1


if __name__ == "__main__":
    raise SystemExit(main())

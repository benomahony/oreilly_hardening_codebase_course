# Copyright (c) 2026 Ben O'Mahony
"""Run mutmut and permit only individually reviewed equivalent survivors."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def capture(*arguments: str) -> str:
    """Run a fixed repository command without a shell and return its report."""
    result = subprocess.run(  # noqa: S603 -- Repository-controlled argument tuple.
        arguments,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        timeout=300,
    )
    return result.stdout


def main() -> int:
    """Fail on unknown survivors, missing tests, timeouts, or an empty result set."""
    # This directory is mutmut's disposable copy. A fresh run must see new tests.
    shutil.rmtree(ROOT / "mutants", ignore_errors=True)
    executable = shutil.which("mutmut")
    if executable is None:
        msg = "mutmut is not installed; run uv sync --locked"
        raise RuntimeError(msg)
    result = subprocess.run(  # noqa: S603 -- Fixed command resolved from the active environment.
        (executable, "run", "--max-children", "2"),
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        return result.returncode
    output = capture("mutmut", "results", "--all", "true")
    rows = [line.strip().rsplit(": ", 1) for line in output.splitlines() if ": " in line]
    if not rows:
        _ = sys.stderr.write("No mutants found; refusing to report a passing mutation gate.\n")
        return 1
    reviewed = {
        line.split("\t")[0]
        for line in (ROOT / "docs/mutation-survivors.tsv").read_text().splitlines()
        if line and not line.startswith("#")
    }
    unexpected: list[str] = []
    survivors = 0
    for name, status in rows:
        if status == "killed":
            continue
        if status != "survived":
            unexpected.append(f"{name}: {status}")
            continue
        survivors += 1
        diff = capture("mutmut", "show", name)
        fingerprint = hashlib.sha256(diff.encode()).hexdigest()
        if fingerprint not in reviewed:
            unexpected.append(diff)
    _ = capture("mutmut", "export-cicd-stats")
    _ = sys.stdout.write(
        f"\n{len(rows) - survivors}/{len(rows)} killed; {survivors} survivors reviewed.\n"
    )
    if unexpected:
        _ = sys.stderr.write("Unreviewed or incomplete mutation results:\n" + "\n".join(unexpected))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

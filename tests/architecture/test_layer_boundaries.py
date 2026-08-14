"""Technique 8: architecture tests, via the AST rather than grepping text
(which would miss `import commons.engines as x` or a match inside a
comment). Rule: `commons/` is the dependency-free base layer and may not
import from `engines/`."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.architecture

SRC_ROOT = Path(__file__).parent.parent.parent / "src" / "oreilly_hardening_codebase_course"
FORBIDDEN_PREFIX = "oreilly_hardening_codebase_course.engines"


def _imported_module_names(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            names.append(node.module)
    return names


def _commons_files() -> list[Path]:
    commons_dir = SRC_ROOT / "commons"
    assert commons_dir.is_dir(), f"expected {commons_dir} to exist"
    files = sorted(commons_dir.glob("*.py"))
    assert files, f"expected at least one file under {commons_dir}"
    return files


@pytest.mark.parametrize("path", _commons_files(), ids=lambda p: p.name)
def test_commons_never_imports_engines(path: Path) -> None:
    imports = _imported_module_names(path)
    violations = [name for name in imports if name.startswith(FORBIDDEN_PREFIX)]
    assert not violations, f"{path.relative_to(SRC_ROOT)} imports from engines/: {violations}"


def test_layer_boundary_check_actually_detects_a_violation(tmp_path: Path) -> None:
    """Pins the detector against a synthetic violation, so it can't silently
    become a no-op."""
    offending_file = tmp_path / "bad_module.py"
    offending_file.write_text("from oreilly_hardening_codebase_course.engines import task_engine\n")

    imports = _imported_module_names(offending_file)

    assert any(name.startswith(FORBIDDEN_PREFIX) for name in imports)

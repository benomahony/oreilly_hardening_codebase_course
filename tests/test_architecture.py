# Copyright (c) 2026 Ben O'Mahony
"""Inspect real imports to enforce the decision to keep the domain independent."""

import grimp
import pytest


@pytest.mark.architecture
def test_domain_has_no_dependencies_on_outer_layers() -> None:
    """Changing a domain module to import an adapter must fail this contract."""
    graph = grimp.build_graph("reservations")
    domain_modules = sorted(name for name in graph.modules if ".domain" in name)
    assert domain_modules, "the contract must inspect at least one real domain module"
    for module in domain_modules:
        imports = graph.find_modules_directly_imported_by(module)
        assert not any(".infrastructure" in name for name in imports)
        assert not any(".application" in name for name in imports)

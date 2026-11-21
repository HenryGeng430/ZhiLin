"""Dependency-direction guard for the public skeleton.

This is a lightweight Python "ArchUnit": parse imports with ``ast`` and fail
if an inner layer imports an outer layer.
"""
from __future__ import annotations

import ast
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1] / "src" / "cola_skeleton"
LAYERS = {"domain", "application", "adapter", "infrastructure"}


def imports(folder: str) -> set[str]:
    names: set[str] = set()
    for path in (PACKAGE / folder).rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module)
    return names


def layer_of(name: str) -> str | None:
    if name.startswith("cola_skeleton."):
        parts = name.split(".")
        return parts[1] if len(parts) > 1 else None
    return None


class DependencyDirectionTest(unittest.TestCase):
    def test_domain_is_innermost(self):
        forbidden = {"adapter", "application", "infrastructure"}
        for name in imports("domain"):
            self.assertNotIn(layer_of(name), forbidden, f"domain imports {name}")

    def test_application_does_not_import_outer_layers(self):
        forbidden = {"adapter", "infrastructure"}
        for name in imports("application"):
            self.assertNotIn(layer_of(name), forbidden, f"application imports {name}")

    def test_domain_has_no_http_framework_imports(self):
        forbidden = {"http.server", "flask", "fastapi", "django", "starlette"}
        for name in imports("domain"):
            self.assertNotIn(name, forbidden, f"domain imports {name}")

    def test_layer_imports_are_qualified(self):
        """No module may import a sibling layer by its bare top-level name."""
        for folder in LAYERS:
            for name in imports(folder):
                top = name.split(".", 1)[0]
                if top in LAYERS:
                    self.assertTrue(
                        name.startswith("cola_skeleton."),
                        f"{folder} imports unqualified {name}",
                    )


if __name__ == "__main__":
    unittest.main()

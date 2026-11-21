"""Dependency-direction guard for the public skeleton."""
from __future__ import annotations

import ast
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def imports(folder: str) -> set[str]:
    out: set[str] = set()
    for base, _dirs, files in os.walk(os.path.join(ROOT, folder)):
        for name in files:
            if not name.endswith(".py"):
                continue
            path = os.path.join(base, name)
            with open(path, encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    out.update(a.name for a in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    out.add(node.module)
    return out


class DependencyDirectionTest(unittest.TestCase):
    def test_domain_is_innermost(self):
        names = imports("domain")
        self.assertFalse(any(n.startswith("adapter") or n.startswith("application")
                             or n.startswith("infrastructure") for n in names))

    def test_application_does_not_import_outer_layers(self):
        names = imports("application")
        self.assertFalse(any(n.startswith("adapter") or n.startswith("infrastructure")
                             for n in names))


if __name__ == "__main__":
    unittest.main()

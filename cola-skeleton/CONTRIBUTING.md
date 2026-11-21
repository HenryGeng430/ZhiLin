# Contributing

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: . .venv/bin/activate
python -m pip install -e ".[dev]"
```

The runtime has no third-party dependencies. The `dev` extra installs pytest,
ruff, and mypy for optional local checks.

## Commands

```bash
make test       # unittest suite
make run        # start the demo server
make demo       # in-memory composition-root example
make lint       # ruff check
make typecheck  # mypy
```

Without `make`:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m cola_skeleton.server --port 8098
```

## Style

- Python 3.11+, type hints on public functions.
- Keep imports qualified inside the package (`cola_skeleton.domain...`).
- Keep `domain` free of HTTP, SQLite, and infrastructure imports.
- Keep `adapter` free of infrastructure imports; inject services from the
  composition root.
- Prefer small functions and explicit data flow over global state.
- Add a test for every behavior change.

## Pull request checklist

- [ ] Tests pass locally.
- [ ] New behavior has a test.
- [ ] No secrets, credentials, or product-specific data.
- [ ] `ARCHITECTURE.md` is updated if the dependency rules change.
- [ ] Public API changes are reflected in `README.md`.

## Scope

This folder is a public framework demo. Do not add product business logic,
private prompts, account policies, quotas, or deployment details.

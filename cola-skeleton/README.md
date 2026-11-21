# COLA Skeleton

A small, dependency-free Python project that demonstrates **COLA / clean
architecture dependency rules** with a generic Note CRUD domain. It is a public
capability showcase, not a reproducible version of any product.

The code is intentionally boring: standard-library HTTP, SQLite, explicit
ports, constructor injection, and tests that fail when an inner layer imports
an outer one.

## What it demonstrates

- `adapter → application → domain` dependency direction.
- Repository ports owned by the domain, implemented by infrastructure.
- A composition root that wires concrete adapters at the edge.
- A stable response envelope: `{code, message, data, traceId}`.
- Pagination, validation, 404/405 handling, and consistent error mapping.
- Architecture tests, use-case tests, SQLite tests, and an HTTP smoke test.
- A `src/` layout with packaging, CI, Docker, and contributor docs.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: . .venv/bin/activate
python -m pip install -e .

python -m cola_skeleton.server --port 8098 --db ./notes.db
```

Or run without installing:

```bash
PYTHONPATH=src python -m cola_skeleton.server --port 8098 --db ./notes.db
```

```bash
curl -s http://127.0.0.1:8098/api/v1/notes \
  -H 'Content-Type: application/json' \
  -d '{"title":"Architecture note","body":"COLA demo"}'
```

## API

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/v1/health` | health and server time |
| `GET` | `/api/v1/notes?limit=20&offset=0` | list notes |
| `POST` | `/api/v1/notes` | create `{title, body}` |
| `GET` | `/api/v1/notes/{id}` | read one note |
| `PATCH` | `/api/v1/notes/{id}` | update `{title?, body?}` |
| `DELETE` | `/api/v1/notes/{id}` | delete one note |

Every response uses the same envelope:

```json
{"code": "OK", "message": "", "data": {}, "traceId": "tr-1a2b3c4d"}
```

## Layout

```text
src/cola_skeleton/
├── domain/          Note entity + NoteRepository port
├── application/     NoteService use cases (depends on the port only)
├── infrastructure/  In-memory and SQLite port implementations
├── adapter/         Framework-free HTTP-shaped router + DTOs
├── common/          Response envelope + demo errors
├── server.py        Standard-library HTTP server + composition root
└── __main__.py      python -m cola_skeleton

tests/               domain, use-case, SQLite, HTTP, architecture tests
examples/            in-memory composition-root example
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the dependency rules and request
flow, and [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow.

## Test

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

The architecture test parses imports with `ast` and fails if `domain/` imports
`adapter/`, `application/`, or `infrastructure/`, or if `application/` imports
an outer layer.

## Docker

```bash
docker build -t cola-skeleton .
docker run --rm -p 8098:8098 -v cola-data:/data cola-skeleton
```

## Design notes

- **No web framework.** The adapter is a small router so the example stays
  portable and the dependency direction is visible.
- **No ORM.** SQLite is accessed with parameterized SQL; the schema is explicit.
- **No hidden globals.** The repository is injected into the service; the
  service is injected into the router.
- **No product rules.** The Note domain is deliberately generic. It contains no
  accounts, prompts, quotas, mastery algorithms, or other product logic.

## License

MIT. See the repository root [LICENSE](../LICENSE).

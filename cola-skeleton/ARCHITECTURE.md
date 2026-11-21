# Architecture

This project is a small demonstration of the COLA dependency rule:

```text
        ┌─────────────────────────────────────────────┐
        │                  adapter                    │
        │  HTTP-shaped router, DTOs, error mapping    │
        └──────────────────────┬──────────────────────┘
                               │ calls
        ┌──────────────────────▼──────────────────────┐
        │                application                  │
        │  use cases, orchestration, validation       │
        └──────────────────────┬──────────────────────┘
                               │ calls
        ┌──────────────────────▼──────────────────────┐
        │                  domain                     │
        │  entities, value objects, repository ports  │
        └──────────────────────▲──────────────────────┘
                               │ implements
        ┌──────────────────────┴──────────────────────┐
        │              infrastructure                 │
        │  in-memory and SQLite adapters              │
        └─────────────────────────────────────────────┘

        common: response envelope, stable demo errors
        server: composition root; wires concrete adapters
```

The arrows are source-code dependencies, not runtime call order. `domain` knows
nothing about HTTP, SQLite, or the application layer. `application` knows the
repository port, but not which adapter implements it. `adapter` knows the
application service, but not the database. `server.py` is the only place where
concrete implementations meet.

## Layer responsibilities

| Layer | Owns | May import | Must not import |
|---|---|---|---|
| `domain` | `Note`, `NoteRepository` | standard library | `application`, `adapter`, `infrastructure` |
| `application` | `NoteService` use cases | `domain`, `common` | `adapter`, `infrastructure` |
| `adapter` | HTTP router, DTO mapping, error translation | `application`, `common` | `infrastructure` |
| `infrastructure` | in-memory and SQLite repositories | `domain`, `common` | `adapter` |
| `common` | response envelope, demo errors | standard library | business layers |
| `server` | composition root, stdlib HTTP transport | all layers | — |

## Request flow

```text
HTTP request
  → server.Handler parses method/path/query/body
  → adapter.NoteRouter.dispatch(...)
  → application.NoteService.create/get/update/delete/list(...)
  → domain.Note rules
  → domain.NoteRepository port
  → infrastructure.SqliteNoteRepository
  → SQLite
  ← domain object
  ← DTO
  ← {code, message, data, traceId}
  ← HTTP response
```

The adapter never opens a database connection. The composition root creates the
repository and passes it to the service:

```python
service = NoteService(SqliteNoteRepository(args.db))
Handler.router = make_router(service)
```

## Adding a slice

1. Add the entity/value objects and a repository port under `domain/`.
2. Add a use-case service under `application/` that depends on the port.
3. Add an infrastructure adapter that implements the port.
4. Add an adapter/controller that converts transport data to use-case calls.
5. Wire the concrete adapter in `server.py` (or another composition root).
6. Add domain, use-case, adapter, and architecture tests.

Keep product-specific rules out of this public skeleton. It is a framework
example, not a product implementation.

## Testing strategy

| Test | What it proves |
|---|---|
| `test_domain.py` | entity invariants without HTTP or SQLite |
| `test_use_cases.py` | orchestration against a fake port |
| `test_sqlite.py` | real SQLite round trip and cleanup |
| `test_http_smoke.py` | real server, real HTTP, real JSON envelope |
| `test_architecture.py` | inner layers do not import outer layers |

The architecture test uses Python's `ast` module. It is deliberately simple: it
checks static imports, not runtime behavior. Code review still matters.

## Trade-offs

- **Standard library over a framework.** This keeps the demo portable and makes
  the dependency direction visible, but it is not a production web stack.
- **SQLite over an ORM.** The SQL is explicit and easy to inspect, but there is
  no migration tool. A real service should add one.
- **One process, one database file.** The demo does not attempt multi-tenant or
  distributed concerns.

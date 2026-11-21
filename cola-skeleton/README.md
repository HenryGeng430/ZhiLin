# COLA Skeleton (public, minimal)

This folder is a **framework-only backend demo** for the public repository. It
shows the dependency direction and engineering habits used by ZhiLin COLA
Edition, without exposing product business rules, prompts, quotas, account
policies, mastery algorithms, data models or deployment details.

```text
domain/          pure entities + repository ports
application/     use cases depending only on ports
infrastructure/  in-memory and SQLite adapters implementing ports
adapter/         framework-free HTTP-shaped adapter
common/          unified response envelope + stable demo errors
server.py        standard-library HTTP server + SQLite wiring
tests/           dependency-direction, use-case, SQLite and HTTP smoke tests
```

## Run

```bash
python server.py --port 8098 --db ./notes.db
```

The server is standard-library only. The example domain is a generic note list,
intentionally unrelated to ZhiLin.

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/health` | health and server time |
| GET | `/api/v1/notes?limit=20&offset=0` | list notes |
| POST | `/api/v1/notes` | create `{title, body}` |
| GET | `/api/v1/notes/{id}` | read one note |
| PATCH | `/api/v1/notes/{id}` | update `{title?, body?}` |
| DELETE | `/api/v1/notes/{id}` | delete one note |

All responses use `{code,message,data,traceId}`.

```bash
curl -s http://127.0.0.1:8098/api/v1/notes \
  -H 'Content-Type: application/json' \
  -d '{"title":"Architecture note","body":"COLA demo"}'
```

## Test

```bash
PYTHONPATH=. python -m unittest discover -s tests -v
```

The architecture test fails if `domain/` imports `adapter/`, `application/` or
`infrastructure/`, or if `application/` imports outer layers.

## Docker

```bash
docker build -t zhilin-cola-demo .
docker run --rm -p 8098:8098 zhilin-cola-demo
```

This demo is deliberately small. It is a public capability showcase, not a
reproducible version of the full product.

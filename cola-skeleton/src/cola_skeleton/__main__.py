"""Allow ``python -m cola_skeleton`` to start the demo server."""
from __future__ import annotations

from cola_skeleton.server import main

if __name__ == "__main__":
    raise SystemExit(main())

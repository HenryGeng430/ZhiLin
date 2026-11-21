PYTHON ?= python
export PYTHONPATH := src

.PHONY: test run demo lint typecheck

test:
	$(PYTHON) -m unittest discover -s tests -v

run:
	$(PYTHON) -m cola_skeleton.server --port 8098 --db ./notes.db

demo:
	$(PYTHON) examples/in_memory_demo.py

lint:
	ruff check src tests

typecheck:
	mypy src

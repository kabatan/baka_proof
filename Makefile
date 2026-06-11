.PHONY: test-unit smoke-env-bootstrap

PYTHON ?= python

test-unit:
	$(PYTHON) -m unittest discover -s tests/unit -p "test_*.py"

smoke-env-bootstrap:
	$(PYTHON) scripts/probe_dependencies.py --json

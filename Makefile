.PHONY: test-unit

PYTHON ?= python

test-unit:
	$(PYTHON) -m unittest discover -s tests/unit -p "test_*.py"

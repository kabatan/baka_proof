.PHONY: test-unit smoke-env-bootstrap smoke-resource-governor smoke-model-provider-set lean-build lean-no-sorry smoke-target-library-status

PYTHON ?= python

test-unit:
	$(PYTHON) -m unittest discover -s tests/unit -p "test_*.py"

smoke-env-bootstrap:
	$(PYTHON) scripts/probe_dependencies.py --json

smoke-resource-governor:
	$(PYTHON) scripts/probe_local_resources.py --json

smoke-model-provider-set:
	$(PYTHON) scripts/smoke_model_provider_set.py

lean-build:
	lake build

lean-no-sorry:
	$(PYTHON) scripts/check_lean_no_sorry.py

smoke-target-library-status:
	$(PYTHON) -m math_auto_research.cli.report_target_library_status

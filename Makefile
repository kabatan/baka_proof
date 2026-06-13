.PHONY: fmt lint typecheck test test-unit test-mutation test-regression test-integration smoke-env-bootstrap smoke-resource-governor smoke-model-provider-set lean-build lean-no-sorry smoke-target-library-status smoke-geometry-extraction smoke-geometry-context-fixture smoke-leangeo-fixture smoke-leangeo-extraction smoke-geometry-provider smoke-real-newclid smoke-real-genesisgeo smoke-geometry-trace smoke-geometry-construction smoke-geometry-final-verify

PYTHON ?= python
ELAN_LAKE := $(USERPROFILE)/.elan/bin/lake.exe
LAKE ?= $(if $(wildcard $(ELAN_LAKE)),$(ELAN_LAKE),lake)

fmt:
	$(PYTHON) -m compileall -q src plugins scripts tests

lint:
	$(PYTHON) scripts/check_domain_contamination.py
	$(PYTHON) scripts/check_no_loose_options.py

typecheck:
	$(PYTHON) -m unittest tests.unit.test_schema_validation

test: test-unit test-regression test-mutation test-integration

test-unit:
	$(PYTHON) -m unittest discover -s tests/unit -p "$(if $(TEST_FILTER),*$(TEST_FILTER)*.py,test_*.py)"

test-mutation:
	$(if $(TEST_FILTER),$(PYTHON) -m unittest discover -s tests/unit -p "*$(TEST_FILTER)*.py",$(PYTHON) -m unittest tests.unit.test_geometry_extraction tests.unit.test_target_subset tests.unit.test_trace_compiler tests.unit.test_geotrace_rule_registry tests.unit.test_construction_compiler tests.unit.test_geometry_bridge tests.unit.test_final_verify tests.unit.test_geometry_standard_loop tests.unit.test_proof_state_dag)

test-regression:
	$(if $(TEST_FILTER),$(PYTHON) -m unittest discover -s tests/unit -p "*$(TEST_FILTER)*.py",$(PYTHON) -m unittest tests.unit.test_domain_contamination tests.unit.test_schema_validation tests.unit.test_target_library_status tests.unit.test_resource_governor tests.unit.test_composite_provider tests.unit.test_geometry_extraction tests.unit.test_real_smoke_corpus tests.unit.test_v03a_real_vs_fixture_integration tests.unit.test_trace_compiler tests.unit.test_geotrace_rule_registry tests.unit.test_construction_compiler tests.unit.test_geometry_bridge tests.unit.test_final_verify tests.unit.test_model_provider_set tests.unit.test_geometry_standard_loop tests.unit.test_proof_state_dag tests.unit.test_run_trace tests.unit.test_evaluation_matrix)
	$(PYTHON) scripts/check_domain_contamination.py
	$(PYTHON) scripts/check_no_loose_options.py

test-integration:
	$(if $(TEST_FILTER),$(PYTHON) -m unittest discover -s tests/unit -p "*$(TEST_FILTER)*.py",$(PYTHON) -m unittest tests.unit.test_composite_provider tests.unit.test_geometry_standard_loop tests.unit.test_newclid_adapter tests.unit.test_genesisgeo_adapter)

smoke-env-bootstrap:
	$(PYTHON) scripts/probe_dependencies.py --json

smoke-resource-governor:
	$(PYTHON) scripts/probe_local_resources.py --json

smoke-model-provider-set:
	$(PYTHON) scripts/smoke_model_provider_set.py

lean-build:
	"$(LAKE)" build

lean-no-sorry:
	$(PYTHON) scripts/check_lean_no_sorry.py

smoke-target-library-status:
	$(PYTHON) -m math_auto_research.cli.report_target_library_status

smoke-geometry-extraction:
	$(PYTHON) scripts/smoke_leangeo_extraction.py

smoke-geometry-context-fixture:
	$(PYTHON) scripts/smoke_geometry_context_fixture.py

smoke-leangeo-fixture:
	$(PYTHON) scripts/check_leangeo_wsl_fixture.py

smoke-leangeo-extraction:
	$(PYTHON) scripts/smoke_leangeo_extraction.py

smoke-geometry-provider:
	$(PYTHON) scripts/smoke_geometry_provider.py

smoke-real-newclid:
	$(PYTHON) scripts/smoke_real_newclid.py

smoke-real-genesisgeo:
	$(PYTHON) scripts/smoke_real_genesisgeo.py

smoke-geometry-trace:
	$(PYTHON) scripts/smoke_geometry_trace.py

smoke-geometry-construction:
	$(PYTHON) scripts/smoke_geometry_construction.py

smoke-geometry-final-verify:
	$(PYTHON) scripts/smoke_geometry_final_verify.py

# T26 GeoTraceV1 and RuleRegistryV1 evidence

Task: T26 — GeoTraceV1 and RuleRegistryV1.

Supports:

```text
R-RULE-001
R-TRACE-001
```

Implemented files:

```text
plugins/geometry_synthetic/trace/geotrace_v1.py
plugins/geometry_synthetic/trace/rule_registry_v1.py
plugins/geometry_synthetic/trace/side_condition_calculus.py
plugins/geometry_synthetic/trace/__init__.py
plugins/geometry_synthetic/rules.py
schemas/geometry/geotrace_v1.schema.json
schemas/geometry/rule_registry_v1.schema.json
```

Notes:

```text
GeoTraceV1 now carries source_provider_result, target_library=LeanGeoSubsetV1,
per-step source_raw_ref, and unsupported_steps. RuleRegistryV1 now carries
provider_trace_patterns, lean_template_id, required side conditions,
generated obligations, auto_discharge_policy, unsupported variants, and
positive/negative/ambiguous/mutation fixtures. Missing side conditions remain
generated obligations or blockers rather than silent proof assumptions.
```

Commands run:

```text
make test-unit TEST_FILTER=geotrace
make test-unit TEST_FILTER=rule_registry
make test-mutation TEST_FILTER=rule_registry
make test-unit TEST_FILTER=trace_compiler
make test-unit TEST_FILTER=schema_validation
python -m compileall -q plugins tests scripts
```

Observed results:

```text
geotrace unit tests: 3 tests OK.
rule_registry unit tests: 3 tests OK.
rule_registry mutation tests: 3 tests OK.
trace_compiler unit tests: 4 tests OK.
schema_validation unit tests: 9 tests OK.
compileall passed.
```

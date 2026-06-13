# RC-6 follow-up fixes evidence

Context: guardian_boundary_reviewer returned FAIL_FIXABLE for RC-6.

Fixed blockers:

```text
1. GeoTraceV1 unsupported_steps now block TraceCompiler compilation.
2. TraceCompiler now blocks target-library mismatch, unsupported_steps,
   unsupported variants, and orientation_mismatch side-condition markers.
3. ConstructionCompiler now blocks missing existence side conditions.
4. ConstructionCompiler now validates dependency refs beyond presence by
   requiring typed dependency refs in the current supported shape.
5. AuxiliaryConstructionCandidateV1 schema now restricts candidate proof_use_status
   to not_allowed_until_final_verify.
```

Commands run after fixes:

```text
make test-unit TEST_FILTER=geotrace
make test-unit TEST_FILTER=rule_registry
make test-mutation TEST_FILTER=rule_registry
make smoke-geometry-trace
make test-unit TEST_FILTER=trace_compiler
make test-mutation TEST_FILTER=trace_compiler
make test-unit TEST_FILTER=auxiliary_construction_candidate
make test-regression TEST_FILTER=aux_rationale_not_proof
make smoke-geometry-construction
make test-unit TEST_FILTER=construction_compiler
make test-mutation TEST_FILTER=construction_compiler
make lean-build
make test-unit TEST_FILTER=schema_validation
python -m compileall -q plugins tests scripts
```

Observed results:

```text
geotrace unit tests: 3 tests OK.
rule_registry unit tests: 3 tests OK.
rule_registry mutation tests: 3 tests OK.
smoke-geometry-trace passed with lean_exit_code=0.
trace_compiler unit tests: 8 tests OK.
trace_compiler mutation tests: 8 tests OK.
auxiliary_construction_candidate unit tests: 2 tests OK.
aux_rationale_not_proof regression: 1 test OK; domain/no-loose checks passed.
smoke-geometry-construction passed with lean_exit_code=0.
construction_compiler unit tests: 7 tests OK.
construction_compiler mutation tests: 7 tests OK.
lean-build completed successfully.
lean-build warning: .lake package repositories UnicodeBasic and batteries report local changes in the dependency cache.
schema_validation unit tests: 9 tests OK.
compileall passed.
```

Claim caveats:

```text
This follow-up addresses RC-6 fixable blockers only. It does not mark R-IDs
VERIFIED and does not claim v0.3 completion, SOURCE_FAITHFUL,
ACCEPTANCE_COMPLETE, or PRODUCTION_SAFE.
```

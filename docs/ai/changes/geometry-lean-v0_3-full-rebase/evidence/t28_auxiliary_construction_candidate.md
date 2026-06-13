# T28 AuxiliaryConstructionCandidateV1 evidence

Task: T28 — AuxiliaryConstructionCandidateV1.

Supports:

```text
R-AUX-001
```

Implemented files:

```text
plugins/geometry_synthetic/construction/auxiliary_construction_candidate_v1.py
plugins/geometry_synthetic/construction/__init__.py
schemas/geometry/auxiliary_construction_candidate_v1.schema.json
plugins/geometry_synthetic/provider.py
scripts/run_genesisgeo_probe.py
tests/unit/test_auxiliary_construction_candidate.py
tests/unit/test_aux_rationale_not_proof.py
tests/unit/test_composite_provider.py
tests/unit/test_genesisgeo_adapter.py
```

Notes:

```text
AuxiliaryConstructionCandidateV1 now emits Base Spec fields:
construction_id, source_provider_result, structured dependencies,
required_side_conditions, lean_introduction_plan, and proof_use_status
not_allowed_until_final_verify. Legacy candidate_id/source_provenance fields
remain for compatibility. GenesisGeo rationale remains non-proof.
```

Commands run:

```text
make test-unit TEST_FILTER=auxiliary_construction_candidate
make test-regression TEST_FILTER=aux_rationale_not_proof
make test-unit TEST_FILTER=construction_compiler
make test-unit TEST_FILTER=composite_provider
make test-unit TEST_FILTER=genesisgeo_adapter
make test-unit TEST_FILTER=schema_validation
python -m compileall -q plugins tests scripts
```

Observed results:

```text
auxiliary_construction_candidate unit tests: 2 tests OK.
aux_rationale_not_proof regression: 1 test OK; domain/no-loose checks passed.
construction_compiler unit tests: 3 tests OK.
composite_provider unit tests: 14 tests OK.
genesisgeo_adapter unit tests: 3 tests OK, skipped=1 due current GenesisGeo runtime/checkpoint diagnostic blockers.
schema_validation unit tests: 9 tests OK.
compileall passed.
```

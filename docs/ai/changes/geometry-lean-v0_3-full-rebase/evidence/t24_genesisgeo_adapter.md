# T24 GenesisGeo-compatible real adapter evidence

Task: T24 — GenesisGeo-compatible real adapter.

Supports:

```text
R-SOLVER-004
R-AUX-001
```

Implemented files:

```text
plugins/geometry_synthetic/providers/genesisgeo_adapter.py
scripts/smoke_real_genesisgeo.py
tests/unit/test_genesisgeo_adapter.py
tests/unit/test_genesis_output_not_proof.py
scripts/run_genesisgeo_probe.py
plugins/geometry_synthetic/provider.py
Makefile
```

Notes:

```text
Plan-path genesisgeo_adapter.py exposes the GenesisGeo-compatible construction
proposer and AuxiliaryConstructionCandidateV1 normalizer. The provider runs
scripts/run_genesisgeo_probe.py through ResourceGovernor-managed external
process execution. Raw GenesisGeo-compatible rationale remains non-proof
diagnostic material. Candidate output, when the environment provides an
admitted runtime/checkpoint, is normalized through AuxiliaryConstructionCandidateV1.
```

Environment diagnostic:

```text
Vendored GenesisGeo source is present at vendor/GenesisGeo commit
e8c4337e782548a4d54e6839558a32965a5a764e. In this environment,
scripts/run_genesisgeo_probe.py reports diagnostic blockers:
python_runtime_required:==3.10.*:actual:3.12.11 and
missing_genesisgeo_model_checkpoint. Therefore the smoke establishes a real
external diagnostic path and candidate-normalization code path, but does not
establish model-backed GenesisGeo construction inference.
```

Commands run:

```text
make smoke-real-genesisgeo
make test-integration TEST_FILTER=genesisgeo_adapter
make test-regression TEST_FILTER=genesis_output_not_proof
python -m compileall -q plugins tests scripts
```

Observed results:

```text
smoke-real-genesisgeo passed. It emitted a construction_proposer engine run
with engine_family=genesisgeo_compatible, engine_version
GenesisGeo@e8c4337e782548a4d54e6839558a32965a5a764e, fixture_flag=false,
real_integration_flag=true, and ResourceUsageReport.logs_ref=external_genesisgeo_stdout.
The provider result remained proof_use_status=not_allowed and geotrace_ref=null.
genesisgeo_adapter integration tests: 3 tests OK, skipped=1 because the current
runtime/checkpoint environment returns diagnostic blockers instead of a candidate.
genesis_output_not_proof regression: 1 test OK; domain/no-loose checks passed.
compileall passed.
```

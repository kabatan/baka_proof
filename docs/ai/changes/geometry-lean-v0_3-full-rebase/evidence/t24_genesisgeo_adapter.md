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
e8c4337e782548a4d54e6839558a32965a5a764e. A dedicated conda environment
geolean-py310 provides Python 3.10.20 for the GenesisGeo-compatible probe.
The public Hugging Face checkpoint ZJUVAI/GenesisGeo was downloaded to
models/GenesisGeo and is intentionally excluded from git by /models/.
The local model.safetensors hash is
sha256:77406d21e84699b3d0d123653e40b7f48f3642beae10c0b608f58249223b8099.
scripts/run_genesisgeo_probe.py invokes scripts/run_genesisgeo_model_smoke.py,
which loads the local Qwen3 checkpoint and tokenizer with transformers and runs
a one-token generate smoke before emitting an auxiliary construction candidate.
```

Commands run:

```text
make smoke-real-genesisgeo
make test-integration TEST_FILTER=genesisgeo_adapter
make test-regression TEST_FILTER=genesis_output_not_proof
python -m compileall -q plugins tests scripts
C:\Users\bakat\miniforge3\envs\geolean-py310\python.exe scripts/run_genesisgeo_probe.py --request-id probe --claim-spec-json "{}"
```

Observed results:

```text
smoke-real-genesisgeo passed after model/runtime provisioning. It emitted a
construction_proposer engine run
with engine_family=genesisgeo_compatible, engine_version
GenesisGeo@e8c4337e782548a4d54e6839558a32965a5a764e, fixture_flag=false,
real_integration_flag=true, status=auxiliary_construction_candidate,
normalized_output_ref=aux_construction_candidate:geometry_request:real_genesisgeo_smoke:construction_proposer:genesisgeo_real,
and ResourceUsageReport.logs_ref=external_genesisgeo_stdout.
The provider result remained proof_use_status=not_allowed and geotrace_ref=null.
The probe reported python_version=3.10.20, model_checkpoint_status=available,
model_inference_status=available, architecture=Qwen3ForCausalLM, model_type=qwen3,
and blocker_reasons=[].
genesisgeo_adapter integration tests: 3 tests OK, skipped=1 for the temporary
checkpoint unit path that intentionally does not contain a real model.
genesis_output_not_proof regression: 1 test OK; domain/no-loose checks passed.
compileall passed.
```

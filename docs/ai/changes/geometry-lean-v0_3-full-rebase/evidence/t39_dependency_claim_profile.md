# T39 Dependency Claim-Profile Evidence

Task: T39 — Dependency claim-profile schema and probe update.

## Changed Files

```text
schemas/base/dependency_resolution_report.schema.json
schemas/resources/dependency_resolution_report.schema.json
schemas/artifact_schema_map.json
src/math_auto_research/base/schemas.py
src/math_auto_research/schema_validation.py
scripts/probe_dependencies.py
scripts/check_dependency_claim_profile.py
scripts/check_dependency_report_model_status.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/dependency_resolution.json
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/tonggeometry_model_discovery_report.md
```

## Result

`DependencyResolutionReport.engines[*]` now separates code installation,
model artifact availability, model inference availability, and claim impact.

Current claim-profile result:

```text
newclid_compatible:
  code_install_status=installed
  model_artifact_status=not_applicable
  claim_impact=none

genesisgeo_compatible:
  code_install_status=vendored
  model_artifact_status=available
  model_inference_status=available
  claim_impact=none

tonggeometry_compatible:
  code_install_status=vendored
  model_artifact_status=admitted_unavailable_external_artifact
  model_inference_status=unavailable
  claim_impact=blocks_model_backed_tonggeometry_claim
```

This supports the v0.3A split claim profile: the missing TongGeometry model
artifacts block only `V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY`, not
the core `V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY` claim by themselves.

## Verification

```text
python scripts/probe_dependencies.py --json --output docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/dependency_resolution.json
status: passed

python -m math_auto_research.cli.validate_artifact docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/dependency_resolution.json
status: passed

python scripts/check_dependency_claim_profile.py
status: passed

python scripts/check_dependency_report_model_status.py
status: passed

make test-unit TEST_FILTER=schema
status: passed, 9 tests
```

## Claim Ceiling

T39 is complete. No v0.3 completion claim is made. The model-backed
TongGeometry claim remains blocked until tokenizer, small LM, large LM, and
classifier artifacts exist and model inference smoke passes.

# T36 Release acceptance evidence

Task: T36 — Release acceptance script.

Supports:

```text
R-TEST-003
Release blockers 1-25
```

Implemented files:

```text
src/math_auto_research/workflow/release_acceptance.py
scripts/check_release_acceptance.py
configs/benchmark_runs/geometry_level2_ablation.yaml
scripts/run_newclid_no_browser.py
src/math_auto_research/base/resources/process_runner.py
plugins/geometry_synthetic/provider.py
tests/unit/test_release_acceptance.py
tests/unit/test_resource_governor.py
tests/unit/test_newclid_adapter.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_report.json
```

Notes:

```text
Release acceptance now accounts for all Base Spec Section 20 blockers. The
script writes the full report to the full-rebase evidence directory. The command
surface also runs the Level2 ablation matrix required by R-TEST-001.

Newclid execution no longer opens browser tabs for dependency_graph.html. The
adapter invokes scripts/run_newclid_no_browser.py, which patches Newclid webapp
output generation to avoid dependency graph HTML generation while preserving
run_infos.json, proof.txt, proof_figure.svg, normalized GeoTrace extraction, and
ResourceUsageReport evidence.
```

Commands run:

```text
make test-unit TEST_FILTER=release_acceptance
python scripts/check_no_fixture_release.py
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_ablation.yaml
python -m compileall -q src plugins tests scripts
python scripts/check_no_loose_options.py
make test-unit TEST_FILTER=resource_governor
make test-unit TEST_FILTER=newclid_adapter
make smoke-real-newclid
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
```

Observed results:

```text
release_acceptance unit tests: 4 tests OK.
post-RC8 release_acceptance unit tests: 8 tests OK.
check_no_fixture_release passed.
ablation matrix ran and replay_status=restored.
compileall passed.
check_no_loose_options passed.
resource_governor unit tests: 8 tests OK.
newclid_adapter unit tests: 4 tests OK.
smoke-real-newclid passed.
dependency_graph.html was not regenerated for the real Newclid smoke run.
post-RC8 release acceptance command returned nonzero as expected because
release blocker 11 remains blocked.
release acceptance report status: blocked.
checked blockers: 25.
open blockers: [release_blocker_11_real_provider_smoke_evidence].
claim ceiling: release_acceptance_blocked_no_v0_3_completion_claim.
model_backed_errors:
- missing_model_checkpoint:genesisgeo_compatible
- missing_model_checkpoint:tonggeometry_compatible
- model_backed_evidence_blocker:t24_genesisgeo_adapter.md:missing_genesisgeo_model_checkpoint
- model_backed_evidence_blocker:t25_tonggeometry_adapter.md:does not establish model-backed
- model_backed_evidence_blocker:t25_tonggeometry_adapter.md:missing_tonggeometry_model_paths
```

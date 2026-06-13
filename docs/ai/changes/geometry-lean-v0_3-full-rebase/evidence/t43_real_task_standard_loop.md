# T43 Real Task Standard Geometry Loop Evidence

Task: T43 — Real task standard geometry loop.

## Changed Files

```text
plugins/geometry_synthetic/standard_loop.py
plugins/geometry_synthetic/evaluation.py
src/math_auto_research/lean_integration/lean_port.py
scripts/check_no_fixture_standard_loop_release.py
tests/unit/test_geometry_standard_loop.py
```

## Result

`StandardGeometryProofLoop` now exposes the release-path API:

```python
run_task(task, baseline, selected, run_root) -> TaskRunResult
```

The release path:

```text
- reads task.theorem_file_path and task.theorem_name
- creates GoalAnchor from the real theorem statement
- runs GeometryExtractionContract over the benchmark theorem statement
- calls CompositeSyntheticGeometryProvider when the baseline enables geometry.solve
- runs FinalVerifyGate against the actual theorem file
- writes per-task artifacts under run_root/<baseline>/<task>/
```

Generated per-task artifacts include:

```text
task_result.json
artifact_index.json
selected_implementations.json
controller_strategy_log.json
extraction_report.json
provider_run_manifest.json
provider_result.json
final_verify_report.json
resource_usage_report_*.json
```

`run_fixture()` remains only for unit/regression tests. Release-facing files no
longer call `run_fixture()` or `build_fixture_run()`.

## Verification

```text
python scripts/check_no_fixture_standard_loop_release.py
status: passed

make test-integration TEST_FILTER=standard_geometry_loop
status: passed, 8 tests

make smoke-geometry-final-verify
status: passed

git diff --check
status: passed, CRLF warnings only
```

## Claim Ceiling

T43 is complete. No v0.3 completion claim is made because the Level2 matrix,
release acceptance, and closure tasks remain.

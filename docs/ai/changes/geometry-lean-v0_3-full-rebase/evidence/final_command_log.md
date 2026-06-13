# Final command log

Track: geometry x Lean v0.3 full rebase.

All commands below were run on 2026-06-13 from repository root.

## Global verification

```text
make fmt
status: passed

make lint
status: passed

make typecheck
status: passed

make test
status: passed
observed: unit discover ran 201 tests OK with 1 skipped; regression ran 116 tests OK; mutation ran 67 tests OK; integration ran 31 tests OK with 1 skipped.

make lean-build
status: passed
observed: Build completed successfully. Lake reported local changes under .lake/packages/UnicodeBasic and .lake/packages/batteries.

make lean-no-sorry
status: passed

make smoke-env-bootstrap
status: passed
observed: DependencyResolutionReport emitted; Newclid installed, GenesisGeo vendored, TongGeometry vendored, unresolved=[].

make smoke-resource-governor
status: passed

make smoke-model-provider-set
status: passed

make smoke-geometry-extraction
status: passed

make smoke-geometry-provider
status: passed

make smoke-geometry-trace
status: passed

make smoke-geometry-construction
status: passed

make smoke-geometry-final-verify
status: passed

make smoke-real-newclid
status: passed
observed: real_integration_flag=true, fixture_flag=false, geotrace_ref present, proof_use_status=not_allowed.

make smoke-real-genesisgeo
status: passed
observed: GenesisGeo-compatible process path admitted; result remains proof_use_status=not_allowed.

make smoke-real-tonggeometry
status: passed
observed: heavy budget admits TongGeometry-compatible path; medium budget does not run heavy search.

make smoke-level2-pilot
status: passed
observed: B0-B5 matrix completed and replay_status=restored.
```

## Required scripts

```text
python scripts/check_old_specs_removed.py
status: passed through release acceptance report

python scripts/check_package_layout.py
status: passed through release acceptance report

python scripts/check_domain_contamination.py
status: passed through make lint and release acceptance report

python scripts/check_no_loose_options.py
status: passed through make lint and release acceptance report

python scripts/check_model_hardcode.py
status: passed through release acceptance report

python scripts/check_resource_bypass.py
status: passed through release acceptance report

python scripts/check_no_fixture_release.py
status: passed

python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_ablation.yaml
status: passed
observed: ablation matrix completed and replay_status=restored.

python scripts/generate_repro_report.py --run-dir runs/geometry_level2_pilot
status: passed
observed: replay_status=restored and missing_components=[].

python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
post-RC8 status: blocked
observed: checked_blockers=25, open_blockers=[release_blocker_11_real_provider_smoke_evidence], claim_ceiling=release_acceptance_blocked_no_v0_3_completion_claim.
```

## Follow-up fix during final verification

```text
make test initially failed because test_plugin_registry asserted global module
absence after unrelated tests had already imported geometry plugin modules.
The test was corrected to inspect modules newly imported by PluginLoader only.
Focused plugin registry test then passed, and make test passed.
```

## Browser suppression evidence

```text
Newclid webapp HTML generation opened dependency_graph.html in the user's
browser during release acceptance. The adapter now invokes
scripts/run_newclid_no_browser.py, which patches Newclid webapp generation to a
no-op for browser-facing HTML. After the change, make smoke-real-newclid passed
and runs/provider_newclid/geometry_request_real_newclid_smoke_9bb71b288dbd6746/html/dependency_graph.html
was not regenerated.

Post-RC8 hardening adds scripts/no_browser_sitecustomize/sitecustomize.py and
injects it through release acceptance and provider subprocess environments.
Focused tests passed:

make test-unit TEST_FILTER=newclid_adapter
make test-unit TEST_FILTER=release_acceptance

The release acceptance command was rerun after hardening. It completed without
changing the dependency_graph.html inventory:

BEFORE_COUNT=7
AFTER_COUNT=7

The command returned nonzero because the report is intentionally blocked until
model-backed GenesisGeo and TongGeometry evidence is provided.
```

## GenesisGeo model-backed smoke remediation

```text
python -c "from huggingface_hub import snapshot_download; snapshot_download('ZJUVAI/GenesisGeo', local_dir='models/GenesisGeo', local_dir_use_symlinks=False)"
status: passed
observed: models/GenesisGeo/model.safetensors downloaded with sha256:77406d21e84699b3d0d123653e40b7f48f3642beae10c0b608f58249223b8099.

conda create -y -n geolean-py310 python=3.10
status: passed
observed: C:\Users\bakat\miniforge3\envs\geolean-py310\python.exe reports Python 3.10.20.

C:\Users\bakat\miniforge3\envs\geolean-py310\python.exe scripts/run_genesisgeo_probe.py --request-id probe --claim-spec-json "{}"
status: passed
observed: blocker_reasons=[], model_checkpoint_status=available, model_inference_status=available, architecture=Qwen3ForCausalLM, model_type=qwen3.

make smoke-real-genesisgeo
status: passed
observed: construction_candidate_refs includes aux_construction_candidate:geometry_request:real_genesisgeo_smoke:construction_proposer:genesisgeo_real.

python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
post-Genesis remediation status: blocked
observed: GenesisGeo removed from model_backed_errors; remaining errors are missing_model_checkpoint:tonggeometry_compatible and TongGeometry evidence blockers.
dependency_graph.html inventory remained unchanged: BEFORE_COUNT=7, AFTER_COUNT=7.
```

## Browser suppression follow-up

```text
The first browser suppression pass did not cover direct make-target execution
or pyvis.Network.show. Additional hardening was applied:

- Makefile exports BROWSER as a no-op Python command for all targets.
- Makefile prepends scripts/no_browser_sitecustomize to PYTHONPATH for all targets.
- scripts/no_browser_sitecustomize/sitecustomize.py patches webbrowser,
  os.startfile, and pyvis.Network.show.
- scripts/run_newclid_no_browser.py imports the no-browser sitecustomize before
  importing Newclid and also patches pyvis.Network.show directly.

Verification:

$env:PYTHONPATH = (Resolve-Path scripts\no_browser_sitecustomize).Path; python -
status: passed
observed: pyvis.network.Network.show resolves to _show_without_browser and calls
write_html(..., open_browser=False).

make test-unit TEST_FILTER=newclid_adapter
status: passed
observed: 5 tests OK.

python -m compileall -q scripts plugins src tests
status: passed

make smoke-real-newclid
status: passed
observed: dependency_graph.html inventory remained unchanged:
DEPENDENCY_GRAPH_COUNT_BEFORE=7
DEPENDENCY_GRAPH_COUNT_AFTER=7.

python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
status: blocked
observed: only open blocker remains release_blocker_11_real_provider_smoke_evidence
for missing TongGeometry model-backed checkpoint/evidence. Browser suppression
held during the full command:
DEPENDENCY_GRAPH_COUNT_BEFORE=7
DEPENDENCY_GRAPH_COUNT_AFTER=7.
```

## Blocked closure synchronization

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance.json
status: synchronized with release_acceptance_report.json
observed: both reports now show status=blocked, open_blockers=[release_blocker_11_real_provider_smoke_evidence],
and model_backed_errors=[missing_model_checkpoint:tonggeometry_compatible].

docs/ai/changes/geometry-lean-v0_3-full-rebase/CLOSURE.md
status: updated
observed: closure claim remains BLOCKED_FOR_V0_3_FULL_IMPLEMENTED_EXPERIMENT_READY
with exact blocker missing_model_checkpoint:tonggeometry_compatible.

docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v03_full_completion_blocker_report.md
status: added
observed: report lists blocking R-IDs/Plan tasks, current machine evidence,
implemented TongGeometry hash/smoke support, and required artifacts to unblock.

make test-unit TEST_FILTER=release_acceptance
status: passed
observed: 8 tests OK.

python -m compileall -q scripts plugins src tests
status: passed

git diff --check
status: passed
```

## TongGeometry model-backed probe hardening

```text
gh release list --repo bigai-ai/tong-geometry --limit 10
gh api repos/bigai-ai/tong-geometry/releases --jq '.[] | {tag_name,name,assets:[.assets[].name]}'
status: passed
observed: release tag public / name 1.0 exists, assets=[].

gh api repos/bigai-ai/tong-geometry/git/trees/public?recursive=1 --jq ...
status: passed
observed: no checkpoint-like paths for checkpoint, ckpt, safetensors,
pytorch_model, model.bin, LM_FT, CLS, or tokenizer.

python scripts/run_tonggeometry_probe.py --request-id probe --claim-spec-json "{}"
status: passed
observed: model_checkpoint_hash=null, model_inference_status=unavailable,
blocker_reasons=[missing_tonggeometry_model_paths:tokenizer,lm_s,lm_l,cls].

make test-unit TEST_FILTER=tonggeometry_adapter
status: passed
observed: 6 tests OK.

python -m compileall -q scripts plugins src tests
status: passed

make smoke-real-tonggeometry
status: passed
observed: heavy_search engine_family=tonggeometry_compatible,
checkpoint_hash=unavailable, logs_ref=external_tonggeometry_stdout, and
proof_use_status=not_allowed.

make test-unit TEST_FILTER=release_acceptance
status: passed
observed: 8 tests OK.

make test-integration TEST_FILTER=tonggeometry_adapter
status: passed
observed: 6 tests OK.

make test-regression TEST_FILTER=heavy_search_budget_gate
status: passed
observed: 1 test OK; domain/no-loose checks passed.

make test-regression TEST_FILTER=heavy_search_no_orphans
status: passed
observed: 1 test OK; domain/no-loose checks passed.

python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
status: blocked
observed: only open blocker remains release_blocker_11_real_provider_smoke_evidence.
Remaining model_backed_errors: missing_model_checkpoint:tonggeometry_compatible.
Browser suppression held:
DEPENDENCY_GRAPH_COUNT_BEFORE=7
DEPENDENCY_GRAPH_COUNT_AFTER=7.
```

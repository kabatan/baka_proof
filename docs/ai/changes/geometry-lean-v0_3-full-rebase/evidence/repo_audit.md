---
title: T01 Evidence — Current Repo Audit
date: 2026-06-13
task: T01
status: COMPLETED
authority: Evidence record only; no implementation code was changed by this audit.
---

# T01 Evidence — Current Repo Audit

## Scope

This audit records the repository state before T02 cleanup and later implementation refactoring under `MARP-GEOLEAN-BASE-004 / MARP-GEOLEAN-PLAN-004`.

Machine-readable inventory:

- `repo_file_inventory.json`

Inventory count:

```text
1193 files from rg --files
```

## Superseded Root Specs To Delete Or Retire In T02

The following active/ambiguous root-level documents exist and are superseded by `BASE-004 / PLAN-004`.

| Path | SHA-256 |
|---|---|
| `geometry_lean_guardian_ACTIVE_CONTEXT_draft_v0_2.md` | `f9ccff0803d29e35b2ee4459eeb70fbda9033cf235063cd1b3e40bdbd41995fe` |
| `geometry_lean_guardian_BASE_SPEC_draft_v0_2.md` | `9fcba98d477529ba7172ec29b04e412ec75cb110d8a21b3c822e71ded9506994` |
| `geometry_lean_guardian_PLAN_draft_v0_2.md` | `0a43e3a0de77365b848ad4eac8692b560e3032f1599a207fdf70e26c9e763a7f` |
| `geometry_lean_guardian_RESOURCE_POLICY_TEMPLATE_draft_v0_2.md` | `32b0536f5cb443e5960f44f43e43c44dcff6fd803d18042aef318863ff07dfc4` |
| `geometry_lean_guardian_SOURCE_MAP_draft_v0_2.md` | `7fc35b740dd33d2664a59ac0f14b42501f2aa502f79f1fb2cc9429e6708c4124` |
| `geometry_lean_guardian_v0_2_sha256sums.txt` | `6dfaae51d98d6cb0e8ea95acdbe483a51b3753373db73aa82ab4e38b027e5b49` |
| `geometry_lean_pipeline_plan_v0_3.md` | `c9086d6d9d7de4b809c3935a26d8ced0a429085097954760982183e117eca5e7` |

T02 action required:

- Delete the root-level v0.2 Guardian drafts and hash file after preserving this index.
- Move `geometry_lean_pipeline_plan_v0_3.md` to `docs/ai/changes/geometry-lean-v0_3-full-rebase/source/` with a non-authoritative header, or delete it if source retention is not needed.

## Duplicate Package Paths

Both package roots currently exist:

```text
math_auto_research/
src/math_auto_research/
```

Observed top-level package files:

```text
math_auto_research/__init__.py
math_auto_research/__pycache__/__init__.cpython-312.pyc
```

T03 action required:

- Audit `math_auto_research/__init__.py`.
- Move any unique non-generated content into `src/math_auto_research`.
- Delete the duplicate top-level package and generated pycache.
- Add `scripts/check_package_layout.py`.

## Fixture-Oriented Production Drift

The repo still contains fixture-oriented paths or configs that are incompatible with final release config under `BASE-004`.

Examples requiring later cleanup or quarantine:

- `configs/benchmark_runs/geometry_level2_smoke.yaml` and `geometry_level2_ablation.yaml` use `sample_target_fixture` and fixture model tiers.
- `configs/model_provider_sets/default.example.yaml` selects `fixture_provider`.
- `configs/selected_implementations/geometry_default.yaml` selects `dummy_controller` and `dummy_worker`.
- `plugins/geometry_synthetic/provider.py` contains fixture adapter classes and dummy adapter markers.
- `plugins/geometry_synthetic/evaluation.py`, `run_trace.py`, and `standard_loop.py` currently build fixture-level runs.
- `scripts/check_release_acceptance.py` is still fixture-ceiling oriented.
- `scripts/generate_repro_report.py` builds a fixture run.

T02/T03/T33/T36 action required:

- Fixture providers may remain only under test/fixture locations allowed by `BASE-004`.
- Release and real experiment configs must not select fixture providers.
- Add `scripts/check_no_fixture_release.py`.

## Current Makefile Surface

Current `Makefile` exposes:

```text
fmt
lint
typecheck
test
test-unit
test-mutation
test-regression
test-integration
smoke-env-bootstrap
smoke-resource-governor
smoke-model-provider-set
lean-build
lean-no-sorry
smoke-target-library-status
smoke-geometry-extraction
smoke-geometry-context-fixture
smoke-leangeo-fixture
smoke-leangeo-extraction
smoke-geometry-provider
smoke-geometry-trace
smoke-geometry-construction
smoke-geometry-final-verify
```

Missing from the final `PLAN-004` global command surface:

```text
make smoke-real-newclid
make smoke-real-genesisgeo
make smoke-real-tonggeometry
make smoke-level2-pilot
python scripts/check_old_specs_removed.py
python scripts/check_package_layout.py
python scripts/check_model_hardcode.py
python scripts/check_resource_bypass.py
python scripts/check_no_fixture_release.py
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_ablation.yaml
python scripts/generate_repro_report.py --run-dir runs/<RUN_ID>
```

## No Code Edits

T01 did not change implementation code. It created only audit evidence.

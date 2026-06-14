---
title: Guardian Plan Amendment — geometry x Lean v0.3A real integration recovery
plan_id: MARP-GEOLEAN-PLAN-003A
base_spec: MARP-GEOLEAN-BASE-003A
amends: MARP-GEOLEAN-PLAN-003
version: v0.3A-recovery-admitted
status: ARCHIVED_SUPERSEDED_BY_MARP-GEOLEAN-BASE-007
created: 2026-06-12
purpose: Define recovery execution order for resolving v0.3 completion blockers without expanding claims prematurely.
authority: Guardian-admitted execution contract for v0.3A recovery; cannot add or weaken BASE-003A requirements.
---

# Guardian Plan Amendment — geometry x Lean v0.3A

## 0. Plan Boundary

This Plan executes `MARP-GEOLEAN-BASE-003A`.

It does not authorize full v0.3 completion claims. Until v0.3A acceptance and final reviews pass, claims remain limited to the existing fixture-level release acceptance.

Fixture adapters and fixture tests must remain as regressions. Recovery work must add real-integration evidence that can be distinguished from fixture behavior.

## 1. Execution Rules

For each task, Codex must:

1. read `docs/ai/ACTIVE_CONTEXT.md`;
2. read this Plan task and required BASE-003A R-IDs;
3. read files in the task ReadSet before editing;
4. update scope before editing outside the ReadSet;
5. run task verification;
6. write evidence under `docs/ai/changes/geometry-lean-v0_3a/evidence/` or `runs/<run_id>/`;
7. commit after each coherent task or blocker-resolution unit.

Stop and request review if a task requires weakening trust rules, using another target library, bypassing ResourceGovernor, bypassing FinalVerifyGate, using raw provider output as proof evidence, destructive OS-level changes outside the repo/local development environment, private credentials, prohibited license terms, impossible hardware, or ResourceGovernor-rejected downloads.

## 2. Task Graph

```text
T-001 preserve fixture evidence
  -> T-002 dependency bootstrap and probe
  -> T-003 ResourceGovernor enforcement
  -> T-004 CompositeSyntheticGeometryProviderV1
  -> T-005 Newclid-compatible symbolic closure
  -> T-006 GenesisGeo-compatible construction proposer
  -> T-007 TongGeometry-compatible heavy search
  -> T-008 LeanGeoSubsetV1.RealSmokeCorpus
  -> T-009 real-vs-fixture integration tests
  -> T-010 release acceptance and final reviews
```

Review checkpoints:

- RC-003A-1 after T-002: dependency bootstrap and claim ceiling.
- RC-003A-2 after T-004: provider/resource boundary.
- RC-003A-3 after T-007: real engine integrations or blocker evidence.
- RC-003A-4 after T-009: corpus and real-vs-fixture tests.
- RC-003A-5 after T-010: final closure claim.

## 3. Tasks

### T-001 — Preserve current fixture-level evidence

Supports: `R-CLAIM-REAL-001`, all inherited v0.3 trust and regression requirements.

ReadSet:

- `docs/ai/changes/geometry-lean-v0_3/CLOSURE.md`
- `docs/ai/changes/geometry-lean-v0_3/evidence/v03_completion_blocker_report.md`
- fixture adapters and tests under `plugins/geometry_synthetic/**` and `tests/**`

Deliverables:

- fixture adapters still pass;
- fixture-level closure remains intact;
- real integration tests are prepared to distinguish fixture path from real path.

Verification:

```text
cmd /c make test-unit
cmd /c make test-regression
```

### T-002 — Implement dependency bootstrap and probe

Supports: `R-ENV-REAL-001`, `R-ENV-REAL-002`.

ReadSet:

- `scripts/probe_dependencies.py`
- `scripts/probe_local_resources.py`
- `pyproject.toml`
- `lakefile.lean`
- existing dependency evidence

Deliverables:

- `scripts/bootstrap_geometry_engines.py`
- `scripts/probe_geometry_dependencies.py`
- `scripts/probe_local_resources.py` updated if needed
- `runs/<run_id>/dependency_probe.json`
- `runs/<run_id>/dependency_resolution_report.json`
- `configs/local_resource_profile.yaml`
- `docs/ai/evidence/dependency_resolution.md`

Required behavior:

- attempt LeanGeo-compatible support, Newclid-compatible engine, GenesisGeo-compatible component, and TongGeometry-compatible engine before reporting blocked;
- pin versions, commits, checksums, or local vendoring records;
- record blocked dependencies as blockers, not stop conditions.

Verification:

```text
python scripts/bootstrap_geometry_engines.py --dry-run
python scripts/probe_geometry_dependencies.py --json
python scripts/probe_local_resources.py --json
```

### T-003 — Implement ResourceGovernor enforcement

Supports: `R-RESOURCE-REAL-001`.

ReadSet:

- `src/math_auto_research/base/resources/**`
- provider adapter modules
- resource tests

Deliverables:

- all real engine launches use ResourceGovernor;
- direct provider subprocess launch is absent or rejected;
- direct-launch prevention, per-engine semaphores, timeouts, process group termination, heartbeat/stale detection, Lean/FinalVerify priority, and ResourceUsageReport are implemented and enforced;
- disk and checkpoint cache limits are enforced, or measured and reported when platform support prevents enforcement.

Verification:

```text
cmd /c make test-unit
cmd /c make test-regression
python scripts/probe_local_resources.py --json
```

Required tests:

- direct provider subprocess launch rejected or absent;
- per-engine semaphore works;
- heavy search cannot starve Lean build;
- timeout kills process group;
- ResourceUsageReport exists for success, timeout, and failure;
- disk/checkpoint cache limits are enforced or measured and reported.

### T-004 — Implement CompositeSyntheticGeometryProviderV1

Supports: `R-PROVIDER-REAL-001`, `R-PROVIDER-REAL-002`.

ReadSet:

- `plugins/geometry_synthetic/providers/**`
- `plugins/geometry_synthetic/solver_provider/**`
- provider schemas and tests

Deliverables:

- `CompositeSyntheticGeometryProviderV1`;
- Base-visible `GeometrySolverProvider` interface remains singular;
- provider manifest records internal engine used;
- real integration flag and fixture flag are explicit.

Verification:

```text
cmd /c make smoke-geometry-provider
python scripts/check_domain_contamination.py
cmd /c make test-regression
```

### T-005 — Newclid-compatible symbolic closure integration

Supports: `R-REAL-NEWCLID-001`, `R-PROVIDER-REAL-002`, `R-RESOURCE-REAL-001`.

Deliverables:

- real engine health check or documented unresolved dependency blocker;
- `GeometryClaimSpec -> real engine input -> real engine run -> raw log -> GeoTraceV1 | Diagnostic`;
- ProviderRunManifest and ResourceUsageReport;
- tests proving raw output is not proof-use.

Verification:

```text
python scripts/probe_geometry_dependencies.py --engine newclid_compatible --json
cmd /c make smoke-geometry-provider
cmd /c make test-regression
```

### T-006 — GenesisGeo-compatible construction proposer integration

Supports: `R-REAL-GENESISGEO-001`, `R-PROVIDER-REAL-002`, `R-RESOURCE-REAL-001`.

Deliverables:

- real run producing non-fixture construction candidate or genuine Diagnostic;
- `AuxiliaryConstructionCandidateV1`;
- raw proposer output remains non-proof-use;
- ConstructionCompiler handles candidate or returns blocker.

Verification:

```text
python scripts/probe_geometry_dependencies.py --engine genesisgeo_compatible --json
cmd /c make smoke-geometry-construction
cmd /c make test-regression
```

### T-007 — TongGeometry-compatible heavy-search integration

Supports: `R-REAL-TONGGEOMETRY-001`, `R-RESOURCE-REAL-001`.

Deliverables:

- policy-gated heavy/extreme run path;
- exclusive heavy_search slot by default;
- timeout Diagnostic and ResourceUsageReport;
- raw heavy-search output remains non-proof-use;
- fixture-only heavy search cannot satisfy real heavy-search acceptance.

Verification:

```text
python scripts/probe_geometry_dependencies.py --engine tonggeometry_compatible --json
cmd /c make smoke-geometry-provider
cmd /c make test-regression
```

### T-008 — Define LeanGeoSubsetV1.RealSmokeCorpus

Supports: `R-CORPUS-REAL-001`, `R-CLAIM-REAL-001`.

Deliverables:

- `benchmarks/leangeo/real_smoke_corpus.yaml`;
- theorem file paths, names, statement hashes, expected extraction classes, supported predicates, coverage, expected final status, acceptance eligibility;
- extraction, safe reject, statement mutation, and toy-library substitution tests.

Verification:

```text
cmd /c make lean-build
cmd /c make test-regression
```

### T-009 — Add real-vs-fixture integration tests

Supports: all v0.3A R-IDs.

Required test families:

- dependency evidence tests;
- provider manifest tests;
- real output normalization tests;
- fixture flag rejection tests;
- ResourceGovernor enforcement tests;
- LeanGeo corpus extraction/final verification tests;
- claim ceiling tests.

Verification:

```text
cmd /c make test
cmd /c make test-regression
cmd /c make test-mutation
cmd /c make lean-build
cmd /c make lean-no-sorry
```

### T-010 — Re-run release acceptance and final reviews

Supports: `R-CLAIM-REAL-001`.

Deliverables:

- v0.3A release acceptance report;
- updated closure with only supported claim ceiling;
- spec verifier review;
- quality reviewer review;
- Guardian boundary review.

Verification:

```text
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_smoke.yaml
```

Closure rules:

- Do not mark R-IDs VERIFIED unless the review process explicitly supports it.
- If any real engine remains unresolved, keep the specific blocker open.
- Do not claim real Level 2 advantage.

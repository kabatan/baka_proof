---
title: Guardian Base Spec Amendment — geometry x Lean v0.3A real integration recovery
spec_id: MARP-GEOLEAN-BASE-003A
amends: MARP-GEOLEAN-BASE-003
version: v0.3A-recovery-admitted
status: GUARDIAN_BOUNDARY_ADMITTED_FOR_RECOVERY
created: 2026-06-12
lane: Guardian Lane
purpose: Define correctness requirements for recovering from v0.3 fixture-level closure blockers into a real-integration track.
authority: Guardian-admitted amendment for v0.3A recovery work; constrains recovery work together with BASE-003.
source_documents:
  - C:/Users/bakat/Downloads/v03_completion_blocker_response_instructions.md
  - docs/ai/changes/geometry-lean-v0_3/evidence/v03_completion_blocker_report.md
  - docs/ai/changes/geometry-lean-v0_3/CLOSURE.md
---

# Guardian Base Spec Amendment — geometry x Lean v0.3A

## 0. Authority And Relationship To BASE-003

This Guardian-admitted amendment defines the recovery target:

```text
V0.3A_REAL_INTEGRATION_RECOVERY
```

It does not replace `MARP-GEOLEAN-BASE-003`. All existing trust, proof-use, target-library, no-loose-options, Base/plugin separation, ResourceGovernor, FinalVerifyGate, GraphPatch-only mutation, and evidence-bound-claim requirements remain in force.

If this amendment conflicts with `BASE-003`, the stricter trust rule wins unless the user explicitly approves a later Base Spec amendment and Guardian boundary review admits it.

The v0.3 fixture-level closure remains valid only for its recorded fixture scope. It must not be reinterpreted as full v0.3 completion.

## 1. Recovery Purpose

The purpose of v0.3A is to move from fixture-level acceptance toward real-integration evidence for:

1. real Newclid-compatible symbolic closure integration;
2. real GenesisGeo-compatible construction proposal integration;
3. real TongGeometry-compatible heavy-search integration;
4. a limited, explicitly declared `LeanGeoSubsetV1.RealSmokeCorpus`;
5. tests and evidence that distinguish real provider behavior from fixture behavior.

v0.3A does not include a real Level 2 advantage claim. Real Level 2 advantage is deferred to a later target, for example `V0.4_LEVEL2_REAL_ADVANTAGE_EVALUATION`.

## 2. Claim Ceiling

Until all v0.3A acceptance criteria pass with fresh evidence, the only allowed positive claim remains:

```text
The geometry x Lean v0.3 Guardian track passed fixture-level release acceptance and final reviews for the recorded fixture scope.
```

After v0.3A passes, the maximum allowed claim may expand only to:

```text
The geometry x Lean pipeline has real-integration evidence for the selected provider engines and limited LeanGeoSubsetV1.RealSmokeCorpus under the recorded trust boundary.
```

Still disallowed after v0.3A:

- arbitrary LeanGeo theorem support;
- broad geometry automation;
- open-problem solving;
- real Level 2 advantage;
- production-safe claims unless separately reviewed;
- R-ID VERIFIED claims without explicit Guardian evidence and review authority.

## 3. Scope

### 3.1 In Scope

v0.3A recovery MUST include:

- reproducible dependency bootstrap and probing for Lean/Lake, LeanGeo-compatible support, Newclid-compatible symbolic closure, GenesisGeo-compatible construction proposal, TongGeometry-compatible heavy search, Python packages, local solver binaries, and build scripts;
- repo-managed dependency records and local resource profile;
- ResourceGovernor enforcement for every real provider process;
- exactly one Base-visible `GeometrySolverProvider` boundary;
- `CompositeSyntheticGeometryProviderV1` with internal engine roles;
- mandatory `ProviderRunManifest` for real runs;
- fixture-vs-real separation tests;
- limited real LeanGeo corpus manifest and corpus checks;
- release acceptance and final reviews after implementation.

### 3.2 Out Of Scope

v0.3A MUST NOT claim or implement as completion criteria:

- arbitrary LeanGeo theorem support;
- real Level 2 advantage;
- broad geometry automation or research-performance claims;
- open-problem solving ability;
- multiple Base-visible geometry providers;
- replacement of LeanGeoSubsetV1 with Mathlib-only geometry or a local toy library;
- raw provider output as proof evidence.

## 4. Recovery Requirements

### R-ENV-REAL-001 — Agent-owned reproducible dependency bootstrap

MUST: The implementation agent is authorized, after amendment admission, to perform dependency bootstrap without further user action for approved scope dependencies, including Lean/Lake dependencies, LeanGeo-compatible package installation or pinning, Newclid-compatible engine installation or vendoring, GenesisGeo-compatible component installation or vendoring, TongGeometry-compatible engine installation or vendoring, Python packages, local solver binaries, build scripts, and local environment files.

MUST: All dependency setup must be reproducible and recorded.

Required evidence:

- `docs/ai/evidence/dependency_resolution.md`
- `runs/<run_id>/dependency_probe.json`
- `runs/<run_id>/dependency_resolution_report.json`
- `configs/local_resource_profile.yaml`
- lockfiles or pinned manifests as applicable

MUST NOT: Silently replace `LeanGeoSubsetV1` with Mathlib-only geometry or a local toy library. If LeanGeo-compatible support cannot be installed, the agent must produce a dependency resolution report and keep real LeanGeo final theorem support blocked.

### R-ENV-REAL-002 — Installation failure is not an immediate stop condition

MUST: `install_status = unavailable` is a blocker for completion claims, not a blocker for recovery work.

The agent MUST attempt, in order:

1. inspect existing repo and dependency files;
2. identify upstream source or package source;
3. install through package manager if available;
4. pin version, commit, and checksum;
5. vendor or add submodule if package installation is not reliable;
6. create a reproducible bootstrap script;
7. run a minimal engine health check;
8. record the result in `DependencyResolutionReport`.

Escalation to the user is required only for missing private credentials, license terms that prohibit local use or vendoring, destructive OS-level changes outside the repo/local development environment, clearly impossible hardware requirements, or downloads rejected by ResourceGovernor policy.

### R-PROVIDER-REAL-001 — Single composite provider boundary

MUST: Base must see exactly one geometry solver provider per run:

```text
GeometrySolverProvider
```

The standard real provider is:

```text
CompositeSyntheticGeometryProviderV1
```

The provider may internally use these engine roles:

```yaml
internal_engine_roles:
  symbolic_closure:
    family: newclid_compatible
    expected_output: GeoTraceV1 | Diagnostic
  construction_proposer:
    family: genesisgeo_compatible
    expected_output: AuxiliaryConstructionCandidateV1 | Diagnostic
  heavy_search:
    family: tonggeometry_compatible
    expected_output: GeoTraceV1 | AuxiliaryConstructionCandidateV1 | ProofPlanCandidate | Diagnostic
    enabled_by_policy_only: true
```

MUST NOT: Base import, branch on, or expose Newclid, GenesisGeo, or TongGeometry as Base concepts.

### R-PROVIDER-REAL-002 — ProviderRunManifest is mandatory

MUST: Every real provider run must produce `ProviderRunManifest`.

The manifest MUST include provider id/version, engine family, engine version, git commit or package version, checkpoint hash if applicable, config hash, random seed if applicable, raw log artifact hash, normalized output hash, fixture flag, real integration flag, unsupported rule count, side-condition loss count, and `ResourceUsageReport` reference.

MUST: A run cannot support a real integration claim if `fixture_flag = true` or if version/commit/checksum evidence is missing for the engine used.

### R-RESOURCE-REAL-001 — ResourceGovernor is mandatory for real providers

MUST: All real provider processes must be launched through `ResourceGovernor`. Direct subprocess launch from provider adapters is forbidden.

ResourceGovernor MUST manage CPU concurrency, memory limit, GPU allocation if present, wall-clock timeout, process group termination, heartbeat/stale process detection, disk usage budget, checkpoint cache budget, Lean/FinalVerifyGate priority over heavy search, per-engine semaphores, and `ResourceUsageReport`.

Default priority:

```text
highest: FinalVerifyGate / Lean build / no-sorry checks
high: ProofWorker compile-repair loop
medium: Newclid-compatible symbolic closure
medium-low: GenesisGeo-compatible construction proposal
lowest / exclusive: TongGeometry-compatible heavy search
```

TongGeometry-compatible heavy search MUST be exclusive by default unless `configs/local_resource_profile.yaml` explicitly permits parallel heavy search.

### R-CORPUS-REAL-001 — LeanGeoSubsetV1.RealSmokeCorpus

MUST: The implementation must define a concrete corpus manifest:

```text
benchmarks/leangeo/real_smoke_corpus.yaml
```

The manifest MUST include theorem file path, theorem name, theorem statement hash, expected extraction class, expected supported predicates, expected construction/rule coverage, expected final verification status, and whether the theorem is allowed for real-integration acceptance.

MUST NOT: Describe this corpus as arbitrary LeanGeo theorem support.

### R-CLAIM-REAL-001 — Claim ceiling discipline

MUST: Closure and user-facing claims remain evidence-bound.

Until v0.3A passes, `CLOSURE.md` or its successor MUST say:

```text
The track has fixture-level release acceptance only.
Real Newclid / GenesisGeo / TongGeometry integration remains unverified.
Real LeanGeo corpus support remains unverified.
Real Level 2 advantage remains unverified and out of scope for this recovery target.
```

After v0.3A passes, closure may claim only real-integration recovery for selected provider roles and the explicitly declared `LeanGeoSubsetV1.RealSmokeCorpus` under the recorded trust boundary and resource policy.

### R-REAL-NEWCLID-001 — Newclid-compatible symbolic closure recovery

MUST: Newclid-compatible integration is the first real provider path to make reliable.

Required path:

```text
GeometryClaimSpec
  -> Newclid-compatible symbolic engine
  -> real raw provider output
  -> normalized GeoTraceV1 or Diagnostic
  -> ProviderRunManifest
```

MUST: Raw Newclid output is never proof evidence. It becomes proof-use relevant only after `GeoTraceV1 -> RuleRegistryV1 -> TraceCompiler -> Lean patch candidate -> ProofWorker -> FinalVerifyGate`.

### R-REAL-GENESISGEO-001 — GenesisGeo-compatible construction proposer recovery

MUST: GenesisGeo-compatible output is used as construction proposal, not proof evidence.

Required path:

```text
GeometryClaimSpec / blocked proof state
  -> GenesisGeo-compatible construction proposer
  -> AuxiliaryConstructionCandidateV1
  -> ConstructionCompiler
  -> generated Lean obligations
  -> ProofWorker / FinalVerifyGate
```

### R-REAL-TONGGEOMETRY-001 — TongGeometry-compatible heavy-search recovery

MUST: TongGeometry-compatible integration is a heavy-search oracle, not the default symbolic closure path.

Allowed uses:

- heavy or extreme auxiliary construction search;
- proof-plan candidates;
- stuck-goal diagnostics;
- construction candidates normalized into `AuxiliaryConstructionCandidateV1`;
- trace candidates normalized into `GeoTraceV1`.

MUST: Raw TongGeometry output is not proof evidence and is not sufficient for a real Level 2 advantage claim.

## 5. Resource Policy Requirements

`configs/local_resource_profile.yaml` MUST include these minimum fields:

```yaml
cpu:
  logical_cores: null
  reserved_for_lean_and_os: 2
  max_provider_workers: null

memory:
  total_gb: null
  reserve_gb: 4
  max_provider_memory_gb: null

gpu:
  available: null
  device_count: null
  vram_gb: null
  allow_genesisgeo_gpu: true
  allow_tonggeometry_gpu: false

disk:
  artifact_cache_limit_gb: null
  checkpoint_cache_limit_gb: null
  raw_log_limit_gb: null

process_policy:
  use_process_groups: true
  kill_on_timeout: true
  heartbeat_interval_sec: 30
```

Budget profiles MUST include exactly these minimum constraints:

```yaml
budget_profiles:
  tiny:
    timeout_sec: 30
    max_parallel_engines: 1
    allowed_roles: [symbolic_closure]

  small:
    timeout_sec: 120
    max_parallel_engines: 1
    allowed_roles: [symbolic_closure]

  medium:
    timeout_sec: 600
    max_parallel_engines: 2
    allowed_roles: [symbolic_closure, construction_proposer]

  heavy:
    timeout_sec: 3600
    max_parallel_engines: 2
    allowed_roles: [symbolic_closure, construction_proposer, heavy_search]
    heavy_search_exclusive: true

  extreme:
    timeout_sec: 14400
    max_parallel_engines: 1
    allowed_roles: [heavy_search]
    heavy_search_exclusive: true
    requires_explicit_run_label: true
```

ResourceGovernor MUST enforce:

```text
Lean build / FinalVerifyGate > ProofWorker > symbolic_closure > construction_proposer > heavy_search
```

Heavy search MUST yield, queue, or fail fast if it would starve Lean verification or proof-worker compilation.

## 6. Anti-overclaim Rules

The implementation agent MUST NOT:

- mark R-IDs VERIFIED from fixture evidence;
- treat installed dependency as real integration without a real provider run;
- treat raw Newclid / GenesisGeo / TongGeometry output as proof evidence;
- bypass `RuleRegistryV1`, `TraceCompiler`, or `ConstructionCompiler`;
- bypass `FinalVerifyGate`;
- replace `LeanGeoSubsetV1` with a local toy library as the target;
- claim arbitrary LeanGeo theorem support;
- claim real Level 2 advantage from smoke counts;
- claim production safety from local success;
- remove fixture tests after adding real integration tests;
- add multiple target libraries or multiple Base-visible solver providers.

## 7. Minimal Acceptance Checklist

v0.3A cannot pass unless:

- BASE-003A and PLAN-003A are admitted before real-integration completion claims;
- dependency bootstrap scripts exist and are reproducible;
- dependency resolution reports each engine status;
- local resource profile is generated;
- ResourceGovernor launches all real provider processes;
- each engine has real run evidence or a documented unresolved dependency blocker;
- ProviderRunManifest exists for each real run;
- real provider tests fail under fixture-only configuration;
- `LeanGeoSubsetV1.RealSmokeCorpus` is explicitly declared;
- corpus extraction, safe reject, and final verification tests pass for admitted entries;
- raw provider output remains non-proof-use;
- RuleRegistryV1, side-condition calculus, ConstructionCompiler, and FinalVerifyGate remain mandatory;
- release acceptance and final reviews are re-run;
- closure states only the claim supported by fresh evidence.

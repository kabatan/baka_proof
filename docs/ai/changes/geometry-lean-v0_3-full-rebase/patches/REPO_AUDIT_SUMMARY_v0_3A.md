---
title: "Current repo audit summary — geometry × Lean v0.3A patch input"
patch_id: "MARP-GEOLEAN-PATCH-004A"
status: "IMPORTED_SOURCE_AUDIT_FOR_PATCH"
target_repo: "kabatan/baka_proof"
created: "2026-06-13"
installed: "2026-06-13"
authority: "Evidence input only; BASE_SPEC_PATCH_v0_3A.md and PLAN_PATCH_v0_3A.md define active amendment requirements after user approval."
---

# Current repo audit summary — v0.3A patch input

This document records the implementation gaps observed after the Codex blocker report `v03_full_completion_blocker_report.md` and a direct inspection of `kabatan/baka_proof`.

It is not an implementation authority by itself. It supports the paired Base Spec patch and Plan patch.

## 1. High-level judgment

The current repository is closer to the intended v0.3 architecture than the earlier fixture-only state, but it is **not yet implemented according to the v0.3 intent**.

The blocker report correctly identifies one machine-visible blocker:

```text
release_blocker_11_real_provider_smoke_evidence
missing_model_checkpoint:tonggeometry_compatible
```

However, repository inspection shows additional, more important experiment-readiness gaps that the current release acceptance script does not fully catch:

```text
A. The Level2 pilot corpus is semantically trivial: nearly all tasks are identity theorems of the form
   h : Coll A B C ⊢ Coll A B C.

B. The Level2 matrix currently derives metrics from corpus metadata and one fixture run,
   not from per-task pipeline execution.

C. The standard loop still has a fixture-only path based on local toy definitions
   (`def Point := Unit`, `def Coll := True`) and `run_fixture()`.

D. The dependency report says TongGeometry is vendored and unresolved=[] even though
   the model artifact is missing; release acceptance catches this separately, but
   the dependency record itself is not expressive enough.

E. Provider implementation exists primarily in a monolithic facade-style module
   `plugins/geometry_synthetic/provider.py`; the Base Spec expected provider internals
   to live under `plugins/geometry_synthetic/providers/**` with a narrow compatibility facade.
```

## 2. What appears aligned with the intended v0.3 design

### 2.1 Guardian authority documents

The repo contains the full-rebase Guardian authority folder:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md
```

The current Base Spec is detailed and correctly states that it is the implementation authority, that v0.3 full experiment-ready is stronger than fixture-level acceptance, and that fixtures cannot satisfy full experiment-ready.

### 2.2 Newclid-compatible real integration

The current evidence says the Newclid-compatible role runs a real Newclid path through the resource-governed process path, emits a `geotrace:` reference, records fixture=false / real=true, and passes `check_no_fixture_release`.

This is consistent with the intended role:

```text
Newclid-compatible symbolic_closure:
  primary symbolic closure and GeoTraceV1 source.
```

### 2.3 GenesisGeo-compatible real integration

The current evidence says GenesisGeo is vendored, the model checkpoint is locally present under `/models/`, model inference smoke is available, the provider emits an `AuxiliaryConstructionCandidateV1`, and raw Genesis rationale remains non-proof.

This is consistent with the intended role:

```text
GenesisGeo-compatible construction_proposer:
  auxiliary construction candidate generation.
```

### 2.4 TongGeometry-compatible code-backed diagnostic path

The current TongGeometry adapter has a vendored source path, import probe, ResourceGovernor-managed subprocess execution, budget gating, timeout / process cleanup evidence, and raw output remains proof-use forbidden.

This satisfies a **code-backed heavy-search diagnostic path**, but not model-backed TongGeometry heavy search.

## 3. Main implementation gaps

### GAP-001 — TongGeometry checkpoint is missing, but this should not be the only blocker model

The current release acceptance blocks full v0.3 because the TongGeometry-compatible model checkpoint is missing. This is accurate under the current `BASE-004` wording, but it is too coarse for practical experiment readiness.

The public TongGeometry source may be vendored and runnable, while the trained checkpoints may be private, unpublished, or not discoverable. Therefore the spec should separate:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY:
  requires code-backed TongGeometry-compatible heavy_search path, resource governance,
  and honest admitted-unavailable model artifact reporting if checkpoints are not public.

V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY:
  requires tokenizer/lm_s/lm_l/cls model paths, aggregate checkpoint hash,
  and model inference smoke available.
```

This split prevents non-public model artifacts from blocking all v0.3 experiment readiness while preserving honesty about what has and has not been achieved.

### GAP-002 — Level2 corpus is too trivial

The current `GeometryLevel2PilotCorpus` appears to use 25 Lean theorem entries that are all variations of:

```lean
theorem level2_pilot_N (A B C : Point) (h : Coll A B C) : Coll A B C := by exact h
```

Even if these import LeanGeo-compatible definitions, they do not exercise:

```text
semantic extraction beyond identity hypothesis lookup,
non-identity RuleRegistry rules,
auxiliary construction admission,
safe-reject diagnostics,
real provider usefulness,
TraceCompiler side-condition calculus.
```

### GAP-003 — Level2 matrix is not artifact-derived

The current matrix code computes metrics from metadata counts such as accepted entries and task categories. It does not appear to run every benchmark task through the actual standard proof loop under B0/B1/B2/B3/B4/B5 and then aggregate artifacts.

This undermines the Level2 pilot’s purpose. A matrix can be experiment-ready even without positive advantage, but it must be driven by real per-task pipeline artifacts.

### GAP-004 — Fixture standard loop remains too close to release path

The standard loop includes a fixture Lean file with local toy definitions:

```lean
def Point := Unit
def Coll (A B C : Point) : Prop := True
```

This is acceptable for unit tests only. It must not be used by release or Level2 matrix code.

### GAP-005 — DependencyResolutionReport lacks claim-profile precision

The current dependency report records TongGeometry as vendored with `checkpoint_hash=null` and `unresolved=[]`. Release acceptance catches the missing checkpoint elsewhere, but the dependency report itself should carry the claim impact:

```text
model_artifact_status = admitted_unavailable | available | unavailable | failed
model_inference_status = available | unavailable | failed | not_applicable
claim_impact = blocks_model_backed_tong_claim | blocks_core_experiment_ready | nonblocking
```

### GAP-006 — Provider module layout has drifted

The Base Spec expected provider internals under:

```text
plugins/geometry_synthetic/providers/**
```

The repo currently has substantial implementation in:

```text
plugins/geometry_synthetic/provider.py
```

A compatibility facade is acceptable, but the actual adapter classes and composite provider logic should be moved under `providers/**` to avoid long-term architecture drift.

## 4. Required patch direction

The patch should not merely unblock TongGeometry. It should harden v0.3 completion acceptance so that:

```text
1. Missing non-public TongGeometry checkpoint is represented honestly and does not falsely block
   core experiment readiness if code-backed heavy_search diagnostics are available.

2. TongGeometry model-backed claims remain blocked until tokenizer/lm_s/lm_l/cls exist and pass smoke.

3. The corpus must become nontrivial enough to exercise extraction, rules, construction,
   safe rejection, and final verification.

4. The Level2 matrix must execute per-task runs and aggregate artifact-derived metrics.

5. Fixture standard loop and local toy geometry cannot satisfy release acceptance.

6. Release acceptance must detect the above conditions automatically.
```

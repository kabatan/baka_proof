<!--
Generated for kabatan/baka_proof Guardian/Codex handoff.
Created: 2026-06-14
Status: USER_APPROVED_ACTIVE
-->
---
title: "Guardian Acceptance Spec — Geometry × Lean Full2D Prover v0.4.2 Governed Full Implementation"
acceptance_id: "MARP-GEOLEAN-ACCEPTANCE-007"
base_spec: "MARP-GEOLEAN-BASE-007"
plan: "MARP-GEOLEAN-PLAN-007"
status: "USER_APPROVED_ACTIVE"
created: "2026-06-14"
---

# Guardian Acceptance Spec — Geometry × Lean Full2D Prover v0.4.2

## 0. Purpose

This document defines the automated checks required before claiming:

```text
V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY
```

The acceptance system must avoid two bad behaviors:

```text
1. Silent weakening:
   Passing release by changing thresholds, removing requirements, or claiming partial completion.

2. Over-blocking:
   Stopping implementation whenever one subsystem is incomplete. Non-fatal issues must become ReleaseBlockers or WorkDebt and Codex must continue other tasks.
```

## 1. Acceptance modes

### Progress acceptance

Command:

```bash
python scripts/check_v0_4_2_progress_acceptance.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml
```

Progress acceptance may return:

```text
status=progress_ok_with_debt
status=progress_blocked_hard
status=progress_failed_infra
```

It is allowed to have ReleaseBlockers and WorkDebt. It is not a release claim.

### Final release acceptance

Command:

```bash
python scripts/check_release_acceptance_v0_4_2.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/release_acceptance_report.json
```

Final release passes only if:

```text
hard_blockers=[]
release_blockers=[]
work_debt_open=[]
all R-IDs passed
all thresholds passed
all anti-gaming checks passed
all release artifacts are reproducible
```

## 2. Severity classification

Every failed check must be classified as:

```text
HardBlocker
ReleaseBlocker
WorkDebt
MeasuredFailure
Informational
```

Only HardBlocker stops Codex. ReleaseBlocker prevents closure but not implementation.

## 3. Required release checks

### A. Guardian authority checks

```text
A-001 exactly one active geometry Base Spec: MARP-GEOLEAN-BASE-007
A-002 older active specs archived
A-003 Plan and Acceptance reference BASE-007
A-004 closure claim ceiling obeys evidence
A-005 no requirement text lowered in repo-local copy
```

### B. Refactor and boundary checks

```text
B-001 plugins/geometry_full2d exists
B-002 release configs do not import geometry_synthetic
B-003 Base imports no geometry_full2d internals
B-004 geometry_full2d imports no geometry_synthetic
B-005 ModelProviderSet boundary preserved
B-006 no AgentC/D taxonomy reintroduced as core runtime mode
```

### C. Target facade checks

```text
C-001 MathAutoResearch.GeometryFull2D Lean namespace builds
C-002 no toy definitions for Point/Line/Circle/Coll/angle/distance
C-003 no axioms/admit/unsafe in release target files
C-004 facade covers required object/predicate/construction families
C-005 facade mapping evidence references LeanGeo/Mathlib sources
```

### D. Structured extraction checks

```text
D-001 Lean-side extraction command exists and runs
D-002 Python regex extraction not used in release path
D-003 CanonicalGeometryStatementV1 schema validates
D-004 every extracted object/predicate has source hash and canonical hash
D-005 nondegeneracy/orientation/order assumptions extracted
D-006 in-target positive tasks not classified unsupported
D-007 target-outside safe-rejects include TargetOutsideReport
```

### E. Engine checks

For every engine role:

```text
E-001 engine implementation exists
E-002 fixture_flag=false in release run
E-003 real_integration_flag=true in release run
E-004 EngineRunRecord schema validates
E-005 ResourceGovernor used
E-006 at least one counted success references this engine role
E-007 engine has negative tests against hard-coded theorem names
E-008 engine cannot produce proof_use_status=final_theorem directly
```

Roles:

```text
synthetic_closure
construction_search
algebraic_geometry
metric_angle
transformation
order_case
inequality
lean_proof_search
portfolio_coordinator
```

### F. Rule registry checks

```text
F-001 concrete rule count >=150
F-002 rule family count >=25
F-003 construction templates >=30
F-004 side-condition discharge procedures >=20
F-005 each rule has side conditions, Lean template, positive/negative/mutation fixtures
F-006 used-rule coverage thresholds pass
F-007 duplicate/inflated rule checks pass
```

Used-rule thresholds:

```text
distinct concrete rules used >=35
distinct rule families used >=15
families outside incidence/collinearity used >=8
families with side-condition discharge used >=5
families with construction introduction used >=4
families with algebraic/metric/angle reasoning used >=3
families with order/case reasoning used >=2
families with transformations used >=2
```

### G. Compiler and proof-use checks

```text
G-001 TraceCompilerFull2D emits LeanPatchCandidateFull2D
G-002 ConstructionCompilerFull2D emits LeanPatchCandidateFull2D
G-003 Algebraic/Metric/Transformation/Order/Inequality compilers emit LeanPatchCandidateFull2D where applicable
G-004 raw solver output not used as proof region replacement
G-005 ProofWorker applies patch only inside proof region
G-006 FinalVerifyGate compiles generated candidate file directly
G-007 SolverBackedProofCertificateFull2D links all required artifacts
G-008 TrustGuard closes final theorem only with FinalVerifyGate + certificate
```

### H. Corpus checks

```text
H-001 positive formal Lean tasks >=3000
H-002 negative/target-outside/malformed tasks >=500
H-003 external/human-curated positive tasks >=900
H-004 synthetic generated positives <=50%
H-005 near duplicates <=10%
H-006 exact template duplicates per family <=5
H-007 difficulty tier floors pass
H-008 frozen_corpus_manifest_hash exists and matches files
```

### I. Performance checks

```text
Full2DCore500 >=0.95
IncidenceParallelPerp350 >=0.92
AngleCyclic450 >=0.90
Construction450 >=0.85
MetricRatioArea350 >=0.85
Transformation250 >=0.75
OrderCase250 >=0.80
Algebraic250 >=0.85
Inequality150 >=0.75
OlympiadStyle300 >=0.70
HardHoldout50 >=0.50
Overall positive >=0.85
In-target positive safe-reject success count = 0
```

### J. Advantage checks

```text
B2 - B1 >=0.25 overall
B2 - B5 >=0.15 construction subset
B2 - B6 >=0.15 algebraic/metric subset
B2 - B7 >=0.10 order/case subset
B2 - B8 >=0.05 olympiad subset if model provider is used
```

### K. Anti-gaming checks

```text
K-001 no theorem-name hard-coding in solver/compiler/proof worker
K-002 final theorem metrics artifact-derived
K-003 no fixture provider manifests counted
K-004 no source theorem already proved counted as solver-backed success
K-005 generated candidate differs only in admitted proof/helper regions
K-006 no corpus edits after frozen manifest
K-007 B1/B2/B5/B6/B7/B8 use identical target corpus and final verification policy
K-008 no threshold values changed from approved Acceptance Spec
K-009 no closure claim while release blockers remain
```

## 4. Report schema

`release_acceptance_report.json` must include:

```yaml
schema_version: "1.0.0"
report_id: "release_acceptance_v0_4_2:..."
status: "passed | failed | blocked"
claim_ceiling: "..."
hard_blockers: []
release_blockers: []
work_debt_open: []
measured_failure_summary: {}
checked_rids: []
checks: []
metrics_summary: {}
advantage_summary: {}
used_rule_coverage_summary: {}
engine_usage_summary: {}
corpus_manifest_hash: "sha256:..."
closure_allowed: false
```

Progress report must include `next_unblocked_work_packages` so Codex can continue without user intervention.

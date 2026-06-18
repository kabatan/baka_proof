---
title: Guardian Active Context — GeometryFull2D v0.5
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-011
version: v0.5-real-solver-causal-reviewed-strict
status: USER_APPROVED_ACTIVE
created: 2026-06-18
last_updated: 2026-06-18
base_spec: MARP-GEOLEAN-BASE-011
plan: MARP-GEOLEAN-PLAN-011
acceptance: MARP-GEOLEAN-ACCEPTANCE-011
purpose: Minimal navigation state for the active GeometryFull2D v0.5 Guardian recovery track.
authority: Navigation only; never overrides the Base Spec, Plan, Acceptance, invariants, evidence, or user approval state.
---

# Guardian Active Context — GeometryFull2D v0.5

## Status

Guardian Lane is active for the GeometryFull2D v0.5 reviewed-strict real solver-causal full pipeline correction track.

Current mission:

```text
Implement V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY under MARP-GEOLEAN-BASE-011 / PLAN-011 / ACCEPTANCE-011.
```

The v0.4.5 closure is invalidated as a false-positive checker-passing scaffold. It remains negative evidence and a red-case source only; it is not active release authority.

## Read First

1. `docs/ai/changes/geometry-full2d-v0_5/BASE_SPEC.md`
2. `docs/ai/changes/geometry-full2d-v0_5/PLAN.md`
3. `docs/ai/changes/geometry-full2d-v0_5/ACCEPTANCE.md`
4. `docs/ai/changes/geometry-full2d-v0_5/RED_CASE_SUITE.md`
5. `docs/ai/changes/geometry-full2d-v0_5/REAL_PIPELINE_INVARIANTS.md`
6. `docs/ai/changes/geometry-full2d-v0_5/REFACTOR_DIRECTIVE.md`
7. `docs/ai/changes/geometry-full2d-v0_5/CODEX_HANDOFF.md`
8. `docs/ai/changes/geometry-full2d-v0_5/FAILURE_ANALYSIS.md`
9. Current Plan work package and required source anchors.
10. Files in the admitted ReadSet before editing.

## Current Task Pointer

Current task:

```text
WP-11 — Actual matrix execution and baselines.
```

Completed preparation:

```text
v0.5 reviewed-strict research-agent bundle imported.
Bundle self-consistency check passed.
Active context and index updated to point to v0.5.
v0.4.5 Guardian authority and closure marked superseded/invalidated as false-positive closure evidence.
v0.5 debt ledger initialized.
Post-admission review loop found fixable Plan/Base/Acceptance alignment gaps and patched them:
  - full Base Spec floor/threshold decision checks;
  - matrix execution before causality, metrics after causality;
  - sealed holdout after implementation freeze;
  - no empty-premise target fact counted success;
  - explicit disabled/failing baseline reports;
  - conditional B8 and closure claim ceiling checks.
WP-01 red-case suite implemented with 19 executable red cases, each with static-code and artifact-run variants.
WP-02 fail-closed acceptance harness, K coverage checker, and checker-suppression guard implemented.
WP-02 evidence captured in docs/ai/changes/geometry-full2d-v0_5/evidence/wp01_wp02_redcase_acceptance_harness.md and wp02_release_acceptance_smoke.json.
WP-03 schema validators implemented with positive/negative self-tests for required v0.5 artifact schemas.
WP-04 corpus system implemented:
  - external goal source discovery wrapper;
  - exact goal-preserved import with content-addressed preservation artifacts;
  - sealed holdout generator blocked from counted generation before freeze;
  - corpus independence, statement diversity, and goal-preservation replay checkers.
WP-04 evidence captured in docs/ai/changes/geometry-full2d-v0_5/evidence/wp04_corpus_system_evidence.md.
WP-05 structured Lean extraction gate implemented:
  - v0.5 extraction builder/checker;
  - LeanExtractionReportFull2D normalization;
  - stale, handwritten, Python-classified, pre-proved, and incomplete/smoke-only extraction rejection.
WP-05 evidence captured in docs/ai/changes/geometry-full2d-v0_5/evidence/wp05_extraction_gate_evidence.md.
WP-06 provider / engine stage boundary implemented:
  - separate `python -m plugins.geometry_full2d.provider_cli` stage;
  - provider/engine downstream-import boundary checker;
  - v0.5 engine output checker;
  - provider/engine release path no longer imports run records or rule registry.
WP-06 evidence captured in docs/ai/changes/geometry-full2d-v0_5/evidence/wp06_provider_boundary_evidence.md.
WP-07 independent solver checkers implemented:
  - provider CLI now writes ClaimSpec and normalized semantic artifacts as content-addressed upstream inputs;
  - `check_independent_solver_checkers_v0_5.py` recomputes role-specific checks from ClaimSpec and artifacts;
  - synthetic target emission was changed to require non-target support for replay;
  - checker report schema rejects self-certified and target-trusting reports.
WP-07 evidence captured in docs/ai/changes/geometry-full2d-v0_5/evidence/wp07_independent_solver_checkers_evidence.md.
WP-08 RuleRegistry implemented:
  - RuleRegistryFull2D emits v0.5 rule contracts with counted/non-counted helper separation;
  - counted rules require input/output patterns, side conditions, generated obligations, Lean template ids, independent checkers, and positive/negative/mutation fixtures;
  - identity/direct-facade helper rules are present only as non-counted helpers;
  - `check_full2d_rule_registry_v0_5.py --self-test` rejects counted identity and naked-target rule registries.
WP-08 evidence captured in docs/ai/changes/geometry-full2d-v0_5/evidence/wp08_rule_registry_evidence.md.
WP-09 compiler input isolation implemented:
  - release compiler CLI accepts ClaimSpec, SelectedSolverDerivationV2, RuleRegistry, and side-condition checker refs;
  - proof-decision behavior is isolated from forbidden corpus/task/family/template/shape metadata;
  - compiler taint checker shows forbidden metadata-only mutations do not change proof-decision output while selected-derivation mutations do;
  - proof-from-shape compiler and rule-list artifact synthesis red cases remain rejected.
WP-09 evidence captured in docs/ai/changes/geometry-full2d-v0_5/evidence/wp09_compiler_input_isolation_evidence.md.
WP-10 ProofWorker and FinalVerifyGate implemented:
  - v0.5 ProofWorker applies LeanPatchCandidateFull2D only inside the MARP proof region;
  - source theorem proof regions must be sorry-only before patching;
  - v0.5 FinalVerifyGate runs `lake env lean`, checks theorem statement unchanged, no sorry, no forbidden declarations, no toy target definitions, admitted imports only, and proof-use provenance;
  - `check_proof_worker_final_verify_v0_5.py --self-test` rejects pre-proved sources, non-region patches, changed theorem statements, sorry, forbidden declarations, toy targets, and non-admitted imports.
WP-10 evidence captured in docs/ai/changes/geometry-full2d-v0_5/evidence/wp10_proof_worker_final_verify_evidence.md.
WP-10A implementation freeze and counted corpus materialization completed for the current implementation hash:
  - freeze manifest binds implementation git head, implementation file hashes, checker hashes, config hash, corpus-tool hashes, and release entrypoints;
  - counted SealedAdversarialHoldout corpus generated after freeze with 1200 counted sealed tasks and 300 negative target-outside/malformed tasks;
  - corpus independence, statement diversity, goal preservation, checker-suppression, and red-case checks pass;
  - fail-closed release probe reports corpus_summary and corpus_statement_diversity_summary as passed, while WP-11+ blockers remain.
WP-10A evidence captured in docs/ai/changes/geometry-full2d-v0_5/evidence/wp10a_freeze_corpus_evidence.md.
```

Implementation work proceeds from WP-11. The WP-10A freeze must be regenerated after later changes to provider, compiler, rule registry, proof worker, final verifier, matrix runner, release checker, corpus generator, or checker code.

## Non-Negotiables

- Do not implement another report-shaped pipeline.
- Do not target green acceptance first.
- Implement red cases and acceptance coverage before provider/compiler/rule implementation.
- Do not use v0.4.5 closure or run records as v0.5 success evidence.
- Do not suppress checker findings by filename, role, or release path.
- Do not count target-fact providers, naked target assertions, identity rules, proof-from-shape compilers, report-only causality, family-coded baselines, or stale evidence.

## Evidence Folder

```text
docs/ai/changes/geometry-full2d-v0_5/evidence/
```

## Current Claim Ceiling

Allowed:

```text
MARP-GEOLEAN-BASE-011 / PLAN-011 / ACCEPTANCE-011 are active; WP-01 through WP-04 implementation gates have local evidence.
WP-05 extraction gate has local evidence.
WP-06 provider boundary and engine-output gates have local evidence.
WP-07 independent solver checker gates have local evidence.
WP-08 RuleRegistry gate has local evidence.
WP-09 compiler input isolation and taint gates have local evidence.
WP-10 ProofWorker and FinalVerifyGate gates have local evidence.
WP-10A freeze and counted corpus gates have local evidence for the current implementation hash.
```

Not allowed yet:

```text
V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
PRODUCTION_SAFE
R-ID VERIFIED
```

---
title: "Guardian Plan — GeometryFull2D v0.4.4 Real Solver-Causal Pipeline Reviewed"
plan_id: "MARP-GEOLEAN-PLAN-009"
base_spec: "MARP-GEOLEAN-BASE-009"
revision: "reviewed-2026-06-18"
status: "USER_APPROVED_ACTIVE"
---

# Guardian Plan — GeometryFull2D v0.4.4 Real Solver-Causal Pipeline Reviewed

## 0. Operating rule for Codex

Codex must implement this Plan exactly against `MARP-GEOLEAN-BASE-009` reviewed revision. It must not reduce scope, lower thresholds, reinterpret projection tasks as external goals, require user-reviewed tasks as a release precondition, or close with a partial claim.

Codex may proceed with ReleaseBlockers and WorkDebt. It stops only for HardBlockers. Final closure is forbidden until all acceptance checks pass.

## 1. Definition of done

Done means this command returns 0:

```bash
python scripts/check_release_acceptance_v0_4_4.py \
  --config configs/benchmark_runs/geometry_full2d_v0_4_4.yaml \
  --output docs/ai/changes/geometry-full2d-v0_4_4/evidence/release_acceptance_report.json
```

The report must include:

```json
{
  "status": "passed",
  "claim_ceiling": "V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY",
  "hard_blockers": [],
  "release_blockers": [],
  "work_debt_open": [],
  "closure_allowed": true
}
```

No other report, partial acceptance, old v0.4.3 closure, or checker-specific success is sufficient.

## 2. Work packages

### WP00 — Authority reset

1. Create `docs/ai/changes/geometry-full2d-v0_4_4/`.
2. Install approved v0.4.4 reviewed docs there:
   - `BASE_SPEC.md`
   - `PLAN.md`
   - `ACCEPTANCE.md`
   - `REAL_PIPELINE_INVARIANTS.md`
   - `REFACTOR_DIRECTIVE.md`
   - `SOURCE_MAP.md`
   - `ACTIVE_CONTEXT.md`
   - `CODEX_HANDOFF.md`
   - `SELF_REVIEW_LOG.md`
   - `README.md`
   - `FAILURE_ANALYSIS.md`
   - `evidence/bundle_sha256sums.txt`
   - `evidence/v0_4_4_bundle_import.md`
3. Mark v0.4.3 and earlier v0.4.4 drafts superseded.
4. Implement `scripts/check_active_guardian_spec_v0_4_4.py`.
5. Initialize `docs/ai/changes/geometry-full2d-v0_4_4/debt/debt_ledger.jsonl`.

Acceptance:

```bash
python scripts/check_active_guardian_spec_v0_4_4.py
```

### WP01 — Quarantine old release paths

1. Remove v0.4.3 release commands from v0.4.4 release path.
   - Renamed, wrapped, copied, shimmed, or substantially equivalent v0.4.3 release commands are also forbidden unless they are regression fixtures that v0.4.4 checks prove fail.
   - The release-path checker must inspect v0.4.4 release entrypoints by path, imports, call graph / direct invocation targets, command provenance, and known old-entrypoint hashes or implementation signatures. It must not rely only on filename matching.
2. Archive but do not use for release positives:
   - `generate_full2d_external_projection_corpus.py`
   - v0.4.3 projection corpus artifacts
   - v0.4.3 release acceptance reports and closure files
   - any matrix that counts from projection labels or proof-artifact overlays
3. Add regression fixtures where those old paths are expected to fail.

Acceptance:

```bash
python scripts/check_no_projection_release_path_v0_4_4.py
python scripts/check_anti_v043_projection_regression.py
```

### WP02 — Corpus schemas and gates

Implement these categories:

```text
ExternalGoalPreserved
SealedSolverChallenge
UserReviewedGoal
NegativeTargetOutsideMalformed
ProjectionNonCounted
```

Tasks:

1. Define `benchmarks/geometry_full2d_v0_4_4/corpus_manifest.schema.json`.
2. Define `GoalPreservationReportV1` schema.
3. Define `SealedChallengeManifestV1` schema.
4. Define `ReviewManifestV1` schema.
5. Implement corpus checker.
   - It must report and enforce every positive family floor from Base Spec section 4.2, not only global positive and negative counts.
6. Implement goal preservation checker.
7. Implement sealed challenge checker.
8. Implement review manifest checker.

Acceptance:

```bash
python scripts/check_full2d_corpus_manifest_v0_4_4.py --corpus-root benchmarks/geometry_full2d_v0_4_4
python scripts/check_goal_preservation_reports.py --corpus-root benchmarks/geometry_full2d_v0_4_4
python scripts/check_sealed_challenge_manifest.py --corpus-root benchmarks/geometry_full2d_v0_4_4
python scripts/check_review_manifest_v0_4_4.py --corpus-root benchmarks/geometry_full2d_v0_4_4
```

Important: `check_review_manifest_v0_4_4.py` must validate any present reviewed tasks, but absence of reviewed tasks is not a release blocker by itself.

### WP03 — ExternalGoalPreserved corpus import

1. Search formal geometry sources already available or installable in the repo environment: LeanGeo-style files, Newclid/JGEX, GenesisGeo DSL, or other formal geometry corpora.
2. Admit a task as `ExternalGoalPreserved` only if the source has an explicit goal and the translated theorem preserves that goal.
3. Generate `GoalPreservationReportV1` for every admitted task.
4. Mark lossy projections as `ProjectionNonCounted`.
5. Do not use external sources merely as point-name pools.

Allowed preservation kinds:

```text
exact_same_formal_goal
structurally_preserved_by_reviewed_translator
formally_equivalent
```

Acceptance:

```bash
python scripts/check_goal_preservation_reports.py --corpus-root benchmarks/geometry_full2d_v0_4_4
```

### WP04 — UserReviewedGoal import, nonblocking

1. Implement import path for user-reviewed Lean theorem files.
2. Validate `ReviewManifestV1` when such tasks are present.
3. Do not create fake review manifests.
4. Missing user-reviewed tasks must not block release if other corpus floors pass.

Acceptance:

```bash
python scripts/check_review_manifest_v0_4_4.py --corpus-root benchmarks/geometry_full2d_v0_4_4
```

### WP05 — SealedSolverChallenge corpus

1. Implement challenge generator that emits theorem statements only, no proof text and no proof-template labels.
2. Store generator hash, selected implementation hash before seal, and sealed manifest hash.
3. Ensure compilers cannot access generator private labels.
4. Cover incidence, construction, angle, metric, transformation, order, algebraic, inequality, olympiad-style, and hard-holdout families.
5. If code changes after sealing, regenerate or revalidate sealed challenges and rerun acceptance. This is a ReleaseBlocker, not a HardBlocker.

Acceptance:

```bash
python scripts/check_sealed_challenge_manifest.py --corpus-root benchmarks/geometry_full2d_v0_4_4
```

### WP06 — Source theorem hygiene

1. Implement `scripts/check_positive_source_theorems_sorry_only.py`.
2. Reject counted positive theorem bodies containing proof commands before pipeline execution.
3. Reject source theorems that are already proved.
4. Allow external source proofs only as non-counted source evidence, not as counted theorem bodies.

Acceptance:

```bash
python scripts/check_positive_source_theorems_sorry_only.py --corpus-root benchmarks/geometry_full2d_v0_4_4
```

### WP07 — Per-theorem structured extraction

1. Implement Lean elaborator-backed extraction for arbitrary release theorem.
2. Remove smoke-only extraction from release path.
3. Cache extraction by source theorem hash and extraction implementation hash.
4. Validate theorem name, source statement hash, and target classification.
5. Mutation: change theorem target; extraction report and ClaimSpec must change.

Acceptance:

```bash
python scripts/check_full2d_extraction_corpus_v0_4_4.py --corpus-root benchmarks/geometry_full2d_v0_4_4 --run-dir runs/geometry_full2d_v0_4_4
```

### WP08 — ClaimSpec exact-goal enforcement

1. Implement `GeometryFull2DClaimSpecV2`.
2. ClaimSpec is created only from extraction report.
3. Reject ClaimSpec fabricated from manifest labels.
4. Verify exact-goal relation.
5. Add `TargetOutsideReport` for negative/outside tasks.

Acceptance:

```bash
python scripts/check_full2d_claimspec_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
```

### WP09 — Provider and engine real execution

1. Upgrade provider to emit `ProviderRunManifestV2`.
2. Every engine emits `EngineOutputFull2D` with real execution evidence.
3. Engine outputs contain semantic artifacts only, no Lean proof text.
4. Engine outputs do not depend on task_id/template_id/theorem_family.
   They also must not depend on benchmark labels, provenance, source refs, theorem names, or generator-private labels.
5. Engine output changes or fails under relevant ClaimSpec mutation.
6. Implement engine challenge suite.

Minimum independent challenge floors:

```text
synthetic_closure: 50 goals, >=30 normalized_success
construction_search: 50 goals requiring auxiliary objects, >=25 normalized_success
algebraic_geometry: 30 nontrivial certificates, >=15 normalized_success
metric_angle: 40 angle-chase goals, >=20 normalized_success
transformation: 30 genuine transformation invariant goals, >=10 normalized_success
order_case: 30 case/order coverage goals, >=15 normalized_success
inequality: 30 inequality/certificate goals, >=10 normalized_success
lean_proof_search: 50 Lean repair goals, >=25 normalized_success
portfolio_coordinator: all families with correct reason codes
```

Acceptance:

```bash
python scripts/check_full2d_engine_challenge_suite_v0_4_4.py --all-engines
python scripts/check_full2d_engine_real_execution_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/check_full2d_engine_no_proof_text_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
```

### WP10 — Compiler rewrite for solver causality

1. Remove compiler paths that select proof text from target shape alone.
2. Remove compiler access to task_id, theorem_family, grammar_family, template_id, difficulty_tier, provenance, and generator labels for proof decisions.
   Also remove proof-decision access to theorem_name except for patch anchoring, source_ref except for artifact bookkeeping, benchmark labels, and renamed/shimmed old-path labels.
3. Compile from normalized solver artifacts plus RuleRegistry and SideConditionCalculus.
4. Generate `SolverCausalityReportV1`.
5. Run mutation tests for every B2 counted final theorem.
6. Treat direct lemma wrapping as shallow, not substantive.

Acceptance:

```bash
python scripts/check_full2d_compiler_input_isolation_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/check_full2d_compiler_evidence_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/check_solver_causality_reports_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
```

### WP11 — ProofWorker and FinalVerifyGate hardening

1. ProofWorker replaces only MARP proof region.
2. ProofWorker cannot claim final theorem.
3. FinalVerifyGate compiles generated candidate file.
4. FinalVerifyGate rejects changed theorem statement, sorry, axioms, toy semantics, unauthorized imports.
5. FinalVerifyGate binds solver causality report.

Acceptance:

```bash
python scripts/check_full2d_proof_worker_hardening_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/check_full2d_final_verify_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
```

### WP12 — ActualTaskPipelineRunV2

1. Define `ActualTaskPipelineRunV2` schema.
2. Include `solver_causality_report_ref` and content-addressed causal chain.
3. Validate every artifact hash.
4. Reject missing, stale, or mismatched artifact refs.
5. Reject records from old implementation hash.

Acceptance:

```bash
python scripts/check_actual_task_pipeline_runs_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
```

### WP13 — Matrix execution and replay

1. Implement `scripts/run_full2d_matrix_v0_4_4.py`.
2. Release execution mode runs all missing records; no `max_executions=0` release mode.
3. Replay requires corpus hash, config hash, selected implementation hash, repo tree hash, and artifact hashes.
4. Matrix never counts success from sidecar overlay or manifest label.
5. Matrix outputs per-baseline records and summary.
6. B8 is required only when a model provider is enabled; otherwise report `not_applicable_model_provider_not_used`.

Acceptance:

```bash
python scripts/run_full2d_matrix_v0_4_4.py --config configs/benchmark_runs/geometry_full2d_v0_4_4.yaml --run-dir runs/geometry_full2d_v0_4_4 --execute-all
python scripts/check_full2d_matrix_evidence_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4
```

### WP14 — Metrics and advantage

1. Metrics derive from `ActualTaskPipelineRunV2` only.
2. Compute per-family final theorem rates.
3. Compute B2-B1/B5/B6/B7 advantage and conditional B8 if required.
4. Compute substantive success profile.
5. Compute solver-causal success fraction.
6. Reject direct/wrapped facade dominance.

Acceptance:

```bash
python scripts/check_full2d_metrics_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4
```

### WP15 — Used-rule and engine contribution coverage

1. Count only certificate-bound rule ids that appear in solver-causal reports.
2. Count rule families only if used in final theorem and mutation-sensitive.
3. Compute engine contribution by engine output actually consumed by compiler and causality report.
4. Reject inflated rule lists.

Acceptance:

```bash
python scripts/check_full2d_used_rule_coverage_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4
python scripts/check_full2d_engine_contribution_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4
```

### WP16 — Regression failure suite

Implement failing fixtures for:

```text
v0.4.2 overlay matrix
v0.4.3 projection-only corpus
compiler reads template_id
compiler reads task_id
compiler reads theorem_family
compiler reads grammar_family
compiler reads provenance/source_ref/generator-private labels
compiler succeeds without selected engine artifact
compiler succeeds after corrupted solver fact
engine emits proof text
engine output from task_id hash
renamed/shimmed v0.4.3 release path accepted as v0.4.4
stale checker, matrix, corpus, or release output accepted without current hash binding
source theorem pre-proved
smoke extraction reused for corpus
open DebtLedger ignored
fake UserReviewedGoal without review manifest
B8 condition inverted
```

Acceptance:

```bash
python scripts/check_v0_4_4_regression_failures.py
```

### WP17 — Release acceptance

1. Implement `scripts/check_release_acceptance_v0_4_4.py`.
2. It must call all required checkers in Acceptance.
3. It fails on empty summaries.
4. It fails on synthetic or undefined `checked_rids`.
5. It emits a nonempty `freshness_summary`.
6. It emits a nonempty `family_floor_summary` derived from the v0.4.4 corpus checker.
7. It either invokes required checks in the current run or verifies reused outputs by current repository tree or selected implementation hash, corpus hash, config hash, run directory hash, and checker code hash as applicable.
8. It parses DebtLedger.
9. It rejects stale v0.4.2/v0.4.3 reports and stale or hash-unbound v0.4.4 reports.
10. It validates B8 applicability.

Acceptance:

```bash
python scripts/check_release_acceptance_v0_4_4.py --config configs/benchmark_runs/geometry_full2d_v0_4_4.yaml --output docs/ai/changes/geometry-full2d-v0_4_4/evidence/release_acceptance_report.json
```

### WP18 — Closure

Only after release acceptance passes:

1. Create `CLOSURE.md`.
2. Claim only `V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY`.
3. Include non-claims.
4. Include command log, corpus hash, selected implementation hash, and release report hash.

## 3. Work sequencing

Recommended order:

```text
WP00 -> WP01 -> WP02 -> WP06 -> WP07 -> WP08 -> WP09 -> WP10 -> WP11 -> WP12 -> WP03/WP04/WP05 -> WP13 -> WP14 -> WP15 -> WP16 -> WP17 -> WP18
```

Corpus work and engine work may proceed in parallel after WP02.

## 4. Stop policy

Codex stops only for HardBlockers defined in Base Spec. All other blockers become DebtLedger entries and work continues.

## 5. Expected temporary state

For much of implementation, release acceptance should fail. This is normal.

Acceptable interim status:

```text
hard_blockers=[]
release_blockers=[...]
work_debt_open=[...]
next_unblocked_work_packages=[...]
```

Unacceptable interim status:

```text
release acceptance passed by weakening thresholds
release acceptance passed with projection-only corpus
release acceptance passed with compiler template shortcuts
release acceptance blocked solely because user-reviewed tasks are absent
```

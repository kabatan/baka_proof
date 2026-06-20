---
title: "Guardian Plan — GeometryFull2D v0.6 Execution-Locked Full Pipeline Reviewed Strict"
plan_id: "MARP-GEOLEAN-PLAN-012"
base_spec: "MARP-GEOLEAN-BASE-012"
related_acceptance: "MARP-GEOLEAN-ACCEPTANCE-012"
status: "USER_APPROVED_ACTIVE"
revision: "reviewed-strict-2026-06-20"
---

# Guardian Plan — GeometryFull2D v0.6 Execution-Locked Full Pipeline

## Operating rule for Codex

Do not optimize for green release first. Optimize for preventing shortcut implementations. The release checker is expected to fail until all real pipeline stages, red-case rejection, live mutation reruns, and all-baseline matrix execution are implemented.

Codex must not reduce Base Spec thresholds, rename v0.6 to a partial release, create bypass modes, or claim completion with ReleaseBlockers open. When a non-HardBlocker is encountered, record it in DebtLedger and continue with the next unblocked work package.

Implementation discretion is limited to internal code organization, performance engineering, and harmless refactoring. It never permits mocks, synthetic success artifacts, sampled-only release runs, static-only release checks, label-coded outcomes, checker-generated counted artifacts, report-shaped causality, reduced corpus floors, reduced baseline sets, reduced rule-family floors, or replacing an executable stage with a summary field.

## WP00 — Install v0.6 authority and invalidate earlier closures

### Tasks

1. Place all v0.6 authority docs under `docs/ai/changes/geometry-full2d-v0_6/`.
2. Set `docs/ai/ACTIVE_CONTEXT.md` and `docs/ai/INDEX.md` to point to `MARP-GEOLEAN-BASE-012`, `PLAN-012`, `ACCEPTANCE-012`.
3. Mark v0.4.x, prior v0.5, and older closures/release artifacts as historical false-positive/regression evidence only.
4. Implement `scripts/check_active_guardian_spec_v0_6.py`.
5. Implement `scripts/check_v0_6_spec_plan_consistency.py` and make it check claim target, ids, K coverage, required checker names, and no active v0.4/v0.5 release authority.

### Acceptance

```bash
python scripts/check_active_guardian_spec_v0_6.py
python scripts/check_v0_6_spec_plan_consistency.py
```

Both pass. No implementation completion is claimed.

## WP01 — Red-case suite before implementation

### Tasks

1. Create `tests/red_cases/geometry_full2d_v0_6/`.
2. Implement every red case in `RED_CASE_SUITE.md` as an executable fixture.
3. Implement `scripts/check_red_case_suite_v0_6.py --all`.
4. For every red case, the report must include:

```yaml
red_case_id: ...
failure_class: ...
fixture_path: ...
expected_K: ...
observed_failure: true
checker_name: ...
evidence_ref: ...
positive_control_passed: true
```

5. Positive controls must include at least one minimal non-red fixture that the relevant checker accepts.
6. Do not implement provider, compiler, rule registry, matrix, corpus expansion, or release-acceptance code until this report passes.

### Acceptance

```bash
python scripts/check_red_case_suite_v0_6.py --all
```

passes and proves all shortcut classes fail for the intended K requirements.

## WP02 — Acceptance coverage lock

### Tasks

1. Implement `scripts/check_acceptance_coverage_v0_6.py`.
2. Create `docs/ai/changes/geometry-full2d-v0_6/evidence/acceptance_coverage_map.json`.
3. Map every K requirement to:

```yaml
K: ...
checker: ...
red_case_or_dynamic_invariant: ...
evidence_field: ...
release_report_path: ...
```

4. Fail if any K is missing, mapped only to a static comment, or mapped to a checker not invoked by final release acceptance.

### Acceptance

```bash
python scripts/check_acceptance_coverage_v0_6.py
```

passes. `RC_CheckerOmission` and `RC_CheckerWhitelist` fail in red-case suite.

## WP03 — Schema contracts and stage records

### Tasks

Implement typed schemas and validators for:

```text
LeanExtractionReportFull2D
GeometryFull2DClaimSpec
ProviderRunManifestV3
EngineOutputFull2D
IndependentSolverArtifactCheckV1
SelectedSolverDerivationV3
DerivationTargetMatchReportV1
CompilerResultFull2D
LeanPatchCandidateFull2D
ProofWorkerResultFull2D
FinalVerifyReportFull2D
SolverBackedProofCertificateFull2D
ActualTaskPipelineRunV4
SolverCausalityLiveRunV1
StageFailureReportV1
DisabledStageReportV1
```

Validators must check content-addressed refs, required fields, no stale refs, no schema-only fake evidence, and red-case negative fixtures.

### Acceptance

```bash
python scripts/check_schema_contracts_v0_6.py --self-test --red-cases
```

passes.

## WP04 — Lean extraction and ClaimSpec

### Tasks

1. Implement Lean-side structured extraction for each counted theorem.
2. Python may invoke Lean but must not infer theorem semantics by regex.
3. Extraction report must include theorem name, statement hash, elaborated expression hash, canonical target, hypotheses, side-condition obligations, and target classification.
4. Implement ClaimSpec builder from extraction report.
5. Reject smoke-only extraction and stale extraction cache.

### Acceptance

```bash
python scripts/check_full2d_extraction_corpus_v0_6.py --corpus-root benchmarks/geometry_full2d_v0_6 --run-dir <fresh>
python scripts/check_full2d_claimspec_v0_6.py --run-dir <fresh> --self-test
```

passes.

## WP05 — Provider and engine isolation

### Tasks

1. Implement provider process/stage. It may receive ClaimSpec including the goal for directed search, but selected artifacts cannot be naked target assertions.
2. Provider/engine modules must not import compiler, rule registry, proof worker, final verifier, matrix, corpus generator, release checker, previous release modules, or proof templates.
3. Provider outputs must be written before compiler starts. Stage timestamps must prove order.
4. Engine outputs must contain nontrivial facts/constructions/certificates/traces produced from hypotheses/constructions/solver algorithms, not from compiler-selected rules.
5. Implement provider import scanner and dynamic stage-order checker.

### Acceptance

```bash
python scripts/check_provider_isolation_v0_6.py --run-dir <fresh> --red-cases
python scripts/check_engine_output_not_from_compiler_rules_v0_6.py --run-dir <fresh> --red-cases
```

passes.

## WP06 — Independent solver artifact checkers

### Tasks

Implement independent checkers for each selected artifact kind:

```text
synthetic trace checker
construction checker
algebraic/metric certificate checker
order/case checker
inequality checker
Lean search certificate checker
external solver trace normalizer/checker
```

Each selected artifact must have `IndependentSolverArtifactCheckV1(status=passed)`. Checkers must reject naked final target fact, target-as-certificate, proof-text artifacts, missing premises, missing side conditions, and schema-only certificates.

Each independent checker must import neither provider nor compiler code, must not consume downstream proof-generation artifacts, and must verify premises, side conditions, and conclusions from artifact data plus ClaimSpec/hypotheses only.

### Acceptance

```bash
python scripts/check_independent_solver_artifacts_v0_6.py --all --red-cases
```

passes.

## WP07 — Rule registry

### Tasks

1. Implement `RuleRegistryFull2D v0.6` with at least 35 counted semantic rules across 15 families.
2. Each counted rule needs Lean lemma, lemma type hash, independent rule checker, positive fixtures, and negative fixtures.
3. Identity/direct/facade rules may exist only as uncounted helper rules and must be marked `counted_release_rule=false`.
4. Aliases do not count. A rule counts only if used in a B2 final theorem, consumed by compiler, present in certificate, and mutation-sensitive.

### Acceptance

```bash
python scripts/check_rule_registry_v0_6.py --release --red-cases
```

passes and rejects identity-only registries and alias inflation.

## WP08 — Selected solver derivation and target matcher

### Tasks

1. Build `SelectedSolverDerivationV3` only from checked solver artifacts.
2. Every B2 counted success must have at least one selected semantic non-target intermediate or checked construction/certificate/case split. A selected intermediate does not count if it is alpha-renaming-equivalent to the final target, has the final target hash, trivially wraps the target, is reflexivity/symmetry-equivalent to the target, is proved by a direct facade lemma, or normalizes to the target without a checked solver construction, certificate, side-condition discharge, or case split.
3. Implement `DerivationTargetMatcher` as a separate stage. It may compare final derivation step hash to target hash but must not output proof text, tactics, target expressions, rule choices, or strategy labels.
4. `DerivationTargetMatcher` is a release-orchestration gate before compiler invocation. The compiler API remains exactly DR-012-004 and does not receive a target-match report, raw target expression, target expression string, proof tactic, rule choice, or strategy label as an input.

### Acceptance

```bash
python scripts/check_selected_derivation_v0_6.py --run-dir <fresh> --red-cases
python scripts/check_derivation_target_matcher_v0_6.py --run-dir <fresh> --red-cases
```

passes.

## WP09 — Compiler input lock

### Tasks

1. Compiler API must match Base Spec DR-012-004 exactly.
2. Compiler cannot import corpus, matrix, benchmark metadata, provider internals, release checker, or prior release code.
3. Compiler cannot read raw target expression. Release orchestration may invoke the compiler only after `DerivationTargetMatcher` has passed target-hash equivalence, but the target-match report is not a `compile_derivation` input.
4. Implement taint tests: poison theorem_family, target_shape_id, task_id, raw target expression, source_ref, category, difficulty tier, theorem name, statement hash, proof-region identity, binder-map identity, and every other `TheoremAnchorV1` identifier field. If compiler proof text or rule plan changes for any forbidden field, release fails. Anchor fields may locate and patch the theorem region only; they must not choose proof strategy, rule selection, lemma selection, or derivation-step ordering.
5. Compiler emits Lean patch by translating selected derivation steps and rule contracts only.

### Acceptance

```bash
python scripts/check_compiler_input_lock_v0_6.py --self-test --red-cases --dynamic-taint
```

passes.

## WP10 — ProofWorker and FinalVerifyGate

### Tasks

1. ProofWorker applies patch only inside MARP region.
2. It must not claim final theorem.
3. FinalVerifyGate runs `lake env lean` or equivalent on generated candidate from scratch.
4. FinalVerifyGate rejects sorry, admit, axiom, unsafe target semantics, protected theorem mutation, imported toy targets, and stale candidate hashes.
5. Certificate binds all upstream artifacts and final verify report.

### Acceptance

```bash
python scripts/check_proof_worker_final_verify_v0_6.py --self-test --red-cases
```

passes.

## WP11 — Live destructive causality runner

### Tasks

Implement `scripts/run_solver_causality_live_v0_6.py`.

For every B2 counted final theorem success:

1. Create isolated temp run dir.
2. Reconstruct original selected artifacts from content-addressed refs.
3. Run positive control through compiler, proof worker, final verifier.
4. Mutate artifact cases:
   - remove selected artifact;
   - corrupt non-target intermediate;
   - corrupt construction/certificate;
   - unsupported rule mutation;
   - side condition mutation;
   - remove checker transcript.
5. Re-run compiler, proof worker, final verifier for each mutation.
6. Store command logs, input/output hashes, patch hashes, final verify reports.
7. Fail if any mutation produces the same counted final theorem.

### Acceptance

```bash
python scripts/run_solver_causality_live_v0_6.py --run-dir <fresh> --all-b2-successes
python scripts/check_solver_causality_live_v0_6.py --run-dir <fresh> --red-cases
```

passes. Field-only causality fixture fails.

## WP12 — Corpus and sealed adversarial holdout

### Tasks

1. Implement external source discovery. Do not make source unavailability a HardBlocker; generate `ExternalSourceAvailabilityReportV2`.
2. Implement `ExternalGoalPreserved` importer with machine-checkable goal mapping only.
3. Freeze implementation hash before counted sealed holdout generation.
4. Generate `SealedAdversarialHoldout` after implementation freeze with a generator that imports no provider, compiler, rule registry, proof worker, final verifier, matrix, previous release code, run records, or proof lemmas.
5. Generator receives release seed from final acceptance pre-run and emits theorem statements only, no proof text, expected rule ids, expected engine roles, target_shape ids, or proof labels.
6. If external sources are unavailable, record `ExternalSourceAvailabilityReportV2`, reduce only the ExternalGoalPreserved subfloor affected by availability, replace the missing counted positives with sealed adversarial holdout tasks, and keep every total corpus/diversity floor from Base Spec.

### Acceptance

```bash
python scripts/check_corpus_independence_v0_6.py --corpus-root benchmarks/geometry_full2d_v0_6 --red-cases
python scripts/check_statement_diversity_v0_6.py --corpus-root benchmarks/geometry_full2d_v0_6
```

passes.

## WP13 — All-baseline matrix

### Tasks

1. Implement `run_full2d_matrix_v0_6.py`.
2. In closure mode, it must execute all counted tasks for B1, B2, B5, B6, B7, and B8 if enabled.
3. It must materialize `ActualTaskPipelineRunV4` for each task/baseline.
4. It must not compute outcomes from labels.
5. Disabled baselines must remove actual artifacts or stages, producing `StageFailureReportV1` / `DisabledStageReportV1` when appropriate.
6. It must fail if any required record is missing, stale, or generated without FinalVerifyGate or measured-stage failure.

### Acceptance

```bash
python scripts/run_full2d_matrix_v0_6.py --config configs/benchmark_runs/geometry_full2d_v0_6.yaml --run-dir <fresh> --execute-all --all-baselines --no-skip
python scripts/check_all_baseline_matrix_v0_6.py --run-dir <fresh> --red-cases
```

passes. B2-only matrix red case fails.

## WP14 — Metrics and advantage

### Tasks

Compute metrics only from actual records and live causality reports:

```text
final theorem rates
solver-causal success fraction
mutation pass fraction
non-target intermediate fraction
construction/case/certificate fraction
direct/facade lemma fraction
used rule family coverage
engine contribution
baseline advantages
measured failure summary
```

Used-rule coverage and engine contribution are not optional subfields of a broad metrics report. They must be checked by dedicated release checkers. A measured unavailability or debt report can explain a release failure, but it cannot satisfy a final release metric for an enabled release-critical engine role or counted rule-family threshold.

`check_engine_contribution_v0_6.py` must enforce the exact `ReleaseCriticalEngineRoleV1` set, enabled/disabled rules, and corpus-subset mapping from Base Spec DR-012-015. The enabled role set must be derived from corpus metadata and config before provider execution, not after observing provider success or failure.

### Acceptance

```bash
python scripts/check_full2d_metrics_v0_6.py --run-dir <fresh> --thresholds-from docs/ai/changes/geometry-full2d-v0_6/BASE_SPEC.md
python scripts/check_used_rule_coverage_v0_6.py --run-dir <fresh> --red-cases
python scripts/check_engine_contribution_v0_6.py --run-dir <fresh> --red-cases
```

passes thresholds from Base Spec.

## WP15 — Release checker and closure ceiling

### Tasks

1. Implement `check_release_acceptance_v0_6.py`.
2. It must create a fresh run directory in closure mode.
3. It must invoke every required checker from Acceptance.
4. It must include `K -> checker -> result -> evidence_ref` mapping.
5. It must fail if any checker detects a forbidden shortcut in release entrypoints.
6. It must generate closure only if release passes.
7. It must fail if any required checker is omitted or any required report field is empty.

### Acceptance

```bash
python scripts/check_release_acceptance_v0_6.py --config configs/benchmark_runs/geometry_full2d_v0_6.yaml --fresh-run --fail-on-stale --no-skip --all-baselines --live-mutations --output docs/ai/changes/geometry-full2d-v0_6/evidence/release_acceptance_report.json
python scripts/check_closure_claim_ceiling_v0_6.py
```

passes only if all requirements pass.

## WP16 — Final fresh release run

### Tasks

Run final command:

```bash
python scripts/check_release_acceptance_v0_6.py   --config configs/benchmark_runs/geometry_full2d_v0_6.yaml   --fresh-run   --fail-on-stale   --no-skip   --all-baselines   --live-mutations   --output docs/ai/changes/geometry-full2d-v0_6/evidence/release_acceptance_report.json
```

Then run:

```bash
python scripts/check_closure_claim_ceiling_v0_6.py
```

### Acceptance

Release report contains:

```text
status=passed
closure_allowed=true
hard_blockers=[]
release_blockers=[]
work_debt_open=[]
claim_ceiling=V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
```

No manual closure is allowed.


Plan flag requirement: `--fail-on-stale` must be used by final release acceptance.


Plan flag requirement: `--live-mutations` must be used by final release acceptance.

---
title: "Guardian Plan — Geometry × Lean Full2D Real Pipeline Recovery v0.4.3 Integrated"
plan_id: "MARP-GEOLEAN-PLAN-008"
status: "USER_APPROVED_ACTIVE"
base_spec: "MARP-GEOLEAN-BASE-008"
created: "2026-06-15"
---

# Guardian Plan — Geometry × Lean Full2D Real Pipeline Recovery v0.4.3

## 0. Execution rule for Codex

Codex must implement this plan literally. If a step cannot be completed, Codex records ReleaseBlocker or WorkDebt and proceeds to unrelated steps. Codex may stop only for HardBlockers listed in the Base Spec.

Do not lower thresholds. Do not relabel synthetic work as curated. Do not reuse the v0.4.2 template proof artifact path as release evidence. The anti-gaming hardening requirements are part of this plan itself; there is no separate patch or addendum to install.

## WP-00 — Install authority and freeze old claims

### Tasks

1. Create `docs/ai/changes/geometry-full2d-v0_4_3/`.
2. Install approved files after user approval:
   - `BASE_SPEC.md`
   - `PLAN.md`
   - `ACCEPTANCE.md`
   - `REAL_PIPELINE_INVARIANTS.md`
   - `REFACTOR_DIRECTIVE.md`
   - `SOURCE_MAP.md`
   - `ACTIVE_CONTEXT.md`
   - `CODEX_HANDOFF.md`
3. Mark v0.4.2 as superseded for release claims. Keep it only as evidence and regression source.
4. Add `docs/ai/changes/geometry-full2d-v0_4_3/debt/debt_ledger.jsonl`.
5. Add `scripts/check_active_guardian_spec_v0_4_3.py`.

### Acceptance

```bash
python scripts/check_active_guardian_spec_v0_4_3.py
```

Pass criteria:

```text
active spec = MARP-GEOLEAN-BASE-008
old specs are not active
no v0.4.2 closure claim is treated as v0.4.3 release evidence
```

## WP-01 — Refactor old v0.4.2 release path out of release commands

### Tasks

1. Archive or rewrite the following as non-release utilities:
   - `scripts/build_full2d_proof_artifact_batch.py`
   - `scripts/run_full2d_matrix.py`
   - `scripts/check_full2d_metrics.py`
   - `scripts/check_release_acceptance_v0_4_2.py`
2. Add release-path guards that fail if:
   - proof patch is chosen from `template_id`;
   - normalized solver ref is generated from `task_id`;
   - matrix applies sidecar overlay without replay-valid `ActualTaskPipelineRunV1`;
   - release report summaries are empty.
3. Add `scripts/check_no_v042_template_release_path.py`.

### Acceptance

```bash
python scripts/check_no_v042_template_release_path.py
```

Pass criteria:

```text
No v0.4.3 release command imports or calls the template artifact batch path.
No release script contains direct mapping from template_id/theorem_family to proof replacement text.
No release script fabricates solver refs from task_id/theorem_name/template_id.
```

## WP-02 — ActualTaskPipelineRunV1 schema and verifier

### Tasks

1. Add JSON schema: `schemas/geometry_full2d/actual_task_pipeline_run_v1.schema.json`.
2. Implement `plugins/geometry_full2d/run_records.py` with dataclasses and validators.
3. Implement `scripts/check_actual_task_pipeline_runs.py`.
4. Checker must verify:
   - every referenced artifact exists;
   - every sha256 ref matches file contents or content-addressed payload;
   - source theorem path/hash matches extraction report;
   - provider manifest exists and matches task request;
   - compiler consumed provider engine output;
   - proof worker consumed compiler patch;
   - FinalVerifyGate checked generated candidate;
   - certificate binds all previous refs.

### Acceptance

```bash
python scripts/check_actual_task_pipeline_runs.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
```

Self-test must include negative cases for missing provider manifest, fabricated solver ref, missing extraction report, and source theorem already proved.

## WP-03 — Per-theorem structured Lean extraction

### Tasks

1. Replace smoke-only extraction with a command:

```bash
python scripts/extract_geometry_full2d_theorem.py --lean-file <path> --theorem-name <name> --output <json>
```

2. The command must invoke `lake env lean` or a Lean elaborator-backed command for that exact theorem.
3. Add Lean code or executable support to inspect the theorem declaration and emit structured JSON.
4. If complete elaborator inspection is not possible for all grammar forms, unsupported extraction becomes measured failure, not success.
5. Add `scripts/check_full2d_extraction_corpus.py` to run extraction for all counted positive successes and all negative tasks.

### Acceptance

```bash
python scripts/check_full2d_extraction_corpus.py \
  --corpus-root benchmarks/geometry_full2d \
  --run-dir runs/geometry_full2d_v0_4_3
```

Pass criteria:

```text
Each counted positive success has LeanExtractionReportFull2D.
No counted positive uses fixed smokeStatement JSON.
The theorem_name and source_statement_hash match source theorem.
regex_used_for_semantics=false for every counted success.
```

## WP-04 — ClaimSpec construction and exact-goal classification

### Tasks

1. Implement `GeometryFull2DClaimSpec` from `LeanExtractionReportFull2D`.
2. Include nondegeneracy, orientation, existence, uniqueness, and order cases.
3. ClaimSpec must include target classification and exact-goal relation.
4. Implement `scripts/check_full2d_claimspec_v0_4_3.py`.

### Acceptance

```bash
python scripts/check_full2d_claimspec_v0_4_3.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
```

Must reject missing side conditions, non-exact relation, and synthetic Python classification.

## WP-05 — Real provider execution

### Tasks

1. Implement `GeometryFull2DProvider.solve` as the sole release provider.
2. It must run per task. It cannot be bypassed by proof artifact generation.
3. It must write `ProviderRunManifestFull2D` to ArtifactStore.
4. Engine outputs must be content-addressed artifacts.
5. Implement `scripts/check_full2d_provider_real_execution.py`.

### Acceptance

```bash
python scripts/check_full2d_provider_real_execution.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
```

Pass criteria:

```text
Each counted success has provider_run_manifest_ref from actual provider.solve.
No normalized_solver_artifact_ref is generated from task_id/template_id.
Each engine output has real_integration_evidence_ref.
At least one counted success references each release-critical engine role through certificate-bound engine output.
```

## WP-06 — Engine implementations with challenge suites

### Tasks

For each engine:

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

implement:

1. Actual engine run code over ClaimSpec.
2. Engine-specific challenge suite under `tests/fixtures/geometry_full2d/engine_challenges/<role>.jsonl`.
3. Real integration evidence generator.
4. Negative tests proving the engine does not depend on task_id/theorem_name/template_id.

### Acceptance

```bash
python scripts/check_full2d_engine_challenge_suite.py --all-engines
```

Pass criteria:

```text
Each engine passes challenge suite.
Each engine fails altered-input mutation tests when output should change.
No engine source contains release benchmark theorem names.
No engine source branches on template_id.
```

## WP-07 — RuleRegistryFull2D used-rule coverage

### Tasks

1. Keep at least 150 rules / 25 families / 30 construction templates.
2. Add `UsedRuleCoverageReportFull2D` from certificates, not from registry definition.
3. Count a rule only if final theorem certificate references it through compiler result.
4. Implement `scripts/check_full2d_used_rule_coverage.py`.

### Acceptance

```bash
python scripts/check_full2d_used_rule_coverage.py --run-dir runs/geometry_full2d_v0_4_3
```

Required actual used coverage:

```text
>= 35 distinct concrete rules
>= 15 distinct rule families
>= 8 families outside incidence/collinearity
>= 5 families requiring nontrivial side-condition discharge
>= 4 families involving construction introduction
>= 3 families involving algebraic/metric/angle reasoning
>= 2 families involving order/case reasoning
>= 2 families involving transformations
```

## WP-08 — Compiler pipeline from actual engine outputs

### Tasks

1. Implement compilers for all engine artifact types.
2. Compiler input must be engine output artifact refs, not benchmark labels.
3. Compiler result must include consumed engine output refs and consumed rule ids.
4. Add `scripts/check_full2d_compiler_evidence.py`.

### Acceptance

```bash
python scripts/check_full2d_compiler_evidence.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
```

Must reject compiler result with no consumed engine output, no rule ids, or benchmark-template-derived patch.

## WP-09 — ProofWorker patch application hardening

### Tasks

1. Ensure ProofWorker edits only MARP proof region.
2. Reject source theorem if it does not contain `sorry` in proof region for solver-backed benchmark mode.
3. Reject generated candidate if it contains `sorry`, `axiom`, `admit`, unsafe target semantics, or edits outside region.
4. Add `scripts/check_full2d_proof_worker_hardening.py`.

### Acceptance

```bash
python scripts/check_full2d_proof_worker_hardening.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
```

## WP-10 — FinalVerifyGate and certificate binding

### Tasks

1. `FinalVerifyGate` must compile generated candidate file.
2. FinalVerify report must include checked candidate file hash.
3. Certificate checker must bind extraction, claimspec, provider, engine outputs, compiler results, patch, worker, final verify.
4. Implement `scripts/check_full2d_certificate_binding.py`.

### Acceptance

```bash
python scripts/check_full2d_certificate_binding.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
```

Must reject modified candidate, mismatched provider manifest, fabricated engine ref, and raw solver output proof-use.

## WP-11 — Honest corpus rebuild

### Tasks

1. Remove or relabel Codex-generated `human_curated_formal` tasks as `synthetic_generated`.
2. Implement `CuratedReviewManifestV1`.
3. To count as `user_reviewed_human_curated`, each task must include:
   - reviewer id or user approval ref;
   - source_ref;
   - theorem statement hash;
   - no synthetic relabeling marker;
   - optional source-fidelity status.
4. External formal tasks must include external source and license/provenance ref.
5. Regenerate and freeze corpus only after provenance checks pass.

### Acceptance

```bash
python scripts/check_full2d_corpus_manifest_v0_4_3.py --corpus-root benchmarks/geometry_full2d
```

Must fail if Codex-created local template tasks are counted as curated without review manifest.

## WP-12 — Matrix execution / replay rewrite

### Tasks

1. Implement `scripts/run_full2d_matrix_v0_4_3.py`.
2. For each task/baseline, it must either execute pipeline or replay valid ActualTaskPipelineRunV1.
3. Baselines must be comparable and cannot disable final verification to create advantage.
4. Matrix summary must be derived from task run records.
5. Implement `scripts/check_full2d_matrix_evidence.py`.

### Acceptance

```bash
python scripts/run_full2d_matrix_v0_4_3.py --config configs/benchmark_runs/geometry_full2d_v0_4_3.yaml --run-dir runs/geometry_full2d_v0_4_3
python scripts/check_full2d_matrix_evidence.py --run-dir runs/geometry_full2d_v0_4_3
```

## WP-13 — Metrics, advantage, measured failures

### Tasks

1. Implement metrics from ActualTaskPipelineRunV1 only.
2. Compute family thresholds, overall threshold, and safe-reject count.
3. Compute advantage B2-B1, B2-B5, B2-B6, B2-B7, B2-B8 from executed baseline records.
4. Store measured failure reasons.
5. Implement `scripts/check_full2d_metrics_v0_4_3.py`.

### Acceptance

```bash
python scripts/check_full2d_metrics_v0_4_3.py --run-dir runs/geometry_full2d_v0_4_3
```

Pass criteria: all thresholds from Base Spec pass from actual run records.


## WP-14 — Substantive corpus profile

### Tasks

1. Add `SubstantiveTaskProfileV1` to every positive corpus record.
2. Implement `scripts/check_full2d_substantive_corpus.py`.
3. The checker must compute floors for reasoning depth, construction, side-condition discharge, order/case reasoning, metric/algebraic/inequality reasoning, transformation reasoning, olympiad-style depth, and hard-holdout uniqueness.
4. The checker must classify repeated-point collinearity, reflexivity-only, structure-evidence-only, and direct facade lemma tasks as `required_reasoning_depth <= 1` unless a valid review manifest explicitly overrides.
5. The checker must compute direct-lemma fraction and fail if it exceeds 0.20.

### Acceptance

```bash
python scripts/check_full2d_substantive_corpus.py --corpus-root benchmarks/geometry_full2d
```

## WP-15 — ReviewManifestV1 gate

### Tasks

1. Add `schemas/geometry_full2d/review_manifest_v1.schema.json`.
2. Implement `scripts/check_full2d_review_manifest.py`.
3. Reject Codex-generated records counted as `user_reviewed_human_curated` unless an explicit user/reviewer/external-source manifest exists.
4. Verify that `review_hash` is content-addressed and that the manifest lists the admitted task ids.
5. Ensure tasks with provenance note indicating Codex-created local facade tasks are counted as `synthetic_generated`, not curated.

### Acceptance

```bash
python scripts/check_full2d_review_manifest.py --corpus-root benchmarks/geometry_full2d
```

## WP-16 — Engine semantic-output guard

### Tasks

1. Add runtime validation that `EngineOutputFull2D` cannot contain Lean proof text, tactic scripts, proof-region replacement text, exact lemma application text, or benchmark dispatch fields.
2. Add static scanner `scripts/check_full2d_engine_no_proof_text.py`.
3. Add mutation tests where engine output includes a fake proof patch and confirm the release checker rejects it.

### Acceptance

```bash
python scripts/check_full2d_engine_no_proof_text.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
```

## WP-17 — Compiler input isolation

### Tasks

1. Refactor compiler interfaces so they receive only ClaimSpec, engine artifacts, RuleRegistry, side-condition calculus, and target hash/edit region.
2. Add `scripts/check_full2d_compiler_input_isolation.py`.
3. Negative tests must fail if compiler reads `template_id`, `theorem_family`, `difficulty_tier`, provenance, or task labels to choose proof text.

### Acceptance

```bash
python scripts/check_full2d_compiler_input_isolation.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
```

## WP-18 — Baseline comparability verifier

### Tasks

1. Add `BaselineComparabilityReportV1` to every matrix run.
2. Implement `scripts/check_full2d_baseline_comparability.py`.
3. Ensure B1/B5/B6/B7/B8 differ only by the intended disabled component.
4. Ensure B1 final verification, ProofWorker, source theorem visibility, Lean library access, and resource class are not weakened.
5. Ensure B1 successes are counted when no geometry solver is needed.

### Acceptance

```bash
python scripts/check_full2d_baseline_comparability.py --run-dir runs/geometry_full2d_v0_4_3
```

## WP-19 — Causal chain hash

### Tasks

1. Extend `ActualTaskPipelineRunV1` with `causal_chain_hash`.
2. Implement recomputation in `scripts/check_actual_task_pipeline_runs.py`.
3. Add negative controls for reordered, missing, fabricated, or substituted artifacts.

### Acceptance

```bash
python scripts/check_actual_task_pipeline_runs.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
```

## WP-20 — Anti-v0.4.2 regression fixture

### Tasks

1. Add fixture directory `tests/fixtures/geometry_full2d/anti_v042_template_overlay/`.
2. Reproduce the old bad path with template-id-to-proof and fabricated solver refs.
3. Implement `scripts/check_anti_v042_regression.py` that verifies the v0.4.3 release checker rejects this fixture.
4. Record rejection reason under `anti_v042_regression_status=passed`.

### Acceptance

```bash
python scripts/check_anti_v042_regression.py
```

## WP-21 — Integrated final release acceptance

### Tasks

1. Implement `scripts/check_release_acceptance_v0_4_3.py`.
2. It must parse debt ledger and fail on any open entry.
3. It must run or verify every checker WP-00..WP-20.
4. It must populate non-empty:
   - `checked_rids`
   - `metrics_summary`
   - `advantage_summary`
   - `used_rule_coverage_summary`
   - `engine_usage_summary`
   - `measured_failure_summary`
   - `corpus_summary`
   - `actual_pipeline_run_summary`
   - `substantive_corpus_summary`
   - `review_manifest_summary`
   - `baseline_comparability_summary`
   - `causal_chain_summary`
   - `anti_v042_regression_status`
   - `engine_semantic_output_summary`
   - `compiler_input_isolation_summary`
5. It must enforce blockers K-001..K-024.
6. Empty or missing summaries are release blockers.

### Acceptance

```bash
python scripts/check_release_acceptance_v0_4_3.py --config configs/benchmark_runs/geometry_full2d_v0_4_3.yaml --output docs/ai/changes/geometry-full2d_v0_4_3/evidence/release_acceptance_report.json
```

## WP-22 — Closure review

### Tasks

1. Create `CLOSURE.md` only after release acceptance passes.
2. Closure must claim only `V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY` if evidence supports it.
3. Closure must list all non-claims: natural-language source fidelity, open problem solving, TongGeometry model-backed readiness, production safety.
4. Implement `scripts/check_closure_v0_4_3.py`.

### Acceptance

```bash
python scripts/check_closure_v0_4_3.py
```

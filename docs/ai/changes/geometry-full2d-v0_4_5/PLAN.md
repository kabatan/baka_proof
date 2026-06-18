---
title: "Guardian Plan — GeometryFull2D v0.4.5 Real Solver-Causal Full Pipeline"
plan_id: "MARP-GEOLEAN-PLAN-010"
base_spec: "MARP-GEOLEAN-BASE-010"
status: "USER_APPROVED_ACTIVE"
revision: "reviewed-2026-06-18-no-shortcuts"
---

Claim target: `V0.4.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY`

# Guardian Plan — GeometryFull2D v0.4.5

## 0. Operating rules for Codex

Codex must treat `MARP-GEOLEAN-BASE-010`, `PLAN-010`, and `ACCEPTANCE-010` as the only v0.4.5 authority.

Do not ask to weaken scope. Do not create a partial completion claim. Do not claim release because intermediate plumbing works. Do not stop on ReleaseBlockers; record them and continue the next unblocked work package. Stop only on HardBlockers.

## WP-00 — Authority install and old-spec quarantine

### Tasks

1. Place v0.4.5 docs under:

```text
docs/ai/changes/geometry-full2d-v0_4_5/
```

2. Mark v0.4.4 docs and closure as superseded, not deleted.
3. Create `scripts/check_active_guardian_spec_v0_4_5.py`.
4. Create `docs/ai/changes/geometry-full2d-v0_4_5/debt/debt_ledger.jsonl`.
5. Register `scripts/check_release_path_forbidden_shortcuts_v0_4_5.py` as a required release-path checker in Plan and Acceptance. The checker is implemented in WP-01; WP-00 must not require run artifacts that cannot exist before implementation work starts.

### Acceptance

```bash
python scripts/check_active_guardian_spec_v0_4_5.py
python scripts/check_v0_4_5_spec_plan_consistency.py
```

Must report only `MARP-GEOLEAN-BASE-010` active.

## WP-01 — Current shortcut audit and quarantine

### Purpose

Before implementing, identify and quarantine all current shortcut paths.

### Must flag as release-forbidden

```text
scripts/generate_full2d_v0_4_4_corpus.py
scripts/run_full2d_actual_task_v0_4_4.py
scripts/check_solver_causality_reports_v0_4_4.py
any _proof_from_shape
any _proof_from_source
any target_expr.startswith(...) -> exact lemma menu
any _baseline_allows_success or family-coded baseline branch
any causality report that only sets booleans
any generated external goal report created by the same corpus generator without independent checker evidence
```

### Output

```text
docs/ai/changes/geometry-full2d-v0_4_5/evidence/shortcut_audit.md
```

### Acceptance

```bash
python scripts/check_release_path_forbidden_shortcuts_v0_4_5.py --static-only
```

The static mode must fail on copied v0.4.4 shortcut fixtures and pass only when the new release entrypoints do not import or call known shortcut paths. It must inspect source files, imports, direct call targets, and forbidden implementation signatures.

The full mode is a final-release gate in WP-13:

```bash
python scripts/check_release_path_forbidden_shortcuts_v0_4_5.py \
  --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml \
  --run-dir runs/geometry_full2d_v0_4_5
```

Full mode must additionally inspect actual release run artifacts. WP-01 must not block on dynamic run evidence that cannot exist yet.

## WP-02 — Corpus v0.4.5

### 2.1 Corpus directories

```text
benchmarks/geometry_full2d_v0_4_5/
  corpus_manifest.json
  lean/
  metadata/
  external_sources/
  sealed_challenges/
  regression_fixtures/
  metadata/external_source_registry.json
```

### 2.2 Corpus categories

Counted positive categories:

```text
ExternalGoalPreserved
SealedPostImplementationChallenge
UserReviewedGoal
```

Non-counted categories:

```text
ProjectionNonCounted
ProjectionDerivedSmoke
CompilerRegressionFixture
TargetOutside
Malformed
```

### 2.3 ExternalGoalPreserved importer

Implement:

```bash
python scripts/import_external_goal_preserved_v0_4_5.py \
  --source-root <external source> \
  --output-root benchmarks/geometry_full2d_v0_4_5
```

Rules:

- importer parses the external source goal into `SourceGoalASTV1`;
- translator creates Lean theorem target `TranslatedGoalASTV1`;
- independent checker, not the importer itself, produces `GoalPreservationReportV2`;
- report must prove exact, formal equivalence, or machine-checked structure-preserving translation;
- projection or easier derived goal must be category `ProjectionNonCounted`;
- if external sources are unavailable/insufficient, create `ExternalSourceAvailabilityReportV1` and fill the deficit with additional sealed challenges.
- availability must be checked by an independent checker against `metadata/external_source_registry.json`; the importer cannot self-declare sources unavailable;
- a local or fetched source goal that exists must either become an admitted `ExternalGoalPreserved` task or receive a concrete `GoalPreservationReportV2` rejection reason.

The importer must not write proof text, expected proof lemma, expected engine role, expected rule ids, or expected baseline outcome.

### 2.4 Sealed challenge grammar and generator

Implement:

```bash
python scripts/generate_sealed_challenges_v0_4_5.py \
  --after-implementation-freeze \
  --grammar benchmarks/geometry_full2d_v0_4_5/metadata/sealed_challenge_grammar.json \
  --output-root benchmarks/geometry_full2d_v0_4_5
```

Rules:

- WP-02 implements the grammar, generator, and static independence checks only;
- WP-02 must not generate counted release sealed challenges because provider/compiler/rule-registry code is not frozen yet;
- generator imports no provider/compiler/rule_registry/proof_worker/matrix/release-checker code;
- generated Lean files contain theorem statements and sorry-only proof regions;
- generator writes no expected proof lemma, proof template, engine role, rule id, solver fact, proof hint, or baseline outcome;
- manifest includes frozen provider/compiler/rule registry selected implementation hash;
- if implementation files change after sealing, release fails until the challenge is regenerated and revalidated.

### Acceptance

```bash
python scripts/check_full2d_corpus_manifest_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_goal_preservation_reports_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_external_source_availability_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_sealed_challenge_generator_independence_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5 --static-only
python scripts/check_counted_sources_sorry_only_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_corpus_no_proof_coupling_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5
```

The final sealed challenge manifest is checked in WP-07A after implementation freeze.

## WP-03 — Lean extraction v0.4.5

### Tasks

Implement per-theorem Lean-side extraction:

```bash
python scripts/extract_full2d_theorem_v0_4_5.py \
  --lean-file <file> \
  --theorem-name <name> \
  --output <json>
```

Required properties:

- Lean elaborator-backed or Lean command-backed.
- No Python semantic classification.
- Regex only for locating theorem text, not semantics.
- Source theorem hash must match manifest hash.
- Target classification must be derived from the extracted expression, not manifest metadata.

### Acceptance

```bash
python scripts/check_full2d_extraction_corpus_v0_4_5.py \
  --corpus-root benchmarks/geometry_full2d_v0_4_5 \
  --run-dir runs/geometry_full2d_v0_4_5
```

Must run on 100% of counted positives and all negative/safe-reject tasks.

## WP-04 — ClaimSpec v0.4.5

Implement:

```python
build_claim_spec_v0_4_5(LeanExtractionReportFull2D) -> ClaimSpecResult
```

Rules:

- in-target positive only if exact goal;
- no unsupported construct losses;
- no dropped hypotheses;
- nondegeneracy/orientation/order/case obligations preserved;
- target-outside and malformed cannot count as positive success.

Acceptance:

```bash
python scripts/check_full2d_claimspec_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
```

## WP-05 — Real provider and engines

### Required engines

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

### Engine implementation rule

Each engine must produce `EngineOutputFull2D` before compiler proof text exists.

Engine normalized output must include solver facts, constructions, or certificates:

```yaml
facts:
  - fact_id
    predicate_family
    args
    conclusion
    premises
    rule_id
    side_conditions
    certificate_ref
```

The output must not include Lean proof text or theorem-specific proof replacement. It must not include `task_id`, `theorem_name`, `template_id`, `theorem_family`, `target_shape_id`, or expected proof labels except as opaque artifact metadata not consumed by the compiler.

### Real integration evidence

For each output, include one of:

```text
external_backend_run
internal_algorithm_run
lean_verified_run
```

A real integration evidence artifact must include command or algorithm identity, input hash, output hash, code hash, resource usage, replay status, and a non-template challenge transcript for that engine. Each normalized fact/construction/certificate must have independent checker evidence; unchecked target assertions are invalid. Provider/engine modules must not import release compiler or proof-generation modules.

### Acceptance

```bash
python scripts/check_full2d_engine_real_execution_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/check_full2d_engine_no_proof_text_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/check_full2d_engine_challenge_suite_v0_4_5.py --all-engines
python scripts/check_engine_output_not_from_compiler_rules_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5
python scripts/check_solver_fact_independent_checkers_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
```

## WP-06 — RuleRegistry and side-condition calculus

Implement `RuleRegistryFull2D` with concrete rule contracts.

Each rule must specify:

```yaml
rule_id
input fact patterns
output fact pattern
side conditions required
generated obligations
Lean lemma/template id
unsupported variants
positive/negative/mutation fixtures
```

A rule counts only if:

```text
- appears in a solver artifact,
- is selected into SelectedSolverDerivationV1,
- is consumed by a compiler result,
- appears in SolverBackedProofCertificateFull2D,
- passes destructive causality mutation,
- final theorem succeeds.
```

Acceptance:

```bash
python scripts/check_full2d_rule_registry_v0_4_5.py
python scripts/check_full2d_used_rule_coverage_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5
```

## WP-07 — Compiler v0.4.5

### Core rule

The compiler may generate proof text only from `SelectedSolverDerivationV1`, consumed solver facts/constructions/certificates, and RuleRegistry templates.

Forbidden:

```python
if target_expr.startswith(...): return "exact ..."
if theorem_family == ...: return ...
if baseline == "B2": ...
proof_text = lookup_by_target_shape(...)
```

Allowed:

```python
for solver_step in selected_solver_derivation.solver_steps:
    rule = RuleRegistry.lookup(solver_step.rule_id)
    instantiate Lean template using solver_step.conclusion / premises / side conditions
```

### Taint checker

Implement `scripts/check_compiler_taint_v0_4_5.py`.

It must fail if release compiler proof decisions depend on:

```text
task_id
template_id
theorem_family
grammar_family
difficulty_tier
category
provenance
source_ref
target_shape_id
raw target expression without solver fact matching
```

### Acceptance

```bash
python scripts/check_full2d_compiler_input_isolation_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/check_compiler_taint_v0_4_5.py
python scripts/check_full2d_compiler_evidence_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/check_selected_solver_derivation_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
```

## WP-07A — Implementation freeze and sealed challenge finalization

### Purpose

Generate counted `SealedPostImplementationChallenge` tasks only after the provider, engine, compiler, and rule-registry release code is frozen.

### Tasks

1. Compute a selected implementation hash over provider, engine, rule registry, compiler, proof worker, matrix, release checker, and checker code that can affect release behavior.
2. Run the sealed challenge generator with `--after-implementation-freeze`.
3. Write a sealed challenge manifest binding every counted sealed challenge to the selected implementation hash and grammar hash.
4. Re-run corpus, sorry-only, no-proof-coupling, extraction, and ClaimSpec checks over the final corpus.
5. Record any post-seal implementation code change as a ReleaseBlocker until challenges are regenerated and revalidated.

### Acceptance

```bash
python scripts/freeze_full2d_v0_4_5_implementation.py --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml
python scripts/generate_sealed_challenges_v0_4_5.py --after-implementation-freeze --grammar benchmarks/geometry_full2d_v0_4_5/metadata/sealed_challenge_grammar.json --output-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_full2d_implementation_freeze_v0_4_5.py --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml --corpus-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_sealed_challenge_manifest_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5 --expect-current-implementation-hash
python scripts/check_full2d_corpus_manifest_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_full2d_extraction_corpus_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5 --run-dir runs/geometry_full2d_v0_4_5
python scripts/check_full2d_claimspec_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
```

WP-08 and later may not run release matrix work until this WP passes.

## WP-08 — ActualTaskPipelineRunV3

Implement:

```bash
python scripts/run_full2d_actual_task_v0_4_5.py \
  --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml \
  --corpus-root benchmarks/geometry_full2d_v0_4_5 \
  --run-dir runs/geometry_full2d_v0_4_5 \
  --task-id <id> \
  --baseline B2
```

Rules:

- run only after WP-07A finalizes the sealed challenge corpus;
- no batch candidate file that bypasses per-task proof worker evidence;
- no source theorem with pre-existing proof;
- no synthetic final verify report;
- FinalVerifyGate must run on generated candidate file;
- actual task record must bind all artifacts with hash references;
- event log must show provider/engine artifacts created before compiler result and patch candidate.

Acceptance:

```bash
python scripts/check_actual_task_pipeline_runs_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
```

## WP-09 — Solver causality destructive reruns

Implement:

```bash
python scripts/run_solver_causality_mutations_v0_4_5.py \
  --run-dir runs/geometry_full2d_v0_4_5 \
  --all-b2-successes
```

For every counted B2 final theorem, run:

```text
positive_control
delete_selected_solver_artifact
corrupt_selected_solver_fact
unsupported_rule_mutation
side_condition_mutation if applicable
```

The same patch must not survive destructive mutation.

Acceptance:

```bash
python scripts/check_solver_causality_reports_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
```

The checker must inspect mutation rerun artifacts and fail on reports that only assign booleans.

## WP-10 — Baseline matrix

Implement actual baseline runner. It must not set outcome by family or label.

```bash
python scripts/run_full2d_matrix_v0_4_5.py \
  --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml \
  --run-dir runs/geometry_full2d_v0_4_5 \
  --execute-all
```

Baseline disabled component must remove artifacts from the pipeline:

```text
B1: no geometry provider output
B5: no construction engine output
B6: no algebraic/metric/angle/inequality output
B7: no order/case output
B8: model-disabled only when model provider is used
```

Acceptance:

```bash
python scripts/check_full2d_baseline_comparability_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5
python scripts/check_full2d_matrix_evidence_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5
python scripts/check_no_family_coded_baseline_v0_4_5.py --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml --run-dir runs/geometry_full2d_v0_4_5
```

## WP-11 — Metrics

Implement:

```bash
python scripts/check_full2d_metrics_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5
```

Metrics must derive from `ActualTaskPipelineRunV3`, `SelectedSolverDerivationV1`, and `SolverCausalityReportV2`, not from manifest labels.

Required summaries:

```text
B2 success rates
family rates
direct/wrapped facade fraction
solver causal success fraction
destructive rerun success fraction
non-target intermediate fact fraction
construction/case/certificate fraction
ExternalGoalPreserved success count
SealedPostImplementationChallenge success count
advantage summary
measured failure summary
```

The B6 advantage subset is exactly the algebraic/metric/angle/inequality subset from Base Spec section 7. It must not be narrowed to only algebraic or metric tasks.

## WP-12 — Regression failure suite

Implement fixtures that must fail:

```text
v0.4.2 overlay matrix
v0.4.3 projection corpus counted success
v0.4.4 proof-from-shape compiler
family-coded baseline
field-assigned causality report
engine output containing proof text
projection counted as positive
stale sealed challenge
pre-proved source theorem
selected solver derivation constructed from ClaimSpec alone
compiler still succeeds after selected solver artifact deletion
mutation rerun checker that only reads booleans
engine emits unchecked target fact with no rule trace/certificate/checker artifact
provider/engine imports compiler or proof-generation module
```

Acceptance:

```bash
python scripts/check_v0_4_5_regression_failures.py
```

## WP-13 — Final release acceptance

Implement:

```bash
python scripts/check_release_acceptance_v0_4_5.py \
  --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml \
  --output docs/ai/changes/geometry-full2d-v0_4_5/evidence/release_acceptance_report.json
```

This command must invoke or verify all WP acceptance commands.

It must fail closed if any required checker is missing, returns a placeholder report, lacks negative self-tests for its shortcut class, or reports success without current hash binding.

Release passes only if:

```text
status == passed
closure_allowed == true
hard_blockers == []
release_blockers == []
work_debt_open == []
all required summaries are nonempty
all thresholds pass
all destructive causality tests pass
all regression failure fixtures fail as expected
```

## WP-14 — Closure

Create `CLOSURE.md` only after final release acceptance passes.

Closure must include non-claims:

```text
no natural-language source fidelity claim unless separately audited
no open-problem solving claim
no TongGeometry model-backed claim
no production safety claim
```

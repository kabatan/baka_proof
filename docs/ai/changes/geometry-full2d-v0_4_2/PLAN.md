<!--
Generated for kabatan/baka_proof Guardian/Codex handoff.
Created: 2026-06-14
Status: USER_APPROVED_ACTIVE
-->
---
title: "Guardian Plan — Geometry × Lean Full2D Prover v0.4.2 Governed Full Implementation"
plan_id: "MARP-GEOLEAN-PLAN-007"
base_spec: "MARP-GEOLEAN-BASE-007"
status: "USER_APPROVED_ACTIVE"
target_repo: "kabatan/baka_proof"
created: "2026-06-14"
---

# Guardian Plan — Geometry × Lean Full2D Prover v0.4.2 Governed Full Implementation

## 0. Plan interpretation

This Plan implements `MARP-GEOLEAN-BASE-007`. It must not weaken the Base Spec.

The Plan is intentionally detailed so Codex can implement directly. Codex must not ask for clarification unless a HardBlocker condition from the Base Spec applies.

Release completion is all-or-nothing. Implementation flow is continue-on-debt. A ReleaseBlocker must be recorded and repaired; it must not stop unrelated tasks.

## 1. Required Guardian file layout

Create or replace:

```text
docs/ai/changes/geometry-full2d-v0_4_2/
  BASE_SPEC.md
  PLAN.md
  ACCEPTANCE.md
  ENGINE_CONTRACTS.md
  REFACTOR_DIRECTIVE.md
  SOURCE_MAP.md
  ACTIVE_CONTEXT.md
  CODEX_HANDOFF.md
  debt/
    debt_ledger.jsonl
  evidence/
    repo_audit.md
    dependency_resolution.json
    target_facade_status.json
    extraction_status.json
    engine_status.json
    rule_registry_status.json
    corpus_manifest.json
    frozen_corpus_manifest_hash.txt
    progress_acceptance_report.json
    release_acceptance_report.json
```

Archive older active geometry Guardian docs under:

```text
docs/ai/archive/geometry_pre_v0_4_2/
```

Do not delete run artifacts unless they are fixture-only and explicitly listed in the refactor directive.

## 2. Stop / continue decision algorithm

At every obstacle, Codex must execute this algorithm:

```text
1. Classify obstacle against HardBlocker list HB-01..HB-09.
2. If HardBlocker: stop, write blocker report, include exact requirement, evidence, and proposed options.
3. If not HardBlocker: create DebtLedgerEntry if it affects final release or future repair.
4. Continue the next independent task in the Plan.
5. Never close release while ReleaseBlockers or WorkDebt remain open.
```

Codex must not stop for:

```text
single failing test
missing optional local cache
one engine underperforming
one corpus family below threshold
one dependency requiring installation
one proof template missing
one extraction family failing
one benchmark subset failing
release acceptance returning blocked
```

Those are ReleaseBlockers or WorkDebt, not HardBlockers.

## 3. Work packages

### WP-00 — Install v0.4.2 authority and audit repo

Steps:

```text
1. Place Base Spec, Plan, Acceptance, Engine Contracts, Refactor Directive, Source Map, Active Context, Handoff under docs/ai/changes/geometry-full2d-v0_4_2/.
2. Move older geometry Guardian drafts to archive.
3. Run repo audit.
4. Produce evidence/repo_audit.md.
5. Initialize debt/debt_ledger.jsonl as empty file.
```

Acceptance:

```text
scripts/check_active_guardian_spec.py reports exactly one active geometry spec: MARP-GEOLEAN-BASE-007.
```

### WP-01 — Refactor release plugin boundary

Steps:

```text
1. Create plugins/geometry_full2d package.
2. Ensure release code imports geometry_full2d only.
3. Keep plugins/geometry_synthetic only as archived legacy.
4. Add regression test that fails if geometry_full2d imports geometry_synthetic.
5. Add regression test that fails if release configs reference geometry_synthetic.
```

Acceptance:

```text
python scripts/check_v0_4_2_plugin_boundary.py
```

### WP-02 — GeometryFull2DTarget Lean facade

Steps:

```text
1. Create lean/MathAutoResearch/GeometryFull2D/Basic.lean.
2. Create facade objects and predicates over LeanGeo/Mathlib, not toy definitions.
3. Create lemma namespaces for incidence, angle, metric, construction, transformation, algebraic, order/case, inequality.
4. Add no-toy-semantics checker.
5. Add Lean examples for each object/predicate family.
```

Default decisions:

```text
If LeanGeo API differs from expected names, create facade wrappers and mapping evidence.
If a LeanGeo concept is absent, use Mathlib or define a proved wrapper from admitted primitives.
Do not create axioms.
```

Acceptance:

```text
make lean-build
make lean-no-sorry
python scripts/check_geometry_full2d_facade.py
```

### WP-03 — Structured Lean extraction

Steps:

```text
1. Implement Lean command or elaborator-backed script that emits CanonicalGeometryStatementV1 JSON.
2. Python wrapper may only run Lean command and validate JSON.
3. Remove regex-only extraction from release path.
4. Include source expr hash and canonical expr hash for every object, hypothesis, target predicate, side condition.
5. Implement TargetClassification with in_target_positive, target_outside, malformed.
6. Add extraction fixtures for every grammar family.
```

Acceptance:

```text
python scripts/check_structured_extraction_v0_4_2.py
make test-unit TEST_FILTER=full2d_extraction
make test-mutation TEST_FILTER=full2d_extraction
```

### WP-04 — ClaimSpec and canonical statement bridge

Steps:

```text
1. Implement GeometryFull2DClaimSpec.
2. Implement canonicalization for objects, predicates, side conditions, target shapes.
3. Implement GoalRelation classifier exact_goal / target_outside / malformed.
4. Add claim_spec_hash and context_hash discipline.
5. Add invalidation on facade/theorem grammar changes.
```

Acceptance:

```text
make test-unit TEST_FILTER=full2d_claimspec
```

### WP-05 — Engine contracts and provider skeleton

Steps:

```text
1. Implement GeometryFull2DProvider.
2. Implement engine role registry with fixed roles.
3. Implement EngineRunRecord and ProviderRunManifestFull2D.
4. Add ResourceGovernor for every external process.
5. Add fixture/dummy detection; fixture_flag must be false in release.
```

Acceptance:

```text
python scripts/check_full2d_engine_contracts.py
make test-unit TEST_FILTER=full2d_provider
```

### WP-06 — SyntheticClosureEngine

Steps:

```text
1. Integrate Newclid-compatible symbolic closure where useful.
2. Implement rule-based synthetic closure over RuleRegistryFull2D.
3. Normalize output to Full2DTraceV1.
4. Include raw output hash and source rule refs.
5. Emit measured_failure if no closure is found.
```

Continue rule:

```text
If Newclid install/API fails, record WorkDebt and continue with local real rule-based closure. The final release still needs thresholds and real_integration_flag=true for this engine.
```

Acceptance:

```text
make test-unit TEST_FILTER=synthetic_closure
python scripts/smoke_full2d_engine.py --engine synthetic_closure
```

### WP-07 — ConstructionSearchEngine

Steps:

```text
1. Integrate GenesisGeo-compatible proposal if available.
2. Implement deterministic construction search over release construction templates.
3. Emit AuxiliaryConstructionFull2D objects with side-condition obligations.
4. Support line/circle/intersection/foot/midpoint/bisector/triangle-center/transform constructions.
5. Ensure B5 construction-disabled ablation disables this engine.
```

Acceptance:

```text
make test-unit TEST_FILTER=construction_search
python scripts/smoke_full2d_engine.py --engine construction_search
```

### WP-08 — AlgebraicGeometryEngine

Steps:

```text
1. Implement coordinate translation for admitted algebraic families.
2. Track nondegeneracy and denominator conditions.
3. Use exact rational/symbolic backend where possible.
4. Emit AlgebraicCertificateFull2D.
5. Implement certificate checker.
6. Compile checked certificate to Lean patch or Lean-checkable summary.
```

Allowed backends:

```text
SymPy exact Groebner/reduction
Sage if installable
Lean/Mathlib algebra tactics for fallback
custom exact checker with certificate artifact
```

Acceptance:

```text
make test-unit TEST_FILTER=algebraic_geometry_engine
python scripts/smoke_full2d_engine.py --engine algebraic_geometry
```

### WP-09 — MetricAngleEngine

Steps:

```text
1. Normalize directed angle expressions.
2. Implement angle chase rule families.
3. Implement cyclic angle and tangent-chord templates.
4. Support mod pi / mod 2pi policy explicitly.
5. Emit MetricAngleTraceFull2D.
```

Acceptance:

```text
make test-unit TEST_FILTER=metric_angle_engine
python scripts/smoke_full2d_engine.py --engine metric_angle
```

### WP-10 — TransformationEngine

Steps:

```text
1. Support reflection, rotation, homothety, inversion, spiral similarity subset.
2. Track construction side conditions.
3. Emit transformation trace and construction witnesses.
4. Compile transformation templates to Lean facade lemmas.
```

Acceptance:

```text
make test-unit TEST_FILTER=transformation_engine
python scripts/smoke_full2d_engine.py --engine transformation
```

### WP-11 — OrderCaseEngine

Steps:

```text
1. Support between / same-side / opposite-side / orientation cases.
2. Generate finite case obligations in ProofStateDAG.
3. Prove coverage of cases.
4. Compile each closed case into parent proof via CoverageGateFull2D.
```

Acceptance:

```text
make test-unit TEST_FILTER=order_case_engine
python scripts/smoke_full2d_engine.py --engine order_case
```

### WP-12 — InequalityEngine

Steps:

```text
1. Support length/angle/area/ratio inequalities in target grammar.
2. Use exact linear/nonlinear/SOS certificate path where applicable.
3. Track domain constraints.
4. Emit InequalityCertificateFull2D.
5. Verify certificate before proof-use.
```

Acceptance:

```text
make test-unit TEST_FILTER=inequality_engine
python scripts/smoke_full2d_engine.py --engine inequality
```

### WP-13 — LeanProofSearchEngine

Steps:

```text
1. Implement controlled Lean tactic proof search using the GeometryFull2D facade.
2. Allowed tactics include simp, aesop, nlinarith, linarith, ring_nf, omega, norm_num, exact known templates, and custom tactics.
3. Never modify theorem statement.
4. Never add axiom/admit/sorry.
5. Return LeanPatchCandidateFull2D only.
```

Acceptance:

```text
make test-unit TEST_FILTER=lean_proof_search_engine
```

### WP-14 — PortfolioCoordinator

Steps:

```text
1. Implement deterministic, versioned coordination policy.
2. Use extraction features to select engine order.
3. Allow parallel execution where resources permit.
4. Record reason_codes and engine selection features.
5. Do not let LLM/model choose proof-critical engine semantics.
```

Acceptance:

```text
make test-unit TEST_FILTER=portfolio_coordinator
python scripts/check_portfolio_reason_codes.py
```

### WP-15 — RuleRegistryFull2D

Steps:

```text
1. Implement >=150 concrete rules across >=25 families.
2. Add side-condition declarations for every rule.
3. Add positive/negative/mutation fixtures for every rule.
4. Add used-rule coverage reporting.
5. Add anti-duplicate rule checker.
```

Acceptance:

```text
python scripts/check_full2d_rule_registry.py
make test-unit TEST_FILTER=full2d_rule_registry
make test-mutation TEST_FILTER=full2d_rule_registry
```

### WP-16 — Compilers

Implement:

```text
TraceCompilerFull2D
ConstructionCompilerFull2D
AlgebraicCompilerFull2D
MetricAngleCompilerFull2D
TransformationCompilerFull2D
OrderCaseCompilerFull2D
InequalityCompilerFull2D
```

Each compiler must emit LeanPatchCandidateFull2D with:

```text
solver_dependency_refs
proof_template_id
used_rule_refs
used_side_condition_refs
raw_provider_output_used_as_proof=false
```

Acceptance:

```text
make test-unit TEST_FILTER=full2d_compilers
make test-mutation TEST_FILTER=full2d_compilers
```

### WP-17 — ProofWorker and FinalVerifyGate integration

Steps:

```text
1. Extend ProofWorker to apply LeanPatchCandidateFull2D.
2. Enforce proof-region-only edits.
3. FinalVerifyGate compiles generated candidate file directly.
4. SolverBackedProofCertificateFull2D must reference extraction, provider, normalized artifact, compiler, patch, worker, final verify, proof-region diff.
5. TrustGuard closes goal only with certificate + final theorem.
```

Acceptance:

```text
make test-unit TEST_FILTER=full2d_proof_worker
make test-unit TEST_FILTER=full2d_final_verify
make test-regression TEST_FILTER=proof_use_laundering
```

### WP-18 — Corpus generation and curation

Steps:

```text
1. Build positive corpora with >=3000 tasks.
2. Build negative/malformed/target-outside corpora with >=500 tasks.
3. Include external/human-curated sources >=900 positives.
4. Limit synthetic generated positives to <=50%.
5. Enforce duplicate constraints.
6. Freeze corpus manifest before final acceptance.
```

If external formal sources are sparse, Codex must create human-curated formal Lean tasks using the facade, but must label provenance honestly. It must not claim natural-language formalization fidelity.

Acceptance:

```text
python scripts/check_full2d_corpus_manifest.py
python scripts/freeze_full2d_corpus.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml
```

### WP-19 — Evaluation matrix

Baselines:

```text
B0 proof_worker_only
B1 controller_worker_no_geometry
B2 full_geometry_enabled
B3 strong_model_no_geometry
B4 lower_model_geometry_enabled
B5 construction_disabled
B6 algebraic_disabled
B7 order_case_disabled
B8 model_disabled
```

Steps:

```text
1. Run all corpora under required baselines.
2. Metrics must be artifact-derived from per-task results.
3. Compute family rates, overall rates, safe-reject counts, used-rule coverage, engine contribution, advantage deltas.
4. Produce reproducibility report.
```

Acceptance:

```text
python scripts/run_full2d_matrix.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml
python scripts/check_full2d_metrics.py --run-dir runs/geometry_full2d_v0_4_2
python scripts/generate_repro_report.py --run-dir runs/geometry_full2d_v0_4_2
```

### WP-20 — Progress acceptance

Codex must run progress acceptance periodically and after each major work package.

```bash
python scripts/check_v0_4_2_progress_acceptance.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/progress_acceptance_report.json
```

Progress acceptance reports:

```text
hard_blockers
release_blockers
work_debt
completed_work_packages
next_unblocked_work_packages
```

A progress acceptance report with ReleaseBlockers is not a reason to stop.

### WP-21 — Final acceptance and closure

Final commands:

```bash
make test-unit
make test-regression
make test-mutation
make test-integration
make lean-build
make lean-no-sorry
python scripts/check_release_acceptance_v0_4_2.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/release_acceptance_report.json
```

Closure allowed only when:

```text
hard_blockers=[]
release_blockers=[]
work_debt_open=[]
all performance thresholds passed
all anti-gaming checks passed
closure claim does not exceed evidence
```

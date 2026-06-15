<!--
Generated for kabatan/baka_proof Guardian/Codex handoff.
Created: 2026-06-14
Status: SUPERSEDED_BY_MARP-GEOLEAN-BASE-008
-->
---
title: "Guardian Base Spec — Geometry × Lean Full2D Prover v0.4.2 Governed Full Implementation"
spec_id: "MARP-GEOLEAN-BASE-007"
status: "SUPERSEDED_BY_MARP-GEOLEAN-BASE-008"
target_repo: "kabatan/baka_proof"
created: "2026-06-14"
supersedes:
  - "MARP-GEOLEAN-BASE-004"
  - "MARP-GEOLEAN-BASE-004A"
  - "MARP-GEOLEAN-BASE-004B"
  - "MARP-GEOLEAN-BASE-005"
  - "MARP-GEOLEAN-BASE-006"
claim_target: "V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY"
authority_model: "After user approval, this Base Spec is the only source of truth. Plan, implementation, tests, debt ledgers, and closure may not weaken it."
---

# Guardian Base Spec — Geometry × Lean Full2D Prover v0.4.2 Governed Full Implementation

## 0. Purpose

This document defines the full implementation target for `kabatan/baka_proof` after v0.3B.

The previous v0.3B state established a safe solver-backed proof-repair path over a small corpus. That is not enough. v0.4.2 requires a broad, high-performance 2D Euclidean geometry prover over the formal target language `GeometryFull2DTarget:1.0.0`.

This version also fixes an execution-management problem: Codex must not change or weaken the specification, but it must also not stop repeatedly for non-fatal implementation obstacles. Therefore v0.4.2 distinguishes:

```text
HardBlocker:
  stop-and-report immediately because continuing would be unsafe, contradictory, destructive, illegal/licensing-ambiguous, or would require changing this Base Spec.

ReleaseBlocker:
  does not allow final release claim, but Codex must continue all independent work, record the debt item, and re-run acceptance later.

WorkDebt:
  implementation debt that must be resolved before closure but must not stop unrelated work.

MeasuredFailure:
  a benchmark task failed honestly. It is counted in metrics; it is not a blocker unless corpus-level thresholds fail.
```

Completion claim is still all-or-nothing. The debt system is for implementation flow only; it is not a way to downgrade scope.

The only admitted completion claim is:

```text
V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY
```

This claim means:

```text
The repository implements a full geometry × Lean automated proving pipeline for GeometryFull2DTarget:1.0.0.
For every theorem in the approved in-target positive release corpora, the system must either produce a Lean final theorem through the full solver-backed chain or count it as a measured failure. It may not safe-reject in-target positive tasks.
The system includes structured Lean extraction, a real solver portfolio, broad rule and construction coverage, side-condition calculus, algebraic/metric/order/inequality fallback, Lean patch compilation, proof repair, FinalVerifyGate, SolverBackedProofCertificateFull2D, artifact-derived metrics, and release acceptance.
```

TongGeometry trained checkpoints are outside the release-critical path because public model artifacts were not found. TongGeometry must not be used to satisfy a required v0.4.2 engine, metric, or release threshold unless official artifacts become available and are separately admitted. v0.4.2 must stand without TongGeometry.

## 1. Non-negotiable decisions

### DR-007-001 — Full implementation, no partial completion

Codex must not close the change with any of the following substitute claims:

```text
experiment-ready only
proof plumbing only
small template corpus only
extractor-only release
Newclid-only release
construction-only release
algebraic-only release
solver-backed patch demonstration only
v0.3B compatibility release
partial completion
```

The final release claim is blocked until all acceptance requirements in this Base Spec and the Acceptance Spec pass.

### DR-007-002 — No spec rewrite by implementation agent

Codex must not change any of the following without explicit user approval:

```text
claim target
GeometryFull2DTarget scope
corpus floors
solve-rate floors
advantage thresholds
engine role list
release blocker severity definitions
Base/plugin separation
trust model
proof-use gates
accepted target library facade
```

If Codex believes a requirement is impossible, it must file a HardBlocker report. It must not silently lower the requirement.

### DR-007-003 — Guardian continue-on-debt policy

Codex must continue implementation when it encounters ReleaseBlocker or WorkDebt conditions. It must:

```text
1. create or update DebtLedgerEntry;
2. mark affected R-IDs and tasks;
3. continue all unrelated tasks;
4. avoid closure claim;
5. re-run acceptance after repairs.
```

Codex may stop only for HardBlockers defined in Section 13.

### DR-007-004 — One canonical proof target

The single release proof target is:

```text
GeometryFull2DTarget:1.0.0
```

It must be implemented as a Lean facade namespace over admitted LeanGeo and Mathlib definitions/theorems:

```text
MathAutoResearch.GeometryFull2D
```

Allowed implementation dependencies:

```text
LeanGeo.*
Mathlib.*
MathAutoResearch.GeometryFull2D.*
```

Forbidden in release target semantics:

```lean
def Point := Unit
def Coll ... := True
axiom Point : Type
axiom Coll : ...
axiom angle_eq : ...
axiom distance_eq : ...
axiom geometry_solver_sound : ...
```

The facade may define aliases, notation, derived lemmas, and proof templates. It must not replace real geometry with toy semantics.

### DR-007-005 — One canonical release plugin

The canonical release plugin is:

```text
plugins/geometry_full2d
```

`plugins/geometry_synthetic` is legacy. It must not be imported by v0.4.2 release code, release benchmarks, release acceptance, or `geometry_full2d`. It may remain only as archived compatibility code outside the release path.

### DR-007-006 — No loose optional engines

The release provider is exactly:

```text
GeometryFull2DProvider
```

The provider has fixed internal engine roles:

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

Each role is release-critical. If a role is missing, fixture-only, dummy-only, or not used by at least one counted release success, release fails. The engine implementation may use different concrete libraries or internal algorithms only if it satisfies the exact engine contract and the same acceptance thresholds.

### DR-007-007 — In-target positive tasks cannot safe-reject

For positive release corpora, a task labelled `target_status=in_target_positive` must never be counted as success by safe-reject, unsupported, diagnostic-only, or out-of-scope.

Allowed outcomes:

```text
final_theorem:
  counted success.

measured_failure:
  counted failure with diagnostic and blocker kind.
```

Disallowed outcomes for counted positive corpus:

```text
safe_reject_success
unsupported_success
out_of_scope_success
fixture_success
diagnostic_only_success
```

### DR-007-008 — Target-outside statements may safe-reject

The pipeline is not responsible for natural-language formalization faithfulness, 3D geometry, non-Euclidean geometry, arbitrary topology/calculus, or arbitrary higher-order Mathlib statements outside `GeometryFull2DTarget`. These are target-outside, not deferred in-target work.

For target-outside tasks, safe-reject is allowed if and only if structured extraction proves the statement is outside the target grammar and records a `TargetOutsideReport`.

## 2. Base architecture invariants

These remain inherited from the final repo target design.

```text
1. Base pipeline is domain-neutral.
2. GeometryFull2D intelligence belongs to plugins/geometry_full2d.
3. ProofStateDAG is minimal and domain-neutral.
4. Plugin may propose GraphPatch but may not mutate DAG directly.
5. ArtifactStore holds raw artifacts; DAG holds references and proof dependencies.
6. Raw solver output is never proof evidence.
7. Witness / certificate / trace / construction evidence must pass its checker/compiler path.
8. Final proof-use requires FinalVerifyGate and SolverBackedProofCertificateFull2D.
9. Agent/model output is proposal or diagnostic only, never proof evidence.
10. Agent note has no execution semantics.
```

Base must not import `plugins.geometry_full2d` internals except through plugin registry and declared capability contracts. Base must not import legacy `plugins.geometry_synthetic`.

## 3. GeometryFull2DTarget:1.0.0

### 3.1 Objects

The target language must support the following object kinds:

```text
Point, Line, Circle, Segment, Ray, Triangle, Polygon, Angle, DirectedAngle,
Length, Ratio, Area, Vector2D, Reflection, Rotation, Homothety, Inversion,
SpiralSimilarity, TriangleCenter, AuxiliaryObject
```

### 3.2 Predicates and relations

The target language must support at least:

```text
incidence:
  on_line, on_circle, collinear, concurrent, concyclic

parallel/perpendicular:
  parallel, perpendicular, perpendicular_bisector, foot_of_perpendicular

circle/tangent:
  tangent, chord, diameter, radical_axis, power_of_point

metric:
  equal_length, length_sum, ratio_eq, ratio_product, area_eq, area_ratio

angle:
  directed_angle_eq_mod_pi, directed_angle_eq_mod_2pi, angle_sum,
  cyclic_angle, tangent_chord_angle, angle_bisector

triangle:
  congruent_triangles, similar_triangles, isosceles, equilateral, right_triangle,
  median, altitude, angle_bisector_line, circumcenter, incenter, orthocenter, centroid

order/case:
  between, same_side, opposite_side, orientation_ccw, orientation_cw,
  inside_circle, outside_circle, inside_angle

transformations:
  reflection_image, rotation_image, homothety_image, inversion_image,
  spiral_similarity_center

inequality:
  length_le, length_lt, angle_le, angle_lt, area_le, ratio_le,
  triangle_inequality, power_sign

logical shapes:
  conjunction, disjunction with explicit case proof, existential construction witness,
  finite case split, implication over geometric hypotheses
```

### 3.3 Constructions

The target must support at least:

```text
line through two distinct points
circle with center through point
circle through three noncollinear points
line-line intersection
line-circle intersection
circle-circle intersection
parallel line through point
perpendicular line through point
foot of perpendicular
midpoint
angle bisector
perpendicular bisector
tangent line construction
reflection / rotation / homothety / inversion image
triangle centers
spiral similarity center
auxiliary point/line/circle introduction with side-condition obligations
```

### 3.4 Required theorem grammar

Release theorems must use the facade namespace `MathAutoResearch.GeometryFull2D`. Arbitrary raw LeanGeo or Mathlib expressions may appear inside facade definitions and bridge lemmas, but release benchmark statements must be expressible in `GeometryFull2DTheoremGrammarV1`.

A theorem is in-target iff structured extraction returns:

```yaml
TargetClassification:
  target_status: "in_target_positive"
  grammar_id: "GeometryFull2DTheoremGrammarV1"
  relation_to_goal: "exact_goal"
  unsupported_constructs: []
```

## 4. Structured Lean extraction

Regex-only extraction is forbidden for release path.

Required path:

```text
Lean theorem file
  -> lake env lean extraction command
  -> structured JSON emitted by Lean or Lean elaborator-backed command
  -> CanonicalGeometryStatementV1
  -> GeometryFull2DClaimSpec
```

Python may invoke the Lean command and validate JSON. Python must not infer target predicates by regex in release path.

### 4.1 CanonicalGeometryStatementV1

Each extracted statement must include:

```yaml
CanonicalGeometryStatementV1:
  schema_version: "1.0.0"
  theorem_name: "..."
  source_file: "..."
  source_statement_hash: "sha256:..."
  lean_context_hash: "sha256:..."
  target_library: "GeometryFull2DTarget:1.0.0"

  objects:
    - object_id: "pt:A"
      kind: "Point"
      source_expr: "..."
      source_expr_hash: "sha256:..."
      canonical_name: "A"

  hypotheses:
    - predicate_id: "hyp:..."
      family: "collinear | parallel | ..."
      args: []
      polarity: "positive | negative"
      source_expr_hash: "sha256:..."
      canonical_expr_hash: "sha256:..."

  target:
    predicate_or_shape_id: "goal:..."
    family: "..."
    args: []
    source_expr_hash: "sha256:..."
    canonical_expr_hash: "sha256:..."

  side_conditions:
    nondegeneracy: []
    orientation: []
    existence: []
    uniqueness: []
    order_cases: []

  relation_to_goal:
    kind: "exact_goal"
    direction_needed: "equivalence"
    direction_available: "lean_elaborated_exact"
```

### 4.2 Extraction acceptance

Release acceptance must fail if:

```text
1. any positive in-target corpus task is extracted by regex-only path;
2. extracted JSON lacks source expression hashes;
3. extractor silently drops nondegeneracy / orientation assumptions;
4. extractor classifies an in-target positive task as unsupported;
5. Python fabricates target grammar classification without Lean-side evidence;
6. extraction does not produce exact_goal relation for counted positive tasks.
```

## 5. Solver portfolio

The provider must be:

```text
plugins/geometry_full2d.provider.GeometryFull2DProvider
```

It must expose one public solve method:

```python
solve(request: GeometryFull2DSolveRequest) -> GeometryFull2DProviderRun
```

Internal engine roles are fixed:

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

Each engine must emit:

```yaml
EngineRunRecord:
  engine_role: "..."
  real_integration_flag: true
  fixture_flag: false
  backend_identity: "..."
  input_ref: "sha256:..."
  raw_output_hash: "sha256:..."
  normalized_output_ref: "... | null"
  checker_or_compiler_ref: "... | null"
  resource_usage_ref: "..."
  status: "normalized_success | measured_failure | diagnostic"
```

No engine may satisfy release by returning hard-coded theorem-name-specific patches. No engine may use raw model output as proof.

## 6. RuleRegistryFull2D

The release registry must include at least:

```text
150 concrete rules
25 rule families
30 construction templates
20 side-condition discharge procedures
```

However, rule count alone is not enough. Counted release successes must use at least:

```text
35 distinct concrete rules
15 distinct rule families
8 families outside incidence/collinearity
5 families requiring nontrivial side-condition discharge
4 families involving construction introduction
3 families involving algebraic/metric/angle reasoning
2 families involving order/case reasoning
2 families involving transformations
```

A rule counts as used only if:

```text
1. it appears in a normalized solver artifact;
2. TraceCompilerFull2D or ConstructionCompilerFull2D consumes it;
3. it is referenced by SolverBackedProofCertificateFull2D;
4. the final Lean theorem passes.
```

Each rule contract must include:

```yaml
RuleContractFull2D:
  rule_id: "..."
  family: "..."
  input_patterns: []
  output_patterns: []
  required_side_conditions: []
  generated_obligations: []
  lean_template_or_lemma: "..."
  proof_template: "..."
  unsupported_variants: []
  positive_fixtures: []
  negative_fixtures: []
  mutation_fixtures: []
```

## 7. SideConditionCalculusFull2D

Every rule and construction must declare side conditions. The calculus must handle:

```text
point distinctness
line nondegeneracy
circle nondegeneracy
intersection existence
intersection uniqueness
parallel/nonparallel alternatives
orientation cases
same/opposite side cases
between/order cases
angle directedness convention
denominator nonzero for ratios
nonzero lengths
nonzero areas
algebraic denominator conditions
inequality domain conditions
```

Missing side conditions must become ProofStateDAG obligations or measured failures. They must not be ignored.

## 8. Proof-use chain

A counted success must pass:

```text
structured extraction
GeometryFull2DClaimSpec creation
solver portfolio execution
normalized solver artifact creation
TraceCompilerFull2D / ConstructionCompilerFull2D / AlgebraicCompiler / InequalityCompiler
LeanPatchCandidateFull2D
ProofWorker patch application
FinalVerifyGate
SolverBackedProofCertificateFull2D
TrustGuard goal closure
artifact-derived metric inclusion
```

The following are never proof evidence:

```text
raw solver output
raw model output
rationale text
proof plan text
diagnostic-only provider output
uncompiled Lean patch
worker success claim without FinalVerifyGate
certificate without target-goal provenance
```

## 9. Corpus and benchmark floors

Release corpus must include at least:

```text
positive formal Lean tasks: 3000
negative / target-outside / malformed tasks: 500
external or human-curated positive tasks: 900
synthetic generated positive tasks: <= 50% of positives
near duplicate positive tasks: <= 10%
exact template duplicate max per theorem family: 5
```

Required positive benchmark families:

```text
Full2DCore500
IncidenceParallelPerp350
AngleCyclic450
Construction450
MetricRatioArea350
Transformation250
OrderCase250
Algebraic250
Inequality150
OlympiadStyle300
HardHoldout50
```

Difficulty tiers:

```text
tier_0_smoke: <= 100
tier_1_basic: >= 400
tier_2_multistep: >= 500
tier_3_construction: >= 350
tier_4_algebraic_metric_angle: >= 350
tier_5_olympiad_style: >= 300
tier_6_hard_holdout: >= 50
```

Corpora must be frozen before final acceptance run. The final run must record `frozen_corpus_manifest_hash` and fail if corpus files change afterward.

## 10. Performance thresholds

Release acceptance must verify:

```text
Full2DCore500 final theorem rate >= 0.95
IncidenceParallelPerp350 final theorem rate >= 0.92
AngleCyclic450 final theorem rate >= 0.90
Construction450 final theorem rate >= 0.85
MetricRatioArea350 final theorem rate >= 0.85
Transformation250 final theorem rate >= 0.75
OrderCase250 final theorem rate >= 0.80
Algebraic250 final theorem rate >= 0.85
Inequality150 final theorem rate >= 0.75
OlympiadStyle300 final theorem rate >= 0.70
HardHoldout50 final theorem rate >= 0.50
Overall positive final theorem rate >= 0.85
In-target positive safe-reject success count = 0
```

Advantage requirements:

```text
B2 full portfolio - B1 no geometry solver >= 0.25 overall final theorem rate
B2 - B5 construction disabled >= 0.15 on construction subset
B2 - B6 algebraic disabled >= 0.15 on algebraic/metric subset
B2 - B7 order/case disabled >= 0.10 on order/case subset
B2 - B8 model disabled >= 0.05 on olympiad-style subset if model provider is used
```

If a threshold fails, the result is a ReleaseBlocker. Codex must continue repair and corpus/engine work. It must not lower the threshold.

## 11. Anti-gaming requirements

Release fails if any of the following occur:

```text
1. benchmark theorems are edited after seeing solver output without updating frozen manifest and review evidence;
2. counted theorem names are hard-coded in solver, compiler, or proof worker;
3. success is obtained by replacing target semantics with toy definitions;
4. rule count is inflated by unused duplicate rules;
5. corpus is dominated by near-duplicates;
6. safe-reject is used as success for positive in-target tasks;
7. B2/B1 advantage comes from disabling final verification in baseline;
8. proof worker directly claims final theorem;
9. raw solver output appears in proof region replacement text;
10. final theorem count is computed from labels rather than artifacts.
```

## 12. Acceptance commands

During implementation Codex should run progress acceptance:

```bash
python scripts/check_v0_4_2_progress_acceptance.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml
```

Progress acceptance may pass with ReleaseBlockers and WorkDebt if no HardBlockers exist. It is not a release claim.

Final release acceptance:

```bash
python scripts/check_release_acceptance_v0_4_2.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/release_acceptance_report.json
```

Final release passes only if:

```text
hard_blockers = []
release_blockers = []
work_debt_open = []
all thresholds pass
all trust and proof-use gates pass
closure claim does not exceed evidence
```

## 13. HardBlocker policy

Codex must stop and report only for these cases:

```text
HB-01: active approved specs conflict and no precedence rule resolves it.
HB-02: implementation would require changing this Base Spec, Acceptance Spec, or thresholds.
HB-03: required action would delete user data or repo history outside explicit refactor scope.
HB-04: dependency license or terms clearly prohibit required use.
HB-05: required credential/secret/private model is unavailable and no allowed substitute contract exists.
HB-06: target semantics require a mathematical design choice not specified here and multiple choices are incompatible.
HB-07: continuing would create an unsound proof-use path that cannot be isolated.
HB-08: local environment cannot run Lean at all after bootstrap attempts, blocking every independent workstream.
HB-09: Guardian state files are corrupted such that source of truth cannot be determined.
```

Anything else is ReleaseBlocker or WorkDebt and must not stop unrelated work.

## 14. DebtLedger

Codex must maintain:

```text
docs/ai/changes/geometry-full2d-v0_4_2/debt/debt_ledger.jsonl
```

Each entry:

```yaml
DebtLedgerEntry:
  debt_id: "debt:..."
  severity: "ReleaseBlocker | WorkDebt"
  affected_rids: []
  affected_tasks: []
  summary: "..."
  evidence_ref: "..."
  unblock_plan: []
  status: "open | in_progress | closed"
  closure_evidence_ref: "... | null"
```

Debt entries do not weaken requirements. A ReleaseBlocker in the debt ledger still blocks final release.

## 15. Closure rules

Closure may claim `V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY` only if final release acceptance passes.

Closure must not claim:

```text
natural-language formalization faithfulness
all possible geometry beyond GeometryFull2DTarget
open-problem solving
production safety
TongGeometry model-backed readiness
```

unless separate approved specs and evidence exist.

<!--
Generated for kabatan/baka_proof Guardian/Codex handoff.
Created: 2026-06-14
Status: USER_APPROVED_ACTIVE
-->
---
title: "Engine Contracts — GeometryFull2D v0.4.2"
contract_id: "MARP-GEOLEAN-ENGINE-CONTRACTS-007"
base_spec: "MARP-GEOLEAN-BASE-007"
status: "USER_APPROVED_ACTIVE"
created: "2026-06-14"
---

# Engine Contracts — GeometryFull2D v0.4.2

## 0. Common engine contract

Every engine role must implement:

```python
run(input: EngineInputFull2D, budget: ResourceBudget, context: RunContext) -> EngineOutputFull2D
```

Every output must include:

```yaml
EngineOutputFull2D:
  schema_version: "1.0.0"
  engine_role: "..."
  backend_identity: "..."
  real_integration_flag: true
  fixture_flag: false
  input_ref: "sha256:..."
  raw_output_hash: "sha256:..."
  normalized_output_ref: "... | null"
  checker_or_compiler_ref: "... | null"
  resource_usage_ref: "..."
  status: "normalized_success | measured_failure | diagnostic"
  proof_use_status: "not_allowed"
```

No engine may emit final theorem evidence. Only FinalVerifyGate + SolverBackedProofCertificateFull2D can close proof-use.

## 1. synthetic_closure

Purpose:

```text
Derive synthetic geometry facts from hypotheses: incidence, collinearity, parallel, perpendicular, cyclic, basic angle facts, and simple triangle facts.
```

Required outputs:

```text
Full2DTraceV1 with rule IDs from RuleRegistryFull2D.
```

Allowed internal backends:

```text
Newclid-compatible closure
custom deterministic deductive database
Lean-based closure over facade lemmas
```

Must not:

```text
hard-code theorem names
return trace without rule IDs
use raw prover text as proof
```

## 2. construction_search

Purpose:

```text
Introduce auxiliary points, lines, circles, centers, intersections, transformations, and witnesses.
```

Required outputs:

```text
AuxiliaryConstructionFull2D with side-condition obligations.
```

Allowed internal backends:

```text
GenesisGeo-compatible proposer
deterministic enumerative construction search
LLM proposal as diagnostic only followed by deterministic checker
```

LLM proposals cannot be proof evidence.

## 3. algebraic_geometry

Purpose:

```text
Solve coordinate/algebraic subgoals with exact certificate tracking.
```

Required outputs:

```text
AlgebraicCertificateFull2D
nondegeneracy and denominator conditions
checker result
```

Allowed backends:

```text
SymPy exact Groebner/reduction
Sage if installable
Lean/Mathlib algebra tactics
custom exact certificate checker
```

## 4. metric_angle

Purpose:

```text
Angle chase, directed angle normalization, cyclic angle, tangent-chord, equal length, ratio and area relations.
```

Required outputs:

```text
MetricAngleTraceFull2D
used angle convention
side-condition obligations
```

## 5. transformation

Purpose:

```text
Reflection, rotation, homothety, inversion, spiral similarity, and transformation image reasoning.
```

Required outputs:

```text
TransformationTraceFull2D or construction witnesses.
```

## 6. order_case

Purpose:

```text
Between, same/opposite side, orientation, inside/outside, and finite case splits with coverage.
```

Required outputs:

```text
OrderCaseSplitFull2D
CoverageCertificateFull2D
per-case proof obligations
```

## 7. inequality

Purpose:

```text
Length, angle, area, ratio, triangle inequality, power sign, and other target inequalities.
```

Required outputs:

```text
InequalityCertificateFull2D
checker result
Lean patch candidate or Lean-checkable summary
```

## 8. lean_proof_search

Purpose:

```text
Generate Lean proof patches using admitted facade lemmas and controlled tactics.
```

Allowed tactics:

```text
simp, aesop, exact, apply, constructor, rcases, obtain, ring_nf, nlinarith, linarith, omega, norm_num, positivity, field_simp with side conditions
```

Forbidden:

```text
sorry
admit
axiom
unsafe theorem statement edit
changing target theorem statement
editing outside admitted proof/helper regions
```

## 9. portfolio_coordinator

Purpose:

```text
Coordinate all engines deterministically, record reason codes, manage fallback, and produce ranked normalized artifacts.
```

Must record:

```text
engine_order
engine_selection_features
fallback_reason_codes
budget profile
resource usage refs
failure reasons
```

Must not delegate proof-critical decisions to an LLM without deterministic validation.

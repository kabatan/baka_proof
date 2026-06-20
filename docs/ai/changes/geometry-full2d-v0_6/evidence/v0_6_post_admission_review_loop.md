# v0.6 Post-Admission Review Loop

Status: fixable review issues found; fixes applied and pending re-review.

Date: 2026-06-20

## Scope

The review checks whether `PLAN.md` necessarily forces `BASE_SPEC.md`, whether Acceptance covers all release-critical requirements, and whether the documents leave room for shortcut closure.

## Local Fix Before Review

`RED_CASE_SUITE.md` was normalized to list the full `RC-001` through `RC-019` set from `BASE_SPEC.md`.

Reason:

```text
The imported red-case suite listed only 16 main items and then had duplicate trailing numbered items after the authority identifier block. Base Spec section 2 defines 19 release-blocking red cases. Without normalization, Plan WP01 could be executed against an incomplete red-case list.
```

This fix tightens the Plan/Red-case alignment to Base Spec and does not reduce any v0.6 requirement.

## Review Result

Initial `guardian_boundary_reviewer` result:

```text
RESULT: FAIL_FIXABLE
```

Issues found:

1. Red-case suite IDs shifted after `RC-008` and did not exactly match Base Spec RC meanings.
2. Acceptance required checker list did not include Plan-required extraction, ClaimSpec, and engine-output-not-from-compiler-rules checkers.
3. Plan wording made the target-match report sound like a compiler input, conflicting with the exact four-input compiler API in Base Spec DR-012-004.

Fixes applied:

1. `RED_CASE_SUITE.md` now maps `RC-001` through `RC-019` exactly to the Base Spec headings and keeps `EngineOutputContainsProofText` as a non-RC K-010 fixture.
2. `ACCEPTANCE.md` now requires nonempty extraction, ClaimSpec, and engine-output-not-from-compiler-rules report fields and final checker invocations.
3. `PLAN.md` now states that `DerivationTargetMatcher` gates compiler invocation, while `compile_derivation` remains exactly the DR-012-004 API and does not receive a target-match report.

Re-review:

```text
RESULT: PASS
```

Non-blocking reviewer note resolved:

```text
PLAN.md and RED_CASE_SUITE.md now both use tests/red_cases/geometry_full2d_v0_6/ as the WP01 red-case fixture path.
```

## Claim Ceiling

Allowed after checks and boundary review pass:

```text
MARP-GEOLEAN-BASE-012 / PLAN-012 / ACCEPTANCE-012 are installed and can be used to begin WP01 implementation.
```

Not allowed:

```text
V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
PRODUCTION_SAFE
R-ID VERIFIED
```

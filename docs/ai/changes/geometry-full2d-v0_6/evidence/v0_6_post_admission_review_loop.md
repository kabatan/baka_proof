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

## Second Intent-Fidelity Review

Reviewer: main agent self-review before implementation start.

Status:

```text
fixes applied; pending boundary re-review
```

Issues found:

1. `PLAN.md` red-case-first prohibition named provider/compiler/matrix but did not explicitly name rule registry, corpus expansion, or release-acceptance code.
2. Some historical-evidence language said only `draft v0.5`, which could leave prior v0.5 implementation artifacts looking more authoritative than intended.
3. Used-rule coverage and engine contribution were present as report fields and metrics, but not as dedicated required release checkers.
4. `K-028` could be read as letting a measured unavailability/debt report satisfy engine contribution in final release, instead of only explaining a ReleaseBlocker or measured failure.

Fixes applied:

1. `PLAN.md` now forbids provider, compiler, rule registry, matrix, corpus expansion, and release-acceptance implementation before WP01 red cases pass.
2. `BASE_SPEC.md`, `PLAN.md`, `ACCEPTANCE.md`, `REFACTOR_DIRECTIVE.md`, `ACTIVE_CONTEXT.md`, and `SOURCE_MAP.md` now consistently treat prior v0.5 release artifacts as historical/non-release evidence.
3. `PLAN.md` and `ACCEPTANCE.md` now require `check_used_rule_coverage_v0_6.py` and `check_engine_contribution_v0_6.py` as dedicated release checks.
4. `BASE_SPEC.md`, `PLAN.md`, and `ACCEPTANCE.md` now state that measured unavailability/debt reports cannot satisfy final release metrics for enabled release-critical engine roles or counted rule-family thresholds.

Boundary reviewer result:

```text
RESULT: FAIL_FIXABLE
```

Additional issues found:

1. The compiler could still use theorem anchor identifiers, such as theorem name, statement hash, proof-region identity, or binder-map identity, as strategy keys.
2. Release-critical engine roles were not enumerated, so an implementation could define a narrow role set after seeing what succeeded.
3. The non-target intermediate requirement was partly syntactic and could count target-equivalent wrappers or direct facade targets.

Fixes applied:

1. `BASE_SPEC.md`, `PLAN.md`, `ACCEPTANCE.md`, and `RED_CASE_SUITE.md` now forbid compiler proof/rule-plan selection from theorem anchor identifiers and require anchor-identifier taint tests.
2. `BASE_SPEC.md` defines the exact `ReleaseCriticalEngineRoleV1` set, enabled/disabled rules, and corpus-subset mapping; `PLAN.md` and `ACCEPTANCE.md` require `check_engine_contribution_v0_6.py` to enforce that exact list.
3. `BASE_SPEC.md`, `PLAN.md`, `ACCEPTANCE.md`, and `RED_CASE_SUITE.md` now require semantic non-targetness and reject target-hash, alpha-renamed, trivial wrapper, reflexivity/symmetry-equivalent, and direct-facade intermediates.

Re-review:

```text
RESULT: PASS
```

Final reviewer note:

```text
No remaining blocker found in the provided packet scope. Anchor identifiers cannot drive compiler strategy/rules/lemmas/ordering; ReleaseCriticalEngineRoleV1 is enumerated and checker-bound; semantic non-targetness rejects target-equivalent intermediates and facade wrappers.
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

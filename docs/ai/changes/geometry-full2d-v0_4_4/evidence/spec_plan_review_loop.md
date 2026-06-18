---
title: "Spec/Plan Review Loop — v0.4.4"
status: "PASS_AFTER_FIXES"
created: "2026-06-18"
base_spec: "MARP-GEOLEAN-BASE-009"
plan: "MARP-GEOLEAN-PLAN-009"
acceptance: "MARP-GEOLEAN-ACCEPTANCE-009"
---

# Spec/Plan Review Loop — v0.4.4

## Scope

This review loop checked:

- Base Spec internal consistency.
- Plan fidelity to the Base Spec.
- Plan executability and likely blocker risks.
- Agent rollback/gaming paths, including old-path reuse, renamed wrappers, stale evidence, and marker-string-only checks.

## Initial Review Result

`guardian_boundary_reviewer` returned `FAIL_FIXABLE`.

Issues found:

- Solver-causality was inconsistent: every counted B2 final theorem required solver causality, but the reported fraction threshold allowed less than 100%.
- Positive family corpus floors were in the Base Spec but not explicitly enforced in Acceptance.
- Used-rule numeric thresholds were in Acceptance without Base Spec sourcing.
- Compiler isolation gates were narrower than the Base Spec's forbidden proof-decision fields.
- Active authority checking relied too much on marker strings.
- Active checker depended on a stale "WP01 and later has not started" context line.
- WP00 checker deliverables did not fully match WP00 Plan deliverables.
- Old-path rollback detection needed explicit renamed/wrapped/shimmed path coverage.

## Fixes Applied

- Set `solver_causal_success_fraction = 1.00` for counted B2 final theorem successes.
- Added `family_floor_summary` and explicit family-floor checks to Acceptance/report shape.
- Moved used-rule numeric thresholds into the Base Spec.
- Expanded `K-015` to fail on every Base-forbidden proof-decision field.
- Added stale/hash-unbound evidence gate `K-026`.
- Added renamed old release path gate `K-027`.
- Required freshness binding for reused checker, matrix, corpus, and release artifacts.
- Required old-path detection by path, imports, call graph/direct invocation targets, command provenance, and known old-entrypoint hashes/signatures.
- Added WP00 deliverables for `README.md`, `FAILURE_ANALYSIS.md`, bundle hashes, and import evidence.
- Removed the active checker dependency on stale "implementation has not started" text.
- Added exact normalized SHA-256 guards for active authority documents in `scripts/check_active_guardian_spec_v0_4_4.py`, including change-local `ACTIVE_CONTEXT.md`.

## Verification

Commands passed:

```bash
python -m py_compile scripts/check_active_guardian_spec_v0_4_4.py scripts/check_active_guardian_spec.py
python scripts/check_active_guardian_spec_v0_4_4.py
python scripts/check_active_guardian_spec.py
```

Final `guardian_boundary_reviewer` re-review returned `PASS` for the remaining mismatch fix:

```text
The previous FAIL_FIXABLE is fixed. scripts/check_active_guardian_spec_v0_4_4.py now requires docs/ai/changes/geometry-full2d-v0_4_4/ACTIVE_CONTEXT.md, includes it in the WP00 required-file guard, and hash-guards it with the v0.4.4 authority bundle.
```

## Claim Boundary

This review does not claim:

```text
V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY
ACCEPTANCE_COMPLETE
SOURCE_FAITHFUL
PRODUCTION_SAFE
R-ID VERIFIED
```

It claims only that the active v0.4.4 Base Spec / Plan / Acceptance review loop passed after fixable documentation and checker issues were corrected.

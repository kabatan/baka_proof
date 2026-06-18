---
title: "Evidence — v0.4.5 Base Spec / Plan Review Loop"
status: "EVIDENCE"
created: "2026-06-18"
base_spec: "MARP-GEOLEAN-BASE-010"
plan: "MARP-GEOLEAN-PLAN-010"
acceptance: "MARP-GEOLEAN-ACCEPTANCE-010"
---

# Evidence — v0.4.5 Base Spec / Plan Review Loop

## Scope

Reviewed the active v0.4.5 Guardian documents for:

- whether executing Plan fully forces Base Spec compliance;
- whether Base Spec and Plan preserve the user's no-shortcuts intent;
- whether Agent freedom remains that could permit easier checker-passing behavior;
- whether the plan is coherent and avoids nonessential blockers.

## Review Loop Findings And Fixes

### Loop 1 — Sealed challenge timing contradiction

Finding:

Base Spec requires counted `SealedPostImplementationChallenge` tasks to be generated after provider/compiler/rule-registry implementation freeze. Plan WP-02 previously placed sealed challenge generation and manifest acceptance before those components existed.

Fix:

- WP-02 now implements only grammar/generator/static independence checks.
- New WP-07A performs implementation freeze and counted sealed challenge finalization.
- WP-08 and later are explicitly blocked until WP-07A passes.
- Acceptance now requires current implementation hash binding for sealed challenge manifests.

### Loop 2 — Shortcut checker nonessential blocker

Finding:

Plan WP-01 required a shortcut checker to inspect actual release run artifacts before actual runs can exist.

Fix:

- WP-01 now requires `check_release_path_forbidden_shortcuts_v0_4_5.py --static-only`.
- WP-13 final release requires full mode with `--config` and `--run-dir`.

### Loop 3 — External source availability escape hatch

Finding:

The availability fallback could be misused if Codex or the importer self-declared external sources unavailable.

Fix:

- Base Spec now requires independent `ExternalSourceAvailabilityReportV1` evidence with registry entries, checked paths/URLs, command or HTTP evidence, timestamps, retry policy, and concrete rejection reasons.
- Plan requires `metadata/external_source_registry.json`.
- Plan states the importer cannot self-declare unavailable sources.

### Loop 4 — Baseline and advantage ambiguity

Finding:

Acceptance shortened the B6 advantage subset label to `algebraic/metric`, while Base Spec requires `algebraic/metric/angle/inequality`. Baseline anti-family checker also lacked dynamic run evidence arguments.

Fix:

- Acceptance now uses the full `algebraic/metric/angle/inequality` subset.
- Plan states the B6 subset must not be narrowed.
- Plan and Acceptance require `check_no_family_coded_baseline_v0_4_5.py --config ... --run-dir ...`.

### Loop 5 — Final gate did not list all WP gates

Finding:

Final Acceptance command list omitted rule registry checking and implementation freeze verification.

Fix:

- Acceptance now includes `check_full2d_rule_registry_v0_4_5.py`.
- Acceptance and WP-07A now include `check_full2d_implementation_freeze_v0_4_5.py`.
- Plan requires final checker to fail closed on missing checkers, placeholder reports, missing negative self-tests, or missing current hash binding.

### Loop 6 — Regression fixture coverage gap

Finding:

Plan WP-12 did not explicitly list all Base-required anti-shortcut regressions.

Fix:

WP-12 now also requires failures for:

- mutation rerun checker that only reads booleans;
- unchecked target fact with no rule trace/certificate/checker artifact;
- provider/engine importing compiler or proof-generation code.

## Verification

Commands run after fixes:

```powershell
python scripts\check_active_guardian_spec_v0_4_5.py
python scripts\check_active_guardian_spec.py
python scripts\check_v0_4_5_spec_plan_consistency.py
python -m py_compile scripts\check_v0_4_5_spec_plan_consistency.py scripts\check_active_guardian_spec_v0_4_5.py
```

All reported `status: passed` or returned 0.

## Claim Ceiling

This review loop only claims:

```text
MARP-GEOLEAN-BASE-010 / PLAN-010 / ACCEPTANCE-010 are more tightly aligned for implementation start.
```

It does not claim:

```text
V0.4.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
ACCEPTANCE_COMPLETE
SOURCE_FAITHFUL
PRODUCTION_SAFE
```

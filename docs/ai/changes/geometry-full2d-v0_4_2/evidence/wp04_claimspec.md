---
title: WP-04 ClaimSpec evidence
status: PASSED
created: 2026-06-15
purpose: Record evidence for the GeometryFull2D ClaimSpec and canonical bridge work package.
authority: Evidence only; does not claim v0.4.2 release completion.
---

# WP-04 ClaimSpec Evidence

## Scope

WP-04 added `GeometryFull2DClaimSpec` creation from `CanonicalGeometryStatementV1` payloads emitted by the Lean extraction smoke. The bridge validates source/canonical hashes, side-condition buckets, exact-goal relation, target-family admission, and deterministic claim/context hashes.

The implementation also emits diagnostic-only `TargetOutsideReport` and `MalformedStatementReport` outputs rather than creating claims for target-outside or malformed payloads.

## Verification

```text
python scripts/check_full2d_claimspec.py
```

Result:

```text
passed
```

```text
python -m pytest tests/unit/test_geometry_full2d_claimspec.py -q
```

Result:

```text
3 passed
```

```text
python scripts/check_v0_4_2_progress_acceptance.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/progress_acceptance_report.json
```

Result:

```text
hard_blockers=[]
completed_work_packages includes WP-04:claimspec-checker-passed
next_unblocked_work_packages includes WP-05, WP-15, and WP-20
```

## Claim Ceiling

This closes the WP-04 ClaimSpec bridge only. It does not yet satisfy provider manifests, engine implementation, rule registry, corpus, performance, or final release acceptance.

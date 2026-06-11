---
title: v0.3A Guardian Boundary Review
date: 2026-06-12
status: PASS
base_spec: MARP-GEOLEAN-BASE-003A
plan: MARP-GEOLEAN-PLAN-003A
authority: Guardian boundary reviewer evidence for document admission only; does not mark R-IDs VERIFIED or grant completion claims.
---

# v0.3A Guardian Boundary Review

## Initial Result

Initial result: BLOCK.

Blocking findings:

1. `BASE-003A` weakened the user local resource policy by summarizing broad profile fields instead of carrying exact minimum fields and budget values.
2. `PLAN-003A` allowed mandatory ResourceGovernor controls to be explicitly reported instead of enforced.

## Remediation

- `BASE-003A` now includes exact `LocalResourceProfile` minimum fields and budget profile constraints, including timeouts, allowed roles, `heavy_search_exclusive`, and `extreme.requires_explicit_run_label`.
- `PLAN-003A` T-003 now requires direct-launch prevention, per-engine semaphores, timeout/process-group termination, heartbeat/stale detection, Lean/FinalVerify priority, and `ResourceUsageReport` to be implemented and enforced. Only disk/checkpoint cache limits may be enforced or measured/reported when platform support prevents enforcement.

## Final Result

Final result: PASS.

Reviewer statement:

> BASE-003A / PLAN-003A document preparation is admissible for Guardian boundary admission.

Admission scope:

- Document preparation only.
- No R-ID is marked VERIFIED.
- No real-integration completion is approved.
- Claims remain within the current fixture-level ceiling until fresh v0.3A evidence and final reviews exist.

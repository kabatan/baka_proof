---
title: Change Index — GeometryFull2D v0.4.2
change_id: geometry-full2d-v0_4_2
version: v0.4.2-governed-full2d
status: WP01_PLUGIN_BOUNDARY_PASSED_WP02_READY
created: 2026-06-15
purpose: Index the Guardian document set for the GeometryFull2D v0.4.2 governed full implementation track.
authority: Navigation only; individual Base Spec, Plan, Acceptance, and contract documents declare their own authority.
---

# Change Index — GeometryFull2D v0.4.2

## Purpose

This change prepares the Guardian track for:

```text
V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY
```

The track supersedes the previous v0.3, v0.3A, v0.3 full-rebase, v0.3A patch, and v0.3B solver-backed proof-repair tracks as release authority. Those tracks remain historical evidence and safety background only.

## Primary Documents

- `BASE_SPEC.md` — correctness authority for `MARP-GEOLEAN-BASE-007`.
- `PLAN.md` — execution contract for `MARP-GEOLEAN-PLAN-007`; it cannot weaken the Base Spec.
- `ACCEPTANCE.md` — release and progress acceptance requirements for `MARP-GEOLEAN-ACCEPTANCE-007`.
- `ENGINE_CONTRACTS.md` — required GeometryFull2D engine contracts.
- `BLOCKER_AND_DEBT_POLICY.md` — mandatory HardBlocker / ReleaseBlocker / WorkDebt policy.
- `REFACTOR_DIRECTIVE.md` — repository refactor directive for the v0.4.2 release path.
- `SOURCE_MAP.md` — non-authoritative traceability aid.
- `ACTIVE_CONTEXT.md` — change-local navigation state.
- `CODEX_HANDOFF.md` — non-authoritative handoff prompt.

## Evidence

- `evidence/bundle_sha256sums.txt` — SHA-256 hashes supplied in the research-agent bundle.
- `evidence/installed_sha256sums.txt` — SHA-256 hashes after local Guardian status installation.
- `evidence/v0_4_2_bundle_import.md` — user-approved bundle import record.
- `evidence/repo_audit.md` — initial import-stage repository audit.
- `debt/debt_ledger.jsonl` — initialized empty debt ledger.

## Current Gate

Current task:

```text
WP-02 — GeometryFull2DTarget Lean facade
```

WP-00 is complete for implementation flow:

```text
scripts/check_active_guardian_spec.py reports exactly one active geometry spec: MARP-GEOLEAN-BASE-007.
Initial progress acceptance reports hard_blockers=[] and progress_ok_with_debt.
ReleaseBlocker and WorkDebt items are recorded in debt/debt_ledger.jsonl.
WP-01 plugin boundary checker passed.
```

## Claim Ceiling

Allowed:

```text
MARP-GEOLEAN-BASE-007 / PLAN-007 / ACCEPTANCE-007 are installed as the active user-approved v0.4.2 Guardian authority set.
Implementation has not yet satisfied v0.4.2 release acceptance.
```

Not allowed:

```text
V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
PRODUCTION_SAFE
R-ID VERIFIED
```

## Superseded Tracks

The older v0.3-family documents are not active release authority for new work. They are retained in their existing locations during import because current repository scripts and tests still reference their evidence paths. Physical archival and reference repair are part of WP-00 implementation, not a pre-implementation file move.

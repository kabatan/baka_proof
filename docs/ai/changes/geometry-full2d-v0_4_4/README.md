---
title: "GeometryFull2D v0.4.4 Guardian Track"
status: "SUPERSEDED_BY_MARP-GEOLEAN-BASE-010"
base_spec: "MARP-GEOLEAN-BASE-009"
plan: "MARP-GEOLEAN-PLAN-009"
acceptance: "MARP-GEOLEAN-ACCEPTANCE-009"
created: "2026-06-18"
---

# GeometryFull2D v0.4.4 Guardian Track

This directory contains the historical Guardian authority set for the v0.4.4 real solver-causal Full2D pipeline track.

The v0.4.4 track is superseded by `MARP-GEOLEAN-BASE-010` for new release work. Its closure and release report remain historical evidence and regression material, but they are not active v0.4.5 release authority.

The v0.4.4 reviewed bundle supersedes v0.4.3 for new release work. v0.4.3 evidence remains historical and may be used only as regression or negative evidence unless it satisfies this v0.4.4 authority set.

## Authority Files

- `BASE_SPEC.md` — correctness authority for `MARP-GEOLEAN-BASE-009`.
- `PLAN.md` — execution contract for `MARP-GEOLEAN-PLAN-009`.
- `ACCEPTANCE.md` — release gates for `MARP-GEOLEAN-ACCEPTANCE-009`.
- `REAL_PIPELINE_INVARIANTS.md` — release-critical invariants.
- `REFACTOR_DIRECTIVE.md` — v0.4.3 release-path quarantine and replacement directive.
- `SOURCE_MAP.md` — traceability aid.
- `ACTIVE_CONTEXT.md` — change-local context seed.
- `CODEX_HANDOFF.md` — implementation handoff.
- `SELF_REVIEW_LOG.md` — research-agent self review notes.
- `FAILURE_ANALYSIS.md` — failure analysis motivating v0.4.4.

## Evidence and Debt

- `evidence/v0_4_4_bundle_import.md` — import evidence, hash verification, installed mapping, and claim ceiling.
- `evidence/bundle_sha256sums.txt` — original reviewed bundle hash manifest.
- `debt/debt_ledger.jsonl` — v0.4.4 debt ledger. Open entries block closure.

## First Command

```bash
python scripts/check_active_guardian_spec_v0_4_4.py
```

## Claim Ceiling

Allowed after this import:

```text
MARP-GEOLEAN-BASE-009 / PLAN-009 / ACCEPTANCE-009 are installed as the active v0.4.4 Guardian authority set.
Implementation may start from WP00/WP01 under the v0.4.4 plan.
```

Not allowed after this import:

```text
V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY
ACCEPTANCE_COMPLETE
SOURCE_FAITHFUL
PRODUCTION_SAFE
```

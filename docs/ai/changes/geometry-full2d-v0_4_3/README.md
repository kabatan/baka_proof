---
title: "GeometryFull2D v0.4.3 Guardian Track"
status: "SUPERSEDED_BY_MARP-GEOLEAN-BASE-009"
base_spec: "MARP-GEOLEAN-BASE-008"
plan: "MARP-GEOLEAN-PLAN-008"
acceptance: "MARP-GEOLEAN-ACCEPTANCE-008"
created: "2026-06-15"
---

# GeometryFull2D v0.4.3 Guardian Track

This directory contains the historical Guardian authority set for the v0.4.3 real pipeline recovery track.

The v0.4.3 integrated bundle replaces the prior v0.4.3 / v0.4.3A split. Anti-gaming hardening is incorporated directly into this authority set; there is no separate addendum to install.

## Authority Files

- `BASE_SPEC.md` — correctness authority for `MARP-GEOLEAN-BASE-008`.
- `PLAN.md` — execution contract for `MARP-GEOLEAN-PLAN-008`.
- `ACCEPTANCE.md` — acceptance authority for `MARP-GEOLEAN-ACCEPTANCE-008`.
- `REAL_PIPELINE_INVARIANTS.md` — real-pipeline and anti-template invariants.
- `REFACTOR_DIRECTIVE.md` — required release-path rewrite and quarantine rules.
- `SOURCE_MAP.md` — traceability from v0.4.2 failure evidence to v0.4.3 requirements.
- `ACTIVE_CONTEXT.md` — change-local navigation seed.
- `CODEX_HANDOFF.md` — implementation handoff.

## Evidence and Debt

- `evidence/v0_4_3_bundle_import.md` — import evidence, hash verification, installed mapping, and claim ceiling.
- `evidence/v0_4_3_release_blocker_report.md` — historical strict verification blocker report from before final remediation.
- `evidence/release_acceptance_report.json` — final v0.4.3 release acceptance evidence.
- `CLOSURE.md` — final closure claim and non-claims.
- `evidence/bundle_sha256sums.txt` — original bundle hash manifest.
- `debt/debt_ledger.jsonl` — v0.4.3 debt ledger. Open entries block closure.

## First Command

```bash
python scripts/check_active_guardian_spec_v0_4_3.py
```

## Claim Ceiling

Final release acceptance passed for the scoped v0.4.3 claim `V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY`. This is historical evidence only and is not active v0.4.4 release authority. It does not mean the pipeline is natural-language source-faithful, TongGeometry model-backed, production-safe, solver-causal under v0.4.4, or correct outside `GeometryFull2DTarget:1.0.0`.

<!--
Generated for kabatan/baka_proof Guardian/Codex handoff.
Created: 2026-06-14
Status: SUPERSEDED_BY_MARP-GEOLEAN-BASE-008
-->
---
title: "Superseded Context — GeometryFull2D v0.4.2"
status: "SUPERSEDED_BY_MARP-GEOLEAN-BASE-008"
created: "2026-06-14"
---

# Superseded Context — GeometryFull2D v0.4.2

This file is retained only as historical evidence and as a regression source for v0.4.3. It is not active release authority.

Current objective:

```text
Superseded objective: V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY.
```

Superseded spec set:

```text
docs/ai/changes/geometry-full2d-v0_4_2/BASE_SPEC.md
docs/ai/changes/geometry-full2d-v0_4_2/PLAN.md
docs/ai/changes/geometry-full2d-v0_4_2/ACCEPTANCE.md
docs/ai/changes/geometry-full2d-v0_4_2/ENGINE_CONTRACTS.md
docs/ai/changes/geometry-full2d-v0_4_2/BLOCKER_AND_DEBT_POLICY.md
docs/ai/changes/geometry-full2d-v0_4_2/REFACTOR_DIRECTIVE.md
```

The active spec set is now `MARP-GEOLEAN-BASE-008` / `MARP-GEOLEAN-PLAN-008` / `MARP-GEOLEAN-ACCEPTANCE-008` under `docs/ai/changes/geometry-full2d-v0_4_3/`.

Execution rule:

```text
Codex must not stop for ReleaseBlockers or WorkDebt.
Codex must stop only for HardBlockers HB-01..HB-09.
Codex must not weaken requirements.
Codex must continue next_unblocked_work_packages from progress acceptance.
```

Historical claim ceiling for v0.4.2:

```text
No v0.4.2 completion claim.
Implementation in progress only.
```

Current task:

```text
WP-20 — Corpus and final release acceptance closure
```

Progress acceptance:

```text
hard_blockers=[]
status=progress_ok_with_debt
completed_work_packages include WP-00, WP-01, WP-02, WP-03, WP-04, WP-05, WP-06, WP-07, WP-08, WP-09, WP-10, WP-11, WP-12, WP-13, WP-14, and WP-15
next_unblocked_work_packages include WP-20
release_acceptance status is blocked on WP-20 metrics because the frozen corpus has no solver-backed certificate/final-verify/proof-region artifacts to support artifact-derived final theorem counts
```

TongGeometry:

```text
Not release-critical. Do not block v0.4.2 on TongGeometry trained checkpoint artifacts.
```

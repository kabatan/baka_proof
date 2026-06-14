---
title: Change Index — geometry x Lean v0.3 full rebase
change_id: geometry-lean-v0_3-full-rebase
version: v0.3-full-rebase+v0.3A+v0.3B-patch
status: USER_APPROVED_V0_3B_PATCH_INSTALLED_T48_READY
created: 2026-06-13
purpose: Index the Guardian document set for the full v0.3 experiment-ready rebase track.
authority: Navigation only; individual documents declare their own authority.
---

# Change Index — geometry x Lean v0.3 full rebase

## Purpose

This change prepares and executes the Guardian track for:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
```

It supersedes the previous fixture-level and limited v0.3A recovery tracks only after Guardian admission and user implementation approval are recorded. It is now amended by the v0.3A and v0.3B patch documents under `patches/`.

## Primary Documents

- `BASE_SPEC.md` — correctness authority for `MARP-GEOLEAN-BASE-004`, amended by `patches/BASE_SPEC_PATCH_v0_3A.md` and `patches/BASE_SPEC_PATCH_v0_3B.md`.
- `PLAN.md` — execution contract for `MARP-GEOLEAN-PLAN-004`, amended by `patches/PLAN_PATCH_v0_3A.md` and `patches/PLAN_PATCH_v0_3B.md`.
- `patches/BASE_SPEC_PATCH_v0_3A.md` — active Base Spec amendment `MARP-GEOLEAN-BASE-004A`.
- `patches/PLAN_PATCH_v0_3A.md` — active Plan amendment `MARP-GEOLEAN-PLAN-004A`.
- `patches/ACCEPTANCE_PATCH_v0_3A.md` — active release acceptance amendment.
- `patches/BASE_SPEC_PATCH_v0_3B.md` — active Base Spec amendment `MARP-GEOLEAN-BASE-004B`.
- `patches/PLAN_PATCH_v0_3B.md` — active Plan amendment `MARP-GEOLEAN-PLAN-004B`.
- `patches/ACCEPTANCE_PATCH_v0_3B.md` — active release acceptance amendment for solver-backed proof repair.
- `patches/SOURCE_MAP_PATCH_v0_3B.md` — traceability aid for the solver-backed proof-repair gap.
- `patches/REPO_AUDIT_FOCUS_v0_3B.md` — focused audit aid for T48.
- `SOURCE_MAP.md` — source-to-requirement traceability aid.
- `REFACTOR_DIRECTIVE.md` — repository cleanup directive for T01/T02 and later implementation work.
- `ACCEPTANCE_MATRIX.md` — concise evidence and command matrix for final acceptance.
- `CODEX_HANDOFF_PROMPT.md` — non-authoritative handoff prompt for future Codex runs.

## Evidence

- `evidence/bundle_sha256sums.txt` — hashes supplied with the research-agent bundle.
- `evidence/bundle_import_preparation.md` — local import and hash-verification record.
- `evidence/v0_3a_patch_import.md` — user-approved v0.3A patch import record.
- `evidence/v0_3a_deviation_audit.md` — current deviation audit for T38.
- `evidence/v0_3b_patch_import.md` — user-approved v0.3B patch import record.

## Current Gate

Current gate: T48 implementation under `MARP-GEOLEAN-BASE-004B` / `MARP-GEOLEAN-PLAN-004B`.

The v0.3A closure passed for core experiment readiness. The v0.3B patch is installed and user-approved; solver-backed proof repair is not yet implemented.

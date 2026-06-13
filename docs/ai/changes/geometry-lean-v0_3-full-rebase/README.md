---
title: Change Index — geometry x Lean v0.3 full rebase
change_id: geometry-lean-v0_3-full-rebase
version: v0.3-full-rebase+v0.3A-patch
status: USER_APPROVED_V0_3A_PATCH_INSTALLED_T39_READY
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

It supersedes the previous fixture-level and limited v0.3A recovery tracks only after Guardian admission and user implementation approval are recorded. It is now amended by the v0.3A patch documents under `patches/`.

## Primary Documents

- `BASE_SPEC.md` — correctness authority for `MARP-GEOLEAN-BASE-004`, amended by `patches/BASE_SPEC_PATCH_v0_3A.md`.
- `PLAN.md` — execution contract for `MARP-GEOLEAN-PLAN-004`, amended by `patches/PLAN_PATCH_v0_3A.md`.
- `patches/BASE_SPEC_PATCH_v0_3A.md` — active Base Spec amendment `MARP-GEOLEAN-BASE-004A`.
- `patches/PLAN_PATCH_v0_3A.md` — active Plan amendment `MARP-GEOLEAN-PLAN-004A`.
- `patches/ACCEPTANCE_PATCH_v0_3A.md` — active release acceptance amendment.
- `SOURCE_MAP.md` — source-to-requirement traceability aid.
- `REFACTOR_DIRECTIVE.md` — repository cleanup directive for T01/T02 and later implementation work.
- `ACCEPTANCE_MATRIX.md` — concise evidence and command matrix for final acceptance.
- `CODEX_HANDOFF_PROMPT.md` — non-authoritative handoff prompt for future Codex runs.

## Evidence

- `evidence/bundle_sha256sums.txt` — hashes supplied with the research-agent bundle.
- `evidence/bundle_import_preparation.md` — local import and hash-verification record.
- `evidence/v0_3a_patch_import.md` — user-approved v0.3A patch import record.
- `evidence/v0_3a_deviation_audit.md` — current deviation audit for T38.

## Current Gate

Current gate: T39 implementation under `MARP-GEOLEAN-BASE-004A` / `MARP-GEOLEAN-PLAN-004A`.

The patch is installed and user-approved. The repo is not yet v0.3A complete.

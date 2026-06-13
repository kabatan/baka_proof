---
title: Change Index — geometry x Lean v0.3 full rebase
change_id: geometry-lean-v0_3-full-rebase
version: v0.3-full-rebase
status: GUARDIAN_BOUNDARY_ADMITTED_PENDING_IMPLEMENTATION_APPROVAL
created: 2026-06-13
purpose: Index the Guardian document set for the full v0.3 experiment-ready rebase track.
authority: Navigation only; individual documents declare their own authority.
---

# Change Index — geometry x Lean v0.3 full rebase

## Purpose

This change prepares a new Guardian track for:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
```

It supersedes the previous fixture-level and limited v0.3A recovery tracks only after Guardian admission and user implementation approval are recorded.

## Primary Documents

- `BASE_SPEC.md` — candidate correctness authority for `MARP-GEOLEAN-BASE-004`.
- `PLAN.md` — candidate execution contract for `MARP-GEOLEAN-PLAN-004`.
- `SOURCE_MAP.md` — source-to-requirement traceability aid.
- `REFACTOR_DIRECTIVE.md` — repository cleanup directive for T01/T02 and later implementation work.
- `ACCEPTANCE_MATRIX.md` — concise evidence and command matrix for final acceptance.
- `CODEX_HANDOFF_PROMPT.md` — non-authoritative handoff prompt for future Codex runs.

## Evidence

- `evidence/bundle_sha256sums.txt` — hashes supplied with the research-agent bundle.
- `evidence/bundle_import_preparation.md` — local import and hash-verification record.

## Current Gate

Current gate: explicit user implementation approval for `MARP-GEOLEAN-BASE-004` and `MARP-GEOLEAN-PLAN-004`.

Implementation code changes are blocked until explicit user implementation approval is recorded.

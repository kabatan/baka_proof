---
title: Bundle Import Preparation — geometry x Lean v0.3 full rebase
date: 2026-06-13
status: IMPORTED_FOR_GUARDIAN_REVIEW
authority: Evidence record only; does not grant implementation permission.
---

# Bundle Import Preparation

## Source

User-provided bundle:

```text
C:/Users/bakat/Downloads/guardian_geometry_lean_v0_3_full_rebase_bundle.zip
```

Temporary extraction path used for inspection:

```text
.tmp/v03_full_rebase_bundle/
```

## Imported Canonical Candidate Paths

- `docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md`
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md`
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/SOURCE_MAP.md`
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/REFACTOR_DIRECTIVE.md`
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/ACCEPTANCE_MATRIX.md`
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/CODEX_HANDOFF_PROMPT.md`
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/bundle_sha256sums.txt`

## Hash Verification

The imported Markdown files matched the bundle-provided SHA-256 sums:

```text
8a831e5da2735048e7c13cfdca98bedc9f8da9c176278f1c69ca2e8af2f911f5  geometry_lean_guardian_ACCEPTANCE_MATRIX_v0_3_full_rebase.md
8bf3b8fb451f2e7e1bcefd75fee674766f27196be6cb937411c110c5dd7722fe  geometry_lean_guardian_ACTIVE_CONTEXT_seed_v0_3_full_rebase.md
3c4b829b4b56733bd968c7cf6debab558e2db6bbd52ef898fa17923c1835f6dd  geometry_lean_guardian_BASE_SPEC_v0_3_full_rebase.md
b5bc1fbdfeda544ee085618a76b71670dd9eca32e92a1b270ceac77765991e76  geometry_lean_guardian_CODEX_HANDOFF_PROMPT_v0_3_full_rebase.md
76637525d070259501b4cc677ab1d067d091777037974c14755ea2df5475b044  geometry_lean_guardian_PLAN_v0_3_full_rebase.md
88861234a0b63ec87b099998e79bccf817f3e468a4af010c3c17f8366f0450e6  geometry_lean_guardian_REFACTOR_DIRECTIVE_v0_3_full_rebase.md
72019513cb00658d6fa44356df7f04348ce48bd4dcd9fe7609e653159ff51803  geometry_lean_guardian_SOURCE_MAP_v0_3_full_rebase.md
```

## Permission State

The user requested import and preparation of the revised Guardian drafts.

This evidence does not record approval to execute implementation tasks under `MARP-GEOLEAN-PLAN-004`. Implementation must not proceed until a dedicated `user_approval.md` is created under this evidence directory.

## Boundary Review Remediation

Initial Guardian boundary review returned `FAIL_FIXABLE`.

Remediations applied:

- Replaced undefined Plan supports references:
  - `R-GUARD implicit` -> `R-TEST-003` approval/release-blocker gate wording.
  - `R-RUN implicit` -> `R-BASE-002`, `R-SCHEMA-006`, `R-EVAL-*`.
  - `R-CLAIM` -> `R-TEST-003`, Base Spec Section 20, and Base Spec Section 21.
- Removed absent background filenames from the source-fidelity authority list in `SOURCE_MAP.md`.
- Clarified that `R-ENV-001` grants dependency-bootstrap authority only after Guardian admission and explicit user implementation approval.

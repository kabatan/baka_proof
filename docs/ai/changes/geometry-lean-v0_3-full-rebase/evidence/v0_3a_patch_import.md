---
title: v0.3A patch import evidence
status: USER_APPROVED_PATCH_IMPORT
created: 2026-06-13
purpose: Record import of the research-agent v0.3A patch bundle into the active full-rebase Guardian track.
authority: User approval and import evidence only; the installed patch files define the amended requirements.
---

# v0.3A Patch Import Evidence

## User Request

The user supplied:

```text
C:/Users/bakat/Downloads/guardian_geometry_lean_v0_3A_patch_bundle.zip
```

and asked Codex to introduce it into the current Guardian environment so work
toward complete v0.3 implementation can resume.

## Installed Patch Documents

Installed under:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/
```

Installed files:

```text
BASE_SPEC_PATCH_v0_3A.md
PLAN_PATCH_v0_3A.md
ACCEPTANCE_PATCH_v0_3A.md
CODEX_HANDOFF_PATCH_v0_3A.md
REPO_AUDIT_SUMMARY_v0_3A.md
v0_3A_patch_source_sha256sums.txt
```

The installed patch documents are marked as user-approved active amendments
where appropriate. The source audit summary remains evidence input only.

## Source Bundle Hashes

The bundle-provided SHA-256 file listed:

```text
5f734fea38c0b1151e9c3d858cd876e568d1edb0de4200f34b100d30a1bae753  geometry_lean_guardian_ACCEPTANCE_PATCH_v0_3A.md
caaf3f1868a5668acde85e353499408ae56ef217a5621ac4a60f4e640a6c8bb7  geometry_lean_guardian_BASE_SPEC_PATCH_v0_3A.md
b79e41db4d59a331bcb17c668c89a1db52b9dbc99080c551bddb23ea6c0c65ec  geometry_lean_guardian_CODEX_HANDOFF_PATCH_v0_3A.md
a394bbc67011abc085c1f0a07a5543bbd7ca1642d02b0ef8fc4bc9d19b5ab4e4  geometry_lean_guardian_PLAN_PATCH_v0_3A.md
4fab76d2aadc43dc07ca3acf360760a11b2cc5fb737ff73e1bd11cf50ca221d4  geometry_lean_guardian_REPO_AUDIT_SUMMARY_v0_3A.md
```

## Authority Notes

`BASE_SPEC_PATCH_v0_3A.md` amends `MARP-GEOLEAN-BASE-004`; it does not replace
the full Base Spec. It supersedes only explicitly listed patched R-IDs, release
blockers, and claim profiles.

`PLAN_PATCH_v0_3A.md` amends `MARP-GEOLEAN-PLAN-004`; it adds T38-T46 hardening
work and modifies T25/T34/T36/T37 acceptance behavior.

No completion claim is made by this import.

## Reviewer Status

No sub-agent reviewer was invoked in this import turn because the current tool
contract only permits spawning sub-agents when the user explicitly asks for
delegation or parallel agent work. A Guardian boundary/spec review remains
required before any final strong completion claim.

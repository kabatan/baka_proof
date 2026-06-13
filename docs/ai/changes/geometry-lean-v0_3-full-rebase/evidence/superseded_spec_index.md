---
title: T02 Evidence — Superseded Spec Index
date: 2026-06-13
task: T02
status: COMPLETED
authority: Evidence record only; superseded files are not implementation authority.
---

# T02 Evidence — Superseded Spec Index

## Deleted Root-Level Guardian Drafts

The following root-level files were deleted after their hashes were recorded in `repo_audit.md`:

| Deleted root file | SHA-256 |
|---|---|
| `geometry_lean_guardian_ACTIVE_CONTEXT_draft_v0_2.md` | `f9ccff0803d29e35b2ee4459eeb70fbda9033cf235063cd1b3e40bdbd41995fe` |
| `geometry_lean_guardian_BASE_SPEC_draft_v0_2.md` | `9fcba98d477529ba7172ec29b04e412ec75cb110d8a21b3c822e71ded9506994` |
| `geometry_lean_guardian_PLAN_draft_v0_2.md` | `0a43e3a0de77365b848ad4eac8692b560e3032f1599a207fdf70e26c9e763a7f` |
| `geometry_lean_guardian_RESOURCE_POLICY_TEMPLATE_draft_v0_2.md` | `32b0536f5cb443e5960f44f43e43c44dcff6fd803d18042aef318863ff07dfc4` |
| `geometry_lean_guardian_SOURCE_MAP_draft_v0_2.md` | `7fc35b740dd33d2664a59ac0f14b42501f2aa502f79f1fb2cc9429e6708c4124` |
| `geometry_lean_guardian_v0_2_sha256sums.txt` | `6dfaae51d98d6cb0e8ea95acdbe483a51b3753373db73aa82ab4e38b027e5b49` |

## Moved Source Architecture Document

The root-level v0.3 source architecture document was moved from:

```text
geometry_lean_pipeline_plan_v0_3.md
```

to:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/source/geometry_lean_pipeline_plan_v0_3.md
```

Original SHA-256:

```text
c9086d6d9d7de4b809c3935a26d8ced0a429085097954760982183e117eca5e7
```

The moved copy has a non-authoritative source header:

```text
authority: NON-AUTHORITATIVE SOURCE
superseded_by: MARP-GEOLEAN-BASE-004
```

## Verification

```text
python scripts/check_old_specs_removed.py
```

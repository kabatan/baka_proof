---
title: v0.3B solver-backed proof-repair patch import evidence
status: USER_APPROVED_PATCH_IMPORT
created: 2026-06-14
purpose: Record import of the planning-agent v0.3B solver-backed proof-repair patch bundle into the active full-rebase Guardian track.
authority: User approval and import evidence only; the installed patch files define the amended requirements.
---

# v0.3B Patch Import Evidence

## User Request

The user supplied:

```text
C:/Users/bakat/Downloads/guardian_geometry_lean_v0_3B_solver_backed_patch_bundle.zip
```

and asked Codex to introduce the revised Base Spec, Plan, and related Guardian
documents into the current workspace so work toward complete v0.3 implementation
can resume.

## Bundle Verification

The bundle was expanded into a temporary inspection directory and its provided
SHA-256 checksums were verified before installation.

Verification result:

```text
sha256 check passed
```

Bundle-provided hashes:

```text
3c155209c4517acf6074ac174e411a98f8758579f6eaf38a5df088562a4ae32d  geometry_lean_guardian_BASE_SPEC_PATCH_v0_3B_solver_backed_proof_repair.md
568092ed5fc023cb97b043bc7ade3628096a1eeff5bb2a735a2ab40a458376a7  geometry_lean_guardian_PLAN_PATCH_v0_3B_solver_backed_proof_repair.md
ff8abd441fad0ffd651181d4e9620374d4d6d6662aea3eb76c483b9805e791c1  geometry_lean_guardian_ACCEPTANCE_PATCH_v0_3B_solver_backed_proof_repair.md
8ef7311a275dc7308c15783b13c7b53e14a49c7d4e8a199f7605374fdb5bbc55  geometry_lean_guardian_REPO_AUDIT_FOCUS_v0_3B_solver_backed_proof_repair.md
9cf1de2d92d23ed1d2e103343866f02668a15d3034e71f745bcf6802589b4438  geometry_lean_guardian_SOURCE_MAP_PATCH_v0_3B_solver_backed_proof_repair.md
4cf8c14fca50157192f2997a91abf3dc1129686a0ed877d6faaded455562a919  geometry_lean_guardian_ACTIVE_CONTEXT_PATCH_seed_v0_3B_solver_backed_proof_repair.md
6e0391edd1ff9c7b60c999408f4f14070061d2fe31a8048ac76c6cf63ff397be  geometry_lean_guardian_CODEX_HANDOFF_PATCH_v0_3B_solver_backed_proof_repair.md
```

## Installed Patch Documents

Installed under:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/
```

Installed files:

```text
BASE_SPEC_PATCH_v0_3B.md
PLAN_PATCH_v0_3B.md
ACCEPTANCE_PATCH_v0_3B.md
CODEX_HANDOFF_PATCH_v0_3B.md
REPO_AUDIT_FOCUS_v0_3B.md
SOURCE_MAP_PATCH_v0_3B.md
ACTIVE_CONTEXT_PATCH_seed_v0_3B.md
v0_3B_patch_source_sha256sums.txt
```

The Base Spec, Plan, and Acceptance patch documents are marked as active
user-approved amendments. The handoff, source-map patch, and audit-focus files
are navigation or evidence aids only and cannot override the Base Spec patches.

## Source-to-Installed Transformation

The bundle source hashes above remain the record of the planning-agent source
files. The installed files intentionally differ for the files that needed local
Guardian status metadata after user approval.

Authorized local transformations:

```text
1. Rename bundle filenames to the active repository patch filenames.
2. For BASE_SPEC_PATCH_v0_3B.md, PLAN_PATCH_v0_3B.md, and
   ACCEPTANCE_PATCH_v0_3B.md:
   - change status from DRAFT_FOR_USER_REVIEW to USER_APPROVED_ACTIVE_AMENDMENT;
   - add installed: 2026-06-14;
   - add approval_evidence pointing to this import record.
3. For SOURCE_MAP_PATCH_v0_3B.md:
   - change status to USER_APPROVED_TRACEABILITY_PATCH;
   - add installed: 2026-06-14;
   - add non-authoritative traceability authority metadata.
4. For REPO_AUDIT_FOCUS_v0_3B.md:
   - change status to ACTIVE_AUDIT_FOCUS;
   - add installed: 2026-06-14;
   - add audit-guidance-only authority metadata.
5. CODEX_HANDOFF_PATCH_v0_3B.md and ACTIVE_CONTEXT_PATCH_seed_v0_3B.md were
   installed without content transformation.
```

Installed artifact hashes are recorded in:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3b_installed_patch_sha256sums.txt
```

Installed hashes:

```text
27c7bad9a7b74e0050777e6313079e5f61492b51ba1823608f6e076015c0c42d  BASE_SPEC_PATCH_v0_3B.md
84f7914e31e84fd0e54e4bbce021b0038134c4ae6c56e11e0897981b9062ac73  PLAN_PATCH_v0_3B.md
958992baee68cebb9395318135717b83a04897f76943dec9ed84bcf2430125d9  ACCEPTANCE_PATCH_v0_3B.md
6e0391edd1ff9c7b60c999408f4f14070061d2fe31a8048ac76c6cf63ff397be  CODEX_HANDOFF_PATCH_v0_3B.md
d399fa1a2b0e452854d15422a6968e4e23d47317ed26f536457a9a60f52cb941  REPO_AUDIT_FOCUS_v0_3B.md
c7639ea01e7d5a55ce61d866dbdb82e114b8b6b31626f4ca936b1be14ab87fb5  SOURCE_MAP_PATCH_v0_3B.md
4cf8c14fca50157192f2997a91abf3dc1129686a0ed877d6faaded455562a919  ACTIVE_CONTEXT_PATCH_seed_v0_3B.md
6040f1597e3b1696e1145c6af4d5d0f98da2dcaa652aa0ebfb8b42cf84f53a58  v0_3B_patch_source_sha256sums.txt
```

## Authority Notes

`BASE_SPEC_PATCH_v0_3B.md` amends `MARP-GEOLEAN-BASE-004` as already amended by
`MARP-GEOLEAN-BASE-004A`. It supersedes only the clauses explicitly listed in
the patch.

`PLAN_PATCH_v0_3B.md` amends `MARP-GEOLEAN-PLAN-004` as already amended by
`MARP-GEOLEAN-PLAN-004A`. It adds T47-T64 solver-backed proof-repair work.

`ACCEPTANCE_PATCH_v0_3B.md` adds release blockers 35-47 and introduces:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
```

No v0.3B completion claim is made by this import.

## Resume State

The prior v0.3A closure remains evidence for:

```text
core_experiment_ready_status = passed
tonggeometry_model_backed_status = blocked
```

After v0.3B patch installation, the intended complete v0.3 claim is not final
until solver-backed proof repair passes the new release acceptance path:

```text
configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml
```

Next implementation task:

```text
T48 — Audit current proof-repair gap
```

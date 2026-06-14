---
title: v0.4.2 GeometryFull2D bundle import evidence
status: USER_APPROVED_IMPORT
created: 2026-06-15
purpose: Record import of the research-agent v0.4.2 governed Full2D Guardian bundle into the active Guardian environment.
authority: User approval and import evidence only; the installed Base Spec, Plan, Acceptance, and contract documents define requirements.
---

# v0.4.2 Bundle Import Evidence

## User Request

The user supplied:

```text
C:/Users/bakat/Downloads/guardian_geometry_lean_v0_4_2_governed_full2d_bundle.zip
```

and asked Codex to introduce the revised Base Spec, Plan, and related Guardian documents into the current workspace so work toward completing the pipeline can begin.

## Bundle Verification

Bundle SHA-256:

```text
CC771F50B6A32A14E2D2DF87DB6B6C7223980D09250F74212014EBEBA7A6B727
```

The bundle was expanded into a temporary inspection directory and its provided SHA-256 checksums were verified before installation.

Verification result:

```text
sha256 check passed
```

Bundle-provided hashes are recorded in:

```text
docs/ai/changes/geometry-full2d-v0_4_2/evidence/bundle_sha256sums.txt
```

## Installed Documents

Installed under:

```text
docs/ai/changes/geometry-full2d-v0_4_2/
```

Installed files:

```text
BASE_SPEC.md
PLAN.md
ACCEPTANCE.md
ENGINE_CONTRACTS.md
BLOCKER_AND_DEBT_POLICY.md
REFACTOR_DIRECTIVE.md
SOURCE_MAP.md
ACTIVE_CONTEXT.md
CODEX_HANDOFF.md
README.md
debt/debt_ledger.jsonl
evidence/bundle_sha256sums.txt
evidence/installed_sha256sums.txt
evidence/repo_audit.md
```

Installed artifact hashes after local status installation are recorded in:

```text
docs/ai/changes/geometry-full2d-v0_4_2/evidence/installed_sha256sums.txt
```

## Source-to-Installed Transformation

The bundle source hashes remain the record of the research-agent source files. The installed files intentionally differ where local Guardian status metadata had to reflect this user-approved import.

Authorized local transformations:

```text
1. Rename bundle filenames to the active repository filenames.
2. Change bundle document status from DRAFT_FOR_USER_APPROVAL to USER_APPROVED_ACTIVE.
3. Initialize debt/debt_ledger.jsonl as an empty debt ledger.
4. Add README.md, this import record, and repo_audit.md as local Guardian navigation/evidence files.
5. Update docs/ai/ACTIVE_CONTEXT.md and docs/ai/INDEX.md to make v0.4.2 the active Guardian track.
```

## Authority Notes

`MARP-GEOLEAN-BASE-007` supersedes the previous v0.3-family Base Specs for new release work. It does not retroactively delete or reinterpret older evidence.

The only final release claim admitted by the installed Base Spec is:

```text
V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY
```

No completion claim is made by this import.

## Resume State

Next implementation task:

```text
WP-00 — Install v0.4.2 authority and audit repo
```

The import did not physically move older v0.3-family documentation because current scripts and tests still reference those evidence paths. That archive/refactor work must happen inside WP-00 together with reference repair and active-spec checking.

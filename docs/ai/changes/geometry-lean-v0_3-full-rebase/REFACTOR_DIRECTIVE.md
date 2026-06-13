---
title: "Repository Refactor Directive — geometry × Lean v0.3 full rebase"
version: "v0.3-full-rebase"
spec_id: "MARP-GEOLEAN-BASE-004"
plan_id: "MARP-GEOLEAN-PLAN-004"
status: "GUARDIAN_BOUNDARY_ADMITTED_PENDING_IMPLEMENTATION_APPROVAL"
created: "2026-06-12"
---

# Repository Refactor Directive

This directive tells Codex how to bring `kabatan/baka_proof` back to a simple, coherent state before implementing the full v0.3 system.

## 1. Main decision

Do not preserve the current drifted implementation for compatibility. The repository must be refactored toward the approved Base Spec.

The following are not acceptable reasons to keep drift:

- old code currently passes tests;
- old root specs are convenient for reference;
- fixture adapters make smoke tests easier;
- local toy Lean definitions compile;
- AgentC/D terminology was already implemented;
- provider-specific branches already exist in Base.

## 2. Delete from root

Delete these root files after their hashes are recorded:

```text
geometry_lean_guardian_ACTIVE_CONTEXT_draft_v0_2.md
geometry_lean_guardian_BASE_SPEC_draft_v0_2.md
geometry_lean_guardian_PLAN_draft_v0_2.md
geometry_lean_guardian_RESOURCE_POLICY_TEMPLATE_draft_v0_2.md
geometry_lean_guardian_SOURCE_MAP_draft_v0_2.md
geometry_lean_guardian_v0_2_sha256sums.txt
```

Move or delete:

```text
geometry_lean_pipeline_plan_v0_3.md
```

If moved, add a non-authoritative header and place it under:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/source/
```

## 3. Canonical authority paths

Use only:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/SOURCE_MAP.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/REFACTOR_DIRECTIVE.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/ACCEPTANCE_MATRIX.md
docs/ai/ACTIVE_CONTEXT.md
```

## 4. Package layout cleanup

Canonical Python package:

```text
src/math_auto_research/**
```

If top-level `math_auto_research/**` exists:

1. compare with `src/math_auto_research/**`;
2. move any unique non-generated files into `src/math_auto_research/**`;
3. delete duplicate top-level package;
4. ensure imports resolve from `src/`;
5. update tests and pyproject.

## 5. Production/fixture separation

Production provider files:

```text
plugins/geometry_synthetic/providers/newclid_adapter.py
plugins/geometry_synthetic/providers/genesisgeo_adapter.py
plugins/geometry_synthetic/providers/tonggeometry_adapter.py
```

Fixture providers may exist only under:

```text
tests/fixtures/**
plugins/geometry_synthetic/tests/fixtures/**
```

Release configs must never select fixture providers.

## 6. Forbidden runtime concepts

Remove core runtime classes, modes, enums, CLI options, config keys, and benchmark run modes containing:

```text
AgentC
AgentD
mode_a
mode_b
mode_c
mode_d
agent_c
agent_d
```

Allowed only in source-map commentary or retired evidence describing superseded documents.

## 7. Forbidden Base dependencies

Base code must not contain these strings except in tests that enforce rejection or in non-authoritative evidence files:

```text
Newclid
GenesisGeo
TongGeometry
LeanGeoSubsetV1
geometry_synthetic
collinear
parallel
perpendicular
concyclic
equal_angle
equal_length
midpoint
```

## 8. Required guard scripts

Implement and run:

```bash
python scripts/check_old_specs_removed.py
python scripts/check_package_layout.py
python scripts/check_domain_contamination.py
python scripts/check_no_loose_options.py
python scripts/check_model_hardcode.py
python scripts/check_resource_bypass.py
python scripts/check_no_fixture_release.py
```

## 9. Refactor completion evidence

Codex must create:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/repo_audit.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/repo_file_inventory.json
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/superseded_spec_index.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/refactor_summary.md
```

`refactor_summary.md` must list deleted files, moved files, package consolidation decisions, and remaining blockers.

# RC-1 Proof-State Schema Files Fix Evidence

Scope: Follow-up fix after the third RC-1 Guardian boundary review.

## Fixes

- Added exact code-side `R-SCHEMA-003` Pydantic records:
  - `ObligationNode`
  - `DerivationNode`
- Added and committed individual proof-state JSON Schema files for every proof-state model:
  - `schemas/proof_state/obligation.schema.json`
  - `schemas/proof_state/obligation_node.schema.json`
  - `schemas/proof_state/derivation.schema.json`
  - `schemas/proof_state/derivation_node.schema.json`
  - `schemas/proof_state/evidence_ref.schema.json`
  - `schemas/proof_state/graph_patch.schema.json`
  - `schemas/proof_state/graph_patch_commit_result.schema.json`
  - `schemas/proof_state/dag_snapshot.schema.json`
  - `schemas/proof_state/state_reader_summary.schema.json`
- Added `scripts/export_proof_state_schemas.py` to regenerate the individual schema files from the Pydantic models.
- Strengthened schema tests so they require:
  - exact `ObligationNode` and `DerivationNode` model names;
  - every proof-state Pydantic model's `schema_path` to exist;
  - each schema file to include `$id`.

## Commands

```powershell
python scripts\export_proof_state_schemas.py
```

Result:

```text
schemas/proof_state/obligation.schema.json
schemas/proof_state/obligation_node.schema.json
schemas/proof_state/derivation.schema.json
schemas/proof_state/derivation_node.schema.json
schemas/proof_state/evidence_ref.schema.json
schemas/proof_state/graph_patch.schema.json
schemas/proof_state/graph_patch_commit_result.schema.json
schemas/proof_state/dag_snapshot.schema.json
schemas/proof_state/state_reader_summary.schema.json
```

```powershell
make test-unit TEST_FILTER=schema
```

Result:

```text
Ran 9 tests
OK
```

```powershell
make test-unit TEST_FILTER=proof_state
```

Result:

```text
Ran 10 tests
OK
```

```powershell
python scripts\check_domain_contamination.py
```

Result:

```text
domain contamination check passed
```

## Claim

The specific missing individual proof-state schema files and exact code-side `R-SCHEMA-003` record names reported by the third RC-1 review are fixed. RC-1 PASS is still not claimed until follow-up Guardian review passes.

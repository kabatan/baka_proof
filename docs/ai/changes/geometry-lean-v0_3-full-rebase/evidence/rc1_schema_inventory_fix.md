# RC-1 Schema Inventory Fix Evidence

Scope: Follow-up fix after the second RC-1 Guardian boundary review.

## Fixes

- Updated `schemas/proof_state/public_contracts.schema.json` to include all `R-SCHEMA-003` proof-state records:
  - `ObligationNode`
  - `DerivationNode`
  - `EvidenceRef`
  - `GraphPatch`
  - `GraphPatchCommitResult`
  - `DAGSnapshot`
  - `StateReaderSummary`
- Updated `schemas/v03_contract_inventory.json` to include:
  - `DAGSnapshot`
  - `StateReaderSummary`
- Aligned `GraphPatchCommitResult` schema metadata with the Pydantic model:
  - uses `committed_obligation_ids`
  - uses `committed_derivation_ids`
  - uses `committed_evidence_ids`
  - removes stale `blocker_summary` and `closed_obligation_ids` requirements.
- Strengthened schema tests to catch missing proof-state inventory entries and stale commit-result fields.

## Commands

```powershell
make test-unit TEST_FILTER=schema
```

Result:

```text
Ran 8 tests
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

The specific schema/inventory mismatch reported by the second RC-1 review is fixed. RC-1 PASS is still not claimed until follow-up Guardian review passes.

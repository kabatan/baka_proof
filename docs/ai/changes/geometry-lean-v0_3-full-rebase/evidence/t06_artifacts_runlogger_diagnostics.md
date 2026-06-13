# T06 Evidence — ArtifactStore, RunLogger, DiagnosticBundle

Task: `T06 — ArtifactStore, RunLogger, DiagnosticBundle`

Supports:
- `R-BASE-001`
- `R-BASE-002`
- `R-BASE-003`
- `R-BASE-004`

## Changes

- Extended `ArtifactStore` with:
  - `put_bytes(data, kind, metadata)`;
  - Pydantic/dict JSON artifact storage through `put_json(obj, kind, metadata)`;
  - backward-compatible `put_json(name, payload)`;
  - `get(ref)`;
  - content-hash verification.
- Moved `ArtifactRef`, `RunRecord`, `DiagnosticBundle`, and `TrustReport` onto the Pydantic-backed schema layer.
- Added Base Spec diagnostic fields:
  - `diagnostic_id`
  - `kind`
  - `blame_layer`
  - `severity`
  - `reason_codes`
  - `repair_options`
  - `evidence_refs`
- Added TrustReport result/proof-use vocabularies and a validation rule that `final_theorem` proof-use can only be represented with `lean_theorem` result level.
- Added focused tests for artifact storage, run logging, diagnostic records, and trust records.

## Commands

```powershell
make test-unit TEST_FILTER=artifact
```

Result:

```text
Ran 4 tests
OK
```

```powershell
make test-unit TEST_FILTER=run_logger
```

Result:

```text
Ran 4 tests
OK
```

```powershell
make test-unit TEST_FILTER=diagnostic
```

Result:

```text
Ran 2 tests
OK
```

```powershell
make test-unit TEST_FILTER=trust
```

Result:

```text
Ran 3 tests
OK
```

## Claim

T06 acceptance is satisfied for Base artifact storage, run record linkage, diagnostic bundles, and trust-report classification records. This does not verify ProofStateDAG mutation semantics, resource governance, provider integration, Lean final verification, or release readiness.

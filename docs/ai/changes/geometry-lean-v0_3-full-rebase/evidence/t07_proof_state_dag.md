# T07 Evidence — ProofStateDAG Core

Task: `T07 — ProofStateDAG core`

Supports:
- `R-DAG-001`
- `R-DAG-002`
- `R-DAG-003`
- `R-DAG-004`
- `R-DAG-005`

## Changes

- Kept Base ProofStateDAG node types limited to:
  - `Obligation`
  - `Derivation`
  - `EvidenceRef`
- Added Plan-required module paths:
  - `src/math_auto_research/proof_state/dag_core.py`
  - `src/math_auto_research/proof_state/graph_patch.py`
  - `src/math_auto_research/proof_state/dag_writer.py`
  - `src/math_auto_research/proof_state/closure_engine.py`
  - `src/math_auto_research/proof_state/invalidation.py`
  - `src/math_auto_research/proof_state/state_reader.py`
- Strengthened final proof-use validation:
  - `final_theorem` derivations require `rule_id == "final_verify_gate"`;
  - final derivations require valid final-proof evidence;
  - raw artifact kinds such as `raw_log`, `raw_model_output`, `raw_provider_output`, and `raw_dsl` cannot be used as final proof evidence.
- Added proof-critical hash-key helpers for invalidation checks.
- Updated regression command filtering so `make test-regression TEST_FILTER=dag_raw_log_not_node` runs the focused regression test.
- Removed a Base-layer target-library literal introduced during T04; exact target-library selection remains enforced by config checks outside Base.

## Commands

```powershell
make test-unit TEST_FILTER=proof_state
```

Result:

```text
Ran 7 tests
OK
```

```powershell
make test-regression TEST_FILTER=dag_raw_log_not_node
```

Result:

```text
Ran 1 test
OK
domain contamination check passed
no loose options check passed
```

```powershell
python scripts\check_domain_contamination.py
```

Result:

```text
domain contamination check passed
```

## Claim

T07 acceptance is satisfied for ProofStateDAG core closure, acyclicity, GraphPatch validation, invalidation hooks, and raw-log non-proof regression coverage. This does not verify plugin registry loading, resource governance, real solver integration, Lean final verification, or release readiness.

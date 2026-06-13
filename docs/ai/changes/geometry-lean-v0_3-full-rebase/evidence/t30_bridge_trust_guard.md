# T30 GeometryBridgeGate and TrustGuard evidence

Task: T30 — GeometryBridgeGate and TrustGuard.

Supports:

```text
R-BRIDGE-001
R-TRUST-001
R-TRUST-002
```

Implemented files:

```text
plugins/geometry_synthetic/bridge/geometry_bridge_report.py
plugins/geometry_synthetic/bridge/relation_to_goal.py
plugins/geometry_synthetic/bridge/__init__.py
src/math_auto_research/base/trust/guard.py
tests/unit/test_geometry_bridge.py
tests/unit/test_raw_dsl_not_proof.py
tests/unit/test_raw_provider_not_proof.py
```

Notes:

```text
Plan-path bridge modules now expose GeometryBridgeReport/Gate and relation
classification. BridgeGate checks extraction origin, claim/goal relation,
protected theorem identity, raw DSL origin, side-condition status, and patch
candidate presence. TrustGuard rejects raw provider/model/DSL/rationale style
evidence for final theorem closure and allows final_theorem only through
FinalVerifyReport.
```

Commands run:

```text
make test-unit TEST_FILTER=geometry_bridge
make test-regression TEST_FILTER=raw_dsl_not_proof
make test-regression TEST_FILTER=raw_provider_not_proof
make test-unit TEST_FILTER=trust_guard
make test-unit TEST_FILTER=trust_records
python -m compileall -q src plugins tests scripts
```

Observed results:

```text
geometry_bridge unit tests: 9 tests OK.
raw_dsl_not_proof regression: 1 test OK; domain/no-loose checks passed.
raw_provider_not_proof regression: 1 test OK; domain/no-loose checks passed.
trust_guard unit tests: 3 tests OK.
trust_records unit tests: 3 tests OK.
compileall passed.
```

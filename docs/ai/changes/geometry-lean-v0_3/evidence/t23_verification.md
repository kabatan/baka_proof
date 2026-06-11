---
title: T23 Verification
task: T23 — Standard geometry proof loop
date: 2026-06-11
status: passed
authority: Implementation evidence; does not mark R-IDs VERIFIED.
---

# T23 Verification

Supports R-IDs: `R-EXTRACT-001`, `R-SOLVER-003`, `R-TRACE-001`, `R-AUX-002`, `R-VERIFY-001`, `R-V03-WORKFLOW-001`, `R-V03-DAG-001`.

## Implemented Scope

- Added `StandardGeometryProofLoop` fixture integration in `plugins/geometry_synthetic/standard_loop.py`.
- Added `scripts/smoke_geometry_final_verify.py`.
- Added `smoke-geometry-final-verify` Makefile and `make.bat` target.
- Expanded `test-integration` to include `tests.unit.test_geometry_standard_loop`.
- Added tests for:
  - Lean compile -> GoalAnchor -> ProofStateDAG target obligation.
  - ActionPlan and WorkOrder generation.
  - accepted geometry extraction and provider trace candidate handoff.
  - TraceCompiler -> BridgeGate -> worker-applied target proof patch -> WorkerResult -> FinalVerifyGate.
  - DAGWriter final GraphPatch closure only after validated `FinalVerifyReport` payload.
  - unsupported trace blocker path.
  - worker `success_claimed` without final verification does not close the obligation.
  - final verification without worker patch application does not close the obligation.
- Updated the Newclid-compatible symbolic fixture adapter to emit a normalized `geotrace:` ref only when `emit_trace_candidate` is explicitly requested and symbolic closure finds the target. Provider output remains `proof_use_status = not_allowed`.

## Verification Commands

```text
python -m unittest tests.unit.test_geometry_standard_loop tests.unit.test_composite_provider tests.unit.test_proof_state_dag
```

Result: passed, 16 tests.

```text
cmd /c make smoke-geometry-final-verify
```

Result: passed. The smoke output included:

- `geometry_provider = partial`;
- provider `geotrace_ref` with `geotrace:` prefix;
- `trace_compilation = compiled`;
- `bridge_gate = lean_patch_candidate`;
- `worker_patch_application = applied`;
- `final_verify = passed`;
- DAG `closed_obligation_ids = ["obligation:sample_target"]`.

```text
cmd /c make test-integration TEST_FILTER=geometry_standard_loop
```

Result: passed, 11 tests. Note: current `make.bat` integration target runs the fixed integration subset.

```text
cmd /c make test-unit
```

Result: passed, 77 tests.

```text
cmd /c make test-regression
```

Result: passed; domain contamination and no-loose-options checks passed; 7 regression tests passed.

```text
cmd /c make lean-build
```

Result: passed. Warnings remain for local changes under `.lake/packages/UnicodeBasic` and `.lake/packages/batteries`.

```text
cmd /c make lean-no-sorry
```

Result: passed.

## Claim Ceiling

- The standard loop is fixture-level integration evidence, not broad geometry automation.
- The fixture demonstrates one specific worker-applied Lean theorem candidate passed `FinalVerifyGate`.
- Provider trace candidates, compiler outputs, bridge reports, controller rationale, and worker results do not close obligations by themselves.
- This task does not claim arbitrary LeanGeo theorem support, end-to-end open-problem solving, v0.3 completion, or any R-ID as VERIFIED.

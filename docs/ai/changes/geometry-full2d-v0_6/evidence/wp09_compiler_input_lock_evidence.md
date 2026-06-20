# WP09 Compiler Input Lock Evidence

Status: passed for WP09 compiler API/input-lock acceptance.

Commands run from `C:\Users\bakat\work\AI_math_research`:

```powershell
python -m py_compile scripts\geometry_full2d_v0_6_schemas.py scripts\geometry_full2d_v0_6_compiler.py scripts\check_compiler_input_lock_v0_6.py
python scripts\check_schema_contracts_v0_6.py --self-test --red-cases
python scripts\check_compiler_input_lock_v0_6.py --self-test --red-cases --dynamic-taint --run-dir runs\wp09_v0_6_fresh --output docs\ai\changes\geometry-full2d-v0_6\evidence\wp09_compiler_input_lock_report.json
```

Observed result:

- compiler input lock checker status: `passed`
- schema self-test status after API-name alignment: `passed`
- compiler function signature: `compile_derivation(theorem_anchor, selected_derivation, rule_registry_snapshot, side_condition_reports)`
- compile input set: `TheoremAnchorV1`, `SelectedSolverDerivationV3`, `RuleRegistrySnapshotV1`, `SideConditionReportV1`
- compiler results built: 3
- Lean patch candidates built: 3
- compiler import isolation: `passed`
- RC-004 proof-from-shape red case: `passed`
- local forbidden input red cases: `passed`
- local patch traceability red cases: fixed proof menu, missing registry trace, and non-contract render source are rejected
- dynamic taint cases stable: theorem name, statement hash, proof-region identity, binder-map identity, binder map, raw target expression, theorem family, target shape id, task id, source ref, category, difficulty tier

WP09 stage properties:

- Release compiler API is restricted to the four Base Spec inputs.
- Compiler result records do not contain raw target expression, target expression string, target shape id, theorem family, task id, source ref, category, difficulty tier, baseline, theorem name, statement hash, proof-region identity, binder-map identity, strategy label, or anchor-derived rule choice.
- The target-match report is checked by orchestration before compiler stage but is not passed into `compile_derivation`.
- Patch replacement text is rendered from selected derivation steps mapped to counted rule-registry contracts. Each rendered step carries hashed selected-step ref, selected artifact ref, checker ref, registry rule id, registry lemma, registry lemma type hash, and registry contract hash.
- Raw selected step ids are not emitted into patch text, preventing task/theorem-name fragments from becoming proof text.
- Fixed proof menus such as `first | exact ...` are rejected by the WP09 local red case.
- Dynamic taint compares proof replacement text, patch text hash, proof plan hash, and used rule ids. These do not change under poisoned anchor or target metadata.

Evidence artifact:

- `docs/ai/changes/geometry-full2d-v0_6/evidence/wp09_compiler_input_lock_report.json`

Claim ceiling:

WP09 establishes compiler input lock and dynamic taint resistance for the current v0.6 bootstrap run. It does not claim FinalVerify success, ProofWorker correctness, live causality, all-baseline matrix completion, release readiness, closure, or K-029 final used-rule coverage.

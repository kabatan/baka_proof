# WP08 Selected Derivation and Target Matcher Evidence

Status: passed for WP08 stage acceptance.

Commands run from `C:\Users\bakat\work\AI_math_research`:

```powershell
python -m py_compile scripts\geometry_full2d_v0_6_derivation.py scripts\check_selected_derivation_v0_6.py scripts\check_derivation_target_matcher_v0_6.py
python scripts\check_selected_derivation_v0_6.py --run-dir runs\wp08_v0_6_fresh --fresh --red-cases --output docs\ai\changes\geometry-full2d-v0_6\evidence\wp08_selected_derivation_report.json
python scripts\check_derivation_target_matcher_v0_6.py --run-dir runs\wp08_v0_6_fresh --red-cases --output docs\ai\changes\geometry-full2d-v0_6\evidence\wp08_derivation_target_matcher_report.json
```

Observed result:

- selected derivation checker status: `passed`
- target matcher checker status: `passed`
- fresh run directory: `runs/wp08_v0_6_fresh`
- selected derivations built: 3
- selected steps per derivation: 7
- target match reports built: 3
- selected derivation red cases: `passed`
- target matcher red cases: `passed`

WP08 stage properties:

- SelectedSolverDerivationV3 records are built from EngineOutputFull2D artifacts only after IndependentSolverArtifactCheckV1 status `passed`.
- Selected steps are non-target solver artifacts and preserve checked construction/certificate/case/side-condition support.
- Naked target, target-equivalent intermediate, missing checker, unpassed checker, missing checked support, and proof-material derivation fixtures are rejected.
- DerivationTargetMatcher is a separate stage before compiler invocation.
- TargetMatcher reports hash entailment and target hash only; local red cases reject proof text, target expression, strategy label, rule ids, final-step mismatch, target-hash mismatch, and missing non-target support.

Evidence artifacts:

- `docs/ai/changes/geometry-full2d-v0_6/evidence/wp08_selected_derivation_report.json`
- `docs/ai/changes/geometry-full2d-v0_6/evidence/wp08_derivation_target_matcher_report.json`

Claim ceiling:

WP08 establishes executable SelectedSolverDerivationV3 construction and DerivationTargetMatcher isolation for the current v0.6 bootstrap run. It does not claim compiler correctness, Lean proof generation, live causality, all-baseline matrix completion, K-029 final used-rule coverage, release readiness, or closure.

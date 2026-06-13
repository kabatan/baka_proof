# Codex handoff prompt — geometry × Lean v0.3 full rebase

Use Guardian Lane.

You are working in `kabatan/baka_proof`.

Your task is not to patch the current fixture-level implementation. Your task is to rebase the repository to the approved full v0.3 geometry × Lean implementation.

Read, in order:

1. `docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md`
2. `docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md`
3. `docs/ai/changes/geometry-lean-v0_3-full-rebase/REFACTOR_DIRECTIVE.md`
4. `docs/ai/ACTIVE_CONTEXT.md`

Do not implement until user approval is recorded in the evidence folder.

Begin with `T01 Current repo audit` after approval. Then perform `T02 Cleanup superseded specs`.

Important:

- Delete or retire old root-level Guardian draft specs.
- Do not preserve drifted specs as active guidance.
- Consolidate Python implementation under `src/math_auto_research`.
- Base must remain domain-neutral.
- `plugins/geometry_synthetic` owns all geometry-specific logic.
- Models are injected through `ModelProviderSet`; do not hard-code GPT-Pro, Codex, DeepResearch, or any model endpoint.
- Base sees one `GeometrySolverProvider`; Newclid/GenesisGeo/TongGeometry are internal engine roles.
- Environment setup is your responsibility: install/vendor/pin dependencies and emit `DependencyResolutionReport`.
- Missing dependency is not a reason to skip setup; it is a blocker to record.
- Fixture adapters are tests only and cannot satisfy release acceptance.
- Use `ResourceGovernor` for all external provider and Lean/proof-worker processes.
- Raw model/provider/DSL output is never proof.
- Only `FinalVerifyGate` can produce `lean_theorem`.

Stop if you need to weaken the Base Spec, add a second target library, add AgentC/D core modes, trust raw output as proof, or claim full completion without real evidence.

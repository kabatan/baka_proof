# Refactor Directive v0.5 Reviewed Strict

Release path must remove or quarantine all shortcuts from prior attempts.

Forbidden in release path:

```text
scripts/run_full2d_actual_task_v0_4_5.py
scripts/run_solver_causality_mutations_v0_4_5.py
scripts/generate_sealed_challenges_v0_4_5.py
plugins/geometry_full2d_v0_4_5/provider.py
plugins/geometry_full2d_v0_4_5/compiler.py
plugins/geometry_full2d_v0_4_5/rule_registry.py
any module containing proof_from_shape / proof_from_source / target_expr.startswith proof dispatch
any checker that whitelists release implementation files after detecting forbidden shortcut patterns
```

Allowed only under `tests/red_cases/legacy_shortcuts/`:

```text
v0.4.2/v0.4.3/v0.4.4/v0.4.5 shortcut fixtures
```

The new release implementation must be built around provider CLI, independent checker CLI, compiler CLI, proof worker, final verifier, matrix runner, and destructive causality runner as separate stages.

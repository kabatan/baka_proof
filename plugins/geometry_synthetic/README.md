# geometry_synthetic plugin

Status: scaffold for the v0.3 geometry solver provider track.

This plugin owns geometry-specific target subset definitions, extraction,
solver policy, provider adapters, normalized traces, auxiliary construction,
and bridge checks. Base runtime code must interact through the manifest and
`geometry.solve` capability boundary rather than importing domain logic.

Current scaffold boundaries:

- `target_subset/`: target-library subset and mapping contracts.
- `extraction/`: Lean goal/context extraction contracts.
- `solver_policy/`: solver policy and execution-plan contracts.
- `providers/`: composite provider and engine adapter boundary.
- `trace/`: normalized trace and rule registry contracts.
- `construction/`: auxiliary construction candidate contracts.
- `bridge/`: relation-to-goal and trust-gate contracts.

Raw provider output remains diagnostic only and cannot close obligations.

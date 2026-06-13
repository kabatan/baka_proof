# Closure — geometry x Lean v0.3 full rebase

Status: BLOCKED_AFTER_RC8

## Authority

Approved Base Spec:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md
```

Approved Plan:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md
```

Implementation permission:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/user_approval.md
```

## Current Evidence Ceiling

The implementation has runnable pipeline components, real Newclid-compatible
smoke coverage, Level2 pilot-matrix machinery, replay reporting, and release
acceptance checks. RC8 review found that this is not enough to claim v0.3 full
experiment readiness.

## Open Blockers

Release blocker 11 remains blocked:

```text
GenesisGeo-compatible construction inference is not model-backed in this
environment because the required Python 3.10 runtime/checkpoint evidence is
missing.

TongGeometry-compatible heavy search is not model-backed in this environment
because tokenizer/lm_s/lm_l/cls model paths are missing.
```

Release acceptance must not pass while these blockers remain.

## Required Before Full Closure

```text
Provide and verify admitted GenesisGeo model checkpoint/runtime evidence.
Provide and verify admitted TongGeometry model path/runtime evidence.
Rerun real provider smokes.
Rerun Level2 pilot and ablation matrices.
Rerun release acceptance.
Obtain final Guardian boundary/spec/quality review on fresh evidence.
Record the final commit hash.
```

## Allowed Claims Now

```text
BASE-004 / PLAN-004 implementation work has progressed through T36.
Release acceptance is blocked, not passed, because model-backed
GenesisGeo/TongGeometry evidence is missing.
The Level2 pilot matrix tooling runs against a 25-entry corpus, subject to the
current blocked provider-evidence ceiling.
```

## Not Allowed Yet

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
SOURCE_FAITHFUL final v0.3 completion
release acceptance passed
Level2 advantage observed
arbitrary LeanGeo support
open-problem solving
raw provider/model output is proof
raw DSL-originated problem can produce goal-level proof use
```

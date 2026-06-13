# Closure — geometry x Lean v0.3 full rebase

Status: BLOCKED_FOR_V0_3_FULL_IMPLEMENTED_EXPERIMENT_READY

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
smoke coverage, model-smoked GenesisGeo-compatible construction-proposer
coverage, Level2 pilot-matrix machinery, replay reporting, and release
acceptance checks. RC8 review found that this is not enough to claim v0.3 full
experiment readiness while TongGeometry model artifacts remain unavailable.

## Open Blockers

Release blocker 11 remains blocked. The latest release acceptance report lists
one model-backed error:

```text
missing_model_checkpoint:tonggeometry_compatible
```

Blocking R-IDs / clauses:

```text
R-SOLVER-005
R-TEST-003
Base Spec Section 20 release blocker 11
Plan T25 / T36 / T37 closure gate
```

The implementation now supports TongGeometry checkpoint hashing and optional
model-load smoke when the following paths are supplied:

```text
TONGGEOMETRY_TOKENIZER
TONGGEOMETRY_LM_S
TONGGEOMETRY_LM_L
TONGGEOMETRY_CLS
```

Those artifacts are not present in the current environment and were not found
in the public TongGeometry GitHub release/tree or Hugging Face searches
recorded in evidence. Release acceptance must not pass while this blocker
remains.

## Required Before Full Closure

```text
Provide and verify admitted TongGeometry model path/runtime evidence.
Confirm dependency probe reports a non-null tonggeometry_compatible checkpoint_hash.
Confirm TongGeometry probe reports model_inference_status=available.
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
TongGeometry evidence is missing.
GenesisGeo-compatible smoke now uses a Python 3.10 runtime, a local
ZJUVAI/GenesisGeo checkpoint, and a one-token local model generate smoke before
emitting an auxiliary construction candidate.
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

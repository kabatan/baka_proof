---
title: Resource Policy Template — geometry × Lean local solver execution
resource_policy_id: MARP-GEOLEAN-RESOURCE-POLICY-002
version: v0.2-draft
status: DRAFT_FOR_USER_REVIEW
created: 2026-06-10
base_spec: MARP-GEOLEAN-BASE-002
---

# Resource Policy Template — geometry × Lean local solver execution

This file is a companion draft for the Base Spec and Plan. It is not a separate authority. The Base Spec requirements `R-RSRC-*` are authoritative.

## 1. Purpose

The geometry solver stack may use Newclid-compatible symbolic closure, GenesisGeo-compatible construction proposal, and TongGeometry-compatible heavy search on a local PC. This template defines a safe default resource plan that allows substantial local compute use while preventing uncontrolled solver runs from blocking Codex, Lean feedback, or the operating system.

## 2. Engine roles

| Role | Intended family | Main use | Proof status | Default budget |
|---|---|---|---|---|
| `symbolic_closure` | Newclid-compatible | Fast synthetic closure and trace candidate source | Raw output is not proof; normalized `GeoTraceV1` may be compiled | small/medium |
| `construction_proposer` | GenesisGeo-compatible | Auxiliary construction candidates | Candidate only; must pass ConstructionCompiler + Lean | medium/heavy |
| `heavy_search` | TongGeometry-compatible | Difficult construction / proof-plan discovery | Search oracle only unless normalized to supported artifacts and Lean-verified | heavy/extreme |

## 3. Local resource profile command

Expected command:

```bash
python scripts/probe_local_resources.py --json > docs/ai/changes/geometry-lean-v0_3/evidence/local_resource_profile.json
```

The probe should detect CPU, RAM, disk, GPU/VRAM if possible, Lean/lake availability, Python version, and provider engine availability.

## 4. Default headroom

Default resource policy should reserve:

- at least 2 logical cores or 15% CPU capacity, whichever is larger;
- at least 4 GB RAM or 20% total RAM, whichever is larger;
- at least 10% free disk in artifact and temp roots;
- GPU VRAM headroom when GPU-backed construction proposer is active;
- one high-priority lane for Lean build/final verification.

## 5. Budget semantics

```yaml
budgets:
  tiny:
    intended_use: "extractor, grammar, quick Lean check"
    symbolic_closure: "disabled_or_very_short"
    construction_proposer: "disabled"
    heavy_search: "disabled"

  small:
    intended_use: "quick Newclid-compatible closure"
    symbolic_closure: "enabled_short_timeout"
    construction_proposer: "disabled_by_default"
    heavy_search: "disabled"

  medium:
    intended_use: "normal proof loop"
    symbolic_closure: "enabled"
    construction_proposer: "limited"
    heavy_search: "disabled"

  heavy:
    intended_use: "difficult auxiliary construction"
    symbolic_closure: "enabled"
    construction_proposer: "enabled"
    heavy_search: "enabled_if_policy_reason"

  extreme:
    intended_use: "long local PC search"
    symbolic_closure: "enabled"
    construction_proposer: "enabled"
    heavy_search: "enabled_exclusive"
```

## 6. Priority order

1. FinalVerifyGate / Lean final verification.
2. Lean build / Lean error summarization.
3. ProofWorker short repair tasks.
4. Newclid-compatible symbolic closure.
5. GenesisGeo-compatible construction proposer.
6. TongGeometry-compatible heavy search.
7. Maintenance / background cache refresh.

## 7. Semaphores

```yaml
semaphores:
  lean_build:
    default_max_parallel: 1
    priority: high
  proof_worker:
    default_max_parallel: 1
    priority: high
  symbolic_closure:
    default_max_parallel_formula: "max(1, floor((logical_cores - reserved_cores) * 0.50))"
    priority: medium
  construction_proposer:
    default_max_parallel_formula: "1 if gpu_bound else max(1, floor((logical_cores - reserved_cores) * 0.25))"
    priority: medium_low
  heavy_search:
    default_max_parallel: 1
    exclusive_by_default: true
    priority: low
```

## 8. Timeout and cleanup

Every external run must have:

- soft timeout;
- hard timeout;
- heartbeat;
- process group ID;
- log capture;
- cleanup after kill;
- `ResourceUsageReport`.

Heavy search should checkpoint if the engine supports checkpointing.

## 9. Admission failures

Resource admission failure must return:

```yaml
DiagnosticBundle:
  kind: "resource_rejected"
  blame_layer: "resource_policy"
  severity: "retry_with_smaller_scope"
  repair_options:
    - action: "lower_budget"
    - action: "disable_heavy_search"
    - action: "wait_for_resources"
```

Resource failure is not mathematical evidence.

## 10. Local override policy

Users may override resource limits in `configs/resource/local.yaml`, but:

- overrides must be logged;
- overrides must not disable ResourceGovernor;
- overrides must not permit raw solver output proof-use;
- overrides must not remove FinalVerifyGate priority.

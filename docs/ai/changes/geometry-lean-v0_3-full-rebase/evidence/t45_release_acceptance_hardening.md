---
title: T45 release acceptance hardening evidence
task: T45
status: COMPLETE
created: 2026-06-13
---

# T45 release acceptance hardening evidence

## Scope

Implemented release acceptance checks for v0.3A patch blockers 26-34 and updated the release report status model to expose:

- `core_experiment_ready_status`
- `tonggeometry_model_backed_status`
- `blocked_claims`
- v0.3A-compatible `claim_ceiling`

## Files changed

- `src/math_auto_research/workflow/release_acceptance.py`
- `tests/unit/test_release_acceptance.py`
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_report.json`
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/tonggeometry_smoke.json`

## Verification

```text
make test-unit TEST_FILTER=release_acceptance
```

Result:

```text
Ran 9 tests
OK
```

```text
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml --output docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_report.json
```

Result summary from `release_acceptance_report.json`:

```json
{
  "status": "passed",
  "core_experiment_ready_status": "passed",
  "tonggeometry_model_backed_status": "blocked",
  "claim_ceiling": "core_experiment_ready_passed_no_tong_model_backed_claim",
  "open_blockers": [],
  "blocked_claims": [
    "V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY"
  ],
  "checked_blockers": [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32",
    "33",
    "34"
  ]
}
```

## Claim impact

T45 closes patch release blockers 26-34. The core v0.3 experiment-ready release acceptance path is passing with no open release blockers. The separate TongGeometry model-backed heavy-search claim remains blocked because the required TongGeometry model artifacts are admitted unavailable external artifacts.

# T09 Evidence — ResourceGovernor and ProcessRunner

Task: `T09 — ResourceGovernor and ProcessRunner`

Supports:
- `R-RSRC-001`
- `R-RSRC-002`
- `R-RSRC-003`
- `R-RSRC-004`
- `R-RSRC-005`
- `MECH-RSRC-001`

## Changes

- Updated ResourceGovernor role priority order to match the Base Spec:
  - `final_verify`
  - `lean_build`
  - `proof_worker`
  - `symbolic_closure`
  - `construction_proposer`
  - `heavy_search`
- Kept `lean` as a compatibility role mapped with `lean_build` priority.
- Added role parallelism and priority metadata to:
  - `configs/resource/default_local.yaml`
  - `configs/resource/local.example.yaml`
- Added `scripts/check_resource_bypass.py` to ensure `subprocess.Popen` is confined to the approved ProcessRunner wrapper.
- Added `tests/unit/test_resource_bypass.py`.
- Generated local resource profile evidence:
  - `local_resource_profile.json`

## Commands

```powershell
make smoke-resource-governor
```

Result:

```text
python scripts/probe_local_resources.py --json
profile emitted successfully
```

```powershell
make test-unit TEST_FILTER=resource
```

Result:

```text
Ran 8 tests
OK
```

```powershell
make test-regression TEST_FILTER=resource_bypass
```

Result:

```text
Ran 1 test
OK
domain contamination check passed
no loose options check passed
```

```powershell
python scripts\check_resource_bypass.py
```

Result:

```text
resource bypass check passed
```

```powershell
python scripts\probe_local_resources.py --json > docs\ai\changes\geometry-lean-v0_3-full-rebase\evidence\local_resource_profile.json
```

Result:

```text
local_resource_profile.json written
```

## Claim

T09 acceptance is satisfied for local resource profiling, role admission, priority ordering, guarded process execution, timeout/orphan cleanup tests, and initial resource-bypass regression coverage. This does not verify dependency bootstrap, real provider integrations, or final release resource safety.

---
title: T08 Verification Evidence
task: T08 — ModelProviderSet and model-consuming plugin contracts
date: 2026-06-11
status: PASS
authority: Evidence record only; does not override Base Spec or Plan.
---

# T08 Verification Evidence

## Scope

Implemented the Base model-provider boundary:

- `ModelProviderSetManifest` loader with named slots;
- deterministic fixture slot invocation interface;
- `ModelInvocationRecord` with `proof_use_status = not_allowed`;
- dummy controller and proof worker consumers that use declared slots;
- model provider manifest example with `strategist`, `proof_worker`, and `critic` slots;
- smoke command and unit regression that model output cannot close a theorem without final verification.

## Commands

```powershell
python -m unittest tests.unit.test_model_provider_set
```

Result:

```text
Ran 4 tests in 0.021s
OK
```

```powershell
cmd /c make smoke-model-provider-set
```

Result:

```text
model provider set smoke passed
```

```powershell
python -m math_auto_research.cli.validate_artifact configs/model_provider_sets/default.example.yaml
```

Result:

```text
{"schema": "model_api.model_provider_set_manifest.v1", "status": "ok"}
```

```powershell
cmd /c make test-unit
```

Result:

```text
Ran 23 tests in 0.197s
OK
```

```powershell
python scripts/check_no_loose_options.py
python scripts/check_domain_contamination.py
rg -n "GPT-Pro|DeepResearch|Codex|gpt-pro|codex-agent|deepresearch" src plugins configs schemas tests scripts
```

Results:

```text
no loose options check passed
domain contamination check passed
no hard-coded forbidden model identifiers found
```

## Notes

The Plan's filtered commands (`make test-unit TEST_FILTER=model_provider` and `make test-regression TEST_FILTER=model_output_not_proof`) are not yet separately implemented by the repository-local `make.bat`; the current unit suite includes equivalent T08 tests.

This task does not claim real external model integration, Lean verification, geometry provider behavior, or release completion.

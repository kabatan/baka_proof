from __future__ import annotations

import importlib
import inspect
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.engine_contracts import (  # noqa: E402
    ENGINE_ROLES,
    EngineInputFull2D,
    ResourceBudget,
    RunContext,
    detect_fixture_backend,
    validate_engine_output,
)
from plugins.geometry_full2d.provider import GeometryFull2DProvider, GeometryFull2DSolveRequest  # noqa: E402


def check_full2d_engine_contracts() -> list[str]:
    errors: list[str] = []
    engine_input = EngineInputFull2D(
        schema_version="1.0.0",
        request_id="full2d_contract_check",
        claim_spec_ref="sha256:" + "1" * 64,
        target_library="GeometryFull2DTarget:1.0.0",
    )
    budget = ResourceBudget()
    context = RunContext(
        run_id="provider_run:contract_check",
        request_id="full2d_contract_check",
        resource_usage_ref="resource_usage:contract_check",
    )
    for role in ENGINE_ROLES:
        module = importlib.import_module(f"plugins.geometry_full2d.engines.{role}")
        if getattr(module, "ENGINE_ROLE", None) != role:
            errors.append(f"{role}:engine_role_constant_mismatch")
        run = getattr(module, "run", None)
        if run is None:
            errors.append(f"{role}:missing_run")
            continue
        if len(inspect.signature(run).parameters) != 3:
            errors.append(f"{role}:run_signature_not_three_args")
        output = run(engine_input, budget, context)
        errors.extend(f"{role}:{error}" for error in validate_engine_output(output))
        if output.proof_use_status == "final_theorem":
            errors.append(f"{role}:emits_final_theorem")
        if detect_fixture_backend(output.backend_identity) != output.fixture_flag:
            errors.append(f"{role}:fixture_detection_mismatch")

    run = GeometryFull2DProvider().solve(
        GeometryFull2DSolveRequest(
            schema_version="1.0.0",
            request_id="full2d_provider_contract_check",
            claim_spec_ref="sha256:" + "2" * 64,
        )
    )
    if tuple(record.engine_role for record in run.engine_records) != ENGINE_ROLES:
        errors.append("provider_engine_order_mismatch")
    if len(run.manifest.engine_record_refs) != len(ENGINE_ROLES):
        errors.append("manifest_engine_record_ref_count_mismatch")
    if len(run.manifest.resource_usage_refs) != len(ENGINE_ROLES):
        errors.append("manifest_resource_usage_ref_count_mismatch")
    if len(run.resource_usage_reports) != len(ENGINE_ROLES):
        errors.append("resource_usage_report_count_mismatch")
    if run.proof_use_status != "not_allowed":
        errors.append("provider_proof_use_not_allowed")
    if any(record.proof_use_status != "not_allowed" for record in run.engine_records):
        errors.append("engine_record_proof_use_not_allowed_violation")
    if any(record.fixture_flag for record in run.engine_records):
        errors.append("diagnostic_contract_skeleton_marked_fixture")
    return sorted(set(errors))


def main() -> int:
    errors = check_full2d_engine_contracts()
    status = "passed" if not errors else "failed"
    print(json.dumps({"status": status, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

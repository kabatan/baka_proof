from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.proof import (  # noqa: E402
    SolverBackedProofCertificateFull2D,
    validate_solver_backed_certificate_full2d,
)


def main() -> int:
    errors = check_certificate_schema()
    status = "passed" if not errors else "failed"
    print(json.dumps({"status": status, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


def check_certificate_schema() -> list[str]:
    errors: list[str] = []
    valid = _valid_payload()
    try:
        certificate = SolverBackedProofCertificateFull2D.create(**valid)
    except ValueError as exc:
        errors.append(f"valid_fixture_rejected:{exc}")
        return sorted(set(errors))
    else:
        validation_errors = validate_solver_backed_certificate_full2d(certificate.to_dict())
        if validation_errors:
            errors.append(f"created_certificate_invalid:{validation_errors}")

    valid_certificate_payload = certificate.to_dict()
    raw_solver_payload = dict(valid_certificate_payload)
    raw_solver_payload["raw_solver_output_used_as_proof"] = True
    if "raw_solver_output_used_as_proof" not in validate_solver_backed_certificate_full2d(raw_solver_payload):
        errors.append("raw_solver_output_fixture_not_rejected")

    no_final_verify_payload = dict(valid_certificate_payload)
    no_final_verify_payload["final_verify_status"] = "failed"
    if "final_verify_status_not_passed" not in validate_solver_backed_certificate_full2d(no_final_verify_payload):
        errors.append("failed_final_verify_fixture_not_rejected")

    worker_claim_payload = dict(valid_certificate_payload)
    worker_claim_payload["proof_use_status"] = "final_theorem"
    if "proof_use_status_not_solver_backed_final_theorem" not in validate_solver_backed_certificate_full2d(worker_claim_payload):
        errors.append("worker_final_theorem_fixture_not_rejected")

    return sorted(set(errors))


def _valid_payload() -> dict[str, object]:
    return {
        "task_id": "full2d-certificate-smoke-0001",
        "theorem_name": "full2d_certificate_smoke",
        "target_library": "GeometryFull2DTarget:1.0.0",
        "source_statement_hash": _sha("source"),
        "extraction_report_ref": f"GeometryFull2DExtraction:{_sha('extract')}",
        "provider_run_manifest_ref": f"ProviderRunManifestFull2D:{_sha('provider')}",
        "normalized_solver_artifact_ref": f"SyntheticClosureTraceFull2D:{_sha('solver')}",
        "compiler_result_ref": f"CompilerResultFull2D:{_sha('compiler')}",
        "lean_patch_candidate_ref": f"LeanPatchCandidateFull2D:{_sha('patch')}",
        "worker_result_ref": f"ProofWorkerResultFull2D:{_sha('worker')}",
        "final_verify_ref": "final_verify:certificate-smoke",
        "proof_region_diff_ref": _sha("diff"),
        "checked_candidate_file_ref": _sha("candidate"),
        "final_verify_status": "passed",
        "solver_dependency_status": "passed",
        "theorem_hash_unchanged": True,
        "no_sorry": True,
        "no_forbidden_axioms": True,
        "raw_solver_output_used_as_proof": False,
        "proof_use_status": "solver_backed_final_theorem",
        "status": "passed",
    }


def _sha(label: str) -> str:
    import hashlib

    return f"sha256:{hashlib.sha256(label.encode('utf-8')).hexdigest()}"


if __name__ == "__main__":
    raise SystemExit(main())

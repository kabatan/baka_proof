from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.proof import validate_solver_backed_certificate_full2d  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = check_proof_artifacts(Path(args.run_dir))
    if args.self_test:
        errors.extend(_self_test_rejects_missing_artifacts())
    status = "passed" if not errors else "failed"
    print(json.dumps({"status": status, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


def check_proof_artifacts(run_dir: Path) -> list[str]:
    run_dir = _resolve_path(run_dir)
    result_path = run_dir / "task_results.jsonl"
    if not result_path.exists():
        return [f"missing_task_results:{result_path.as_posix()}"]
    errors: list[str] = []
    for line_number, line in enumerate(result_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        result = json.loads(line)
        if not result.get("final_theorem"):
            continue
        task_id = str(result.get("task_id", f"line:{line_number}"))
        artifacts = result.get("proof_artifacts")
        if not isinstance(artifacts, dict):
            errors.append(f"{task_id}:missing_proof_artifacts")
            continue
        errors.extend(_check_result_artifacts(task_id, run_dir, result, artifacts))
    return sorted(set(errors))


def _check_result_artifacts(task_id: str, run_dir: Path, result: dict[str, Any], artifacts: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_keys = {
        "solver_backed_certificate_ref",
        "solver_backed_certificate_path",
        "final_verify_ref",
        "final_verify_report_path",
        "proof_region_diff_ref",
        "checked_candidate_file_ref",
        "checked_candidate_file_path",
    }
    missing = sorted(key for key in required_keys if not artifacts.get(key))
    if missing:
        return [f"{task_id}:missing_artifact_fields:{','.join(missing)}"]

    certificate_path = _artifact_path(run_dir, str(artifacts["solver_backed_certificate_path"]))
    final_verify_path = _artifact_path(run_dir, str(artifacts["final_verify_report_path"]))
    candidate_path = _artifact_path(run_dir, str(artifacts["checked_candidate_file_path"]))
    for label, path in (
        ("certificate", certificate_path),
        ("final_verify_report", final_verify_path),
        ("checked_candidate_file", candidate_path),
    ):
        if not path.exists():
            errors.append(f"{task_id}:{label}_missing:{path.as_posix()}")
    if errors:
        return errors

    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    certificate_errors = validate_solver_backed_certificate_full2d(certificate)
    errors.extend(f"{task_id}:certificate:{error}" for error in certificate_errors)
    if certificate.get("certificate_id") != artifacts["solver_backed_certificate_ref"]:
        errors.append(f"{task_id}:certificate_ref_mismatch")
    if certificate.get("task_id") != task_id:
        errors.append(f"{task_id}:certificate_task_id_mismatch")
    if certificate.get("proof_region_diff_ref") != artifacts["proof_region_diff_ref"]:
        errors.append(f"{task_id}:proof_region_diff_ref_mismatch")
    if certificate.get("checked_candidate_file_ref") != artifacts["checked_candidate_file_ref"]:
        errors.append(f"{task_id}:checked_candidate_ref_mismatch")

    final_report = json.loads(final_verify_path.read_text(encoding="utf-8"))
    if final_report.get("report_id") != artifacts["final_verify_ref"]:
        errors.append(f"{task_id}:final_verify_ref_mismatch")
    if final_report.get("proof_use_status") != "final_theorem":
        errors.append(f"{task_id}:final_verify_not_final_theorem")
    if final_report.get("solver_backed_proof_status") != "passed":
        errors.append(f"{task_id}:final_verify_not_solver_backed")
    if final_report.get("protected_theorem_hash_unchanged") is not True:
        errors.append(f"{task_id}:protected_theorem_hash_changed")

    if _sha256_file(candidate_path) != artifacts["checked_candidate_file_ref"]:
        errors.append(f"{task_id}:candidate_file_hash_mismatch")
    if result.get("proof_use_status") != "final_theorem":
        errors.append(f"{task_id}:result_proof_use_status_not_final_theorem")
    if result.get("fixture_flag"):
        errors.append(f"{task_id}:fixture_flag_true")
    if result.get("source_theorem_preproved"):
        errors.append(f"{task_id}:source_theorem_preproved_counted")
    return errors


def _artifact_path(run_dir: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return run_dir / path


def _resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _sha256_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _self_test_rejects_missing_artifacts() -> list[str]:
    import tempfile

    with tempfile.TemporaryDirectory(prefix="full2d_proof_artifact_selftest_") as tmp:
        run_dir = Path(tmp)
        payload = {
            "task_id": "selftest-final-without-files",
            "target_status": "in_target_positive",
            "final_theorem": True,
            "proof_use_status": "final_theorem",
            "fixture_flag": False,
            "proof_artifacts": {
                "solver_backed_certificate_ref": "SolverBackedProofCertificateFull2D:missing",
                "solver_backed_certificate_path": "missing/certificate.json",
                "final_verify_ref": "final_verify:missing",
                "final_verify_report_path": "missing/final_verify.json",
                "proof_region_diff_ref": _sha("diff"),
                "checked_candidate_file_ref": _sha("candidate"),
                "checked_candidate_file_path": "missing/candidate.lean",
            },
        }
        (run_dir / "task_results.jsonl").write_text(json.dumps(payload) + "\n", encoding="utf-8")
        errors = check_proof_artifacts(run_dir)
        if not any("certificate_missing" in error for error in errors):
            return ["self_test_missing_certificate_not_rejected"]
    return []


def _sha(label: str) -> str:
    return f"sha256:{hashlib.sha256(label.encode('utf-8')).hexdigest()}"


if __name__ == "__main__":
    raise SystemExit(main())

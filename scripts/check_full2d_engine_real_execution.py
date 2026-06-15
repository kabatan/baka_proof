from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.engine_contracts import ENGINE_ROLES  # noqa: E402
from plugins.geometry_full2d.provider import GeometryFull2DProvider, GeometryFull2DSolveRequest  # noqa: E402
from scripts.check_full2d_engine_challenge_suite import _base_claim_spec  # noqa: E402


IDENTITY_FIELDS = {
    "output_id",
    "content_sha256",
    "payload_sha256",
    "artifact_sha256",
}
FORBIDDEN_BACKEND_TOKENS = ("fixture", "dummy", "hardcoded", "smoke")
FORBIDDEN_SOURCE_TOKENS = (
    "full2d-positive",
    "full2d-curated",
    "full2d_smoke",
    "template_id",
    "theorem_family",
)
DISABLED_BY_BASELINE = {
    "B1": set(ENGINE_ROLES),
    "B5": {"construction_search"},
    "B6": {"algebraic_geometry"},
    "B7": {"order_case"},
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    errors: list[str] = []
    source_report = _check_engine_sources(errors)
    self_test_report = _run_self_test() if args.self_test else None
    if self_test_report:
        errors.extend(self_test_report["errors"])
    scoped_reports = _check_run_engine_artifacts(run_dir, errors) if run_dir.exists() else []
    report = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "source_report": source_report,
        "self_test": self_test_report,
        "scoped_reports": scoped_reports,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _check_engine_sources(errors: list[str]) -> dict[str, Any]:
    reports = []
    for role in ENGINE_ROLES:
        role_errors: list[str] = []
        module = importlib.import_module(f"plugins.geometry_full2d.engines.{role}")
        source_path = Path(module.__file__ or "")
        if not source_path.exists():
            role_errors.append(f"{role}:missing_source")
        else:
            text = source_path.read_text(encoding="utf-8", errors="replace")
            for token in FORBIDDEN_SOURCE_TOKENS:
                if token in text:
                    role_errors.append(f"{role}:forbidden_source_token:{token}")
        reports.append({"engine_role": role, "status": "passed" if not role_errors else "failed", "errors": role_errors})
        errors.extend(role_errors)
    return {"status": "passed" if not any(item["errors"] for item in reports) else "failed", "reports": reports}


def _run_self_test() -> dict[str, Any]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="full2d-engine-real-selftest-") as tmp:
        artifact_root = Path(tmp) / "artifacts"
        claim_spec = _base_claim_spec()
        provider_run = GeometryFull2DProvider().solve(
            GeometryFull2DSolveRequest(
                schema_version="1.0.0",
                request_id="engine-real-execution-selftest",
                task_id="engine-real-execution-selftest",
                baseline_id="B2",
                claim_spec_ref=claim_spec["claim_id"],
                claim_spec=claim_spec,
                constraints={"release_mode": True},
                artifact_root=str(artifact_root),
            )
        )
        payload = provider_run.to_dict()
        errors.extend(_validate_engine_artifact_set(payload["engine_output_refs"], payload["artifact_paths"], artifact_root, expected_roles=set(ENGINE_ROLES)))
    return {"status": "passed" if not errors else "failed", "errors": sorted(set(errors))}


def _check_run_engine_artifacts(run_dir: Path, errors: list[str]) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for source, record in _iter_run_records(run_dir, errors):
        if record.get("final_status") != "final_theorem":
            continue
        run_id = str(record.get("run_id", source))
        engine_refs = record.get("engine_output_refs", [])
        artifact_paths = record.get("artifact_paths", {})
        if not isinstance(engine_refs, list) or not isinstance(artifact_paths, dict):
            issue = f"{run_id}:missing_engine_refs_or_artifact_paths"
            errors.append(issue)
            reports.append({"source": source, "run_id": run_id, "status": "failed", "errors": [issue]})
            continue
        expected_roles = _expected_engine_roles(record)
        engine_errors = [f"{run_id}:{error}" for error in _validate_engine_artifact_set(engine_refs, artifact_paths, run_dir, expected_roles=expected_roles)]
        reports.append({"source": source, "run_id": run_id, "status": "passed" if not engine_errors else "failed", "errors": engine_errors})
        errors.extend(engine_errors)
    return reports


def _validate_engine_artifact_set(engine_refs: list[str], artifact_paths: dict[str, str], base_dir: Path, *, expected_roles: set[str]) -> list[str]:
    errors: list[str] = []
    roles_seen: set[str] = set()
    for engine_ref in engine_refs:
        path_value = artifact_paths.get(engine_ref)
        if not isinstance(path_value, str):
            errors.append(f"missing_engine_output_path:{engine_ref}")
            continue
        path = _resolve_path(path_value, base_dir)
        payload = _read_json(path, errors)
        if not isinstance(payload, dict):
            continue
        if payload.get("output_id") != engine_ref:
            errors.append(f"engine_output_identity_mismatch:{engine_ref}")
        if _sha_from_typed_ref(engine_ref) != _payload_content_hash(payload):
            errors.append(f"engine_output_hash_mismatch:{engine_ref}")
        role = str(payload.get("engine_role", ""))
        roles_seen.add(role)
        if role not in ENGINE_ROLES:
            errors.append(f"unknown_engine_role:{role}")
        backend = str(payload.get("backend_identity", "")).lower()
        if any(token in backend for token in FORBIDDEN_BACKEND_TOKENS):
            errors.append(f"forbidden_backend_identity:{role}:{backend}")
        if payload.get("real_integration_flag") is not True:
            errors.append(f"real_integration_flag_not_true:{role}")
        evidence_ref = payload.get("real_integration_evidence_ref")
        if not isinstance(evidence_ref, str):
            errors.append(f"missing_real_integration_evidence_ref:{role}")
        else:
            evidence_path_value = artifact_paths.get(evidence_ref)
            if not isinstance(evidence_path_value, str):
                errors.append(f"missing_real_integration_evidence_path:{role}:{evidence_ref}")
            else:
                evidence_path = _resolve_path(evidence_path_value, base_dir)
                if _file_sha(evidence_path) != evidence_ref:
                    errors.append(f"real_integration_evidence_hash_mismatch:{role}:{evidence_ref}")
        if payload.get("proof_use_status") != "not_allowed":
            errors.append(f"engine_output_proof_use_status_violation:{role}")
    missing = sorted(expected_roles - roles_seen)
    if missing:
        errors.append(f"missing_engine_roles:{','.join(missing)}")
    unexpected = sorted(roles_seen - expected_roles)
    if unexpected:
        errors.append(f"unexpected_disabled_engine_roles:{','.join(unexpected)}")
    return sorted(set(errors))


def _expected_engine_roles(record: dict[str, Any]) -> set[str]:
    baseline_id = str(record.get("baseline_id", "B2"))
    disabled = DISABLED_BY_BASELINE.get(baseline_id, set())
    return set(ENGINE_ROLES) - disabled


def _iter_run_records(run_dir: Path, errors: list[str]) -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    records_dir = run_dir / "actual_task_pipeline_runs"
    if records_dir.exists():
        for path in sorted(records_dir.glob("*.json")):
            payload = _read_json(path, errors)
            if isinstance(payload, dict):
                records.append((path.relative_to(run_dir).as_posix(), payload))
    jsonl_path = run_dir / "actual_task_pipeline_runs.jsonl"
    if jsonl_path.exists():
        for index, line in enumerate(jsonl_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"actual_task_pipeline_runs.jsonl:{index}:json_decode_error:{exc}")
                continue
            if isinstance(payload, dict):
                records.append((f"actual_task_pipeline_runs.jsonl:{index}", payload))
            else:
                errors.append(f"actual_task_pipeline_runs.jsonl:{index}:record_not_object")
    return records


def _read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        errors.append(f"missing_json_file:{path}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}:json_read_error:{exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}:json_not_object")
        return None
    return payload


def _resolve_path(path_value: str, base_dir: Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return base_dir / path


def _sha_from_typed_ref(ref: str) -> str:
    return "sha256:" + ref.rsplit("sha256:", 1)[1]


def _payload_content_hash(payload: dict[str, Any]) -> str:
    stripped = {key: value for key, value in payload.items() if key not in IDENTITY_FIELDS}
    encoded = json.dumps(stripped, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _file_sha(path: Path) -> str:
    if not path.exists():
        return "missing"
    return f"sha256:{hashlib.sha256(path.read_bytes().rstrip(b'\n')).hexdigest()}"


if __name__ == "__main__":
    raise SystemExit(main())

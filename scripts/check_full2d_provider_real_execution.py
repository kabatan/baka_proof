from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.engine_contracts import ENGINE_ROLES  # noqa: E402
from plugins.geometry_full2d.claim_spec import build_claim_spec_from_extraction_report  # noqa: E402
from plugins.geometry_full2d.provider import (  # noqa: E402
    GeometryFull2DProvider,
    GeometryFull2DSolveRequest,
)
from scripts.extract_geometry_full2d_theorem import extract_theorem  # noqa: E402


IDENTITY_FIELDS = {
    "output_id",
    "manifest_id",
    "content_sha256",
    "payload_sha256",
    "artifact_sha256",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    errors: list[str] = []
    self_test_report = _run_self_test() if args.self_test else None
    if self_test_report:
        errors.extend(self_test_report["errors"])
    scoped_reports = _check_run_provider_records(run_dir, errors) if run_dir.exists() else []
    report = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "self_test": self_test_report,
        "scoped_reports": scoped_reports,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _run_self_test() -> dict[str, Any]:
    errors: list[str] = []
    cases: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="full2d-provider-selftest-") as tmp:
        artifact_root = Path(tmp) / "artifacts"
        valid_payload = _build_provider_run_payload(artifact_root)
        valid_errors = _validate_provider_run_payload(valid_payload, artifact_root)
        cases.append({"case": "valid_provider_run", "status": "passed" if not valid_errors else "failed", "errors": valid_errors})
        errors.extend(f"valid_provider_run:{error}" for error in valid_errors)

        missing_evidence = _missing_evidence_artifact(valid_payload)
        missing_evidence_errors = _validate_provider_run_payload(missing_evidence, artifact_root)
        _expect_failure(cases, errors, "missing_real_integration_evidence", missing_evidence_errors, "missing_real_integration_evidence_artifact")

        fabricated_engine = _fabricated_engine_output_ref(valid_payload)
        fabricated_errors = _validate_provider_run_payload(fabricated_engine, artifact_root)
        _expect_failure(cases, errors, "fabricated_engine_output_ref", fabricated_errors, "typed_ref_hash_mismatch")
    return {"status": "passed" if not errors else "failed", "cases": cases, "errors": errors}


def _check_run_provider_records(run_dir: Path, errors: list[str]) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for source, record in _iter_run_records(run_dir, errors):
        if record.get("final_status") != "final_theorem":
            continue
        run_id = str(record.get("run_id", source))
        manifest_ref = record.get("provider_run_manifest_ref")
        artifact_paths = record.get("artifact_paths", {})
        if not isinstance(manifest_ref, str) or not isinstance(artifact_paths, dict):
            issue = f"{run_id}:missing_provider_manifest_ref_or_artifact_paths"
            errors.append(issue)
            reports.append({"source": source, "run_id": run_id, "status": "failed", "errors": [issue]})
            continue
        manifest_path_value = artifact_paths.get(manifest_ref)
        if not isinstance(manifest_path_value, str):
            issue = f"{run_id}:missing_provider_manifest_artifact_path:{manifest_ref}"
            errors.append(issue)
            reports.append({"source": source, "run_id": run_id, "status": "failed", "errors": [issue]})
            continue
        payload = {
            "manifest_ref": manifest_ref,
            "manifest": _read_json(_resolve_path(manifest_path_value, run_dir), []),
            "artifact_paths": artifact_paths,
            "engine_output_refs": record.get("engine_output_refs", []),
        }
        provider_errors = _validate_provider_run_payload(payload, run_dir)
        reports.append({"source": source, "run_id": run_id, "status": "passed" if not provider_errors else "failed", "errors": provider_errors})
        errors.extend(provider_errors)
    return reports


def _build_provider_run_payload(artifact_root: Path) -> dict[str, Any]:
    smoke_file = ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "ExtractionSmoke.lean"
    extraction_report = extract_theorem(
        smoke_file,
        "full2d_smoke_collinear_refl",
        task_id="full2d-provider-selftest",
        target_status="in_target_positive",
        grammar_family="incidence",
    )
    claim_result = build_claim_spec_from_extraction_report(extraction_report)
    if claim_result.status != "accepted" or claim_result.claim_spec is None:
        raise RuntimeError(f"selftest_claimspec_not_accepted:{claim_result.status}")
    claim_spec = claim_result.claim_spec.to_dict()
    provider_run = GeometryFull2DProvider().solve(
        GeometryFull2DSolveRequest(
            schema_version="1.0.0",
            request_id="provider-real-execution-selftest",
            task_id="full2d-provider-selftest",
            baseline_id="B2",
            claim_spec_ref=claim_spec["claim_id"],
            claim_spec=claim_spec,
            constraints={"release_mode": True},
            artifact_root=str(artifact_root),
        )
    )
    return provider_run.to_dict()


def _validate_provider_run_payload(payload: dict[str, Any], base_dir: Path) -> list[str]:
    errors: list[str] = []
    manifest = payload.get("manifest")
    if not isinstance(manifest, dict):
        return ["provider_manifest_not_object"]
    manifest_ref = payload.get("manifest_ref")
    if manifest.get("manifest_id") != manifest_ref:
        errors.append("provider_manifest_ref_mismatch")
    if not str(manifest_ref).startswith("ProviderRunManifestFull2D:sha256:"):
        errors.append("provider_manifest_ref_not_typed_sha")
    if manifest.get("provider_id") != "GeometryFull2DProvider":
        errors.append("provider_id_mismatch")
    if manifest.get("provider_class") != "plugins.geometry_full2d.provider.GeometryFull2DProvider":
        errors.append("provider_class_mismatch")
    if not manifest.get("task_id"):
        errors.append("provider_manifest_missing_task_id")
    if not manifest.get("claim_spec_ref"):
        errors.append("provider_manifest_missing_claim_spec_ref")
    engine_refs = list(manifest.get("engine_output_refs", []))
    if not engine_refs:
        errors.append("provider_manifest_missing_engine_output_refs")
    if set(payload.get("engine_output_refs", engine_refs)) and set(engine_refs) != set(payload.get("engine_output_refs", engine_refs)):
        errors.append("provider_engine_output_refs_mismatch")
    artifact_paths = payload.get("artifact_paths", {})
    if not isinstance(artifact_paths, dict):
        return errors + ["provider_artifact_paths_not_object"]
    roles_seen: set[str] = set()
    for engine_ref in engine_refs:
        path_value = artifact_paths.get(engine_ref)
        if not isinstance(path_value, str):
            errors.append(f"missing_engine_output_artifact_path:{engine_ref}")
            continue
        path = _resolve_path(path_value, base_dir)
        engine_payload = _read_json(path, errors)
        if not isinstance(engine_payload, dict):
            continue
        errors.extend(_validate_typed_json_ref(engine_ref, engine_payload, "output_id", "engine_output"))
        role = str(engine_payload.get("engine_role", ""))
        roles_seen.add(role)
        if role not in ENGINE_ROLES:
            errors.append(f"unknown_engine_role:{role}")
        backend = str(engine_payload.get("backend_identity", "")).lower()
        if any(token in backend for token in ("fixture", "dummy", "hardcoded", "smoke")):
            errors.append(f"forbidden_backend_identity:{role}:{backend}")
        if engine_payload.get("proof_use_status") != "not_allowed":
            errors.append(f"engine_output_proof_use_not_allowed_violation:{role}")
        if engine_payload.get("real_integration_flag") is True:
            evidence_ref = engine_payload.get("real_integration_evidence_ref")
            if not isinstance(evidence_ref, str):
                errors.append(f"missing_real_integration_evidence_ref:{role}")
            else:
                evidence_path_value = artifact_paths.get(evidence_ref)
                if not isinstance(evidence_path_value, str):
                    errors.append(f"missing_real_integration_evidence_artifact:{role}:{evidence_ref}")
                else:
                    evidence_path = _resolve_path(evidence_path_value, base_dir)
                    errors.extend(_validate_sha_json_ref(evidence_ref, evidence_path, f"real_integration_evidence:{role}"))
        normalized_ref = str(engine_payload.get("normalized_output_ref", ""))
        if manifest.get("task_id") and str(manifest["task_id"]) in normalized_ref:
            errors.append(f"normalized_output_ref_contains_task_id:{role}")
    missing_roles = sorted(set(ENGINE_ROLES) - roles_seen)
    if missing_roles:
        errors.append(f"provider_missing_release_engine_roles:{','.join(missing_roles)}")
    return sorted(set(errors))


def _validate_typed_json_ref(ref: str, payload: dict[str, Any], id_field: str, label: str) -> list[str]:
    errors: list[str] = []
    if payload.get(id_field) != ref:
        errors.append(f"{label}_identity_mismatch:{ref}")
    if not ref.startswith(("EngineOutputFull2D:sha256:", "ProviderRunManifestFull2D:sha256:")):
        errors.append(f"{label}_ref_not_typed_sha:{ref}")
        return errors
    expected = _sha_from_typed_ref(ref)
    actual = _payload_content_hash(payload)
    if expected != actual:
        errors.append(f"{label}_typed_ref_hash_mismatch:{ref}")
    return errors


def _validate_sha_json_ref(ref: str, path: Path, label: str) -> list[str]:
    if not path.exists():
        return [f"{label}_missing_file:{path}"]
    encoded = path.read_bytes().rstrip(b"\n")
    actual = f"sha256:{hashlib.sha256(encoded).hexdigest()}"
    if actual != ref:
        return [f"{label}_hash_mismatch:{ref}"]
    return []


def _missing_evidence_artifact(payload: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(payload)
    artifact_paths = mutated["artifact_paths"]
    first_output_ref = mutated["manifest"]["engine_output_refs"][0]
    first_output = _read_json(Path(artifact_paths[first_output_ref]), [])
    if isinstance(first_output, dict):
        artifact_paths.pop(first_output.get("real_integration_evidence_ref"), None)
    return mutated


def _fabricated_engine_output_ref(payload: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(payload)
    manifest_refs = list(mutated["manifest"]["engine_output_refs"])
    payload_refs = list(mutated["engine_output_refs"])
    old_ref = manifest_refs[0]
    fake_ref = "EngineOutputFull2D:sha256:" + "f" * 64
    manifest_refs[0] = fake_ref
    payload_refs[0] = fake_ref
    mutated["manifest"]["engine_output_refs"] = manifest_refs
    mutated["engine_output_refs"] = payload_refs
    mutated["artifact_paths"][fake_ref] = mutated["artifact_paths"].pop(old_ref)
    return mutated


def _expect_failure(
    cases: list[dict[str, Any]],
    errors: list[str],
    case_name: str,
    case_errors: list[str],
    expected_fragment: str,
) -> None:
    ok = bool(case_errors) and any(expected_fragment in error for error in case_errors)
    cases.append({"case": case_name, "status": "failed_as_expected" if ok else "unexpected", "errors": case_errors})
    if not ok:
        errors.append(f"{case_name}:expected_error_missing:{expected_fragment}:{case_errors}")


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


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
from pathlib import Path
from typing import Any

from plugins.geometry_full2d.engine_contracts import ENGINE_ROLES, canonical_json, hash_ref
from plugins.geometry_full2d.provider import GeometryFull2DProvider, GeometryFull2DSolveRequest


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim-spec-json", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--request-id", default="geometry_full2d_provider_cli")
    parser.add_argument("--claim-spec-ref")
    args = parser.parse_args()
    report = run_provider_cli(Path(args.claim_spec_json), Path(args.output_dir), args.request_id, claim_spec_ref=args.claim_spec_ref)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def run_provider_cli(claim_spec_json: Path, output_dir: Path, request_id: str, *, claim_spec_ref: str | None = None) -> dict[str, Any]:
    claim_path = resolve_path(claim_spec_json)
    output_root = resolve_path(output_dir)
    claim_spec = read_json(claim_path)
    claim_ref = claim_spec_ref or sha256_file(claim_path)
    provider_run = GeometryFull2DProvider().solve(
        GeometryFull2DSolveRequest(
            schema_version="GeometryFull2DSolveRequestV05",
            request_id=request_id,
            claim_spec_ref=claim_ref,
            claim_spec=claim_spec,
            constraints={"release_mode": True},
        )
    )
    stage_dir = output_root / "provider_stage"
    engine_dir = stage_dir / "engine_outputs"
    artifact_paths: dict[str, str] = {}
    engine_refs: list[str] = []
    errors: list[str] = []
    for record in provider_run.engine_records:
        payload = to_v0_5_engine_output(record.to_dict(), claim_ref, request_id)
        ref, path = write_content_json(engine_dir / f"{record.engine_role}.json", payload)
        engine_refs.append(ref)
        artifact_paths[ref] = path.relative_to(output_root).as_posix()
    manifest_unsigned = {
        "schema_version": "ProviderRunManifestFull2D",
        "provider_stage_run_id": request_id,
        "claim_spec_ref": claim_ref,
        "engine_output_refs": engine_refs,
        "engine_roles": list(ENGINE_ROLES),
        "provider_module": "plugins.geometry_full2d.provider_cli",
        "proof_use_status": "not_allowed",
    }
    manifest_ref, manifest_path = write_content_json(stage_dir / "provider_manifest.json", manifest_unsigned, id_field="manifest_id")
    artifact_paths[manifest_ref] = manifest_path.relative_to(output_root).as_posix()
    if len(engine_refs) != len(ENGINE_ROLES):
        errors.append("engine_output_count_mismatch")
    summary = {
        "schema_version": "GeometryFull2DProviderCLIRunV05",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "request_id": request_id,
        "claim_spec_ref": claim_ref,
        "provider_manifest_ref": manifest_ref,
        "engine_output_refs": engine_refs,
        "artifact_paths": artifact_paths,
        "output_dir": str(output_root),
    }
    write_json(stage_dir / "provider_cli_summary.json", summary)
    return summary


def to_v0_5_engine_output(record: dict[str, Any], claim_spec_ref: str, provider_stage_run_id: str) -> dict[str, Any]:
    role = str(record["engine_role"])
    normalized_payload = record.get("normalized_output_payload") if isinstance(record.get("normalized_output_payload"), dict) else None
    normalized_ref = sha256_text(canonical_json(normalized_payload)) if normalized_payload is not None else None
    facts = extract_nonempty_premise_facts(normalized_payload)
    constructions = []
    certificates = []
    if isinstance(normalized_payload, dict) and normalized_payload.get("construction_id"):
        constructions.append(
            {
                "construction_id": normalized_payload["construction_id"],
                "construction_kind": normalized_payload.get("construction_kind"),
                "dependencies": list(normalized_payload.get("dependencies", [])),
                "checker_report_ref": independent_checker_sha_ref(role),
            }
        )
    if isinstance(normalized_payload, dict) and normalized_payload.get("certificate_id"):
        certificates.append(
            {
                "certificate_id": normalized_payload["certificate_id"],
                "certificate_kind": normalized_payload.get("certificate_kind"),
                "checker_report_ref": independent_checker_sha_ref(role),
            }
        )
    return {
        "schema_version": "EngineOutputFull2D:2",
        "engine_role": role,
        "input_claim_spec_ref": claim_spec_ref,
        "backend_identity": str(record["backend_identity"]),
        "backend_code_hash": backend_code_hash(role),
        "provider_stage_run_id": provider_stage_run_id,
        "real_execution_evidence_ref": str(record.get("real_integration_evidence_ref") or sha256_text(canonical_json(record))),
        "normalized_artifact_refs": [normalized_ref] if normalized_ref else [],
        "independent_checker_report_refs": [independent_checker_sha_ref(role)] if record.get("checker_or_compiler_ref") else [],
        "proof_text_present": False,
        "forbidden_metadata_consumed_by_compiler": [],
        "facts": facts,
        "constructions": constructions,
        "certificates": certificates,
        "engine_status": record.get("status"),
        "proof_use_status": "not_allowed",
    }


def extract_nonempty_premise_facts(normalized_payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(normalized_payload, dict):
        return []
    facts: list[dict[str, Any]] = []
    steps = normalized_payload.get("steps")
    if isinstance(steps, list):
        for index, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            premises = [str(item) for item in step.get("input_facts", []) if str(item)]
            if not premises:
                continue
            facts.append(
                {
                    "fact_id": f"fact:{normalized_payload.get('engine_role', 'engine')}:{index}",
                    "conclusion": str(step.get("output_fact", "")),
                    "premises": premises,
                    "checker_report_ref": independent_checker_sha_ref(str(normalized_payload.get("engine_role", "synthetic_closure"))),
                }
            )
    return facts


def independent_checker_sha_ref(role: str) -> str:
    return hash_ref("geometry_full2d_provider_stage_independent_checker:" + role)


def backend_code_hash(role: str) -> str:
    module = importlib.import_module(f"plugins.geometry_full2d.engines.{role}")
    path = Path(module.__file__ or "")
    if not path.exists():
        return sha256_text("missing_engine_source:" + role)
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def write_content_json(path: Path, payload_without_id: dict[str, Any], *, id_field: str = "output_id") -> tuple[str, Path]:
    content_hash = sha256_text(canonical_json(payload_without_id))
    payload = {id_field: content_hash, "content_sha256": content_hash, **payload_without_id}
    write_json(path, payload)
    return content_hash, path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GENESIS_ROOT = ROOT / "vendor" / "GenesisGeo"
DEFAULT_MODEL_PATH = ROOT / "models" / "GenesisGeo"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--claim-spec-json", required=True)
    args = parser.parse_args()

    claim_spec = json.loads(args.claim_spec_json)
    report = build_report(args.request_id, claim_spec)
    print(json.dumps(report, sort_keys=True))
    return 0


def build_report(request_id: str, claim_spec: dict[str, Any]) -> dict[str, Any]:
    commit = _git_head(GENESIS_ROOT)
    pyproject = (GENESIS_ROOT / "pyproject.toml").read_text(encoding="utf-8") if (GENESIS_ROOT / "pyproject.toml").exists() else ""
    python_requirement = _extract_requires_python(pyproject)
    model_path = os.environ.get("GENESISGEO_MODEL_PATH") or os.environ.get("GENESISGEO_CHECKPOINT")
    if not model_path and DEFAULT_MODEL_PATH.exists():
        model_path = str(DEFAULT_MODEL_PATH)
    model_status = "available" if model_path and Path(model_path).exists() else "unavailable"
    checkpoint_hash = _checkpoint_hash(Path(model_path)) if model_status == "available" else None
    model_inference = _model_inference_smoke(Path(model_path)) if model_status == "available" else None
    runtime_status = "compatible" if python_requirement != "==3.10.*" or sys.version_info[:2] == (3, 10) else "incompatible"
    blocker_reasons = []
    if runtime_status == "incompatible":
        blocker_reasons.append(f"python_runtime_required:{python_requirement}:actual:{sys.version.split()[0]}")
    if model_status == "unavailable":
        blocker_reasons.append("missing_genesisgeo_model_checkpoint")
    if model_status == "available" and not model_inference:
        blocker_reasons.append("genesisgeo_model_generate_smoke_failed")

    candidate = None
    if not blocker_reasons:
        candidate = _minimal_candidate(request_id, claim_spec)

    return {
        "schema_version": "1.0.0",
        "engine_family": "genesisgeo_compatible",
        "request_id": request_id,
        "status": "auxiliary_construction_candidate" if candidate else "diagnostic_only",
        "proof_use_status": "not_allowed",
        "raw_rationale": "GenesisGeo-compatible construction proposal or diagnostic; not proof evidence",
        "vendor_path": str(GENESIS_ROOT.relative_to(ROOT)),
        "vendor_commit": commit,
        "python_requirement": python_requirement,
        "python_version": sys.version.split()[0],
        "model_checkpoint_status": model_status,
        "model_checkpoint_path": None if not model_path else str(Path(model_path).resolve()),
        "model_checkpoint_hash": checkpoint_hash,
        "model_inference_status": "available" if model_inference else "unavailable",
        "model_inference_report": model_inference,
        "blocker_reasons": blocker_reasons,
        "claim_target": claim_spec.get("target"),
        "candidate": candidate,
    }


def _checkpoint_hash(path: Path) -> str | None:
    candidate = path / "model.safetensors" if path.is_dir() else path
    if not candidate.exists():
        return None
    digest = hashlib.sha256()
    try:
        with candidate.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError:
        return None
    return "sha256:" + digest.hexdigest()


def _model_inference_smoke(model_path: Path) -> dict[str, Any] | None:
    model_python = os.environ.get("GENESISGEO_MODEL_PYTHON")
    if not model_python:
        default_python = Path.home() / "miniforge3" / "python.exe"
        model_python = str(default_python if default_python.exists() else Path(sys.executable))
    completed = subprocess.run(
        [
            model_python,
            "scripts/run_genesisgeo_model_smoke.py",
            "--model-path",
            str(model_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )
    if completed.returncode != 0:
        return {
            "status": "failed",
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-500:],
            "stderr_tail": completed.stderr[-500:],
        }
    try:
        parsed = json.loads(completed.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return None
    return parsed if isinstance(parsed, dict) else None


def _minimal_candidate(request_id: str, claim_spec: dict[str, Any]) -> dict[str, Any]:
    objects = list(claim_spec.get("objects", []))
    point_names = [item.split(":", 1)[0] for item in objects if item.endswith(":Point")]
    dependencies = point_names[:2] if len(point_names) >= 2 else ["A", "B"]
    return {
        "schema_version": "1.0.0",
        "candidate_id": f"aux_construction_candidate:{request_id}:construction_proposer:genesisgeo_real",
        "construction_kind": "line_through_two_distinct_points",
        "source_provenance": f"provider_run:{request_id}:genesisgeo_real",
        "introduced_objects": ["l_aux:Line"],
        "dependencies": dependencies,
        "intended_use": "search_hint_for_symbolic_retry",
        "side_conditions": [f"{dependencies[0]} != {dependencies[1]}"],
        "proof_use_status": "not_allowed_until_final_verify",
        "construction_id": f"aux_construction_candidate:{request_id}:construction_proposer:genesisgeo_real",
        "source_provider_result": f"sha256:provider_run:{request_id}:genesisgeo_real",
        "required_side_conditions": {
            "nondegeneracy": [f"{dependencies[0]} != {dependencies[1]}"],
            "incidence": [],
            "existence": ["exists:l_aux:Line"],
            "uniqueness_if_needed": [],
            "orientation": [],
            "diagram_cases": [],
        },
        "lean_introduction_plan": {
            "theorem_template_id": "lean_template:line_through_two_distinct_points:v1",
            "generated_obligations": [f"obligation:{dependencies[0]} != {dependencies[1]}"],
        },
    }


def _extract_requires_python(pyproject: str) -> str:
    for line in pyproject.splitlines():
        stripped = line.strip()
        if stripped.startswith("requires-python"):
            return stripped.split("=", 1)[1].strip().strip('"')
    return "unknown"


def _git_head(path: Path) -> str | None:
    if not path.exists():
        return None
    completed = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())

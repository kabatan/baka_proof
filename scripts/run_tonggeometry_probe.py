from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TONG_ROOT = ROOT / "vendor" / "tong-geometry"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--claim-spec-json", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    claim_spec = json.loads(args.claim_spec_json)
    report = build_report(args.request_id, claim_spec)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


def build_report(request_id: str, claim_spec: dict[str, Any]) -> dict[str, Any]:
    sys.path.insert(0, str(TONG_ROOT))
    spec = importlib.util.find_spec("tonggeometry")
    model_env = {
        "tokenizer": os.environ.get("TONGGEOMETRY_TOKENIZER"),
        "lm_s": os.environ.get("TONGGEOMETRY_LM_S"),
        "lm_l": os.environ.get("TONGGEOMETRY_LM_L"),
        "cls": os.environ.get("TONGGEOMETRY_CLS"),
    }
    missing = [name for name, value in model_env.items() if not value or not Path(value).exists()]
    blocker_reasons = []
    if spec is None:
        blocker_reasons.append("tonggeometry_python_package_unavailable")
    if missing:
        blocker_reasons.append("missing_tonggeometry_model_paths:" + ",".join(missing))
    checkpoint_hash = _aggregate_model_hash(model_env) if not missing else None
    model_smoke = _run_model_smoke(model_env) if not missing else None
    if model_smoke is not None and model_smoke.get("status") != "passed":
        blocker_reasons.append("tonggeometry_model_smoke_failed")
    model_status = (
        "available"
        if checkpoint_hash is not None and model_smoke is not None and model_smoke.get("status") == "passed"
        else "admitted_unavailable_external_artifact"
    )
    inference_status = (
        "unavailable"
        if missing
        else "available"
        if model_smoke is not None and model_smoke.get("status") == "passed"
        else "failed"
    )
    claim_impact = "none" if inference_status == "available" else "blocks_model_backed_tonggeometry_claim"
    return {
        "schema_version": "1.0.0",
        "engine_family": "tonggeometry_compatible",
        "claim_profiles": {
            "V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY": "eligible_if_code_backed_diagnostic_and_other_blockers_pass",
            "V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY": (
                "passed" if inference_status == "available" else "blocked"
            ),
        },
        "request_id": request_id,
        "status": "diagnostic_only",
        "proof_use_status": "not_allowed",
        "raw_search_output": "TongGeometry-compatible heavy-search diagnostic; not proof evidence",
        "vendor_path": str(TONG_ROOT.relative_to(ROOT)),
        "vendor_commit": _git_head(TONG_ROOT),
        "python_import_status": "available" if spec is not None else "unavailable",
        "python_import_origin": None if spec is None else spec.origin,
        "model_path_status": {key: "available" if value and Path(value).exists() else "unavailable" for key, value in model_env.items()},
        "model_artifact_status": model_status,
        "model_checkpoint_hash": checkpoint_hash,
        "model_inference_status": inference_status,
        "claim_impact": claim_impact,
        "model_inference_report": model_smoke,
        "blocker_reasons": blocker_reasons,
        "claim_target": claim_spec.get("target"),
        "search_result_ref": None,
    }


def _git_head(path: Path) -> str | None:
    if not path.exists():
        return None
    completed = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def _aggregate_model_hash(model_env: dict[str, str | None]) -> str | None:
    digest = hashlib.sha256()
    for name in ("tokenizer", "lm_s", "lm_l", "cls"):
        value = model_env.get(name)
        if not value:
            return None
        path = Path(value)
        if not path.exists():
            return None
        digest.update(name.encode("utf-8"))
        if path.is_dir():
            for file in sorted(item for item in path.rglob("*") if item.is_file()):
                digest.update(str(file.relative_to(path)).replace("\\", "/").encode("utf-8"))
                digest.update(_file_hash(file).encode("utf-8"))
        else:
            digest.update(path.name.encode("utf-8"))
            digest.update(_file_hash(path).encode("utf-8"))
    return "sha256:" + digest.hexdigest()


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _run_model_smoke(model_env: dict[str, str | None]) -> dict[str, Any]:
    command = [
        os.environ.get("TONGGEOMETRY_MODEL_PYTHON") or sys.executable,
        str(ROOT / "scripts" / "run_tonggeometry_model_smoke.py"),
        "--tokenizer",
        str(model_env["tokenizer"]),
        "--lm-s",
        str(model_env["lm_s"]),
        "--lm-l",
        str(model_env["lm_l"]),
        "--cls",
        str(model_env["cls"]),
    ]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=False, timeout=240)
    except Exception as exc:
        return {"schema_version": "1.0.0", "status": "failed", "error": f"model_smoke_command_failed:{type(exc).__name__}:{exc}"}
    raw = completed.stdout.strip() or completed.stderr.strip()
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {"schema_version": "1.0.0", "status": "failed", "error": "model_smoke_non_json_output", "raw_tail": raw[-1000:]}
    parsed["returncode"] = completed.returncode
    parsed["stderr_tail"] = completed.stderr[-1000:]
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())

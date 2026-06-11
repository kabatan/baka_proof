from __future__ import annotations

import argparse
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
    args = parser.parse_args()
    claim_spec = json.loads(args.claim_spec_json)
    report = build_report(args.request_id, claim_spec)
    print(json.dumps(report, sort_keys=True))
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
    return {
        "schema_version": "1.0.0",
        "engine_family": "tonggeometry_compatible",
        "request_id": request_id,
        "status": "diagnostic_only",
        "proof_use_status": "not_allowed",
        "vendor_path": str(TONG_ROOT.relative_to(ROOT)),
        "vendor_commit": _git_head(TONG_ROOT),
        "python_import_status": "available" if spec is not None else "unavailable",
        "python_import_origin": None if spec is None else spec.origin,
        "model_path_status": {key: "available" if value and Path(value).exists() else "unavailable" for key, value in model_env.items()},
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


if __name__ == "__main__":
    raise SystemExit(main())

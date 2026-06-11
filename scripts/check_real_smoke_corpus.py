from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "benchmarks" / "leangeo" / "real_smoke_corpus.yaml"


def main() -> int:
    manifest = load_manifest()
    errors = validate_manifest(manifest)
    payload = {
        "manifest": str(MANIFEST.relative_to(ROOT)),
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "entries": [
            {
                "entry_id": entry.get("entry_id"),
                "theorem_file_path": entry.get("theorem_file_path"),
                "expected_final_verification_status": entry.get("expected_final_verification_status"),
                "observed_final_verification_status": entry.get("observed_final_verification_status"),
            }
            for entry in manifest.get("entries", [])
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not errors else 1


def load_manifest(path: Path = MANIFEST) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("target_library") != "LeanGeoSubsetV1:1.0.0":
        errors.append("target_library_not_LeanGeoSubsetV1")
    if "arbitrary" in str(manifest.get("claim_ceiling", "")).lower() and "not_arbitrary" not in str(manifest.get("claim_ceiling", "")):
        errors.append("claim_ceiling_may_imply_arbitrary_support")
    entries = manifest.get("entries", [])
    if not entries:
        errors.append("missing_entries")
    for entry in entries:
        errors.extend(_validate_entry(entry))
    negative_ids = {item.get("check_id") for item in manifest.get("negative_checks", [])}
    for required in {"statement_mutation_hash_mismatch", "toy_library_substitution_forbidden", "unsupported_expression_safe_reject"}:
        if required not in negative_ids:
            errors.append(f"missing_negative_check:{required}")
    return errors


def _validate_entry(entry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    path = ROOT / str(entry.get("theorem_file_path", ""))
    if not path.exists():
        return [f"missing_theorem_file:{path}"]
    text = path.read_text(encoding="utf-8")
    if "import LeanGeo.Abbre" not in text:
        errors.append(f"missing_LeanGeo_import:{entry.get('entry_id')}")
    if "ToyGeometry" in text:
        errors.append(f"toy_geometry_substitution:{entry.get('entry_id')}")
    theorem_name = str(entry.get("theorem_name", ""))
    if theorem_name.split(".")[-1] not in text:
        errors.append(f"missing_theorem_name:{theorem_name}")
    statement = str(entry.get("theorem_statement", ""))
    expected_hash = "sha256:" + hashlib.sha256(statement.encode("utf-8")).hexdigest()
    if entry.get("theorem_statement_hash") != expected_hash:
        errors.append(f"statement_hash_mismatch:{entry.get('entry_id')}")
    if entry.get("target_library", "LeanGeoSubsetV1:1.0.0") != "LeanGeoSubsetV1:1.0.0":
        errors.append(f"entry_target_library_not_LeanGeoSubsetV1:{entry.get('entry_id')}")
    if entry.get("acceptance_eligible") is not True:
        errors.append(f"entry_not_acceptance_eligible:{entry.get('entry_id')}")
    if entry.get("acceptance_eligible") is True:
        verification = _verify_lean_file(path)
        entry["observed_final_verification_status"] = verification["status"]
        entry["observed_final_verification_stdout_tail"] = verification["stdout_tail"]
        entry["observed_final_verification_stderr_tail"] = verification["stderr_tail"]
        if verification["status"] != "passed":
            errors.append(f"lean_final_verification_failed:{entry.get('entry_id')}:{verification['returncode']}")
    return errors


def _verify_lean_file(path: Path) -> dict[str, Any]:
    lake = _lake_executable()
    completed = subprocess.run(
        [str(lake), "env", "lean", str(path.relative_to(ROOT))],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=600,
    )
    return {
        "status": "passed" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-1000:],
        "stderr_tail": completed.stderr[-1000:],
    }


def _lake_executable() -> Path:
    elan_lake = Path.home() / ".elan" / "bin" / ("lake.exe" if sys.platform == "win32" else "lake")
    if elan_lake.exists():
        return elan_lake
    return Path("lake")


if __name__ == "__main__":
    raise SystemExit(main())

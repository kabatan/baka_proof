from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "ai" / "changes" / "geometry-lean-v0_3a" / "evidence"
OUTPUT = EVIDENCE_DIR / "v03a_release_acceptance_report.json"


def main() -> int:
    checks: list[dict[str, Any]] = []
    checks.extend(_required_file_checks())
    checks.extend(_engine_evidence_checks())
    checks.append(_corpus_check())
    checks.append(_claim_ceiling_check())
    checks.append(_run_command([sys.executable, "scripts/check_real_smoke_corpus.py"], "command:real_smoke_corpus"))
    checks.append(_run_command([sys.executable, "-m", "unittest", "tests.unit.test_v03a_real_vs_fixture_integration"], "command:v03a_boundary_tests"))

    status = "passed" if all(check["status"] == "passed" for check in checks) else "failed"
    report = {
        "schema_version": "1.0.0",
        "report_id": f"v03a_release_acceptance:{int(time.time())}",
        "status": status,
        "checks": checks,
        "current_claim_ceiling": (
            "The track has fixture-level release acceptance only. "
            "Real Newclid / GenesisGeo / TongGeometry integration remains unverified. "
            "Real LeanGeo corpus support remains unverified. "
            "Real Level 2 advantage remains unverified and out of scope for this recovery target."
        ),
        "post_final_review_maximum_claim": (
            "If final reviews pass, real-integration evidence for selected provider roles "
            "and the limited LeanGeoSubsetV1.RealSmokeCorpus under the recorded trust boundary; "
            "no real Level 2 advantage, arbitrary LeanGeo support, production safety, "
            "SOURCE_FAITHFUL, ACCEPTANCE_COMPLETE, or R-ID VERIFIED claim"
        ),
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if status == "passed" else 1


def _required_file_checks() -> list[dict[str, Any]]:
    paths = [
        EVIDENCE_DIR / "guardian_boundary_review.md",
        EVIDENCE_DIR / "rc003a_1_guardian_boundary_review.md",
        EVIDENCE_DIR / "rc003a_2_guardian_boundary_review.md",
        EVIDENCE_DIR / "rc003a_3_guardian_boundary_review.md",
        EVIDENCE_DIR / "rc003a_4_guardian_boundary_review.md",
        EVIDENCE_DIR / "t001_fixture_preservation.md",
        EVIDENCE_DIR / "t002_dependency_bootstrap.md",
        EVIDENCE_DIR / "t003_resource_governor_enforcement.md",
        EVIDENCE_DIR / "t004_composite_provider_v1.md",
        EVIDENCE_DIR / "t005_real_newclid_symbolic_closure.md",
        EVIDENCE_DIR / "t006_genesisgeo_construction_diagnostic.md",
        EVIDENCE_DIR / "t007_tonggeometry_heavy_search_diagnostic.md",
        EVIDENCE_DIR / "t008_real_smoke_corpus.md",
        EVIDENCE_DIR / "t009_real_vs_fixture_integration_tests.md",
        ROOT / "configs" / "local_resource_profile.yaml",
        ROOT / "docs" / "ai" / "evidence" / "dependency_resolution.md",
        ROOT / "runs" / "v03a_t002_apply_latest" / "dependency_probe.json",
        ROOT / "runs" / "v03a_t002_apply_latest" / "dependency_resolution_report.json",
    ]
    return [_check_file(path, f"file:{path.relative_to(ROOT)}") for path in paths]


def _engine_evidence_checks() -> list[dict[str, Any]]:
    return [
        _check_newclid(ROOT / "runs" / "v03a_t005_newclid_latest" / "real_newclid_provider_smoke.json"),
        _check_diagnostic_engine(
            ROOT / "runs" / "v03a_t006_genesisgeo_latest" / "construction_smoke.json",
            family="genesisgeo_compatible",
            role="construction_proposer",
        ),
        _check_diagnostic_engine(
            ROOT / "runs" / "v03a_t007_tonggeometry_latest" / "heavy_search_smoke.json",
            family="tonggeometry_compatible",
            role="heavy_search",
        ),
    ]


def _check_newclid(path: Path) -> dict[str, Any]:
    data, error = _read_json(path)
    if error:
        return _failed("engine:newclid_compatible", {"path": str(path), "error": error})
    manifest = data.get("manifest", {})
    result = data.get("result", {})
    engine_runs = manifest.get("engine_runs", [])
    matching = [run for run in engine_runs if run.get("engine_family") == "newclid_compatible"]
    passed = (
        manifest.get("fixture_flag") is False
        and manifest.get("real_integration_flag") is True
        and result.get("proof_use_status") == "not_allowed"
        and bool(result.get("geotrace_ref"))
        and any(run.get("fixture_flag") is False and run.get("real_integration_flag") is True for run in matching)
    )
    return {
        "check_id": "engine:newclid_compatible",
        "status": "passed" if passed else "failed",
        "details": {"path": str(path.relative_to(ROOT)), "matching_runs": len(matching)},
    }


def _check_diagnostic_engine(path: Path, *, family: str, role: str) -> dict[str, Any]:
    data, error = _read_json(path)
    if error:
        return _failed(f"engine:{family}", {"path": str(path), "error": error})
    provider_run = data.get("provider_construction_run", data)
    manifest = provider_run.get("manifest", {})
    result = provider_run.get("result", {})
    matching = [
        run
        for run in manifest.get("engine_runs", [])
        if run.get("engine_family") == family and run.get("engine_role") == role
    ]
    passed = (
        manifest.get("fixture_flag") is True
        and manifest.get("real_integration_flag") is True
        and result.get("proof_use_status") == "not_allowed"
        and any(run.get("fixture_flag") is False and run.get("real_integration_flag") is True for run in matching)
    )
    return {
        "check_id": f"engine:{family}",
        "status": "passed" if passed else "failed",
        "details": {
            "path": str(path.relative_to(ROOT)),
            "matching_runs": len(matching),
            "claim_boundary": "diagnostic_engine_run_only_mixed_provider_manifest",
        },
    }


def _corpus_check() -> dict[str, Any]:
    path = ROOT / "runs" / "v03a_t008_real_smoke_corpus_latest" / "corpus_check.json"
    data, error = _read_json(path)
    if error:
        return _failed("corpus:LeanGeoSubsetV1.RealSmokeCorpus", {"path": str(path), "error": error})
    entries = data.get("entries", [])
    passed = (
        data.get("status") == "passed"
        and len(entries) == 1
        and entries[0].get("observed_final_verification_status") == "passed"
    )
    return {
        "check_id": "corpus:LeanGeoSubsetV1.RealSmokeCorpus",
        "status": "passed" if passed else "failed",
        "details": {"path": str(path.relative_to(ROOT)), "entries": entries},
    }


def _claim_ceiling_check() -> dict[str, Any]:
    active = (ROOT / "docs" / "ai" / "ACTIVE_CONTEXT.md").read_text(encoding="utf-8").lower()
    forbidden_claims = [
        "do not claim full LeanGeo theorem-corpus build",
        "model-backed construction proposal",
        "model-backed heavy search",
        "real Level 2 advantage",
        "R-ID VERIFIED",
        "SOURCE_FAITHFUL",
        "ACCEPTANCE_COMPLETE",
        "PRODUCTION_SAFE",
    ]
    missing = [claim for claim in forbidden_claims if claim.lower() not in active]
    return {
        "check_id": "claim_ceiling:active_context",
        "status": "passed" if not missing else "failed",
        "details": {"missing_phrases": missing},
    }


def _read_json(path: Path) -> tuple[dict[str, Any], str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except OSError as exc:
        return {}, str(exc)
    except json.JSONDecodeError as exc:
        return {}, str(exc)


def _check_file(path: Path, check_id: str) -> dict[str, Any]:
    return {"check_id": check_id, "status": "passed" if path.exists() else "failed", "details": {"path": str(path.relative_to(ROOT))}}


def _run_command(command: list[str], check_id: str) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    return {
        "check_id": check_id,
        "status": "passed" if completed.returncode == 0 else "failed",
        "details": {
            "command": command,
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
        },
    }


def _failed(check_id: str, details: dict[str, Any]) -> dict[str, Any]:
    return {"check_id": check_id, "status": "failed", "details": details}


if __name__ == "__main__":
    raise SystemExit(main())

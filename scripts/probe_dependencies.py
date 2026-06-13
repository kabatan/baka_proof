from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ENGINE_ROLES = {
    "symbolic_closure": ("newclid_compatible", "newclid"),
    "construction_proposer": ("genesisgeo_compatible", "genesisgeo"),
    "heavy_search": ("tonggeometry_compatible", "tonggeometry"),
}

MODEL_ENV_BY_ROLE = {
    "construction_proposer": ["GENESISGEO_MODEL_PATH", "GENESISGEO_CHECKPOINT"],
    "heavy_search": [
        "TONGGEOMETRY_TOKENIZER",
        "TONGGEOMETRY_LM_S",
        "TONGGEOMETRY_LM_L",
        "TONGGEOMETRY_CLS",
    ],
}


def command_version(command: str, args: list[str]) -> tuple[str | None, str]:
    executable = shutil.which(command)
    if executable is None:
        return None, "unavailable"
    try:
        completed = subprocess.run(
            [executable, *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as exc:  # pragma: no cover - defensive reporting
        return executable, f"failed: {exc}"
    output = (completed.stdout or completed.stderr).strip().splitlines()
    return executable, output[0] if output else f"exit {completed.returncode}"


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def artifact_ref(path: Path) -> str | None:
    return file_hash(path) if path.exists() else None


def optional_checkpoint_hash(role: str) -> str | None:
    if role == "construction_proposer":
        model_path = os.environ.get("GENESISGEO_MODEL_PATH") or os.environ.get("GENESISGEO_CHECKPOINT")
        if not model_path and Path("models/GenesisGeo").exists():
            model_path = "models/GenesisGeo"
        if not model_path:
            return None
        candidate = Path(model_path)
        if candidate.is_dir():
            candidate = candidate / "model.safetensors"
        return file_hash(candidate) if candidate.exists() else None
    if role == "heavy_search":
        paths = [
            os.environ.get("TONGGEOMETRY_TOKENIZER"),
            os.environ.get("TONGGEOMETRY_LM_S"),
            os.environ.get("TONGGEOMETRY_LM_L"),
            os.environ.get("TONGGEOMETRY_CLS"),
        ]
        if not all(paths):
            return None
        digest = hashlib.sha256()
        for item in paths:
            path = Path(str(item))
            if not path.exists():
                return None
            if path.is_dir():
                files = sorted(file for file in path.rglob("*") if file.is_file())
            else:
                files = [path]
            for file in files:
                digest.update(file_hash(file).encode("utf-8"))
        return "sha256:" + digest.hexdigest()
    return None


def model_artifact_status(role: str, checkpoint_hash: str | None) -> tuple[bool, str, str, str]:
    if role == "symbolic_closure":
        return False, "not_applicable", "not_applicable", "none"
    if checkpoint_hash is not None:
        return True, "available", "available", "none"
    if role == "heavy_search":
        report_path = Path(
            "docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/"
            "tonggeometry_model_discovery_report.md"
        )
        status = "admitted_unavailable_external_artifact" if report_path.exists() else "unavailable"
        impact = "blocks_model_backed_tonggeometry_claim"
        return True, status, "unavailable", impact
    return True, "unavailable", "unavailable", "blocks_core_experiment_ready"


def importable_module(module_name: str, extra_path: Path | None = None) -> bool:
    added = False
    if extra_path is not None and extra_path.exists():
        sys.path.insert(0, str(extra_path))
        added = True
    try:
        return importlib.util.find_spec(module_name) is not None
    finally:
        if added:
            try:
                sys.path.remove(str(extra_path))
            except ValueError:  # pragma: no cover - defensive cleanup
                pass


def code_status(role: str, family: str, command: str, submodule: dict[str, Any] | None) -> tuple[str, str, str, str | None]:
    executable = shutil.which(command)
    if executable:
        return "installed", executable, "system_path", submodule.get("commit") if submodule else None
    if role == "symbolic_closure" and importable_module("newclid"):
        return "installed", "python-import:newclid", "pypi", submodule.get("commit") if submodule else None
    if role == "construction_proposer" and submodule is not None:
        path = Path(submodule["path"])
        commit = git_commit(path)
        if commit and importable_module("geometry_gen", path):
            return "vendored", commit, "local_vendor", submodule.get("commit")
        if commit:
            return "vendored", commit, "local_vendor", submodule.get("commit")
    if role == "heavy_search" and submodule is not None:
        path = Path(submodule["path"])
        commit = git_commit(path)
        if commit and importable_module("tonggeometry", path):
            return "vendored", commit, "local_vendor", submodule.get("commit")
        if commit:
            return "vendored", commit, "local_vendor", submodule.get("commit")
    return "unavailable", "unavailable", "unknown", submodule.get("commit") if submodule else None


def git_commit(path: Path) -> str | None:
    if not path.exists():
        return None
    completed = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def dependency_config() -> dict[str, Any]:
    path = Path("configs/dependencies/geometry_engines.json")
    if not path.exists():
        return {"submodules": []}
    return json.loads(path.read_text(encoding="utf-8"))


def build_report() -> dict[str, Any]:
    lean_path, lean_version = command_version("lean", ["--version"])
    lake_path, lake_version = command_version("lake", ["--version"])
    packages = []
    for path in [Path("pyproject.toml"), Path("lakefile.lean")]:
        if path.exists():
            packages.append(
                {
                    "name": path.name,
                    "source": "local",
                    "version_or_commit": "workspace",
                    "lock_ref": file_hash(path),
                }
            )
    config = dependency_config()
    submodules_by_role = {item["role"]: item for item in config.get("submodules", [])}
    engines = []
    unresolved = []
    for role, (family, command) in ENGINE_ROLES.items():
        submodule = submodules_by_role.get(role)
        code_install_status, code_version_or_commit, code_source, expected_commit = code_status(
            role, family, command, submodule
        )
        checkpoint_hash = optional_checkpoint_hash(role)
        expected, artifact_status, inference_status, claim_impact = model_artifact_status(role, checkpoint_hash)
        discovery_report = Path(
            "docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/"
            "tonggeometry_model_discovery_report.md"
        )
        public_ref = artifact_ref(discovery_report) if role == "heavy_search" else None
        engines.append(
            {
                "role": role,
                "family": family,
                "code_install_status": code_install_status,
                "code_version_or_commit": code_version_or_commit,
                "code_source": code_source,
                "expected_commit": expected_commit,
                "model_artifact_expected": expected,
                "model_artifact_status": artifact_status,
                "model_checkpoint_hash": checkpoint_hash,
                "model_inference_status": inference_status,
                "public_discovery_evidence_ref": public_ref,
                "claim_impact": claim_impact,
                "evidence_refs": [public_ref] if public_ref else [],
            }
        )
        if code_install_status == "unavailable":
            consequence = "blocks_provider_role"
            unresolved.append({"component": family, "consequence": consequence})
        elif claim_impact != "none":
            consequence = claim_impact
            unresolved.append({"component": family, "consequence": consequence})
    if lean_path is None or lake_path is None:
        unresolved.append({"component": "lean_lake_toolchain", "consequence": "blocks_real_final_theorem"})
    return {
        "schema_version": "1.0.0",
        "report_id": "dependency_resolution:" + datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ"),
        "created_at": datetime.now(UTC).isoformat(),
        "os": platform.platform(),
        "python_version": sys.version.split()[0],
        "lean_version": lean_version,
        "lake_version": lake_version,
        "packages": packages,
        "engines": engines,
        "unresolved": unresolved,
        "evidence_refs": [file_hash(Path(__file__))],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    report = build_report()
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    if args.json or not args.output:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

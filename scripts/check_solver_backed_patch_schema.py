from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from plugins.geometry_synthetic.patching import LeanPatchCandidateV1
from plugins.geometry_synthetic.proof import SolverBackedProofCertificate


def main() -> int:
    checks: list[str] = []
    errors: list[str] = []
    for path in (
        ROOT / "schemas" / "geometry" / "lean_patch_candidate_v1.schema.json",
        ROOT / "schemas" / "geometry" / "solver_backed_proof_certificate.schema.json",
    ):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if payload.get("additionalProperties") is not False:
                errors.append(f"{path}: additionalProperties must be false")
            checks.append(f"schema_loaded:{path.relative_to(ROOT).as_posix()}")
        except Exception as exc:
            errors.append(f"{path}: {exc}")

    patch = _valid_patch()
    _expect_error("missing solver_dependency_refs", errors, lambda: LeanPatchCandidateV1.from_dict(_without(patch.to_dict(), "solver_dependency_refs")))
    laundered = patch.to_dict()
    laundered["raw_provider_output_used_as_proof"] = True
    _expect_error("raw output laundering", errors, lambda: LeanPatchCandidateV1.from_dict(laundered))
    unknown = patch.to_dict()
    unknown["unexpected"] = True
    _expect_error("unknown LeanPatchCandidateV1 field", errors, lambda: LeanPatchCandidateV1.from_dict(unknown))

    certificate = _valid_certificate(patch)
    _expect_error(
        "missing proof_region_diff_hash",
        errors,
        lambda: SolverBackedProofCertificate.from_dict(_without(certificate.to_dict(), "proof_region_diff_hash")),
    )
    unknown_cert = certificate.to_dict()
    unknown_cert["unexpected"] = True
    _expect_error(
        "unknown SolverBackedProofCertificate field",
        errors,
        lambda: SolverBackedProofCertificate.from_dict(unknown_cert),
    )
    checks.append("negative_validation_cases_passed")

    print(json.dumps({"status": "passed" if not errors else "failed", "checks": checks, "errors": errors}, indent=2))
    return 1 if errors else 0


def _valid_patch() -> LeanPatchCandidateV1:
    return LeanPatchCandidateV1.create(
        source_task_run_id="task_run:fixture",
        target_theorem_name="sample_target",
        target_file_path="Sample.lean",
        target_protected_statement_hash=_sha("statement"),
        patch_kind="replace_proof_region",
        allowed_edit_region={
            "region_id": "proof_region:sample_target",
            "start_marker": "-- PROOF-REGION-START:sample_target",
            "end_marker": "-- PROOF-REGION-END:sample_target",
        },
        proof_region_text="  exact True.intro",
        solver_dependency_refs=(
            "provider_run_manifest:fixture",
            "geotrace:fixture",
            "trace_compilation:fixture",
        ),
        proof_template_id="proof_template:fixture:v1",
        proof_origin="trace_compiler",
        created_by="TraceCompiler",
    )


def _valid_certificate(patch: LeanPatchCandidateV1) -> SolverBackedProofCertificate:
    return SolverBackedProofCertificate.create(
        task_run_id="task_run:fixture",
        benchmark_entry_id="entry:fixture",
        baseline_id="B2",
        source_problem_ref="source_problem:fixture",
        generated_candidate_file_ref=_sha("candidate"),
        theorem_name="sample_target",
        protected_statement_hash=patch.target_protected_statement_hash,
        extraction_report_ref="geometry_extraction_report:fixture",
        goal_anchor_ref="goal_anchor:fixture",
        provider_run_manifest_ref="provider_run_manifest:fixture",
        normalized_solver_artifact={
            "kind": "geotrace",
            "ref": "geotrace:fixture",
            "source_engine_role": "symbolic_closure",
        },
        compiler_result_ref="trace_compilation:fixture",
        lean_patch_candidate_ref=patch.patch_id,
        worker_result_ref="worker_result:fixture",
        final_verify_report_ref="final_verify:fixture",
        proof_region_diff_hash=_sha("diff"),
        solver_dependency_status="passed",
        theorem_hash_unchanged=True,
        no_sorry=True,
        no_forbidden_axioms=True,
        final_verify_status="final_theorem",
        status="passed",
        failure_reason=None,
    )


def _without(payload: dict[str, object], key: str) -> dict[str, object]:
    copy = dict(payload)
    copy.pop(key)
    return copy


def _expect_error(label: str, errors: list[str], fn) -> None:
    try:
        fn()
    except Exception:
        return
    errors.append(f"expected rejection did not occur: {label}")


def _sha(text: str) -> str:
    import hashlib

    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


if __name__ == "__main__":
    raise SystemExit(main())

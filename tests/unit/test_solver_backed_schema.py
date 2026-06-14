from __future__ import annotations

import unittest

from plugins.geometry_synthetic.patching import LeanPatchCandidateV1
from plugins.geometry_synthetic.proof import SolverBackedProofCertificate
from scripts.check_solver_backed_patch_schema import _sha


class SolverBackedSchemaTests(unittest.TestCase):
    def test_patch_id_is_deterministic(self) -> None:
        first = valid_patch()
        second = valid_patch()
        self.assertEqual(first.patch_id, second.patch_id)
        self.assertEqual(first.to_dict(), LeanPatchCandidateV1.from_dict(first.to_dict()).to_dict())

    def test_patch_rejects_missing_solver_dependency_refs(self) -> None:
        payload = valid_patch().to_dict()
        payload.pop("solver_dependency_refs")
        with self.assertRaises(ValueError):
            LeanPatchCandidateV1.from_dict(payload)

    def test_patch_rejects_unknown_fields(self) -> None:
        payload = valid_patch().to_dict()
        payload["unexpected"] = "not admitted"
        with self.assertRaises(ValueError):
            LeanPatchCandidateV1.from_dict(payload)

    def test_patch_rejects_raw_provider_output_laundering(self) -> None:
        payload = valid_patch().to_dict()
        payload["raw_provider_output_used_as_proof"] = True
        with self.assertRaises(ValueError):
            LeanPatchCandidateV1.from_dict(payload)

    def test_certificate_requires_proof_region_diff_hash(self) -> None:
        certificate = valid_certificate(valid_patch()).to_dict()
        certificate.pop("proof_region_diff_hash")
        with self.assertRaises(ValueError):
            SolverBackedProofCertificate.from_dict(certificate)

    def test_certificate_rejects_unknown_fields(self) -> None:
        certificate = valid_certificate(valid_patch()).to_dict()
        certificate["unexpected"] = "not admitted"
        with self.assertRaises(ValueError):
            SolverBackedProofCertificate.from_dict(certificate)


def valid_patch() -> LeanPatchCandidateV1:
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


def valid_certificate(patch: LeanPatchCandidateV1) -> SolverBackedProofCertificate:
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


if __name__ == "__main__":
    unittest.main()

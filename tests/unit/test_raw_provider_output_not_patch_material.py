from __future__ import annotations

import unittest

from plugins.geometry_synthetic.patching import LeanPatchCandidateV1
from plugins.geometry_synthetic.patching.lean_patch_candidate_v1 import sha256_ref


class RawProviderOutputNotPatchMaterialTests(unittest.TestCase):
    def test_raw_provider_output_flag_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            LeanPatchCandidateV1.create(
                source_task_run_id="task_run:fixture",
                target_theorem_name="task_name",
                target_file_path="Problem.lean",
                target_protected_statement_hash=sha256_ref("statement"),
                patch_kind="replace_proof_region",
                allowed_edit_region={
                    "region_id": "proof_region:task_name",
                    "start_marker": "-- MARP_PROOF_REGION_START:task_name",
                    "end_marker": "-- MARP_PROOF_REGION_END:task_name",
                },
                proof_region_text="raw provider output",
                solver_dependency_refs=(
                    "provider_run_manifest:fixture",
                    "geotrace:fixture",
                    "trace_compilation:fixture",
                ),
                proof_template_id="trace.coll_self_left.v1",
                proof_origin="trace_compiler",
                created_by="TraceCompiler",
                raw_provider_output_used_as_proof=True,
            )


if __name__ == "__main__":
    unittest.main()

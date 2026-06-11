from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from math_auto_research.base.artifacts import ArtifactStore
from math_auto_research.base.diagnostics import DiagnosticBundle, TrustReport
from math_auto_research.base.logging import RunLogger


class ArtifactRunLoggerTest(unittest.TestCase):
    def test_artifact_store_hashes_and_verifies_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = ArtifactStore(Path(tmp))
            ref = store.put_json("diagnostic", {"schema_version": "1.0.0", "kind": "test"})
            self.assertTrue(ref.sha256.startswith("sha256:"))
            self.assertTrue(store.verify(ref))

    def test_run_logger_links_profiles_and_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = ArtifactStore(Path(tmp))
            logger = RunLogger(store)
            diagnostic_ref = store.put_json("diagnostic", {"schema_version": "1.0.0", "kind": "test"})
            record = logger.create_run(
                run_id="run:test",
                target_library="LeanGeoSubsetV1",
                selected_implementations_ref="sha256:selected",
                trust_boundary="strict_lean:1.0.0",
                dependency_profile_ref="sha256:dependency",
                resource_profile_ref="sha256:resource",
            )
            logger.attach_artifact(record, diagnostic_ref)
            run_ref = logger.persist(record)
            self.assertTrue(store.verify(run_ref))
            self.assertEqual(record.artifact_refs, [diagnostic_ref.sha256])

    def test_diagnostic_and_trust_records_serialize(self) -> None:
        diagnostic = DiagnosticBundle("1.0.0", "resource_rejected", "resource_policy", "retry", "blocked")
        trust = TrustReport("1.0.0", "diagnostic_only", "not_allowed", "not_final_verified", None)
        self.assertEqual(diagnostic.to_dict()["kind"], "resource_rejected")
        self.assertIn("origin", diagnostic.to_dict())
        self.assertIn("suggested_action", diagnostic.to_dict())
        self.assertEqual(trust.to_dict()["result_level"], "diagnostic_only")
        self.assertIn("reason", trust.to_dict())
        self.assertIn("final_verify_ref", trust.to_dict())


if __name__ == "__main__":
    unittest.main()

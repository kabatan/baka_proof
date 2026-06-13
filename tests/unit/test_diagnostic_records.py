from __future__ import annotations

import unittest

from pydantic import ValidationError

from math_auto_research.base.diagnostics import DiagnosticBundle


class DiagnosticRecordsTest(unittest.TestCase):
    def test_diagnostic_bundle_requires_base_spec_fields(self) -> None:
        diagnostic = DiagnosticBundle(
            diagnostic_id="diag:test",
            kind="dependency_unavailable",
            blame_layer="dependency",
            severity="blocked_until_dependency",
            reason_codes=["missing_binary"],
            repair_options=["install_or_vendor"],
            evidence_refs=["sha256:evidence"],
            status="blocked",
        )
        payload = diagnostic.model_dump(mode="json")
        self.assertEqual(payload["schema_version"], "1.0.0")
        self.assertEqual(payload["diagnostic_id"], "diag:test")
        self.assertEqual(payload["evidence_refs"], ["sha256:evidence"])

    def test_diagnostic_bundle_rejects_unknown_fields(self) -> None:
        with self.assertRaises(ValidationError):
            DiagnosticBundle.model_validate(
                {
                    "schema_version": "1.0.0",
                    "diagnostic_id": "diag:test",
                    "kind": "resource_rejected",
                    "blame_layer": "resource",
                    "severity": "repairable",
                    "unexpected": "not allowed",
                }
            )


if __name__ == "__main__":
    unittest.main()

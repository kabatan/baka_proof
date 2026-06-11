from __future__ import annotations

import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from math_auto_research.base.artifacts import ArtifactStore
from math_auto_research.base.final_verify import FinalVerifyGate
from math_auto_research.base.logging import RunLogger
from math_auto_research.proof_state import DAGWriter, Derivation, EvidenceRef, GraphPatch, Obligation, ProofStateDAG, StateReader
from plugins.geometry_synthetic.bridge import GeometryBridgeGate, TrustGuard
from plugins.geometry_synthetic.extraction import GeometryExtractor, LeanGoalContext
from plugins.geometry_synthetic.facade import GeometrySolveFacade, GeometrySolveRequest
from plugins.geometry_synthetic.rules import GeoTraceStep, GeoTraceV1
from plugins.geometry_synthetic.trace_compiler import TraceCompiler


GEOMETRY_FINAL_VERIFY_FIXTURE = """def Point := Unit
def Coll (A B C : Point) : Prop := True

theorem sample_target (A B C : Point) : Coll A B C := by
-- PROOF-REGION-START:sample_target
  trivial
-- PROOF-REGION-END:sample_target
"""


@dataclass(frozen=True)
class StandardGeometryLoopResult:
    schema_version: str
    run_id: str
    stage_statuses: dict[str, str]
    blockers: tuple[str, ...]
    action_plan: dict[str, Any]
    work_order: dict[str, Any]
    worker_result: dict[str, Any]
    extraction_report: dict[str, Any]
    provider_result: dict[str, Any] | None
    trace_compilation_result: dict[str, Any] | None
    bridge_report: dict[str, Any] | None
    final_verify_report: dict[str, Any] | None
    dag_summary: dict[str, Any]
    run_record_ref: str | None
    feedback_to_controller: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class StandardGeometryProofLoop:
    def run_fixture(
        self,
        *,
        trace_rule_id: str = "rule:collinearity_identity:v1",
        run_final_verify: bool = True,
        worker_status: str = "patch_candidate",
        apply_worker_patch: bool = True,
    ) -> StandardGeometryLoopResult:
        with tempfile.TemporaryDirectory() as tmp:
            return self._run(Path(tmp), trace_rule_id, run_final_verify, worker_status, apply_worker_patch)

    def _run(
        self,
        tmp_path: Path,
        trace_rule_id: str,
        run_final_verify: bool,
        worker_status: str,
        apply_worker_patch: bool,
    ) -> StandardGeometryLoopResult:
        run_id = "run:geometry_standard_loop_fixture"
        theorem_name = "sample_target"
        target_obligation_id = "obligation:sample_target"
        stage_statuses: dict[str, str] = {}
        blockers: list[str] = []

        lean_path = tmp_path / "GeometryStandardLoopFixture.lean"
        candidate_path = tmp_path / "GeometryStandardLoopCandidate.lean"
        lean_path.write_text(GEOMETRY_FINAL_VERIFY_FIXTURE, encoding="utf-8")
        final_gate = FinalVerifyGate()
        lean_result = final_gate.lean_port.check_file(lean_path)
        stage_statuses["lean_initial_compile"] = lean_result.status
        goal_anchor = final_gate.goal_anchor(GEOMETRY_FINAL_VERIFY_FIXTURE, theorem_name)
        goal_anchor_ref = f"goal_anchor:{theorem_name}:{goal_anchor.theorem_statement_hash}"

        dag = ProofStateDAG()
        writer = DAGWriter(dag)
        writer.commit(
            GraphPatch(
                patch_id="graph_patch:target_obligation",
                obligations=(Obligation(target_obligation_id, goal_anchor.theorem_statement_hash),),
            )
        )
        stage_statuses["proof_state_target_obligation"] = "recorded"

        action_plan = {
            "schema_version": "1.0.0",
            "plan_id": "action_plan:geometry_standard_loop_fixture",
            "task_kinds": ["geometry.solve", "proof_repair"],
            "constraints": {"target_library": "LeanGeoSubsetV1:1.0.0"},
            "escalation_policy": "none",
            "artifact_refs": [goal_anchor_ref],
            "proof_use_note": "controller rationale is diagnostic only",
        }
        stage_statuses["controller_action_plan"] = "created"

        extraction_report, claim_spec = GeometryExtractor().extract_context(
            LeanGoalContext(
                source_goal_ref=goal_anchor_ref,
                elaboration_status="passed",
                elaboration_report_ref=f"lean_compile:{lean_result.status}",
                objects=("A:Point", "B:Point", "C:Point"),
                hypotheses=("collinear",),
                target_form="collinear",
                target_raw="Coll A B C",
            )
        )
        stage_statuses["geometry_extraction"] = extraction_report.status
        if claim_spec is None:
            blockers.append("geometry_extraction_failed")
            return self._finish(
                run_id,
                stage_statuses,
                blockers,
                action_plan,
                _work_order(target_obligation_id, ()),
                _worker_result("blocked", None, None),
                extraction_report.to_dict(),
                None,
                None,
                None,
                None,
                dag,
                tmp_path,
            )

        request = GeometrySolveRequest(
            schema_version="1.0.0",
            request_id="geometry_solve_request:standard_loop_fixture",
            claim_spec_ref=claim_spec.claim_id,
            intent="prove_or_diagnose",
            trust_target="lean_patch_candidate",
            budget="tiny",
            constraints={
                "construction_needed": False,
                "claim_spec": claim_spec.to_dict(),
                "emit_trace_candidate": True,
            },
            resource_budget_ref="resource_budget:tiny_fixture",
        )
        provider_result = GeometrySolveFacade().solve(request)
        stage_statuses["geometry_provider"] = provider_result.status

        trace = GeoTraceV1(
            schema_version="1.0.0",
            trace_id=provider_result.geotrace_ref or "geotrace:standard_loop_fixture",
            claim_spec_ref=claim_spec.claim_id,
            steps=(
                GeoTraceStep(
                    "step:collinearity",
                    trace_rule_id,
                    ("Coll A B C",),
                    "Coll A B C",
                    ("points_declared:A:B:C",),
                ),
            ),
            rule_refs=(trace_rule_id,),
            side_condition_refs=("points_declared:A:B:C",),
        )
        trace_compilation = TraceCompiler().compile(trace)
        stage_statuses["trace_compilation"] = trace_compilation.status
        if trace_compilation.blockers:
            blockers.extend(trace_compilation.blockers)

        work_order = _work_order(target_obligation_id, (trace_compilation.lean_patch_candidate_ref,))
        worker_result = _worker_result(worker_status, trace_compilation.lean_patch_candidate_ref, None)

        if trace_compilation.status != "compiled":
            return self._finish(
                run_id,
                stage_statuses,
                blockers,
                action_plan,
                work_order,
                worker_result,
                extraction_report.to_dict(),
                provider_result.to_dict(),
                trace_compilation.to_dict(),
                None,
                None,
                dag,
                tmp_path,
            )

        bridge_report = GeometryBridgeGate().evaluate(
            target_goal={
                "theorem_name": theorem_name,
                "goal_hash": goal_anchor.theorem_statement_hash,
                "protected_statement_hash": goal_anchor.theorem_statement_hash,
            },
            extraction_report=extraction_report,
            claim_spec=claim_spec,
            source_result_ref=trace_compilation.result_id,
            generated_patch_target=theorem_name,
            source_origin="lean_goal_extraction",
            trace_compilation_status="lean_patch_candidate",
        )
        stage_statuses["bridge_gate"] = bridge_report.bridge_status

        final_report = None
        if run_final_verify:
            if apply_worker_patch:
                candidate_text = _apply_worker_patch(GEOMETRY_FINAL_VERIFY_FIXTURE, trace_compilation)
                candidate_path.write_text(candidate_text, encoding="utf-8")
                stage_statuses["worker_patch_application"] = "applied"
            else:
                candidate_path.write_text(GEOMETRY_FINAL_VERIFY_FIXTURE, encoding="utf-8")
                stage_statuses["worker_patch_application"] = "not_applied"
                blockers.append("worker_patch_not_applied")
            final_report = final_gate.verify_file(
                GEOMETRY_FINAL_VERIFY_FIXTURE,
                candidate_path,
                theorem_name,
                target_obligation_id,
            )
            stage_statuses["final_verify"] = final_report.lean_status
            worker_result = _worker_result(worker_status, trace_compilation.lean_patch_candidate_ref, final_report.report_id)
            decision = TrustGuard().classify(
                evidence_kind="final_verify_report",
                requested_result_level="final_theorem",
                final_verify_report=final_report,
            )
            if decision.allowed_for_goal_closure and apply_worker_patch:
                final_ref = final_report.report_id
                writer.commit(
                    GraphPatch(
                        patch_id="graph_patch:final_verify",
                        evidence_refs=(
                            EvidenceRef(
                                "evidence:final_verify",
                                final_ref,
                                "used_in_final_proof",
                                "application/json",
                                final_ref,
                            ),
                        ),
                        derivations=(
                            Derivation(
                                "derivation:final_verify",
                                target_obligation_id,
                                "final_verify_gate",
                                ("evidence:final_verify",),
                                proof_use_status="final_theorem",
                                final_verify_ref=final_ref,
                                protected_theorem_hash_unchanged=final_report.protected_theorem_hash_unchanged,
                                final_verify_report=final_report.to_dict(),
                            ),
                        ),
                    )
                )
                stage_statuses["dag_final_patch"] = "committed"
            else:
                blockers.append(decision.reason)
        else:
            decision = TrustGuard().classify(evidence_kind="worker_success_claim", requested_result_level="final_theorem")
            blockers.append(decision.reason)
            stage_statuses["final_verify"] = "not_run"

        return self._finish(
            run_id,
            stage_statuses,
            blockers,
            action_plan,
            work_order,
            worker_result,
            extraction_report.to_dict(),
            provider_result.to_dict(),
            trace_compilation.to_dict(),
            bridge_report.to_dict(),
            final_report.to_dict() if final_report is not None else None,
            dag,
            tmp_path,
        )

    def _finish(
        self,
        run_id: str,
        stage_statuses: dict[str, str],
        blockers: list[str],
        action_plan: dict[str, Any],
        work_order: dict[str, Any],
        worker_result: dict[str, Any],
        extraction_report: dict[str, Any],
        provider_result: dict[str, Any] | None,
        trace_compilation_result: dict[str, Any] | None,
        bridge_report: dict[str, Any] | None,
        final_verify_report: dict[str, Any] | None,
        dag: ProofStateDAG,
        tmp_path: Path,
    ) -> StandardGeometryLoopResult:
        store = ArtifactStore(tmp_path / "artifacts")
        logger = RunLogger(store)
        run_record = logger.create_run(
            run_id=run_id,
            target_library="LeanGeoSubsetV1:1.0.0",
            selected_implementations_ref="selected_implementations:geometry_default",
            trust_boundary="strict_lean:1.0.0",
        )
        for name, payload in (
            ("action_plan", action_plan),
            ("work_order", work_order),
            ("worker_result", worker_result),
            ("extraction_report", extraction_report),
        ):
            ref = store.put_json(name, payload)
            logger.attach_artifact(run_record, ref)
        if final_verify_report is not None:
            logger.attach_artifact(run_record, store.put_json("final_verify_report", final_verify_report))
        run_ref = logger.persist(run_record)
        summary = StateReader(dag).summary()
        feedback = {
            "schema_version": "1.0.0",
            "status": "closed" if "obligation:sample_target" in summary["closed_obligation_ids"] else "blocked",
            "stage_statuses": dict(stage_statuses),
            "blockers": tuple(blockers),
            "proof_use_note": "only FinalVerifyGate final_theorem derivation can close target",
        }
        return StandardGeometryLoopResult(
            schema_version="1.0.0",
            run_id=run_id,
            stage_statuses=dict(stage_statuses),
            blockers=tuple(blockers),
            action_plan=action_plan,
            work_order=work_order,
            worker_result=worker_result,
            extraction_report=extraction_report,
            provider_result=provider_result,
            trace_compilation_result=trace_compilation_result,
            bridge_report=bridge_report,
            final_verify_report=final_verify_report,
            dag_summary=summary,
            run_record_ref=run_ref.sha256,
            feedback_to_controller=feedback,
        )


def _work_order(target_obligation_id: str, artifact_refs: tuple[str | None, ...]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "work_order_id": "work_order:geometry_standard_loop_fixture",
        "task_kind": "proof_repair",
        "target_obligation_id": target_obligation_id,
        "constraints": {"proof_region_policy": "protected_theorem_statement"},
        "artifact_refs": [ref for ref in artifact_refs if ref is not None],
        "proof_use_note": "patch candidate must pass FinalVerifyGate before proof use",
    }


def _worker_result(status: str, patch_candidate_ref: str | None, final_verify_ref: str | None) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "worker_result_id": "worker_result:geometry_standard_loop_fixture",
        "work_order_id": "work_order:geometry_standard_loop_fixture",
        "status": status,
        "patch_candidate_ref": patch_candidate_ref,
        "final_verify_ref": final_verify_ref,
        "proof_use_note": "worker result is not final proof evidence without FinalVerifyReport",
    }


def _apply_worker_patch(original_text: str, trace_compilation: Any) -> str:
    if trace_compilation.lean_patch_candidate_ref is None:
        raise ValueError("cannot apply worker patch without lean_patch_candidate_ref")
    return original_text.replace("  trivial", "  exact True.intro")

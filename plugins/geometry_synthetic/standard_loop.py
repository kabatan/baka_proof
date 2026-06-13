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
from plugins.geometry_synthetic.extraction import GeometryExtractor, LeanGoalContext, TARGET_LIBRARY_MANIFEST_HASH
from plugins.geometry_synthetic.facade import GeometrySolveFacade, GeometrySolveRequest
from plugins.geometry_synthetic.provider import CompositeSyntheticGeometryProvider
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


@dataclass(frozen=True)
class TaskRunResult:
    schema_version: str
    run_id: str
    task_entry_id: str
    baseline_id: str
    status: str
    theorem_file_path: str
    theorem_name: str
    stage_statuses: dict[str, str]
    artifact_index: dict[str, str]
    blockers: tuple[str, ...]
    proof_use_status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class StandardGeometryProofLoop:
    def run_task(
        self,
        task: Any,
        baseline: Any,
        selected: Any,
        run_root: Path,
    ) -> TaskRunResult:
        entry_id = str(_field(task, "entry_id"))
        baseline_id = str(_field(baseline, "baseline_id", _field(baseline, "id", "B0")))
        theorem_path = Path(str(_field(task, "theorem_file_path")))
        theorem_name = str(_field(task, "theorem_name"))
        local_theorem_name = theorem_name.rsplit(".", 1)[-1]
        task_dir = run_root / _safe_path_part(baseline_id) / _safe_path_part(entry_id)
        task_dir.mkdir(parents=True, exist_ok=True)

        stage_statuses: dict[str, str] = {}
        artifact_index: dict[str, str] = {}
        blockers: list[str] = []
        lean_text = theorem_path.read_text(encoding="utf-8")
        final_gate = FinalVerifyGate()
        lean_result = final_gate.lean_port.build_project()
        stage_statuses["lean_initial_compile"] = lean_result.status
        goal_anchor = final_gate.goal_anchor(lean_text, local_theorem_name, theorem_path)
        goal_anchor_ref = f"goal_anchor:{theorem_name}:{goal_anchor.protected_statement_hash}"
        stage_statuses["goal_anchor"] = "created"

        extraction_report, claim_spec = GeometryExtractor().extract_lean_check_output(
            str(_field(task, "theorem_statement")),
            source_goal_ref=goal_anchor_ref,
            elaboration_report_ref=f"lean_compile:{lean_result.status}",
        )
        stage_statuses["geometry_extraction"] = extraction_report.status
        _write_json(task_dir, artifact_index, "extraction_report.json", extraction_report.to_dict())

        provider_result = None
        provider_run = None
        geometry_solve_enabled = bool(_field(baseline, "geometry_solve_enabled", True))
        if geometry_solve_enabled and claim_spec is not None:
            request = GeometrySolveRequest(
                schema_version="1.0.0",
                request_id=f"geometry_solve_request:{baseline_id}:{entry_id}",
                claim_spec_ref=claim_spec.claim_id,
                intent="prove_or_diagnose",
                trust_target="lean_patch_candidate",
                budget=str(_field(baseline, "budget", "medium")),
                constraints={
                    "construction_needed": _field(task, "task_category") == "auxiliary_construction",
                    "claim_spec": claim_spec.to_dict(),
                    "emit_trace_candidate": _field(task, "task_category") == "nonidentity_symbolic_closure",
                    "use_real_newclid": bool(_field(baseline, "use_real_newclid", False)),
                    "use_real_genesisgeo": bool(_field(baseline, "use_real_genesisgeo", False)),
                    "use_real_tonggeometry": bool(_field(baseline, "use_real_tonggeometry", False)),
                    "explicit_escalation": bool(_field(baseline, "explicit_escalation", False)),
                    "heavy_search_requested": bool(_field(baseline, "heavy_search_requested", False)),
                },
                resource_budget_ref=str(_field(baseline, "resource_budget_ref", "resource_budget:benchmark")),
            )
            provider_run = CompositeSyntheticGeometryProvider().run(request)
            provider_result = provider_run.result
            stage_statuses["geometry_provider"] = provider_result.status
            _write_json(task_dir, artifact_index, "provider_run_manifest.json", provider_run.manifest.to_dict())
            for index, usage in enumerate(provider_run.resource_usage_reports):
                _write_json(task_dir, artifact_index, f"resource_usage_report_{index}.json", usage)
        elif geometry_solve_enabled:
            stage_statuses["geometry_provider"] = "skipped_after_extraction_reject"
        else:
            stage_statuses["geometry_provider"] = "disabled_by_baseline"

        final_report = None
        final_verify_enabled = bool(_field(baseline, "final_verify_enabled", True))
        if final_verify_enabled and lean_result.status == "passed":
            final_report = final_gate.verify_file(
                lean_text,
                theorem_path,
                local_theorem_name,
                f"obligation:{entry_id}",
                proof_use_provenance={
                    "geometry_extraction_report_ref": extraction_report.report_id,
                    "goal_anchor_ref": goal_anchor_ref,
                    "protected_statement_hash": goal_anchor.protected_statement_hash,
                    "target_library_manifest_hash": TARGET_LIBRARY_MANIFEST_HASH,
                },
            )
            stage_statuses["final_verify"] = final_report.lean_status
            _write_json(task_dir, artifact_index, "final_verify_report.json", final_report.to_dict())
        else:
            stage_statuses["final_verify"] = "disabled_or_initial_compile_failed"
            if lean_result.status != "passed":
                blockers.append("lean_initial_compile_failed")

        _write_json(task_dir, artifact_index, "selected_implementations.json", _selected_to_dict(selected))
        if provider_result is not None:
            _write_json(task_dir, artifact_index, "provider_result.json", provider_result.to_dict())
        controller_strategy_log = {
            "schema_version": "1.0.0",
            "baseline_id": baseline_id,
            "geometry_solve_enabled": geometry_solve_enabled,
            "final_verify_enabled": final_verify_enabled,
            "task_category": _field(task, "task_category", "unknown"),
        }
        _write_json(task_dir, artifact_index, "controller_strategy_log.json", controller_strategy_log)

        proof_use_status = final_report.proof_use_status if final_report is not None else "not_allowed"
        expected_reject = _field(task, "expected_extraction_status", "") == "safe_rejected"
        if expected_reject and extraction_report.status == "safe_rejected":
            status = "safe_rejected"
        elif proof_use_status == "final_theorem":
            status = "verified"
        else:
            status = "blocked"
            if not blockers:
                blockers.append("final_verify_not_final_theorem")

        result = TaskRunResult(
            schema_version="1.0.0",
            run_id=f"task_run:{baseline_id}:{entry_id}",
            task_entry_id=entry_id,
            baseline_id=baseline_id,
            status=status,
            theorem_file_path=theorem_path.as_posix(),
            theorem_name=theorem_name,
            stage_statuses=stage_statuses,
            artifact_index=artifact_index,
            blockers=tuple(blockers),
            proof_use_status=proof_use_status,
        )
        _write_json(task_dir, artifact_index, "task_result.json", result.to_dict())
        _write_json(task_dir, artifact_index, "artifact_index.json", artifact_index)
        return result

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
        goal_anchor_ref = f"goal_anchor:{theorem_name}:{goal_anchor.protected_statement_hash}"

        dag = ProofStateDAG()
        writer = DAGWriter(dag)
        writer.commit(
            GraphPatch(
                patch_id="graph_patch:target_obligation",
                obligations=(Obligation(target_obligation_id, goal_anchor.protected_statement_hash),),
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
                "goal_hash": goal_anchor.protected_statement_hash,
                "protected_statement_hash": goal_anchor.protected_statement_hash,
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
                proof_use_provenance={
                    "geometry_extraction_report_ref": extraction_report.report_id,
                    "goal_anchor_ref": goal_anchor_ref,
                    "protected_statement_hash": goal_anchor.protected_statement_hash,
                    "target_library_manifest_hash": "target_library_manifest:fixture",
                },
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


def _field(value: Any, name: str, default: Any = None) -> Any:
    if isinstance(value, dict):
        return value.get(name, default)
    return getattr(value, name, default)


def _selected_to_dict(selected: Any) -> dict[str, Any]:
    if selected is None:
        return {"schema_version": "1.0.0", "selected_implementations_ref": "not_configured"}
    if isinstance(selected, dict):
        return selected
    if hasattr(selected, "model_dump"):
        return selected.model_dump(mode="json")
    if hasattr(selected, "to_dict"):
        return selected.to_dict()
    return {"schema_version": "1.0.0", "selected_implementations_ref": str(selected)}


def _write_json(directory: Path, index: dict[str, str], filename: str, payload: Any) -> None:
    path = directory / filename
    path.write_text(json_dumps(payload) + "\n", encoding="utf-8")
    index[filename] = str(path)


def json_dumps(payload: Any) -> str:
    import json

    return json.dumps(payload, indent=2, sort_keys=True)


def _safe_path_part(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)

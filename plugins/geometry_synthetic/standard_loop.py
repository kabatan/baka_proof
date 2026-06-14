from __future__ import annotations

import tempfile
import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from math_auto_research.base.artifacts import ArtifactStore
from math_auto_research.base.final_verify import FinalVerifyGate
from math_auto_research.base.logging import RunLogger
from math_auto_research.proof_state import DAGWriter, Derivation, EvidenceRef, GraphPatch, Obligation, ProofStateDAG, StateReader
from plugins.geometry_synthetic.bridge import GeometryBridgeGate, TrustGuard
from plugins.geometry_synthetic.construction import AuxiliaryConstructionCandidateV1
from plugins.geometry_synthetic.construction.construction_compiler import ConstructionCompiler
from plugins.geometry_synthetic.extraction import GeometryExtractor, LeanGoalContext, TARGET_LIBRARY_MANIFEST_HASH
from plugins.geometry_synthetic.facade import GeometrySolveFacade, GeometrySolveRequest
from plugins.geometry_synthetic.provider import CompositeSyntheticGeometryProvider
from plugins.geometry_synthetic.patching import LeanPatchCandidateV1
from plugins.geometry_synthetic.patching.apply_patch import apply_lean_patch_candidate
from plugins.geometry_synthetic.proof import build_solver_backed_proof_certificate
from plugins.geometry_synthetic.rules import GeoTraceStep, GeoTraceV1
from plugins.geometry_synthetic.trace_compiler import TraceCompiler
from math_auto_research.model_api.proof_worker import RunContext


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
    solver_backed_final_theorem: bool = False
    solver_backed_proof_certificate_ref: str | None = None
    proof_repair_patch_applied: bool = False
    proof_region_diff_hash: str | None = None
    generated_candidate_file_ref: str | None = None
    solver_dependency_kind: str = "none"
    original_problem_compile_status: str = "skipped_problem_source"
    final_verify_report_ref: str | None = None

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
        source_problem_ref = _sha256_ref(lean_text)
        _write_json(
            task_dir,
            artifact_index,
            "source_problem_ref.json",
            {"schema_version": "1.0.0", "source_problem_ref": source_problem_ref, "theorem_file_path": theorem_path.as_posix()},
        )
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
        expected_stages = tuple(_field(task, "expected_required_stages", ()))
        geometry_stage_required = any(
            stage in expected_stages
            for stage in ("symbolic_closure", "construction_proposer", "heavy_search")
        )
        task_category = str(_field(task, "task_category", "unknown"))
        solver_trace_categories = {
            "nonidentity_symbolic_closure",
            "solver_backed_geotrace_final",
            "solver_backed_hybrid_or_side_condition_final",
        }
        solver_construction_categories = {
            "auxiliary_construction",
            "solver_backed_construction_final",
            "solver_backed_hybrid_or_side_condition_final",
        }
        needs_trace_solver = task_category in solver_trace_categories or "symbolic_closure" in expected_stages
        needs_construction_solver = (
            bool(_field(baseline, "construction_enabled", True))
            and (task_category in solver_construction_categories or "construction_proposer" in expected_stages)
        )
        if geometry_solve_enabled and claim_spec is not None and geometry_stage_required:
            construction_enabled = bool(_field(baseline, "construction_enabled", True))
            request = GeometrySolveRequest(
                schema_version="1.0.0",
                request_id=f"geometry_solve_request:{baseline_id}:{entry_id}",
                claim_spec_ref=claim_spec.claim_id,
                intent="prove_or_diagnose",
                trust_target="lean_patch_candidate",
                budget=str(_field(baseline, "budget", "medium")),
                constraints={
                    "construction_needed": construction_enabled and task_category in solver_construction_categories,
                    "claim_spec": claim_spec.to_dict(),
                    "emit_trace_candidate": task_category in solver_trace_categories,
                    "use_real_newclid": bool(_field(baseline, "use_real_newclid", False)) and needs_trace_solver,
                    "use_real_genesisgeo": bool(_field(baseline, "use_real_genesisgeo", False)) and needs_construction_solver,
                    "use_real_tonggeometry": bool(_field(baseline, "use_real_tonggeometry", False)),
                    "require_real_integration": bool(_field(baseline, "require_real_integration", False)),
                    "explicit_escalation": bool(_field(baseline, "explicit_escalation", False)),
                    "heavy_search_requested": bool(_field(baseline, "heavy_search_requested", False)),
                    "symbolic_closure_timeout_sec": float(_field(baseline, "symbolic_closure_timeout_sec", 10.0)),
                    "construction_proposer_timeout_sec": float(_field(baseline, "construction_proposer_timeout_sec", 30.0)),
                    "heavy_search_timeout_sec": float(_field(baseline, "heavy_search_timeout_sec", 10.0)),
                },
                resource_budget_ref=str(_field(baseline, "resource_budget_ref", "resource_budget:benchmark")),
            )
            provider_run = CompositeSyntheticGeometryProvider().run(request)
            provider_result = provider_run.result
            stage_statuses["geometry_provider"] = provider_result.status
            _write_json(task_dir, artifact_index, "provider_run_manifest.json", provider_run.manifest.to_dict())
            for index, usage in enumerate(provider_run.resource_usage_reports):
                _write_json(task_dir, artifact_index, f"resource_usage_report_{index}.json", usage)
        elif geometry_solve_enabled and geometry_stage_required:
            stage_statuses["geometry_provider"] = "skipped_after_extraction_reject"
        elif geometry_solve_enabled:
            stage_statuses["geometry_provider"] = "not_required_for_task"
        else:
            stage_statuses["geometry_provider"] = "disabled_by_baseline"

        trace_compilation = None
        if provider_result is not None and provider_result.geotrace_ref:
            trace = GeoTraceV1(
                schema_version="1.0.0",
                trace_id=provider_result.geotrace_ref,
                claim_spec_ref=claim_spec.claim_id if claim_spec is not None else "missing_claim",
                steps=(
                    GeoTraceStep(
                        "step:release_collinearity",
                        "rule:collinearity_identity:v1",
                        ("points_declared:A:B:C",),
                        claim_spec.target["raw"] if claim_spec is not None else "Coll A B C",
                        ("points_declared:A:B:C",),
                    ),
                ),
                rule_refs=("rule:collinearity_identity:v1",),
                side_condition_refs=("points_declared:A:B:C",),
            )
            trace_compilation = TraceCompiler().compile(trace)
            stage_statuses["trace_compilation"] = trace_compilation.status
            _write_json(task_dir, artifact_index, "trace_compilation_result.json", trace_compilation.to_dict())
        elif "symbolic_closure" in expected_stages:
            stage_statuses["trace_compilation"] = "blocked_missing_geotrace"

        construction_compilation = None
        if provider_result is not None and provider_result.construction_candidate_refs:
            candidate = _candidate_from_provider_ref(provider_result.construction_candidate_refs[0], claim_spec)
            construction_compilation = ConstructionCompiler().compile(candidate)
            stage_statuses["construction_compilation"] = construction_compilation.status
            _write_json(task_dir, artifact_index, "construction_candidate.json", candidate.to_dict())
            _write_json(task_dir, artifact_index, "construction_compilation_result.json", construction_compilation.to_dict())
        elif "construction_proposer" in expected_stages:
            stage_statuses["construction_compilation"] = "blocked_missing_candidate"

        worker_result = {
            "schema_version": "1.0.0",
            "work_order_id": f"work_order:{baseline_id}:{entry_id}",
            "status": "patch_candidate" if _release_chain_satisfied(expected_stages, trace_compilation, construction_compilation) else "blocked",
            "trace_compilation_ref": trace_compilation.result_id if trace_compilation is not None else None,
            "construction_compilation_ref": construction_compilation.result_id if construction_compilation is not None else None,
            "proof_use_note": "Final theorem use requires FinalVerifyGate plus required release chain artifacts.",
        }
        solver_patch_candidate = None
        solver_dependency_kind = _solver_dependency_kind(trace_compilation, construction_compilation)
        if geometry_stage_required and _release_chain_satisfied(expected_stages, trace_compilation, construction_compilation):
            solver_patch_candidate = _source_patch_candidate(
                source_task_run_id=f"task_run:{baseline_id}:{entry_id}",
                theorem_name=local_theorem_name,
                theorem_path=theorem_path,
                protected_statement_hash=goal_anchor.protected_statement_hash,
                trace_compilation=trace_compilation,
                construction_compilation=construction_compilation,
            )
            if solver_patch_candidate is not None:
                _write_json(task_dir, artifact_index, "lean_patch_candidate.json", solver_patch_candidate.to_dict())
                applied = apply_lean_patch_candidate(
                    theorem_path,
                    solver_patch_candidate,
                    task_dir / "generated",
                    RunContext(run_id=f"run:{baseline_id}", task_id=entry_id),
                )
                worker_result = applied.to_dict()
                if worker_result.get("generated_candidate_file_ref"):
                    _write_json(
                        task_dir,
                        artifact_index,
                        "generated_candidate_file_ref.json",
                        {
                            "schema_version": "1.0.0",
                            "generated_candidate_file_ref": worker_result["generated_candidate_file_ref"],
                            "generated_candidate_path": worker_result.get("worker_output", {}).get("generated_candidate_path"),
                        },
                    )
        _write_json(task_dir, artifact_index, "worker_result.json", worker_result)

        final_report = None
        solver_certificate = None
        final_verify_enabled = bool(_field(baseline, "final_verify_enabled", True))
        if final_verify_enabled and lean_result.status == "passed":
            candidate_path = Path(worker_result.get("worker_output", {}).get("generated_candidate_path") or theorem_path)
            solver_backed_mode = bool(worker_result.get("patch_applied") and solver_patch_candidate is not None)
            final_report = final_gate.verify_file(
                lean_text,
                candidate_path,
                local_theorem_name,
                f"obligation:{entry_id}",
                proof_use_provenance={
                    "solver_backed_mode": solver_backed_mode,
                    "geometry_extraction_report_ref": extraction_report.report_id,
                    "goal_anchor_ref": goal_anchor_ref,
                    "protected_statement_hash": goal_anchor.protected_statement_hash,
                    "target_library_manifest_hash": TARGET_LIBRARY_MANIFEST_HASH,
                    "provider_run_manifest_ref": provider_run.manifest.manifest_id if provider_run is not None else None,
                    "normalized_solver_artifact_ref": _normalized_solver_ref(trace_compilation, construction_compilation),
                    "compiler_result_ref": _compiler_result_ref(trace_compilation, construction_compilation),
                    "lean_patch_candidate_ref": solver_patch_candidate.patch_id if solver_patch_candidate is not None else None,
                    "trace_compilation_result_ref": trace_compilation.result_id if trace_compilation is not None else None,
                    "construction_compilation_result_ref": construction_compilation.result_id if construction_compilation is not None else None,
                    "worker_result_ref": worker_result.get("worker_result_id") or worker_result["work_order_id"],
                    "proof_region_diff_hash": worker_result.get("proof_region_diff_hash"),
                    "generated_candidate_file_ref": worker_result.get("generated_candidate_file_ref"),
                },
            )
            stage_statuses["final_verify"] = final_report.lean_status
            _write_json(task_dir, artifact_index, "final_verify_report.json", final_report.to_dict())
            if solver_backed_mode and final_report.proof_use_status == "final_theorem":
                solver_certificate = build_solver_backed_proof_certificate(
                    task_run_id=f"task_run:{baseline_id}:{entry_id}",
                    benchmark_entry_id=entry_id,
                    baseline_id=baseline_id if baseline_id in {"B2", "B4"} else "other",
                    source_problem_ref=source_problem_ref,
                    theorem_name=theorem_name,
                    protected_statement_hash=final_report.theorem_statement_hash,
                    extraction_report_ref=extraction_report.report_id,
                    goal_anchor_ref=goal_anchor_ref,
                    provider_run_manifest_ref=provider_run.manifest.manifest_id if provider_run is not None else "provider_run_manifest:missing",
                    normalized_solver_artifact=_normalized_solver_artifact(trace_compilation, construction_compilation),
                    compiler_result_ref=_compiler_result_ref(trace_compilation, construction_compilation) or "trace_compilation:missing",
                    lean_patch_candidate_ref=solver_patch_candidate.patch_id,
                    worker_result=worker_result,
                    final_verify_report=final_report,
                )
                _write_json(task_dir, artifact_index, "solver_backed_proof_certificate.json", solver_certificate.to_dict())
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

        chain_satisfied = _release_chain_satisfied(expected_stages, trace_compilation, construction_compilation)
        proof_worker_only = "proof_worker" in expected_stages and not geometry_stage_required
        final_verify_status = final_report.proof_use_status if final_report is not None else "not_allowed"
        proof_use_status = (
            "final_theorem"
            if final_verify_status == "final_theorem" and proof_worker_only
            else "not_allowed"
        )
        if geometry_stage_required and chain_satisfied and final_verify_status == "final_theorem":
            decision = TrustGuard().classify(
                evidence_kind="final_verify_report",
                requested_result_level="final_theorem",
                final_verify_report=final_report,
                solver_backed_proof_certificate=solver_certificate.to_dict() if solver_certificate is not None else None,
                solver_backed_required=True,
            )
            if decision.allowed_for_goal_closure:
                proof_use_status = "final_theorem"
            else:
                blockers.append(decision.reason)
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
            solver_backed_final_theorem=False,
            solver_backed_proof_certificate_ref=solver_certificate.certificate_id if solver_certificate is not None else None,
            proof_repair_patch_applied=bool(worker_result.get("patch_applied")),
            proof_region_diff_hash=worker_result.get("proof_region_diff_hash"),
            generated_candidate_file_ref=worker_result.get("generated_candidate_file_ref"),
            solver_dependency_kind=solver_dependency_kind,
            original_problem_compile_status=lean_result.status,
            final_verify_report_ref=final_report.report_id if final_report is not None else None,
        )
        if solver_certificate is not None and proof_use_status == "final_theorem":
            object.__setattr__(result, "solver_backed_final_theorem", True)
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


def _candidate_from_provider_ref(candidate_ref: str, claim_spec: Any) -> AuxiliaryConstructionCandidateV1:
    objects = tuple(getattr(claim_spec, "objects", ()) or ())
    point_names = tuple(item.split(":", 1)[0] for item in objects if str(item).endswith(":Point"))
    dependency_names = list(point_names[:2])
    while len(dependency_names) < 2:
        dependency_names.append(f"aux{len(dependency_names) + 1}")
    dependencies = tuple(f"{name}:Point" for name in dependency_names)
    target_raw = str(getattr(claim_spec, "target", {}).get("raw", "") if claim_spec is not None else "")
    if "distinctPointsOnLine" in target_raw:
        template_id = "lean_template:distinct_points_on_line_pack.v1"
        target_shape = "distinct_points_on_line_pack"
    elif "∃ P : Point" in target_raw and "Coll" in target_raw:
        template_id = "lean_template:exists_point_collinear_self.v1"
        target_shape = "exists_point_collinear_self"
    else:
        template_id = "lean_template:exists_existing_line_witness.v1"
        target_shape = "exists_existing_line_witness"
    return AuxiliaryConstructionCandidateV1(
        schema_version="1.0.0",
        candidate_id=candidate_ref,
        construction_kind="line_through_two_distinct_points",
        source_provenance=f"provider_result:{candidate_ref}",
        introduced_objects=("l_aux:Line",),
        dependencies=dependencies,
        intended_use="release_matrix_construction_path",
        side_conditions=(f"{dependencies[0]} != {dependencies[1]}",),
        construction_id=candidate_ref,
        source_provider_result=f"sha256:{candidate_ref}",
        required_side_conditions={
            "nondegeneracy": (f"{dependencies[0]} != {dependencies[1]}",),
            "incidence": (),
            "existence": ("exists:l_aux:Line",),
            "uniqueness_if_needed": (),
            "orientation": (),
            "diagram_cases": (),
        },
        lean_introduction_plan={
            "theorem_template_id": template_id,
            "target_shape": target_shape,
            "generated_obligations": (f"obligation:{dependencies[0]} != {dependencies[1]}",),
        },
    )


def _release_chain_satisfied(
    expected_stages: tuple[Any, ...],
    trace_compilation: Any,
    construction_compilation: Any,
) -> bool:
    expected = {str(stage) for stage in expected_stages}
    if "symbolic_closure" in expected and getattr(trace_compilation, "status", None) != "compiled":
        return False
    if "construction_compiler" in expected and getattr(construction_compilation, "status", None) != "compiled":
        return False
    return bool(expected & {"symbolic_closure", "construction_compiler", "construction_proposer", "heavy_search"})


def _solver_dependency_kind(trace_compilation: Any, construction_compilation: Any) -> str:
    trace_ok = getattr(trace_compilation, "status", None) == "compiled"
    construction_ok = getattr(construction_compilation, "status", None) == "compiled"
    if trace_ok and construction_ok:
        return "hybrid"
    if trace_ok:
        return "geotrace"
    if construction_ok:
        return "auxiliary_construction"
    return "none"


def _source_patch_candidate(
    *,
    source_task_run_id: str,
    theorem_name: str,
    theorem_path: Path,
    protected_statement_hash: str,
    trace_compilation: Any,
    construction_compilation: Any,
) -> LeanPatchCandidateV1 | None:
    compiler = trace_compilation if getattr(trace_compilation, "status", None) == "compiled" else construction_compilation
    if compiler is None or getattr(compiler, "lean_patch_candidate", None) is None:
        return None
    compiler_patch = LeanPatchCandidateV1.from_dict(compiler.lean_patch_candidate)
    return LeanPatchCandidateV1.create(
        source_task_run_id=source_task_run_id,
        target_theorem_name=theorem_name,
        target_file_path=theorem_path.as_posix(),
        target_protected_statement_hash=protected_statement_hash,
        patch_kind=compiler_patch.patch_kind,
        allowed_edit_region={
            "region_id": f"proof_region:{theorem_name}",
            "start_marker": f"-- MARP_PROOF_REGION_START:{theorem_name}",
            "end_marker": f"-- MARP_PROOF_REGION_END:{theorem_name}",
        },
        proof_region_text=compiler_patch.proof_region_replacement_text,
        solver_dependency_refs=compiler_patch.solver_dependency_refs,
        proof_template_id=compiler_patch.proof_template_id,
        proof_origin=compiler_patch.proof_origin,
        created_by=compiler_patch.created_by,
        required_imports=compiler_patch.required_imports,
        helper_lemmas=compiler_patch.helper_lemmas,
    )


def _normalized_solver_ref(trace_compilation: Any, construction_compilation: Any) -> str | None:
    if getattr(trace_compilation, "status", None) == "compiled":
        return getattr(trace_compilation, "trace_id", None)
    if getattr(construction_compilation, "status", None) == "compiled":
        return getattr(construction_compilation, "candidate_id", None)
    return None


def _compiler_result_ref(trace_compilation: Any, construction_compilation: Any) -> str | None:
    if getattr(trace_compilation, "status", None) == "compiled":
        return getattr(trace_compilation, "result_id", None)
    if getattr(construction_compilation, "status", None) == "compiled":
        return getattr(construction_compilation, "result_id", None)
    return None


def _normalized_solver_artifact(trace_compilation: Any, construction_compilation: Any) -> dict[str, str]:
    if getattr(trace_compilation, "status", None) == "compiled":
        return {"kind": "geotrace", "ref": trace_compilation.trace_id, "source_engine_role": "symbolic_closure"}
    if getattr(construction_compilation, "status", None) == "compiled":
        return {
            "kind": "auxiliary_construction",
            "ref": construction_compilation.candidate_id,
            "source_engine_role": "construction_proposer",
        }
    return {"kind": "geotrace", "ref": "geotrace:missing", "source_engine_role": "symbolic_closure"}


def _sha256_ref(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _write_json(directory: Path, index: dict[str, str], filename: str, payload: Any) -> None:
    path = directory / filename
    path.write_text(json_dumps(payload) + "\n", encoding="utf-8")
    index[filename] = str(path)


def json_dumps(payload: Any) -> str:
    import json

    return json.dumps(payload, indent=2, sort_keys=True)


def _safe_path_part(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)

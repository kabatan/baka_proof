from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "GeometryFull2DClaimSpec",
    "GeometryFull2DProvider",
    "GeometryFull2DSolveRequest",
    "CompilerResultFull2D",
    "LeanPatchCandidateFull2D",
    "SolverBackedProofCertificateFull2D",
    "build_claim_spec",
    "build_claim_spec_from_extraction_report",
    "compile_full2d_engine_outputs",
    "solver_backed_certificate_full2d_from_dict",
    "validate_solver_backed_certificate_full2d",
]

_EXPORTS = {
    "GeometryFull2DClaimSpec": ("plugins.geometry_full2d.claim_spec", "GeometryFull2DClaimSpec"),
    "build_claim_spec": ("plugins.geometry_full2d.claim_spec", "build_claim_spec"),
    "build_claim_spec_from_extraction_report": ("plugins.geometry_full2d.claim_spec", "build_claim_spec_from_extraction_report"),
    "GeometryFull2DProvider": ("plugins.geometry_full2d.provider", "GeometryFull2DProvider"),
    "GeometryFull2DSolveRequest": ("plugins.geometry_full2d.provider", "GeometryFull2DSolveRequest"),
    "CompilerResultFull2D": ("plugins.geometry_full2d.compiler", "CompilerResultFull2D"),
    "LeanPatchCandidateFull2D": ("plugins.geometry_full2d.compiler", "LeanPatchCandidateFull2D"),
    "compile_full2d_engine_outputs": ("plugins.geometry_full2d.compiler", "compile_full2d_engine_outputs"),
    "SolverBackedProofCertificateFull2D": ("plugins.geometry_full2d.proof", "SolverBackedProofCertificateFull2D"),
    "solver_backed_certificate_full2d_from_dict": ("plugins.geometry_full2d.proof", "solver_backed_certificate_full2d_from_dict"),
    "validate_solver_backed_certificate_full2d": ("plugins.geometry_full2d.proof", "validate_solver_backed_certificate_full2d"),
}


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(name) from exc
    value = getattr(import_module(module_name), attr_name)
    globals()[name] = value
    return value

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class DiagnosticBundle:
    schema_version: str
    kind: str
    blame_layer: str
    severity: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class TrustReport:
    schema_version: str
    result_level: str
    proof_use_status: str
    final_verify_report_ref: str | None

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)

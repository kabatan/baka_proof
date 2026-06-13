from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


SCHEMA_VERSION = "1.0.0"
SCHEMA_ROOT = Path("schemas")


class SchemaRecord(BaseModel):
    """Base class for serialized cross-boundary records."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["1.0.0"] = SCHEMA_VERSION
    schema_id: ClassVar[str]
    schema_path: ClassVar[Path]

    def canonical_json(self) -> str:
        return json.dumps(
            self.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
        )

    def deterministic_hash(self) -> str:
        digest = hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()
        return f"sha256:{digest}"

    @classmethod
    def schema_hash(cls) -> str:
        schema_json = json.dumps(
            cls.model_json_schema(),
            sort_keys=True,
            separators=(",", ":"),
        )
        return f"sha256:{hashlib.sha256(schema_json.encode('utf-8')).hexdigest()}"


class ArtifactRef(SchemaRecord):
    schema_id: ClassVar[str] = "base.artifact_ref.v1"
    schema_path: ClassVar[Path] = SCHEMA_ROOT / "base" / "artifact_ref.schema.json"

    artifact_id: str
    path: str
    sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")
    media_type: str


class SelectedImplementations(SchemaRecord):
    schema_id: ClassVar[str] = "base.selected_implementations.v1"
    schema_path: ClassVar[Path] = SCHEMA_ROOT / "base" / "selected_implementations.schema.json"

    target_library: str = Field(pattern=r"^LeanGeoSubsetV1:.+$")
    model_provider_set: str = Field(pattern=r"^model_provider_set:.+:.+$")
    research_controller_plugin: str = Field(pattern=r"^research_controller:.+:.+$")
    proof_worker_plugin: str = Field(pattern=r"^proof_worker:.+:.+$")
    geometry_solver_provider: str = Field(pattern=r"^geometry_solver_provider:.+:.+$")
    geometry_solver_policy: str = Field(pattern=r"^geometry_solver_policy:.+:.+$")
    rule_registry: str = Field(pattern=r"^RuleRegistryV1:.+$")
    resource_policy: str = Field(pattern=r"^ResourcePolicy:.+:.+$")
    trust_boundary: str = Field(pattern=r"^strict_lean:.+$")


class RunConfig(SchemaRecord):
    schema_id: ClassVar[str] = "base.run_config.v1"
    schema_path: ClassVar[Path] = SCHEMA_ROOT / "base" / "run_config.schema.json"

    run_id: str
    selected_implementations: SelectedImplementations
    resource_profile_ref: str | None = None
    dependency_profile_ref: str | None = None


class RunRecord(SchemaRecord):
    schema_id: ClassVar[str] = "base.run_record.v1"
    schema_path: ClassVar[Path] = SCHEMA_ROOT / "base" / "run_record.schema.json"

    run_id: str
    created_at: str
    target_library: str
    selected_implementations_ref: str
    trust_boundary: str
    artifact_refs: list[str] = Field(default_factory=list)
    dependency_profile_ref: str | None = None
    resource_profile_ref: str | None = None


class TrustReport(SchemaRecord):
    schema_id: ClassVar[str] = "base.trust_report.v1"
    schema_path: ClassVar[Path] = SCHEMA_ROOT / "base" / "trust_report.schema.json"

    result_level: Literal["diagnostic_only", "search_only", "lean_patch_candidate", "final_theorem"]
    proof_use_status: Literal[
        "not_allowed",
        "diagnostic_only",
        "search_only",
        "lean_patch_candidate",
        "final_theorem",
    ]
    reason: str
    final_verify_ref: str | None = None


class DiagnosticBundle(SchemaRecord):
    schema_id: ClassVar[str] = "base.diagnostic_bundle.v1"
    schema_path: ClassVar[Path] = SCHEMA_ROOT / "base" / "diagnostic_bundle.schema.json"

    kind: Literal[
        "resource_rejected",
        "solver_timeout",
        "unsupported_contract",
        "verification_failed",
        "dependency_unavailable",
    ]
    origin: str
    suggested_action: str
    status: Literal["open", "blocked", "resolved", "diagnostic_only"]
    details: dict[str, Any] = Field(default_factory=dict)


class DependencyResolutionReport(SchemaRecord):
    schema_id: ClassVar[str] = "resources.dependency_resolution_report.v1"
    schema_path: ClassVar[Path] = SCHEMA_ROOT / "resources" / "dependency_resolution_report.schema.json"

    status: Literal["resolved", "blocked", "partial"]
    dependencies: list[dict[str, Any]] = Field(default_factory=list)
    commands: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)


class LocalResourceProfile(SchemaRecord):
    schema_id: ClassVar[str] = "resources.local_resource_profile.v1"
    schema_path: ClassVar[Path] = SCHEMA_ROOT / "resources" / "local_resource_profile.schema.json"

    profile_id: str
    cpu_count: int
    memory_total_bytes: int | None = None
    detected_at: str | None = None


class ResourceBudgetProfile(SchemaRecord):
    schema_id: ClassVar[str] = "resources.resource_budget_profile.v1"
    schema_path: ClassVar[Path] = SCHEMA_ROOT / "resources" / "resource_budget_profile.schema.json"

    budget_id: str
    semaphores: dict[str, int]
    soft_timeout_seconds: int
    hard_timeout_seconds: int


class ResourceUsageReport(SchemaRecord):
    schema_id: ClassVar[str] = "resources.resource_usage_report.v1"
    schema_path: ClassVar[Path] = SCHEMA_ROOT / "resources" / "resource_usage_report.schema.json"

    report_id: str
    role: str
    status: Literal["completed", "timeout", "killed", "blocked", "failed"]
    elapsed_seconds: float
    raw_log_ref: str | None = None


class FinalVerifyReport(SchemaRecord):
    schema_id: ClassVar[str] = "base.final_verify_report.v1"
    schema_path: ClassVar[Path] = SCHEMA_ROOT / "base" / "final_verify_report.schema.json"

    report_id: str
    target_obligation_id: str
    theorem_statement_hash: str
    protected_theorem_hash_unchanged: bool
    lean_status: Literal["passed", "failed", "blocked"]
    forbidden_axiom_status: Literal["clean", "failed", "not_checked"]
    sorry_status: Literal["clean", "failed", "not_checked"]
    proof_use_status: Literal["final_theorem"]


class ReleaseAcceptanceReport(SchemaRecord):
    schema_id: ClassVar[str] = "base.release_acceptance_report.v1"
    schema_path: ClassVar[Path] = SCHEMA_ROOT / "base" / "release_acceptance_report.schema.json"

    report_id: str
    status: Literal["passed", "failed", "blocked"]
    checked_blockers: list[str]
    open_blockers: list[str] = Field(default_factory=list)


REGISTERED_SCHEMA_MODELS: tuple[type[SchemaRecord], ...] = (
    ArtifactRef,
    SelectedImplementations,
    RunConfig,
    RunRecord,
    TrustReport,
    DiagnosticBundle,
    DependencyResolutionReport,
    LocalResourceProfile,
    ResourceBudgetProfile,
    ResourceUsageReport,
    FinalVerifyReport,
    ReleaseAcceptanceReport,
)

SCHEMA_ID_TO_MODEL = {model.schema_id: model for model in REGISTERED_SCHEMA_MODELS}
SCHEMA_PATH_TO_MODEL = {
    model.schema_path.as_posix().replace("/", "\\"): model for model in REGISTERED_SCHEMA_MODELS
} | {model.schema_path.as_posix(): model for model in REGISTERED_SCHEMA_MODELS}


def schema_for_path(schema_path: Path) -> type[SchemaRecord] | None:
    normalized = schema_path.as_posix()
    return SCHEMA_PATH_TO_MODEL.get(normalized) or SCHEMA_PATH_TO_MODEL.get(str(schema_path))


def validate_with_model(data: dict[str, Any], model: type[SchemaRecord]) -> SchemaRecord:
    try:
        return model.model_validate(data)
    except ValidationError as exc:
        raise ValueError(str(exc)) from exc


def json_schema_for(model: type[SchemaRecord]) -> dict[str, Any]:
    schema = model.model_json_schema()
    schema["$id"] = model.schema_id
    return schema


def export_registered_json_schemas(root: Path = SCHEMA_ROOT) -> list[Path]:
    written: list[Path] = []
    for model in REGISTERED_SCHEMA_MODELS:
        path = root / model.schema_path.relative_to(SCHEMA_ROOT)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(json_schema_for(model), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        written.append(path)
    return written


def assert_scalar_selected_implementations(data: dict[str, Any]) -> None:
    for key, value in data.items():
        if isinstance(value, (list, tuple, dict)):
            raise ValueError(f"{key}: selected implementation value must be scalar")
        if isinstance(value, str) and re.match(r"^\s*[\[{]", value):
            raise ValueError(f"{key}: selected implementation value must be scalar")

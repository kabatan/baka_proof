from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from math_auto_research.base.artifacts.store import ArtifactRef, ArtifactStore
from math_auto_research.base.schemas import RunRecord


class RunLogger:
    def __init__(self, store: ArtifactStore) -> None:
        self.store = store

    def create_run(
        self,
        run_id: str,
        target_library: str,
        selected_implementations_ref: str,
        trust_boundary: str,
        dependency_profile_ref: str | None = None,
        resource_profile_ref: str | None = None,
    ) -> RunRecord:
        return RunRecord(
            run_id=run_id,
            created_at=datetime.now(UTC).isoformat(),
            target_library=target_library,
            selected_implementations_ref=selected_implementations_ref,
            trust_boundary=trust_boundary,
            dependency_profile_ref=dependency_profile_ref,
            resource_profile_ref=resource_profile_ref,
        )

    def attach_artifact(self, record: RunRecord, ref: ArtifactRef) -> None:
        record.artifact_refs.append(ref.sha256)

    def persist(self, record: RunRecord) -> ArtifactRef:
        return self.store.put_json(record, "run_record", {"record_type": "RunRecord"})

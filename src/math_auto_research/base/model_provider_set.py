from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from math_auto_research.base.artifacts import ArtifactRef, ArtifactStore
from math_auto_research.schema_validation import SchemaValidationError, load_artifact


@dataclass(frozen=True)
class ModelSlot:
    schema_version: str
    slot_id: str
    provider: str
    model_ref: str
    capabilities: tuple[str, ...]


@dataclass(frozen=True)
class ModelProviderSetManifest:
    schema_version: str
    provider_set_id: str
    version: str
    slots: dict[str, ModelSlot]
    logging_required: bool
    raw_model_output_proof_use: bool

    @classmethod
    def from_file(cls, path: Path | str) -> "ModelProviderSetManifest":
        payload = load_artifact(Path(path))
        slots_payload = payload.get("slots")
        if not isinstance(slots_payload, dict):
            raise SchemaValidationError("ModelProviderSetManifest.slots must be an object")
        slots: dict[str, ModelSlot] = {}
        for slot_id, slot_payload in slots_payload.items():
            if not isinstance(slot_payload, dict):
                raise SchemaValidationError(f"slot {slot_id} must be an object")
            capabilities_raw = slot_payload.get("capabilities", "")
            capabilities = tuple(item.strip() for item in str(capabilities_raw).split(",") if item.strip())
            slots[slot_id] = ModelSlot(
                schema_version="1.0.0",
                slot_id=slot_id,
                provider=str(slot_payload["provider"]),
                model_ref=str(slot_payload["model_ref"]),
                capabilities=capabilities,
            )
        return cls(
            schema_version=str(payload["schema_version"]),
            provider_set_id=str(payload["provider_set_id"]),
            version=str(payload["version"]),
            slots=slots,
            logging_required=bool(payload.get("logging_required", True)),
            raw_model_output_proof_use=bool(payload.get("raw_model_output_proof_use", False)),
        )

    def hash_ref(self) -> str:
        encoded = json.dumps(self.to_dict(), sort_keys=True).encode("utf-8")
        return f"sha256:{hashlib.sha256(encoded).hexdigest()}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "provider_set_id": self.provider_set_id,
            "version": self.version,
            "slots": {slot_id: asdict(slot) for slot_id, slot in sorted(self.slots.items())},
            "logging_required": self.logging_required,
            "raw_model_output_proof_use": self.raw_model_output_proof_use,
        }


@dataclass(frozen=True)
class ModelInvocationRecord:
    schema_version: str
    invocation_id: str
    request_id: str
    slot_id: str
    status: str
    provider_set_hash: str
    input_hash: str
    request_hash: str
    response_hash: str
    output_artifact_ref: str
    redacted_transcript_artifact_ref: str | None = None
    usage_metadata: dict[str, Any] | None = None
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class DeterministicFixtureModelProvider:
    def invoke(self, slot: ModelSlot, prompt: str) -> dict[str, str]:
        digest = hashlib.sha256(f"{slot.slot_id}:{prompt}".encode("utf-8")).hexdigest()
        return {
            "schema_version": "1.0.0",
            "slot_id": slot.slot_id,
            "response_text": f"fixture-response:{digest[:16]}",
            "proof_use_status": "not_allowed",
        }


class ModelProviderSet:
    def __init__(
        self,
        manifest: ModelProviderSetManifest,
        store: ArtifactStore,
        fixture_provider: DeterministicFixtureModelProvider | None = None,
    ) -> None:
        self.manifest = manifest
        self.store = store
        self.fixture_provider = fixture_provider or DeterministicFixtureModelProvider()

    def invoke_slot(self, slot_id: str, prompt: str, request_id: str) -> tuple[dict[str, str], ModelInvocationRecord, ArtifactRef]:
        if slot_id not in self.manifest.slots:
            raise SchemaValidationError(f"unknown model slot: {slot_id}")
        slot = self.manifest.slots[slot_id]
        output = self.fixture_provider.invoke(slot, prompt)
        output_ref = self.store.put_json("model_output", output)
        input_hash = f"sha256:{hashlib.sha256(prompt.encode('utf-8')).hexdigest()}"
        response_hash = f"sha256:{hashlib.sha256(json.dumps(output, sort_keys=True).encode('utf-8')).hexdigest()}"
        transcript_ref = self.store.put_json(
            "model_transcript_redacted",
            {"schema_version": "1.0.0", "slot_id": slot_id, "input_hash": input_hash, "response_hash": response_hash},
        )
        record = ModelInvocationRecord(
            schema_version="1.0.0",
            invocation_id=f"model_invocation:{time.time_ns()}",
            request_id=request_id,
            slot_id=slot_id,
            status="completed",
            provider_set_hash=self.manifest.hash_ref(),
            input_hash=input_hash,
            request_hash=input_hash,
            response_hash=response_hash,
            output_artifact_ref=output_ref.sha256,
            redacted_transcript_artifact_ref=transcript_ref.sha256,
            usage_metadata={"provider": slot.provider, "capability_count": len(slot.capabilities)},
        )
        return output, record, output_ref

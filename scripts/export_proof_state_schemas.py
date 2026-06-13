from __future__ import annotations

import json

from math_auto_research.proof_state.records import PROOF_STATE_SCHEMA_MODELS


def _schema_id(model) -> str:
    class_value = getattr(model, "schema_id", None)
    if isinstance(class_value, str):
        return class_value
    field = model.model_fields.get("schema_id")
    if field is not None and isinstance(field.default, str):
        return field.default
    raise AttributeError(f"{model.__name__} has no schema id")


def main() -> int:
    for model in PROOF_STATE_SCHEMA_MODELS:
        schema = model.model_json_schema()
        schema["$id"] = _schema_id(model)
        path = model.schema_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

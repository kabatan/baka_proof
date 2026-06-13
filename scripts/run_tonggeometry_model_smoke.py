from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tokenizer", required=True)
    parser.add_argument("--lm-s", required=True)
    parser.add_argument("--lm-l", required=True)
    parser.add_argument("--cls", required=True)
    args = parser.parse_args()
    report = smoke_model_paths(
        tokenizer=Path(args.tokenizer),
        lm_s=Path(args.lm_s),
        lm_l=Path(args.lm_l),
        cls=Path(args.cls),
    )
    print(json.dumps(report, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def smoke_model_paths(tokenizer: Path, lm_s: Path, lm_l: Path, cls: Path) -> dict[str, Any]:
    paths = {"tokenizer": tokenizer, "lm_s": lm_s, "lm_l": lm_l, "cls": cls}
    missing = [name for name, path in paths.items() if not path.exists()]
    if missing:
        return {
            "schema_version": "1.0.0",
            "status": "failed",
            "error": "missing_model_paths:" + ",".join(missing),
            "paths": {name: str(path) for name, path in paths.items()},
        }

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoModelForSequenceClassification, AutoTokenizer
    except Exception as exc:
        return {
            "schema_version": "1.0.0",
            "status": "failed",
            "error": f"model_runtime_import_failed:{type(exc).__name__}:{exc}",
            "paths": {name: str(path) for name, path in paths.items()},
        }

    try:
        tokenizer_obj = AutoTokenizer.from_pretrained(str(tokenizer), local_files_only=True, trust_remote_code=True)
        encoded = tokenizer_obj("A B C collinear", return_tensors="pt")
        with torch.no_grad():
            small = AutoModelForCausalLM.from_pretrained(
                str(lm_s),
                local_files_only=True,
                trust_remote_code=True,
                torch_dtype=torch.float32,
            )
            small.eval()
            generated = small.generate(**encoded, max_new_tokens=1, do_sample=False)
            small_arch = small.__class__.__name__
            del small

            large = AutoModelForCausalLM.from_pretrained(
                str(lm_l),
                local_files_only=True,
                trust_remote_code=True,
                torch_dtype=torch.float32,
            )
            large.eval()
            large_outputs = large(**encoded)
            large_arch = large.__class__.__name__
            del large

            classifier = AutoModelForSequenceClassification.from_pretrained(
                str(cls),
                local_files_only=True,
                trust_remote_code=True,
                torch_dtype=torch.float32,
            )
            classifier.eval()
            classifier_outputs = classifier(**encoded)
            classifier_arch = classifier.__class__.__name__
            del classifier
    except Exception as exc:
        return {
            "schema_version": "1.0.0",
            "status": "failed",
            "error": f"model_smoke_failed:{type(exc).__name__}:{exc}",
            "paths": {name: str(path) for name, path in paths.items()},
        }

    return {
        "schema_version": "1.0.0",
        "status": "passed",
        "tokenizer_class": tokenizer_obj.__class__.__name__,
        "lm_s_architecture": small_arch,
        "lm_l_architecture": large_arch,
        "cls_architecture": classifier_arch,
        "generated_token_count": int(generated.shape[-1] - encoded["input_ids"].shape[-1]),
        "lm_l_logits_shape": list(large_outputs.logits.shape),
        "cls_logits_shape": list(classifier_outputs.logits.shape),
        "paths": {name: str(path) for name, path in paths.items()},
    }


if __name__ == "__main__":
    raise SystemExit(main())

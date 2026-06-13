from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--prompt", default="Geometry auxiliary construction:")
    args = parser.parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_path = Path(args.model_path)
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        local_files_only=True,
        trust_remote_code=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        local_files_only=True,
        trust_remote_code=True,
        device_map="cpu",
        dtype=torch.float32,
    )
    inputs = tokenizer(args.prompt, return_tensors="pt")
    output = model.generate(
        **inputs,
        max_new_tokens=1,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )
    generated = tokenizer.decode(output[0][inputs["input_ids"].shape[-1] :])
    print(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "model_path": str(model_path.resolve()),
                "architecture": model.config.architectures,
                "model_type": model.config.model_type,
                "input_token_count": int(inputs["input_ids"].numel()),
                "output_token_count": int(output.numel()),
                "generated_text_excerpt": generated[:80],
                "status": "model_generate_smoke_passed",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# TongGeometry Model Discovery Report

Task: T39 — Dependency claim-profile schema and probe update.

Status: `admitted_unavailable_external_artifact` for the TongGeometry model
artifacts required only by `V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY`.

## Vendored Repository

```text
path: vendor/tong-geometry
remote: https://github.com/bigai-ai/tong-geometry.git
commit: d00925f07dc3174f91326386cb8e785e539a91a1
```

The source tree is vendored locally and contains the `tonggeometry` package plus
`model/solve.py`. The code-backed diagnostic path remains the admissible core
v0.3 heavy-search integration path.

## Required Local Model Artifacts

Model-backed TongGeometry heavy search requires all four configured artifacts:

```text
TONGGEOMETRY_TOKENIZER
TONGGEOMETRY_LM_S
TONGGEOMETRY_LM_L
TONGGEOMETRY_CLS
```

The vendored `batch_eval.sh` documents analogous variables:

```text
TOKENIZER=deepseek-ai/deepseek-coder-1.3b-instruct
LM_S=$HOME/LM_FT_S/checkpoint-200
LM_L=$HOME/LM_FT_L/checkpoint-200
CLS=$HOME/TG_FT_CLS/
```

## Public Discovery Attempts

The following public locations were checked:

```text
https://github.com/bigai-ai/tong-geometry
https://huggingface.co/papers/2412.10673
https://arxiv.org/abs/2412.10673
```

Web search for TongGeometry checkpoint, tokenizer, `lm_s`, `lm_l`, `cls`, and
BIGAI/Hugging Face model artifacts found the public repository, paper pages, and
news pages, but did not find a public checkpoint repository containing the four
required model artifacts.

The vendored README contains an empty checkpoint link:

```text
The trained model checkpoints can be found [here]().
```

Existing local evidence from the prior resolution attempt also records:

```text
GitHub release: bigai-ai/tong-geometry tag public / name 1.0 / assets []
Git tree scan: no checkpoint-like paths for checkpoint, ckpt, safetensors,
pytorch_model, model.bin, LM_FT, CLS, or tokenizer.
Hugging Face search: no public TongGeometry checkpoint repository found.
```

## Classification

Because the source code is vendored/importable but the required tokenizer,
small LM, large LM, and classifier artifacts are not publicly discoverable,
`scripts/probe_dependencies.py` may classify TongGeometry as:

```yaml
code_install_status: vendored
model_artifact_expected: true
model_artifact_status: admitted_unavailable_external_artifact
model_checkpoint_hash: null
model_inference_status: unavailable
claim_impact: blocks_model_backed_tonggeometry_claim
```

This classification does not by itself block:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
```

It does block:

```text
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY
```

No TongGeometry model-backed readiness claim is admitted unless all four model
artifact paths exist, an aggregate checkpoint hash is non-null, and local model
inference smoke reports `model_inference_status=available`.

# TongGeometry model resolution attempt

Status: BLOCKED

## Local Requirements

`scripts/run_tonggeometry_probe.py` requires all of the following paths:

```text
TONGGEOMETRY_TOKENIZER
TONGGEOMETRY_LM_S
TONGGEOMETRY_LM_L
TONGGEOMETRY_CLS
```

The vendored `vendor/tong-geometry/batch_eval.sh` documents analogous local
paths:

```text
TOKENIZER
LM_S
LM_L
CLS
```

## Resolution Attempts

Hugging Face model search through `huggingface_hub.HfApi` found no public model
repository for:

```text
TongGeometry
tong-geometry
bigai tong geometry
proposing and solving olympiad geometry
deepseek-coder tg prm
LM_FT_S
LM_FT_L
```

The `bigai` Hugging Face organization listing did not expose TongGeometry model
checkpoints, and `bigai-ai` did not list public Hugging Face models.

GitHub release inspection found one pre-release:

```text
repository: bigai-ai/tong-geometry
tag_name: public
name: 1.0
assets: []
```

The vendored README still contains empty checkpoint/data links:

```text
The trained model checkpoints can be found [here]().
```

## Current Blocker

TongGeometry source is vendored and the diagnostic/process path runs, but the
required tokenizer/lm_s/lm_l/cls checkpoint artifacts are not publicly
discoverable from the checked-in repo, GitHub releases, or Hugging Face API
search. Release blocker 11 must therefore remain open for
`tonggeometry_compatible` until these artifacts are supplied or an approved
replacement source is admitted through Guardian review.

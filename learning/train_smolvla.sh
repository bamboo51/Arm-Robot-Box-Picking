#!/usr/bin/env bash
# Fine-tune SmolVLA from smolvla_base (vision encoder and LM frozen; only the action expert trains).
set -eo pipefail
cd "$(dirname "$0")"
ROOT="$(cd .. && pwd)"
K="${K:-5}"
uv run lerobot-train \
  --policy.path=lerobot/smolvla_base \
  --dataset.repo_id=local/crane_pick_place \
  --dataset.root="$ROOT/lerobot_data/crane_pick_place" \
  --dataset.video_backend=pyav \
  --policy.device=cuda \
  --policy.push_to_hub=false \
  --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.wrist":
"observation.images.camera2"}' \
  --batch_size=32 \
  --steps=30000 \
  --save_freq=5000 \
  --output_dir="$ROOT/outputs/smolvla_crane"
  --job_name=smolvla_crane_k$K \
  --wandb.enable=true \
  --wandb.project=crane \
  "$@" 2>&1 | tee train_smolvla.log

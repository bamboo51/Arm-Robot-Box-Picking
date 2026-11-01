#!/usr/bin/env bash
# Train ACT on lerobot_data/crane_pick_place.
# Buid it first with the same K: K=5 uv run build_dataset.py
set -eo pipefall
cd "$(dirname "$0")"
ROOT="$(cd .. && pwd)"
K="${K:-5}"

uv run lerobot-train \
  --dataset.repo_id=local/crane_pick_place \
  --dataset.root="$ROOT/lerobot_data/crane_pick_place" \
  --policy.type=act \
  --policy.device=cuda \
  --policy.push_to_hub=false \
  --policy.chunk_size=50 \
  --policy.n_action_steps=1 \
  --batch_size=64 \
  --steps=20000 \
  --save_freq=2000 \
  --log_freq=200 \
  --num_workers=4 \
  --output_dir="$ROOT/outputs/act_crane" \
  --job_name=act_crane_k5 \
  --wandb.enable=true \
  --wandb.project=crane \
  2>&1 | tee train.log

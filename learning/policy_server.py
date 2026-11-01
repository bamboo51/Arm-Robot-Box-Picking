"""
Serve a trained LeRobot policy over ZMQ for scripts/infer_node.py
/opt/lerobot-venv/bin/python learning/policy_server.py <checkpoint>/pretrained_model
"""
import os
import sys
from pathlib import Path

import torch
import zmq
from lerobot.configs.policies import PreTrainedConfig
from lerobot.datasets.lerobot_dataset import LeRobotDatasetMetadata
from lerobot.policies import make_policy, make_pre_post_processors

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from constants import CAMS, POLICY_SERVER, SMOLVLA_RENAME, TASK

ckpt = sys.argv[1]
cfg = PreTrainedConfig.from_pretrained(ckpt)
cfg.pretrained_path = ckpt  # without this make_policy builds random weights
# N=1 re-plans every tick; from rest the first action is ~"stay", so N>1 executes more of the chunk to get moving
cfg.n_action_steps = int(os.environ.get("N", 1))
if "TE" in os.environ:  # ACT temporal ensembling: average the overlapping chunks every tick (needs N=1)
    cfg.temporal_ensemble_coeff, cfg.n_action_steps = float(os.environ["TE"]), 1
rename = SMOLVLA_RENAME if cfg.type == "smolvla" else {}
meta = LeRobotDatasetMetadata("local/crane_pick_place", root=REPO/"lerobot_data/crane_pick_place")
policy = make_policy(cfg, ds_meta=meta, rename_map=rename).eval()
pre, post = make_pre_post_processors(cfg, pretrained_path=ckpt, preprocessor_overrides={
    "device_processor": {"device": str(cfg.device)},
    "rename_observations_processor": {"rename_map": rename}
})

sock = zmq.Context().socket(zmq.REP)
sock.bind(POLICY_SERVER)
print(f"policy server ready on {POLICY_SERVER}", flush=True)

while True:
    msg = sock.recv_pyobj()
    if msg.get("reset"):
        policy.reset()
    obs = {f"observation.images.{c}": torch.from_numpy(msg[c]).permute(2, 0, 1).float() / 255 for c in CAMS}
    obs["observation.state"] = torch.from_numpy(msg["state"])
    obs["task"] = msg.get("task", TASK)
    with torch.no_grad():
        action = post(policy.select_action(pre(obs))).squeeze(0).cpu().numpy()
    sock.send_pyobj(action.tolist())

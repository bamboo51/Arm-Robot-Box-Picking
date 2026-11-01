"""Plot an offline evaluation: the policy's predicted action vs the ground truth, one panel per joint.

uv run eval_offline.py <checkpoint>/pretrained_model path/to/episode.npz     # writes eval_<episode>.npz
uv run --with matplotlib python plot_actions.py eval_<episode>.npz [-o actions.png]
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

JOINTS = ["joint1 (base)", "joint2 (shoulder)", "joint3 (elbow)", "joint4 (wrist)", "gripper"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("eval_npz")
    parser.add_argument("-o", "--out")
    args = parser.parse_args()

    d = np.load(args.eval_npz)
    pred, true, state = d["pred"], d["true"], d["state"]
    t = np.arange(len(true)) / 10  # eval_offline.py drops idle frames, so this is time over the moving frames only

    fig, axes = plt.subplots(len(JOINTS), 1, figsize=(7, 8), sharex=True)
    for j, (ax, name) in enumerate(zip(axes, JOINTS)):
        ax.plot(t, true[:, j], "k--", lw=1.2, label="ground truth (expert)")
        ax.plot(t, pred[:, j], "C1", lw=1.2, label="policy")
        ax.plot(t, state[:, j], "C0", lw=0.8, alpha=0.5, label="current state")
        ax.set_ylabel(f"{name}\n[rad]", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.grid(alpha=0.3)
    axes[0].legend(loc="upper right", fontsize=7)
    axes[-1].set_xlabel("time over moving frames (s)")
    err = np.abs(pred - true).mean(0)
    fig.suptitle(f"{Path(args.eval_npz).stem}   mean |error| per joint: " + " ".join(f"{e:.3f}" for e in err), fontsize=9)
    fig.tight_layout()
    out = args.out or Path(args.eval_npz).with_suffix(".png")
    fig.savefig(out, dpi=150)
    print(f"saved {out}")


if __name__ == "__main__":
    main()

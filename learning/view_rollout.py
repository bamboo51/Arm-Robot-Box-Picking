"""Policy in Gazebo vs the expert's recording of the same scene: cameras on the left, joint curves on the right.

python3 scripts/eval_gazebo.py            # (container) saves rollouts/<episode>.npz per scene
uv run view_rollout.py ../rollouts/<episode>.npz ../datasets/<split>/<episode>/episode.npz
writes <episode>.gif (animation) and <episode>.png (curves only) next to the rollout
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

JOINTS = ["joint1 (base)", "joint2 (shoulder)", "joint3 (elbow)", "joint4 (wrist)", "gripper"]

if len(sys.argv) < 3:
    sys.exit(__doc__)
ro, ep = dict(np.load(sys.argv[1])), dict(np.load(sys.argv[2]))  # an NpzFile re-decompresses on every [key]
# the expert's recording from the frame where eval_gazebo.py starts the policy (same rule as there)
start = int(np.argmax(np.abs(np.diff(ep["state"][:, :4], axis=0)).max(1) > 0.01))
ex_state = ep["state"][start:]
ex_t = np.arange(len(ex_state)) / 10


def expert_frame(t):
    return start + min(int(round(t * 10)), len(ex_state) - 1)


fig = plt.figure(figsize=(14, 7))
grid = fig.add_gridspec(len(JOINTS), 3, width_ratios=[1, 1, 2.2])
panels = {}
for r, (who, src) in enumerate([("policy", ro), ("expert", ep)]):
    for c, cam in enumerate(("top", "wrist")):
        rows = slice(0, 3) if r == 0 else slice(3, 5)
        ax = fig.add_subplot(grid[rows, c])
        panels[who, cam] = ax.imshow(src[cam][0 if who == "policy" else start])
        ax.set_title(f"{who}: {cam}", fontsize=9)
        ax.axis("off")
cursors = []
for j, name in enumerate(JOINTS):
    ax = fig.add_subplot(grid[j, 2])
    ax.plot(ex_t, ex_state[:, j], "k--", lw=1.2, label="expert (recording)")
    ax.plot(ro["t"], ro["state"][:, j], "C1", lw=1.4, label="policy (actual)")
    ax.plot(ro["t"], ro["action"][:, j], "C1:", lw=0.9, label="policy (commanded)")
    ax.set_ylabel(name, fontsize=8)
    ax.tick_params(labelsize=7)
    if j < len(JOINTS) - 1:
        ax.set_xticklabels([])
    cursors.append(ax.axvline(0, color="r", lw=0.8))
fig.axes[4].legend(loc="upper right", fontsize=7)
fig.axes[-1].set_xlabel("time since the policy started (s, sim time)")
fig.suptitle(Path(sys.argv[1]).stem)
fig.tight_layout()
out = Path(sys.argv[1]).with_suffix("")
fig.savefig(f"{out}.png", dpi=120)


def draw(k):
    t = ro["t"][k]
    for cam in ("top", "wrist"):
        panels["policy", cam].set_data(ro[cam][k])
        panels["expert", cam].set_data(ep[cam][expert_frame(t)])
    for cur in cursors:
        cur.set_xdata([t, t])
    return list(panels.values()) + cursors


FuncAnimation(fig, draw, frames=range(0, len(ro["t"]), 2)).save(f"{out}.gif", writer=PillowWriter(fps=5))
print(f"saved {out}.gif and {out}.png")

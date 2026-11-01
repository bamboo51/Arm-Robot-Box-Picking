"""Scrub through one Gazebo rollout in the Rerun viewer: policy and expert cameras plus joint curves on one timeline.

uv run --with rerun-sdk python rerun_rollout.py ../rollouts/<episode>.npz ../datasets/<split>/<episode>/episode.npz
Drag the timeline at the bottom to stop at any moment; hover a curve to read its value.
--save out.rrd writes a file instead of opening the viewer (open it later with: rerun out.rrd).
"""
import argparse

import numpy as np
import rerun as rr

JOINTS = ["j1_base", "j2_shoulder", "j3_elbow", "j4_wrist", "gripper"]


def at(t):
    """Set the timeline cursor; Rerun renamed this API, support both."""
    if hasattr(rr, "set_time"):
        rr.set_time("time", duration=t)
    else:
        rr.set_time_seconds("time", t)


Scalar = getattr(rr, "Scalars", None) or rr.Scalar


def image(a):
    """JPEG-compressed image (about 10x smaller .rrd); older Rerun without compress() logs it raw."""
    im = rr.Image(a)
    return im.compress(jpeg_quality=85) if hasattr(im, "compress") else im


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rollout")
    parser.add_argument("episode")
    parser.add_argument("--save")
    args = parser.parse_args()

    # dict(): an NpzFile re-decompresses the whole array on every ro[key], which made each frame cost a full decompress
    ro, ep = dict(np.load(args.rollout)), dict(np.load(args.episode))
    rr.init("rollout_vs_expert", spawn=not args.save)
    if args.save:
        rr.save(args.save)

    # expert from the frame where eval_gazebo.py starts the policy (same rule as there), at 10 Hz
    start = int(np.argmax(np.abs(np.diff(ep["state"][:, :4], axis=0)).max(1) > 0.01))
    for i in range(start, len(ep["state"])):
        at((i - start) / 10)
        for cam in ("top", "wrist"):
            rr.log(f"expert/{cam}", image(ep[cam][i]))
        for j, name in enumerate(JOINTS):
            rr.log(f"joints/{name}/expert", Scalar(float(ep["state"][i, j])))

    for k, t in enumerate(ro["t"]):
        at(float(t))
        for cam in ("top", "wrist"):
            rr.log(f"policy/{cam}", image(ro[cam][k]))
        for j, name in enumerate(JOINTS):
            rr.log(f"joints/{name}/policy_actual", Scalar(float(ro["state"][k, j])))
            rr.log(f"joints/{name}/policy_command", Scalar(float(ro["action"][k, j])))
    print("sent to Rerun" + (f" -> {args.save}" if args.save else ""))


if __name__ == "__main__":
    main()

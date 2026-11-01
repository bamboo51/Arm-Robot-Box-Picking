"""Run the policy on every test scene in Gazebo and check whether the box ends on the car roof.

Start learning/policy_server.py first, then: python3 scripts/eval_gazebo.py [--pause]
"""
import json
import os
import subprocess
import sys
import time

import numpy as np
from collect_dataset import box_on_roof
from infer_node import ARM, HAND
from sim_utils import DATASET_DIR, load_scene, place_scene


def move_to(names, positions, topic, sec=2):
    """Send the joints straight to positions (no planning; fine for the start pose)."""
    pts = ", ".join(f"{p:.4f}" for p in positions)
    subprocess.run(["ros2", "topic", "pub", "--once", topic, "trajectory_msgs/msg/JointTrajectory",
                    f"{{joint_names: {names}, points: [{{positions: [{pts}], time_from_start: {{sec: {sec}}}}}]}}"],
                   check=True, capture_output=True)


def main():
    cfg = load_scene()
    results = {}
    split = os.environ.get("SPLIT", "test")  # SPLIT=val to choose settings without touching the test scenes
    for ep_dir in sorted(p.parent for p in (DATASET_DIR / split).glob("*/episode.npz")):
        state = np.load(ep_dir / "episode.npz")["state"]
        # start where the expert's arm first moves (upright, gripper reset to 0): before that the expert only waits
        # and resets the gripper, with no visible cue for when it starts, so the policy would wait forever
        # 0.01 rad/frame: the expert's first command nudges the already-upright arm by ~0.01 rad in total; skip that
        start = int(np.argmax(np.abs(np.diff(state[:, :4], axis=0)).max(1) > 0.01))
        move_to(ARM, state[start, :4], "/crane_plus_arm_controller/joint_trajectory")
        move_to(HAND, state[start, 4:], "/crane_plus_gripper_controller/joint_trajectory")
        time.sleep(3.0)
        place_scene("default", json.loads((ep_dir / "initial_pose.json").read_text())["scene"], cfg)
        time.sleep(1.0)

        print(f"== {ep_dir.name}", flush=True)
        rollout = DATASET_DIR.parent / "rollouts" / f"{ep_dir.name}.npz"  # for learning/view_rollout.py
        rollout.parent.mkdir(exist_ok=True)
        node = subprocess.Popen([sys.executable, "scripts/infer_node.py"], env={**os.environ, "ROLLOUT": str(rollout)})
        time.sleep((len(state) - start) / 10 + 10)  # the expert's remaining time, plus slack
        node.terminate()
        node.wait(timeout=30)  # saving the rollout's images takes a few seconds

        results[ep_dir.name] = box_on_roof(ep_dir, cfg)
        print(f"   success {results[ep_dir.name]['success']}  xy_err {results[ep_dir.name]['xy_err']:.3f}")
        if "--pause" in sys.argv:
            input("   Enter for the next episode ")

    n = sum(r["success"] for r in results.values())
    print(f"success {n}/{len(results)}")
    with open("eval_gazebo.json", "w") as f:
        json.dump(results, f, indent=1)


if __name__ == "__main__":
    main()

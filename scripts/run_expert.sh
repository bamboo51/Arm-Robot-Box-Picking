#!/usr/bin/env bash
#  Build and run the expert once (Gazebo must already be running: scripts/run_simulation.sh).
#  Usage: scripts/run_expert.sh             # default box/car position from config/scene.yaml
#         scripts/run_expert.sh <episode>   # position from datasets/<episode>/initial_pose.json
set -eo pipefail

cd "${ROS_WORKSPACE: -$HOME/airobot_ws}"
colcon build --symlink-install --packages-select crane_dataset_expert
source install/setup.bash

if [[ -n "$1" ]]; then
    export EPISODE="$1"
fi
ros2 launch crane_dataset_expert dataset_expert.launch.py

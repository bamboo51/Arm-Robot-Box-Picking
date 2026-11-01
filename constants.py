"""
Constants file for system wide use
"""

# Joints, in state/action order
ARM = ["crane_plus_joint1", "crane_plus_joint2", "crane_plus_joint3", "crane_plus_joint4"]
HAND = ["crane_plus_joint_hand"]
JOINTS = ARM + HAND

# ROS image topic
CAM_TOPICS = {
    "/camera_top/image_raw": "top",
    "/camera_wrist/image_raw": "wrist",
#    "/camera_left/image_raw": "left",
#    "/camera_right/image_raw": "right",
}
CAMS = list(CAM_TOPICS.values())
IMAGE_SHAPE = (240, 320, 3) # height, width, channels
FPS = 10
STEP = 1.0 / FPS
K = 5 # action = joint target K frames ahead

# Sentence for SmolVLA; for training ACT, this is not necessary
TASK = "put the box on the car"

# Dataset camera names (for SmolVLA)
SMOLVLA_RENAME = {
  "observation.images.top": "observation.images.camera1",
  "observation.images.wrist": "observation.images.camera2",
  # "observation.images.left": "observation.images.camera3",
  # "observation.images.right": "observation.images.camera4",
}

POLICY_SERVER = "tcp://127.0.0.1:5555" # policy server for lerobot, policy_server.py binds, infer_node.py connects

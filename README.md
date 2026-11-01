# Arm-Robot-Box-Picking
<!-- Classical Robotics & Simulation -->
![ROS 2](https://shields.io)
![MoveIt 2](https://shields.io)
![Gazebo](https://shields.io)

<!-- AI, Learning, & Control Frameworks -->
![LeRobot](https://shields.io)
![PyTorch](https://shields.io)
![Python](https://shields.io)

This project is the source code developed as part of final assignment in UTokyo MatsuoLab's Physical AI course. 
This simulation runs on Gazebo and ROS2 Humble for CRANE+ to grab the box and place it to the car position. This repo also trained the ACT [1] model that uses the images from top view and gripper, and joints state for imitation learning. The original world is referenced from the reference [2,3].

日本語バージョンは[docs/README_ja.md](docs/README_ja.md)

![example](docs/images/example.png)

## Long-Term Plan
- [x] Improve the precision on grabbing the box to lift higher than the height of the car.
- [x] Resample the box position and car position for better generalizability.
- [x] Train SmolVLA for commanding the arm using sentence.
- [x] Add other stuff, like apple or banana in the world.
  - [x] Maybe have to use YOLO and other models to generate the teacher dataset for general object detection.
- [x] To be continue...

## Getting Started

### Dataset
The dataset used for training the ACT model is on [Train set](https://huggingface.co/datasets/Phongwit/crane_pick_place_topwrist). This include the images from top view, images from wrist view, and the joints state around 70 episodes. 
For validation set and test set, is separated from the training set. They are formatted using the initial position of the box and the car, along with the trajectory .npz file. These files can be found at this dataset. [NPZ dataset](https://huggingface.co/datasets/Phongwit/crane_pick_place_episodes/tree/main)

## Useful Commands
All useful commands are included in the [docs/commands.md](docs/commands.md).

## References
1. Zhao et al., "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware" (ACT), RSS 2023.
2. [Physical AI Course Classwork](https://skinny-chord-c58.notion.site/5-ROS-2-2-2-2049a7a1061380fc8928e500eafc57d0)
3. [matsuolab/pai_training](https://github.com/matsuolab/pai_training)

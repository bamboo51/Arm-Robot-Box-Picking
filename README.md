# Arm-Robot-Box-Picking

![ROS 2 Humble](https://img.shields.io/badge/ROS_2-22314E?style=flat&logo=ros&logoColor=white)
![MoveIt 2](https://img.shields.io/badge/MoveIt_2-01A183?style=flat)
![Gazebo](https://img.shields.io/badge/Gazebo-FFB800?style=flat)
![LeRobot](https://img.shields.io/badge/LeRobot-FFD21E?style=flat&logo=huggingface&logoColor=black)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

This project is the source code developed as part of final assignment in UTokyo MatsuoLab's Physical AI course. 
This simulation runs on Gazebo and ROS2 Humble for CRANE+ to grab the box and place it to the car position. This repo also trained the ACT [1] model that uses the images from top view and gripper, and joints state for imitation learning. The original world is referenced from the reference [2,3].

<img width="1406" height="845" alt="image" src="https://github.com/user-attachments/assets/024d5a26-6d09-47d5-895c-135001f12ab4" />

YouTube video: https://youtu.be/QIHJ2aa_FPA?si=tyzqP1tWc467VJy8

## Long-Term Plan
- [ ] Improve the precision on grabbing the box to lift higher than the height of the car.
- [ ] Resample the box position and car position for better generalizability.
- [ ] Train SmolVLA for commanding the arm using sentence.
- [ ] Add other stuff, like apple or banana in the world.
  - [ ] Maybe have to use YOLO and other models to generate the teacher dataset for general object detection.
- [ ] To be continue...

## Getting Started

### Dataset
The dataset used for training the ACT model is on [Train set](https://huggingface.co/datasets/bamboo51/crane_pick_place_topwrist). This include the images from top view, images from wrist view, and the joints state around 70 episodes. 
For validation set and test set, is separated from the training set. They are formatted using the initial position of the box and the car, along with the trajectory .npz file. These files can be found at this dataset. [NPZ dataset](https://huggingface.co/datasets/bamboo51/crane_pick_place_episodes/tree/main)

### Trained Model
You can download the trained ACT model at: [Bamboo51's Huggingface Model](https://huggingface.co/bamboo51/act_crane_topwrist/)

## Useful Commands
All useful commands are included in the [docs/commands.md](docs/commands.md).


## References
1. Zhao et al., "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware" (ACT), RSS 2023.
2. [Physical AI Course Classwork](https://skinny-chord-c58.notion.site/5-ROS-2-2-2-2049a7a1061380fc8928e500eafc57d0)
3. [matsuolab/pai_training](https://github.com/matsuolab/pai_training)

# Useful Commands List

## Docker Image & Container
Please set `.env` file based on `.env.example`.
This proxy is set because my school has proxy server to be set. If your environment does not require proxy, you can keep it nothing.

```bash
cp .env.example .env
docker compose up -d
docker compose down
```

This image is included the some library compared to the reference [2] on the root [README](../README.md#References) as list below:
- `ros-humble-rosbag2-storage-mcap` (for recording episodes)
- `/opt/lerobot-venv`: `learning/uv.lock` (for LeRobot which requires Python >= 3.13)
- `pyzmq` (for integrating with ROS2 Humble)

## Simulation
Gazebo environment
```bash
# for the simulation 
./scripts/run_simulation.sh
ros2 topic hz /camera_top/image_raw
```

## Running Dataset Expert and Build
This is the dataset expert running for making the dataset.
```bash
bash ./scripts/run_expert.sh
```

## Gathering Dataset

### Randomize the position of the box and the car
First create the scene. (aka. the position of the box and the car). The range of the box and the car that can be generated is defined in [`config/scene.yaml`](../config/scene.yaml)
```bash
python3 scripts/randomize_box.py --seed <n> --episode <name>
```

For making the whole dataset. I recommend you to run
```bash
bash ./scripts/randomize_box.sh [--count N] [--interval SECONDS]
```

### Record the simulation
```bash
python3 scripts/collect_dataset.py
```
This will record the generated simulations that has no `result.json` in the folder.

> [!WARNING]
> One episode's bag would utilize the disk around 300 MB + npz round 95 MB. Please make sure you have enough disk space.

## Training

### Building train dataset
Build the training dataset to be used for ACT model.
```bash
cd learning && uv sync
rm -rf ../lerobot_data && uv run build_dataset.py
```

### Train the model
Train the model. The main one is ACT.
```bash
bash train_act.sh # ACT model
bash train_smolvla.sh # SmolVLA model
```

### Evaluation
Evaluate the model.
```bash
uv run eval_offline.py <MODEL_PATH> <EPISODE_PATH>
```

## Inference
Between the ROS Node and the Policy Server, there is the communication using ZMQ via address `tcp://127.0.0.1:5555`.
```bash
# Terminal 1
bash ./scripts/run_simulation.sh

# Terminal 2 (Policy Server, Python 3.13, GPU)
/opt/lerobot-venv/bin/python learning/policy_server.py <MODEL_PATH>

# Terminal 3 (ROS Node, Python 3.10)
python3 scripts/infer_node.py
```

## Other Useful Commands
```bash
# check camera
export DISPLAY=:0
ros2 run rqt_image_view rqt_image_view

# model position
ign model -m placement_car -p
ign model -m pick_box -p
for m in $(ign model --list | grep -- '- ' | sed 's/.*- //'); do
    echo "== $m"; ign model -m "$m" -p | sed -n '/Pose/,+2p'
done
```

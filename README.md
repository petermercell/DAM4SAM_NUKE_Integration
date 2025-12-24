# DAM4SAM Nuke Integration

A Foundry Nuke integration for [DAM4SAM](https://github.com/jovanavidenovic/DAM4SAM) (Distractor-Aware Memory for SAM2), enabling AI-powered visual object tracking and segmentation directly within your compositing workflow.

## Overview

DAM4SAM is a state-of-the-art visual object tracking system built on Meta's Segment Anything Model 2 (SAM2). It introduces a distractor-aware memory module that significantly improves tracking robustness when dealing with visually similar objects (distractors) in the scene.

This integration allows Nuke artists to leverage DAM4SAM's capabilities for:

- **Rotoscoping assistance** — Generate accurate segmentation masks from a single click or bounding box
- **Object tracking** — Track objects across frames with improved handling of occlusions and distractors
- **Matte extraction** — Create clean mattes for complex subjects like hair, fur, or transparent objects

## Features

- Seamless integration with Nuke's node-based workflow
- Bounding box-based object selection
- Automatic mask generation and tracking
- GPU-accelerated inference via CUDA

## Requirements

- **Foundry Nuke** (tested on Nuke 13+)
- **Windows** operating system
- **Miniconda/Anaconda** with Python 3.10+
- **CUDA-capable GPU** with sufficient VRAM (8GB+ recommended)
- **DAM4SAM** repository and model checkpoints

## Installation

### 1. Install DAM4SAM

First, set up the DAM4SAM environment following the [official instructions](https://github.com/jovanavidenovic/DAM4SAM):

```bash
# Clone DAM4SAM repository
git clone https://github.com/jovanavidenovic/DAM4SAM.git
cd DAM4SAM

# Create conda environment
conda create -n DAM4SAM python=3.10.15
conda activate DAM4SAM

# Install PyTorch with CUDA support
pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu121

# Install requirements
pip install -r requirements.txt

# Download model checkpoints
cd checkpoints && ./download_ckpts.sh && cd ..
```

### 2. Install Nuke Integration

1. Download `DAM4SAM_WIN.py` and `DAM4SAM_WIN.nk` from this repository
2. Place both files in your `.nuke` directory (typically `C:/Users/<USERNAME>/.nuke/`)
3. Copy the DAM4SAM repository to your `.nuke` directory or note its location

### 3. Configure Paths

Open `DAM4SAM_WIN.py` and update **lines 79–81** with your specific paths:

```python
conda_activate = r'C:/Users/%USERNAME%/miniconda3/Scripts/activate.bat'  # Path to your Conda activate script
conda_env = "DAM4SAM"                                                     # Your Conda environment name
script_dir = r'C:/Users/<USERNAME>/.nuke/DAM4SAM'                        # Directory containing DAM4SAM
```

## Usage

1. Open the `DAM4SAM_WIN.nk` Nuke script or import it into your project
2. Connect your footage to the input
3. Draw a bounding box around the object you want to track on the first frame
4. Execute the DAM4SAM node to generate segmentation masks
5. The output mask can be used for compositing, keying, or further refinement

## Video Tutorial

For a complete walkthrough, watch the video tutorial:

[![DAM4SAM Nuke Integration Tutorial](https://img.youtube.com/vi/_9cLWZtqm7k/0.jpg)](https://www.youtube.com/watch?v=_9cLWZtqm7k)

> Right-click the thumbnail and select "Open link in new tab" to watch.

## How It Works

The integration uses Nuke's Python API to:

1. Export the current frame and bounding box coordinates
2. Launch DAM4SAM inference through the configured Conda environment
3. Process the footage using SAM2 with distractor-aware memory
4. Import the generated masks back into Nuke as image sequences

DAM4SAM's key innovation is its dual-memory architecture:

- **Recent Appearance Memory (RAM)** — Stores recent target appearances for accurate frame-to-frame segmentation
- **Distractor-Resolving Memory (DRM)** — Maintains anchor frames to differentiate the target from similar-looking objects

## Troubleshooting

**"Conda not found" error**  
Ensure the `conda_activate` path points to your actual Conda installation's `activate.bat` file.

**CUDA out of memory**  
Try reducing the input resolution or using a smaller SAM2 model variant.

**Masks not generating**  
Verify that the DAM4SAM checkpoints are downloaded and the `script_dir` path is correct.

## Credits

- **DAM4SAM** — [Jovana Videnovic, Alan Lukezic, Matej Kristan](https://github.com/jovanavidenovic/DAM4SAM) (CVPR 2025)
- **Segment Anything Model 2** — [Meta AI Research](https://github.com/facebookresearch/sam2)

## Citation

If you use this integration in your work, please cite the original DAM4SAM paper:

```bibtex
@InProceedings{dam4sam,
    author    = {Videnovic, Jovana and Lukezic, Alan and Kristan, Matej},
    title     = {A Distractor-Aware Memory for Visual Object Tracking with SAM2},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
    year      = {2025}
}
```

## License

This integration is provided as-is for use with Foundry Nuke. DAM4SAM and SAM2 are subject to their respective licenses.

## Author

**Peter Mercell**  
[www.petermercell.com](https://www.petermercell.com)

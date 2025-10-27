# LongCat-Video Installation Guide

**Optimized for Windows + RTX 5090 + Latest NVIDIA Drivers**

This guide provides step-by-step installation instructions for LongCat-Video on Windows systems with high-end NVIDIA GPUs (RTX 5090, RTX 4090, etc.).

---

## System Requirements

### Hardware
- **GPU**: NVIDIA RTX 5090 (32GB VRAM) or similar (RTX 4090, A6000, etc.)
- **RAM**: 32GB minimum, 64GB recommended
- **Storage**: 100GB+ free space (50GB for model weights, 50GB for outputs)
- **CPU**: Modern multi-core processor (Intel i7/i9 or AMD Ryzen 7/9)

### Software
- **OS**: Windows 10/11 (64-bit)
- **NVIDIA Driver**: Latest Game Ready or Studio Driver (version 560.xx+)
- **CUDA Toolkit**: 12.4 or later (bundled with PyTorch installation)
- **Python**: 3.10.x (do not use 3.11+ or 3.9-)

---

## Pre-Installation Checklist

### 1. Verify GPU and Driver

```powershell
# Open PowerShell or Command Prompt
nvidia-smi
```

**Expected Output:**
- Driver Version: 560.xx or higher
- CUDA Version: 12.4 or higher
- GPU: RTX 5090 with ~32GB memory

**If nvidia-smi doesn't work:**
1. Download latest driver from [nvidia.com/drivers](https://www.nvidia.com/Download/index.aspx)
2. Install and restart your computer
3. Run `nvidia-smi` again to verify

### 2. Install Python 3.10

**Option A: Official Python Installer**
1. Download Python 3.10.x from [python.org](https://www.python.org/downloads/)
2. Run installer, check "Add Python to PATH"
3. Verify: `python --version` (should show 3.10.x)

**Option B: Anaconda/Miniconda (Recommended)**
1. Download Miniconda from [docs.conda.io](https://docs.conda.io/en/latest/miniconda.html)
2. Install Miniconda
3. Continue to Step 3 below

### 3. Install Git (if not already installed)

Download Git for Windows from [git-scm.com](https://git-scm.com/download/win)

Verify: `git --version`

---

## Installation Steps

### Step 1: Create Conda Environment

Open **Anaconda Prompt** or **PowerShell** (as Administrator):

```powershell
# Create environment with Python 3.10
conda create -n longcat-video python=3.10 -y

# Activate environment
conda activate longcat-video

# Verify Python version
python --version
# Should output: Python 3.10.x
```

### Step 2: Clone LongCat-Video Repository

```powershell
# Navigate to your projects directory
cd C:\Users\YourUsername\Documents
# Or wherever you want to store the project

# Clone repository
git clone --single-branch --branch main https://github.com/meituan-longcat/LongCat-Video
cd LongCat-Video
```

### Step 3: Install PyTorch with CUDA Support

**For RTX 5090 with CUDA 12.4:**

```powershell
# Install PyTorch 2.6.0 with CUDA 12.4 support
pip install torch==2.6.0+cu124 torchvision==0.21.0+cu124 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
```

**Verify PyTorch installation:**

```python
python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'GPU: {torch.cuda.get_device_name(0)}')"
```

**Expected output:**
```
PyTorch version: 2.6.0+cu124
CUDA available: True
CUDA version: 12.4
GPU: NVIDIA GeForce RTX 5090
```

### Step 4: Install FlashAttention-2

**Important**: FlashAttention-2 requires Visual Studio Build Tools on Windows.

**4a. Install Visual Studio Build Tools (if not already installed):**

1. Download from [visualstudio.microsoft.com](https://visualstudio.microsoft.com/downloads/)
2. Select "Build Tools for Visual Studio 2022"
3. Install with "Desktop development with C++"
4. Restart your computer

**4b. Install FlashAttention-2:**

```powershell
# Install build dependencies
pip install ninja psutil packaging wheel

# Install FlashAttention-2
pip install flash-attn==2.7.4.post1 --no-build-isolation
```

**Note**: This may take 10-20 minutes to compile. Be patient.

**If installation fails:**
- Ensure Visual Studio Build Tools are installed
- Try: `pip install flash-attn --no-build-isolation` (without version pin)
- Alternative: Use xformers instead (see troubleshooting section)

### Step 5: Install Other Dependencies

```powershell
# Install remaining requirements
pip install -r requirements.txt
```

### Step 6: Download Model Weights

**6a. Install HuggingFace CLI:**

```powershell
pip install "huggingface_hub[cli]"
```

**6b. Download model weights:**

```powershell
# Create weights directory
mkdir weights

# Download LongCat-Video model (~13.6B parameters, ~30-50GB)
huggingface-cli download meituan-longcat/LongCat-Video --local-dir ./weights/LongCat-Video
```

**Note**: This download may take 30-60 minutes depending on your internet speed.

**Optional: Login to HuggingFace (for gated models):**

```powershell
huggingface-cli login
# Enter your HuggingFace token when prompted
```

### Step 7: Verify Installation

```powershell
# Test CUDA and GPU
python -c "import torch; print(f'GPU Count: {torch.cuda.device_count()}'); print(f'Current GPU: {torch.cuda.current_device()}'); print(f'GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB')"
```

**Expected output for RTX 5090:**
```
GPU Count: 1
Current GPU: 0
GPU Memory: 32.00 GB
```

---

## Running Your First Generation

### Text-to-Video Demo

```powershell
# Ensure environment is activated
conda activate longcat-video

# Navigate to LongCat-Video directory
cd C:\Users\YourUsername\Documents\LongCat-Video

# Run text-to-video demo with compile optimization
python run_demo_text_to_video.py --checkpoint_dir=./weights/LongCat-Video --enable_compile
```

**Alternative using torchrun (for multi-GPU or optimized single-GPU):**

```powershell
torchrun --nproc_per_node=1 run_demo_text_to_video.py --checkpoint_dir=./weights/LongCat-Video --enable_compile
```

### Image-to-Video Demo

```powershell
python run_demo_image_to_video.py --checkpoint_dir=./weights/LongCat-Video --enable_compile
```

### Long Video Generation Demo

```powershell
python run_demo_long_video.py --checkpoint_dir=./weights/LongCat-Video --enable_compile
```

### Video Continuation Demo

```powershell
python run_demo_video_continuation.py --checkpoint_dir=./weights/LongCat-Video --enable_compile
```

---

## Optimization for RTX 5090

### Memory Optimization

**Enable Mixed Precision (FP16):**

Edit demo scripts or add flags (if supported):
```python
# In your generation script
torch.set_float32_matmul_precision('high')
```

**Monitor GPU Usage:**

```powershell
# In a separate terminal, watch GPU usage
nvidia-smi -l 1
```

### Performance Tips

1. **Use `--enable_compile` flag**: Enables PyTorch compilation for faster inference
2. **Batch Size**: Start with 1, increase if VRAM allows
3. **Resolution**: Start with 720p, scale to 1080p if VRAM permits
4. **Frame Count**: 
   - 128 frames: ~12-16GB VRAM
   - 256 frames: ~20-24GB VRAM
   - 512 frames: May require gradient checkpointing

### VRAM Management

**If you encounter Out-of-Memory (OOM) errors:**

```python
# Clear CUDA cache between generations
import torch
torch.cuda.empty_cache()
```

**Or reduce parameters:**
- Decrease frame count
- Lower resolution (512×512 or 640×360)
- Use gradient checkpointing (if available in config)

---

## Configuration File Setup

### Create Custom Config (config.yaml)

```yaml
# config/longcat_config.yaml
model:
  checkpoint_dir: "./weights/LongCat-Video"
  enable_compile: true
  dtype: "fp16"  # Use FP16 for faster inference

generation:
  resolution:
    width: 720
    height: 1280  # 9:16 vertical for social media
  fps: 30
  num_frames: 128  # ~4.3 seconds at 30fps
  
optimization:
  batch_size: 1
  use_flash_attention: true
  gradient_checkpointing: false  # Enable if OOM

output:
  save_dir: "./outputs"
  format: "mp4"
  codec: "h264"
  quality: "high"
```

### Use Custom Config

```python
# In your Python script
import yaml

with open('config/longcat_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Use config in your generation pipeline
```

---

## Troubleshooting

### Issue 1: FlashAttention-2 Won't Compile

**Solution 1**: Use xformers as alternative:
```powershell
pip install xformers
# Modify model config to use xformers instead of flash_attn
```

**Solution 2**: Skip FlashAttention and use standard attention:
- Comment out FlashAttention imports in model files
- Performance will be slower but should work

### Issue 2: CUDA Out of Memory

**Solutions:**
1. Reduce frame count: 128 → 64 frames
2. Lower resolution: 720p → 512p
3. Enable gradient checkpointing (in config)
4. Close other GPU-using applications
5. Restart Python kernel to clear CUDA cache

### Issue 3: Slow Generation Times

**Solutions:**
1. Ensure `--enable_compile` flag is used
2. Verify FlashAttention-2 is properly installed
3. Use FP16 precision
4. Check GPU is being utilized: `nvidia-smi`
5. Update NVIDIA drivers to latest version

### Issue 4: Import Errors

**Solution:**
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall --no-cache-dir
```

### Issue 5: Model Weights Not Loading

**Check:**
1. Weights directory exists: `./weights/LongCat-Video`
2. Weights fully downloaded (should be 30-50GB)
3. Correct path in `--checkpoint_dir` argument
4. Re-download if corrupted:
   ```powershell
   rm -r weights/LongCat-Video
   huggingface-cli download meituan-longcat/LongCat-Video --local-dir ./weights/LongCat-Video
   ```

---

## Environment Management

### Deactivate Environment

```powershell
conda deactivate
```

### Reactivate Environment (for future sessions)

```powershell
conda activate longcat-video
cd C:\Users\YourUsername\Documents\LongCat-Video
```

### Update Environment

```powershell
conda activate longcat-video
pip install --upgrade torch torchvision torchaudio flash-attn
```

### Delete Environment (if needed)

```powershell
conda deactivate
conda env remove -n longcat-video
```

---

## Next Steps

1. **Experiment with Prompts**: See [LONGCAT_VIDEO_PROMPT_TEMPLATES.md](LONGCAT_VIDEO_PROMPT_TEMPLATES.md)
2. **Integrate with PrismQ**: See main [LONGCAT_VIDEO_RESEARCH.md](LONGCAT_VIDEO_RESEARCH.md) for integration workflows
3. **Create Horror Content**: See prompt templates for horror/true-crime specific examples
4. **Optimize Workflow**: Develop custom scripts for batch processing

---

## Additional Resources

- **Official Repository**: [github.com/meituan-longcat/LongCat-Video](https://github.com/meituan-longcat/LongCat-Video)
- **HuggingFace Model**: [huggingface.co/meituan-longcat/LongCat-Video](https://huggingface.co/meituan-longcat/LongCat-Video)
- **PyTorch Documentation**: [pytorch.org/docs](https://pytorch.org/docs/stable/index.html)
- **CUDA Toolkit**: [developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)

---

*Installation guide prepared for Windows + RTX 5090 systems*  
*Last updated: October 27, 2025*  
*Part of PrismQ.Research.Generator.Video documentation*

# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/PrismQDev/PrismQ.Research.Generator.Video.git
cd PrismQ.Research.Generator.Video

# Install dependencies
pip install -r requirements.txt
```

## Generate Your First Video

### 1. Run the Example Script

The easiest way to get started:

```bash
python example.py
```

This generates a 27-second video with all engagement optimizations at `output/engagement_video.mp4`.

### 2. Custom Configuration

Create your own script:

```python
from src.config import GenerationConfig
from src.pipeline import VideoPipeline

# Configure your video
config = GenerationConfig(
    output_resolution=(1080, 1920),  # Vertical format
    fps=30,
    target_duration=30,  # seconds
    seed=42,  # For reproducibility
)

# Create pipeline
pipeline = VideoPipeline(config)

# Add your captions
captions = [
    ("Welcome!", 0),
    ("Constant Motion", 90),
    ("High Contrast", 180),
    ("Pattern Breaks", 270),
    ("Subscribe!", 540),
]

# Generate!
pipeline.run_full_pipeline("my_video.mp4", captions)
```

### 3. Test Installation

Run the test suite to verify everything works:

```bash
python tests/test_pipeline.py
```

You should see: `Ran 21 tests ... OK`

## Key Parameters

### Video Settings

```python
config = GenerationConfig(
    # Output format
    output_resolution=(1080, 1920),  # 9:16 vertical
    fps=30,                          # Frame rate
    target_duration=27,              # Length in seconds
    
    # Generation
    seed=42,                         # Lock randomness
    cfg_scale=7.0,                   # Creativity (lower = more creative)
)
```

### Motion Settings

```python
config = GenerationConfig(
    # Micro-movements
    micro_movement_amplitude=2.0,    # pixels (1-3 recommended)
    micro_movement_frequency=1.0,    # Hz (0.5-2 recommended)
    
    # Zoom
    micro_zoom_range=(1.0, 1.05),   # Start to end scale (0-5% zoom)
    
    # Pattern breaks
    minor_break_interval=40,         # frames (~1.3s at 30fps)
    major_break_interval=80,         # frames (~2.7s at 30fps)
)
```

### Visual Style

```python
config = GenerationConfig(
    # Contrast and saturation
    contrast_boost=1.5,              # 1.0-2.0 range
    saturation_boost=1.4,            # 1.0-2.0 range
    
    # Neon colors (RGB tuples)
    neon_colors=[
        (0, 255, 255),               # Cyan
        (255, 0, 255),               # Magenta
        (0, 128, 255),               # Electric blue
    ],
)
```

## Advanced Usage

### Step-by-Step Pipeline

For more control, run each step individually:

```python
from src.pipeline import VideoPipeline

pipeline = VideoPipeline()

# Step 1: Generate base video
pipeline.generate_base_video()

# Step 2: Apply visual style
pipeline.apply_visual_style()

# Step 3: Add motion effects
pipeline.apply_motion_effects()

# Step 4: Add captions
captions = [("Text", 0)]
pipeline.add_captions(captions)

# Step 5: Apply overlays
pipeline.apply_overlays()

# Step 6: Export
pipeline.export_video("output.mp4")
```

### Using Individual Components

```python
from src.generator import VideoGenerator
from src.visual_style import VisualStyle
from src.motion import MotionEffects
from src.overlay import Overlay
from src.config import GenerationConfig

config = GenerationConfig()

# Generate frames
generator = VideoGenerator(config)
frames = generator.generate_base_clip()

# Apply style
style = VisualStyle(config)
styled_frames = [style.apply_full_style(f) for f in frames]

# Add motion
motion = MotionEffects(config)
for i, frame in enumerate(styled_frames):
    styled_frames[i] = motion.apply_micro_movement(frame, i)
    styled_frames[i] = motion.apply_micro_zoom(styled_frames[i], i, len(frames))

# Add overlays
overlay = Overlay(config)
overlay.add_caption("Hello!", 0)
final_frames = [overlay.apply_overlays(f, i, len(frames)) 
                for i, f in enumerate(styled_frames)]
```

## Caption Timing Tips

### Sync with Pattern Breaks

Pattern breaks occur at predictable intervals. Align captions for maximum impact:

```python
# At 30 fps with default settings:
# Minor breaks: frames 40, 80, 120, 160, 200...
# Major breaks: frames 80, 160, 240, 320...

captions = [
    ("Intro", 0),
    ("Point 1", 80),    # Major break
    ("Point 2", 160),   # Major break
    ("Point 3", 240),   # Major break
    ("Outro", 400),
]
```

### Caption Duration

Default caption duration is 2.5 seconds. Plan spacing accordingly:

```python
fps = 30
caption_duration = 2.5  # seconds
caption_frames = int(caption_duration * fps)  # 75 frames

# Space captions at least 75 frames apart
captions = [
    ("First", 0),
    ("Second", 90),   # 3 seconds later
    ("Third", 180),   # 3 seconds later
]
```

## Performance Tips

### Faster Generation (Lower Quality)

For quick previews:

```python
config = GenerationConfig(
    output_resolution=(540, 960),   # Half resolution
    fps=15,                          # Half frame rate
    target_duration=6,               # Shorter duration
)
```

### Production Quality (Slower)

For final output:

```python
config = GenerationConfig(
    output_resolution=(1080, 1920),  # Full HD
    fps=30,                          # Smooth motion
    target_duration=30,              # Full length
)
```

### GPU Acceleration (Future)

When SDXL/AnimateDiff is integrated, use GPU:

```python
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
```

## Troubleshooting

### ImportError with relative imports

If you get import errors, make sure to run from the project root:

```bash
cd PrismQ.Research.Generator.Video
python example.py  # ✓ Correct
```

Not:

```bash
cd PrismQ.Research.Generator.Video/src
python ../example.py  # ✗ Wrong
```

### Video doesn't play

Make sure you have a video player that supports MP4/H.264:
- VLC Media Player (recommended)
- QuickTime (macOS)
- Windows Media Player (Windows 10+)

### Low performance

Processing is CPU-intensive. Expected times:
- 6s video @ 540×960: ~30-60 seconds
- 27s video @ 1080×1920: ~70-130 seconds

For faster processing:
1. Use lower resolution for previews
2. Reduce fps (15 instead of 30)
3. Shorter duration
4. Future: GPU acceleration

### Tests fail

Ensure you have all dependencies:

```bash
pip install numpy opencv-python
python tests/test_pipeline.py
```

## Examples Gallery

### Example 1: Minimal Config

```python
from src.pipeline import VideoPipeline

pipeline = VideoPipeline()  # Use all defaults
pipeline.run_full_pipeline("minimal.mp4")
```

### Example 2: Custom Colors

```python
from src.config import GenerationConfig
from src.pipeline import VideoPipeline

config = GenerationConfig(
    neon_colors=[
        (255, 0, 0),     # Red
        (0, 255, 0),     # Green
        (0, 0, 255),     # Blue
    ]
)

pipeline = VideoPipeline(config)
pipeline.run_full_pipeline("custom_colors.mp4")
```

### Example 3: More Frequent Pattern Breaks

```python
config = GenerationConfig(
    minor_break_interval=20,  # More frequent (every ~0.7s)
    major_break_interval=40,  # More frequent (every ~1.3s)
)

pipeline = VideoPipeline(config)
pipeline.run_full_pipeline("intense.mp4")
```

### Example 4: Subtle Motion

```python
config = GenerationConfig(
    micro_movement_amplitude=1.0,     # Less movement
    micro_zoom_range=(1.0, 1.02),    # Less zoom
    contrast_boost=1.2,               # Less contrast
)

pipeline = VideoPipeline(config)
pipeline.run_full_pipeline("subtle.mp4")
```

## Next Steps

1. **Read the research**: See `RESEARCH.md` for the science behind the parameters
2. **Experiment**: Try different configurations and see what works best
3. **Integrate SDXL**: Follow instructions in `README.md` for AI-generated content
4. **Share results**: Test engagement metrics and iterate

## Support

- **Documentation**: See `README.md` and `RESEARCH.md`
- **Issues**: Open an issue on GitHub
- **Tests**: Run `python tests/test_pipeline.py`
- **Examples**: Check `example.py`

## Quick Reference

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `fps` | 30 | 15-60 | Frame rate (smoothness) |
| `target_duration` | 27s | 6-60s | Video length |
| `micro_movement_amplitude` | 2.0px | 1-3px | Motion intensity |
| `micro_zoom_range` | (1.0, 1.05) | (1.0, 1.1) | Zoom amount |
| `minor_break_interval` | 40 | 20-60 | Pattern break frequency |
| `contrast_boost` | 1.5 | 1.0-2.0 | Contrast intensity |
| `saturation_boost` | 1.4 | 1.0-2.0 | Color saturation |
| `caption_duration` | 2.5s | 1-5s | Caption display time |

---

**Ready to create engaging videos? Run `python example.py` to start!** 🎬

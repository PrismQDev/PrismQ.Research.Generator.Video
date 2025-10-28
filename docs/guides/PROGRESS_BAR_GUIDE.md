# Enhanced Progress Bar Documentation

## Overview

The enhanced progress bar implements research-backed design principles optimized for retention and engagement in short-form vertical videos (Reddit/AITA drama videos, TikTok, Reels, Shorts).

## Features

### 1. **Slim Bottom-Edge Design**
- 2-3 pixel height for non-intrusive visibility
- Full-width horizontal bar anchored at the very bottom edge
- Positioned to avoid overlap with captions, faces, or UI elements

### 2. **Visual Design**
- **Foreground Fill**: Bold, brand-aligned deep red/burgundy color for drama content
- **Background Track**: Subtle translucent gray line beneath the fill for contrast
- **Glowing End Marker**: Small dot that travels along the bar, signaling momentum (mimics YouTube's red dot)
- **Shadow Effect**: Subtle shadow for better contrast against bright/dark backgrounds

### 3. **Psychological Engagement**
- **Goal-Gradient Effect**: Slight visual acceleration at ~80% progress to create anticipation
- **Zeigarnik Effect**: Incomplete progress motivates viewers to finish
- **Time-Respect Cue**: Visually reassures viewers the video is short

### 4. **Smooth Animation**
- Continuous fill from 0% to 100% over entire video duration
- No stalling, jerky jumps, or early completion

## Configuration Options

All configuration options are available in `GenerationConfig` class in `src/config.py`:

### Basic Settings

```python
# Progress bar height (2-3px slim design)
progress_bar_height: int = 3

# Higher opacity for better visibility
progress_bar_opacity: float = 0.85

# Offset from bottom edge (0 = very bottom)
progress_bar_y_offset: int = 0

# Span full width of frame
progress_bar_full_width: bool = True
```

### Color Settings

```python
# Deep red/burgundy for drama/engagement (BGR format)
progress_bar_fg_color: Tuple[int, int, int] = (25, 25, 139)

# Translucent gray background track (BGR format)
progress_bar_bg_color: Tuple[int, int, int] = (60, 60, 60)

# Background track opacity
progress_bar_bg_opacity: float = 0.4
```

### End Marker (Glowing Dot)

```python
# Enable/disable glowing end marker
progress_bar_marker_enabled: bool = True

# Radius of glowing dot
progress_bar_marker_radius: int = 5

# Glow effect radius
progress_bar_marker_glow_radius: int = 10

# Brighter red for marker (BGR format)
progress_bar_marker_color: Tuple[int, int, int] = (50, 50, 200)
```

### Goal-Gradient Effect

```python
# Start acceleration at 80% progress
progress_bar_gradient_start: float = 0.80

# Slight acceleration multiplier
progress_bar_gradient_factor: float = 1.2
```

### Shadow/Contrast

```python
# Enable/disable shadow
progress_bar_shadow_enabled: bool = True

# Shadow offset in pixels
progress_bar_shadow_offset: int = 1

# Shadow opacity
progress_bar_shadow_opacity: float = 0.6
```

## Usage Example

### Basic Usage

```python
from src.config import GenerationConfig
from src.pipeline import VideoPipeline

# Use default enhanced progress bar settings
config = GenerationConfig()
pipeline = VideoPipeline(config)

# Add captions and generate video
captions = [
    ("Your Message Here", 0),
    ("Second Caption", 120),
]

pipeline.run_full_pipeline("output/video.mp4", captions)
```

### Custom Configuration

```python
from src.config import GenerationConfig
from src.pipeline import VideoPipeline

# Customize progress bar settings
config = GenerationConfig(
    # Use a different color scheme (e.g., electric blue)
    progress_bar_fg_color=(255, 128, 0),  # BGR: Electric Blue
    
    # Make it slightly taller
    progress_bar_height=4,
    
    # Disable the glowing marker
    progress_bar_marker_enabled=False,
    
    # Adjust goal-gradient effect
    progress_bar_gradient_start=0.75,  # Start at 75%
)

pipeline = VideoPipeline(config)
pipeline.run_full_pipeline("output/video.mp4")
```

### Testing Individual Frames

```python
from src.config import GenerationConfig
from src.overlay import Overlay
import numpy as np
import cv2

# Create configuration
config = GenerationConfig()
overlay = Overlay(config)

# Create test frame
frame = np.zeros((1920, 1080, 3), dtype=np.uint8)

# Draw progress bar at 50%
frame_with_bar = overlay.draw_progress_bar(frame, 0.5)

# Save or display
cv2.imwrite("test_progress.png", frame_with_bar)
```

## Color Customization for Different Content Types

### Drama/AITA (Default)
```python
progress_bar_fg_color=(25, 25, 139)  # Deep red/burgundy
```

### Mystery/Suspense
```python
progress_bar_fg_color=(139, 25, 139)  # Violet/Purple
```

### Modern/Tech
```python
progress_bar_fg_color=(255, 128, 0)  # Electric Blue/Cyan
```

### Educational
```python
progress_bar_fg_color=(0, 165, 255)  # Orange
```

### Feel-Good/Positive
```python
progress_bar_fg_color=(0, 255, 128)  # Neon Green
```

## Implementation Details

The enhanced progress bar is implemented in the `draw_progress_bar` method of the `Overlay` class (`src/overlay.py`). It:

1. Calculates position at the very bottom edge of the frame
2. Applies goal-gradient effect when progress >= 80%
3. Draws shadow layer (if enabled)
4. Draws translucent gray background track
5. Draws foreground progress fill
6. Draws glowing end marker dot (if enabled)
7. Applies proper alpha blending for all layers

## Research Basis

This implementation is based on:

- **Zeigarnik Effect**: People remember uncompleted tasks better than completed ones
- **Goal-Gradient Effect**: Motivation increases as people get closer to a goal
- **Visual Continuity**: Familiar UI patterns (YouTube-style) blend seamlessly
- **Time-Respect Cues**: Clear progress indication for short-form content

Optimized for:
- YouTube Shorts
- TikTok
- Instagram Reels
- Facebook Reels

Target audience: 15-25 year old viewers who expect pacing cues in short-form content.

## Performance

The enhanced progress bar adds minimal overhead:
- ~0.1-0.2ms per frame
- No significant impact on video generation time
- All rendering done with OpenCV for efficiency

## Testing

Run the progress bar tests with:

```bash
python -m unittest tests.test_pipeline.TestOverlay -v
```

Test coverage includes:
- Progress bar rendering at various stages (0%, 25%, 50%, 75%, 85%, 95%, 100%)
- Goal-gradient effect validation
- Marker enabled/disabled scenarios
- Shadow enabled/disabled scenarios
- Configuration validation

"""
Configuration for video generation parameters.
"""
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class GenerationConfig:
    """Configuration for video generation."""
    
    # Video output settings
    output_resolution: Tuple[int, int] = (1080, 1920)  # 9:16 vertical
    fps: int = 30
    target_duration: int = 27  # seconds (middle of 24-30s range)
    base_clip_duration: int = 3  # seconds for initial generation
    
    # SDXL/AnimateDiff settings
    model_name: str = "stabilityai/stable-diffusion-xl-base-1.0"
    seed: int = 42  # Locked seed for consistency
    cfg_scale: float = 7.0  # Low CFG for creative variation
    num_inference_steps: int = 30
    
    # Motion settings
    motion_threshold_ms: int = 300  # Nothing static for >300ms
    micro_movement_amplitude: float = 2.0  # pixels
    micro_movement_frequency: float = 1.0  # Hz
    parallax_speed: float = 0.3  # pixels per frame
    
    # Zoom settings
    micro_zoom_range: Tuple[float, float] = (1.0, 1.05)  # 0-5% zoom
    zoom_cycle_duration: int = 90  # frames
    
    # Pattern break settings
    minor_break_interval: int = 40  # frames (~1.3s)
    major_break_interval: int = 80  # frames (~2.7s)
    break_duration: int = 5  # frames
    
    # Visual style settings
    base_darkness: Tuple[int, int] = (20, 60)  # RGB range for dark base
    neon_colors: List[Tuple[int, int, int]] = None  # Set in __post_init__
    accent_coverage: float = 0.12  # 12% of frame
    contrast_boost: float = 1.5
    saturation_boost: float = 1.4
    
    # Overlay settings
    caption_font_size: int = 48
    caption_duration: float = 2.5  # seconds
    progress_bar_height: int = 4  # pixels
    progress_bar_opacity: float = 0.5
    
    def __post_init__(self):
        """Initialize default neon colors if not provided."""
        if self.neon_colors is None:
            self.neon_colors = [
                (0, 255, 255),    # Cyan
                (255, 0, 255),    # Magenta
                (0, 128, 255),    # Electric Blue
                (0, 255, 0),      # Neon Green
                (255, 20, 147),   # Hot Pink
            ]
    
    @property
    def total_frames(self) -> int:
        """Calculate total frames for target duration."""
        return self.target_duration * self.fps
    
    @property
    def base_frames(self) -> int:
        """Calculate frames for base clip."""
        return self.base_clip_duration * self.fps
    
    @property
    def tiles_needed(self) -> int:
        """Calculate number of tiles needed."""
        return (self.total_frames + self.base_frames - 1) // self.base_frames

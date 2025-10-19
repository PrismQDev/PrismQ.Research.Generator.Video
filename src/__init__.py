"""
PrismQ Video Generator Package
High-engagement abstract video generation with visual principles.
"""

__version__ = "1.0.0"

from .config import GenerationConfig
from .pipeline import VideoPipeline
from .generator import VideoGenerator
from .motion import MotionEffects
from .visual_style import VisualStyle
from .overlay import Overlay

__all__ = [
    'GenerationConfig',
    'VideoPipeline',
    'VideoGenerator',
    'MotionEffects',
    'VisualStyle',
    'Overlay',
]

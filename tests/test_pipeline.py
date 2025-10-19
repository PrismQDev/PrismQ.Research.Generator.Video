"""
Unit tests for video generation pipeline components.
"""
import unittest
import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import GenerationConfig
from motion import MotionEffects
from visual_style import VisualStyle
from overlay import Overlay
from generator import VideoGenerator


class TestGenerationConfig(unittest.TestCase):
    """Test configuration dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = GenerationConfig()
        
        self.assertEqual(config.output_resolution, (1080, 1920))
        self.assertEqual(config.fps, 30)
        self.assertEqual(config.target_duration, 27)
        self.assertEqual(config.base_clip_duration, 3)
        self.assertEqual(config.seed, 42)
    
    def test_calculated_properties(self):
        """Test calculated properties."""
        config = GenerationConfig(target_duration=30, base_clip_duration=3, fps=30)
        
        self.assertEqual(config.total_frames, 900)  # 30 * 30
        self.assertEqual(config.base_frames, 90)    # 3 * 30
        self.assertEqual(config.tiles_needed, 10)   # 900 / 90
    
    def test_neon_colors_initialization(self):
        """Test neon colors are properly initialized."""
        config = GenerationConfig()
        
        self.assertIsNotNone(config.neon_colors)
        self.assertEqual(len(config.neon_colors), 5)
        self.assertEqual(config.neon_colors[0], (0, 255, 255))  # Cyan


class TestMotionEffects(unittest.TestCase):
    """Test motion effects."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = GenerationConfig()
        self.motion = MotionEffects(self.config)
        self.test_frame = np.ones((1920, 1080, 3), dtype=np.uint8) * 128
    
    def test_micro_movement(self):
        """Test micro-movement effect."""
        result = self.motion.apply_micro_movement(self.test_frame, 0)
        
        self.assertEqual(result.shape, self.test_frame.shape)
        self.assertIsInstance(result, np.ndarray)
    
    def test_parallax(self):
        """Test parallax effect."""
        result = self.motion.apply_parallax(self.test_frame, 0)
        
        self.assertEqual(result.shape, self.test_frame.shape)
        self.assertIsInstance(result, np.ndarray)
    
    def test_micro_zoom(self):
        """Test micro-zoom effect."""
        result = self.motion.apply_micro_zoom(self.test_frame, 0, 100)
        
        self.assertEqual(result.shape, self.test_frame.shape)
        self.assertIsInstance(result, np.ndarray)
    
    def test_pattern_break_detection(self):
        """Test pattern break detection."""
        # Should not break at frame 0
        should_break, break_type = self.motion.should_apply_pattern_break(0)
        self.assertFalse(should_break)
        
        # Should break at minor interval
        should_break, break_type = self.motion.should_apply_pattern_break(40)
        self.assertTrue(should_break)
        self.assertEqual(break_type, "minor")
        
        # Should break at major interval
        should_break, break_type = self.motion.should_apply_pattern_break(80)
        self.assertTrue(should_break)
        self.assertEqual(break_type, "major")
    
    def test_pattern_break_application(self):
        """Test pattern break effects."""
        # Minor break
        result = self.motion.apply_pattern_break(
            self.test_frame, 0, "minor", 0.5
        )
        self.assertEqual(result.shape, self.test_frame.shape)
        
        # Major break
        result = self.motion.apply_pattern_break(
            self.test_frame, 0, "major", 0.5
        )
        self.assertEqual(result.shape, self.test_frame.shape)
    
    def test_speed_pulse(self):
        """Test speed pulse calculation."""
        # Normal speed
        speed = self.motion.apply_speed_pulse(30, 50)
        self.assertEqual(speed, 1.0)
        
        # Pulsed speed at major break
        speed = self.motion.apply_speed_pulse(30, 80)
        self.assertEqual(speed, 1.4)


class TestVisualStyle(unittest.TestCase):
    """Test visual style processing."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = GenerationConfig()
        self.style = VisualStyle(self.config)
        self.test_frame = np.ones((1920, 1080, 3), dtype=np.uint8) * 128
    
    def test_dark_base(self):
        """Test dark base application."""
        result = self.style.apply_dark_base(self.test_frame)
        
        self.assertEqual(result.shape, self.test_frame.shape)
        # Should be darker than original
        self.assertLess(result.mean(), self.test_frame.mean())
    
    def test_edge_detection(self):
        """Test edge detection."""
        edges = self.style.detect_edges(self.test_frame)
        
        self.assertEqual(edges.shape, self.test_frame.shape[:2])
        self.assertEqual(edges.dtype, np.uint8)
    
    def test_neon_edges(self):
        """Test neon edge application."""
        edges = np.zeros((1920, 1080), dtype=np.uint8)
        edges[100:200, 100:200] = 255  # Create some edges
        
        result = self.style.apply_neon_edges(self.test_frame, edges)
        
        self.assertEqual(result.shape, self.test_frame.shape)
    
    def test_contrast_saturation_boost(self):
        """Test contrast and saturation boost."""
        result = self.style.boost_contrast_saturation(self.test_frame)
        
        self.assertEqual(result.shape, self.test_frame.shape)
        self.assertIsInstance(result, np.ndarray)
    
    def test_full_style_pipeline(self):
        """Test complete style pipeline."""
        result = self.style.apply_full_style(self.test_frame)
        
        self.assertEqual(result.shape, self.test_frame.shape)
        self.assertIsInstance(result, np.ndarray)


class TestOverlay(unittest.TestCase):
    """Test overlay system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = GenerationConfig()
        self.overlay = Overlay(self.config)
        self.test_frame = np.ones((1920, 1080, 3), dtype=np.uint8) * 128
    
    def test_add_caption(self):
        """Test caption addition."""
        self.overlay.add_caption("Test Caption", 0)
        
        self.assertEqual(len(self.overlay.captions), 1)
        self.assertEqual(self.overlay.captions[0]['text'], "Test Caption")
        self.assertEqual(self.overlay.captions[0]['start'], 0)
    
    def test_draw_caption(self):
        """Test caption drawing."""
        result = self.overlay.draw_caption(self.test_frame, "Test", 1.0)
        
        self.assertEqual(result.shape, self.test_frame.shape)
        # Should be different from original due to text
        self.assertFalse(np.array_equal(result, self.test_frame))
    
    def test_draw_progress_bar(self):
        """Test progress bar drawing."""
        result = self.overlay.draw_progress_bar(self.test_frame, 0.5)
        
        self.assertEqual(result.shape, self.test_frame.shape)
        # Should be different from original due to progress bar
        self.assertFalse(np.array_equal(result, self.test_frame))
    
    def test_apply_overlays(self):
        """Test overlay application."""
        self.overlay.add_caption("Test", 0)
        result = self.overlay.apply_overlays(self.test_frame, 10, 100)
        
        self.assertEqual(result.shape, self.test_frame.shape)


class TestVideoGenerator(unittest.TestCase):
    """Test video generator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = GenerationConfig(base_clip_duration=1)  # Short for testing
        self.generator = VideoGenerator(self.config)
    
    def test_generate_abstract_frame(self):
        """Test abstract frame generation."""
        frame = self.generator.generate_abstract_frame(0, 30)
        
        h, w = self.config.output_resolution[1], self.config.output_resolution[0]
        self.assertEqual(frame.shape, (h, w, 3))
        self.assertEqual(frame.dtype, np.uint8)
    
    def test_generate_base_clip(self):
        """Test base clip generation."""
        frames = self.generator.generate_base_clip()
        
        self.assertEqual(len(frames), self.config.base_frames)
        self.assertEqual(frames[0].shape[0], 1920)
        self.assertEqual(frames[0].shape[1], 1080)
    
    def test_tile_clip(self):
        """Test clip tiling."""
        base_frames = self.generator.generate_base_clip()
        tiled_frames = self.generator.tile_clip(base_frames)
        
        # Should have close to target number of frames
        self.assertGreaterEqual(len(tiled_frames), self.config.total_frames)


if __name__ == '__main__':
    unittest.main()

"""
Unit tests for universal keyframe generation.

Tests the core functionality of the universal keyframe generator
for 2-3 minute videos.
"""

import sys
import os
import unittest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from universal_keyframes import (
    Scene,
    Keyframe,
    TransitionEffect,
    UniversalKeyframeGenerator,
    TransitionRenderer,
    generate_example_video_structure
)
import numpy as np


class TestScene(unittest.TestCase):
    """Test Scene class."""
    
    def test_scene_creation(self):
        """Test basic scene creation."""
        scene = Scene(0, 0.0, 15.0, "Test scene")
        self.assertEqual(scene.index, 0)
        self.assertEqual(scene.start_time, 0.0)
        self.assertEqual(scene.end_time, 15.0)
        self.assertEqual(scene.duration, 15.0)
        self.assertEqual(scene.content, "Test scene")
    
    def test_scene_auto_content(self):
        """Test automatic content generation."""
        scene = Scene(5, 50.0, 65.0)
        self.assertEqual(scene.content, "Scene 6")


class TestKeyframe(unittest.TestCase):
    """Test Keyframe class."""
    
    def test_keyframe_creation(self):
        """Test keyframe creation."""
        kf = Keyframe('scene_end', 0, 450, 15.0, "Test content")
        self.assertEqual(kf.type, 'scene_end')
        self.assertEqual(kf.scene_index, 0)
        self.assertEqual(kf.frame, 450)
        self.assertEqual(kf.time, 15.0)
        self.assertEqual(kf.content, "Test content")


class TestTransitionEffect(unittest.TestCase):
    """Test TransitionEffect class."""
    
    def test_transition_creation(self):
        """Test transition effect creation."""
        transition = TransitionEffect('crossfade', 0.5, easing='ease_in_out')
        self.assertEqual(transition.type, 'crossfade')
        self.assertEqual(transition.duration, 0.5)
        self.assertEqual(transition.params['easing'], 'ease_in_out')


class TestUniversalKeyframeGenerator(unittest.TestCase):
    """Test UniversalKeyframeGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = UniversalKeyframeGenerator(fps=30)
    
    def test_define_scenes_basic(self):
        """Test basic scene definition."""
        scenes = self.generator.define_scenes(150, 10)
        
        self.assertEqual(len(scenes), 10)
        self.assertEqual(scenes[0].start_time, 0.0)
        self.assertEqual(scenes[0].end_time, 15.0)
        self.assertEqual(scenes[-1].end_time, 150.0)
    
    def test_define_scenes_with_content(self):
        """Test scene definition with custom content."""
        contents = ["Scene 1", "Scene 2", "Scene 3"]
        scenes = self.generator.define_scenes(45, 3, contents)
        
        self.assertEqual(len(scenes), 3)
        self.assertEqual(scenes[0].content, "Scene 1")
        self.assertEqual(scenes[1].content, "Scene 2")
        self.assertEqual(scenes[2].content, "Scene 3")
    
    def test_define_scenes_duration_warning(self):
        """Test warning for unusual durations."""
        # Should still work but print warning
        scenes = self.generator.define_scenes(60, 5)  # 60s is below 120s
        self.assertEqual(len(scenes), 5)
    
    def test_generate_keyframes(self):
        """Test keyframe generation."""
        scenes = self.generator.define_scenes(150, 10)
        keyframes = self.generator.generate_keyframes(scenes)
        
        # Should be 2 keyframes per transition (9 transitions for 10 scenes)
        self.assertEqual(len(keyframes), 18)
        
        # Check first transition
        self.assertEqual(keyframes[0].type, 'scene_end')
        self.assertEqual(keyframes[0].scene_index, 0)
        self.assertEqual(keyframes[1].type, 'scene_start')
        self.assertEqual(keyframes[1].scene_index, 1)
    
    def test_keyframe_frame_numbers(self):
        """Test correct frame number calculation."""
        scenes = self.generator.define_scenes(30, 2)  # 2 scenes, 15s each
        keyframes = self.generator.generate_keyframes(scenes)
        
        # At 30 fps, 15s = 450 frames
        self.assertEqual(keyframes[0].frame, 450)  # End of scene 0
        self.assertEqual(keyframes[1].frame, 450)  # Start of scene 1
    
    def test_select_transition_effect_default(self):
        """Test default transition effect selection."""
        scene_a = Scene(0, 0.0, 15.0, "Scene A")
        scene_b = Scene(1, 15.0, 30.0, "Scene B")
        
        transition = self.generator.select_transition_effect(scene_a, scene_b)
        
        self.assertEqual(transition.type, 'crossfade')
        self.assertEqual(transition.duration, 0.5)
    
    def test_select_transition_effect_custom(self):
        """Test custom transition effect selection."""
        scene_a = Scene(0, 0.0, 15.0, "Scene A")
        scene_b = Scene(1, 15.0, 30.0, "Scene B")
        
        rules = {
            '0->1': {
                'type': 'dip_to_black',
                'duration': 0.7,
                'params': {'fade_out': 0.3, 'fade_in': 0.3}
            }
        }
        
        transition = self.generator.select_transition_effect(scene_a, scene_b, rules)
        
        self.assertEqual(transition.type, 'dip_to_black')
        self.assertEqual(transition.duration, 0.7)
    
    def test_get_transition_frames(self):
        """Test transition frame count calculation."""
        transition = TransitionEffect('crossfade', 0.5)
        frames = self.generator.get_transition_frames(transition)
        
        # 0.5s at 30fps = 15 frames
        self.assertEqual(frames, 15)
    
    def test_calculate_video_structure(self):
        """Test video structure calculation."""
        scenes = self.generator.define_scenes(150, 10)
        structure = self.generator.calculate_video_structure(scenes)
        
        self.assertEqual(structure['total_duration'], 150.0)
        self.assertEqual(structure['scene_count'], 10)
        self.assertEqual(structure['transition_count'], 9)
        self.assertEqual(structure['keyframe_count'], 18)
        self.assertEqual(structure['fps'], 30)


class TestTransitionRenderer(unittest.TestCase):
    """Test TransitionRenderer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.frame_a = np.ones((1080, 1920, 3), dtype=np.uint8) * 100
        self.frame_b = np.ones((1080, 1920, 3), dtype=np.uint8) * 200
    
    def test_apply_crossfade(self):
        """Test crossfade transition."""
        # At 0% progress, should be frame_a
        result = TransitionRenderer.apply_crossfade(self.frame_a, self.frame_b, 0.0)
        np.testing.assert_array_equal(result, self.frame_a)
        
        # At 100% progress, should be frame_b
        result = TransitionRenderer.apply_crossfade(self.frame_a, self.frame_b, 1.0)
        np.testing.assert_array_equal(result, self.frame_b)
        
        # At 50% progress, should be blend
        result = TransitionRenderer.apply_crossfade(self.frame_a, self.frame_b, 0.5)
        expected = np.ones((1080, 1920, 3), dtype=np.uint8) * 150
        np.testing.assert_array_equal(result, expected)
    
    def test_apply_dip_to_black_fade_out(self):
        """Test dip to black fade out phase."""
        result = TransitionRenderer.apply_dip_to_black(self.frame_a, 0.0, 'fade_out')
        np.testing.assert_array_equal(result, self.frame_a)
        
        result = TransitionRenderer.apply_dip_to_black(self.frame_a, 1.0, 'fade_out')
        expected = np.zeros_like(self.frame_a)
        np.testing.assert_array_equal(result, expected)
    
    def test_apply_dip_to_black_black_phase(self):
        """Test dip to black black phase."""
        result = TransitionRenderer.apply_dip_to_black(self.frame_a, 0.5, 'black')
        expected = np.zeros_like(self.frame_a)
        np.testing.assert_array_equal(result, expected)
    
    def test_apply_dip_to_black_fade_in(self):
        """Test dip to black fade in phase."""
        result = TransitionRenderer.apply_dip_to_black(self.frame_b, 0.0, 'fade_in')
        expected = np.zeros_like(self.frame_b)
        np.testing.assert_array_equal(result, expected)
        
        result = TransitionRenderer.apply_dip_to_black(self.frame_b, 1.0, 'fade_in')
        np.testing.assert_array_equal(result, self.frame_b)
    
    def test_apply_wipe_left_to_right(self):
        """Test wipe transition left to right."""
        result = TransitionRenderer.apply_wipe(self.frame_a, self.frame_b, 0.5, 'left_to_right')
        
        # Left half should be frame_b, right half should be frame_a
        mid_point = 1920 // 2
        np.testing.assert_array_equal(result[:, :mid_point], self.frame_b[:, :mid_point])
        np.testing.assert_array_equal(result[:, mid_point:], self.frame_a[:, mid_point:])
    
    def test_apply_wipe_top_to_bottom(self):
        """Test wipe transition top to bottom."""
        result = TransitionRenderer.apply_wipe(self.frame_a, self.frame_b, 0.5, 'top_to_bottom')
        
        # Top half should be frame_b, bottom half should be frame_a
        mid_point = 1080 // 2
        np.testing.assert_array_equal(result[:mid_point, :], self.frame_b[:mid_point, :])
        np.testing.assert_array_equal(result[mid_point:, :], self.frame_a[mid_point:, :])
    
    def test_apply_subtle_slide(self):
        """Test subtle slide transition."""
        result = TransitionRenderer.apply_subtle_slide(self.frame_a, self.frame_b, 0.5, 'up')
        
        # Should be a valid frame
        self.assertEqual(result.shape, self.frame_a.shape)
        self.assertEqual(result.dtype, np.uint8)
    
    def test_apply_transition_dispatcher(self):
        """Test the apply_transition dispatcher method."""
        # Test crossfade
        result = TransitionRenderer.apply_transition(self.frame_a, self.frame_b, 'crossfade', 0.5)
        expected = np.ones((1080, 1920, 3), dtype=np.uint8) * 150
        np.testing.assert_array_equal(result, expected)
        
        # Test zoom_in
        result = TransitionRenderer.apply_transition(self.frame_a, self.frame_b, 'zoom_in', 0.5)
        self.assertEqual(result.shape, self.frame_a.shape)
        
        # Test zoom_out
        result = TransitionRenderer.apply_transition(self.frame_a, self.frame_b, 'zoom_out', 0.5)
        self.assertEqual(result.shape, self.frame_a.shape)
        
        # Test subtle_slide
        result = TransitionRenderer.apply_transition(self.frame_a, self.frame_b, 'subtle_slide', 0.5, direction='up')
        self.assertEqual(result.shape, self.frame_a.shape)
        
        # Test unknown type (should default to crossfade)
        result = TransitionRenderer.apply_transition(self.frame_a, self.frame_b, 'unknown', 0.5)
        np.testing.assert_array_equal(result, expected)


class TestExampleGeneration(unittest.TestCase):
    """Test example video structure generation."""
    
    def test_generate_example_structure(self):
        """Test generating example video structure."""
        structure = generate_example_video_structure(150, 10, 30)
        
        self.assertEqual(structure['total_duration'], 150.0)
        self.assertEqual(structure['scene_count'], 10)
        self.assertEqual(structure['transition_count'], 9)
        self.assertEqual(structure['keyframe_count'], 18)
        self.assertEqual(structure['fps'], 30)
        
        # Check scenes have content
        self.assertTrue(all(scene.content for scene in structure['scenes']))


if __name__ == '__main__':
    unittest.main()

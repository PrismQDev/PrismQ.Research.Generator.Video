#!/usr/bin/env python3
"""
Example script demonstrating universal keyframe generation for 2-3 minute videos.

This script shows how to use the UniversalKeyframeGenerator to create
optimal scene-based structures for longer-form content that works across
all major video platforms.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from universal_keyframes import (
    UniversalKeyframeGenerator,
    TransitionEffect,
    generate_example_video_structure,
    print_video_structure
)


def example_educational_tutorial():
    """
    Example: Educational tutorial video (2.5 minutes).
    
    This demonstrates creating a structured educational video with
    clear scene boundaries and appropriate transitions.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 1: EDUCATIONAL TUTORIAL (2.5 minutes)")
    print("=" * 70 + "\n")
    
    generator = UniversalKeyframeGenerator(fps=30)
    
    # Define educational content
    educational_content = [
        "Introduction and hook",
        "Problem statement",
        "Solution overview",
        "Step 1: Setup",
        "Step 2: Configuration",
        "Step 3: Implementation",
        "Step 4: Testing",
        "Results and benefits",
        "Summary and recap",
        "Call to action"
    ]
    
    # Create scenes (150 seconds / 10 scenes = 15s per scene)
    scenes = generator.define_scenes(
        total_duration=150,
        target_scene_count=10,
        scene_contents=educational_content
    )
    
    # Generate keyframes
    keyframes = generator.generate_keyframes(scenes)
    
    # Define custom transition rules
    transition_rules = {
        '0->1': {'type': 'crossfade', 'duration': 0.5},      # Intro → Problem
        '1->2': {'type': 'crossfade', 'duration': 0.5},      # Problem → Solution
        '2->3': {'type': 'dip_to_black', 'duration': 0.7},   # Solution → Steps (major shift)
        '3->4': {'type': 'wipe', 'duration': 0.5, 'params': {'direction': 'left_to_right'}},
        '4->5': {'type': 'wipe', 'duration': 0.5, 'params': {'direction': 'left_to_right'}},
        '5->6': {'type': 'wipe', 'duration': 0.5, 'params': {'direction': 'left_to_right'}},
        '6->7': {'type': 'crossfade', 'duration': 0.5},      # Steps → Results
        '7->8': {'type': 'crossfade', 'duration': 0.5},      # Results → Summary
        '8->9': {'type': 'dip_to_black', 'duration': 0.7},   # Summary → CTA (major shift)
    }
    
    # Print structure
    structure = generator.calculate_video_structure(scenes)
    print_video_structure(structure)
    
    print("\nTRANSITION STRATEGY:")
    print("-" * 70)
    for i in range(len(scenes) - 1):
        scene_a = scenes[i]
        scene_b = scenes[i + 1]
        transition = generator.select_transition_effect(scene_a, scene_b, transition_rules)
        print(f"  Scene {i} → {i+1}: {transition.type} ({transition.duration}s)")
    
    print("\nPLATFORM COMPATIBILITY:")
    print("-" * 70)
    print("  ✅ TikTok (9:16, 1080×1920) - PRIMARY")
    print("  ✅ Instagram Reels (9:16, 1080×1920) - PRIMARY")
    print("  ✅ YouTube Shorts (9:16, 1080×1920) - PRIMARY")
    print("  ✅ YouTube (16:9, 1920×1080 or adapt from 9:16)")
    print("  ✅ Facebook (1:1, 1080×1080 or crop from 9:16)")
    print("  ✅ LinkedIn (16:9, 1920×1080 or adapt from 9:16)")
    print("  ✅ Twitter/X (16:9, 1920×1080 or adapt from 9:16)")
    
    print("\nEXPECTED METRICS:")
    print("-" * 70)
    print("  • Target completion rate: 65-75%")
    print("  • Average view duration: 90-120s")
    print("  • Retention at 30s: 80-85%")
    print("  • Retention at 60s: 70-75%")
    print("  • Retention at 90s: 60-70%")


def example_storytelling_video():
    """
    Example: Storytelling video (3 minutes).
    
    This demonstrates creating a narrative structure with dramatic
    transitions at key moments.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: STORYTELLING VIDEO (3 minutes)")
    print("=" * 70 + "\n")
    
    generator = UniversalKeyframeGenerator(fps=30)
    
    # Define story content
    story_content = [
        "Hook: Mysterious opening",
        "Character introduction",
        "Setting the scene",
        "Rising action: Conflict emerges",
        "Rising action: Tension builds",
        "Rising action: Stakes raised",
        "Climax build-up",
        "Climax: Peak moment",
        "Falling action: Resolution begins",
        "Resolution: Conclusion",
        "Twist or reveal",
        "Final message"
    ]
    
    # Create scenes (180 seconds / 12 scenes = 15s per scene)
    scenes = generator.define_scenes(
        total_duration=180,
        target_scene_count=12,
        scene_contents=story_content
    )
    
    # Generate keyframes
    keyframes = generator.generate_keyframes(scenes)
    
    # Define narrative-driven transition rules
    transition_rules = {
        '0->1': {'type': 'crossfade', 'duration': 0.6},       # Hook → Character
        '1->2': {'type': 'crossfade', 'duration': 0.5},       # Character → Setting
        '2->3': {'type': 'subtle_slide', 'duration': 0.4},    # Setting → Rising 1
        '3->4': {'type': 'subtle_slide', 'duration': 0.4},    # Rising 1 → 2
        '4->5': {'type': 'subtle_slide', 'duration': 0.4},    # Rising 2 → 3
        '5->6': {'type': 'zoom_in', 'duration': 0.6},         # Rising 3 → Build-up
        '6->7': {'type': 'crossfade', 'duration': 0.3},       # Build-up → Climax (fast)
        '7->8': {'type': 'dip_to_black', 'duration': 0.8},    # Climax → Falling (dramatic)
        '8->9': {'type': 'crossfade', 'duration': 0.5},       # Falling → Resolution
        '9->10': {'type': 'zoom_out', 'duration': 0.6},       # Resolution → Twist
        '10->11': {'type': 'crossfade', 'duration': 0.5},     # Twist → Conclusion
    }
    
    # Print structure
    structure = generator.calculate_video_structure(scenes)
    print_video_structure(structure)
    
    print("\nNARRATIVE STRUCTURE:")
    print("-" * 70)
    print("  Act 1 (Setup):    Scenes 0-2   (0-45s)")
    print("  Act 2 (Rising):   Scenes 3-6   (45-105s)")
    print("  Act 3 (Climax):   Scenes 7-8   (105-135s)")
    print("  Act 4 (Resolve):  Scenes 9-11  (135-180s)")
    
    print("\nEXPECTED METRICS:")
    print("-" * 70)
    print("  • Target completion rate: 60-70%")
    print("  • Average view duration: 110-140s")
    print("  • Hook retention (0-5s): 85-90%")
    print("  • Retention at climax (105s): 65-70%")
    print("  • Rewatch rate: 15-25%")


def example_product_demo():
    """
    Example: Product demonstration (2 minutes).
    
    This demonstrates creating a concise product demo with
    feature highlights and clear calls to action.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: PRODUCT DEMONSTRATION (2 minutes)")
    print("=" * 70 + "\n")
    
    generator = UniversalKeyframeGenerator(fps=30)
    
    # Define product demo content
    demo_content = [
        "Product introduction",
        "Problem it solves",
        "Feature 1: Core functionality",
        "Feature 2: Advanced options",
        "Feature 3: Integration",
        "Use case scenario",
        "Pricing and availability",
        "Call to action"
    ]
    
    # Create scenes (120 seconds / 8 scenes = 15s per scene)
    scenes = generator.define_scenes(
        total_duration=120,
        target_scene_count=8,
        scene_contents=demo_content
    )
    
    # Generate keyframes
    keyframes = generator.generate_keyframes(scenes)
    
    # Define product-focused transition rules
    transition_rules = {
        '0->1': {'type': 'crossfade', 'duration': 0.5},      # Intro → Problem
        '1->2': {'type': 'dip_to_black', 'duration': 0.7},   # Problem → Features (shift)
        '2->3': {'type': 'wipe', 'duration': 0.4, 'params': {'direction': 'left_to_right'}},
        '3->4': {'type': 'wipe', 'duration': 0.4, 'params': {'direction': 'left_to_right'}},
        '4->5': {'type': 'zoom_out', 'duration': 0.6},       # Features → Use case
        '5->6': {'type': 'crossfade', 'duration': 0.5},      # Use case → Pricing
        '6->7': {'type': 'dip_to_black', 'duration': 0.7},   # Pricing → CTA
    }
    
    # Print structure
    structure = generator.calculate_video_structure(scenes)
    print_video_structure(structure)
    
    print("\nPRODUCT DEMO FLOW:")
    print("-" * 70)
    print("  Introduction:  Scene 0      (0-15s)    - Hook + product reveal")
    print("  Problem:       Scene 1      (15-30s)   - Pain points")
    print("  Features:      Scenes 2-4   (30-75s)   - Feature highlights")
    print("  Use Case:      Scene 5      (75-90s)   - Real-world example")
    print("  Conversion:    Scenes 6-7   (90-120s)  - Pricing + CTA")
    
    print("\nEXPECTED METRICS:")
    print("-" * 70)
    print("  • Target completion rate: 70-80%")
    print("  • Average view duration: 85-100s")
    print("  • Feature section retention: 75-80%")
    print("  • CTA click-through rate: 8-12%")


def encoding_specifications():
    """Display recommended encoding specifications."""
    print("\n" + "=" * 70)
    print("UNIVERSAL ENCODING SPECIFICATIONS")
    print("=" * 70 + "\n")
    
    print("VIDEO CODEC SETTINGS:")
    print("-" * 70)
    print("  Codec:            H.264 (libx264)")
    print("  Profile:          High")
    print("  Level:            4.2")
    print("  Pixel Format:     yuv420p")
    print("  Color Space:      bt709 (HD standard)")
    print("  Color Range:      TV (limited, 16-235)")
    
    print("\nRESOLUTION & ASPECT RATIO:")
    print("-" * 70)
    print("  9:16 Vertical:    1080×1920 (TikTok, Reels, Shorts) - PRIMARY")
    print("  16:9 Landscape:   1920×1080 (YouTube, Facebook, LinkedIn)")
    print("  1:1 Square:       1080×1080 (Instagram Feed, Facebook)")
    print("  4:5 Portrait:     1080×1350 (Instagram Feed)")
    print("\n  Recommendation: Use 9:16 (1080×1920) as primary for 2-3 min videos")
    
    print("\nFRAME RATE:")
    print("-" * 70)
    print("  Recommended:      30 fps (universal compatibility)")
    print("  Alternative:      24, 25, 60 fps")
    
    print("\nBITRATE & GOP:")
    print("-" * 70)
    print("  Video Bitrate:    8 Mbps (high quality)")
    print("  Audio Bitrate:    192 kbps AAC")
    print("  GOP Size:         60 frames (2s at 30fps)")
    print("  Keyframe Int:     2 seconds")
    
    print("\nFILE SIZE ESTIMATES:")
    print("-" * 70)
    print("  2 min @ 1080p:    ~30-50 MB")
    print("  2.5 min @ 1080p:  ~40-65 MB")
    print("  3 min @ 1080p:    ~45-75 MB")
    
    print("\nFFMPEG COMMAND EXAMPLE:")
    print("-" * 70)
    print("""  ffmpeg -i input.mp4 \\
    -c:v libx264 -profile:v high -level 4.2 \\
    -pix_fmt yuv420p -colorspace bt709 -color_range tv \\
    -b:v 8M -maxrate 10M -bufsize 20M \\
    -g 60 -keyint_min 60 -sc_threshold 0 \\
    -c:a aac -b:a 192k -ar 48000 -ac 2 \\
    -movflags +faststart \\
    output_universal.mp4""")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("UNIVERSAL KEYFRAME GENERATION - EXAMPLES")
    print("=" * 70)
    print("\nThis script demonstrates optimal keyframe generation strategies")
    print("for 2-3 minute videos that work across all major platforms.")
    print("\nKey principles:")
    print("  • Scene-based structure (8-15 scenes)")
    print("  • Two keyframes per transition (scene end + scene start)")
    print("  • Strategic transitions for retention")
    print("  • Platform-universal encoding")
    
    # Run examples
    example_educational_tutorial()
    example_storytelling_video()
    example_product_demo()
    encoding_specifications()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("\nKey takeaways:")
    print("  ✅ Use 8-15 scenes for 2-3 minute videos")
    print("  ✅ Generate exactly 2 keyframes per transition")
    print("  ✅ Primary format: 9:16 (1080×1920) for mobile platforms")
    print("  ✅ Use crossfade (0.5s) as default transition")
    print("  ✅ Add dramatic transitions (dip to black) sparingly")
    print("  ✅ Encode with H.264, yuv420p, 30fps, 2s GOP")
    print("  ✅ Test on TikTok/Reels/Shorts first, then adapt for other platforms")
    print("\nFor more details, see: docs/UNIVERSAL_KEYFRAME_GUIDE.md")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

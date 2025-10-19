#!/usr/bin/env python3
"""
Example script demonstrating video generation with visual engagement principles.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import GenerationConfig
from pipeline import VideoPipeline


def main():
    """Generate example video with optimal engagement settings."""
    
    # Create configuration
    config = GenerationConfig(
        output_resolution=(1080, 1920),  # 9:16 vertical
        fps=30,
        target_duration=27,  # 27 seconds
        base_clip_duration=3,
        seed=42,
        cfg_scale=7.0,
    )
    
    # Initialize pipeline
    pipeline = VideoPipeline(config)
    
    # Define captions (synchronized with pattern breaks)
    captions = [
        ("Visual Engagement Principles", 0),
        ("Constant Motion", 120),
        ("High Contrast + Neon", 240),
        ("Pattern Breaks", 360),
        ("Optimized for Watch Time", 480),
        ("Built with PrismQ", 600),
    ]
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "engagement_video.mp4")
    
    # Run pipeline
    print("\n🎬 Starting video generation...")
    print(f"📊 Configuration:")
    print(f"   - Resolution: {config.output_resolution[0]}×{config.output_resolution[1]}")
    print(f"   - Duration: {config.target_duration}s")
    print(f"   - FPS: {config.fps}")
    print(f"   - Seed: {config.seed}\n")
    
    pipeline.run_full_pipeline(output_path, captions)
    
    print(f"\n✅ Done! Video saved to: {output_path}")
    print(f"\n💡 Key features applied:")
    print(f"   ✓ Constant micro-movement (nothing static >300ms)")
    print(f"   ✓ High contrast with neon accents")
    print(f"   ✓ Pattern breaks every ~1.5s")
    print(f"   ✓ Micro-zoom progression")
    print(f"   ✓ Story captions")
    print(f"   ✓ Progress bar overlay")


if __name__ == "__main__":
    main()

"""
SRT Subtitles to Universal Keyframes Workflow

This module implements the complete workflow for generating universal keyframes
from SRT subtitle files for 2-3 minute videos optimized for mobile platforms.
"""

import re
import json
from typing import List, Dict, Optional


def parse_srt_file(filepath: str) -> List[Dict]:
    """
    Parse SRT subtitle file into structured data.
    
    Args:
        filepath: Path to .srt file
        
    Returns:
        List of subtitle entries with timing and text
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into subtitle blocks
    blocks = content.strip().split('\n\n')
    subtitles = []
    
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            # Parse timing line (format: HH:MM:SS,mmm --> HH:MM:SS,mmm)
            timing_line = lines[1]
            time_pattern = r'(\d{2}):(\d{2}):(\d{2}),(\d{3})'
            times = re.findall(time_pattern, timing_line)
            
            if len(times) >= 2:
                # Calculate start time in seconds
                start_h, start_m, start_s, start_ms = times[0]
                start_time = (int(start_h) * 3600 + 
                            int(start_m) * 60 + 
                            int(start_s) + 
                            int(start_ms) / 1000.0)
                
                # Calculate end time in seconds
                end_h, end_m, end_s, end_ms = times[1]
                end_time = (int(end_h) * 3600 + 
                          int(end_m) * 60 + 
                          int(end_s) + 
                          int(end_ms) / 1000.0)
                
                # Extract text (lines 3 onwards)
                text = ' '.join(lines[2:])
                
                subtitles.append({
                    'index': len(subtitles),
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': end_time - start_time,
                    'text': text.strip()
                })
    
    return subtitles


def identify_scenes_from_subtitles(
    subtitles: List[Dict],
    min_scene_duration: float = 10.0,
    max_scene_duration: float = 20.0,
    target_scene_count: Optional[int] = None
) -> List[Dict]:
    """
    Convert subtitles into scenes based on content and timing.
    
    Args:
        subtitles: Parsed subtitle data
        min_scene_duration: Minimum scene length (seconds)
        max_scene_duration: Maximum scene length (seconds)
        target_scene_count: Desired number of scenes (optional)
        
    Returns:
        List of scene definitions
    """
    if not subtitles:
        return []
    
    scenes = []
    current_scene_start = subtitles[0]['start_time']
    current_scene_text = []
    
    # Transition words that suggest scene breaks
    transition_words = [
        'but', 'however', 'meanwhile', 'next', 'then', 
        'finally', 'now', 'suddenly', 'later', 'first',
        'second', 'third', 'lastly'
    ]
    
    for i, subtitle in enumerate(subtitles):
        current_scene_text.append(subtitle['text'])
        current_duration = subtitle['end_time'] - current_scene_start
        
        # Determine if this is a scene boundary
        is_sentence_end = subtitle['text'].strip().endswith(('.', '?', '!'))
        is_long_enough = current_duration >= min_scene_duration
        is_too_long = current_duration >= max_scene_duration
        is_last = (i == len(subtitles) - 1)
        
        # Check for transition words
        has_transition = any(
            word in subtitle['text'].lower().split()
            for word in transition_words
        )
        
        # Check for timing gap to next subtitle
        has_gap = False
        if i < len(subtitles) - 1:
            gap = subtitles[i + 1]['start_time'] - subtitle['end_time']
            has_gap = gap > 0.5  # 500ms pause
        
        # Create scene if conditions met
        if (is_sentence_end and is_long_enough) or is_too_long or is_last:
            scene = {
                'index': len(scenes),
                'start_time': current_scene_start,
                'end_time': subtitle['end_time'],
                'duration': subtitle['end_time'] - current_scene_start,
                'text': ' '.join(current_scene_text),
                'subtitle_count': len(current_scene_text),
                'has_transition': has_transition,
                'has_gap': has_gap
            }
            scenes.append(scene)
            
            # Reset for next scene
            if not is_last:
                current_scene_start = subtitles[i + 1]['start_time'] if i + 1 < len(subtitles) else subtitle['end_time']
                current_scene_text = []
    
    return scenes


def generate_keyframes_from_scenes(
    scenes: List[Dict],
    fps: int = 30
) -> List[Dict]:
    """
    Generate transition keyframes from scene structure.
    
    Args:
        scenes: Scene definitions from identify_scenes_from_subtitles()
        fps: Frame rate (default 30)
        
    Returns:
        List of keyframe specifications
    """
    keyframes = []
    
    for i in range(len(scenes) - 1):
        current_scene = scenes[i]
        next_scene = scenes[i + 1]
        
        # Keyframe 1: Scene End
        scene_end_kf = {
            'type': 'scene_end',
            'scene_index': i,
            'frame': int(current_scene['end_time'] * fps),
            'time': current_scene['end_time'],
            'content': current_scene['text'][:100],  # Truncate for display
            'subtitle_context': current_scene['text'].split('.')[-1].strip() if '.' in current_scene['text'] else current_scene['text'][:50]
        }
        keyframes.append(scene_end_kf)
        
        # Keyframe 2: Scene Start
        scene_start_kf = {
            'type': 'scene_start',
            'scene_index': i + 1,
            'frame': int(next_scene['start_time'] * fps),
            'time': next_scene['start_time'],
            'content': next_scene['text'][:100],
            'subtitle_context': next_scene['text'].split('.')[0].strip() if '.' in next_scene['text'] else next_scene['text'][:50]
        }
        keyframes.append(scene_start_kf)
    
    return keyframes


def select_transition_for_scenes(
    scene_a: Dict,
    scene_b: Dict
) -> Dict:
    """
    Select appropriate transition based on scene content.
    
    Args:
        scene_a: Outgoing scene
        scene_b: Incoming scene
        
    Returns:
        Transition specification
    """
    # Analyze content relationship
    has_transition_word = scene_a.get('has_transition', False)
    has_timing_gap = scene_a.get('has_gap', False)
    
    # Check for topic shift (simple heuristic: different first words)
    words_a = set(scene_a['text'].lower().split()[:10])
    words_b = set(scene_b['text'].lower().split()[:10])
    topic_shift = len(words_a & words_b) < 3  # Less than 3 words in common
    
    # Select transition type
    if topic_shift and has_timing_gap:
        # Major topic change with pause
        return {
            'type': 'dip_to_black',
            'duration': 0.7,
            'fade_out': 0.3,
            'black_hold': 0.1,
            'fade_in': 0.3
        }
    elif has_transition_word:
        # Sequential content (step 1 → step 2)
        return {
            'type': 'wipe',
            'duration': 0.5,
            'direction': 'left_to_right'
        }
    else:
        # Related content, smooth flow
        return {
            'type': 'crossfade',
            'duration': 0.5,
            'easing': 'ease_in_out'
        }


def create_video_structure_from_srt(
    srt_filepath: str,
    fps: int = 30,
    min_scene_duration: float = 10.0,
    max_scene_duration: float = 20.0
) -> Dict:
    """
    Complete workflow: SRT → Scenes → Keyframes → Video Structure.
    
    Args:
        srt_filepath: Path to SRT subtitle file
        fps: Frame rate
        min_scene_duration: Minimum scene length (seconds)
        max_scene_duration: Maximum scene length (seconds)
        
    Returns:
        Complete video structure with all specifications
    """
    # Step 1: Parse SRT
    print("Step 1: Parsing SRT file...")
    subtitles = parse_srt_file(srt_filepath)
    print(f"  ✓ Parsed {len(subtitles)} subtitle entries")
    
    if not subtitles:
        print("  ✗ No subtitles found in file")
        return {}
    
    # Step 2: Identify scenes
    print("\nStep 2: Identifying scenes...")
    scenes = identify_scenes_from_subtitles(
        subtitles,
        min_scene_duration=min_scene_duration,
        max_scene_duration=max_scene_duration
    )
    print(f"  ✓ Created {len(scenes)} scenes")
    
    # Step 3: Generate keyframes
    print("\nStep 3: Generating keyframes...")
    keyframes = generate_keyframes_from_scenes(scenes, fps)
    print(f"  ✓ Generated {len(keyframes)} keyframes")
    
    # Step 4: Select transitions
    print("\nStep 4: Selecting transitions...")
    transitions = []
    for i in range(len(scenes) - 1):
        transition = select_transition_for_scenes(scenes[i], scenes[i + 1])
        transitions.append(transition)
    print(f"  ✓ Configured {len(transitions)} transitions")
    
    # Step 5: Calculate metrics
    total_duration = scenes[-1]['end_time'] if scenes else 0
    avg_scene_duration = total_duration / len(scenes) if scenes else 0
    
    structure = {
        'source': srt_filepath,
        'total_duration': total_duration,
        'subtitle_count': len(subtitles),
        'scene_count': len(scenes),
        'keyframe_count': len(keyframes),
        'transition_count': len(transitions),
        'avg_scene_duration': avg_scene_duration,
        'fps': fps,
        'scenes': scenes,
        'keyframes': keyframes,
        'transitions': transitions,
        'encoding': {
            'resolution': '1080x1920',  # 9:16 vertical
            'aspect_ratio': '9:16',
            'codec': 'H.264',
            'fps': fps,
            'gop_size': fps * 2,  # 2 seconds
            'pixel_format': 'yuv420p',
            'bitrate': '8M'
        }
    }
    
    print("\n" + "=" * 60)
    print("VIDEO STRUCTURE COMPLETE")
    print("=" * 60)
    print(f"Total Duration:     {total_duration:.1f}s ({total_duration/60:.1f} min)")
    print(f"Scenes:             {len(scenes)}")
    print(f"Avg Scene Duration: {avg_scene_duration:.1f}s")
    print(f"Keyframes:          {len(keyframes)} (2 per transition)")
    print(f"Transitions:        {len(transitions)}")
    print(f"Format:             9:16 vertical (1080×1920)")
    print("=" * 60)
    
    return structure


def format_timecode(seconds: float) -> str:
    """Convert seconds to SRT timecode format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def export_json_structure(structure: Dict, output_path: str):
    """Export complete structure as JSON."""
    # Convert for JSON serialization
    export_data = {
        'metadata': {
            'source': structure['source'],
            'duration': structure['total_duration'],
            'scenes': structure['scene_count'],
            'keyframes': structure['keyframe_count'],
            'format': '9:16 vertical (1080×1920)',
            'fps': structure['fps']
        },
        'scenes': structure['scenes'],
        'keyframes': structure['keyframes'],
        'transitions': structure['transitions'],
        'encoding': structure['encoding']
    }
    
    with open(output_path, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"✓ Exported JSON structure to: {output_path}")


def export_edl_markers(structure: Dict, output_path: str):
    """Export keyframe markers in EDL format for video editors."""
    with open(output_path, 'w') as f:
        f.write("TITLE: Video Keyframes\n")
        f.write(f"FCM: NON-DROP FRAME\n\n")
        
        for i, kf in enumerate(structure['keyframes'], 1):
            # Convert to timecode (HH:MM:SS:FF)
            total_frames = kf['frame']
            fps = structure['fps']
            
            hours = total_frames // (fps * 3600)
            minutes = (total_frames // (fps * 60)) % 60
            seconds = (total_frames // fps) % 60
            frames = total_frames % fps
            
            timecode = f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frames:02d}"
            
            f.write(f"{i:03d}  001  V  C        {timecode} {timecode} ")
            f.write(f"{timecode} {timecode}\n")
            f.write(f"* FROM CLIP NAME: {kf['type']}_scene_{kf['scene_index']}\n")
            f.write(f"* COMMENT: {kf['subtitle_context'][:60]}\n\n")
    
    print(f"✓ Exported EDL markers to: {output_path}")


def export_enhanced_srt(structure: Dict, output_path: str):
    """Export SRT with scene transition markers."""
    with open(output_path, 'w') as f:
        subtitle_idx = 1
        
        for scene_idx, scene in enumerate(structure['scenes']):
            # Add scene marker
            start_tc = format_timecode(scene['start_time'])
            marker_tc = format_timecode(scene['start_time'] + 0.5)
            
            f.write(f"{subtitle_idx}\n")
            f.write(f"{start_tc} --> {marker_tc}\n")
            f.write(f"[SCENE {scene_idx + 1}]\n\n")
            subtitle_idx += 1
            
            # Add scene content (split into readable chunks)
            text = scene['text']
            max_chars = 60
            words = text.split()
            current_line = []
            lines = []
            
            for word in words:
                if sum(len(w) for w in current_line) + len(word) + len(current_line) > max_chars:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Write subtitle content
            content_start = scene['start_time'] + 0.5
            content_end = scene['end_time']
            
            start_tc = format_timecode(content_start)
            end_tc = format_timecode(content_end)
            
            f.write(f"{subtitle_idx}\n")
            f.write(f"{start_tc} --> {end_tc}\n")
            f.write('\n'.join(lines) + "\n\n")
            subtitle_idx += 1
    
    print(f"✓ Exported enhanced SRT to: {output_path}")


def print_structure_summary(structure: Dict):
    """Print a detailed summary of the video structure."""
    print("\n" + "=" * 70)
    print("DETAILED VIDEO STRUCTURE")
    print("=" * 70)
    
    print("\nSCENES:")
    print("-" * 70)
    for scene in structure['scenes']:
        print(f"Scene {scene['index']:2d}: {scene['start_time']:6.1f}s - {scene['end_time']:6.1f}s ({scene['duration']:5.1f}s)")
        print(f"  {scene['text'][:65]}...")
    
    print("\nKEYFRAMES:")
    print("-" * 70)
    for kf in structure['keyframes']:
        print(f"{kf['type']:12} | Frame {kf['frame']:5d} | {kf['time']:6.2f}s | Scene {kf['scene_index']}")
    
    print("\nTRANSITIONS:")
    print("-" * 70)
    for i, trans in enumerate(structure['transitions']):
        print(f"Scene {i} → {i+1}: {trans['type']:15} ({trans['duration']:.1f}s)")
    
    print("=" * 70)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python srt_to_keyframes.py <srt_file> [output_prefix]")
        print("\nExample:")
        print("  python srt_to_keyframes.py my_video.srt output")
        print("\nThis will create:")
        print("  - output_structure.json")
        print("  - output_markers.edl")
        print("  - output_enhanced.srt")
        sys.exit(1)
    
    srt_file = sys.argv[1]
    output_prefix = sys.argv[2] if len(sys.argv) > 2 else 'output'
    
    print("=" * 70)
    print("UNIVERSAL KEYFRAME GENERATION FROM SRT")
    print("=" * 70)
    print(f"\nInput:  {srt_file}")
    print(f"Output: {output_prefix}_*")
    print("Target: 9:16 vertical (1080×1920) for TikTok/Reels/Shorts\n")
    
    # Run complete workflow
    structure = create_video_structure_from_srt(srt_file, fps=30)
    
    if not structure:
        print("\n✗ Failed to create structure")
        sys.exit(1)
    
    # Export in multiple formats
    print("\nExporting outputs...")
    export_json_structure(structure, f'{output_prefix}_structure.json')
    export_edl_markers(structure, f'{output_prefix}_markers.edl')
    export_enhanced_srt(structure, f'{output_prefix}_enhanced.srt')
    
    # Print detailed summary
    print_structure_summary(structure)
    
    # Final summary
    print("\n" + "=" * 70)
    print("OUTPUTS CREATED")
    print("=" * 70)
    print(f"✓ {output_prefix}_structure.json  - Complete structure (JSON)")
    print(f"✓ {output_prefix}_markers.edl     - Timeline markers (EDL)")
    print(f"✓ {output_prefix}_enhanced.srt    - Subtitles with scene markers")
    print("\nNext steps:")
    print("1. Import structure.json into your video editing pipeline")
    print("2. Use scene boundaries to cut and arrange footage")
    print("3. Apply transitions according to specifications")
    print("4. Render at 1080×1920 (9:16) with H.264 encoding")
    print("5. Test on TikTok/Reels/Shorts before wide distribution")
    print("=" * 70)

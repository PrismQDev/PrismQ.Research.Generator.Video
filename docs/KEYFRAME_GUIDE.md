# Keyframe Generation Guide: From Subtitles to Visual Scenes

## Overview

This guide explains how to generate **strategic keyframes** from subtitle-derived scenes for short-form mobile video content (YouTube Shorts, TikTok, Instagram Reels).  

Keyframes serve as visual anchors that:
- Reinforce narrative structure  
- Capture and sustain viewer attention  
- Prevent habituation through visual variety  
- Sync visuals to narration/subtitles  
- Optimize for retention and virality

## Table of Contents

1. [Understanding Keyframes in Short-Form Content](#understanding-keyframes)
2. [Subtitle-to-Scene Segmentation](#subtitle-to-scene-segmentation)
3. [Keyframe Timing Strategy](#keyframe-timing-strategy)
4. [Visual Design Principles for Keyframes](#visual-design-principles)
5. [Platform-Specific Optimization](#platform-specific-optimization)
6. [Implementation Guide](#implementation-guide)
7. [Best Practices](#best-practices)

---

## Understanding Keyframes

### What Are Keyframes?

In short-form video, **keyframes** are the critical visual moments that:
- Mark scene transitions or narrative beats  
- Provide visual hooks to capture attention  
- Reinforce subtitle/narration timing  
- Prevent monotony through variation

### Types of Keyframes

1. **Hook Keyframe (0–3s)**  
   - Purpose: Prevent swipe-away  
   - Visuals: High contrast, bold motion, intrigue  
   - Sync: Opening statement or question  

2. **Transition Keyframes (every 3–5s)**  
   - Purpose: Maintain rhythm and variety  
   - Visuals: Pattern breaks, zoom, style shifts  
   - Sync: New sentence or topic  

3. **Emphasis Keyframes (narrative peaks)**  
   - Purpose: Highlight reveals or punchlines  
   - Visuals: Flash, zoom, color bursts  
   - Sync: Keywords, emotional spikes  

4. **Completion Keyframe (final 2–3s)**  
   - Purpose: Resolution, replay, or CTA  
   - Visuals: Loop point or call-to-action  
   - Sync: Closing line or outro

---

## Subtitle-to-Scene Segmentation

### Step 1: Parse Subtitle File

Common subtitle formats for short-form content:
- **SRT** (SubRip Subtitle)
- **VTT** (Web Video Text Tracks)
- **JSON** (Custom caption format)

Example SRT structure:
```
1
00:00:00,000 --> 00:00:03,000
Did you know this crazy fact?

2
00:00:03,000 --> 00:00:06,500
Scientists discovered something shocking.

3
00:00:06,500 --> 00:00:10,000
It changes everything we thought we knew.
```

### Step 2: Identify Scene Boundaries

Scene boundaries occur at:

**Natural Break Points:**
- Sentence endings (period, question mark, exclamation)
- Topic shifts (indicated by conjunctions: "but", "however", "meanwhile")
- Emotional tone changes (calm → exciting, serious → humorous)

**Timing-Based Breaks:**
- Every 3–5 seconds (optimal for maintaining attention)
- At pattern break intervals (aligns with visual rhythm)
- Before/after key reveals or punchlines

**Semantic Analysis:**
```python
def identify_scene_boundaries(subtitles):
    """
    Identify scene boundaries from subtitle timing and content.
    
    Args:
        subtitles: List of subtitle entries with text and timing
        
    Returns:
        List of scene boundary timestamps
    """
    boundaries = [0]  # Always start with opening frame
    
    for i, subtitle in enumerate(subtitles):
        # Check for sentence endings
        if subtitle['text'].strip().endswith(('.', '?', '!')):
            boundaries.append(subtitle['end_time'])
        
        # Check for 3-5 second rule
        if i > 0:
            time_since_last = subtitle['start_time'] - boundaries[-1]
            if time_since_last >= 3.0:
                boundaries.append(subtitle['start_time'])
        
        # Check for transition words
        transition_words = ['but', 'however', 'meanwhile', 'suddenly', 
                          'then', 'next', 'finally', 'now']
        if any(word in subtitle['text'].lower().split() 
               for word in transition_words):
            boundaries.append(subtitle['start_time'])
    
    return boundaries
```

### Step 3: Define Scene Duration

**Optimal Scene Lengths:**
- **YouTube Shorts**: 2–5 seconds per scene (12–30 scenes in 60s)
- **TikTok**: 1–3 seconds per scene (5–10 scenes in 15s)
- **Instagram Reels**: 2–4 seconds per scene (8–15 scenes in 30s)

**Scene Duration Guidelines:**
- **Min:** 1.5s (avoid jarring cuts)  
- **Max:** 5s (avoid attention decay)  
- **Optimal:** 3s (balance of variety + readability)

---

## Keyframe Timing Strategy

### Frame-Level Precision

For 30 fps video:
- **Keyframe interval**: 1 frame (precise visual change)
- **Transition duration**: 3–8 frames (0.1–0.27s for smooth blend)
- **Hold time**: 60–150 frames (2–5s per scene)

### Timing Alignment with Subtitles

**Method 1: Subtitle Start Sync**  
Keyframe appears at exact subtitle start time.

```python
def generate_keyframe_at_subtitle_start(subtitle_start_time, fps=30):
    """Generate keyframe at exact subtitle start."""
    return int(subtitle_start_time * fps)
```

**Method 2: Anticipatory Sync** (Recommended)  
Keyframe appears 200ms *before* subtitle for natural feel.

```python
def generate_anticipatory_keyframe(subtitle_start_time, fps=30, 
                                   anticipation_ms=200):
    """
    Generate keyframe slightly before subtitle appears.
    Creates visual-audio sync that feels natural.
    """
    anticipation_seconds = anticipation_ms / 1000.0
    keyframe_time = max(0, subtitle_start_time - anticipation_seconds)
    return int(keyframe_time * fps)
```

**Method 3: Pattern Break Sync** (Most Engaging)  
Align keyframes with rhythmic visual breaks for maximum engagement.
```python
def generate_pattern_break_keyframes(subtitles, fps=30, 
                                    minor_interval=40, 
                                    major_interval=80):
    """
    Align keyframes with pattern breaks for maximum engagement.
    Combines visual rhythm with narrative structure.
    """
    keyframes = []
    pattern_breaks = []
    
    # Generate pattern break points
    total_frames = int(subtitles[-1]['end_time'] * fps)
    for frame in range(0, total_frames, minor_interval):
        pattern_breaks.append(frame)
    
    # Align keyframes to nearest pattern break
    for subtitle in subtitles:
        subtitle_frame = int(subtitle['start_time'] * fps)
        nearest_break = min(pattern_breaks, 
                          key=lambda x: abs(x - subtitle_frame))
        
        if abs(nearest_break - subtitle_frame) <= fps * 0.5:  # Within 0.5s
            keyframes.append(nearest_break)
    
    return keyframes
```

### Keyframe Density Guidelines

**High Density (1–2s intervals)** — Energetic content  
- Use for: Comedy, action, rapid-fire facts  
- Platform: TikTok, fast Reels  

**Medium Density (3–4s intervals)** — Balanced content  
- Use for: Stories, tutorials, explanations  
- Platform: YouTube Shorts, standard Reels  

**Low Density (5–7s intervals)** — Slow-burn content  
- Use for: Emotional stories, suspense, art  
- Platform: Instagram Reels (aesthetic focus)

---

## Visual Design Principles for Keyframes

### 1. Hook Keyframes

**Visual Requirements:**
- **Maximum contrast + motion**: Start with highest impact  
- **Intrigue element**: Mystery, shock, or curiosity hook  
- **Large, readable text**: First subtitle immediately visible

**Design Formula:**
```python
def create_hook_keyframe(base_frame):
    """
    Apply maximum visual impact for opening frame.
    """
    # 1. Boost contrast to maximum
    contrast_factor = 2.0
    
    # 2. Add motion blur suggestion (directional blur)
    motion_intensity = "high"
    
    # 3. Apply brightest neon accents
    neon_coverage = 0.15  # 15% of frame
    
    # 4. Add zoom-in effect (starts at 105%, zooms to 100%)
    initial_scale = 1.05
    
    # 5. Position first subtitle prominently
    subtitle_position = "upper_third"
    subtitle_size = "large"  # 20% larger than normal
    
    return styled_frame
```

**Examples by Platform:**
- **YouTube Shorts**: Question text + zooming background
- **TikTok**: Fast motion + bright colors + text overlay
- **Instagram Reels**: Aesthetic hook + elegant text

### 2. Transition Keyframes

**Visual Strategy:**  
Provide variety while staying coherent. Use zooms, color shifts, motion speed changes, and pattern breaks for rhythm resets.

**Transition Types:**

**A. Zoom Transitions**
```python
# Zoom In: For emphasis or detail
zoom_range = (1.0, 1.15)  # 15% zoom over 0.3s

# Zoom Out: For reveal or context
zoom_range = (1.15, 1.0)  # Return to normal

# Pulsing: For rhythm and pattern breaks
zoom_pattern = [1.0, 1.05, 1.0]  # Quick pulse
```

**B. Color Transitions**
```python
# Color shift for mood change
color_transitions = {
    'neutral_to_exciting': (cyan, magenta),
    'calm_to_tense': (blue, red),
    'explanation_to_reveal': (white, yellow)
}
```

**C. Motion Transitions**
```python
# Speed changes
speed_transitions = {
    'normal_to_fast': 1.4,      # Action/excitement
    'fast_to_slow': 0.7,        # Emphasis/dramatic
    'slow_to_normal': 1.0       # Return to baseline
}
```

**D. Pattern Break Transitions**
```python
def apply_pattern_break_at_keyframe(frame, break_type, intensity):
    """
    Apply pattern break synchronized with scene change.
    
    Args:
        frame: Input frame
        break_type: 'minor' (rotation) or 'major' (zoom)
        intensity: 0.5 to 1.0
    """
    if break_type == 'minor':
        # Rotation twirl: ±45° over 5 frames
        rotation_angle = 45 * intensity
        
    elif break_type == 'major':
        # Zoom pop: 1.2x scale over 3 frames
        zoom_scale = 1.0 + (0.2 * intensity)
    
    return transformed_frame
```

### 3. Emphasis Keyframes

**When to Use:**  
Apply flash bursts, scale pops, or neon accents on:
- Keywords, punchlines, reveals  
- Call-to-action moments  
- Emotional peaks

**Visual Techniques:**

**A. Flash Emphasis**
```python
# Brief white flash or color burst
flash_duration = 2 frames  # 0.067s at 30fps
flash_intensity = 0.3      # 30% opacity
```

**B. Scale Emphasis**
```python
# Quick scale pop
scale_sequence = [1.0, 1.15, 1.05, 1.0]  # Over 6-8 frames
```

**C. Neon Accent Emphasis**
```python
# Intensify neon edges around key text
neon_boost = 1.5           # 50% brighter
glow_radius = 2.0          # Larger glow
```

### 4. Completion Keyframes

**Purpose:**  
Provide satisfying closure, encourage replay, or prompt next action.

**Options:**  
- **Seamless loop** → match opening frame  
- **CTA** → directive overlay  
- **Cliffhanger** → freeze or suspense frame  
- **Resolution** → warm, soft close

**Design Strategy:**
```python
def create_completion_keyframe(context):
    """
    Final frame design based on content type.
    """
    if context == 'loop_content':
        # Match opening frame for seamless loop
        return match_opening_visual()
        
    elif context == 'call_to_action':
        # Clear, bright, directive
        return cta_visual(text="Follow for more!", 
                         brightness=high,
                         motion=slow_zoom_in)
        
    elif context == 'cliffhanger':
        # Leave on mysterious note
        return suspense_visual(motion=freeze_frame,
                              contrast=high,
                              text="Part 2 coming...")
    
    else:  # satisfying_conclusion
        # Resolve visual tension
        return resolution_visual(motion=slow_settle,
                                contrast=medium,
                                color=warm)
```

---

## Platform-Specific Optimization

### YouTube Shorts (15–60 seconds)

**Keyframe Strategy:**
- **Density**: 1 keyframe every 3–4s (15–20 total)
- **Hook**: Questions/statements  
- **Mid-content**: Clear scene breaks  
- **Completion**: CTA or loop point

**Subtitle Integration:**
```python
youtube_shorts_keyframes = {
    'hook': 0,                    # Frame 0 (0.0s)
    'establish': 60,              # 2.0s
    'point_1': 120,               # 4.0s
    'point_2': 180,               # 6.0s
    'point_3': 240,               # 8.0s
    'conclusion': 300,            # 10.0s
    'cta': 360                    # 12.0s
}
```

**Visual Style:**
- Educational + entertaining aesthetic  
- Clear subtitles (many muted viewers)  
- Progress cues helpful  
- Aim for 90%+ completion

### TikTok (7–60 seconds, optimal 7–21s)

**Keyframe Strategy:**
- **Density**: 1 keyframe every 1–2s (7–10 in 15s)
- **Hook**: Within 1s (critical)  
- **Rapid pacing**: Quick scene changes  
- **Loop**: Loop-friendly completion

**Subtitle Integration:**
```python
tiktok_keyframes = {
    'hook': 0,                    # Frame 0 (0.0s) - CRITICAL
    'beat_1': 30,                 # 1.0s
    'beat_2': 60,                 # 2.0s
    'beat_3': 90,                 # 3.0s
    'climax': 120,                # 4.0s
    'resolve': 150,               # 5.0s
}
```

**Visual Style:**
- High energy, fast transitions  
- Bold text overlays  
- Seamless loop potential  
- Sound-on culture (captions still help)

### Instagram Reels (15–90 seconds, optimal 15–30s)

**Keyframe Strategy:**
- **Density**: 1 keyframe every 2–4s (8–15 in 30s)
- **Hook**: Aesthetic + intriguing  
- **Smooth transitions**: Polished, cohesive  
- **Brand-friendly**: Professional appearance

**Subtitle Integration:**
```python
instagram_reels_keyframes = {
    'hook': 0,                    # Frame 0 (0.0s)
    'scene_1': 90,                # 3.0s
    'scene_2': 180,               # 6.0s
    'scene_3': 270,               # 9.0s
    'scene_4': 360,               # 12.0s
    'conclusion': 450,            # 15.0s
}
```

**Visual Style:**
- Cohesive color + branding  
- Smooth, aesthetic transitions  
- Works both sound-on and sound-off

---

## Implementation Workflow

### Complete Workflow

#### Step 1: Parse Subtitles

```python
import json
import re
from typing import List, Dict

def parse_srt_file(filepath: str) -> List[Dict]:
    """
    Parse SRT subtitle file into structured data.
    
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
            # Parse timing
            timing_line = lines[1]
            times = re.findall(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', timing_line)
            
            if len(times) >= 2:
                start_time = (int(times[0][0]) * 3600 + 
                            int(times[0][1]) * 60 + 
                            int(times[0][2]) + 
                            int(times[0][3]) / 1000.0)
                
                end_time = (int(times[1][0]) * 3600 + 
                          int(times[1][1]) * 60 + 
                          int(times[1][2]) + 
                          int(times[1][3]) / 1000.0)
                
                # Parse text
                text = ' '.join(lines[2:])
                
                subtitles.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': end_time - start_time,
                    'text': text
                })
    
    return subtitles
```

#### Step 2: Identify Scenes

```python
def identify_scenes(subtitles: List[Dict], 
                   min_scene_duration: float = 1.5,
                   max_scene_duration: float = 5.0,
                   fps: int = 30) -> List[Dict]:
    """
    Segment subtitles into scenes based on content and timing.
    
    Args:
        subtitles: Parsed subtitle data
        min_scene_duration: Minimum scene length in seconds
        max_scene_duration: Maximum scene length in seconds
        fps: Frame rate
        
    Returns:
        List of scene definitions with keyframe positions
    """
    scenes = []
    current_scene_start = 0
    current_scene_text = []
    
    for i, subtitle in enumerate(subtitles):
        current_scene_text.append(subtitle['text'])
        
        # Check for scene break conditions
        is_sentence_end = subtitle['text'].strip().endswith(('.', '?', '!'))
        is_long_enough = (subtitle['end_time'] - current_scene_start) >= min_scene_duration
        is_too_long = (subtitle['end_time'] - current_scene_start) > max_scene_duration
        is_last = (i == len(subtitles) - 1)
        
        # Check for transition keywords
        transition_words = ['but', 'however', 'meanwhile', 'next', 'then']
        has_transition = any(word in subtitle['text'].lower() 
                           for word in transition_words)
        
        if (is_sentence_end and is_long_enough) or is_too_long or is_last:
            # Create scene
            scene = {
                'start_time': current_scene_start,
                'end_time': subtitle['end_time'],
                'duration': subtitle['end_time'] - current_scene_start,
                'start_frame': int(current_scene_start * fps),
                'end_frame': int(subtitle['end_time'] * fps),
                'text': ' '.join(current_scene_text),
                'has_transition': has_transition
            }
            scenes.append(scene)
            
            # Reset for next scene
            if not is_last:
                current_scene_start = subtitle['end_time']
                current_scene_text = []
    
    return scenes
```

#### Step 3: Generate Keyframes

```python
def generate_keyframes(scenes: List[Dict], 
                      platform: str = 'youtube_shorts',
                      fps: int = 30) -> List[Dict]:
    """
    Generate keyframe specifications for each scene.
    
    Args:
        scenes: Scene definitions from identify_scenes()
        platform: Target platform (youtube_shorts, tiktok, instagram_reels)
        fps: Frame rate
        
    Returns:
        List of keyframe definitions with visual instructions
    """
    keyframes = []
    
    # Platform-specific settings
    platform_config = {
        'youtube_shorts': {
            'hook_emphasis': 'high',
            'scene_density': 'medium',
            'transition_style': 'clear_cuts',
            'subtitle_prominence': 'very_high'
        },
        'tiktok': {
            'hook_emphasis': 'maximum',
            'scene_density': 'high',
            'transition_style': 'fast_blend',
            'subtitle_prominence': 'medium'
        },
        'instagram_reels': {
            'hook_emphasis': 'high',
            'scene_density': 'medium',
            'transition_style': 'smooth_aesthetic',
            'subtitle_prominence': 'high'
        }
    }
    
    config = platform_config.get(platform, platform_config['youtube_shorts'])
    
    for i, scene in enumerate(scenes):
        # Determine keyframe type
        if i == 0:
            keyframe_type = 'hook'
        elif i == len(scenes) - 1:
            keyframe_type = 'completion'
        else:
            keyframe_type = 'transition'
        
        # Create keyframe specification
        keyframe = {
            'frame': scene['start_frame'],
            'time': scene['start_time'],
            'type': keyframe_type,
            'scene_index': i,
            'text': scene['text'],
            
            # Visual properties
            'visual': generate_visual_properties(
                keyframe_type, 
                scene['has_transition'],
                config
            )
        }
        
        keyframes.append(keyframe)
    
    return keyframes

def generate_visual_properties(keyframe_type: str, 
                               has_transition: bool,
                               config: Dict) -> Dict:
    """Generate visual properties for keyframe."""
    
    if keyframe_type == 'hook':
        return {
            'contrast': 2.0,          # Maximum contrast
            'saturation': 1.5,        # Boosted colors
            'motion_intensity': 'high',
            'zoom_start': 1.05,       # Start zoomed in
            'zoom_end': 1.0,
            'neon_coverage': 0.15,    # 15% neon accents
            'subtitle_scale': 1.2,    # 20% larger text
        }
    
    elif keyframe_type == 'completion':
        return {
            'contrast': 1.3,
            'saturation': 1.2,
            'motion_intensity': 'low',
            'zoom_start': 1.0,
            'zoom_end': 1.02,         # Slow zoom
            'neon_coverage': 0.10,
            'subtitle_scale': 1.0,
        }
    
    else:  # transition
        intensity = 'high' if has_transition else 'medium'
        return {
            'contrast': 1.5,
            'saturation': 1.4,
            'motion_intensity': intensity,
            'zoom_start': 1.0,
            'zoom_end': 1.03,
            'neon_coverage': 0.12,
            'subtitle_scale': 1.0,
            'pattern_break': has_transition,
        }
```

#### Step 4: Apply to Video Pipeline

```python
from src.pipeline import VideoPipeline
from src.config import GenerationConfig

def generate_video_with_subtitle_keyframes(subtitle_file: str,
                                          output_path: str,
                                          platform: str = 'youtube_shorts'):
    """
    Complete workflow: subtitles → scenes → keyframes → video.
    
    Args:
        subtitle_file: Path to SRT file
        output_path: Output video path
        platform: Target platform
    """
    # 1. Parse subtitles
    subtitles = parse_srt_file(subtitle_file)
    
    # 2. Identify scenes
    scenes = identify_scenes(subtitles)
    
    # 3. Generate keyframes
    keyframes = generate_keyframes(scenes, platform)
    
    # 4. Setup video pipeline
    total_duration = subtitles[-1]['end_time']
    config = GenerationConfig(
        output_resolution=(1080, 1920),
        fps=30,
        target_duration=int(total_duration) + 1,
    )
    
    pipeline = VideoPipeline(config)
    
    # 5. Add captions at keyframe positions
    captions = [(kf['text'], kf['frame']) for kf in keyframes]
    
    # 6. Generate video with keyframe-driven visuals
    pipeline.run_full_pipeline(output_path, captions)
    
    print(f"✅ Generated video with {len(keyframes)} keyframes")
    print(f"   Scenes: {len(scenes)}")
    print(f"   Duration: {total_duration:.1f}s")
    print(f"   Platform: {platform}")
```

---

## Best Practices

### 1. Subtitle Quality

**Essential Requirements:**
- **Accurate timing**: Sync to audio peaks and pauses  
- **Readable duration**: 2–3s on screen  
- **Sentence structure**: Natural phrasing (40–60 characters)  
- **Character limit**: 40–60 characters per subtitle for mobile readability

**Common Mistakes:**
- ❌ Too fast (< 1.5s per subtitle)
- ❌ Too slow (> 5s per subtitle)
- ❌ Breaking mid-sentence without reason
- ❌ Inconsistent timing between subtitles

### 2. Scene Transitions

**Smooth Transitions:**  
Crossfade for smooth flow (5–8 frames at 30fps).

```python
transition_duration = 5-8 frames  # 0.17-0.27s at 30fps
use_crossfade = True
ease_function = 'ease_in_out'
```

**Hard Cuts (Use Intentionally):**  
For shock reveals, comedy beats, fast action (1–2 frames).

```python
transition_duration = 1-2 frames  # 0.03-0.07s
use_cut = True  # Hard cut
```

### 3. Visual Consistency

**Maintain Throughout:**
- Color palette (3-5 neon colors)
- Motion style (continuous micro-movement)
- Contrast ratio (1:7 minimum)
- Font style and size

**Vary Strategically:**
- Scene-to-scene zoom direction
- Pattern break intensity
- Neon accent colors (rotate through palette)

### 4. Iteration & Testing

**A/B Testing Recommendations:**  
Test density, transition styles, and caption timing.

- Density: 1 keyframe per 2s vs. 4s  
- Transitions: Smooth crossfades vs. hard cuts  
- Timing: Exact sync vs. 200ms anticipation  

**Track Metrics:**
- Hook rate (first 3s retention)  
- Scene-by-scene drop-off  
- Completion rate  
- Rewatch rate  
- Average watch time

### 5. Platform-Specific Tips

**YouTube Shorts:**
- ✅ Clear keyframes at major points
- ✅ Strong progress indication
- ✅ Readable subtitles (many watch muted)
- ✅ Aim for 90%+ completion

**TikTok:**
- ✅ Immediate hook (1s max)
- ✅ Rapid keyframe changes
- ✅ Loop potential
- ✅ Trend-aware visuals

**Instagram Reels:**
- ✅ Aesthetic cohesion
- ✅ Smooth transitions
- ✅ Brand-friendly style
- ✅ Mixed audio context

---

## Example Workflows

### Example 1: Educational Short (15 seconds)

**Subtitle Structure:**
```
1. "Here's a mind-blowing fact" (0-2s) → Hook keyframe
2. "Scientists just discovered" (2-4s) → Transition keyframe
3. "That time doesn't exist" (4-7s) → Emphasis keyframe
4. "The way you think it does" (7-10s) → Transition keyframe
5. "Mind = Blown 🤯" (10-13s) → Completion keyframe
```

**Keyframe Strategy:**
- 5 keyframes total
- 3s intervals
- High contrast on hook
- Flash emphasis on "time doesn't exist"
- CTA on completion

### Example 2: Story Short (30 seconds)

**Subtitle Structure:**
```
1. "This happened to me yesterday" (0-3s) → Hook
2. "I was walking to the store" (3-6s) → Scene 1
3. "When suddenly I saw" (6-9s) → Build-up
4. "The craziest thing ever" (9-12s) → Climax keyframe
5. "You won't believe what it was" (12-15s) → Transition
6. "It was... [reveal]" (15-18s) → Emphasis keyframe
7. "And that's how I learned" (18-21s) → Transition
8. "Never to do that again" (21-24s) → Resolution
9. "Follow for more stories!" (24-27s) → CTA keyframe
```

**Keyframe Strategy:**
- 9 keyframes total
- 3s intervals
- Building intensity through scenes
- Maximum emphasis at reveal
- Clear call-to-action

### Example 3: Comedy Short (12 seconds, TikTok)

**Subtitle Structure:**
```
1. "POV: You're trying to" (0-2s) → Hook
2. "Act normal" (2-4s) → Setup keyframe
3. "When your crush walks by" (4-6s) → Transition
4. "But you're actually" (6-8s) → Build
5. "*awkward noises*" (8-10s) → Punchline keyframe
6. "Story of my life 😅" (10-12s) → Completion/Loop
```

**Keyframe Strategy:**
- 6 keyframes total
- 2s intervals (fast-paced)
- Maximum visual comedy on punchline
- Loop-ready ending

---

## Troubleshooting

### Issue: Disjointed Keyframes

**Solution:**  
Lengthen transitions, add crossfade, align with rhythm.

### Issue: Unreadable Subtitles

**Solution:**  
Increase font (60–80px), add outline/shadow, reduce background clutter.

### Issue: Too Many/Few Keyframes

**Solution:**  
Adjust min/max scene duration (2–4s range).

### Issue: Weak Hook

**Solution:**  
Start with shocking statement, bold text, immediate motion.

---

## Conclusion

Effective keyframe generation requires:  

1. **Segmentation** → subtitles into meaningful scenes  
2. **Timing** → precise alignment with narrative beats  
3. **Visual Impact** → strong design principles for hooks and emphasis  
4. **Platform Fit** → density and style adapted to Shorts, TikTok, Reels  
5. **Testing** → iterate using retention metrics  

Following these practices leads to **engaging, subtitle-driven visual stories** optimized for short-form video virality.

---

**Related Documentation:**
- [RESEARCH.md](RESEARCH.md) — Visual engagement principles  
- [QUICKSTART.md](../QUICKSTART.md) — Getting started guide  
- [README.md](../README.md) — Project overview

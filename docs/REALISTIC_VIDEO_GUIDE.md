# Realistic Video Generation Guide: AI-Driven Scripts with Research-Based Visuals

## Overview

This guide explains how to generate realistic short-form videos that implement the visual principles documented in RESEARCH.md, synchronized with AI-generated scripts. The approach combines multiple movement types, pattern breaks, and platform-specific optimization for YouTube Shorts, TikTok, and Instagram Reels.

## Table of Contents

1. [Video Generation Workflow](#video-generation-workflow)
2. [AI Script Integration](#ai-script-integration)
3. [Movement Types Implementation](#movement-types-implementation)
4. [Realistic Visual Styles](#realistic-visual-styles)
5. [Platform-Specific Examples](#platform-specific-examples)
6. [Implementation Code](#implementation-code)
7. [Production Recommendations](#production-recommendations)

---

## Video Generation Workflow

### Complete Pipeline

```
AI Script Generation
        ↓
Scene Segmentation (from KEYFRAME_GUIDE.md)
        ↓
Visual Style Selection (based on audience/platform)
        ↓
Base Video Generation (SDXL/AnimateDiff or stock footage)
        ↓
Motion Enhancement (multiple movement layers)
        ↓
Visual Style Application (color grading, effects)
        ↓
Pattern Breaks Insertion (timing-based)
        ↓
Overlay Addition (captions, progress bar)
        ↓
Platform-Specific Export
```

### Timing Synchronization

```python
def synchronize_script_to_visuals(script, target_duration, platform):
    """
    Synchronize AI-generated script with visual timing.
    
    Args:
        script: AI-generated text content
        target_duration: Total video duration in seconds
        platform: 'tiktok', 'youtube_shorts', or 'instagram_reels'
    
    Returns:
        Synchronized timing data with movement cues
    """
    # Platform-specific parameters
    platform_config = {
        'tiktok': {
            'optimal_duration': 15,
            'hook_time': 0.5,
            'scene_interval': 2.0,
            'movement_intensity': 'high',
        },
        'youtube_shorts': {
            'optimal_duration': 30,
            'hook_time': 2.0,
            'scene_interval': 4.0,
            'movement_intensity': 'medium',
        },
        'instagram_reels': {
            'optimal_duration': 25,
            'hook_time': 3.0,
            'scene_interval': 3.5,
            'movement_intensity': 'medium',
        }
    }
    
    config = platform_config[platform]
    
    # Parse script into segments
    segments = parse_script_segments(script)
    
    # Distribute timing
    timing_data = []
    current_time = 0
    
    for i, segment in enumerate(segments):
        segment_duration = calculate_segment_duration(
            segment, 
            target_duration, 
            len(segments)
        )
        
        # Determine movement type based on position
        if i == 0:
            movement_type = 'hook'  # Maximum motion for first segment
        elif current_time > target_duration * 0.7:
            movement_type = 'resolution'  # Calming movements
        else:
            movement_type = 'development'  # Active movements
        
        timing_data.append({
            'start': current_time,
            'end': current_time + segment_duration,
            'text': segment,
            'movement_type': movement_type,
            'intensity': config['movement_intensity'],
            'scene_break': i % int(config['scene_interval']) == 0,
        })
        
        current_time += segment_duration
    
    return timing_data
```

---

## AI Script Integration

### Script Generation for Video Types

#### 1. Reddit Story Videos (per RESEARCH.md Section 15)

```python
def generate_reddit_story_script(story_type, target_age_group, duration):
    """
    Generate AI script for Reddit story content.
    
    Args:
        story_type: 'aita', 'relationship', 'workplace', 'family'
        target_age_group: '10-14', '15-18', '19-25'
        duration: Target duration in seconds
    
    Returns:
        Structured script with timing markers
    """
    
    # Age-specific language and themes
    age_profiles = {
        '10-14': {
            'vocabulary': 'simple',
            'themes': ['school', 'family', 'friends'],
            'pacing': 'fast',
            'sentences_per_second': 1.5,
        },
        '15-18': {
            'vocabulary': 'teen',
            'themes': ['relationships', 'drama', 'social'],
            'pacing': 'medium',
            'sentences_per_second': 1.2,
        },
        '19-25': {
            'vocabulary': 'adult',
            'themes': ['work', 'dating', 'independence'],
            'pacing': 'moderate',
            'sentences_per_second': 1.0,
        }
    }
    
    profile = age_profiles[target_age_group]
    
    # Story structure (AITA format)
    if story_type == 'aita':
        script_structure = [
            {
                'section': 'hook',
                'duration': 3,
                'template': "You won't believe what [antagonist] did to me...",
                'movement': 'zoom_in_dramatic',
            },
            {
                'section': 'setup',
                'duration': duration * 0.25,
                'template': "So here's what happened. [context]",
                'movement': 'parallax_drift',
            },
            {
                'section': 'conflict',
                'duration': duration * 0.40,
                'template': "Then [antagonist] [action]. I was shocked!",
                'movement': 'rapid_pattern_breaks',
            },
            {
                'section': 'reaction',
                'duration': duration * 0.20,
                'template': "So I [response]. Everyone thinks [opinion].",
                'movement': 'oscillating_zoom',
            },
            {
                'section': 'question',
                'duration': duration * 0.15,
                'template': "AITA? Let me know in the comments!",
                'movement': 'freeze_emphasis',
            },
        ]
    
    # Generate actual script using AI (placeholder for LLM integration)
    generated_script = []
    
    for section in script_structure:
        # AI prompt would go here
        ai_prompt = f"""
        Generate {section['section']} for a {story_type} story.
        Target age: {target_age_group}
        Duration: {section['duration']} seconds
        Vocabulary: {profile['vocabulary']}
        Theme: {profile['themes'][0]}
        Template: {section['template']}
        """
        
        # Simulated AI response (replace with actual LLM call)
        text = generate_with_llm(ai_prompt, max_tokens=50)
        
        generated_script.append({
            'section': section['section'],
            'text': text,
            'duration': section['duration'],
            'movement': section['movement'],
        })
    
    return generated_script


def generate_with_llm(prompt, max_tokens=50):
    """
    Placeholder for LLM integration.
    Replace with actual API calls to OpenAI, Claude, etc.
    """
    # Example integration:
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[{"role": "user", "content": prompt}],
    #     max_tokens=max_tokens
    # )
    # return response.choices[0].message.content
    
    return "AI-generated content here"
```

#### 2. Educational/Explainer Videos

```python
def generate_educational_script(topic, duration, complexity_level):
    """
    Generate script for educational content.
    
    Args:
        topic: Subject matter
        duration: Target duration
        complexity_level: 'beginner', 'intermediate', 'advanced'
    
    Returns:
        Educational script with visual cues
    """
    
    script_structure = [
        {
            'section': 'hook_question',
            'duration': 2,
            'text_template': "Did you know that [surprising_fact]?",
            'visual_cue': 'question_mark_animation',
            'movement': 'attention_pulse',
        },
        {
            'section': 'introduction',
            'duration': duration * 0.20,
            'text_template': "Let me explain [concept] in [duration] seconds",
            'visual_cue': 'topic_title_card',
            'movement': 'smooth_zoom_in',
        },
        {
            'section': 'explanation_1',
            'duration': duration * 0.25,
            'text_template': "First, [point_1]",
            'visual_cue': 'bullet_point_1',
            'movement': 'parallax_left',
        },
        {
            'section': 'explanation_2',
            'duration': duration * 0.25,
            'text_template': "Second, [point_2]",
            'visual_cue': 'bullet_point_2',
            'movement': 'parallax_right',
        },
        {
            'section': 'conclusion',
            'duration': duration * 0.20,
            'text_template': "So that's why [conclusion]",
            'visual_cue': 'checkmark_animation',
            'movement': 'smooth_zoom_out',
        },
        {
            'section': 'cta',
            'duration': duration * 0.10,
            'text_template': "Follow for more [topic] content!",
            'visual_cue': 'follow_button_highlight',
            'movement': 'gentle_bob',
        },
    ]
    
    return script_structure
```

---

## Movement Types Implementation

### 1. Constant Micro-Movement (Base Layer)

Always active, implements research principle of "no element static >300ms".

```python
def apply_constant_micromovement(frame, time_offset, config):
    """
    Apply constant micro-movement to prevent habituation.
    Based on RESEARCH.md Section 1.
    
    Args:
        frame: Input frame (H, W, C)
        time_offset: Current time in seconds
        config: Movement configuration
    
    Returns:
        Frame with micro-movements applied
    """
    h, w = frame.shape[:2]
    
    # Layer 1: Background drift (0.2-0.5px/frame)
    drift_x = np.sin(time_offset * 0.5) * 0.3
    drift_y = np.cos(time_offset * 0.7) * 0.3
    
    # Layer 2: Subtle rotation (±0.5-2° per second)
    angle = np.sin(time_offset * 2 * np.pi) * 1.5
    
    # Layer 3: Micro zoom (100-101.5%)
    scale = 1.0 + (np.sin(time_offset * np.pi) * 0.015)
    
    # Apply transformations
    center = (w // 2, h // 2)
    
    # Combined transformation matrix
    M_drift = np.float32([[1, 0, drift_x], [0, 1, drift_y]])
    M_rotate = cv2.getRotationMatrix2D(center, angle, scale)
    
    # Apply drift first
    frame = cv2.warpAffine(frame, M_drift, (w, h), 
                          borderMode=cv2.BORDER_REFLECT)
    
    # Then rotation and zoom
    frame = cv2.warpAffine(frame, M_rotate, (w, h),
                          borderMode=cv2.BORDER_REFLECT)
    
    return frame
```

### 2. Parallax Movement (Multiple Layers)

Creates depth perception through differential motion speeds.

```python
def apply_parallax_layers(background, midground, foreground, 
                         time_offset, intensity='medium'):
    """
    Apply parallax effect with multiple movement speeds.
    Based on RESEARCH.md Section 6C (Depth and Layering).
    
    Args:
        background: Background layer
        midground: Middle layer  
        foreground: Foreground layer
        time_offset: Current time
        intensity: 'low', 'medium', 'high'
    
    Returns:
        Composite frame with parallax
    """
    
    intensity_multiplier = {
        'low': 0.5,
        'medium': 1.0,
        'high': 1.5,
    }[intensity]
    
    # Different speeds for depth
    bg_speed = 0.2 * intensity_multiplier
    mid_speed = 1.0 * intensity_multiplier
    fg_speed = 1.5 * intensity_multiplier
    
    # Calculate offsets
    bg_offset = np.sin(time_offset * bg_speed) * 10
    mid_offset = np.sin(time_offset * mid_speed) * 20
    fg_offset = np.sin(time_offset * fg_speed) * 30
    
    # Apply offsets to each layer
    bg_shifted = shift_layer(background, bg_offset, 0)
    mid_shifted = shift_layer(midground, mid_offset, 0)
    fg_shifted = shift_layer(foreground, fg_offset, 0)
    
    # Composite with proper alpha blending
    result = bg_shifted
    result = alpha_blend(result, mid_shifted, alpha=0.8)
    result = alpha_blend(result, fg_shifted, alpha=0.9)
    
    return result


def shift_layer(layer, offset_x, offset_y):
    """Shift layer with wrap-around."""
    h, w = layer.shape[:2]
    M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
    return cv2.warpAffine(layer, M, (w, h), borderMode=cv2.BORDER_WRAP)
```

### 3. Pattern Breaks (Attention Maintenance)

Implements research principle of "pattern break every 1.2-2.5s".

```python
def apply_pattern_break(frame, break_type, intensity, progress):
    """
    Apply pattern break for attention maintenance.
    Based on RESEARCH.md Section 3.
    
    Args:
        frame: Input frame
        break_type: 'minor' or 'major'
        intensity: 0.0 to 1.0
        progress: 0.0 to 1.0 (position within break)
    
    Returns:
        Frame with pattern break applied
    """
    h, w = frame.shape[:2]
    
    if break_type == 'minor':
        # Small rotation twirl (±45°, 5 frames)
        angle = 45 * intensity * np.sin(progress * np.pi)
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        frame = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        
    elif break_type == 'major':
        # Zoom pop (1.2x scale, 3 frames)
        scale = 1.0 + (0.2 * intensity * np.sin(progress * np.pi))
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, 0, scale)
        frame = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    
    return frame
```

### 4. Oscillating Movements

Creates rhythmic engagement without being repetitive.

```python
def apply_oscillating_movement(frame, time_offset, movement_type):
    """
    Apply oscillating movements for rhythm.
    
    Args:
        frame: Input frame
        time_offset: Current time
        movement_type: 'bounce', 'sway', 'pulse', 'orbit'
    
    Returns:
        Frame with oscillation applied
    """
    h, w = frame.shape[:2]
    
    if movement_type == 'bounce':
        # Vertical bounce (0.5-2Hz)
        frequency = 1.5  # Hz
        amplitude = 5  # pixels
        offset_y = amplitude * np.sin(2 * np.pi * frequency * time_offset)
        M = np.float32([[1, 0, 0], [0, 1, offset_y]])
        frame = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        
    elif movement_type == 'sway':
        # Horizontal sway
        frequency = 0.8
        amplitude = 8
        offset_x = amplitude * np.sin(2 * np.pi * frequency * time_offset)
        M = np.float32([[1, 0, offset_x], [0, 1, 0]])
        frame = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        
    elif movement_type == 'pulse':
        # Scale pulse (100-105%)
        frequency = 1.0
        scale = 1.0 + (0.05 * np.sin(2 * np.pi * frequency * time_offset))
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, 0, scale)
        frame = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        
    elif movement_type == 'orbit':
        # Circular camera motion
        radius = 10
        angle = 2 * np.pi * time_offset * 0.5
        offset_x = radius * np.cos(angle)
        offset_y = radius * np.sin(angle)
        M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
        frame = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    
    return frame
```

### 5. Directional Transitions

For scene changes and narrative flow.

```python
def apply_directional_transition(frame_a, frame_b, progress, direction):
    """
    Apply directional transition between frames.
    Based on RESEARCH.md Section 6B (Scene Transitions).
    
    Args:
        frame_a: Starting frame
        frame_b: Ending frame
        progress: 0.0 to 1.0
        direction: 'left', 'right', 'up', 'down', 'zoom_in', 'zoom_out'
    
    Returns:
        Blended transition frame
    """
    h, w = frame_a.shape[:2]
    
    if direction in ['left', 'right', 'up', 'down']:
        # Swipe/slide transition
        if direction == 'left':
            offset = (-w * progress, 0)
        elif direction == 'right':
            offset = (w * progress, 0)
        elif direction == 'up':
            offset = (0, -h * progress)
        elif direction == 'down':
            offset = (0, h * progress)
        
        # Shift frame_a out
        M_a = np.float32([[1, 0, offset[0]], [0, 1, offset[1]]])
        shifted_a = cv2.warpAffine(frame_a, M_a, (w, h))
        
        # Shift frame_b in (from opposite side)
        if direction == 'left':
            offset_b = (w * (1 - progress), 0)
        elif direction == 'right':
            offset_b = (-w * (1 - progress), 0)
        elif direction == 'up':
            offset_b = (0, h * (1 - progress))
        elif direction == 'down':
            offset_b = (0, -h * (1 - progress))
        
        M_b = np.float32([[1, 0, offset_b[0]], [0, 1, offset_b[1]]])
        shifted_b = cv2.warpAffine(frame_b, M_b, (w, h))
        
        # Composite
        result = cv2.addWeighted(shifted_a, 1 - progress, shifted_b, progress, 0)
        
    elif direction == 'zoom_in':
        # Zoom into frame_b
        scale_a = 1.0 + (0.2 * progress)  # Zoom out frame_a
        scale_b = 0.8 + (0.2 * progress)  # Zoom in frame_b
        
        center = (w // 2, h // 2)
        M_a = cv2.getRotationMatrix2D(center, 0, scale_a)
        M_b = cv2.getRotationMatrix2D(center, 0, scale_b)
        
        scaled_a = cv2.warpAffine(frame_a, M_a, (w, h))
        scaled_b = cv2.warpAffine(frame_b, M_b, (w, h))
        
        # Crossfade
        result = cv2.addWeighted(scaled_a, 1 - progress, scaled_b, progress, 0)
        
    elif direction == 'zoom_out':
        # Zoom out to reveal frame_b
        scale_a = 1.0 - (0.2 * progress)  # Zoom in frame_a
        scale_b = 1.2 - (0.2 * progress)  # Zoom out frame_b
        
        center = (w // 2, h // 2)
        M_a = cv2.getRotationMatrix2D(center, 0, scale_a)
        M_b = cv2.getRotationMatrix2D(center, 0, scale_b)
        
        scaled_a = cv2.warpAffine(frame_a, M_a, (w, h))
        scaled_b = cv2.warpAffine(frame_b, M_b, (w, h))
        
        result = cv2.addWeighted(scaled_a, 1 - progress, scaled_b, progress, 0)
    
    return result
```

---

## Realistic Visual Styles

### 1. Stock Footage Integration

Using real footage as base with movement enhancements.

```python
def load_and_prepare_footage(footage_path, target_resolution, duration, fps):
    """
    Load stock footage and prepare for movement application.
    
    Args:
        footage_path: Path to video file
        target_resolution: (width, height) tuple
        duration: Target duration in seconds
        fps: Target frames per second
    
    Returns:
        Prepared frames list
    """
    cap = cv2.VideoCapture(footage_path)
    
    # Read and resize frames
    frames = []
    target_frame_count = int(duration * fps)
    
    while len(frames) < target_frame_count:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop
            continue
        
        # Resize to target resolution
        frame = cv2.resize(frame, target_resolution)
        frames.append(frame)
    
    cap.release()
    return frames


# Recommended stock footage types by content
FOOTAGE_RECOMMENDATIONS = {
    'reddit_story_10_14': [
        'minecraft_parkour.mp4',
        'roblox_gameplay.mp4',
        'slime_videos.mp4',
    ],
    'reddit_story_15_18': [
        'subway_surfers.mp4',
        'gta_gameplay.mp4',
        'satisfying_soap_cutting.mp4',
    ],
    'reddit_story_19_25': [
        'coffee_making_aesthetic.mp4',
        'cooking_overhead.mp4',
        'city_driving_pov.mp4',
    ],
    'educational': [
        'abstract_patterns.mp4',
        'geometric_animations.mp4',
        'particle_effects.mp4',
    ],
}
```

### 2. AI-Generated Backgrounds

Using Stable Diffusion XL or similar for custom backgrounds.

```python
def generate_ai_background(prompt, style, duration, fps, resolution):
    """
    Generate AI background using SDXL + AnimateDiff.
    
    Args:
        prompt: Text description
        style: Visual style preset
        duration: Duration in seconds
        fps: Frames per second
        resolution: (width, height)
    
    Returns:
        Generated frame sequence
    """
    
    # Style presets based on research
    style_presets = {
        'neon_abstract': {
            'prompt_suffix': ', neon colors, high contrast, dark background, glowing edges',
            'negative_prompt': 'realistic, photographic, dull colors',
            'cfg_scale': 7.0,
        },
        'satisfying_geometric': {
            'prompt_suffix': ', satisfying patterns, geometric shapes, smooth motion',
            'negative_prompt': 'chaotic, random, messy',
            'cfg_scale': 8.0,
        },
        'aesthetic_minimalist': {
            'prompt_suffix': ', minimalist aesthetic, soft colors, elegant, clean',
            'negative_prompt': 'cluttered, busy, overwhelming',
            'cfg_scale': 7.5,
        },
    }
    
    preset = style_presets.get(style, style_presets['neon_abstract'])
    full_prompt = prompt + preset['prompt_suffix']
    
    # Generate base frames (placeholder for actual SDXL integration)
    # In production, use:
    # from diffusers import StableDiffusionXLPipeline, AnimateDiffPipeline
    # pipe = StableDiffusionXLPipeline.from_pretrained(...)
    # frames = pipe(prompt=full_prompt, num_frames=duration*fps, ...)
    
    frames = []
    target_frames = int(duration * fps)
    
    for i in range(target_frames):
        # Placeholder: generate procedural frame
        frame = generate_procedural_frame(i, target_frames, resolution)
        frames.append(frame)
    
    return frames
```

### 3. Hybrid Approach (Recommended)

Combining stock footage with AI-generated elements and effects.

```python
def create_hybrid_visual(base_footage, ai_overlay, effects_config):
    """
    Combine stock footage with AI-generated overlays and effects.
    Best for professional-looking results.
    
    Args:
        base_footage: Stock video frames
        ai_overlay: AI-generated visual elements
        effects_config: Effects configuration dict
    
    Returns:
        Hybrid frame sequence
    """
    
    hybrid_frames = []
    
    for i, (base_frame, overlay_frame) in enumerate(zip(base_footage, ai_overlay)):
        # 1. Start with base footage
        result = base_frame.copy()
        
        # 2. Apply color grading (from RESEARCH.md Section 6A)
        result = apply_color_grading(result, effects_config['grading_preset'])
        
        # 3. Add AI overlay with blending
        if effects_config['use_overlay']:
            result = blend_overlay(result, overlay_frame, 
                                  mode=effects_config['blend_mode'],
                                  opacity=effects_config['overlay_opacity'])
        
        # 4. Add neon accents (from RESEARCH.md Section 2)
        result = add_neon_accents(result, 
                                 coverage=effects_config['neon_coverage'],
                                 colors=effects_config['neon_colors'])
        
        # 5. Apply edge glow
        result = apply_edge_glow(result, 
                                intensity=effects_config['glow_intensity'])
        
        hybrid_frames.append(result)
    
    return hybrid_frames
```

---

## Platform-Specific Examples

### Example 1: TikTok Reddit Story (15-18 age group)

```python
def generate_tiktok_reddit_story():
    """
    Generate TikTok-optimized Reddit story video.
    Target: Female 15-18, US
    Background: Subway Surfers gameplay
    """
    
    # Configuration
    config = {
        'platform': 'tiktok',
        'duration': 30,  # 15-45s optimal
        'resolution': (1080, 1920),
        'fps': 30,
        'target_completion': 0.75,  # 70-85% target
    }
    
    # 1. Generate AI script
    script = generate_reddit_story_script(
        story_type='relationship_drama',
        target_age='15-18',
        duration=config['duration']
    )
    
    # 2. Load background footage
    background = load_and_prepare_footage(
        'assets/subway_surfers.mp4',
        config['resolution'],
        config['duration'],
        config['fps']
    )
    
    # 3. Apply movements
    enhanced_frames = []
    for frame_idx, frame in enumerate(background):
        time = frame_idx / config['fps']
        
        # Constant micro-movement (always active)
        frame = apply_constant_micromovement(frame, time, {})
        
        # Pattern breaks every 1.5s
        if frame_idx % 45 == 0:  # 1.5s at 30fps
            break_progress = (frame_idx % 15) / 15  # Break lasts 0.5s
            frame = apply_pattern_break(frame, 'minor', 0.8, break_progress)
        
        enhanced_frames.append(frame)
    
    # 4. Apply color grading
    styled_frames = []
    for frame in enhanced_frames:
        # High saturation, neon aesthetic
        frame = apply_color_grading(frame, preset='tiktok_vibrant')
        frame = add_neon_accents(frame, coverage=0.12, 
                                colors=['cyan', 'magenta', 'yellow'])
        styled_frames.append(frame)
    
    # 5. Add overlays
    final_frames = []
    for frame_idx, frame in enumerate(styled_frames):
        # Add captions (word-by-word reveal)
        frame = add_tiktok_captions(frame, script, frame_idx, config['fps'])
        
        # No progress bar for TikTok (UI interference)
        
        final_frames.append(frame)
    
    # 6. Export
    export_video(final_frames, 'output/tiktok_reddit_story.mp4', 
                config['fps'], audio=None)
    
    return final_frames


def add_tiktok_captions(frame, script, frame_idx, fps):
    """Add TikTok-style captions with word-by-word reveal."""
    h, w = frame.shape[:2]
    
    # Caption configuration (from RESEARCH.md Section 15)
    caption_config = {
        'font': cv2.FONT_HERSHEY_DUPLEX,
        'size': 70,  # 60-80px for mobile
        'color': (255, 255, 255),  # White
        'outline_color': (0, 0, 0),  # Black
        'outline_thickness': 4,
        'position': 'upper_third',  # Top 33% of frame
    }
    
    # Find current word based on timing
    current_time = frame_idx / fps
    current_word = get_word_at_time(script, current_time)
    
    if current_word:
        # Position text
        y_pos = int(h * 0.25)  # Upper third
        
        # Draw outline
        (text_w, text_h), _ = cv2.getTextSize(
            current_word, 
            caption_config['font'],
            caption_config['size'] / 30.0,
            caption_config['outline_thickness']
        )
        
        x_pos = (w - text_w) // 2
        
        # Draw shadow/outline (multiple passes)
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx != 0 or dy != 0:
                    cv2.putText(frame, current_word,
                              (x_pos + dx, y_pos + dy),
                              caption_config['font'],
                              caption_config['size'] / 30.0,
                              caption_config['outline_color'],
                              caption_config['outline_thickness'] + 1,
                              cv2.LINE_AA)
        
        # Draw main text
        cv2.putText(frame, current_word,
                   (x_pos, y_pos),
                   caption_config['font'],
                   caption_config['size'] / 30.0,
                   caption_config['color'],
                   caption_config['outline_thickness'],
                   cv2.LINE_AA)
    
    return frame
```

### Example 2: YouTube Shorts Educational Video

```python
def generate_youtube_educational():
    """
    Generate YouTube Shorts educational video.
    Duration: 45s
    Style: Professional with clear visuals
    """
    
    config = {
        'platform': 'youtube_shorts',
        'duration': 45,
        'resolution': (1080, 1920),
        'fps': 30,
        'target_completion': 0.65,  # 60-75% target
    }
    
    # 1. Generate script
    script = generate_educational_script(
        topic='psychology_facts',
        duration=config['duration'],
        complexity='beginner'
    )
    
    # 2. Generate AI background (geometric patterns)
    background = generate_ai_background(
        prompt='abstract geometric patterns, educational aesthetic',
        style='satisfying_geometric',
        duration=config['duration'],
        fps=config['fps'],
        resolution=config['resolution']
    )
    
    # 3. Apply medium-intensity movements
    enhanced_frames = []
    for frame_idx, frame in enumerate(background):
        time = frame_idx / config['fps']
        
        # Slower, more professional movements
        frame = apply_constant_micromovement(frame, time, {})
        frame = apply_oscillating_movement(frame, time, 'pulse')
        
        # Pattern breaks every 3s
        if frame_idx % 90 == 0:
            break_progress = (frame_idx % 20) / 20
            frame = apply_pattern_break(frame, 'major', 0.6, break_progress)
        
        enhanced_frames.append(frame)
    
    # 4. Professional color grading
    styled_frames = []
    for frame in enhanced_frames:
        frame = apply_color_grading(frame, preset='youtube_professional')
        frame = add_neon_accents(frame, coverage=0.10,
                                colors=['blue', 'cyan'])
        styled_frames.append(frame)
    
    # 5. Add overlays
    final_frames = []
    for frame_idx, frame in enumerate(styled_frames):
        # Sentence-by-sentence captions
        frame = add_youtube_captions(frame, script, frame_idx, config['fps'])
        
        # Progress bar (important for YouTube)
        progress = frame_idx / len(styled_frames)
        frame = add_progress_bar(frame, progress, style='youtube')
        
        final_frames.append(frame)
    
    # 6. Export
    export_video(final_frames, 'output/youtube_educational.mp4',
                config['fps'], audio=None)
    
    return final_frames
```

### Example 3: Instagram Reels Aesthetic Video

```python
def generate_instagram_aesthetic():
    """
    Generate Instagram Reels aesthetic video.
    Duration: 25s
    Style: Cohesive, brand-friendly
    """
    
    config = {
        'platform': 'instagram_reels',
        'duration': 25,
        'resolution': (1080, 1920),
        'fps': 30,
        'target_save_rate': 0.08,  # 5-10% target
    }
    
    # 1. Load aesthetic stock footage
    background = load_and_prepare_footage(
        'assets/coffee_making_aesthetic.mp4',
        config['resolution'],
        config['duration'],
        config['fps']
    )
    
    # 2. Generate complementary AI overlay
    overlay = generate_ai_background(
        prompt='soft gradients, pastel colors, elegant patterns',
        style='aesthetic_minimalist',
        duration=config['duration'],
        fps=config['fps'],
        resolution=config['resolution']
    )
    
    # 3. Create hybrid visual
    hybrid = create_hybrid_visual(
        background,
        overlay,
        effects_config={
            'grading_preset': 'instagram_aesthetic',
            'use_overlay': True,
            'blend_mode': 'soft_light',
            'overlay_opacity': 0.3,
            'neon_coverage': 0.08,
            'neon_colors': ['rose_gold', 'lavender', 'mint'],
            'glow_intensity': 0.4,
        }
    )
    
    # 4. Apply smooth movements
    enhanced_frames = []
    for frame_idx, frame in enumerate(hybrid):
        time = frame_idx / config['fps']
        
        # Gentle, professional movements
        frame = apply_constant_micromovement(frame, time, {})
        frame = apply_oscillating_movement(frame, time, 'sway')
        
        # Subtle pattern breaks every 4s
        if frame_idx % 120 == 0:
            break_progress = (frame_idx % 25) / 25
            frame = apply_pattern_break(frame, 'minor', 0.4, break_progress)
        
        enhanced_frames.append(frame)
    
    # 5. Add clean overlays
    final_frames = []
    for frame_idx, frame in enumerate(enhanced_frames):
        # Clean, readable captions
        frame = add_instagram_captions(frame, script, frame_idx, config['fps'])
        
        # Minimal progress indicator
        progress = frame_idx / len(enhanced_frames)
        frame = add_progress_bar(frame, progress, style='instagram_minimal')
        
        final_frames.append(frame)
    
    # 6. Export
    export_video(final_frames, 'output/instagram_aesthetic.mp4',
                config['fps'], audio=None)
    
    return final_frames
```

---

## Implementation Code

### Complete Video Generator with AI Script

```python
class RealisticVideoGenerator:
    """
    Complete video generator implementing research principles.
    Supports AI script integration and multiple movement types.
    """
    
    def __init__(self, config):
        self.config = config
        self.movements = []
        self.timing_data = []
    
    def generate_from_script(self, script, platform, video_type):
        """
        Generate complete video from AI script.
        
        Args:
            script: AI-generated script text or structure
            platform: 'tiktok', 'youtube_shorts', 'instagram_reels'
            video_type: 'reddit_story', 'educational', 'aesthetic', etc.
        
        Returns:
            Generated video frames
        """
        
        # 1. Synchronize script to visuals
        self.timing_data = synchronize_script_to_visuals(
            script,
            self.config.duration,
            platform
        )
        
        # 2. Select visual style
        visual_style = self.select_visual_style(platform, video_type)
        
        # 3. Generate or load base visuals
        if visual_style['source'] == 'stock':
            base_frames = self.load_stock_footage(visual_style['footage_path'])
        elif visual_style['source'] == 'ai':
            base_frames = self.generate_ai_background(visual_style['prompt'])
        elif visual_style['source'] == 'hybrid':
            base_frames = self.create_hybrid_visual(visual_style)
        
        # 4. Apply movements based on timing data
        enhanced_frames = self.apply_all_movements(base_frames, self.timing_data)
        
        # 5. Apply visual styling
        styled_frames = self.apply_visual_style(enhanced_frames, platform)
        
        # 6. Add overlays
        final_frames = self.add_overlays(styled_frames, self.timing_data, platform)
        
        return final_frames
    
    def apply_all_movements(self, frames, timing_data):
        """Apply all movement types based on timing."""
        enhanced = []
        
        for frame_idx, frame in enumerate(frames):
            time = frame_idx / self.config.fps
            
            # Find current segment
            current_segment = self.get_segment_at_time(timing_data, time)
            
            # Always apply base micro-movement
            frame = apply_constant_micromovement(frame, time, {})
            
            # Apply segment-specific movement
            if current_segment:
                movement_type = current_segment['movement_type']
                intensity = current_segment['intensity']
                
                if movement_type == 'hook':
                    frame = self.apply_hook_movement(frame, time, intensity)
                elif movement_type == 'development':
                    frame = self.apply_development_movement(frame, time, intensity)
                elif movement_type == 'resolution':
                    frame = self.apply_resolution_movement(frame, time, intensity)
            
            # Apply pattern breaks
            if self.should_apply_pattern_break(frame_idx):
                frame = self.apply_timed_pattern_break(frame, frame_idx)
            
            enhanced.append(frame)
        
        return enhanced
    
    def apply_hook_movement(self, frame, time, intensity):
        """Maximum motion for hook (first 3s)."""
        # Combine multiple movement types
        frame = apply_oscillating_movement(frame, time, 'pulse')
        frame = apply_oscillating_movement(frame, time * 1.5, 'bounce')
        
        # Dramatic zoom
        h, w = frame.shape[:2]
        scale = 1.05 - (0.05 * min(time / 3, 1.0))  # Zoom from 1.05 to 1.0
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, 0, scale)
        frame = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        
        return frame
    
    def apply_development_movement(self, frame, time, intensity):
        """Active but sustainable movement for main content."""
        # Parallax-style movement
        frame = apply_oscillating_movement(frame, time, 'sway')
        frame = apply_oscillating_movement(frame, time * 0.7, 'orbit')
        return frame
    
    def apply_resolution_movement(self, frame, time, intensity):
        """Calming movement for conclusion."""
        # Gentle, slowing movements
        frame = apply_oscillating_movement(frame, time * 0.5, 'pulse')
        return frame
```

---

## Production Recommendations

### 1. Asset Preparation

**Stock Footage Sources:**
- Pexels.com (free, high quality)
- Pixabay.com (free)
- Envato Elements (paid, premium)
- Specialized: GameplayFootage.com for gaming content

**AI Generation:**
- Stable Diffusion XL for static images
- AnimateDiff for video animation
- Runway ML for AI video generation
- Pika Labs for realistic motion

### 2. Performance Optimization

```python
# Optimize for real-time generation
def optimize_generation_pipeline():
    """
    Optimization strategies for production.
    """
    
    strategies = {
        'caching': 'Cache base frames and movement patterns',
        'gpu_acceleration': 'Use GPU for video processing (CuPy, GPU-accelerated OpenCV)',
        'parallel_processing': 'Process frames in parallel batches',
        'lazy_loading': 'Load footage segments on-demand',
        'compression': 'Use efficient codecs (H.264, H.265)',
    }
    
    return strategies
```

### 3. Quality Assurance Checklist

- [ ] Constant motion verified (no static elements >300ms)
- [ ] Pattern breaks occur every 1.2-2.5s
- [ ] High contrast maintained (minimum 1:7 ratio)
- [ ] Neon accents cover 8-15% of frame
- [ ] Captions readable on mobile (60-80px)
- [ ] Platform-specific duration met
- [ ] Target completion rate metrics
- [ ] Audio synchronization perfect (±50ms)
- [ ] Export settings correct for platform

### 4. A/B Testing Framework

```python
def setup_ab_test(base_config, test_variables):
    """
    Setup A/B test variations.
    
    Args:
        base_config: Base configuration
        test_variables: Dict of variables to test
    
    Returns:
        List of configuration variations
    """
    
    variations = []
    
    for var_name, var_values in test_variables.items():
        for value in var_values:
            config = base_config.copy()
            config[var_name] = value
            config['variant_id'] = f"{var_name}_{value}"
            variations.append(config)
    
    return variations


# Example test
test_config = setup_ab_test(
    base_config={'duration': 30, 'platform': 'tiktok'},
    test_variables={
        'movement_intensity': ['low', 'medium', 'high'],
        'pattern_break_frequency': [1.0, 1.5, 2.0, 2.5],
        'neon_coverage': [0.08, 0.12, 0.15],
    }
)
```

### 5. Metrics Tracking

Track these metrics for each video variant:
- Hook rate (3s retention)
- Average watch time
- Completion rate
- Engagement rate (likes + comments + shares) / views
- Share rate
- Save rate (Instagram specific)
- Click-through rate (for series)

---

## Conclusion

This guide provides a complete framework for generating realistic videos that implement the visual principles documented in RESEARCH.md. By combining AI-generated scripts with multiple movement types, platform-specific optimization, and proper timing synchronization, you can create engaging short-form content that maximizes retention and virality.

**Key Takeaways:**
1. Always maintain constant micro-movement (no static elements)
2. Layer multiple movement types for depth and interest
3. Synchronize pattern breaks with script timing
4. Optimize for specific platform and audience
5. Test variations to find optimal parameters
6. Track metrics to validate research principles

**Next Steps:**
1. Set up development environment with required libraries
2. Gather or generate base visual assets
3. Implement AI script generation pipeline
4. Build movement application system
5. Create platform-specific export pipeline
6. Launch A/B tests to validate approach
7. Iterate based on performance data

For questions or contributions, refer to the main RESEARCH.md and KEYFRAME_GUIDE.md documentation.

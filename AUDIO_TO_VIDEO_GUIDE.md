# Audio Story to Video Generation Guide

## Overview

This guide explains how to transform audio stories (narration, podcasts, Reddit stories read aloud) into visually engaging short-form videos by applying research-based movement rules and generating appropriate visuals through AI prompts. The approach synchronizes visual keyframes with audio content to maximize retention and virality.

## Table of Contents

1. [Audio-Visual Synchronization Workflow](#audio-visual-synchronization-workflow)
2. [AI Prompt Generation for Audio Content](#ai-prompt-generation-for-audio-content)
3. [Keyframe Generation from Audio](#keyframe-generation-from-audio)
4. [Movement Rules Application](#movement-rules-application)
5. [Platform-Specific Audio-to-Video Examples](#platform-specific-audio-to-video-examples)
6. [Complete Implementation](#complete-implementation)
7. [Prompt Engineering Best Practices](#prompt-engineering-best-practices)

---

## Audio-Visual Synchronization Workflow

### Complete Pipeline

```
Audio Story Input
        ↓
Audio Analysis (Speech-to-Text + Emotion Detection)
        ↓
Scene Segmentation (Based on narration beats)
        ↓
AI Prompt Generation (Context-aware visual descriptions)
        ↓
Keyframe Generation (SDXL/Midjourney prompts)
        ↓
Visual Generation (AI image/video generation)
        ↓
Movement Application (All research-based rules)
        ↓
Audio-Visual Synchronization
        ↓
Platform-Specific Export
```

### Audio Analysis

```python
def analyze_audio_story(audio_path):
    """
    Analyze audio to extract timing, content, and emotion.
    
    Args:
        audio_path: Path to audio file (MP3, WAV, M4A)
    
    Returns:
        Structured audio analysis with timing and emotion data
    """
    import whisper
    import librosa
    import numpy as np
    
    # 1. Transcribe audio with timestamps
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=True)
    
    # 2. Analyze audio features for emotion/intensity
    y, sr = librosa.load(audio_path)
    
    # Energy/intensity over time
    rms = librosa.feature.rms(y=y)[0]
    
    # Tempo/rhythm
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    
    # Spectral features (for mood detection)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    
    # 3. Combine transcription with audio features
    segments = []
    for segment in result['segments']:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        
        # Calculate average intensity for this segment
        start_frame = int(start_time * sr / 512)
        end_frame = int(end_time * sr / 512)
        avg_intensity = np.mean(rms[start_frame:end_frame]) if end_frame > start_frame else 0
        avg_spectral = np.mean(spectral_centroid[start_frame:end_frame]) if end_frame > start_frame else 0
        
        # Detect emotion from text and audio features
        emotion = detect_emotion(text, avg_intensity, avg_spectral)
        
        segments.append({
            'start': start_time,
            'end': end_time,
            'duration': end_time - start_time,
            'text': text.strip(),
            'intensity': float(avg_intensity),
            'spectral_brightness': float(avg_spectral),
            'emotion': emotion,
            'words': segment.get('words', []),
        })
    
    return {
        'segments': segments,
        'total_duration': result['segments'][-1]['end'] if result['segments'] else 0,
        'tempo': float(tempo),
        'language': result.get('language', 'en'),
    }


def detect_emotion(text, intensity, spectral):
    """
    Detect emotion from text content and audio features.
    
    Args:
        text: Transcribed text
        intensity: Audio intensity/energy
        spectral: Spectral brightness
    
    Returns:
        Emotion label
    """
    # Keyword-based emotion detection
    text_lower = text.lower()
    
    # High intensity emotions
    if intensity > 0.15:
        if any(word in text_lower for word in ['angry', 'furious', 'rage', 'yelled', 'screamed']):
            return 'anger'
        elif any(word in text_lower for word in ['shocked', 'surprised', 'wow', 'omg', 'unbelievable']):
            return 'shock'
        elif any(word in text_lower for word in ['excited', 'amazing', 'love', 'happy', 'thrilled']):
            return 'excitement'
    
    # Medium intensity
    elif intensity > 0.08:
        if any(word in text_lower for word in ['concerned', 'worried', 'afraid', 'nervous']):
            return 'concern'
        elif any(word in text_lower for word in ['sad', 'depressed', 'cry', 'tears', 'heartbroken']):
            return 'sadness'
    
    # Low intensity (calm/neutral)
    else:
        if any(word in text_lower for word in ['but', 'then', 'so', 'because']):
            return 'explanation'
        else:
            return 'neutral'
    
    return 'neutral'
```

---

## AI Prompt Generation for Audio Content

### Context-Aware Prompt Builder

```python
def generate_visual_prompt_for_audio_segment(segment, story_context, visual_style):
    """
    Generate AI image generation prompt from audio segment.
    
    Args:
        segment: Audio segment dict with text, emotion, timing
        story_context: Overall story context (type, setting, characters)
        visual_style: Visual style preference
    
    Returns:
        AI generation prompt optimized for SDXL/Midjourney
    """
    
    # Base prompt components
    emotion_to_visual = {
        'anger': 'intense red lighting, dramatic shadows, aggressive angles, high contrast',
        'shock': 'bright flash effect, wide-angle distortion, vibrant colors, dynamic composition',
        'excitement': 'energetic motion blur, vivid colors, upward movement, radiant glow',
        'concern': 'cool blue tones, soft shadows, gentle vignette, contemplative mood',
        'sadness': 'desaturated colors, heavy shadows, downward angles, melancholic atmosphere',
        'explanation': 'balanced composition, clear lighting, organized elements, professional look',
        'neutral': 'clean aesthetic, balanced colors, steady composition, modern style',
    }
    
    # Story type to visual style mapping
    story_type_styles = {
        'reddit_story': {
            'base': 'modern digital aesthetic, clean composition',
            'background': 'abstract geometric patterns, satisfying visuals, minimalist design',
        },
        'horror': {
            'base': 'dark moody atmosphere, cinematic lighting, dramatic shadows',
            'background': 'ominous textures, mysterious fog, eerie glow effects',
        },
        'romance': {
            'base': 'soft romantic lighting, warm color palette, dreamy atmosphere',
            'background': 'bokeh lights, gentle gradients, pastel colors, elegant design',
        },
        'mystery': {
            'base': 'noir atmosphere, selective lighting, high contrast, suspenseful mood',
            'background': 'shadowy textures, mysterious silhouettes, cool tones',
        },
        'comedy': {
            'base': 'bright vibrant colors, playful composition, energetic feel',
            'background': 'fun patterns, cheerful gradients, pop art style, dynamic shapes',
        },
        'educational': {
            'base': 'professional clean aesthetic, clear visual hierarchy',
            'background': 'geometric patterns, educational infographic style, organized layout',
        },
    }
    
    # Get style components
    style_config = story_type_styles.get(story_context.get('type', 'reddit_story'))
    emotion_style = emotion_to_visual.get(segment['emotion'], emotion_to_visual['neutral'])
    
    # Build prompt based on content
    content_keywords = extract_visual_keywords(segment['text'])
    
    # Construct prompt
    prompt_parts = []
    
    # 1. Main subject/scene (if extractable from text)
    if content_keywords:
        prompt_parts.append(', '.join(content_keywords))
    else:
        prompt_parts.append(style_config['background'])
    
    # 2. Emotion-based visual treatment
    prompt_parts.append(emotion_style)
    
    # 3. Base style
    prompt_parts.append(style_config['base'])
    
    # 4. Visual style modifiers
    if visual_style == 'neon':
        prompt_parts.append('neon colors, glowing edges, cyberpunk aesthetic, high saturation')
    elif visual_style == 'aesthetic':
        prompt_parts.append('soft pastel colors, elegant gradients, Instagram aesthetic, minimalist')
    elif visual_style == 'dramatic':
        prompt_parts.append('cinematic lighting, dramatic composition, film grain, high quality')
    elif visual_style == 'satisfying':
        prompt_parts.append('satisfying patterns, mesmerizing motion, perfect symmetry, ASMR visuals')
    
    # 5. Technical quality
    prompt_parts.append('4k, high quality, sharp details, professional')
    
    # 6. Platform optimization
    prompt_parts.append('vertical 9:16 aspect ratio, mobile optimized')
    
    # Combine into final prompt
    prompt = ', '.join(prompt_parts)
    
    # Negative prompt (what to avoid)
    negative_prompt = 'blurry, low quality, distorted, text, watermark, signature, cropped, out of frame, worst quality, low resolution, jpeg artifacts, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, ugly'
    
    return {
        'prompt': prompt,
        'negative_prompt': negative_prompt,
        'emotion': segment['emotion'],
        'intensity': segment['intensity'],
        'duration': segment['duration'],
    }


def extract_visual_keywords(text):
    """
    Extract visual elements from text for prompt generation.
    
    Args:
        text: Transcribed text segment
    
    Returns:
        List of visual keywords
    """
    # Common visual nouns and descriptions
    visual_keywords = []
    
    text_lower = text.lower()
    
    # Settings/locations
    locations = ['beach', 'ocean', 'mountain', 'forest', 'city', 'room', 'house', 
                'office', 'car', 'restaurant', 'park', 'street', 'store', 'mall',
                'school', 'classroom', 'gym', 'hospital', 'airport', 'train']
    
    # Objects
    objects = ['phone', 'computer', 'car', 'door', 'window', 'table', 'chair',
              'coffee', 'food', 'book', 'bag', 'keys', 'wallet', 'clothes']
    
    # People/characters
    characters = ['person', 'man', 'woman', 'child', 'friend', 'family', 'mother',
                 'father', 'sister', 'brother', 'boyfriend', 'girlfriend', 'boss',
                 'coworker', 'neighbor', 'stranger']
    
    # Actions (convert to visual states)
    action_to_visual = {
        'running': 'motion blur, dynamic movement',
        'sitting': 'calm composition, static scene',
        'talking': 'conversation bubble, animated speech',
        'crying': 'tears, emotional atmosphere',
        'laughing': 'joyful expression, bright colors',
        'working': 'focused scene, professional setting',
        'driving': 'road perspective, motion lines',
        'walking': 'pedestrian view, steady movement',
    }
    
    # Extract matches
    for location in locations:
        if location in text_lower:
            visual_keywords.append(location)
    
    for obj in objects:
        if obj in text_lower:
            visual_keywords.append(obj)
    
    for character in characters:
        if character in text_lower:
            visual_keywords.append(character + ' silhouette')  # Use silhouettes for privacy
    
    for action, visual in action_to_visual.items():
        if action in text_lower:
            visual_keywords.append(visual)
    
    return visual_keywords[:3]  # Limit to top 3 to avoid prompt overload
```

### Platform-Specific Prompt Optimization

```python
def optimize_prompt_for_platform(base_prompt, platform, target_audience):
    """
    Optimize AI generation prompt for specific platform algorithms.
    
    Args:
        base_prompt: Base generation prompt
        platform: 'tiktok', 'youtube_shorts', 'instagram_reels'
        target_audience: Age/demographic info
    
    Returns:
        Platform-optimized prompt
    """
    
    platform_modifiers = {
        'tiktok': {
            'style': 'trending TikTok aesthetic, viral style, Gen-Z appealing',
            'colors': 'highly saturated, vibrant neon accents, eye-catching',
            'composition': 'centered subject, clear focal point, vertical format',
            'energy': 'high energy, dynamic, fast-paced feel',
        },
        'youtube_shorts': {
            'style': 'YouTube quality, professional look, polished aesthetic',
            'colors': 'bold contrasts, complementary color scheme, rich colors',
            'composition': 'rule of thirds, balanced, visually pleasing',
            'energy': 'engaging but not overwhelming, steady progression',
        },
        'instagram_reels': {
            'style': 'Instagram aesthetic, cohesive theme, brand-friendly',
            'colors': 'curated color palette, harmonious tones, aesthetic appeal',
            'composition': 'aesthetic composition, negative space, elegant',
            'energy': 'smooth and polished, aspirational quality',
        },
    }
    
    # Age-specific modifiers
    age_modifiers = {
        '10-14': 'fun and playful, Minecraft/Roblox inspired, kid-friendly, bright colors',
        '15-18': 'trendy and cool, Subway Surfers/TikTok style, teen aesthetic',
        '19-25': 'sophisticated but relatable, modern minimalist, young adult appeal',
        '25+': 'professional and polished, mature aesthetic, refined quality',
    }
    
    platform_config = platform_modifiers.get(platform, platform_modifiers['tiktok'])
    
    # Build optimized prompt
    optimized_parts = [base_prompt]
    optimized_parts.append(platform_config['style'])
    optimized_parts.append(platform_config['colors'])
    optimized_parts.append(platform_config['composition'])
    optimized_parts.append(platform_config['energy'])
    
    # Add age-specific modifier if provided
    if target_audience:
        age_group = target_audience.get('age_group')
        if age_group and age_group in age_modifiers:
            optimized_parts.append(age_modifiers[age_group])
    
    return ', '.join(optimized_parts)
```

---

## Keyframe Generation from Audio

### Audio-Driven Keyframe Timing

```python
def generate_keyframes_from_audio(audio_analysis, platform, visual_style):
    """
    Generate keyframe specifications from audio analysis.
    
    Args:
        audio_analysis: Output from analyze_audio_story()
        platform: Target platform
        visual_style: Visual aesthetic choice
    
    Returns:
        List of keyframe specifications with prompts
    """
    
    segments = audio_analysis['segments']
    total_duration = audio_analysis['total_duration']
    
    # Platform-specific keyframe intervals
    platform_config = {
        'tiktok': {
            'min_interval': 1.5,  # Change visual every 1.5-2s
            'max_interval': 2.5,
            'hook_duration': 0.5,  # Critical first 0.5s
        },
        'youtube_shorts': {
            'min_interval': 3.0,  # Change visual every 3-4s
            'max_interval': 5.0,
            'hook_duration': 2.0,  # First 2s important
        },
        'instagram_reels': {
            'min_interval': 2.5,  # Change visual every 2.5-4s
            'max_interval': 4.0,
            'hook_duration': 3.0,  # First 3s important
        },
    }
    
    config = platform_config.get(platform, platform_config['tiktok'])
    
    keyframes = []
    current_time = 0
    keyframe_index = 0
    
    # Story context from first segments
    story_context = {
        'type': 'reddit_story',  # Default, can be detected from content
        'setting': None,
        'mood': segments[0]['emotion'] if segments else 'neutral',
    }
    
    while current_time < total_duration:
        # Find segment at current time
        current_segment = None
        for seg in segments:
            if seg['start'] <= current_time < seg['end']:
                current_segment = seg
                break
        
        if not current_segment and segments:
            # If between segments, use closest
            current_segment = min(segments, key=lambda s: abs(s['start'] - current_time))
        
        if not current_segment:
            break
        
        # Generate prompt for this keyframe
        prompt_data = generate_visual_prompt_for_audio_segment(
            current_segment,
            story_context,
            visual_style
        )
        
        # Optimize for platform
        optimized_prompt = optimize_prompt_for_platform(
            prompt_data['prompt'],
            platform,
            {'age_group': '15-18'}  # Default, should be parameterized
        )
        
        # Determine keyframe type
        if keyframe_index == 0:
            keyframe_type = 'hook'
            duration = config['hook_duration']
        elif current_time > total_duration * 0.85:
            keyframe_type = 'conclusion'
            duration = min(config['max_interval'], total_duration - current_time)
        else:
            keyframe_type = 'development'
            # Vary duration based on emotion intensity
            intensity_factor = current_segment['intensity'] / 0.2  # Normalize
            duration = config['min_interval'] + (config['max_interval'] - config['min_interval']) * (1 - min(intensity_factor, 1))
        
        keyframes.append({
            'index': keyframe_index,
            'start_time': current_time,
            'duration': duration,
            'type': keyframe_type,
            'prompt': optimized_prompt,
            'negative_prompt': prompt_data['negative_prompt'],
            'emotion': current_segment['emotion'],
            'text_content': current_segment['text'],
            'movement_intensity': 'high' if current_segment['intensity'] > 0.15 else 'medium',
        })
        
        current_time += duration
        keyframe_index += 1
    
    return keyframes
```

### Prompt Examples by Emotion

```python
EMOTION_PROMPT_TEMPLATES = {
    'hook': {
        'anger': 'explosive visual impact, intense red and orange flames, dramatic dark shadows, aggressive geometric shapes, high contrast lighting, powerful energy, cinematic storm clouds, electric atmosphere',
        'shock': 'sudden bright flash effect, lightning bolt strike, shattered glass effect, explosive particles, wide-angle distortion, vibrant electric colors, dramatic reveal, jaw-dropping moment',
        'excitement': 'radiant golden light burst, confetti explosion, upward spiraling energy, vivid rainbow colors, celebration atmosphere, dynamic motion trails, sparkling effects, euphoric glow',
        'mystery': 'dark silhouette reveal, fog rolling in, mysterious shadows, blue moonlight, noir atmosphere, dramatic spotlight, enigmatic composition, suspenseful lighting',
    },
    'development': {
        'anger': 'stormy red atmosphere, turbulent energy, aggressive patterns, intense heat waves, dramatic tension, dark crimson tones, powerful movement, conflict visualization',
        'concern': 'cool blue gradient, gentle shadows, contemplative atmosphere, soft focus areas, worried mood, subtle vignette, thoughtful composition, uncertain lighting',
        'sadness': 'rain-streaked window, desaturated colors, heavy downward flow, melancholic blue tones, gentle tears effect, soft crying mood, emotional weight, somber atmosphere',
        'explanation': 'clear organized infographic style, balanced composition, professional diagrams, logical flow visualization, structured layout, educational aesthetic, clean modern design',
        'neutral': 'smooth gradient background, balanced colors, steady composition, modern minimalist aesthetic, professional quality, clean lines, organized elements',
    },
    'conclusion': {
        'resolution': 'sunrise golden hour, hope emerging, warm uplifting colors, peaceful resolution, harmonious composition, satisfied mood, complete circle, gentle closure',
        'cliffhanger': 'sudden darkness, cut to black, suspended moment, unresolved tension, mysterious fade, question mark energy, dramatic pause, suspenseful ending',
        'satisfaction': 'complete rainbow arc, perfect symmetry achieved, satisfying conclusion, harmonious colors, balanced resolution, peaceful ending, fulfilled atmosphere, content mood',
    },
}


def get_prompt_template(keyframe_type, emotion):
    """Get pre-designed prompt template for emotion and keyframe type."""
    if keyframe_type == 'hook':
        return EMOTION_PROMPT_TEMPLATES['hook'].get(emotion, EMOTION_PROMPT_TEMPLATES['hook']['mystery'])
    elif keyframe_type == 'conclusion':
        return EMOTION_PROMPT_TEMPLATES['conclusion'].get('resolution')
    else:  # development
        return EMOTION_PROMPT_TEMPLATES['development'].get(emotion, EMOTION_PROMPT_TEMPLATES['development']['neutral'])
```

---

## Movement Rules Application

### Apply Research-Based Movement to Audio-Generated Visuals

```python
def apply_movements_to_audio_video(keyframes, audio_analysis, platform):
    """
    Apply all movement rules from research to audio-generated visuals.
    
    Args:
        keyframes: Generated keyframes with prompts
        audio_analysis: Audio timing and emotion data
        platform: Target platform
    
    Returns:
        Movement configuration for each keyframe
    """
    
    movement_configs = []
    
    for i, keyframe in enumerate(keyframes):
        # Base movement (ALWAYS ACTIVE - Research principle #1)
        base_movement = {
            'type': 'constant_micromovement',
            'drift_speed': 0.3,  # px/frame
            'rotation_range': 1.5,  # degrees
            'zoom_range': 0.015,  # 100-101.5%
        }
        
        # Emotion-driven movement intensity
        emotion = keyframe['emotion']
        intensity = keyframe.get('movement_intensity', 'medium')
        
        emotion_movement = {
            'anger': {
                'type': 'oscillating',
                'pattern': 'bounce',
                'frequency': 2.0,  # Hz
                'amplitude': 8,  # pixels
                'additional': 'shake',
            },
            'shock': {
                'type': 'pattern_break',
                'break_type': 'major',
                'frequency': 0.5,  # Every 2 seconds
                'intensity': 0.9,
            },
            'excitement': {
                'type': 'oscillating',
                'pattern': 'pulse',
                'frequency': 1.5,
                'amplitude': 0.08,  # 8% scale
                'additional': 'zoom_in',
            },
            'concern': {
                'type': 'oscillating',
                'pattern': 'sway',
                'frequency': 0.5,
                'amplitude': 5,
                'additional': 'slow_drift',
            },
            'sadness': {
                'type': 'directional',
                'direction': 'down',
                'speed': 2,  # px/frame
                'additional': 'slow_fade',
            },
            'neutral': {
                'type': 'oscillating',
                'pattern': 'orbit',
                'frequency': 0.8,
                'amplitude': 10,
            },
        }
        
        secondary_movement = emotion_movement.get(emotion, emotion_movement['neutral'])
        
        # Pattern breaks (Research principle #3)
        # Frequency based on platform and intensity
        pattern_break_config = {
            'enabled': True,
            'min_interval': 1.2,  # seconds
            'max_interval': 2.5,  # seconds
            'break_types': ['minor', 'major'] if intensity == 'high' else ['minor'],
        }
        
        # Parallax layers for depth (if using layered visuals)
        parallax_config = {
            'enabled': True,
            'layers': [
                {'speed': 0.2, 'name': 'background'},
                {'speed': 1.0, 'name': 'midground'},
                {'speed': 1.5, 'name': 'foreground'},
            ],
        }
        
        # Transition to next keyframe
        if i < len(keyframes) - 1:
            next_emotion = keyframes[i + 1]['emotion']
            
            # Determine transition type based on emotion change
            if emotion != next_emotion:
                if next_emotion in ['shock', 'anger']:
                    transition = 'zoom_in'
                elif next_emotion in ['sadness', 'concern']:
                    transition = 'fade'
                else:
                    transition = 'slide_left'
            else:
                transition = 'crossfade'
        else:
            transition = 'fade_out'
        
        movement_configs.append({
            'keyframe_index': i,
            'start_time': keyframe['start_time'],
            'duration': keyframe['duration'],
            'base_movement': base_movement,
            'emotion_movement': secondary_movement,
            'pattern_breaks': pattern_break_config,
            'parallax': parallax_config,
            'transition_out': transition,
            'intensity': intensity,
        })
    
    return movement_configs
```

---

## Platform-Specific Audio-to-Video Examples

### Example 1: TikTok Reddit Story from Audio

```python
def generate_tiktok_reddit_story_from_audio(audio_path, output_path):
    """
    Complete pipeline: Audio Reddit story → TikTok video
    
    Args:
        audio_path: Path to audio narration (MP3/WAV)
        output_path: Output video path
    
    Returns:
        Generated video info
    """
    
    # 1. Analyze audio
    print("📊 Analyzing audio...")
    audio_analysis = analyze_audio_story(audio_path)
    
    print(f"   Duration: {audio_analysis['total_duration']:.1f}s")
    print(f"   Segments: {len(audio_analysis['segments'])}")
    
    # 2. Generate keyframes with prompts
    print("\n🎨 Generating keyframes...")
    keyframes = generate_keyframes_from_audio(
        audio_analysis,
        platform='tiktok',
        visual_style='neon'  # TikTok-optimized
    )
    
    print(f"   Keyframes: {len(keyframes)}")
    
    # 3. Generate visuals from prompts
    print("\n🖼️  Generating visuals from AI prompts...")
    generated_visuals = []
    
    for kf in keyframes:
        print(f"   [{kf['index']}] {kf['type']}: {kf['emotion']}")
        print(f"       Prompt: {kf['prompt'][:80]}...")
        
        # Generate image/video from prompt
        # Using SDXL or similar
        visual = generate_from_prompt(
            prompt=kf['prompt'],
            negative_prompt=kf['negative_prompt'],
            width=1080,
            height=1920,
            duration=kf['duration'],
        )
        
        generated_visuals.append(visual)
    
    # 4. Apply movements
    print("\n🎬 Applying movement rules...")
    movement_configs = apply_movements_to_audio_video(
        keyframes,
        audio_analysis,
        platform='tiktok'
    )
    
    enhanced_visuals = []
    for visual, movement_config in zip(generated_visuals, movement_configs):
        enhanced = apply_all_movements(visual, movement_config)
        enhanced_visuals.append(enhanced)
    
    # 5. Add captions synchronized with audio
    print("\n💬 Adding captions...")
    captioned_visuals = []
    
    for i, visual in enumerate(enhanced_visuals):
        keyframe = keyframes[i]
        
        # Get words for this time range
        words_in_range = []
        for segment in audio_analysis['segments']:
            if segment['start'] >= keyframe['start_time'] and segment['start'] < keyframe['start_time'] + keyframe['duration']:
                words_in_range.extend(segment.get('words', []))
        
        # Add word-by-word captions (TikTok style)
        captioned = add_tiktok_word_captions(
            visual,
            words_in_range,
            keyframe['start_time'],
            fps=30
        )
        
        captioned_visuals.append(captioned)
    
    # 6. Composite with audio
    print("\n🔊 Syncing with audio...")
    final_video = composite_video_with_audio(
        captioned_visuals,
        audio_path,
        keyframes
    )
    
    # 7. Export
    print(f"\n💾 Exporting to {output_path}...")
    export_video(
        final_video,
        output_path,
        fps=30,
        codec='h264',
        bitrate='8M',
        audio_codec='aac',
    )
    
    print("\n✅ Complete!")
    
    return {
        'output_path': output_path,
        'duration': audio_analysis['total_duration'],
        'keyframes': len(keyframes),
        'platform': 'tiktok',
    }


def add_tiktok_word_captions(visual_frames, words, start_time, fps):
    """
    Add TikTok-style word-by-word captions.
    
    Args:
        visual_frames: List of video frames
        words: Word timing data from Whisper
        start_time: Keyframe start time
        fps: Frames per second
    
    Returns:
        Frames with captions added
    """
    import cv2
    import numpy as np
    
    captioned_frames = []
    
    for frame_idx, frame in enumerate(visual_frames):
        frame_time = start_time + (frame_idx / fps)
        
        # Find word at this time
        current_word = None
        for word_data in words:
            if word_data['start'] <= frame_time < word_data['end']:
                current_word = word_data['word'].strip()
                break
        
        if current_word:
            # Add caption with TikTok styling
            h, w = frame.shape[:2]
            
            # Position in upper third
            y_pos = int(h * 0.25)
            
            # Font configuration
            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 2.5
            thickness = 6
            
            # Get text size
            (text_w, text_h), _ = cv2.getTextSize(current_word, font, font_scale, thickness)
            x_pos = (w - text_w) // 2
            
            # Draw black outline (multiple passes)
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    if dx != 0 or dy != 0:
                        cv2.putText(frame, current_word,
                                  (x_pos + dx, y_pos + dy),
                                  font, font_scale,
                                  (0, 0, 0),  # Black
                                  thickness + 2,
                                  cv2.LINE_AA)
            
            # Draw white text
            cv2.putText(frame, current_word,
                       (x_pos, y_pos),
                       font, font_scale,
                       (255, 255, 255),  # White
                       thickness,
                       cv2.LINE_AA)
        
        captioned_frames.append(frame)
    
    return captioned_frames
```

### Example 2: YouTube Shorts Educational Audio

```python
def generate_youtube_educational_from_audio(audio_path, topic, output_path):
    """
    Generate YouTube Shorts educational video from audio explanation.
    
    Args:
        audio_path: Audio explanation file
        topic: Educational topic for better prompts
        output_path: Output video path
    
    Returns:
        Video generation info
    """
    
    # 1. Analyze audio
    audio_analysis = analyze_audio_story(audio_path)
    
    # 2. Generate keyframes with educational styling
    keyframes = generate_keyframes_from_audio(
        audio_analysis,
        platform='youtube_shorts',
        visual_style='aesthetic'  # Professional, clean
    )
    
    # Enhance prompts with topic context
    for kf in keyframes:
        # Add topic-specific elements
        topic_elements = {
            'science': 'scientific diagrams, molecule structures, laboratory aesthetic',
            'history': 'historical documents, vintage textures, timeline visualization',
            'psychology': 'brain imagery, thought bubbles, mind map visualization',
            'technology': 'circuit boards, digital interfaces, futuristic design',
            'finance': 'charts, graphs, professional business aesthetic',
        }
        
        if topic.lower() in topic_elements:
            kf['prompt'] = f"{kf['prompt']}, {topic_elements[topic.lower()]}"
    
    # 3. Generate visuals
    generated_visuals = []
    for kf in keyframes:
        visual = generate_from_prompt(
            prompt=kf['prompt'],
            negative_prompt=kf['negative_prompt'],
            width=1080,
            height=1920,
            duration=kf['duration'],
            style='professional'
        )
        generated_visuals.append(visual)
    
    # 4. Apply moderate movements (professional style)
    movement_configs = apply_movements_to_audio_video(
        keyframes,
        audio_analysis,
        platform='youtube_shorts'
    )
    
    # Override for more subtle movements
    for config in movement_configs:
        config['base_movement']['drift_speed'] = 0.2  # Slower
        config['base_movement']['rotation_range'] = 1.0  # Less rotation
        config['pattern_breaks']['min_interval'] = 3.0  # Less frequent
    
    enhanced_visuals = []
    for visual, config in zip(generated_visuals, movement_configs):
        enhanced = apply_all_movements(visual, config)
        enhanced_visuals.append(enhanced)
    
    # 5. Add sentence-level captions (not word-by-word)
    captioned_visuals = []
    for i, visual in enumerate(enhanced_visuals):
        keyframe = keyframes[i]
        
        # Get sentence for this segment
        sentence = keyframe['text_content']
        
        captioned = add_youtube_sentence_caption(
            visual,
            sentence,
            keyframe['duration'],
            fps=30
        )
        
        captioned_visuals.append(captioned)
    
    # 6. Add progress bar (important for YouTube)
    with_progress = []
    total_duration = audio_analysis['total_duration']
    
    for i, visual in enumerate(captioned_visuals):
        kf_start = keyframes[i]['start_time']
        kf_duration = keyframes[i]['duration']
        
        frames_with_progress = []
        for frame_idx, frame in enumerate(visual):
            current_time = kf_start + (frame_idx / 30)
            progress = current_time / total_duration
            
            frame_with_bar = add_progress_bar(frame, progress, style='youtube')
            frames_with_progress.append(frame_with_bar)
        
        with_progress.append(frames_with_progress)
    
    # 7. Composite and export
    final_video = composite_video_with_audio(with_progress, audio_path, keyframes)
    export_video(final_video, output_path, fps=30)
    
    return {
        'output_path': output_path,
        'duration': total_duration,
        'keyframes': len(keyframes),
        'platform': 'youtube_shorts',
    }
```

---

## Complete Implementation

### Full Audio-to-Video Generator Class

```python
class AudioToVideoGenerator:
    """
    Complete audio story to video generator applying all research principles.
    """
    
    def __init__(self, platform='tiktok', visual_style='neon', target_audience=None):
        """
        Initialize generator.
        
        Args:
            platform: 'tiktok', 'youtube_shorts', 'instagram_reels'
            visual_style: 'neon', 'aesthetic', 'dramatic', 'satisfying'
            target_audience: Dict with demographic info
        """
        self.platform = platform
        self.visual_style = visual_style
        self.target_audience = target_audience or {'age_group': '15-18'}
        
        # Load AI models (placeholder)
        self.whisper_model = None  # Load Whisper
        self.image_generator = None  # Load SDXL/Midjourney API
        
    def generate(self, audio_path, output_path, story_type='reddit_story'):
        """
        Main generation pipeline.
        
        Args:
            audio_path: Input audio file
            output_path: Output video path
            story_type: Type of story for prompt optimization
        
        Returns:
            Generation results
        """
        
        # Step 1: Analyze audio
        print("🎤 Step 1/7: Analyzing audio...")
        audio_analysis = analyze_audio_story(audio_path)
        
        # Step 2: Generate keyframes
        print("🎨 Step 2/7: Generating keyframes...")
        keyframes = generate_keyframes_from_audio(
            audio_analysis,
            self.platform,
            self.visual_style
        )
        
        # Add story type context
        story_context = {'type': story_type}
        
        # Step 3: Generate AI visuals
        print("🖼️  Step 3/7: Generating visuals from prompts...")
        visuals = self._generate_visuals(keyframes, story_context)
        
        # Step 4: Apply movements
        print("🎬 Step 4/7: Applying movement rules...")
        enhanced_visuals = self._apply_movements(visuals, keyframes, audio_analysis)
        
        # Step 5: Add captions
        print("💬 Step 5/7: Adding captions...")
        captioned_visuals = self._add_captions(enhanced_visuals, keyframes, audio_analysis)
        
        # Step 6: Add overlays
        print("📊 Step 6/7: Adding overlays...")
        final_visuals = self._add_overlays(captioned_visuals, keyframes, audio_analysis)
        
        # Step 7: Composite and export
        print("💾 Step 7/7: Compositing and exporting...")
        self._export(final_visuals, audio_path, output_path, keyframes)
        
        print("✅ Generation complete!")
        
        return {
            'success': True,
            'output_path': output_path,
            'duration': audio_analysis['total_duration'],
            'keyframes': len(keyframes),
            'platform': self.platform,
        }
    
    def _generate_visuals(self, keyframes, story_context):
        """Generate visuals from keyframe prompts."""
        visuals = []
        
        for kf in keyframes:
            # Call AI image/video generation API
            # Placeholder for actual implementation
            visual = self._call_ai_generator(
                prompt=kf['prompt'],
                negative_prompt=kf['negative_prompt'],
                duration=kf['duration'],
            )
            visuals.append(visual)
        
        return visuals
    
    def _call_ai_generator(self, prompt, negative_prompt, duration):
        """
        Call AI generation service (SDXL, Midjourney, etc.)
        
        This is a placeholder - integrate with actual API
        """
        # Example: Using Stability AI SDXL
        # import stability_sdk
        # image = stability_sdk.generate(prompt=prompt, ...)
        
        # For now, return placeholder
        import numpy as np
        
        # Generate placeholder frames
        fps = 30
        num_frames = int(duration * fps)
        frames = []
        
        for i in range(num_frames):
            # Placeholder: colored frame
            frame = np.random.randint(0, 255, (1920, 1080, 3), dtype=np.uint8)
            frames.append(frame)
        
        return frames
    
    def _apply_movements(self, visuals, keyframes, audio_analysis):
        """Apply all research-based movements."""
        movement_configs = apply_movements_to_audio_video(
            keyframes,
            audio_analysis,
            self.platform
        )
        
        enhanced = []
        for visual, config in zip(visuals, movement_configs):
            enhanced_visual = apply_all_movements(visual, config)
            enhanced.append(enhanced_visual)
        
        return enhanced
    
    def _add_captions(self, visuals, keyframes, audio_analysis):
        """Add platform-appropriate captions."""
        if self.platform == 'tiktok':
            # Word-by-word
            return [add_tiktok_word_captions(v, kf, audio_analysis) 
                    for v, kf in zip(visuals, keyframes)]
        elif self.platform == 'youtube_shorts':
            # Sentence-level
            return [add_youtube_sentence_caption(v, kf) 
                    for v, kf in zip(visuals, keyframes)]
        else:  # instagram_reels
            # Clean minimal
            return [add_instagram_caption(v, kf) 
                    for v, kf in zip(visuals, keyframes)]
    
    def _add_overlays(self, visuals, keyframes, audio_analysis):
        """Add progress bars and other overlays."""
        if self.platform == 'youtube_shorts':
            # Add progress bar
            total_duration = audio_analysis['total_duration']
            return [add_progress_bar_to_visual(v, kf, total_duration) 
                    for v, kf in zip(visuals, keyframes)]
        else:
            # No progress bar for TikTok/Instagram
            return visuals
    
    def _export(self, visuals, audio_path, output_path, keyframes):
        """Composite with audio and export."""
        final_video = composite_video_with_audio(visuals, audio_path, keyframes)
        export_video(final_video, output_path, fps=30)
```

---

## Prompt Engineering Best Practices

### General Principles

1. **Be Specific But Not Overloaded**
   - Good: "neon cyberpunk aesthetic, glowing blue and purple, dark background, high contrast"
   - Bad: "neon cyberpunk aesthetic with glowing blue purple pink orange yellow green and dark black background with high contrast and shadows and highlights..."

2. **Use Weight/Priority Markers**
   - For Stable Diffusion: `(keyword:1.2)` increases weight
   - For Midjourney: `keyword::2` doubles weight

3. **Start with Subject, Then Style**
   - Structure: [Subject] + [Action/Pose] + [Environment] + [Lighting] + [Style] + [Quality]
   - Example: "abstract geometric patterns, slowly rotating, dark void background, neon accent lighting, cyberpunk aesthetic, 4k quality"

4. **Platform-Specific Optimization**
   - TikTok: Emphasize "trending", "viral", "eye-catching"
   - YouTube: Emphasize "professional", "polished", "high quality"
   - Instagram: Emphasize "aesthetic", "cohesive", "curated"

### Emotion-Specific Prompt Templates

```python
COMPREHENSIVE_PROMPT_LIBRARY = {
    'backgrounds': {
        'neon_abstract': 'abstract neon geometric patterns, glowing edges, dark background, vibrant cyan and magenta, high saturation, modern digital art, 4k',
        'satisfying_geometric': 'perfectly symmetrical geometric shapes, satisfying patterns, smooth gradients, pastel colors, ASMR visual aesthetic, mesmerizing',
        'dramatic_cinematic': 'cinematic atmosphere, dramatic lighting, film grain, moody colors, high contrast, professional cinematography, epic scale',
        'minimalist_aesthetic': 'clean minimalist design, soft pastel gradients, negative space, elegant composition, Instagram aesthetic, refined',
        'gaming_overlay': 'video game HUD elements, digital interface, gaming aesthetic, pixelated effects, retro gaming style, vibrant UI colors',
    },
    
    'moods': {
        'energetic': 'high energy, dynamic motion, vivid colors, explosive effects, fast-paced, adrenaline rush, intense atmosphere',
        'calm': 'peaceful atmosphere, gentle flow, soft colors, tranquil mood, relaxing vibes, serene composition, meditative',
        'mysterious': 'enigmatic atmosphere, shadows and fog, blue moonlight, noir style, suspenseful mood, dramatic mystery',
        'joyful': 'bright cheerful colors, celebration atmosphere, happy vibes, uplifting mood, positive energy, sunshine feeling',
        'dramatic': 'intense drama, high stakes atmosphere, powerful emotions, cinematic tension, epic scale, grand composition',
    },
    
    'technical': {
        'quality': '4k, uhd, high quality, sharp focus, detailed, professional photography, crisp details, crystal clear',
        'vertical_mobile': 'vertical 9:16 aspect ratio, mobile optimized, portrait orientation, smartphone friendly',
        'avoid': 'blurry, low quality, distorted, ugly, deformed, bad anatomy, worst quality, low resolution, jpeg artifacts',
    },
}


def build_comprehensive_prompt(subject, mood, background_style, platform):
    """
    Build comprehensive prompt from library.
    
    Args:
        subject: Main subject/content
        mood: Emotional mood
        background_style: Visual style
        platform: Target platform
    
    Returns:
        Complete prompt string
    """
    
    parts = []
    
    # 1. Subject
    if subject:
        parts.append(subject)
    
    # 2. Background style
    if background_style in COMPREHENSIVE_PROMPT_LIBRARY['backgrounds']:
        parts.append(COMPREHENSIVE_PROMPT_LIBRARY['backgrounds'][background_style])
    
    # 3. Mood
    if mood in COMPREHENSIVE_PROMPT_LIBRARY['moods']:
        parts.append(COMPREHENSIVE_PROMPT_LIBRARY['moods'][mood])
    
    # 4. Platform optimization
    platform_additions = {
        'tiktok': 'trending TikTok style, viral aesthetic, Gen-Z appealing, highly engaging',
        'youtube_shorts': 'YouTube quality, professional look, polished production, watch-worthy',
        'instagram_reels': 'Instagram aesthetic, feed-worthy, influencer style, shareable',
    }
    if platform in platform_additions:
        parts.append(platform_additions[platform])
    
    # 5. Technical quality
    parts.append(COMPREHENSIVE_PROMPT_LIBRARY['technical']['quality'])
    parts.append(COMPREHENSIVE_PROMPT_LIBRARY['technical']['vertical_mobile'])
    
    prompt = ', '.join(parts)
    negative_prompt = COMPREHENSIVE_PROMPT_LIBRARY['technical']['avoid']
    
    return prompt, negative_prompt
```

### Testing and Iteration

```python
def test_prompt_variations(base_prompt, variations_count=5):
    """
    Generate variations of a prompt for A/B testing.
    
    Args:
        base_prompt: Starting prompt
        variations_count: Number of variations
    
    Returns:
        List of prompt variations
    """
    
    variations = [base_prompt]  # Original
    
    # Variation strategies
    strategies = [
        ('color_shift', 'Replace color words with alternatives'),
        ('intensity_shift', 'Adjust intensity descriptors'),
        ('style_shift', 'Try different art styles'),
        ('composition_shift', 'Modify composition descriptions'),
    ]
    
    for i in range(variations_count - 1):
        strategy = strategies[i % len(strategies)]
        
        if strategy[0] == 'color_shift':
            # Replace colors
            color_map = {
                'blue': 'cyan',
                'red': 'crimson',
                'purple': 'violet',
                'green': 'emerald',
            }
            variant = base_prompt
            for old, new in color_map.items():
                variant = variant.replace(old, new)
        
        elif strategy[0] == 'intensity_shift':
            # Adjust intensity
            intensity_map = {
                'high': 'extreme',
                'bright': 'radiant',
                'dark': 'deep',
                'soft': 'gentle',
            }
            variant = base_prompt
            for old, new in intensity_map.items():
                variant = variant.replace(old, new)
        
        elif strategy[0] == 'style_shift':
            # Add style variation
            style_additions = [
                ', digital art style',
                ', photorealistic render',
                ', illustrated aesthetic',
                ', 3D rendered',
            ]
            variant = base_prompt + style_additions[i % len(style_additions)]
        
        elif strategy[0] == 'composition_shift':
            # Modify composition
            composition_additions = [
                ', centered composition',
                ', dynamic angle',
                ', symmetrical layout',
                ', rule of thirds',
            ]
            variant = base_prompt + composition_additions[i % len(composition_additions)]
        
        variations.append(variant)
    
    return variations
```

---

## Usage Examples

### Complete Example: Reddit Story Audio to TikTok Video

```python
# Initialize generator
generator = AudioToVideoGenerator(
    platform='tiktok',
    visual_style='neon',
    target_audience={'age_group': '15-18', 'gender': 'female', 'region': 'US'}
)

# Generate video from audio story
result = generator.generate(
    audio_path='story_narration.mp3',
    output_path='output/tiktok_story.mp4',
    story_type='reddit_story'
)

print(f"✅ Generated {result['keyframes']} keyframes")
print(f"📹 Video: {result['output_path']}")
print(f"⏱️  Duration: {result['duration']:.1f}s")
```

### Quick Prompt Generation

```python
# Generate prompt for specific audio segment
segment = {
    'text': "And then she said the most shocking thing I've ever heard",
    'emotion': 'shock',
    'intensity': 0.18,
    'start': 5.2,
    'end': 8.1,
}

prompt_data = generate_visual_prompt_for_audio_segment(
    segment,
    story_context={'type': 'reddit_story'},
    visual_style='neon'
)

print("Prompt:", prompt_data['prompt'])
print("Emotion:", prompt_data['emotion'])
```

### Batch Processing

```python
# Process multiple audio files
audio_files = [
    'story1.mp3',
    'story2.mp3',
    'story3.mp3',
]

for i, audio_file in enumerate(audio_files):
    print(f"\n📁 Processing {i+1}/{len(audio_files)}: {audio_file}")
    
    generator.generate(
        audio_path=f'input/{audio_file}',
        output_path=f'output/story_{i+1}.mp4',
        story_type='reddit_story'
    )

print("\n✅ All videos generated!")
```

---

## Conclusion

This guide provides a complete framework for transforming audio stories into visually engaging videos by:

1. **Analyzing audio content** for timing, emotion, and intensity
2. **Generating context-aware AI prompts** that match the narrative
3. **Creating keyframes** synchronized with audio beats and emotional arcs
4. **Applying all research-based movement rules** for maximum engagement
5. **Optimizing for specific platforms** (TikTok, YouTube Shorts, Instagram Reels)

**Key Takeaways:**
- Audio emotion drives visual style and movement intensity
- AI prompts should be emotion-specific and platform-optimized
- Keyframe timing follows audio beats and platform best practices
- All movement rules from RESEARCH.md apply (constant motion, pattern breaks, parallax)
- Captions must sync precisely with audio (word-level for TikTok, sentence-level for YouTube)

**Next Steps:**
1. Set up audio analysis pipeline (Whisper + librosa)
2. Integrate AI image/video generation API (SDXL, Midjourney, Runway)
3. Implement movement application system from REALISTIC_VIDEO_GUIDE.md
4. Build caption synchronization system from KEYFRAME_GUIDE.md
5. Test with various audio story types and iterate on prompts
6. A/B test different visual styles and movement configurations

For questions or advanced implementations, refer to:
- RESEARCH.md - Core visual principles
- KEYFRAME_GUIDE.md - Keyframe generation strategies
- REALISTIC_VIDEO_GUIDE.md - Movement implementations

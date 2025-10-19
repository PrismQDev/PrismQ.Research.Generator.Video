# Průvodce generováním videa z audio příběhů

## Přehled

Tento průvodce vysvětluje, jak transformovat audio příběhy (narace, podcasty, nahlas čtené Reddit příběhy) do vizuálně poutavých krátkých videí aplikací výzkumem podložených pravidel pohybu a generováním vhodných vizuálů prostřednictvím AI promptů. Přístup synchronizuje vizuální klíčové snímky s audio obsahem pro maximalizaci retence a virality.

## Obsah

1. [Workflow audio-vizuální synchronizace](#workflow-audio-vizuální-synchronizace)
2. [AI generování promptů pro audio obsah](#ai-generování-promptů)
3. [Generování klíčových snímků z audia](#generování-klíčových-snímků-z-audia)
4. [Aplikace pravidel pohybu](#aplikace-pravidel-pohybu)
5. [Příklady audio-to-video specifické pro platformy](#příklady-specifické-pro-platformy)
6. [Kompletní implementace](#kompletní-implementace)
7. [Osvědčené postupy promptového inženýrství](#osvědčené-postupy-promptů)

---

## Workflow audio-vizuální synchronizace

### Kompletní pipeline

```
Vstup audio příběhu
        ↓
Audio analýza (Speech-to-Text + detekce emocí)
        ↓
Segmentace scén (na základě narativních beatů)
        ↓
AI generování promptů (kontextově  vědomé vizuální popisy)
        ↓
Generování klíčových snímků (SDXL/Midjourney prompty)
        ↓
Generování vizuálů (AI generování obrázků/videa)
        ↓
Aplikace pohybu (všechna výzkumem podložená pravidla)
        ↓
Audio-vizuální synchronizace
        ↓
Export specifický pro platformu
```

### Audio analýza

```python
def analyze_audio_story(audio_path):
    """
    Analyzuje audio pro extrakci časování, obsahu a emoce.
    
    Args:
        audio_path: Cesta k audio souboru (MP3, WAV, M4A)
    
    Returns:
        Strukturovaná audio analýza s časováním a emočními daty
    """
    import whisper
    import librosa
    import numpy as np
    
    # 1. Transkripce audia s časovými razítky
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=True)
    
    # 2. Analýza audio vlastností pro emoci/intenzitu
    y, sr = librosa.load(audio_path)
    
    # Energie/intenzita v čase
    rms = librosa.feature.rms(y=y)[0]
    
    # Tempo/rytmus
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    
    # Spektrální vlastnosti (pro detekci nálady)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    
    # 3. Kombinace transkripce s audio vlastnostmi
    segments = []
    for segment in result['segments']:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        
        # Výpočet průměrné intenzity pro tento segment
        start_frame = int(start_time * sr / 512)
        end_frame = int(end_time * sr / 512)
        avg_intensity = np.mean(rms[start_frame:end_frame]) if end_frame > start_frame else 0
        avg_spectral = np.mean(spectral_centroid[start_frame:end_frame]) if end_frame > start_frame else 0
        
        # Detekce emocí z textu a audio vlastností
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
        'total_duration': result['duration'],
        'tempo': float(tempo),
        'beat_times': beats.tolist(),
        'language': result['language']
    }


def detect_emotion(text, audio_intensity, spectral_brightness):
    """
    Detekuje emoce z kombinace textu a audio vlastností.
    
    Args:
        text: Transkribovaný text
        audio_intensity: Průměrná intenzita audia (RMS)
        spectral_brightness: Spektrální centroid (jasnost)
    
    Returns:
        Detekovaná emoce a skóre spolehlivosti
    """
    # Emoční klíčová slova
    emotion_keywords = {
        'anger': ['wściekły', 'zuřivý', 'naštvaný', 'nenávidím', 'stupid', 'idiot'],
        'shock': ['nemůžu uvěřit', 'šokující', 'nemyslitelné', 'co?!', 'vážně?'],
        'excitement': ['úžasné', 'neuvěřitelné', 'skvělé', 'wow', 'ano!'],
        'concern': ['starostlivý', 'obava', 'co když', 'možná', 'nervózní'],
        'sadness': ['smutné', 'depresivní', 'plakat', 'bolest', 'ztráta'],
        'neutral': ['a tak', 'pak', 'další', 'také', 'nicméně'],
    }
    
    text_lower = text.lower()
    
    # Bodování emocí na základě klíčových slov
    emotion_scores = {}
    for emotion, keywords in emotion_keywords.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        emotion_scores[emotion] = score
    
    # Úprava pomocí audio vlastností
    # Vysoká intenzita zvyšuje hněv/vzrušení
    if audio_intensity > 0.15:
        emotion_scores['anger'] += 2
        emotion_scores['excitement'] += 2
    
    # Nízká intenzita zvyšuje smutek/obavu
    if audio_intensity < 0.08:
        emotion_scores['sadness'] += 1
        emotion_scores['concern'] += 1
    
    # Vysoká spektrální jasnost zvyšuje vzrušení/šok
    if spectral_brightness > 2000:
        emotion_scores['excitement'] += 1
        emotion_scores['shock'] += 1
    
    # Získání dominantní emoce
    if sum(emotion_scores.values()) == 0:
        return {'type': 'neutral', 'confidence': 0.5}
    
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    max_score = emotion_scores[dominant_emotion]
    confidence = min(max_score / 5, 1.0)  # Normalizace na 0-1
    
    return {
        'type': dominant_emotion,
        'confidence': confidence,
        'all_scores': emotion_scores
    }
```

---

## AI generování promptů

### Mapování emoce na vizuál

```python
EMOTION_VISUAL_MAPPING = {
    'anger': {
        'colors': ['deep red', 'burning orange', 'dark crimson'],
        'mood': 'intense, dramatic, aggressive',
        'motion': 'rapid, shaking, turbulent',
        'style': 'high contrast, sharp edges, dynamic lighting',
        'effects': 'fire particles, red glow, intense shadows',
        'keywords': ['rage', 'fury', 'conflict', 'tension']
    },
    'shock': {
        'colors': ['bright white', 'electric blue', 'stark contrast'],
        'mood': 'sudden, surprising, attention-grabbing',
        'motion': 'quick zoom, flash, burst',
        'style': 'high brightness, stark contrasts, geometric patterns',
        'effects': 'light burst, flash frame, radiating lines',
        'keywords': ['revelation', 'surprise', 'unexpected', 'dramatic']
    },
    'excitement': {
        'colors': ['vibrant yellow', 'golden', 'energetic orange'],
        'mood': 'uplifting, energetic, positive',
        'motion': 'bouncing, pulsing, expanding',
        'style': 'bright, saturated, dynamic composition',
        'effects': 'particle burst, glow, sparkles',
        'keywords': ['celebration', 'joy', 'energy', 'enthusiasm']
    },
    'concern': {
        'colors': ['muted blue', 'gray', 'desaturated purple'],
        'mood': 'worried, uncertain, contemplative',
        'motion': 'slow drift, gentle sway, uncertain',
        'style': 'soft focus, subdued colors, atmospheric',
        'effects': 'fog, soft shadows, ambient particles',
        'keywords': ['worry', 'uncertainty', 'caution', 'doubt']
    },
    'sadness': {
        'colors': ['deep blue', 'gray', 'muted tones'],
        'mood': 'melancholic, somber, reflective',
        'motion': 'slow, downward, fading',
        'style': 'low saturation, soft lighting, minimal contrast',
        'effects': 'rain, tears, fade to darkness',
        'keywords': ['loss', 'grief', 'loneliness', 'sorrow']
    },
    'neutral': {
        'colors': ['balanced tones', 'natural colors', 'moderate saturation'],
        'mood': 'calm, steady, informative',
        'motion': 'smooth, constant, predictable',
        'style': 'clean, professional, balanced composition',
        'effects': 'subtle movement, gentle transitions',
        'keywords': ['explanation', 'narrative', 'story', 'information']
    },
    'joy': {
        'colors': ['warm yellow', 'soft pink', 'bright pastels'],
        'mood': 'happy, lighthearted, cheerful',
        'motion': 'bouncy, playful, upward',
        'style': 'bright, cheerful, high saturation',
        'effects': 'confetti, sparkles, warm glow',
        'keywords': ['happiness', 'delight', 'pleasure', 'fun']
    }
}


def generate_visual_prompt_for_audio_segment(segment, story_context, visual_style='realistic'):
    """
    Generuje AI prompt pro vizuální reprezentaci audio segmentu.
    
    Args:
        segment: Audio segment s textem a emocí
        story_context: Kontext příběhu (typ, prostředí, nálada)
        visual_style: Styl vizuálu ('realistic', 'abstract', 'anime', 'neon')
    
    Returns:
        Dict s promptem a negativním promptem
    """
    emotion = segment['emotion']['type']
    text_content = segment['text']
    
    # Získání vlastností emoce
    emotion_props = EMOTION_VISUAL_MAPPING.get(emotion, EMOTION_VISUAL_MAPPING['neutral'])
    
    # Extrakce vizuálních klíčových slov z textu
    visual_keywords = extract_visual_keywords(text_content)
    
    # Konstrukce základního promptu
    base_prompt_parts = []
    
    # 1. Nastavení scény (pokud je detekováno z textu)
    if 'outdoor' in text_content.lower() or 'outside' in text_content.lower():
        base_prompt_parts.append("outdoor scene")
    elif 'room' in text_content.lower() or 'inside' in text_content.lower():
        base_prompt_parts.append("interior room")
    else:
        base_prompt_parts.append("abstract background")
    
    # 2. Nálada a barvy založené na emoci
    base_prompt_parts.append(f"{emotion_props['mood']}")
    color_str = ', '.join(emotion_props['colors'][:2])
    base_prompt_parts.append(f"color palette: {color_str}")
    
    # 3. Styl vizuálu
    base_prompt_parts.append(emotion_props['style'])
    
    # 4. Vizuální klíčová slova z obsahu
    if visual_keywords:
        base_prompt_parts.append(', '.join(visual_keywords[:3]))
    
    # 5. Technické specifikace kvality
    base_prompt_parts.append("high quality, detailed, professional lighting")
    
    # 6. Specifika stylu
    style_modifiers = {
        'realistic': 'photorealistic, cinematic, 8k resolution',
        'abstract': 'abstract art, geometric patterns, modern design',
        'anime': 'anime style, vibrant colors, stylized',
        'neon': 'neon lights, cyberpunk, glowing effects, dark background'
    }
    base_prompt_parts.append(style_modifiers.get(visual_style, style_modifiers['realistic']))
    
    prompt = ', '.join(base_prompt_parts)
    
    # Negativní prompt (co se vyhnout)
    negative_prompt = "low quality, blurry, distorted, watermark, text, logos, faces, people, hands, disfigured"
    
    return {
        'prompt': prompt,
        'negative_prompt': negative_prompt,
        'emotion': emotion,
        'visual_keywords': visual_keywords,
        'color_palette': emotion_props['colors']
    }


def extract_visual_keywords(text):
    """
    Extrahuje vizuální klíčová slova z textu pomocí NLP.
    """
    # Zjednodušená extrakce (v produkci použijte NLP knihovnu jako spaCy)
    visual_nouns = []
    
    # Běžná vizuální slova v příbězích
    visual_vocab = {
        'objects': ['car', 'house', 'tree', 'sky', 'water', 'fire', 'mountain', 'city'],
        'settings': ['beach', 'forest', 'desert', 'space', 'ocean', 'street', 'park'],
        'weather': ['rain', 'snow', 'storm', 'sunset', 'sunrise', 'clouds'],
        'actions': ['running', 'flying', 'falling', 'burning', 'glowing']
    }
    
    text_lower = text.lower()
    for category, words in visual_vocab.items():
        for word in words:
            if word in text_lower:
                visual_nouns.append(word)
    
    return visual_nouns[:5]  # Vrátit top 5


def optimize_prompt_for_platform(prompt, platform, audience_data):
    """
    Optimalizuje AI prompt pro specifickou platformu a cílové publikum.
    
    Args:
        prompt: Základní AI prompt
        platform: 'tiktok', 'youtube_shorts', nebo 'instagram_reels'
        audience_data: Dict s informacemi o cílovém publiku
    
    Returns:
        Optimalizovaný prompt
    """
    platform_modifiers = {
        'tiktok': {
            'style': 'trending, viral aesthetic, bold colors, high energy',
            'technical': 'vertical 9:16, mobile optimized, eye-catching',
            'mood': 'fast-paced, attention-grabbing, dynamic'
        },
        'youtube_shorts': {
            'style': 'professional, polished, clear composition',
            'technical': 'vertical 9:16, high resolution, cinematic',
            'mood': 'engaging, informative, storytelling'
        },
        'instagram_reels': {
            'style': 'aesthetic, beautiful, cohesive visual theme',
            'technical': 'vertical 9:16, instagram-worthy, high quality',
            'mood': 'stylish, curated, visually pleasing'
        }
    }
    
    # Modifikátory věku
    age_group = audience_data.get('age_group', '15-18')
    age_modifiers = {
        '10-14': 'colorful, playful, energetic, game-like elements',
        '15-18': 'trendy, edgy, bold, social media aesthetic',
        '19-25': 'sophisticated, aesthetic, modern, relatable',
        '25+': 'professional, refined, quality-focused'
    }
    
    platform_mod = platform_modifiers.get(platform, platform_modifiers['tiktok'])
    age_mod = age_modifiers.get(age_group, age_modifiers['15-18'])
    
    # Kombinace původního promptu s modifikátory
    optimized_prompt = f"{prompt}, {platform_mod['style']}, {age_mod}, {platform_mod['technical']}"
    
    return optimized_prompt
```

---

## Generování klíčových snímků z audia

### Automatické časování klíčových snímků

```python
def generate_keyframes_from_audio(audio_analysis, platform='tiktok', visual_style='realistic'):
    """
    Generuje specifikace klíčových snímků z analyzovaného audia.
    
    Args:
        audio_analysis: Výstup z analyze_audio_story()
        platform: Cílová platforma
        visual_style: Volba vizuální estetiky
    
    Returns:
        Seznam specifikací klíčových snímků s prompty
    """
    segments = audio_analysis['segments']
    total_duration = audio_analysis['total_duration']
    
    # Konfigurace intervalů klíčových snímků specifická pro platformu
    platform_config = {
        'tiktok': {
            'min_interval': 1.5,  # Změna vizuálu každé 1.5-2s
            'max_interval': 2.5,
            'hook_duration': 0.5,  # Kritických prvních 0.5s
        },
        'youtube_shorts': {
            'min_interval': 3.0,  # Změna vizuálu každé 3-4s
            'max_interval': 5.0,
            'hook_duration': 2.0,  # Prvních 2s důležité
        },
        'instagram_reels': {
            'min_interval': 2.5,  # Změna vizuálu každé 2.5-4s
            'max_interval': 4.0,
            'hook_duration': 3.0,  # Prvních 3s důležité
        },
    }
    
    config = platform_config.get(platform, platform_config['tiktok'])
    
    keyframes = []
    current_time = 0
    keyframe_index = 0
    
    # Kontext příběhu z prvních segmentů
    story_context = {
        'type': 'reddit_story',
        'setting': None,
        'mood': segments[0]['emotion']['type'] if segments else 'neutral',
    }
    
    while current_time < total_duration:
        # Najít segment v aktuálním čase
        current_segment = None
        for seg in segments:
            if seg['start'] <= current_time < seg['end']:
                current_segment = seg
                break
        
        if not current_segment and segments:
            # Pokud mezi segmenty, použít nejbližší
            current_segment = min(segments, key=lambda s: abs(s['start'] - current_time))
        
        if not current_segment:
            break
        
        # Generování promptu pro tento klíčový snímek
        prompt_data = generate_visual_prompt_for_audio_segment(
            current_segment,
            story_context,
            visual_style
        )
        
        # Optimalizace pro platformu
        optimized_prompt = optimize_prompt_for_platform(
            prompt_data['prompt'],
            platform,
            {'age_group': '15-18'}
        )
        
        # Určení typu klíčového snímku
        if keyframe_index == 0:
            keyframe_type = 'hook'
            duration = config['hook_duration']
        elif current_time > total_duration * 0.85:
            keyframe_type = 'conclusion'
            duration = min(config['max_interval'], total_duration - current_time)
        else:
            keyframe_type = 'development'
            # Variabilní délka na základě intenzity emoce
            intensity_factor = current_segment['intensity'] / 0.2
            duration = config['min_interval'] + (config['max_interval'] - config['min_interval']) * (1 - min(intensity_factor, 1))
        
        keyframes.append({
            'index': keyframe_index,
            'start_time': current_time,
            'duration': duration,
            'type': keyframe_type,
            'prompt': optimized_prompt,
            'negative_prompt': prompt_data['negative_prompt'],
            'emotion': current_segment['emotion']['type'],
            'text_content': current_segment['text'],
            'movement_intensity': 'high' if current_segment['intensity'] > 0.15 else 'medium',
        })
        
        current_time += duration
        keyframe_index += 1
    
    return keyframes
```

### Šablony promptů podle emocí

```python
EMOTION_PROMPT_TEMPLATES = {
    'anger': {
        'hook': "dramatic intense scene, deep red and orange color scheme, high contrast, aggressive lighting, turbulent atmosphere, {keywords}, cinematic 8k",
        'development': "escalating tension, red and dark tones, sharp angular shapes, intense shadows, {keywords}, dramatic lighting, high quality",
        'conclusion': "explosive culmination, bright red burst, dramatic resolution, {keywords}, intense final moment, cinematic"
    },
    'shock': {
        'hook': "sudden reveal, bright white flash, stark high contrast, electric atmosphere, {keywords}, attention-grabbing, 8k quality",
        'development': "unfolding surprise, bright electric colors, geometric patterns, radiating energy, {keywords}, dynamic composition",
        'conclusion': "shocking resolution, burst of light, stark contrast, {keywords}, memorable final image, cinematic"
    },
    'excitement': {
        'hook': "energetic burst, vibrant golden and yellow tones, dynamic motion, uplifting atmosphere, {keywords}, high energy, 8k",
        'development': "building enthusiasm, bright saturated colors, bouncing particles, positive energy, {keywords}, dynamic lighting",
        'conclusion': "triumphant finale, golden glow, celebratory burst, {keywords}, uplifting resolution, cinematic"
    },
    'concern': {
        'hook': "uncertain atmosphere, muted blue and gray tones, soft shadows, contemplative mood, {keywords}, atmospheric, high quality",
        'development': "growing worry, desaturated colors, subtle tension, ambient fog, {keywords}, thoughtful composition",
        'conclusion': "unresolved tension, fading light, open-ended atmosphere, {keywords}, reflective final moment"
    },
    'sadness': {
        'hook': "melancholic scene, deep blue and gray palette, soft lighting, somber mood, {keywords}, emotional, cinematic 8k",
        'development': "deepening sorrow, muted tones, gentle downward motion, rain effects, {keywords}, reflective atmosphere",
        'conclusion': "poignant resolution, fade to darkness, emotional closure, {keywords}, touching final moment"
    },
    'neutral': {
        'hook': "clear informative scene, balanced colors, professional lighting, clean composition, {keywords}, high quality 8k",
        'development': "steady progression, natural tones, smooth transitions, {keywords}, professional presentation",
        'conclusion': "clear conclusion, balanced final frame, professional wrap-up, {keywords}, polished final scene"
    },
    'joy': {
        'hook': "cheerful bright scene, warm yellow and pink tones, uplifting energy, happy atmosphere, {keywords}, joyful, 8k quality",
        'development': "growing happiness, bright pastels, playful motion, sparkle effects, {keywords}, lighthearted mood",
        'conclusion': "happy ending, warm glow, celebratory finale, {keywords}, delightful resolution, cinematic"
    }
}


def generate_emotion_based_prompt(emotion, keyframe_type, visual_keywords):
    """
    Generuje prompt založený na emoci a typu klíčového snímku.
    
    Args:
        emotion: Typ emoce
        keyframe_type: 'hook', 'development', nebo 'conclusion'
        visual_keywords: Seznam vizuálních klíčových slov z textu
    
    Returns:
        Kompletní prompt pro AI generování obrazu
    """
    template = EMOTION_PROMPT_TEMPLATES.get(emotion, EMOTION_PROMPT_TEMPLATES['neutral'])
    type_template = template.get(keyframe_type, template['development'])
    
    # Nahrazení {keywords} skutečnými klíčovými slovy
    keywords_str = ', '.join(visual_keywords) if visual_keywords else 'abstract background'
    prompt = type_template.replace('{keywords}', keywords_str)
    
    return prompt
```

---

## Aplikace pravidel pohybu

### Mapování intenzity pohybu založené na emoci

```python
def apply_movement_rules_to_audio_video(keyframes, audio_analysis):
    """
    Aplikuje všechna 5 typů pohybu na video založené na audio analýze.
    
    Args:
        keyframes: Seznam klíčových snímků s vizuály
        audio_analysis: Analyzovaná data audia
    
    Returns:
        Slovník s parametry pohybu pro každý klíčový snímek
    """
    movement_specs = []
    
    for i, keyframe in enumerate(keyframes):
        emotion = keyframe['emotion']
        intensity = keyframe.get('movement_intensity', 'medium')
        
        # Mapování emocí na intenzitu pohybu
        emotion_intensity_map = {
            'anger': 'high',
            'shock': 'high',
            'excitement': 'high',
            'joy': 'medium',
            'concern': 'low',
            'sadness': 'low',
            'neutral': 'medium'
        }
        
        base_intensity = emotion_intensity_map.get(emotion, 'medium')
        
        movement_spec = {
            'keyframe_index': i,
            'start_time': keyframe['start_time'],
            'duration': keyframe['duration'],
            
            # 1. KONSTANTNÍ MIKRO-POHYB (vždy aktivní)
            'micro_movement': {
                'enabled': True,
                'drift_amount': 0.5 if base_intensity == 'high' else 0.3,  # pixely/snímek
                'rotation_amount': 2.0 if base_intensity == 'high' else 1.0,  # stupně
                'zoom_amount': 1.015 if base_intensity == 'high' else 1.008,  # faktor
                'noise_seed': i * 1000  # Jedinečné pro každý keyframe
            },
            
            # 2. PARALLAX VRSTVY (hloubka)
            'parallax': {
                'enabled': True,
                'background_speed': 0.2,
                'midground_speed': 1.0,
                'foreground_speed': 1.5 if base_intensity != 'low' else 1.2
            },
            
            # 3. VZOROVÉ ZLOMY (zachování pozornosti)
            'pattern_breaks': generate_pattern_breaks_for_emotion(
                emotion,
                keyframe['duration'],
                base_intensity
            ),
            
            # 4. OSCILAČNÍ POHYBY (rytmické zapojení)
            'oscillating': {
                'enabled': base_intensity != 'low',
                'type': get_oscillation_type_for_emotion(emotion),
                'amplitude': 10 if base_intensity == 'high' else 5,
                'frequency': 2.0 if base_intensity == 'high' else 1.0
            },
            
            # 5. SMĚROVÉ PŘECHODY (změny scén)
            'transition': {
                'type': get_transition_type_for_emotion(emotion),
                'duration': 0.3 if base_intensity == 'high' else 0.5,
                'easing': 'ease_out' if i == 0 else 'ease_in_out'
            }
        }
        
        movement_specs.append(movement_spec)
    
    return movement_specs


def generate_pattern_breaks_for_emotion(emotion, duration, intensity):
    """
    Generuje vzorové zlomy synchronizované s audio beaty.
    """
    # Frekvence vzorových zlomů podle intenzity
    interval_map = {
        'high': 1.2,    # Každých 1.2s
        'medium': 2.0,  # Každé 2s
        'low': 2.5      # Každých 2.5s
    }
    
    interval = interval_map.get(intensity, 2.0)
    
    # Typy zlomů podle emocí
    break_types = {
        'anger': ['shake', 'rotation_twirl', 'flash'],
        'shock': ['flash', 'zoom_burst', 'color_flash'],
        'excitement': ['bounce', 'zoom_pulse', 'particle_burst'],
        'joy': ['bounce', 'sparkle', 'gentle_pulse'],
        'concern': ['slow_zoom', 'gentle_sway'],
        'sadness': ['slow_fade', 'gentle_drift'],
        'neutral': ['zoom_pulse', 'gentle_pan']
    }
    
    available_breaks = break_types.get(emotion, break_types['neutral'])
    
    pattern_breaks = []
    current_time = interval
    
    while current_time < duration:
        break_type = available_breaks[int(current_time / interval) % len(available_breaks)]
        pattern_breaks.append({
            'time': current_time,
            'type': break_type,
            'duration': 0.2,
            'intensity': 1.0 if intensity == 'high' else 0.7
        })
        current_time += interval
    
    return pattern_breaks


def get_oscillation_type_for_emotion(emotion):
    """Vrací typ oscilačního pohybu pro emoce."""
    oscillation_map = {
        'anger': 'shake',
        'shock': 'bounce',
        'excitement': 'pulse',
        'joy': 'bounce',
        'concern': 'sway',
        'sadness': 'slow_sway',
        'neutral': 'gentle_pulse'
    }
    return oscillation_map.get(emotion, 'gentle_pulse')


def get_transition_type_for_emotion(emotion):
    """Vrací typ přechodu pro emoce."""
    transition_map = {
        'anger': 'slam',
        'shock': 'flash_cut',
        'excitement': 'zoom_in',
        'joy': 'bounce_in',
        'concern': 'fade',
        'sadness': 'slow_fade',
        'neutral': 'crossfade'
    }
    return transition_map.get(emotion, 'crossfade')
```

---

## Příklady specifické pro platformy

### Příklad 1: TikTok Reddit Story (Ženy 15-18)

```python
def generate_tiktok_reddit_story_video(audio_path, output_path):
    """
    Kompletní pipeline pro TikTok Reddit story video.
    
    Args:
        audio_path: Cesta k audio souboru s narací příběhu
        output_path: Cesta k výstupnímu video souboru
    """
    # Krok 1: Analýza audia
    print("Analyzuji audio...")
    audio_data = analyze_audio_story(audio_path)
    print(f"✓ Analyzováno {len(audio_data['segments'])} segmentů")
    
    # Krok 2: Generování klíčových snímků s prompty
    print("Generuji klíčové snímky...")
    keyframes = generate_keyframes_from_audio(
        audio_data,
        platform='tiktok',
        visual_style='neon'  # Neonový styl populární na TikToku
    )
    print(f"✓ Vygenerováno {len(keyframes)} klíčových snímků")
    
    # Krok 3: Generování vizuálů pomocí SDXL
    print("Generuji AI vizuály...")
    visuals = []
    for kf in keyframes:
        # Použití SDXL API pro generování obrázků
        image = generate_image_with_sdxl(
            prompt=kf['prompt'],
            negative_prompt=kf['negative_prompt'],
            width=576,   # 9:16 aspect ratio
            height=1024,
            steps=25
        )
        visuals.append(image)
    print(f"✓ Vygenerováno {len(visuals)} vizuálů")
    
    # Krok 4: Aplikace pravidel pohybu
    print("Aplikuji pravidla pohybu...")
    movement_specs = apply_movement_rules_to_audio_video(keyframes, audio_data)
    print(f"✓ Pohybové specifikace připraveny")
    
    # Krok 5: Generování titulků slovo po slově
    print("Generuji titulky slovo po slově...")
    word_captions = generate_word_by_word_captions(
        audio_data,
        style='tiktok',  # Velké tučné titulky
        position='center'
    )
    print(f"✓ Vygenerováno {len(word_captions)} titulků")
    
    # Krok 6: Kompozice finálního videa
    print("Skládám finální video...")
    compose_video(
        visuals=visuals,
        keyframes=keyframes,
        movement_specs=movement_specs,
        audio_path=audio_path,
        captions=word_captions,
        output_path=output_path,
        platform='tiktok'
    )
    print(f"✓ Video uloženo do {output_path}")
    
    return {
        'output_path': output_path,
        'duration': audio_data['total_duration'],
        'keyframe_count': len(keyframes),
        'metrics': {
            'target_completion_rate': '70-85%',
            'hook_duration': '0.5s',
            'avg_keyframe_interval': '1.5-2s'
        }
    }
```

### Příklad 2: YouTube Shorts Educational (30s)

```python
def generate_youtube_shorts_educational(audio_path, output_path):
    """
    Kompletní pipeline pro YouTube Shorts edukativní video.
    """
    # Krok 1: Analýza audia
    audio_data = analyze_audio_story(audio_path)
    
    # Krok 2: Generování klíčových snímků
    keyframes = generate_keyframes_from_audio(
        audio_data,
        platform='youtube_shorts',
        visual_style='realistic'  # Profesionální realistický styl
    )
    
    # Krok 3: Generování geometrických AI pozadí
    visuals = []
    for kf in keyframes:
        # Modifikace promptu pro edukativní styl
        educational_prompt = f"{kf['prompt']}, geometric patterns, educational infographic style, clean professional design"
        image = generate_image_with_sdxl(
            prompt=educational_prompt,
            negative_prompt=kf['negative_prompt'],
            width=576,
            height=1024,
            steps=30
        )
        visuals.append(image)
    
    # Krok 4: Aplikace středních pohybů (ne příliš agresivní)
    movement_specs = apply_movement_rules_to_audio_video(keyframes, audio_data)
    
    # Krok 5: Generování titulků založených na větách
    sentence_captions = generate_sentence_based_captions(
        audio_data,
        style='youtube',  # Profesionální styl
        position='lower_third'
    )
    
    # Krok 6: Přidání lišty postupu
    progress_bar = create_progress_bar(
        duration=audio_data['total_duration'],
        style='minimal_white',
        position='top'
    )
    
    # Krok 7: Kompozice s lištou postupu
    compose_video(
        visuals=visuals,
        keyframes=keyframes,
        movement_specs=movement_specs,
        audio_path=audio_path,
        captions=sentence_captions,
        overlays=[progress_bar],
        output_path=output_path,
        platform='youtube_shorts'
    )
    
    return {
        'output_path': output_path,
        'metrics': {
            'target_completion_rate': '60-75%',
            'hook_duration': '2s',
            'avg_keyframe_interval': '3-4s'
        }
    }
```

### Příklad 3: Instagram Reels Aesthetic (25s)

```python
def generate_instagram_reels_aesthetic(audio_path, background_video_path, output_path):
    """
    Kompletní pipeline pro Instagram Reels s estetickým hybridním stylem.
    
    Args:
        audio_path: Audio narace
        background_video_path: Stock video (např. café, příroda)
        output_path: Výstupní soubor
    """
    # Krok 1: Analýza audia
    audio_data = analyze_audio_story(audio_path)
    
    # Krok 2: Generování jemných klíčových snímků
    keyframes = generate_keyframes_from_audio(
        audio_data,
        platform='instagram_reels',
        visual_style='realistic'
    )
    
    # Krok 3: Načtení a zpracování stock videa
    stock_video = load_video(background_video_path)
    
    # Krok 4: Generování AI overlayů pro každý klíčový snímek
    ai_overlays = []
    for kf in keyframes:
        # Jemné AI overlay kompatibilní s estetickým stylem
        aesthetic_prompt = f"{kf['prompt']}, aesthetic overlay, soft gradient, dreamy atmosphere, instagram aesthetic"
        overlay = generate_image_with_sdxl(
            prompt=aesthetic_prompt,
            negative_prompt=kf['negative_prompt'] + ", harsh, aggressive, neon",
            width=576,
            height=1024,
            steps=35  # Vyšší kroky pro kvalitu
        )
        ai_overlays.append(overlay)
    
    # Krok 5: Aplikace jemných pohybů
    movement_specs = apply_movement_rules_to_audio_video(keyframes, audio_data)
    # Snížení intenzity pro Instagram
    for spec in movement_specs:
        spec['micro_movement']['drift_amount'] *= 0.5
        spec['micro_movement']['rotation_amount'] *= 0.5
    
    # Krok 6: Minimální titulky
    minimal_captions = generate_sentence_based_captions(
        audio_data,
        style='minimal_elegant',
        position='center_lower',
        font_size='medium'
    )
    
    # Krok 7: Kompozice hybridního videa
    compose_hybrid_video(
        stock_video=stock_video,
        ai_overlays=ai_overlays,
        keyframes=keyframes,
        movement_specs=movement_specs,
        audio_path=audio_path,
        captions=minimal_captions,
        blend_mode='soft_light',  # Jemné prolnutí
        opacity=0.4,  # 40% overlay pro jemný efekt
        output_path=output_path,
        platform='instagram_reels'
    )
    
    return {
        'output_path': output_path,
        'metrics': {
            'target_completion_rate': '55-70%',
            'target_save_rate': '5-10%',
            'hook_duration': '3s',
            'avg_keyframe_interval': '2.5-4s'
        }
    }
```

---

## Kompletní implementace

### Třída AudioToVideoGenerator

```python
class AudioToVideoGenerator:
    """
    Kompletní třída pro generování videí z audio příběhů.
    """
    
    def __init__(self, platform='tiktok', visual_style='realistic', sdxl_api_key=None):
        self.platform = platform
        self.visual_style = visual_style
        self.sdxl_api_key = sdxl_api_key
        
        # Načtení konfigurace platformy
        self.config = self._load_platform_config()
    
    def _load_platform_config(self):
        """Načte konfiguraci pro platformu."""
        configs = {
            'tiktok': {
                'resolution': (576, 1024),
                'fps': 30,
                'hook_duration': 0.5,
                'keyframe_interval': (1.5, 2.5),
                'caption_style': 'word_by_word',
                'movement_intensity': 'high'
            },
            'youtube_shorts': {
                'resolution': (576, 1024),
                'fps': 30,
                'hook_duration': 2.0,
                'keyframe_interval': (3.0, 5.0),
                'caption_style': 'sentence',
                'movement_intensity': 'medium',
                'include_progress_bar': True
            },
            'instagram_reels': {
                'resolution': (576, 1024),
                'fps': 30,
                'hook_duration': 3.0,
                'keyframe_interval': (2.5, 4.0),
                'caption_style': 'minimal',
                'movement_intensity': 'low'
            }
        }
        return configs.get(self.platform, configs['tiktok'])
    
    def generate_video(self, audio_path, output_path, stock_video_path=None):
        """
        Hlavní metoda pro generování videa.
        
        Args:
            audio_path: Cesta k audio souboru
            output_path: Cesta k výstupnímu videu
            stock_video_path: Volitelné: cesta ke stock videu pro hybridní režim
        
        Returns:
            Dict s informacemi o vygenerovaném videu
        """
        print(f"\n=== Generování {self.platform} videa ===\n")
        
        # Krok 1: Analýza audia
        print("📊 Krok 1/7: Analýza audia...")
        audio_data = analyze_audio_story(audio_path)
        print(f"   ✓ Analyzováno {len(audio_data['segments'])} segmentů")
        print(f"   ✓ Celková délka: {audio_data['total_duration']:.1f}s")
        
        # Krok 2: Generování klíčových snímků
        print("\n🎬 Krok 2/7: Generování klíčových snímků...")
        keyframes = generate_keyframes_from_audio(
            audio_data,
            platform=self.platform,
            visual_style=self.visual_style
        )
        print(f"   ✓ Vygenerováno {len(keyframes)} klíčových snímků")
        
        # Krok 3: Generování vizuálů
        print("\n🎨 Krok 3/7: Generování AI vizuálů...")
        visuals = self._generate_visuals(keyframes)
        print(f"   ✓ Vygenerováno {len(visuals)} vizuálů")
        
        # Krok 4: Aplikace pohybu
        print("\n🎭 Krok 4/7: Aplikace pravidel pohybu...")
        movement_specs = apply_movement_rules_to_audio_video(keyframes, audio_data)
        print(f"   ✓ Specifikace pohybu připraveny")
        
        # Krok 5: Generování titulků
        print("\n💬 Krok 5/7: Generování titulků...")
        captions = self._generate_captions(audio_data)
        print(f"   ✓ Vygenerováno {len(captions)} titulků")
        
        # Krok 6: Přidání overlay prvků
        print("\n✨ Krok 6/7: Přidávání overlay prvků...")
        overlays = self._generate_overlays(audio_data['total_duration'])
        print(f"   ✓ Přidáno {len(overlays)} overlayů")
        
        # Krok 7: Finální kompozice
        print("\n🎞️  Krok 7/7: Kompozice finálního videa...")
        result = self._compose_final_video(
            visuals=visuals,
            keyframes=keyframes,
            movement_specs=movement_specs,
            audio_path=audio_path,
            captions=captions,
            overlays=overlays,
            output_path=output_path,
            stock_video=stock_video_path
        )
        print(f"   ✓ Video uloženo do {output_path}")
        
        print(f"\n✅ Hotovo! Video vygenerováno úspěšně.\n")
        
        return result
    
    def _generate_visuals(self, keyframes):
        """Generuje vizuály pro klíčové snímky."""
        visuals = []
        for i, kf in enumerate(keyframes):
            print(f"   Generuji vizuál {i+1}/{len(keyframes)}...")
            # Zde by byla integrace se SDXL API
            visual = {
                'prompt': kf['prompt'],
                'emotion': kf['emotion'],
                'index': i
            }
            visuals.append(visual)
        return visuals
    
    def _generate_captions(self, audio_data):
        """Generuje titulky podle stylu platformy."""
        style = self.config['caption_style']
        if style == 'word_by_word':
            return generate_word_by_word_captions(audio_data, self.platform)
        elif style == 'sentence':
            return generate_sentence_based_captions(audio_data, self.platform)
        else:
            return generate_minimal_captions(audio_data, self.platform)
    
    def _generate_overlays(self, duration):
        """Generuje overlay prvky (lišta postupu atd.)."""
        overlays = []
        if self.config.get('include_progress_bar', False):
            overlays.append(create_progress_bar(duration))
        return overlays
    
    def _compose_final_video(self, **kwargs):
        """Skládá finální video ze všech komponent."""
        # Zde by byla logika kompozice videa
        return {
            'output_path': kwargs['output_path'],
            'duration': len(kwargs['keyframes']) * 2,  # Přibližně
            'keyframes': len(kwargs['keyframes']),
            'captions': len(kwargs['captions']),
            'platform': self.platform
        }


# PŘÍKLAD POUŽITÍ
if __name__ == "__main__":
    # TikTok Reddit Story
    tiktok_generator = AudioToVideoGenerator(
        platform='tiktok',
        visual_style='neon'
    )
    tiktok_generator.generate_video(
        audio_path='reddit_story.mp3',
        output_path='tiktok_video.mp4'
    )
    
    # YouTube Shorts Educational
    youtube_generator = AudioToVideoGenerator(
        platform='youtube_shorts',
        visual_style='realistic'
    )
    youtube_generator.generate_video(
        audio_path='educational_story.mp3',
        output_path='youtube_shorts_video.mp4'
    )
    
    # Instagram Reels s hybridním stylem
    instagram_generator = AudioToVideoGenerator(
        platform='instagram_reels',
        visual_style='realistic'
    )
    instagram_generator.generate_video(
        audio_path='aesthetic_story.mp3',
        output_path='instagram_reels_video.mp4',
        stock_video_path='coffee_making.mp4'
    )
```

---

## Osvědčené postupy promptů

### Knihovna promptů

```python
PROMPT_LIBRARY = {
    'backgrounds': {
        'abstract': [
            "abstract geometric patterns, flowing shapes, dynamic composition",
            "liquid motion, fluid dynamics, organic shapes, abstract art",
            "particle system, floating elements, ethereal atmosphere",
            "gradient waves, smooth transitions, modern abstract design"
        ],
        'neon': [
            "neon lights, cyberpunk aesthetic, glowing edges, dark background",
            "electric glow, bright neon colors, futuristic city vibes",
            "neon grid, synthwave style, retro-futuristic atmosphere",
            "glowing particles, neon trails, high-tech aesthetic"
        ],
        'geometric': [
            "geometric shapes, clean lines, mathematical precision, modern design",
            "tessellated patterns, repeating geometry, structured composition",
            "3D geometric forms, angular design, contemporary aesthetic",
            "minimalist geometry, precise shapes, architectural elements"
        ],
        'realistic': [
            "photorealistic scene, natural lighting, cinematic composition",
            "real-world setting, atmospheric perspective, detailed textures",
            "lifelike environment, authentic mood, professional photography style",
            "hyperrealistic details, physical accuracy, natural colors"
        ],
        'aesthetic': [
            "aesthetic composition, dreamy atmosphere, soft colors, instagram-worthy",
            "minimalist aesthetic, clean background, elegant simplicity",
            "pastel tones, soft lighting, gentle mood, curated visual",
            "artistic aesthetic, refined composition, stylish arrangement"
        ]
    },
    'moods': {
        'intense': "dramatic lighting, high contrast, powerful atmosphere, intense mood",
        'calm': "peaceful atmosphere, soft lighting, tranquil mood, serene environment",
        'energetic': "dynamic energy, vibrant colors, active composition, exciting mood",
        'mysterious': "mysterious atmosphere, shadowy elements, enigmatic mood, intrigue",
        'uplifting': "bright atmosphere, positive energy, uplifting mood, optimistic feel",
        'melancholic': "melancholic atmosphere, subdued tones, reflective mood, somber feel"
    },
    'technical_quality': {
        'ultra_high': "8k resolution, ultra detailed, professional rendering, perfect composition",
        'high': "high quality, detailed, well-composed, professional lighting",
        'standard': "good quality, clear details, balanced composition",
    }
}


def build_prompt_from_library(background_style, mood, quality='high', custom_elements=None):
    """
    Vytváří prompt z knihovny šablon.
    
    Args:
        background_style: Typ pozadí ('abstract', 'neon', atd.)
        mood: Nálada ('intense', 'calm', atd.)
        quality: Úroveň technické kvality
        custom_elements: Volitelné: vlastní prvky k přidání
    
    Returns:
        Kompletní prompt
    """
    import random
    
    # Získání pozadí
    bg_templates = PROMPT_LIBRARY['backgrounds'].get(background_style, PROMPT_LIBRARY['backgrounds']['abstract'])
    background = random.choice(bg_templates)
    
    # Získání nálady
    mood_template = PROMPT_LIBRARY['moods'].get(mood, PROMPT_LIBRARY['moods']['calm'])
    
    # Získání kvality
    quality_template = PROMPT_LIBRARY['technical_quality'].get(quality, PROMPT_LIBRARY['technical_quality']['high'])
    
    # Sestavení promptu
    prompt_parts = [background, mood_template, quality_template]
    
    if custom_elements:
        prompt_parts.insert(1, ', '.join(custom_elements))
    
    return ', '.join(prompt_parts)
```

### Testování variací promptů

```python
def test_prompt_variations(base_segment, num_variations=3):
    """
    Generuje několik variací promptu pro A/B testování.
    
    Args:
        base_segment: Audio segment s emocí a textem
        num_variations: Počet variací k vytvoření
    
    Returns:
        Seznam variant promptů
    """
    variations = []
    
    emotion = base_segment['emotion']['type']
    visual_keywords = extract_visual_keywords(base_segment['text'])
    
    # Variace 1: Realistický styl
    variations.append({
        'style': 'realistic',
        'prompt': build_prompt_from_library('realistic', emotion, 'high', visual_keywords),
        'description': 'Fotorealistické pozadí s přirozeným osvětlením'
    })
    
    # Variace 2: Abstraktní styl
    variations.append({
        'style': 'abstract',
        'prompt': build_prompt_from_library('abstract', emotion, 'high', visual_keywords),
        'description': 'Abstraktní geometrické vzory a tvary'
    })
    
    # Variace 3: Neonový styl (populární na TikToku)
    variations.append({
        'style': 'neon',
        'prompt': build_prompt_from_library('neon', emotion, 'high', visual_keywords),
        'description': 'Neonové světla a cyberpunk estetika'
    })
    
    return variations[:num_variations]
```

---

## Závěr

Tento průvodce poskytuje kompletní framework pro transformaci audio příběhů do vizuálně poutavých krátkých videí optimalizovaných pro TikTok, YouTube Shorts a Instagram Reels.

**Klíčové poznatky:**

1. **Detekce emocí řídí vše**: Audio analýza s detekcí emocí informuje vizuální styl, intenzitu pohybu a AI prompty
2. **Platforma-první přístup**: Každá platforma vyžaduje odlišné časování, styl a intenzitu
3. **Synchronizace je kritická**: Vizuální změny musí zarovnat s audio beaty a narativními zlomy
4. **Pohyb udržuje pozornost**: Všech 5 typů pohybu pracuje společně pro maximální zapojení
5. **AI prompty potřebují kontext**: Nejlepší prompty kombinují emoce, obsah a vizuální klíčová slova

**Další kroky:**

- Implementujte `AudioToVideoGenerator` třídu
- Integrujte SDXL nebo Midjourney API
- Vytvořte knihovnu emočních šablon
- A/B testujte různé vizuální styly
- Sledujte metriky a iterujte

Šťastné vytváření! 🎬✨🎵

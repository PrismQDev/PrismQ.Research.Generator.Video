# Documentation Index

This directory contains comprehensive research, guides, and documentation for the PrismQ Video Generation project.

## 📁 Documentation Structure

### 📋 Implementation Summaries
**Location:** `docs/summaries/`

High-level summaries of major implementation components.

- **[PIPELINE_IMPLEMENTATION.md](summaries/PIPELINE_IMPLEMENTATION.md)** - Complete video generation pipeline summary:
  - Visual engagement principles and research findings
  - Core architecture and pipeline flow
  - Testing results and performance metrics
  - Security scan results

- **[KEYFRAME_IMPLEMENTATION.md](summaries/KEYFRAME_IMPLEMENTATION.md)** - Universal keyframe generation summary:
  - Scene-based architecture for 2-3 minute videos
  - Implementation classes and features
  - Transition effects and retention optimization
  - Expected engagement metrics

- **[PIPELINE_IMPLEMENTATION_CS.md](summaries/PIPELINE_IMPLEMENTATION_CS.md)** - Czech translation of pipeline summary

### 📊 Research
**Location:** `docs/research/`

Core research and analysis documents that form the theoretical foundation of the project.

- **[RESEARCH.md](research/RESEARCH.md)** - Main research document covering:
  - Visual principles for maximizing engagement
  - Constant motion, high contrast, and pattern-breaking strategies
  - Color theory and video flow optimization
  - Platform-specific optimization (YouTube Shorts, TikTok, Instagram Reels)
  - 27 comprehensive research questions
  - Reddit story video strategies for target audiences
  - Performance benchmarks and A/B testing frameworks

- **[REDDIT_STORIES_EXPANDED.md](research/REDDIT_STORIES_EXPANDED.md)** - ⭐ NEW: Expanded Reddit stories research:
  - 50+ content topics and story categories
  - Deep dive into 18-24 demographic behavior
  - Platform-specific strategies (TikTok, YouTube Shorts, Instagram Reels)
  - Psychological triggers for 12-25 female audiences
  - Neurological engagement mechanisms
  - Emerging trends and future directions (2024-2025)
  - Performance metrics and success indicators
  - Content calendar and posting strategies

- **[VIDEO_GENERATION_PROJECTS_COMPARISON.md](research/VIDEO_GENERATION_PROJECTS_COMPARISON.md)** - Comprehensive comparison of AI video generation projects:
  - Open-source models (Open-Sora, CogVideoX, AnimateDiff, etc.)
  - Commercial solutions (RunwayML Gen-3/Gen-4, OpenAI Sora, Google Veo 3)
  - Feature matrices and quality assessments
  - Hardware requirements and technical specifications
  - Integration strategies with PrismQ pipeline
  - Use case recommendations

### 🤖 AI Models
**Location:** `docs/models/`

Detailed research and analysis of specific AI video generation models.

- **[HUNYUANVIDEO_RESEARCH.md](models/HUNYUANVIDEO_RESEARCH.md)** - Tencent's HunyuanVideo model:
  - 13B+ parameter open-source foundation model
  - Text-to-video (T2V) and image-to-video (I2V) capabilities
  - 3D VAE compression and dual-stream transformer architecture
  - RTX 5090 setup and optimization guide
  - Horror/true crime content workflows
  - Integration patterns with PrismQ pipeline

- **[LONGCAT_VIDEO_RESEARCH.md](models/LONGCAT_VIDEO_RESEARCH.md)** - Meituan's LongCat-Video model:
  - 13.6B parameter model for long-form video generation
  - Unified dense transformer with block sparse attention
  - Text-to-video, image-to-video, and video continuation
  - Multi-reward RLHF training approach
  - Minutes-long video generation capabilities
  - Detailed comparison with Sora, CogVideoX, and AnimateDiff

- **[LTXV_VIDEO_RESEARCH.md](models/LTXV_VIDEO_RESEARCH.md)** - Lightricks' LTX-Video model:
  - Real-time video generation (30 FPS @ 1216×704)
  - Model family: 13B, 2B variants, FP8/INT8 optimizations
  - Multi-keyframe conditioning and shot extension
  - ComfyUI integration with official workflows
  - TeaCache acceleration and Q8 kernels
  - Future LTX-2 developments

### 📚 Guides
**Location:** `docs/guides/`

Practical implementation guides and how-to documentation.

#### Content Creation Guides

- **[PROMPT_LIBRARY.md](guides/PROMPT_LIBRARY.md)** - ⭐ NEW: Comprehensive prompt library for Reddit stories:
  - 200+ ready-to-use prompts categorized by topic
  - Optimized for US women ages 12-25
  - Platform-specific optimization (TikTok, YouTube Shorts, Instagram Reels)
  - Story structure formulas and engagement triggers
  - Customization framework and A/B testing strategies
  - Ethical guidelines and content safety

- **[CONTENT_PIPELINE_RECOMMENDATIONS.md](guides/CONTENT_PIPELINE_RECOMMENDATIONS.md)** - ⭐ NEW: Technical pipeline for 9:16 HD 60fps video:
  - Three-tier pipeline approach (Basic, Advanced, Professional)
  - Hardware and software recommendations by budget
  - Platform-specific export optimization
  - Frame rate strategy (30fps vs 60fps)
  - Workflow optimization and batching strategies
  - Cost analysis and ROI expectations
  - Scaling path from beginner to enterprise

#### Video Generation Guides

- **[AUDIO_TO_VIDEO_GUIDE.md](guides/AUDIO_TO_VIDEO_GUIDE.md)** - Transform audio narration into visually engaging videos:
  - Speech-to-text with emotion detection
  - AI prompt generation synchronized with audio
  - Automatic keyframe timing from narration beats
  - Movement application with research-based rules
  - Platform-specific examples (TikTok, YouTube, Instagram)
  - Complete AudioToVideoGenerator implementation

- **[REALISTIC_VIDEO_GUIDE.md](guides/REALISTIC_VIDEO_GUIDE.md)** - Generate realistic videos with engagement principles:
  - AI script integration with visual timing
  - Multiple movement types (micro-movement, parallax, pattern breaks)
  - Platform-specific examples for all major platforms
  - Stock footage and AI-generated background integration
  - Production optimization and quality assurance

#### Keyframe Guides

- **[KEYFRAME_GUIDE.md](guides/KEYFRAME_GUIDE.md)** - Strategic keyframe generation from subtitles:
  - Subtitle-to-scene segmentation strategies
  - Platform-specific keyframe timing
  - Visual design for hook, transition, and completion keyframes
  - Scene-based visual structure for maximum engagement

- **[UNIVERSAL_KEYFRAME_GUIDE.md](guides/UNIVERSAL_KEYFRAME_GUIDE.md)** - Optimal keyframes for 2-3 minute videos:
  - Scene-based keyframe architecture
  - Two-keyframe approach (scene end + scene start)
  - Strategic transition effects for retention
  - Platform-universal specifications (9:16 vertical format)
  - Works across YouTube, TikTok, Instagram, Facebook, etc.
  - Complete implementation with code examples

- **[SDXL_KEYFRAME_GUIDE.md](guides/SDXL_KEYFRAME_GUIDE.md)** - High-quality keyframe generation with SDXL:
  - SDXL Base + Refiner + Tiled VAE + Real-ESRGAN pipeline
  - Optimal settings for resolution, samplers, and CFG scales
  - Structured prompt engineering for cinematic quality
  - Local generation on RTX 5090
  - Troubleshooting and quality optimization

#### Model-Specific Guides

- **[LONGCAT_VIDEO_INSTALLATION_GUIDE.md](guides/LONGCAT_VIDEO_INSTALLATION_GUIDE.md)** - Step-by-step LongCat-Video setup:
  - Installation for Windows + RTX 5090
  - Hardware requirements and dependencies
  - Model weight downloads and configuration
  - Demo scripts and testing procedures

- **[LONGCAT_VIDEO_PROMPT_TEMPLATES.md](guides/LONGCAT_VIDEO_PROMPT_TEMPLATES.md)** - Ready-to-use prompt templates:
  - 50+ prompts for horror/true-crime content
  - Optimized for vertical video (9:16)
  - Atmospheric scenes for suspense and mystery
  - Targeting US female audience (10-30)

### 🌍 Translations
**Location:** `docs/translations/`

Czech translations of key documentation.

- **[RESEARCH_CS.md](translations/RESEARCH_CS.md)** - Czech translation of main research document
- **[AUDIO_TO_VIDEO_GUIDE_CS.md](translations/AUDIO_TO_VIDEO_GUIDE_CS.md)** - Czech audio-to-video guide
- **[KEYFRAME_GUIDE_CS.md](translations/KEYFRAME_GUIDE_CS.md)** - Czech keyframe guide
- **[VIDEO_GENERATION_PROJECTS_COMPARISON_CS.md](translations/VIDEO_GENERATION_PROJECTS_COMPARISON_CS.md)** - Czech projects comparison

## 🗺️ Quick Navigation

### By Use Case

**Reddit Stories & Real-Life Drama (NEW!):**
- Start with [REDDIT_STORIES_EXPANDED.md](research/REDDIT_STORIES_EXPANDED.md) for expanded research
- Use [PROMPT_LIBRARY.md](guides/PROMPT_LIBRARY.md) for 200+ story prompts
- Follow [CONTENT_PIPELINE_RECOMMENDATIONS.md](guides/CONTENT_PIPELINE_RECOMMENDATIONS.md) for technical setup
- Target: US women ages 12-25 on TikTok, YouTube Shorts, Instagram Reels

**Short-form vertical videos (15-60 seconds):**
- Start with [RESEARCH.md](research/RESEARCH.md) for principles
- Use [KEYFRAME_GUIDE.md](guides/KEYFRAME_GUIDE.md) for scene structure
- Apply [AUDIO_TO_VIDEO_GUIDE.md](guides/AUDIO_TO_VIDEO_GUIDE.md) if working with narration

**Medium-form videos (2-3 minutes):**
- Review [UNIVERSAL_KEYFRAME_GUIDE.md](guides/UNIVERSAL_KEYFRAME_GUIDE.md)
- Consider [REALISTIC_VIDEO_GUIDE.md](guides/REALISTIC_VIDEO_GUIDE.md) for realistic content

**Long-form videos (minutes-long):**
- Explore [LONGCAT_VIDEO_RESEARCH.md](models/LONGCAT_VIDEO_RESEARCH.md)
- Follow [LONGCAT_VIDEO_INSTALLATION_GUIDE.md](guides/LONGCAT_VIDEO_INSTALLATION_GUIDE.md)

**Horror/true-crime content:**
- Use [LONGCAT_VIDEO_PROMPT_TEMPLATES.md](guides/LONGCAT_VIDEO_PROMPT_TEMPLATES.md)
- Reference [HUNYUANVIDEO_RESEARCH.md](models/HUNYUANVIDEO_RESEARCH.md)

**High-quality keyframes:**
- Follow [SDXL_KEYFRAME_GUIDE.md](guides/SDXL_KEYFRAME_GUIDE.md)

**9:16 HD 60fps Production:**
- Review [CONTENT_PIPELINE_RECOMMENDATIONS.md](guides/CONTENT_PIPELINE_RECOMMENDATIONS.md)
- Choose pipeline based on budget and volume

### By Platform

**TikTok:**
- [RESEARCH.md](research/RESEARCH.md) - Platform-specific optimization
- [AUDIO_TO_VIDEO_GUIDE.md](guides/AUDIO_TO_VIDEO_GUIDE.md) - TikTok Reddit stories

**YouTube Shorts:**
- [RESEARCH.md](research/RESEARCH.md) - Algorithm optimization
- [UNIVERSAL_KEYFRAME_GUIDE.md](guides/UNIVERSAL_KEYFRAME_GUIDE.md) - 2-3 min format

**Instagram Reels:**
- [RESEARCH.md](research/RESEARCH.md) - Visual engagement
- [REALISTIC_VIDEO_GUIDE.md](guides/REALISTIC_VIDEO_GUIDE.md) - Platform examples

### By Technology

**SDXL:**
- [SDXL_KEYFRAME_GUIDE.md](guides/SDXL_KEYFRAME_GUIDE.md)

**HunyuanVideo:**
- [HUNYUANVIDEO_RESEARCH.md](models/HUNYUANVIDEO_RESEARCH.md)

**LongCat-Video:**
- [LONGCAT_VIDEO_RESEARCH.md](models/LONGCAT_VIDEO_RESEARCH.md)
- [LONGCAT_VIDEO_INSTALLATION_GUIDE.md](guides/LONGCAT_VIDEO_INSTALLATION_GUIDE.md)

**LTX-Video:**
- [LTXV_VIDEO_RESEARCH.md](models/LTXV_VIDEO_RESEARCH.md)

**Comparison of all models:**
- [VIDEO_GENERATION_PROJECTS_COMPARISON.md](research/VIDEO_GENERATION_PROJECTS_COMPARISON.md)

## 📊 Documentation Statistics

- **Total documents:** 26 files (⭐ 3 new!)
- **Implementation summaries:** 3 documents
- **Research papers:** 3 documents (⭐ 1 new: REDDIT_STORIES_EXPANDED.md)
- **AI model analyses:** 3 documents
- **Implementation guides:** 9 documents (⭐ 2 new: PROMPT_LIBRARY.md, CONTENT_PIPELINE_RECOMMENDATIONS.md)
- **Translations:** 4 documents (Czech)
- **Total lines:** ~30,000+ lines of documentation (⭐ +10,400 lines added)
- **Translations:** 4 documents (Czech)
- **Total lines:** ~19,600+ lines of documentation

## 🔗 External Resources

- **Main Repository:** [github.com/PrismQDev/PrismQ.Research.Generator.Video](https://github.com/PrismQDev/PrismQ.Research.Generator.Video)
- **Root README:** [../README.md](../README.md)
- **Quick Start Guide:** [../QUICKSTART.md](../QUICKSTART.md)

## 📝 Contributing

When adding new documentation:

1. Place implementation summaries in `docs/summaries/`
2. Place research papers in `docs/research/`
3. Place AI model analyses in `docs/models/`
4. Place implementation guides in `docs/guides/`
5. Place translations in `docs/translations/`
6. Update this INDEX.md file
7. Update the main README.md if needed

## 📄 License

All documentation is released under MIT License - See LICENSE file for details.

---

**Last updated:** 2025-10-27

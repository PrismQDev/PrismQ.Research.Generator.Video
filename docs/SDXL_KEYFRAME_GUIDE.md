# High-Quality Local Keyframe Generation (SDXL)

## Goal
Achieve **consistent, high-quality keyframes** locally (RTX 5090), free from artifacts, extra limbs, or blurry details, suitable as cinematic references for video generation.

---

## Recommended Model Stack
- **SDXL Base** → main generation (1024×1024)  
- **SDXL Refiner** → fine detail refinement at low denoise  
- **Tiled VAE** → prevents seams, handles high-res decoding  
- **IP-Adapter (optional)** → character consistency from reference images  
- **Real-ESRGAN** → upscale 2×-4× (models: realesr-animevideov3, RealESRGAN_x4plus)  
- **CodeFormer (optional)** → mild face enhancement  

---

## Prompting Guidelines
- **Prompt structure**:  
  ```
  [Style/Genre], [Composition], [Environment], [Characters + Expression],
  [Lighting], [Color Palette], [Optics/Camera]
  ```

- **Example positive prompt**:  
  ```
  cinematic close-up portrait, 35mm photograph, natural skin texture,
  moody cinematic lighting, volumetric light, shallow depth of field,
  ultra-detailed, intricate, 8k master
  ```

- **Negative prompt** (short & effective):  
  ```
  blurry, low-res, noisy, deformed, extra fingers, extra limbs,
  disfigured, bad anatomy, warped, artifacts, text, watermark, logo
  ```

---

## Settings (Sweet Spot)
- **Resolution**: 1024×1024 (native SDXL)  
- **Sampler**: DPM++ 2M Karras / Euler a / UniPC  
- **Steps**: 35–50 (40 typical)  
- **CFG scale**: 5.0–6.5  
- **Seed**: locked for consistency  

### Refiner
- **Denoising strength**: 0.15–0.25  
- **Steps**: 15–20  

### Hi-Res Latent Upscale
- Scale: 1.5×–2×  
- **Strength**: 0.25–0.35  
- **Steps**: 15–20  

### Tiled VAE
- **Tile size**: 512–1024  
- **Overlap**: 64–96 px  

---

## Python Pipeline (Diffusers)

```python
import torch
from diffusers import (
    StableDiffusionXLPipeline,
    StableDiffusionXLImg2ImgPipeline,
    AutoencoderKL,
    DPMSolverMultistepScheduler
)
from PIL import Image
import subprocess, os

DEVICE = "cuda"
DTYPE = torch.float16

SDXL_BASE_PATH = "./models/sdxl-base"
SDXL_REFINER_PATH = "./models/sdxl-refiner"
SDXL_VAE_PATH = "./models/sdxl-vae"
REALESRGAN_BIN = "./realesrgan-ncnn-vulkan"
REALESRGAN_MODEL = "realesr-animevideov3"

vae = AutoencoderKL.from_pretrained(SDXL_VAE_PATH, torch_dtype=DTYPE).to(DEVICE)
vae.enable_tiling()
vae.enable_slicing()

pipe_base = StableDiffusionXLPipeline.from_pretrained(
    SDXL_BASE_PATH, vae=vae, torch_dtype=DTYPE, use_safetensors=True
).to(DEVICE)
pipe_base.scheduler = DPMSolverMultistepScheduler.from_config(pipe_base.scheduler.config)

pipe_refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    SDXL_REFINER_PATH, vae=vae, torch_dtype=DTYPE, use_safetensors=True
).to(DEVICE)
pipe_refiner.scheduler = DPMSolverMultistepScheduler.from_config(pipe_refiner.scheduler.config)

prompt = "cinematic close-up portrait, 35mm photograph, natural skin texture, cinematic lighting, ultra-detailed"
negative = "blurry, low-res, noisy, deformed, extra fingers, extra limbs, bad anatomy, artifacts, text, watermark"

seed = 123456
generator = torch.Generator(device=DEVICE).manual_seed(seed)

# 1. Base
image_base = pipe_base(
    prompt=prompt, negative_prompt=negative,
    width=1024, height=1024,
    num_inference_steps=40, guidance_scale=5.5,
    generator=generator
).images[0]

# 2. Refiner
image_refined = pipe_refiner(
    prompt=prompt, negative_prompt=negative,
    image=image_base, strength=0.2,
    num_inference_steps=18, guidance_scale=5.5,
    generator=generator
).images[0]

# 3. Hi-Res upscale via img2img
hires_input = image_refined.resize((1536, 1536), Image.LANCZOS)
image_hires = pipe_refiner(
    prompt=prompt, negative_prompt=negative,
    image=hires_input, strength=0.3,
    num_inference_steps=18, guidance_scale=5.0,
    generator=generator
).images[0]

os.makedirs("out", exist_ok=True)
p_hires = "out/keyframe_hires.png"
image_hires.save(p_hires)

# 4. Real-ESRGAN 2× upscale
p_up = "out/keyframe_upscaled.png"
if os.path.exists(REALESRGAN_BIN) and os.access(REALESRGAN_BIN, os.X_OK):
    subprocess.run([
        REALESRGAN_BIN, "-i", p_hires, "-o", p_up,
        "-n", REALESRGAN_MODEL, "-s", "2"
    ], check=True)
else:
    print(f"Warning: Real-ESRGAN binary not found at {REALESRGAN_BIN}")
```

---

## Troubleshooting
- **Artifacts/fragments** → lower `strength` in refiner/hi-res, increase steps, ensure correct VAE.  
- **Noise/overcooked** → reduce CFG scale, use Karras scheduler.  
- **Seams at high res** → increase VAE tile overlap.  
- **Broken faces/hands** → add negatives or apply CodeFormer (weight 0.3–0.5).  

---

## Presets
- **Portraits**: 40 steps base, Refiner 0.2 / 18 steps, Hi-Res ×1.5, Real-ESRGAN 2× (realesr-animevideov3)  
- **Complex scenes**: 48 steps base, Refiner 0.22 / 20 steps, Hi-Res ×2, tiled VAE overlap ≥96, Real-ESRGAN 2×-4× then downscale to final resolution

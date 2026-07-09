# Image Generation

*Part of the [pipeline docs](../pipeline_automation.md). Stills are made by `generate_images.py` (Gemini "nano banana"), with prompts composed at runtime by `prompt_builder.py`. Accuracy enforcement lives in the [`visual-accuracy-gate` skill](../visual-accuracy-gate/SKILL.md).*

## AI Image Prompt Structure

Every image prompt follows this pattern (composed automatically by `prompt_builder.py`):

```
[STYLE CARD PREFIX]

Scene type: [establishing / cross_section / map / detail / scale_comparison]
Subject: [specific description of what to illustrate]
Factual constraints: [the scene's visual_facts, when present]
Civilization accent color: [hex from color system]
Composition: [specific framing instructions]
```

## Style Card (Prepended to Every Prompt)

```
Isometric flat-design technical illustration. Clean vector aesthetic, 
warm parchment background (#F5F0E8), precise geometric lines, 
charcoal dark elements (#2C2C2C). Architectural cross-section style.
Warm golden-hour ambient lighting with soft directional shadows.
No humans visible (or tiny silhouettes for scale only). 
No text in image. High architectural precision. 
Educational diagram aesthetic. Quietly dramatic mood.
```

*(Single source of truth: `style_card.txt` — `prompt_builder.py` reads it at runtime.)*

## Image Resolution

- **Generate at:** 2048×2048 (minimum) or the model's highest native resolution
- **Upscale to:** 4096×4096 before passing to the assembler
- **Why:** Ken Burns zooms crop into the image — low-res source = blurry zoom

Upscaling options:
- Real-ESRGAN (free, local, `pip install realesrgan`)
- Topaz Gigapixel AI (paid, best quality)
- Nano Banana's built-in upscaler (if available via API)

## Style Consistency — Three Tiers

> **This is your batch-consistency lever — the "same look across the whole video" problem.** Two things to separate: *within-video* consistency (all ~55 images of one video match) and *cross-video* brand consistency (video #30 looks like video #1). Reference anchors solve the first; a LoRA solves the second. At 2 videos/month, adopt anchors immediately and add a LoRA after ~5–8 videos.

**Tier 1: Prompt Prefix (use from day 1)**
- Prepend the style card to every generation
- Consistency: ~70–80%
- Effort: zero — just copy-paste the prefix

**Tier 2: Reference Image Conditioning (adopt immediately, not month 2–3)**
- Generate 8–10 "anchor" images that define your visual identity, keep them in `assets/style_anchors/`
- Pass one anchor as a style reference on **every** generation for a video — this is what locks the look across all ~55 images of a single video
- **Within-video tip:** generate all of a video's images in one session, same model version, same anchor, and keep seeds in a related range for extra coherence
- Consistency: ~85–90%

```python
response = client.generate_image(
    model="nano-banana-2-lite",
    prompt=f"{STYLE_CARD}\n\n{scene_prompt}",
    reference_images=["./assets/style_anchors/anchor_01.png"],
    style_strength=0.7
)
```

> **Two reference images, two roles.** Scenes with a `reference_image` (real photo) get it passed **alongside** the style anchor by `generate_images.py`. The prompt tells the model which image plays which role: **anchor = LOOK, reference photo = GEOMETRY.** See the [`visual-accuracy-gate` skill](../visual-accuracy-gate/SKILL.md).

**Tier 3: LoRA Fine-Tuning (add after ~5–8 videos, once you have 20–30 "keeper" images)**
- Train a custom LoRA on Flux using 20–30 of your best on-brand images
- One-time cost: ~$5–$10 on Replicate, ~30 min training
- This is the strongest lever for *cross-video* brand consistency (every future video inherits the exact look)
- Consistency: ~95%+

> **Reality check on the AI-visual dependency:** you're right that you can't hand-animate — and you don't need to. The pipeline is built so AI does what it's genuinely reliable at: (1) generating consistent stills (anchors + LoRA make this a solved-enough problem in 2026), and (2) adding *subtle* motion (parallax, flowing water, drifting dust) to those stills via Kling — image-to-video's strongest, most dependable mode. The risky "full character animation" is never attempted. And because of graceful degradation (any scene can fall back to Ken Burns + text overlay, pure ffmpeg), **the worst realistic case is a Simple-History-style video of clean stills with motion overlays — still perfectly shippable.** You are not betting the channel on any single AI tool behaving perfectly.

# Video Pipeline Automation — Technical Reference

> **Revised operating assumptions (July 6, 2026 — see `strategy_review.md`):**
> - **Cadence: 2 videos/month**, not 8. This fits comfortably inside Pro-tier / entry-plan limits, so **no self-hosted video model (Wan/Hunyuan on RunPod/Modal) is needed** — self-hosting would cost tens of hours of engineering to save ~₹1,500–2,000/mo, with a quality downgrade on your flat/isometric style. Revisit only if you ever go full-time at 30+ videos/month.
> - **Narration is your own recorded voice** from day 1 (AI clone is a pickup-only fallback). See the Voice section below.
> - **Two mandatory human steps are now part of the pipeline: a real fact-check pass, and the "Altered content" disclosure on upload.** These are non-optional — they're what keeps the channel monetizable under YouTube's 2026 inauthentic-content policy.
> - **Graceful degradation:** if AI animation ever fails on a clip, that scene falls back to Ken Burns + text overlay (pure ffmpeg, zero AI). You always have a shippable video even if every animation attempt disappoints — so you are never existentially dependent on one AI tool.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                               │
│              Claude Desktop (Pro plan)                        │
│                                                               │
│  You type a topic. Claude handles everything via MCP tools:   │
│                                                               │
│  Step 1: Claude drafts script from YOUR fact-checked notes    │
│  Step 2: Generate ~55 still images via Gemini MCP             │
│  Step 3: Tag 50% of scenes for AI animation                   │
│  Step 4: YOU record narration (AI clone = pickup fallback)    │
│  Step 5: Output assembler commands                            │
│                                                               │
│  Connected MCP Servers:                                       │
│  ┌────────────────────┐ ┌─────────────────┐ ┌──────────────┐│
│  │ 🎨 Gemini Image   │ │ 🎙️ ElevenLabs  │ │ 📂 Filesystem ││
│  │ (Nano Banana)      │ │ (Voice Clone)   │ │              ││
│  │                    │ │                 │ │              ││
│  │ generate_image()   │ │ text_to_speech()│ │ read/write   ││
│  └────────────────────┘ └─────────────────┘ └──────────────┘│
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    ANIMATION (50% of scenes)                  │
│              Kling AI / Runway (via API or web UI)            │
│                                                               │
│  For ~27 "animate" scenes:                                   │
│  Upload still → prompt parallax/element motion → 5-8s clip   │
│  Download animated clips to clips/ folder                     │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    ASSEMBLY                                   │
│              video_assembler.py (local)                       │
│                                                               │
│  Static scenes: Ken Burns + text overlays                    │
│  Animated scenes: import clips + text overlays               │
│  Particle overlays composited on ~10 scenes                  │
│  Voiceover + ambient music mixed                             │
│  Crossfade transitions → final_video.mp4                     │
└──────────────────────────────────────────────────────────────┘
```

---

## One-Time Setup

### Prerequisites

```bash
# Core tools
brew install ffmpeg imagemagick
pip install moviepy pillow numpy

# Node.js (for MCP servers)
brew install node
```

### API Keys

| Service | Where to get it | Cost |
|:---|:---|:---|
| **Google AI Studio** | [aistudio.google.com](https://aistudio.google.com) → "Get API key" | Free tier (generous daily limits) |
| **ElevenLabs** | [elevenlabs.io](https://elevenlabs.io) → Settings → API Key | Starter plan ~$5/month |
| **Anthropic** (optional, for headless scripting) | [console.anthropic.com](https://console.anthropic.com) | $5 free credit, then pay-per-use |

> [!IMPORTANT]
> Your Google AI Plus subscription (₹400/mo) does NOT provide API access. The API key comes from Google AI Studio, which is free and completely separate. Your Claude Pro subscription (₹2,000/mo) gives you Claude Desktop with MCP support — that's the part you use.

### Claude Desktop MCP Configuration

**File:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mcp-kling": {
      "command": "npx",
      "args": ["-y", "mcp-kling@latest"],
      "env": {
        "KLING_ACCESS_KEY": "YOUR_ACCESS_KEY_HERE",
        "KLING_SECRET_KEY": "YOUR_SECRET_KEY_HERE"
      }
    },
    "gemini-image": {
      "command": "npx",
      "args": ["-y", "@anthropic/gemini-mcp-server"],
      "env": {
        "GOOGLE_API_KEY": "AIza..."
      }
    },
    "elevenlabs-voice": {
      "command": "npx",
      "args": ["-y", "elevenlabs-mcp-server"],
      "env": {
        "ELEVENLABS_API_KEY": "sk_..."
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/mritunjaymohitesh/dev/yt video ideas"
      ]
    }
  }
}
```

After editing, restart Claude Desktop. The tools will appear in your "Search and Tools" menu.

### Voice Clone Setup (One-Time)

1. Go to ElevenLabs → Voices → "Add Voice" → "Instant Voice Cloning"
2. Record a 30–60 second sample of yourself reading narration (calm, measured, ~140 wpm)
3. Upload and name it (e.g., "Channel Narrator")
4. Note the `voice_id` — this goes into your pipeline config

---

## Project Folder Structure

Each video is a self-contained project folder:

```
yt video ideas/
├── video_assembler.py          ← the assembly script
├── style_card.txt              ← master prompt prefix (see strategy doc)
├── example_storyboard.json     ← template
│
├── projects/
│   ├── 001_roman_aqueducts/
│   │   ├── storyboard.json     ← scene list + metadata (~54 scenes)
│   │   ├── script.md           ← full narration script
│   │   ├── images/             ← AI-generated stills (~55 images)
│   │   │   ├── scene_01.png
│   │   │   └── ...
│   │   ├── images_4k/          ← upscaled versions (static scenes only)
│   │   │   └── ...
│   │   ├── clips/              ← AI-animated clips (~27 clips)
│   │   │   ├── scene_01_animated.mp4
│   │   │   └── ...
│   │   ├── particles/          ← particle overlay videos
│   │   │   ├── dust_overlay.mp4
│   │   │   └── sparks_overlay.mp4
│   │   ├── audio/
│   │   │   ├── voiceover.mp3
│   │   │   └── ambient.mp3
│   │   ├── output/
│   │   │   ├── final_video.mp4
│   │   │   └── thumbnail.png
│   │   └── metadata.json       ← title, description, tags for upload
│   │
│   ├── 002_mohenjo_daro/
│   │   └── ...
│   └── ...
│
└── assets/
    ├── style_anchors/           ← 8-10 reference images defining visual brand
    ├── music/                   ← ambient background tracks (royalty-free)
    ├── particles/               ← reusable particle overlay clips
    └── fonts/                   ← custom fonts for text overlays
```

---

## The Storyboard JSON Schema

This is the contract between the script stage and the assembly stage:

```json
{
  "base_dir": "./projects/001_roman_aqueducts",
  "voiceover": "audio/voiceover.mp3",
  "background_music": "audio/ambient.mp3",
  "music_volume": 0.08,
  "scenes": [
    {
      "image": "images/scene_01.png",
      "type": "animated",
      "animated_clip": "clips/scene_01_animated.mp4",
      "duration": 8,
      "texts": [
        { "text": "The Pont du Gard", "start": 1, "end": 4, "position": "center" },
        { "text": "50 km of gravity-fed water flow", "start": 4.5, "end": 7.5, "position": "bottom" }
      ],
      "scene_type": "establishing",
      "animation_prompt": "subtle parallax, clouds drifting, water visible in channel",
      "narration_segment": "In 19 BCE, Roman engineers completed something..."
    },
    {
      "image": "images/scene_02.png",
      "type": "static",
      "duration": 14,
      "motion": "pan_right",
      "texts": [
        { "text": "Three tiers of arches", "start": 2, "end": 7, "position": "top" },
        { "text": "Each bearing the weight above", "start": 7.5, "end": 13, "position": "bottom" }
      ],
      "scene_type": "cross_section"
    },
    {
      "image": "images/scene_03.png",
      "type": "animated",
      "animated_clip": "clips/scene_03_animated.mp4",
      "duration": 7,
      "texts": [],
      "scene_type": "detail",
      "animation_prompt": "water flowing right-to-left through channel, subtle ripples"
    }
  ]
}
```

### Field Reference

> **Two-pass storyboard.** The storyboard is built in two passes so you lock the *story* before any visual prompts are written:
> - **Pass 1 — Narrative** (what you review first): the structural/story fields only. No generation prompts.
> - **Pass 2 — Generation** (added *after* you approve Pass 1): the image/animation prompts and file paths.
>
> The `Pass` column below shows when each field appears. The assembler ignores the prompt fields (`image_prompt`, `animation_prompt`) — they're instructions for the image/animation steps, not for assembly.

| Field | Pass | Type | Required | Description |
|:---|:---|:---|:---|:---|
| `type` | 1 | string | ✅ | `"animated"` or `"static"` |
| `duration` | 1 | number | ✅ | Scene duration in seconds. Animated: 6–10s, Static: 10–15s |
| `scene_type` | 1 | string | ❌ | `establishing`, `cross_section`, `map`, `detail`, `scale_comparison` |
| `motion` | 1 | string | ❌ | Ken Burns motion for static scenes: `zoom_in`, `zoom_out`, `pan_left`, `pan_right`, `pan_up`, `zoom_detail` |
| `focus_x`, `focus_y` | 1 | number | ❌ | For `zoom_detail` only (0.0–1.0, default center) |
| `texts` | 1 | array | ❌ | Array of text objects: `[{"text": "...", "start": 2, "end": 6, "position": "bottom"}]`. Set to `[]` for no text |
| `narration_segment` | 1 | string | ❌ | Narration text for this scene (reference only) |
| `image_prompt` | 2 | string | ❌ | Full still-image prompt (style card + subject + accent + composition). Added after Pass 1 approval. |
| `image` | 2 | string | ✅* | Relative path to the generated scene image (*required at assembly time) |
| `animation_prompt` | 2 | string | ❌ | Prompt for Kling AI (used during the animation step) |
| `animated_clip` | 2 | string | ❌ | Path to AI-animated clip (required when type=animated, at assembly time) |
| `particle_overlay` | 2 | string | ❌ | Path to particle overlay clip (dust, sparks, rain) |

---

## Video Assembly

### Running the Assembler

```bash
cd "/Users/mritunjaymohitesh/dev/yt video ideas"

python video_assembler.py \
  --storyboard ./projects/001_roman_aqueducts/storyboard.json \
  --output ./projects/001_roman_aqueducts/output/final_video.mp4
```

### What the Assembler Does

For each scene in the storyboard:
1. Loads the image and scales it up (adds zoom headroom)
2. Applies the specified Ken Burns motion (or auto-cycles through motions)
3. Adds staggered/timed text overlays with semi-transparent dark background bars based on the `texts` array
4. Applies 0.5-second crossfade to next scene

After all scenes:
5. Concatenates all scene clips
6. Mixes voiceover audio (full volume)
7. Mixes background music (8% volume by default)
8. Exports as 1080p h264 MP4

### Motion Types

| Motion | Effect | Best for |
|:---|:---|:---|
| `zoom_in` | Slow zoom into center | Establishing shots, wide views |
| `zoom_out` | Start tight, pull back | Reveals, "big picture" moments |
| `pan_left` | Slide right → left | Timelines, sequences |
| `pan_right` | Slide left → right | Following a path, flow |
| `pan_up` | Slide bottom → top | Tall structures, vertical reveals |
| `zoom_detail` | Zoom into specific point (x, y) | Callouts, mechanism close-ups |

---

## Image Generation

### AI Image Prompt Structure

Every image prompt follows this pattern:

```
[STYLE CARD PREFIX]

Scene type: [establishing / cross_section / map / detail / scale_comparison]
Subject: [specific description of what to illustrate]
Civilization accent color: [hex from color system]
Composition: [specific framing instructions]
```

### Style Card (Prepend to Every Prompt)

```
Isometric flat-design technical illustration. Clean vector aesthetic, 
warm parchment background (#F5F0E8), precise geometric lines, 
charcoal dark elements (#2C2C2C). Architectural cross-section style.
Warm golden-hour ambient lighting with soft directional shadows.
No humans visible (or tiny silhouettes for scale only). 
No text in image. High architectural precision. 
Educational diagram aesthetic. Quietly dramatic mood.
```

### Image Resolution

- **Generate at:** 2048×2048 (minimum) or the model's highest native resolution
- **Upscale to:** 4096×4096 before passing to the assembler
- **Why:** Ken Burns zooms crop into the image — low-res source = blurry zoom

Upscaling options:
- Real-ESRGAN (free, local, `pip install realesrgan`)
- Topaz Gigapixel AI (paid, best quality)
- Nano Banana's built-in upscaler (if available via API)

### Style Consistency — Three Tiers

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

**Tier 3: LoRA Fine-Tuning (add after ~5–8 videos, once you have 20–30 "keeper" images)**
- Train a custom LoRA on Flux using 20–30 of your best on-brand images
- One-time cost: ~$5–$10 on Replicate, ~30 min training
- This is the strongest lever for *cross-video* brand consistency (every future video inherits the exact look)
- Consistency: ~95%+

> **Reality check on the AI-visual dependency:** you're right that you can't hand-animate — and you don't need to. The pipeline is built so AI does what it's genuinely reliable at: (1) generating consistent stills (anchors + LoRA make this a solved-enough problem in 2026), and (2) adding *subtle* motion (parallax, flowing water, drifting dust) to those stills via Kling — image-to-video's strongest, most dependable mode. The risky "full character animation" is never attempted. And because of graceful degradation (any scene can fall back to Ken Burns + text overlay, pure ffmpeg), **the worst realistic case is a Simple-History-style video of clean stills with motion overlays — still perfectly shippable.** You are not betting the channel on any single AI tool behaving perfectly.

---

## Voice Generation

### Primary: record your own narration (from day 1)

Recording ~10–12 minutes of narration for 2 videos/month is a trivial time cost (~20–30 min/video including cleanup) and is the single strongest authenticity + differentiation signal you can send. This is the default.

**Workflow:**
1. Read the **fact-checked, perspective-added** script into a USB condenser mic (~₹4,000) in a quiet room.
2. One or two takes; drop obvious flubs.
3. Clean up with Audacity or Adobe Podcast (free) — noise removal, light leveling.
4. Export `voiceover.mp3` → `projects/XXX/audio/`.
5. **Tick the "Altered content" box on upload** if the video uses AI-generated visuals prominently (it does), and always if any AI-voice pickups are spliced in.

**Narration settings to aim for (documentary style):** calm, measured, ~140–150 wpm, curious not lecturing.

### Fallback only: ElevenLabs clone for pickups

Keep a clone of *your own* voice for surgical fixes — a mispronounced name, a sentence you changed post-recording — so you don't re-record a whole session. Splice sparingly. **This is a convenience tool, never the narration source.** If it becomes the default, you've drifted into the "AI narration without human context" profile YouTube demonetizes.

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="sk_...")

# Pickup line only — e.g., re-recording a single sentence you changed.
audio = client.text_to_speech.convert(
    voice_id="your_cloned_voice_id",
    text=pickup_sentence,
    model_id="eleven_multilingual_v2",
    voice_settings={
        "stability": 0.7,        # higher = more consistent
        "similarity_boost": 0.8,  # higher = more like your sample
        "style": 0.3,            # lower = more neutral/documentary
    }
)

with open("pickup_01.mp3", "wb") as f:
    f.write(audio)
```

### Voice Settings for Documentary Style

| Setting | Value | Why |
|:---|:---|:---|
| Stability | 0.7 | Consistent tone, slight natural variation |
| Similarity Boost | 0.8 | Sounds like you, not generic |
| Style | 0.2–0.3 | Calm and measured, not dramatic |
| Speed | 0.9–1.0 | Slightly slower than default for clarity |

---

## Per-Video Cost Breakdown (50% Animation)

| Component | Unit Cost | Quantity | Total |
|:---|:---|:---|:---|
| Script draft (Claude via Pro plan) | Included in sub | 1 | $0.00 |
| Images (Nano Banana / Gemini) | ~$0.02/image | 55 + ~20 retries | ~$1.50 |
| AI animation (Kling AI) | ~$0.15/clip | 27 clips + ~10 retries | ~$5.55 |
| Upscaling (Real-ESRGAN, local) | $0.00 | 27 static scenes | $0.00 |
| Voice (self-recorded) | $0.00 | 1 | $0.00 |
| Particle overlays (stock) | $0.00 | ~10 | $0.00 |
| ffmpeg/moviepy assembly | $0.00 | 1 | $0.00 |
| Background music (royalty-free) | $0.00 | 1 | $0.00 |
| **Cash cost per video** | | | **~$7.00** |
| ⏱️ **Your time per video** (the real cost) | | ~5–7 hrs | *research + fact-check + narration + QA* |

> **The dollar cost is trivial; your time is the binding constraint.** "$7/video" is honest on cash but the true cost is the 5–7 hours of research, verification, narration, and QA — which is exactly the human effort that makes the video monetizable and good. Never optimize the $7 at the expense of that time.

### Monthly Cost Summary (at 2 videos/month)

| Expense | Cost |
|:---|:---|
| Claude Pro (orchestrator + script drafts) | ₹2,000/mo |
| Kling AI (entry plan, ~54 clips/mo incl. retries) | ~₹1,000–1,500/mo |
| Google AI Studio images (~150/mo — within/near free tier) | Free–low |
| ElevenLabs (optional, pickup fallback only) | Free tier or skip |
| Self-recorded voice, ffmpeg/moviepy, royalty-free music | Free |
| **Total** | **~₹3,000–3,500/mo (~$40)** |

> At 2 videos/month you generate ~110 images and ~54 clips — comfortably inside Pro-tier + a modest Kling plan. **This is the whole reason no self-hosted GPU model is warranted:** the variable cost is already ~₹1,500/mo. Self-hosting Wan/Hunyuan on RunPod (~$2.4–2.9/hr) to shave that is a false economy until you're at 30+ videos/month.
>
> ⚠️ **Gemini free-tier caveat:** if you ever scale cadence up, ~55 images × retries × N videos will blow past free-tier rate limits — budget for the paid image tier at that point.

---

## Production Workflow (2 videos/month)

Produce videos in a steady rhythm — one focused block per video, ~2 videos worth of work spread across the month. **Do not batch 4–6 in a weekend**; that guarantees either burnout or shallow fact-checking, and the templated-batch signature is what YouTube's inauthentic-content enforcement flags.

### Session 0: Research + Fact-Check (NEW — 2–4 hours, non-negotiable)

```
For the topic:
  → Gather real sources (books, papers, museum/engineering references), not just AI summary
  → Claude drafts the script from your research notes
  → YOU verify every date, tonnage, mechanism, name, and attribution against sources
  → YOU rewrite the hook + 2–3 paragraphs with your own engineering perspective
  → This step is what makes the video authentic, accurate, and monetizable
```

### Session 1: Scripting / Storyboard (1–2 hours)

```
For the topic (using your fact-checked research notes from Session 0):
  → Open Claude Desktop
  → Prompt: "Using these research notes, write a 10-min script about [topic].
     Output storyboard.json with ~54 scenes, tagging ~27 'animated' and ~27 'static'."
  → Claude generates script + storyboard
  → Save to projects/XXX/storyboard.json + script.md
  → You've already fact-checked in Session 0 — here you polish the hook and
    your perspective paragraphs so they're in your voice, not the LLM's.
```

### Session 2: Image Generation (1–2 hours, can run while doing other work)

```
For the project:
  → Open Claude Desktop
  → Prompt: "Generate all images for storyboard.json in projects/XXX/,
     passing anchor_01.png as style reference on every call" (see Style Consistency below)
  → Claude calls Gemini MCP ~55x
  → Review images: accept or regenerate (flag style inconsistencies)
  → Upscale accepted static-scene images to 4K
```

### Session 3: Animation (2–3 hours, semi-automated)

```
For the project:
  → For each "animate" scene in storyboard (~27):
     → Upload still to Kling AI (web UI or API)
     → Set animation prompt from storyboard
     → Generate 5–8 second clip
     → Review: accept or regenerate
     → GRACEFUL DEGRADATION: if a clip won't come out right after ~2 tries,
       retag that scene as "static" and let it be Ken Burns + overlay. A clean
       Ken Burns scene beats a glitchy animation, and you always ship.
     → Save to projects/XXX/clips/
  → Tip: queue all animations at once, review after all complete
```

### Session 4: Voice Recording (~30 min)

```
For the project:
  → Record narration yourself into your mic (see Voice Generation section)
  → Clean up in Audacity / Adobe Podcast
  → (Optional) splice in ElevenLabs clone pickups for any changed lines
  → Save voiceover.mp3 to projects/XXX/audio/
```

### Session 5: Assembly (automated, ~8 min)

```bash
python video_assembler.py \
  --storyboard "./projects/XXX/storyboard.json" \
  --output "./projects/XXX/output/final_video.mp4"
```

### Session 6: QA + Disclosure + Publish

```
For the video:
  → Watch it FULLY (not 2x) at least once — you're checking facts and feel, not just glitches
  → Check: animation glitches, audio errors, factual claims, on-screen text
  → On upload: TICK the "Altered content" checkbox (AI-assisted visuals/voice) — required
  → Write title (per formula) + description + tags
  → Publish/schedule on your consistent day/time (e.g., Saturday AM US)
```

**Time per video:** ~5–7 hours end to end, spread across the two-week cycle. Two videos ≈ 10–14 hours/month — sustainable alongside a full-time job.

---

## File Reference

| File | Location | Purpose |
|:---|:---|:---|
| `video_assembler.py` | `/Users/mritunjaymohitesh/dev/yt video ideas/video_assembler.py` | Main assembly script |
| `example_storyboard.json` | `/Users/mritunjaymohitesh/dev/yt video ideas/example_storyboard.json` | Template storyboard |

---

*Last updated: July 6, 2026 — revised for 2 videos/month, self-recorded narration, mandatory fact-check + "Altered content" disclosure, graceful-degradation fallback, and reference-anchor/LoRA style consistency. No self-hosted GPU model needed at this volume. See `strategy_review.md`.*

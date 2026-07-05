# Video Pipeline Automation — Technical Reference

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                               │
│              Claude Desktop (Pro plan)                        │
│                                                               │
│  You type a topic. Claude handles everything via MCP tools:   │
│                                                               │
│  Step 1: Write script + storyboard.json (~54 scenes)          │
│  Step 2: Generate ~55 still images via Gemini MCP             │
│  Step 3: Tag 50% of scenes for AI animation                   │
│  Step 4: Generate voiceover via ElevenLabs MCP                │
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

| Field | Type | Required | Description |
|:---|:---|:---|:---|
| `image` | string | ✅ | Relative path to the scene image |
| `type` | string | ✅ | `"animated"` or `"static"` |
| `duration` | number | ✅ | Scene duration in seconds. Animated: 6–10s, Static: 10–15s |
| `animated_clip` | string | ❌ | Path to AI-animated clip (required when type=animated) |
| `animation_prompt` | string | ❌ | Prompt for Kling AI (used during animation step) |
| `motion` | string | ❌ | Ken Burns motion for static scenes: `zoom_in`, `zoom_out`, `pan_left`, `pan_right`, `pan_up`, `zoom_detail` |
| `texts` | array | ❌ | Array of text objects: `[{"text": "...", "start": 2, "end": 6, "position": "bottom"}]`. Set to `[]` for no text |
| `focus_x`, `focus_y` | number | ❌ | For `zoom_detail` only (0.0–1.0, default center) |
| `scene_type` | string | ❌ | `establishing`, `cross_section`, `map`, `detail`, `scale_comparison` |
| `narration_segment` | string | ❌ | Narration text for this scene (reference only) |
| `particle_overlay` | string | ❌ | Path to particle overlay clip (dust, sparks, rain) |

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

**Tier 1: Prompt Prefix (start here)**
- Prepend the style card to every generation
- Consistency: ~70–80%
- Effort: zero — just copy-paste the prefix

**Tier 2: Reference Image Conditioning (add at month 2–3)**
- Generate 8–10 "anchor" images that define your visual identity
- Pass one anchor image as a style reference with every new generation
- Consistency: ~85–90%

```python
response = client.generate_image(
    model="nano-banana-2-lite",
    prompt=f"{STYLE_CARD}\n\n{scene_prompt}",
    reference_images=["./assets/style_anchors/anchor_01.png"],
    style_strength=0.7
)
```

**Tier 3: LoRA Fine-Tuning (add when committed to 50+ videos)**
- Train a custom LoRA on Flux using 20–30 of your best images
- One-time cost: ~$5–$10 on Replicate, ~30 min training
- Consistency: ~95%+

---

## Voice Generation

### With ElevenLabs Voice Clone

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="sk_...")

audio = client.text_to_speech.convert(
    voice_id="your_cloned_voice_id",
    text=full_narration_script,
    model_id="eleven_multilingual_v2",
    voice_settings={
        "stability": 0.7,        # higher = more consistent
        "similarity_boost": 0.8,  # higher = more like your sample
        "style": 0.3,            # lower = more neutral/documentary
    }
)

with open("voiceover.mp3", "wb") as f:
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
| Script (Claude via Pro plan) | Included in sub | 1 | $0.00 |
| Images (Nano Banana, free tier) | ~$0.02/image | 55 + ~20 retries | ~$1.50 |
| AI animation (Kling AI) | ~$0.15/clip | 27 clips + ~10 retries | ~$5.55 |
| Upscaling (Real-ESRGAN, local) | $0.00 | 27 static scenes | $0.00 |
| Voice (ElevenLabs Creator) | Included in $11/mo plan | ~10K chars | ~$0.00 |
| Particle overlays (stock) | $0.00 | ~10 | $0.00 |
| ffmpeg/moviepy assembly | $0.00 | 1 | $0.00 |
| Background music (royalty-free) | $0.00 | 1 | $0.00 |
| **Total per video** | | | **~$7.00** |

*ElevenLabs Creator ($11/mo) includes 100K characters/month, enough for ~8 full 10-min narrations. Matches 2 videos/week cadence.

### Monthly Cost Summary

| Expense | Cost |
|:---|:---|
| Claude Pro (orchestrator) | ₹2,000/mo |
| ElevenLabs Creator | ~₹920/mo ($11) |
| Kling AI Pro plan | ~₹2,350/mo ($28) |
| Google AI Studio (images) | Free tier |
| ffmpeg/moviepy | Free |
| Background music (Pixabay, etc.) | Free |
| **Total** | **~₹5,270/mo** (~$63) + ~$56 variable animation credits |
| **Effective total** | **~₹7,600/mo** (~$91) |

---

## Batch Production Workflow

For maximum efficiency, batch-produce 4–6 videos in a single weekend session:

### Session 1: Scripting (2–3 hours, one sitting)

```
For each of 4–6 topics:
  → Open Claude Desktop
  → Prompt: "Write a 10-min script about [topic]. Output storyboard.json with ~54 scenes,
     tagging ~27 as 'animated' and ~27 as 'static'."
  → Claude generates script + storyboard
  → Save to projects/XXX/storyboard.json + script.md
  → Quick 2-min review of facts/claims per script
```

### Session 2: Image Generation (1–2 hours, can run while doing other work)

```
For each project:
  → Open Claude Desktop
  → Prompt: "Generate all images for storyboard.json in projects/XXX/"
  → Claude calls Gemini MCP ~55x per video
  → Review images: accept or regenerate (flag inconsistencies)
  → Upscale accepted static-scene images to 4K
```

### Session 3: Animation (2–3 hours, semi-automated)

```
For each project:
  → For each "animate" scene in storyboard (~27 per video):
     → Upload still to Kling AI (web UI or API)
     → Set animation prompt from storyboard
     → Generate 5–8 second clip
     → Review: accept or regenerate
     → Save to projects/XXX/clips/
  → Batch tip: queue all 27 at once, review after all complete
```

### Session 4: Voice Generation (30 min)

```
For each project:
  → Paste narration script into ElevenLabs (or API call)
  → Download voiceover.mp3
  → Save to projects/XXX/audio/
```

### Session 5: Assembly (automated, ~8 min per video)

```bash
# Batch assemble all projects
for dir in projects/*/; do
  python video_assembler.py \
    --storyboard "$dir/storyboard.json" \
    --output "$dir/output/final_video.mp4"
done
```

### Session 6: QA + Schedule (2 min per video)

```
For each video:
  → Watch at 2x speed (5 min → 2.5 min viewing)
  → Check: animation glitches, voice errors, factual claims
  → Upload via YouTube Studio or YouTube Data API
  → Schedule: Tuesday + Friday, optimized for US morning
```

**Total time for 4–6 videos:** ~8–12 hours once, then drip-publish over 2–3 weeks.

---

## File Reference

| File | Location | Purpose |
|:---|:---|:---|
| `video_assembler.py` | `/Users/mritunjaymohitesh/dev/yt video ideas/video_assembler.py` | Main assembly script |
| `example_storyboard.json` | `/Users/mritunjaymohitesh/dev/yt video ideas/example_storyboard.json` | Template storyboard |

---

*Last updated: July 5, 2026*

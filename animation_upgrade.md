# Animation Strategy: 50% Animated from Day 1

> **Revised context (July 6, 2026 — see `strategy_review.md`):**
> - **The old cadence contradiction is resolved.** This doc's "quality from day 1, slower output" now *agrees* with the strategy doc, because cadence dropped to **2 videos/month**. At that pace you have ample time for 50% animation without it fighting a publishing treadmill. Quality is the whole point.
> - **Graceful degradation is built in.** Any scene tagged "animated" can fall back to Ken Burns + text overlay (pure ffmpeg, zero AI) if the AI animation won't come out right. Worst realistic case: a clean stills-plus-motion-overlay video, still fully shippable. You're never betting the channel on one AI tool.
> - **No self-hosted GPU model (Wan/Hunyuan on RunPod/Modal).** At ~54 clips/month, Kling on an entry plan (~₹1,000–1,500/mo) is cheaper *in total cost of ownership* than the tens of engineering hours self-hosting would demand — and open models render your flat/isometric style worse than photoreal styles. Revisit only at 30+ videos/month.

## What Dinzo and Bound Actually Do (It's Not What You Think)

These channels do NOT use frame-by-frame character animation. That would cost $500–$5,000 per minute and take weeks. What they actually use is **6 layers of motion on top of illustrated stills** — and most of these layers are now automatable with AI.

### The 6 Animation Layers

Watch any Dinzo or Bound video carefully and you'll see the same tricks repeating:

```
Layer 6: Animated text / callouts          ← After Effects or moviepy
Layer 5: Particle effects                  ← AI-animated (dust, rain, sparks)
Layer 4: Element animation                 ← AI-animated (water flowing, fire, smoke)
Layer 3: Character micro-movement          ← AI image-to-video (subtle breathing, head tilt)
Layer 2: Parallax depth (2.5D)             ← Layer separation + depth camera
Layer 1: Ken Burns pan/zoom (base)         ← ffmpeg zoompan (what we already have)
```

**Layer 1** is what our current pipeline does. Channels like Dinzo use **Layers 1–4 consistently** and **Layers 5–6 selectively**. That's the gap.

Here's what each layer actually is and how hard it is:

---

### Layer 1: Ken Burns Pan/Zoom ✅ ALREADY BUILT
**Difficulty:** Easy (automated in video_assembler.py)
**Cost:** $0 (ffmpeg)

What we already have. Slow zoom, pan across image. Every faceless channel does this minimum.

**The Golden Rule for Ken Burns:**
15 seconds of *just* a slow zoom feels dead. Viewer attention drops hard after ~8 seconds of the same visual with no change. Therefore:
- **Pure unadorned Ken Burns** should be capped at ~8 seconds max.
- **10–15s of Ken Burns WITH layered changes** works great. A "static" scene means the base image uses Ken Burns, but you layer on top of it. No visual element should stay unchanged for more than 5 seconds.
- In a 10–15s scene, stack 2–3 visual changes: text appearing/disappearing, arrow/callout animating in, or particle overlays.

---

### Layer 2: Parallax Depth (2.5D) — THE BIGGEST UPGRADE
**Difficulty:** Medium → Easy with AI depth tools
**Cost:** ~$0.02–$0.05 per scene

This is the single trick that makes Dinzo and Bound look "animated" when they're really not. The illusion:

1. Take a still image
2. AI separates it into **foreground** and **background** layers (depth estimation)
3. AI fills in the hidden area behind the foreground (inpainting)
4. Move the foreground slightly faster than the background
5. Result: a 3D depth illusion from a 2D image

**How to do it in 2026:**

| Tool | How it works | Cost |
|:---|:---|:---|
| **Kling AI** (image-to-video) | Upload still → prompt "subtle parallax camera movement" → 5-second animated clip | ~$0.10–$0.25/clip |
| **Runway Motion Brush** | Paint foreground → assign motion direction → background stays still | ~$0.15–$0.30/clip |
| **DepthAnything v2** (open source) | Generate depth map → split layers in Python → composite in moviepy | Free (local GPU needed) |
| **After Effects** (manual) | Import depth map as displacement map, apply camera with 3D layers | $23/mo (Adobe sub) |

**For your pipeline (50/50 animated/static from day 1):**
- Use **Kling AI image-to-video** for hero scenes (establishing shots, dramatic moments, water/fire/smoke) — ~25–28 scenes per video
- Use **Ken Burns** for informational scenes (diagrams, maps, text-heavy cross-sections) — ~25–28 scenes per video
- Blend: alternate between "alive" animated shots and "informational" static shots — the contrast makes both hit harder

---

### Layer 3: Character/Object Micro-Movement
**Difficulty:** Easy with AI image-to-video
**Cost:** ~$0.10–$0.25 per clip

This is the "breathing" effect — a character's cape flutters slightly, a flag waves, a torch flickers. The still image is 95% static, but one or two elements have subtle motion. It makes the scene feel *alive* without full animation.

**How to do it:**
- Generate your still image
- Upload to Kling AI or Runway
- Prompt: "subtle movement, [specific element] gently moves, camera mostly static"
- Output: 5-second animated clip that looks hand-animated

**Examples for your engineering content:**
- Water gently flowing through an aqueduct cross-section
- Smoke rising from a Roman forge
- Dust particles floating in a beam of light inside a temple
- A flag on a distant tower fluttering
- Construction pulleys gently swaying

---

### Layer 4: Element Animation (Water, Fire, Smoke)
**Difficulty:** Easy with AI — these elements are what AI does BEST
**Cost:** Same as Layer 3 (~$0.10–$0.25/clip, combined)

AI video models are *incredibly good* at physics-based elements: flowing water, flickering fire, rising smoke, falling rain. These are the easiest things to add because they require no character consistency — fire doesn't have a "face" that drifts.

**Tool of choice: Runway Motion Brush**
- Upload your still illustration
- Paint ONLY the water/fire/smoke area
- Set motion direction (downward for water, upward for fire)
- Everything else stays perfectly still
- Result: a professional-looking animated illustration

This is the highest bang-for-buck animation upgrade for engineering content because your scenes naturally contain water (aqueducts), fire (forges), smoke (factories), and flowing material (grain supply chains).

---

### Layer 5: Particle Effects
**Difficulty:** Easy (can be done in post with simple compositing)
**Cost:** $0 (stock particle overlays are free)

Floating dust, falling snow, rain, sparks, embers — these are simply transparent video overlays composited on top of your scene. They're not AI-generated; they're stock footage elements blended in post.

**How to do it:**
1. Download free particle overlays (Pixabay, Pexels, or generate with After Effects)
2. In moviepy or After Effects, overlay the particle video with "screen" or "add" blend mode
3. Adjust opacity to ~20–30% for subtle effect

This is surprisingly effective for engineering content: dust in ancient construction sites, sparks from metalworking, embers from fires, rain on outdoor scenes.

---

### Layer 6: Animated Text and Callouts
**Difficulty:** Easy (already partially in our pipeline)
**Cost:** $0 (moviepy/After Effects)

Text that flies in, arrows that draw themselves, numbers that count up, labels that fade in with a highlight effect. This is standard motion graphics — no AI needed, just keyframe animation.

Our `video_assembler.py` already handles basic text overlays. For more complex animated callouts (arrows drawing paths, numbers counting), you'd add After Effects or upgrade the moviepy script.

---

## Scene Count Math: Why 50–55, Not 35

With 50% animation, animated clips tend to be shorter (5–8 seconds from Kling AI) while static Ken Burns scenes stretch longer (10–15 seconds). You need more total scenes to fill 10–12 minutes:

| Mix | Animated scenes | Static scenes | Total duration | Total scenes |
|:---|:---|:---|:---|:---|
| 50/50 at 7s/13s avg | 27 × 7s = 189s | 27 × 13s = 351s | **540s (9 min)** | 54 |
| 50/50 at 7s/14s avg | 27 × 7s = 189s | 27 × 14s = 378s | **567s (9.5 min)** | 54 |
| 50/50 at 8s/14s avg | 26 × 8s = 208s | 26 × 14s = 364s | **572s (9.5 min)** | 52 |
| **Target** | **~27 animated** | **~27 static** | **~600s (10 min)** | **~54** |

**Target: 50–55 scenes per video.** Generate 50–55 still images, animate ~27 of them via Kling AI, apply Ken Burns to the remaining ~27.

> [!IMPORTANT]
> **Default animated clips to 6s.** Duration is the main Kling cost lever — a 10s clip costs ~2× a 6s one, and the 6s bias is what keeps 2 videos/month inside the 3,000-credit Pro plan (see [docs/costs.md](docs/costs.md)). You *can* run longer — pick a 10s duration, or chain "extend" onto a 6s clip — but treat that as a deliberate, per-scene spend, not the default. Longer clips also mean fewer scenes (~45–50) for the same runtime.
>
> **Fallback:** any animated scene that fails the accuracy gate's scrub-check twice is retagged `type:"static"` and covered by Ken Burns. That fallback is accurate by construction (it IS the validated still) and free — a clean Ken Burns scene beats a third paid Kling roll.

---

## Production Targets (Day 1 Baseline)

**50% animated from launch. No tiered upgrade — establish quality from the start.**

For a 10-minute video with ~54 scenes:
- **~27 scenes:** AI-animated (Kling AI / Runway — parallax, element animation, micro-movement)
- **~27 scenes:** Ken Burns with text overlays (diagrams, maps, cross-sections, data displays)
- **+ particle overlays** on ~10 scenes for atmosphere (dust, sparks, rain — free stock composites)
- **+ animated text/callouts** on ~15 scenes (moviepy/After Effects)

**Cost per video:**
| Component | Unit Cost | Quantity | Total |
|:---|:---|:---|:---|
| Still images (Nano Banana) | ~$0.02 | 55 + ~20 retries | ~$1.50 |
| AI animation (Kling) | ~$0.15 | 27 clips + ~10 retries | ~$5.55 |
| Voice (ElevenLabs) | included in $11/mo plan | 1 | ~$0.00 |
| Particle overlays | $0.00 (stock) | 10 | $0.00 |
| Assembly (ffmpeg/moviepy) | $0.00 | 1 | $0.00 |
| **Total per video** | | | **~$7.00** |

**Monthly cost at 2 videos/month:** ~$14 in animation + image credits, plus ₹2,000 Claude Pro (self-recorded voice = free) = **~₹3,000–3,500/month** (~$40). The low cadence is exactly what keeps this cheap and keeps you inside entry-tier limits.

### Growth path (quality, not quantity):

| Stage | % animated | Feel | Cost/video |
|:---|:---|:---|:---|
| ✅ **Day 1 baseline** | **50%** (27 of 54) | **"Animated channel"** — matches Dinzo/Bound | **~$7** |
| 🔜 Month 3+ | 60% | "High production" — add more element animation | ~$9 |
| 🔜 Month 6+ | 70%+ | "Near Kurzgesagt" — most scenes have motion | ~$12 |

---

## Pipeline Architecture (Day 1)

```
Step 1: SCRIPT + STORYBOARD                    ← Claude Desktop
  └─ ~54 scenes, each tagged: "animate" or "static"
  └─ Animated scenes get an animation_prompt
  └─ Static scenes get a motion type (zoom_in, pan_right, etc.)

Step 2: IMAGE GENERATION                        ← Nano Banana via MCP
  └─ All ~55 images generated (+ ~20 retries)
  └─ Upscale static scenes to 4K for zoom headroom

Step 3: ANIMATION (50% of scenes)               ← Kling AI / Runway
  └─ For each "animate" scene (~27):
     └─ Upload still to Kling AI
     └─ Prompt: parallax + element motion
     └─ Download 5–8 sec animated clip
     └─ Extend if needed for longer scenes
  └─ For each "static" scene (~27):
     └─ Keep as still image (Ken Burns in assembly)

Step 4: PARTICLE OVERLAYS                       ← Stock composites
  └─ Select ~10 scenes for atmosphere
  └─ Apply dust/sparks/rain overlays in assembly

Step 5: VOICEOVER                               ← YOU record (mic + Audacity)
  └─ Fact-checked script → single audio file (AI clone = pickup fallback only)

Step 6: ASSEMBLY                                ← video_assembler.py
  └─ Static scenes: Ken Burns + text overlays
  └─ Animated scenes: import as video clips + text overlays
  └─ Particle overlays composited
  └─ Audio: voiceover + ambient music mixed
  └─ Crossfade transitions between all scenes
  └─ Export h264 MP4 — 1080p for review, --resolution 2160p for the 4K publish master

Step 7: QA + UPLOAD                             ← Manual (~2 min)
```

### What changes in the storyboard JSON:

```json
{
  "scenes": [
    {
      "image": "images/scene_01.png",
      "type": "animated",
      "animated_clip": "clips/scene_01_animated.mp4",
      "duration": 8,
      "texts": [
        { "text": "50 km of gravity-fed water flow", "start": 2, "end": 7, "position": "bottom" }
      ],
      "animation_prompt": "subtle parallax depth, water gently flowing through channel, dust particles in sunlight"
    },
    {
      "image": "images/scene_02.png",
      "type": "static",
      "duration": 14,
      "motion": "pan_right",
      "texts": [
        { "text": "Three tiers of arches", "start": 2, "end": 6, "position": "top" },
        { "text": "Each bearing the weight above", "start": 7, "end": 13, "position": "bottom" }
      ]
    }
  ]
}
```

---

## Which AI Animation Tool to Use

| Tool | Best for | Cost | API available? | Verdict |
|:---|:---|:---|:---|:---|
| **Kling AI 3.0** | Best overall image-to-video, maintains illustration style, good physics | ~$0.10–$0.25/clip | ✅ Yes | **Primary tool** — use for most animated scenes |
| **Runway Motion Brush** | Selective element animation (animate ONLY the water, keep rest still) | ~$0.15–$0.30/clip | ✅ Yes | **Precision tool** — use when you need only one element to move |
| **Google Veo 3.1** | Photorealistic motion, integrated with your existing Google stack | Varies | ✅ Yes (Vertex AI) | **Backup** — good but may not handle illustrated style as well |
| **Luma Dream Machine** | Quick, cheap, good for atmospheric/ambient motion | ~$0.05–$0.15/clip | ✅ Yes | **Budget option** — use for simple parallax |

**My recommendation:** Start with **Kling AI** as your primary animation tool. Its image-to-video mode handles illustrated/flat-design content well, maintains style consistency, and its API can be integrated into your pipeline. Use **Runway Motion Brush** for scenes where you need surgical control (e.g., animate ONLY the water in a cross-section while keeping the structure perfectly still).

---

## What This Looks Like in Practice

### Example: Roman Aqueduct scene breakdown

**Scene 1 — Establishing shot (ANIMATED)**
- Still image: wide isometric view of the Pont du Gard
- AI animation: subtle parallax, clouds drifting slowly, water visible in the channel at top
- Duration: 8 seconds
- Texts: [2s-7s] "Pont du Gard — 50 km of gravity-fed flow"

**Scene 2 — Cross-section (STATIC + Ken Burns + Layered Changes)**
- Still image: cutaway view of the arch structure
- Motion: slow pan right revealing the internal structure
- Duration: 14 seconds
- Texts: [2s-6s] "Three tiers of arches" (top), [7s-13s] "Each bearing the weight above" (bottom)
- *Why it works:* The base pans right, but the viewer's eye is refreshed by new text appearing midway through.

**Scene 3 — Water flow detail (ANIMATED)**
- Still image: close-up of the water channel at the top
- AI animation: water gently flowing right-to-left, subtle ripple effect
- Duration: 6 seconds
- Texts: none (let the visual speak)

**Scene 4 — Gradient diagram (STATIC + Ken Burns + Layered Changes)**
- Still image: side-view showing the 1:3000 gradient over 50 km
- Motion: slow zoom into the gradient detail
- Duration: 12 seconds
- Texts: [2s-6s] "A drop of just 17 meters", [7s-11s] "over 50 kilometers"

**Scene 5 — Scale comparison (ANIMATED)**
- Still image: aqueduct next to modern building for scale
- AI animation: subtle parallax depth, tiny birds flying in background
- Duration: 8 seconds
- Text overlay: "As tall as a 15-story building"

**Result:** 5 scenes, 44 seconds. 3 AI-animated + 2 Ken Burns. The alternation between "alive" and "informational" creates the perception that the whole video is animated.

---

## The Key Insight

Dinzo and Bound look fully animated, but they're not. They're using **selective AI animation on key moments** interleaved with simpler motion on informational scenes. The viewer's brain fills in the gap.

At 50% animation from day 1, your channel establishes itself as a **high-production animated channel** immediately — no "quality ramp" where early videos look worse than later ones. Every video in your library will hold up.

**The tradeoff is speed, not quality:** Early on, each video will take longer to produce (~4–6 hours total vs ~2 hours for pure Ken Burns). But the channel's identity is locked in from video #1, which is worth more than a few extra videos published early.

*Last updated: July 6, 2026 — revised: cadence contradiction resolved (2 videos/month makes 50% animation comfortable), graceful-degradation fallback added, self-recorded narration, no self-hosted GPU model needed. See `strategy_review.md`.*

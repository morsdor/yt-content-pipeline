# Animation Strategy: 50% Animated, Hand-Built in After Effects

> **Revised July 12, 2026 — the animation pivot.** This doc originally proposed generative
> image-to-video for the animated half of each video. That was tried at full-batch scale and
> failed the quality bar: ~70% of clips softened the crisp linework, warped precise geometry,
> or added uninvited camera moves — generative video models are realism-tuned, and flat
> isometric illustration is their weak case. Motion is now **hand-built in After Effects**
> over the validated AI stills + a reusable asset library. AE transforms the art but never
> redraws it, so scenes stay sharp and accurate *by construction*, and animation costs
> nothing at the margin. The practical how-to lives in
> [docs/after_effects_workflow.md](docs/after_effects_workflow.md); this doc is the *why*
> and the *what*.

## What Dinzo, Bound and Oversimplified Actually Do (It's Not What You Think)

These channels do NOT use frame-by-frame character animation. That would cost $500–$5,000
per minute and take weeks. What they actually use is **layers of simple motion on top of
illustrated stills** — position, scale, rotation and puppet-pin keyframes on flat art.
Every layer of it is achievable by one person in AE, and most of it is *fast*.

### The 6 Animation Layers (all deterministic, all AE)

```
Layer 6: Animated text / callouts       ← assembler (video_assembler.py) or AE
Layer 5: Particle effects               ← stock overlays, Screen blend (assembler/AE)
Layer 4: Element animation              ← AE: water level, light sweep, smoke drift
Layer 3: Character motion               ← AE: puppet pins / Duik on library characters
Layer 2: Parallax depth (2.5D)          ← AE: separated layers, bg moves ~0.25× of fg
Layer 1: Ken Burns pan/zoom (base)      ← ffmpeg zoompan (static scenes, assembler)
```

**Layer 1** is what the assembler does unaided. The animated half of each video adds
**Layers 2–4 in AE** (and later 3 for characters); 5–6 are compositing, not animation.
Mapped to the learning ladder in the AE workflow doc: Rung 1 = camera moves (a scaled-up
Layer 1 done *with easing and taste*), Rung 2 = Layer 2, Rung 3 = Layers 3–4.

**The Golden Rule for Ken Burns (unchanged):**
15 seconds of *just* a slow zoom feels dead. Viewer attention drops hard after ~8 seconds
of the same visual with no change. Therefore:
- **Pure unadorned Ken Burns** capped at ~8 seconds.
- **10–15s scenes need layered changes** — text appearing, a callout animating in, a
  particle overlay. No visual element unchanged for more than ~5 seconds.

**Why AE wins for this style (the pivot's logic, kept short):**

| | Generative image-to-video | After Effects |
|:---|:---|:---|
| Line sharpness | softens/melts fine lines | pixel-exact — never redrawn |
| Geometry | can morph mid-motion | cannot change, by construction |
| Control | prompt roulette, paid retries | keyframe-exact, free retries |
| Marginal cost | credits per second, per attempt | ₹0 |
| Consistency | varies clip to clip | template comps = identical treatment |
| Cost of iteration | a charged re-roll | a Cmd+Z |

The trade is **your hands-on time** — controlled by three things: the motion briefs (no
figuring out what to build), the asset library (no re-making elements), and template comps
(scene #10 of a type takes ~15 minutes, not 2 hours).

---

## Scene Count Math: Why 50–55, Not 35

With 50% animation, animated clips run shorter (6–10 seconds of built motion) while static
Ken Burns scenes stretch longer (10–15 seconds). You need more total scenes to fill 10–12
minutes:

| Mix | Animated scenes | Static scenes | Total duration | Total scenes |
|:---|:---|:---|:---|:---|
| 50/50 at 7s/13s avg | 27 × 7s = 189s | 27 × 13s = 351s | **540s (9 min)** | 54 |
| 50/50 at 8s/14s avg | 26 × 8s = 208s | 26 × 14s = 364s | **572s (9.5 min)** | 52 |
| **Target** | **~27 animated** | **~27 static** | **~600s (10 min)** | **~54** |

**Target: 50–55 scenes per video.** Generate 50–55 still images, build ~27 in AE, apply
Ken Burns to the remaining ~27.

> [!IMPORTANT]
> **Duration is now a time-budget lever, not a cash lever.** A longer animated scene costs
> more of *your* build-and-render time, not credits. Bias animated scenes to 6–8s; go
> 10s+ only when the motion genuinely needs it (a route arrow crossing a map, a slow
> reveal). And **not every "animated" scene needs more than Rung 1** — a well-eased push-in
> IS an animated scene.
>
> **Fallback:** any scene not worth AE time this cycle is retagged `type:"static"` and
> covered by Ken Burns + overlays. The fallback is accurate by construction (it IS the
> validated still) and free — you always ship.

---

## Production Targets (Day 1 Baseline)

**50% animated from launch. No tiered upgrade — establish quality from the start.**

For a 10-minute video with ~54 scenes:
- **~27 scenes:** built in AE — every one gets an eased camera move; 3–5 hero scenes get parallax; 2–3 get element motion
- **~27 scenes:** Ken Burns with text overlays (diagrams, maps, cross-sections, data displays)
- **+ particle overlays** on ~10 scenes for atmosphere (dust, sparks, rain — free stock composites)
- **+ animated text/callouts** on ~15 scenes (assembler/AE)

**Cost per video:**

| Component | Unit Cost | Quantity | Total |
|:---|:---|:---|:---|
| Still images (Gemini 3.1 Flash Image) | ~₹7.4/image | ~54 + gate regens | ~₹450 |
| New library assets (amortizing toward zero) | ~₹7.4/asset | ~5–15 after video 1 | ~₹50–110 |
| AE animation | ₹0 marginal (sub below) | 27 scenes | ₹0 |
| Voice (self-recorded), particles, assembly, music | ₹0 | | ₹0 |
| **Marginal cash per video** | | | **~₹500–560** |
| ⏱️ **Your time per video** (the real cost) | | **~10–14 hrs** | *incl. the 3–5 hr AE session; falls toward 8–10 as templates accumulate* |

**Monthly at 2 videos:** ~₹1,000 in generation + Claude Pro ₹2,000 + **After Effects
~₹2,000 (~$23 single-app)** ≈ **~₹5,000/month.** DaVinci Resolve (Fusion) is the free
alternative while trialing — the concepts transfer 1:1.

### Growth path (quality, not quantity):

| Stage | Capability | Feel |
|:---|:---|:---|
| ✅ **Day 1** | Rung-1 camera moves on all animated scenes + overlays | Clean, crafted — already beats generative slop |
| 🔜 Month 2 | + parallax hero scenes, element motion, first rigged character | "Animated channel" — matches Dinzo/Bound |
| 🔜 Month 3+ | + Duik walk cycles, Oversimplified-style map sequences | "High production" — most scenes have designed motion |

---

## Pipeline Architecture (Day 1)

```
Step 1: SCRIPT + STORYBOARD                    ← Claude
  └─ ~54 scenes, each tagged: "animated" or "static"
  └─ Animated scenes get an animation_prompt (the MOTION INTENT —
     what moves, how far, how slow)
  └─ Static scenes get a motion type (zoom_in, pan_right, etc.)

Step 2: IMAGE GENERATION                        ← Gemini (generate_images.py)
  └─ All ~55 images generated → ACCURACY GATE → upscale to 4K

Step 3: ANIMATION PREP                          ← Claude (free)
  └─ prompt_builder.py --motion-briefs → motion_briefs.md
  └─ Asset shopping list vs assets_library/INDEX.md → generate_asset.py
  └─ Layered plates for parallax scenes; JSX scaffolds in ae_scripts/

Step 4: THE AE SESSION                          ← YOU (3–5 hrs, falling)
  └─ Per brief, on the ladder: camera → parallax → element motion
  └─ Template comps: build a scene type once, swap art forever after
  └─ Render clips/scene_NN_animated.mp4 (native 4K)
  └─ Render QC (visual-accuracy-gate Layer 3): easing, restraint,
     cut discipline, asset consistency — fixes are free

Step 5: PARTICLE OVERLAYS                       ← Stock composites
Step 6: VOICEOVER                               ← YOU record
Step 7: ASSEMBLY                                ← video_assembler.py
  └─ 1080p review · --resolution 2160p publish master
Step 8: QA + UPLOAD                             ← Manual
```

### What this looks like in the storyboard JSON:

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
      "animation_prompt": "slow push-in; clouds drift right slowly; water surface breathes"
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

`animation_prompt` is intent, not implementation — `--motion-briefs` expands it into the
buildable AE direction (layer stack, pixel distances, easing) with the scene's
`visual_facts` as hold-constraints.

---

## What This Looks Like in Practice

### Example: Roman Aqueduct scene breakdown

**Scene 1 — Establishing shot (ANIMATED, Rung 1+2)**
- Base: wide isometric still of the Pont du Gard, plus a separated cloud layer
- Build: camera scale 100→105% eased over 8s; clouds drift right, far cloud at half speed
- Texts: [2s–7s] "Pont du Gard — 50 km of gravity-fed flow"

**Scene 2 — Cross-section (STATIC + Ken Burns + layered changes)**
- Slow pan right, 14s; new text appears midway — the viewer's eye is refreshed without AE work

**Scene 3 — Water flow detail (ANIMATED, Rung 3)**
- Base: close-up still of the channel; water band as its own layer
- Build: water layer position oscillates a few px (`loopOut("pingpong")`); subtle 6s push-in
- Texts: none (let the visual speak)

**Scene 4 — Gradient diagram (STATIC + Ken Burns + layered changes)**
- Slow zoom into the gradient detail, 12s, two timed callouts

**Scene 5 — Scale comparison (ANIMATED, Rung 2)**
- Base: aqueduct + modern building as separate layers over a shared background
- Build: gentle opposing parallax between the two subjects, 8s
- Text overlay: "As tall as a 15-story building"

**Result:** 5 scenes, 48 seconds. 3 AE-built + 2 Ken Burns. The alternation between
"alive" and "informational" creates the perception that the whole video is animated.

---

## The Key Insight

Dinzo, Bound and Oversimplified look fully animated, but they're not. They're using
**selective, well-crafted motion on key moments** interleaved with simpler motion on
informational scenes. The viewer's brain fills in the gap.

The pivot didn't change that thesis — it changed the *engine*. Deterministic AE motion is
what those channels actually use, and it's why their videos never melt, shimmer, or warp:
**the craft ceiling of transforms-on-sharp-art is higher than the quality floor of
generative video, and for an engineering channel the floor is what kills you.** Sharp,
accurate, restrained motion reads as *crafted*; impressive-but-wobbly motion reads as slop.

**The tradeoff is your time, not quality or money:** the first video's AE session will be
slow. Templates, the asset library, and the JSX scaffolds are what flatten the curve —
by design, every hour spent makes the next video faster.

*Last updated: July 12, 2026 — rewritten for the After Effects pivot (generative
image-to-video removed; layer model, scene math, and alternation insight retained).
Previous revision July 6, 2026 — see `strategy_review.md`.*

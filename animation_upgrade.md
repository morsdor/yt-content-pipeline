# Animation Strategy: Every Scene Hand-Built in After Effects

> **What this doc is.** The *why* and the *what* of the channel's motion approach — the
> reasoning, the history, and the targets. The *how-to* lives in
> [docs/after_effects_workflow.md](docs/after_effects_workflow.md) (the AE build) and
> [docs/production_workflow.md](docs/production_workflow.md) (where it sits in the pipeline);
> the scene contract is [docs/storyboard_schema.md](docs/storyboard_schema.md).
>
> **How we got here (two pivots).**
> - **Generative image-to-video — tried and dropped (Jul 12, 2026).** This doc originally
>   proposed generative i2v for the "animated" scenes. At full-batch scale ~70% of clips
>   softened the crisp linework, warped precise geometry, or added uninvited camera moves —
>   realism-tuned video models are weakest on flat isometric illustration. Motion is now
>   **hand-built in After Effects** over validated AI stills + a reusable asset library. AE
>   transforms the art but never redraws it, so scenes stay sharp *by construction* and
>   animation costs nothing at the margin.
> - **The studio pivot (Jul 13, 2026).** The old "50% animated / 50% Ken Burns" split is
>   gone: **every scene is an AE scene now**, from a bare eased camera push to a fully
>   layered shot. Richness is a *spectrum*, not a scene type. Scenes are directed by the
>   seven-pass **studio chain** (`studio-director`) into one `storyboard.json` v2,
>   timestamped to the pre-recorded VO, built in AE, and conformed in **Premiere Pro**.
>   `video_assembler.py` survives only as the animatic tool.
>
> The layer/rung analysis below — *why AE wins* — is the durable core and is unchanged.

## What Dinzo, Bound and Oversimplified Actually Do (It's Not What You Think)

These channels do NOT use frame-by-frame character animation. That would cost $500–$5,000
per minute and take weeks. What they actually use is **layers of simple motion on top of
illustrated stills** — position, scale, rotation and puppet-pin keyframes on flat art.
Every layer of it is achievable by one person in AE, and most of it is *fast*.

### The animation layers (all deterministic, all AE)

```
Layer 6: Animated text / callouts    ← AE (the animatic previews them)
Layer 5: Particle effects            ← stock overlays, Screen blend
Layer 4: Element animation           ← AE: water level, light sweep, smoke drift
Layer 3: Character motion            ← AE: puppet pins / Duik on library characters
Layer 2: Parallax depth (2.5D)       ← AE: separated layers, bg moves ~0.25× of fg
Layer 1: Camera move (base)          ← AE: eased push / pan on every scene
```

These map onto the AE build's **learning ladder**: Rung 1 = Layer 1 (a camera move done
*with easing and taste*, on every scene), Rung 2 = Layer 2 (parallax on hero scenes),
Rung 3 = Layers 3–4 (element / character motion, 2–3 scenes max). Layers 5–6 are
compositing, not animation. `video_assembler.py` only *approximates* Layer 1 in the
animatic (ffmpeg Ken-Burns on the still) so pacing is checkable before AE — the final
motion is always AE.

**The golden rule (attention decay):**
15 seconds of *just* a slow zoom feels dead — viewer attention drops hard after ~8 seconds
of the same visual with no change. Therefore:
- **A bare camera push** carries a scene for ~8 seconds, no more.
- **10–15s scenes need a layered change** — text appearing, a callout animating in, a
  particle overlay, an element that moves. No visual element sits unchanged for >~5 seconds.

**Why AE wins for this style (the pivot's logic, kept short):**

| | Generative image-to-video | After Effects |
|:---|:---|:---|
| Line sharpness | softens / melts fine lines | pixel-exact — never redrawn |
| Geometry | can morph mid-motion | cannot change, by construction |
| Control | prompt roulette, paid retries | keyframe-exact, free retries |
| Marginal cost | credits per second, per attempt | ₹0 |
| Consistency | varies clip to clip | template comps = identical treatment |
| Cost of iteration | a charged re-roll | a Cmd+Z |

The trade is **your hands-on time** — controlled by three things: the board (numeric motion
specs per scene, so there's nothing to figure out), the asset library (no re-making
elements), and template comps (scene #10 of a type takes ~15 minutes, not 2 hours).

---

## Scene Count: Why 60–80

Every scene is an AE scene, so the old "animated vs static" math is gone. Scenes run
**8–12 seconds** each and are timestamped to the recorded VO by the script-analyzer pass; a
10–13 minute video lands at **60–80 scenes**. More, shorter scenes keep the eye moving (the
golden rule) and give the edit more cut points to land on narration beats.

Richness is a spectrum across those scenes, not a 50/50 split:

| Rung | What it adds | How many scenes |
|:---|:---|:---|
| **Rung 1 — camera** | eased push / pan (the board's `camera{}` numbers) | **every scene** |
| **Rung 2 — parallax** | 3–4 separated layers, bg at ~0.25× foreground | 3–5 hero scenes |
| **Rung 3 — element / character** | water level, light sweep, flag ripple, map arrow, gesture | 2–3 scenes max |

> **Duration is a time-budget lever, not a cash lever.** A longer or richer scene costs more
> of *your* build time, not credits. Bias scenes to ~8s; go 10s+ only when the motion needs
> it (a route arrow crossing a map, a slow reveal). **Not every scene needs more than Rung 1**
> — a well-eased push-in IS a finished, crafted scene.
>
> **Graceful degradation:** any scene not worth AE time this cycle ships as its Rung-1
> camera-only build. It's accurate by construction (it IS the validated plate) and free —
> you always ship.

**Cost stays tiny.** Images (~₹7.4 each, ~60 gens ≈ ₹450/video) are the only per-video cash;
AE animation is ₹0 marginal on a flat ~$23/mo subscription. Full breakdown:
[docs/costs.md](docs/costs.md).

---

## Where This Sits in the Pipeline

The full operating sequence lives in
[docs/production_workflow.md](docs/production_workflow.md); in one glance:

```
studio chain (7 passes) → storyboard.json v2          ← Claude, ₹0
  → record VO + true-up the scene timings             ← you
  → generate plates → accuracy gate → upscale 4K      ← Gemini + you
  → animatic (video_assembler.py) → fix pacing IN THE BOARD
  → AE build on the ladder → render clips/scene_NN.mp4 (native 4K)   ← you
  → conform in Premiere Pro → QA → publish
```

The board arrives finished: every scene carries numeric `camera{}` + `layers[].motion{}`
specs (motion-director pass) and an `ae_build{}` blueprint (ae-director pass). **The board
IS the brief** — there is no separate motion-brief step anymore. The scene contract is
[docs/storyboard_schema.md](docs/storyboard_schema.md).

---

## What This Looks Like in Practice

### Example: a Roman-aqueduct scene run

**Scene 1 — Establishing shot (Rung 1 + 2)**
- Base: wide isometric still of the Pont du Gard, plus a separated cloud layer
- Build: camera scale 100→105% eased over 8s; clouds drift right, far cloud at half speed
- Text: [2s–7s] "Pont du Gard — 50 km of gravity-fed flow"

**Scene 2 — Cross-section (Rung 1 + timed text)**
- Slow eased pan right, 14s; a second callout appears midway — the eye is refreshed with no
  extra AE rig

**Scene 3 — Water-flow detail (Rung 3)**
- Base: close-up still of the channel; water band as its own layer
- Build: water layer position oscillates a few px (`loopOut("pingpong")`); subtle 6s push-in
- Text: none — let the visual speak

**Scene 4 — Gradient diagram (Rung 1 + callouts)**
- Slow eased zoom into the gradient detail, 12s, two timed callouts

**Scene 5 — Scale comparison (Rung 2)**
- Base: aqueduct + modern building as separate layers over a shared background
- Build: gentle opposing parallax between the two subjects, 8s
- Text: "As tall as a 15-story building"

**Result:** 5 scenes, 48 seconds — every one has an eased camera move; two add parallax, one
adds element motion. The alternation between "alive" and "informational" makes the whole
video read as animated.

---

## The Key Insight

Dinzo, Bound and Oversimplified look fully animated, but they're not. They use
**selective, well-crafted motion on key moments** interleaved with simpler motion on
informational scenes. The viewer's brain fills in the gap.

The pivot didn't change that thesis — it changed the *engine*. Deterministic AE motion is
what those channels actually use, and it's why their videos never melt, shimmer, or warp:
**the craft ceiling of transforms-on-sharp-art is higher than the quality floor of
generative video, and for an engineering channel the floor is what kills you.** Sharp,
accurate, restrained motion reads as *crafted*; impressive-but-wobbly motion reads as slop.

**The tradeoff is your time, not quality or money:** the first video's AE session will be
slow. Template comps, the asset library, and the JSX scaffolds are what flatten the curve —
by design, every hour spent makes the next video faster.

*Last updated July 22, 2026 — aligned to the studio chain + storyboard v2: scene count
60–80, the animated/static split and the old per-scene motion-brief step removed, cost and
pipeline now point to the canonical docs. Motion-approach history: generative i2v dropped
July 12, hand-built AE adopted; see `strategy_review.md` for the July 6 review that drove it.*

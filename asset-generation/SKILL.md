---
name: asset-generation
description: >-
  Use when generating a video's visual assets after the storyboard is approved —
  the full stills → validation → animation chain. Trigger on "generate the assets",
  "run asset generation", "make the images and clips", "animate the storyboard",
  or Phase 2–3 of an Engineering Atlas video. Runs generate_images.py for stills,
  enforces the visual-accuracy-gate before any animation spend, then drives the
  Kling MCP (file_upload → image_to_video → query_tasks) with cost confirmation,
  scrub-checks, one-retry rule, and Ken Burns fallback. Requires the Kling MCP
  connector and GEMINI_API_KEY in .env.
---

# Asset Generation — Stills → Gate → Animation

**What this produces:** `images/scene_NN.png` (~55 validated stills), `clips/scene_NN_animated.mp4` (~27 clips), an updated `assets_manifest.json`, and a validation report — everything Phase 5 (voice) and Phase 6 (assembly) need.

**The chain, in order — order is the budget protection:**

```
stills (cheap) → accuracy gate (free) → animation (expensive, charged per job)
```

Companion skills: [`visual-accuracy-gate`](../visual-accuracy-gate/SKILL.md) (invoked at two points below), `the-engineering-atlas-video` (the parent checklist).

---

## Stage 0 — Preflight (all must pass before anything is generated)

- [ ] **Storyboard is approved** (the parent skill's review gate passed). Scenes depicting the real structure carry `visual_facts` + `reference_image`; `references/` pack exists.
- [ ] `GEMINI_API_KEY` present in `.env` (repo root or project folder).
- [ ] **Kling MCP connected:** call `who_am_i` — confirms auth and returns the current tier's models/durations/args. Do not guess parameter values; use what it returns.
- [ ] **Credits check (BLOCKING):** call `query_membership_and_credits`. Estimate the batch: `python prompt_builder.py <sb> --anim-jobs` prints total seconds; at roughly 6 credits/second (verify against current tier) a ~27-clip batch at 6–10s needs **~1,500–2,200 credits**. If available credits < estimate, **STOP and tell the user** — do not submit a partial batch. (Free tier / 0 credits = stop here.)
- [ ] Style anchor decision: **video #1** → `style_card.txt` only (no anchors exist yet); **video #2+** → pass an anchor from `assets/style_anchors/` on every call.

## Stage A — Stills (`generate_images.py`)

```bash
SB=projects/NNN_topic/storyboard.json

# 1. Dry-run: verify the plan + one composed prompt, zero API calls
python generate_images.py --storyboard $SB --dry-run

# 2. Scene 1 first — it becomes the in-video reference; eyeball before continuing
python generate_images.py --storyboard $SB --scenes 1

# 3. The rest (auto-references scene_01; scenes with reference_image also get
#    the real photo passed as a geometry reference — anchor = LOOK, photo = GEOMETRY)
python generate_images.py --storyboard $SB
```

- Same session, same model version for within-video consistency. Per-scene `image_model` override exists for hero frames.
- Re-generate individual scenes with `--scenes "3,7,12-14" --force`.
- Failures print per-scene errors and continue; re-run with `--scenes` for the gaps.

## Stage B — Accuracy gate (HARD GATE — run `visual-accuracy-gate`, Layer 2)

- [ ] Claude vision compares each still vs. its `reference_image` + `visual_facts`; user confirms the verdict table (~15–20 min).
- [ ] Failures → regenerate with a **corrective delta prompt naming the error**, via `--scenes N --force`.
- [ ] Results → `projects/NNN_topic/validation_report.md`.
- [ ] **Nothing proceeds to Stage C until every animated-type scene's still is validated.** Animation costs ~10–40× a still and inherits its every error.

## Stage C — Animation (Kling MCP, agent-driven)

**Prep:**

```bash
python prompt_builder.py $SB --anim-jobs   # → anim_jobs.json + total seconds
```

Each job carries: scene #, still path, clip path, duration, and the composed motion prompt (already includes "do not add, remove, or deform any structural element" + the scene's `visual_facts`).

**Model selection (verify against `who_am_i`, but the default is settled): use `kling-video-v3_0_turbo`.** Two reasons it's the right default for this channel:
- **Duration:** it supports **3–15s**, so the 6s cost-bias actually works. `v2_5`/`v2_6` only allow 5s/10s (a "6" is invalid — clamp to 5 there), so they can't hold the 6s bias.
- **No audio:** its params are exactly `prompt, duration, resolution, imageCount` — it has **no `enable_audio` flag and generates no soundtrack**, which is precisely what we want (narration + music are mixed at assembly). Nothing is spent producing audio we'd discard. By contrast `v2_5`/`v2_6` default `enable_audio=true` (you'd have to remember to disable it), and `v3_0`/`v3_0_omni` expose `enable_audio` (defaults false — leave it off).

Resolution 720p std. If `v3_0_turbo` is ever unavailable, fall back to `kling-video-v3_0` at 6s with `enable_audio` **false** (never `v2_x` unless you accept 5s/10s + a mandatory audio-off flag).

**Confirm before submitting (MANDATORY):** present the batch to the user — number of clips, total seconds, estimated credits vs. available — and get an explicit go. **Every job is charged; there are no trial runs.** Never auto-resubmit a failed/ambiguous job; report and ask.

**Per job:**

1. `file_upload` the validated still (PNG/JPG, <4K, ≤30MB, aspect ≤1:2) → returns a Kling URL. **Only `file_upload` URLs are accepted as `first_image`** — no local paths, no external URLs.
2. `image_to_video` — model per above; `first_image` = uploaded URL; `prompt` = the job's motion prompt; `duration` = the job's duration (clamped to the model's allowed values).
3. Poll `query_tasks` until complete. Batch tip: submit all confirmed jobs, then poll collectively — don't serialize submit→wait→submit.
4. **Download immediately** to `projects/NNN_topic/clips/scene_NN_animated.mp4` — **result URLs expire in 24h.**
5. Record in `assets_manifest.json` under `scene_NN.clip`.

**Scrub-check (run `visual-accuracy-gate`, Layer 3):** first/middle/last frame per clip; compare last frame to the source still (~20s each).

**Failure ladder per scene (hard rules):**
- 1st bad result → **one retry** with tightened motion ("parallax and drifting haze only"). Confirm with the user first — the retry is also charged.
- 2nd bad result, or moderation block → **retag the scene `type:"static"` in the storyboard** and let Ken Burns cover it. The fallback is accurate by construction — it IS the validated still. Append the outcome to `validation_report.md`.

## Stage D — Upscale statics

- [ ] Upscale all `type:"static"` scene images to 4K (`images_4k/`) for Ken Burns zoom headroom (Real-ESRGAN local, free). Animated scenes skip this — Kling output is the deliverable.

## Final report (always give the user this summary)

```
Stills:      54 generated · 51 passed gate first pass · 3 delta-fixed
Animation:   27 planned → 25 clips accepted · 1 retried-then-accepted · 1 → Ken Burns fallback
Credits:     ~1,640 spent · N remaining
Fallbacks:   scene 23 retagged static (geometry morph on both attempts)
Next:        Phase 4 (particles) → Phase 5 (record narration) → assembly
```

---

## Rules that override everything

1. **Credits check before stills, cost confirmation before every Kling batch** — every job is charged; no trial runs, no auto-resubmit.
2. **No unvalidated still is ever uploaded to Kling.** The gate is not optional under schedule pressure.
3. **One animation retry, then Ken Burns.** Ship beats perfect.
4. **Download clips promptly** — result URLs die in 24h.
5. On timeout/failure/unexpected results: report to the user and ask; never silently change parameters or intent.

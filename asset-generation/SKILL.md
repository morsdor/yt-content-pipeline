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
- [ ] **Credits check (BLOCKING):** call `query_membership_and_credits`. Estimate the batch: `python prompt_builder.py <sb> --anim-jobs` prints total seconds; at **6 cr/s** (720p, no native audio — confirmed) a ~27-clip batch ≈ **~1,300–1,500 credits** (with the 6s bias). If available credits < estimate, **STOP and tell the user** — do not submit a partial batch. (Free tier / 0 credits = stop here.)
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

**Model selection (settled empirically): use `kling-video-v3_0`, `enable_audio=false`, resolution `720p`.** Best value *and* accuracy for this channel:
- **No audio = cheaper.** Turning native audio OFF drops the rate **8→6 cr/s at 720p** (10→8 at 1080p). We mix narration + music at assembly, so native audio is pure waste. `v3_0` declares `enable_audio` (default `false`) — pass it explicitly. ⚠️ **Do NOT use `v3_0_turbo`:** despite the name it has *no* audio flag, **bakes audio in** (can't disable), and bills at the pricier 10 cr/s. `v2_5`/`v2_6` default `enable_audio=true`.
- **Element consistency.** `v3_0` = *"enhanced native audio, improved element consistency"* — that consistency is exactly our anti-morph property.
- **Duration.** `v3_0` supports **3–15s**, so the 6s bias works.
- **Resolution.** Generate at **720p (6 cr/s)**; upscale to 4K locally for free (Stage D). **Confirmed rate: a 7s 720p no-audio clip = 42 credits.** Full video (~221 animated s) ≈ **1,300–1,500 cr → ~2 videos/month** on the 3,000-credit Pro plan.
  - **Flicker hybrid (measured, not guessed):** 720p→4K ~matches 1080p on smooth scenes but **shimmers on dense lattice/steps in motion** (Kling's 720p + the per-frame upscale each add flicker; temporal denoise can't fix it). So after generating, run **`python flicker_check.py projects/NNN/clips/*.mp4`** and **re-generate only the flagged (`flicker_HF > 3`) scenes at 1080p** (8 cr/s) — don't pre-classify by scene type (a "lattice" wide can be smooth; scene 5 was, scene 31 wasn't). ~⅓ of animated scenes typically cross the line. Full detail: [docs/upscaling.md](../docs/upscaling.md).

Via the `kling-cli`, that's: `kling image_to_video --model kling-video-v3_0 --image <still> --duration <d> --resolution 720p --enable_audio false "<prompt>"`.

**Confirm before submitting (MANDATORY):** present the batch to the user — number of clips, total seconds, estimated credits vs. available — and get an explicit go. **Every job is charged; there are no trial runs.** Never auto-resubmit a failed/ambiguous job; report and ask.

**Per job:**

1. Provide the validated still (PNG/JPG, <4K, ≤30MB, aspect ≤1:2). Via the **MCP**: `file_upload` first → use the returned URL as `first_image` (local paths not accepted). Via the **`kling-cli`**: pass the local path to `--image` directly — the CLI auto-uploads.
2. `image_to_video` with `--model kling-video-v3_0 --resolution 720p --enable_audio false`, `prompt` = the job's motion prompt, `duration` = the job's duration.
3. **🚨 Capture the `generationId` immediately** — write full submit stdout to a file, parse the id from it, and append to `clips/kling_generations.jsonl`. **Never pipe the submit through a lossy parser** (you'll truncate before the id and orphan a *charged* job). There is **no server-side task-list tool** — a lost `generationId` is unreachable by `query_tasks` and recoverable only from the Kling web history.
4. Poll `query_tasks <generationId>` until complete. Batch tip: submit all confirmed jobs, then poll collectively — don't serialize submit→wait→submit.
5. **Download immediately** to `projects/NNN_topic/clips/scene_NN_animated.mp4` — **result URLs expire in 24h.**
6. Record in `assets_manifest.json` under `scene_NN.clip`.

**Scrub-check (run `visual-accuracy-gate`, Layer 3):** two passes per clip — **3a accuracy** (first/middle/last frame; compare last frame to the source still — catches geometry morphing, ~20s each) and **3b polish** (does it look *sloppy*? shimmer, uncanny/too-fast motion, cut pops, wandering accent). The shimmer sub-check is the flicker hybrid below — `flicker_check.py` flags dense-lattice scenes to re-gen at 1080p.

**Failure ladder per scene (hard rules):**
- 1st bad result → **one retry** with tightened motion ("parallax and drifting haze only"). Confirm with the user first — the retry is also charged.
- 2nd bad result, or moderation block → **retag the scene `type:"static"` in the storyboard** and let Ken Burns cover it. The fallback is accurate by construction — it IS the validated still. Append the outcome to `validation_report.md`.

## Stage D — Upscale to 4K (local, free)

The free alternative to paying Kling credits for native 1080p/4K. Uses the vendored Real-ESRGAN (`realesr-animevideov3` — the temporally-stable illustration *video* model). **One-time install + the model-bundle gotcha: [docs/upscaling.md](../docs/upscaling.md).**

- [ ] **Static stills → 4K** (`images_4k/`) for Ken Burns zoom headroom — `realesrgan-x4plus-anime`.
- [ ] **Animated 720p clips → 4K** — `python upscale_video.py clips/scene_NN_animated.mp4 clips_4k/scene_NN_4k.mp4` (x3 → 3840×2160, silent, source fps preserved). ~0.6s/frame on CPU under Rosetta, so a full video is a background/overnight pass — as measured on scene 1: 169 frames in ~107s.
- On flat isometric line art the 720p→4K upscale ~matches native 1080p/4K. **Upload 4K to YouTube regardless of source res** — YouTube gives 4K uploads more bitrate, so even 1080p playback looks cleaner.

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

---
name: asset-generation
description: >-
  Use when generating a video's visual assets after the storyboard is approved —
  stills → validation → animation prep → render QC. Trigger on "generate the assets",
  "run asset generation", "make the images", "prep the animation", or Phase 2–3 of an
  Engineering Atlas video. Runs generate_images.py for stills, enforces the
  visual-accuracy-gate before anything is animated, writes the per-scene motion briefs,
  fills the assets_library shopping list (generate_asset.py), scaffolds JSX comp
  builders, and QCs the After Effects renders when they land in clips/. Requires
  GEMINI_API_KEY in .env. The AE build itself is done by the user.
---

# Asset Generation — Stills → Gate → Animation Prep → Render QC

**What this produces:** `images/scene_NN.png` (~55 validated stills, upscaled to 4K),
`motion_briefs.md` (per-scene AE shot directions), any missing `assets_library/` elements,
optional `ae_scripts/` comp builders, and — after the user's AE session — QC'd
`clips/scene_NN_animated.mp4`. Everything Phase 5 (voice) and Phase 6 (assembly) need.

**The chain, in order — order is the budget protection:**

```
stills (cheap) → accuracy gate (free) → AE prep (free) → USER builds in AE → render QC (free)
```

Animation itself has **no marginal cost** — no credits, no charged retries. The scarce
resource is the user's AE time; the prep stages exist to make that time short.

Companion skills: [`visual-accuracy-gate`](../visual-accuracy-gate/SKILL.md) (invoked at two
points below), `the-engineering-atlas-video` (the parent checklist). Reference:
[docs/after_effects_workflow.md](../docs/after_effects_workflow.md),
[assets_library/STYLE_BIBLE.md](../assets_library/STYLE_BIBLE.md).

---

## Stage 0 — Preflight (all must pass before anything is generated)

- [ ] **Storyboard is approved** (the parent skill's review gate passed). Scenes depicting the real structure carry `visual_facts` + `reference_image`; `references/` pack exists.
- [ ] `GEMINI_API_KEY` present in `.env` (repo root or project folder).
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
- [ ] **Nothing proceeds to Stage C until every animated-type scene's still is validated.** The AE build starts from these frames and inherits their every error — and unlike a prompt fix, a wrong still discovered mid-build wastes the user's hands-on time.

## Stage C — Animation prep (agent-driven, free)

**C.1 — Motion briefs:**

```bash
python prompt_builder.py $SB --motion-briefs   # → motion_briefs.md
```

One brief per animated scene: what moves, direction and distance, duration, easing, and
what must NOT move (the scene's `visual_facts` ride along as hold-constraints). Review the
briefs and tighten any that read vague — a good brief is buildable without asking questions.

**C.2 — Asset shopping list:** diff what the briefs need (characters, props, parallax
elements, diagram arrows) against `assets_library/INDEX.md`. Generate **only the missing
assets** with `generate_asset.py` (STYLE_BIBLE rules enforced: flat magenta background →
4× upscale → keyed alpha → indexed). Reuse beats regenerate — for cost *and* cross-video
consistency.

**C.3 — Layered plates (parallax scenes only):** for scenes getting Rung-2 parallax,
generate clean plates ("same scene without the tower") so foreground elements become their
own layers. Same accuracy gate applies to new plates of the real structure.

**C.4 — Upscale stills to 4K** (local, free — [docs/upscaling.md](../docs/upscaling.md)):
`realesrgan-x4plus-anime` on every accepted still. AE comps are 3840×2160; the assembler's
Ken Burns wants the headroom too.

**C.5 — JSX scaffolds (optional but cheap):** anything repetitive in the briefs — armies of
duplicated soldiers, staggered layer imports, a standard push-in comp per scene — gets a
script in `ae_scripts/` instead of manual clicks. Write them proactively when a brief
implies more than ~10 identical manual steps.

**Handoff:** tell the user what's ready — briefs, new assets, scaffolds — and which scenes
are good first builds (simplest motion first). The AE session is theirs.

## Stage D — Render QC (when AE clips land in `clips/`)

Run `visual-accuracy-gate` **Layer 3 (motion craft)** on each delivered
`scene_NN_animated.mp4`:

- [ ] Eased motion everywhere (linear moves are the #1 amateur tell)
- [ ] ≤2 moving elements per scene; speeds subtle; nothing warps or "breathes"
- [ ] First/last frames sit clean against the neighboring scenes (no cut pop)
- [ ] Same asset files across scenes (consistency gate)
- [ ] Duration matches the storyboard within ~0.5s; 3840×2160 @ 30fps

Fixes are free — note the issue, the user adjusts the comp and re-renders. No retry
budget, no fallback pressure. A scene that isn't worth more AE time gets retagged
`type:"static"` (Ken Burns — accurate by construction; you always ship).

## Final report (always give the user this summary)

```
Stills:       54 generated · 51 passed gate first pass · 3 delta-fixed · all 4K
Motion prep:  27 briefs written · 6 new library assets (indexed) · 2 JSX scaffolds
AE build:     27 scenes → 25 accepted · 2 notes sent back for re-render
Fallbacks:    scene 23 retagged static (not worth AE time this cycle)
Next:         Phase 4 (particles) → Phase 5 (record narration) → assembly
```

---

## Rules that override everything

1. **No unvalidated still is ever animated.** The gate is not optional under schedule pressure.
2. **Check `INDEX.md` before generating any library asset** — a duplicate wastes money; an off-style twin poisons consistency.
3. **Briefs must be buildable** — if a brief needs interpretation, rewrite the brief, don't make the user guess.
4. **Ken Burns fallback is always available.** Ship beats perfect.
5. On generation failures/unexpected results: report to the user and ask; never silently change intent.

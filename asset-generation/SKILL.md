---
name: asset-generation
description: >-
  Use when executing a boarded video's generation — after the studio-director chain has
  produced the approved storyboard.json v2. Trigger on "generate the assets", "run asset
  generation", "make the plates", "execute the board", or the Generation stage of an Engineering Atlas
  video. Generates exactly what the board specifies: plates from plate{} blocks
  (generate_images.py), library assets from the asset-planner's approved batch
  (generate_asset.py), 4K upscale, layered-plate prep — with the visual-accuracy-gate
  enforced on every plate (Layer 2) and every asset (Layer 2.5) before anything proceeds.
  Requires GEMINI_API_KEY in .env. The AE build itself is done by the user.
---

# Asset Generation — Executing the Board (plates → gate → assets → prep)

**What this produces:** validated 4K `images/scene_NN.png` plates for every `plate`/
`plate+layers` scene, the approved batch's new `assets_library/` elements (keyed, indexed),
layered plates where the board separates depth bands — everything the animatic (the Animatic stage)
and the user's AE session (AE build) need.

**The contract:** this skill **generates nothing the board doesn't specify.** Subjects,
references, facts, layers, and the asset batch were all decided by the studio passes
(scene-composer + asset-planner); this is the illustration department executing a signed-off
plan. If something seems missing or wrong here, it goes back to the board — not into an
improvised prompt.

```
plates (cheap) → accuracy gate (free) → batch assets + asset gate → AE prep (free)
```

Companion skills: `studio-director` (the board that drives this), [`visual-accuracy-gate`](../visual-accuracy-gate/SKILL.md)
(Layers 2 + 2.5 below), `the-engineering-atlas-video` (the parent checklist). Reference:
[docs/after_effects_workflow.md](../../../docs/after_effects_workflow.md),
[assets_library/STYLE_BIBLE.md](../../../assets_library/STYLE_BIBLE.md),
[docs/storyboard_schema.md](../../../docs/storyboard_schema.md).

---

## Stage 0 — Preflight

- [ ] Board approved: `passes.ae_director` stamped, the final gate answered, `--validate` clean.
- [ ] `GEMINI_API_KEY` present in `.env` (repo root or project folder).
- [ ] Style anchor decision: **video #1** → `style_card.txt` only; **video #2+** → pass an anchor from `assets/style_anchors/` on every call.
- [ ] VO recorded + true-up done (preferred — the animatic right after this stage needs it).

## Stage A — Plates (`generate_images.py`)

Only `build: "plate"` and `"plate+layers"` scenes generate; `assembly` scenes are skipped
(they're built in AE from library assets).

```bash
SB=projects/NNN_topic/storyboard.json

# 1. Dry-run: verify the plan + one composed prompt, zero API calls
python generate_images.py --storyboard $SB --dry-run

# 2. Scene 1 first — it becomes the in-video reference; eyeball before continuing
python generate_images.py --storyboard $SB --scenes 1

# 3. The rest (auto-references scene_01; scenes with plate.reference_image also get
#    the real photo passed as a geometry reference — anchor = LOOK, photo = GEOMETRY)
python generate_images.py --storyboard $SB
```

- Prompts compose from `plate.subject` + the scene's recipe + style card + accent + the
  reserved negative space — the board's decisions, verbatim.
- **`plate+layers` scenes:** the plate must NOT contain its layered subjects (the
  scene-composer's subject line excludes them — verify on the render: empty sky where the
  cloud goes).
- Same session, same model version; per-scene `image_model` override for hero frames;
  re-roll with `--scenes "3,7" --force`.

## Stage B — Plate accuracy gate (HARD — `visual-accuracy-gate` Layer 2)

- [ ] Vision-compare each plate vs. its `plate.reference_image` + `plate.visual_facts`; user confirms the verdict table (~15–20 min).
- [ ] Failures → **corrective delta prompt naming the error**, `--scenes N --force`.
- [ ] Results → `validation_report.md`. **No unvalidated plate proceeds** — the AE build inherits every error, and a wrong plate found mid-build wastes the user's craft hours.

## Stage C — Batch assets + AE prep (free except the approved batch)

**C.1 — The batch:** run the asset-planner's approved batch —
`python generate_asset.py --batch assets_library/_batches/batch_NN.json` (magenta bg → 4×
upscale → keyed alpha → edge bleed → INDEX.md). Every new asset passes the
**Layer 2.5 asset gate** before its `layers[].asset` reference counts as resolved.
**Only the approved batch** — a mid-generation "we also need X" goes back through the
asset-planner's gate.

**C.2 — Layered plates (Rung-2 parallax scenes):** where `ae_build` separates depth bands
beyond what layers already provide, generate the clean variant plates ("same scene, empty
sky") — same Layer 2 gate for real-structure plates.

**C.3 — 4K upscale** (local, free — [docs/upscaling.md](../../../docs/upscaling.md)):
`realesrgan-x4plus-anime` on every accepted plate. AE comps are 3840×2160.

**C.4 — Scaffolds check:** the ae-director already wrote the JSX scaffolds; confirm each
`ae_build.jsx` path exists and imports resolve against the now-real files.

**Handoff:** report what's ready (plates n/n validated, batch m/m indexed, scaffolds
checked), then → **animatic** (`video_assembler.py`, the Animatic stage), then the AE session is the
user's, per the ae-director's session plan.

## Stage D — Render QC (when AE clips land in `clips/`)

Run `visual-accuracy-gate` **Layer 3 (motion craft)** on each delivered `scene_NN.mp4`:

- [ ] Motion matches the board's numbers (camera verb/amount, layer speeds, ≤2 moving)
- [ ] Eased everywhere (linear moves are the #1 amateur tell); nothing warps or "breathes"
- [ ] First/last frames sit clean against neighbors; **~1s handles present both ends**
- [ ] Same asset files across scenes; continuity registry respected
- [ ] 3840×2160 @ 30fps; duration ≈ board within the handles

Fixes are free — note the issue, the user adjusts the comp and re-renders. A scene not
worth more AE time simplifies to its Rung-1 camera-only build. You always ship.

## Final report (always give the user this summary)

```
Plates:   48 specified · 48 generated · 45 passed gate first pass · 3 delta-fixed · all 4K
Batch:    9 assets generated · 9 passed asset gate · INDEX.md updated
Prep:     3 layered plates · 4 JSX scaffolds verified
Next:     animatic → AE session (session plan in shot_list.md) → Layer 3 QC → Premiere
```

---

## Rules that override everything

1. **No unvalidated plate is ever built on.** The gate is not optional under schedule pressure.
2. **The board is the spec.** No improvised subjects, no unbatched assets, no "while we're at it."
3. **Check `INDEX.md` before generating anything** — a duplicate wastes money; an off-style twin poisons consistency.
4. **The camera-only fallback is always available.** Ship beats perfect.
5. On generation failures/unexpected results: report to the user and ask; never silently change intent.

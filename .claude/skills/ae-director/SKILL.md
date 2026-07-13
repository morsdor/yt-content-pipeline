---
name: ae-director
description: >-
  Studio pass 7 of 7. Use after motion-director to turn motion specs into After Effects build
  blueprints (invoked by studio-director, or on "plan the AE build", "write the comp specs",
  "scaffold the comps"). Fills ae_build{} per scene in storyboard.json v2 — comp settings,
  layer hierarchy/parenting, precomps, expressions, render spec (3840x2160@30, ~1s handles,
  clips/scene_NN.mp4) — and writes JSX comp-builder scaffolds into ae_scripts/ for repetitive
  builds. Ends at the final HUMAN gate: the complete shot_list.md review before generation
  and the AE session.
---

# AE Director — Studio Pass 7: motion specs → build blueprints

**Role:** the technical director. You translate each scene's motion spec into the concrete
AE build: what gets parented to what, which precomps exist, which expressions run, what the
render settings are — and where a JSX script should build the comp instead of the user's
hands. After this pass the user opens AE and *executes*; nothing is designed at the desk.

**Loads:** `storyboard.json` (passes 1–6) · `docs/after_effects_workflow.md` (the build
craft, template comps, expressions library `ae_recipes.md`) · `brand_guide.md` §5 (render
spec) · `ae_scripts/` (existing scaffolds, e.g. `build_practice_scene_01.jsx`).

**Fills:** per-scene `ae_build{}`. Writes JSX scaffolds to `ae_scripts/`. Stamps
`passes.ae_director`. Appends "Pass 7 — AE blueprints" to `shot_list.md`, then runs the
direction QA checklist and presents the finished board at the **final human gate**.

---

## Procedure

1. **Group scenes into build families.** Scenes sharing a structure (plate + camera null /
   flat stage + characters / map + trim-path arrow / section + waterline) share a template
   comp — name the family in `ae_build.hierarchy`. By video 5 the families ARE the
   pipeline's speed.
2. **Per scene, write `ae_build{}`:**
   - `comp`: `3840x2160 @ 30fps`, duration = scene duration + 2×handles.
   - `hierarchy`: one line — nulls and parenting. Default pattern: `CAMERA_CTRL null ►
     [plate, layers…]`, parallax layers coupled at their ratio (slider/expression), text
     and overlays *not* parented to camera unless they belong to the world.
   - `precomps[]`: repeated element groups (a soldier rank, a label cluster) — precomp
     what repeats or what needs a single collective transform.
   - `expressions[]`: from the motion specs — `loopOut` drift loops with de-synced phase,
     `wiggle` for ambient only, time-based position drift; name each with its target layer.
   - `jsx`: path if scripted (below), else `null`.
   - `render`: `{ "clip": "clips/scene_NN.mp4", "handles_s": 1.0 }` — H.264/ProRes per the
     workflow doc, **native 4K, no upscaling stage**.
3. **Decide what gets a JSX scaffold.** Script it when: ≥3 scenes share a family (one
   builder, parameterized), or a build is mechanical-but-fiddly (import 12 layers, scale,
   position, parent, set eased keys). Hand-build when: puppet pins, taste-heavy timing, or
   one-off scenes — scripting those costs more than it saves. Write scaffolds in
   ExtendScript ES3 (no let/const/arrows), one undo group, teaching comments — follow
   `ae_scripts/build_practice_scene_01.jsx` as the house pattern.
4. **Sequence the user's AE session** in shot_list: build order (families together,
   Rung-1-only scenes first for momentum), per-scene expected time, which scaffold to run
   for which scene (`File → Scripts → Run Script File…`).
5. **Run the direction QA checklist** (`docs/cinematography.md` §11) across the whole
   board. Fix or flag every miss.
6. **STOP — FINAL HUMAN GATE.** Present `shot_list.md` complete (all seven pass sections +
   QA result). On approval, the board is frozen: plates/assets generate
   (`asset-generation` skill), VO records if not already done, and the AE session begins.

## Rules

1. **The blueprint must be executable cold.** The user at the AE desk should never have to
   re-derive a decision — if a question could come up mid-build, answer it in `ae_build`
   or the session notes now.
2. **Handles are law.** Every render is ~1s longer at both ends than its nominal duration;
   Premiere conform is trim-only (`RHYTHM-1`). A clip without handles gets rebuilt.
3. **Template comps compound; name them consistently** (`fam_plate_push`, `fam_stage`,
   `fam_map_route`, `fam_section_water`) so next video's board reuses the names.
4. **Expressions are for ambient motion; keyframes are for meaning.** Anything that
   communicates (camera, gestures, draw-ons) is keyframed and eased by hand — expressions
   never carry the scene's message.
5. **Don't inflate the JSX surface.** Scaffolds set up comps; the user animates. A script
   that tries to place every keyframe of a gesture has crossed into taste — stop short.

## Enrichment mode

Existing scenes are single-plate builds: most get the `fam_plate_push` family with a
one-line hierarchy, and only the scenes where pass 4 added layers get richer blueprints.
JSX leverage is high here — one builder can scaffold all 54 comps with plates imported,
camera nulls rigged, and eased push keys set from `camera{}`.

**Handoff:** the final gate → `asset-generation` (plates + batch) → user's AE session →
`visual-accuracy-gate` Layer 3 render QC → Premiere conform.

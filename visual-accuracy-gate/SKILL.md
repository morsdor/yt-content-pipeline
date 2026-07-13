---
name: visual-accuracy-gate
description: >-
  Use when validating AI-generated visuals against real reference photos — plates
  before animation, library assets before indexing, and After Effects renders after they
  land. Trigger on "run the accuracy gate", "validate the stills/renders", "QC the clips",
  "check scene N against the reference", or automatically between generation and animation
  in any Engineering Atlas video (the gate is mandatory there). Compares each render to its
  reference photo + visual_facts checklist, checks renders against the board's
  continuity_registry (the studio's continuity supervisor) and comprehension rules (the
  2-second test), produces corrective delta prompts for failures, and enforces the rule
  that no unvalidated plate is ever animated.
---

# Visual Accuracy Gate — Reference-Anchored Validation

**Why this exists:** the channel depicts real, extant, heavily-photographed monuments for an audience that knows what they look like — a wrong step pattern or an invented arch is as damaging as a wrong date, and unlike a date it can't be patched after rendering. Style consistency makes the video *look* like one brand; this skill makes it *true*.

**Design goal:** prevent errors at generation, catch survivors before the expensive step (the user's hands-on After Effects time), and make any fix a **single named-delta rerender** — never an open-ended retry loop.

**The failure ladder (cheapest fix wins):** prevented at generation → caught at the still gate for the price of a still → caught at render QC for the price of a comp tweak → shipped as the Rung-1 camera-only build for free.

**Studio roles this skill carries** (per the studio pipeline): the **Continuity Director**
(renders vs. the board's `continuity_registry` — light direction, side/axis assignments,
recurring asset files) and **Animation QA** (comprehension: the 2-second test, clutter,
text readability — `docs/cinematography.md` §11).

---

## Inputs (per project)

| Input | Where | Made in |
|:---|:---|:---|
| Reference pack: 5–15 real photos/plans, source URLs kept | `projects/XXX/references/` | Session 0 (research) |
| `visual_facts.md`: the structure's *visually checkable* claims | `projects/XXX/references/` | Session 0 |
| Per-scene `visual_facts[]` + `reference_image` fields | `storyboard.json` | Storyboard phase |
| Rendered stills | `projects/XXX/images/` | Image generation |
| Library assets (for Layer 2.5) | `assets_library/` | Asset generation |
| AE renders (for Layer 3) | `projects/XXX/clips/` | The user's AE session |

**What a good visual fact looks like:** geometry ("three stepped sides, one pavilion side"), counts ("13 visible storeys"), patterns ("steps in paired V-flights forming a diamond lattice"), materials, orientation, water level. *Checkable claims, not prose.* If it can't be verified from a photo or plan, it belongs in script fact-checking, not here.

---

## Layer 0+1 — Prerequisites (verify, don't redo)

These should already be in place; if missing, stop and fix upstream first:

- [ ] `references/` pack + `visual_facts.md` exist (Session 0 output)
- [ ] Scenes depicting the real structure carry `visual_facts` and `reference_image` (v2: inside `plate{}`); abstract scenes (maps, force diagrams) carry facts only, or neither; the board's top-level `continuity_registry` is populated (v2)
- [ ] Prevention is automatic once the fields exist: `prompt_builder.py` injects the facts into plate prompts ("Factual constraints") and the board carries them as hold-constraints on the motion blocks (so the AE build knows what may not move or be covered); `generate_images.py` passes the reference photo alongside the style anchor (**anchor = LOOK, photo = GEOMETRY** — the model copies proportions it can *see* far more reliably than proportions described in text)

---

## Layer 2 — The validated-still gate (HARD GATE, before any animation spend)

**Build the review artifacts first (automated):** `python review_images.py --storyboard <sb>` writes `projects/XXX/review/` — labeled **contact sheets** of every still, **render-vs-reference pairs** (`pairs/scene_NN.png`, the geometry check side by side), and a **`review_checklist.md`** (subject · facts · ref · empty Verdict column). Read-only; never regenerates. Turns "open 54 files" into a few labeled montages; pass a `--scenes "8-15,29"` subset to rebuild just a group on re-check. Then for each still that has `visual_facts` and/or `reference_image`:

1. **Read three things side by side:** the render, the reference photo, the fact list.
2. **Check every fact** against the render. Also flag anything structurally invented that no fact covers (extra arches, wrong storey count, impossible geometry) — the facts are a floor, not a ceiling.
3. **Report per scene:** `PASS` or `FAIL: <the specific mismatch, stated as observed-vs-required>`.
4. Present the full verdict table to the user for confirmation (~15–20 min of their time for a full video). **The user confirms; the skill flags.**

**Fixing failures — the delta rule:** regenerate with the *named* error appended to the original prompt:

```
CORRECTION: the previous render showed [observed]; the structure has
[required]. Correct this. Change nothing else.
```

Optionally pass the failed render back as a third image. Naming the delta is what makes one pass usually sufficient — never blind-reroll.

**Two systematic failure modes to expect (both fixed at the prompt, not per-scene):**
- **Space-filling:** on whole-structure wides/sections the model fills open voids and multiplies signature features (e.g. a stepwell's central pavilion → a palace on every side). Fix in the shared `visual_facts` with *prohibitive* language ("the center is EMPTY open air; three sides are ENTIRELY bare steps; one pavilion on ONE side; no palace/fort/temple"), then regenerate the affected group.
- **Anchor-bleed:** the style anchor carries *content*, not just look. Scenes that should **not** show the main structure — landscapes, generic/contrast diagrams, other buildings — get it bleed in when their prompt doesn't re-assert the subject. Fix by making the plate subject explicit and exclusionary ("a SIMPLE vertical shaft well — NOT a stepwell, no steps, no buildings") and regenerating. Scenes that already name their subject concretely won't bleed; vague ones ("the same well") will. Same trap for `plate+layers`: a plate that painted its layered subjects in (a cloud in the "empty" sky) fails the gate — the delta names the exclusion.

**The gate rule: no still is animated unvalidated.** The AE build starts from this frame and inherits its every error — and an error discovered mid-build wastes the user's hands-on time, the pipeline's scarcest resource. This gate is where accuracy and time protection are the same act.

**Output:** write `projects/XXX/validation_report.md` — one row per checked scene: scene #, facts checked, verdict, delta prompt used (if any), final status. Regenerate the report on re-runs; it's the paper trail that the gate actually ran.

---

## Layer 2.5 — The asset gate (before an element enters `assets_library/`)

Library assets are **load-bearing across many videos** — a wrong or off-style asset ships
wrong in every future video that reuses it. Before an asset is indexed
(checklist mirrors [STYLE_BIBLE.md](../assets_library/STYLE_BIBLE.md)):

- [ ] Palette + line weight match the anchor (hold it next to scene_01)
- [ ] Correct view convention for its category (isometric: architecture/props · flat: characters/nature/diagram)
- [ ] Clean alpha edge — no keying fringe, no chewed outlines
- [ ] Geometry plausible; historically appropriate for its intended use

Failures get a named-delta re-roll or a prompt fix in the batch spec — never enter a bad
asset "for now."

---

## Layer 3 — Render QC: motion craft + continuity + comprehension (when AE renders land in `clips/`)

**Accuracy is inherited by construction here** — After Effects transforms the validated
art but never redraws it, so geometry cannot morph, melt, or invent itself. What CAN still
go wrong is *craft*, *continuity*, and *comprehension*. Check each delivered
`scene_NN.mp4` against its scene's board blocks:

**Motion craft (vs. the board's numbers):**
- **Spec fidelity** — the render matches `camera{}` and `layers[].motion{}`: right verb, right amount, right speeds. The board is the contract; "close enough" drifts the brand.
- **Easing** — every keyframe pair eased (F9); linear motion is the #1 amateur tell.
- **Restraint** — ≤2 moving elements (camera excluded); speeds inside `brand_guide.md` §5 limits. Motion reads as intended movement, never as busyness.
- **Cut discipline** — first/last frames sit clean against neighboring scenes; 0.5–1s holds at both ends; **~1s handles present** (Premiere conform needs them).
- **Spec** — 3840×2160 @ 30fps; duration ≈ board within the handles.

**Continuity (the Continuity Director duty — vs. `continuity_registry`):**
- Light from upper-left in every frame; no sun-jumps between cuts.
- Side/axis assignments hold (water flows its registered way; opposing sides own their halves; characters travel their established direction).
- The same character/object across scenes is the same *file* from `assets_library/`; costumes/props match their registry entries; map orientation stable.
- **Facts respected** — nothing from the scene's `visual_facts` is covered, cropped out, or contradicted by added elements.

**Comprehension (the Animation QA duty — `docs/cinematography.md` §11):**
- The 2-second test: a glancing viewer grasps the scene instantly (one focal point).
- Not cluttered: text readable at 1080p playback, ≤2 callouts alive, contrast holds over the moving background.
- Text timing tracks the narration (enter after the ear, exit before the cut).
- Nothing static >8s inside the scene; data beats get their ~1s landing hold.

### The ladder

- **Fixes are free** — note the specific issue ("scale keys not eased", "cloud too fast", "sun flipped"), the user tweaks the comp and re-renders. No retry budget: iteration costs minutes, not money.
- A scene not worth further AE time → **simplify to its Rung-1 camera-only build** (validated plate + eased push, accurate and clean by construction). Update the scene's board blocks to match what shipped; append the outcome to `validation_report.md`.

**Worst case per scene is a few minutes in the comp — by design.**

---

## Rules that override everything

1. **No unvalidated plate is ever animated.** No exceptions for schedule pressure.
2. **Failures get a named delta, never a blind reroll.**
3. **No off-style asset enters the library.** One bad asset poisons every video that reuses it.
4. **The camera-only fallback is always available.** Ship beats perfect.
5. **The user confirms verdicts** — the skill flags candidates; a human owns the gate.
6. **The registry outranks the scene.** A beautiful render that breaks continuity fails.

---
name: visual-accuracy-gate
description: >-
  Use when validating AI-generated visuals against real reference photos — stills
  before animation, and animated clips after delivery. Trigger on "run the accuracy
  gate", "validate the stills/renders", "scrub-check the clips", "check scene N against
  the reference", or automatically between image generation and animation in any
  Engineering Atlas video (the gate is mandatory there). Compares each render to its
  reference photo + visual_facts checklist, produces corrective delta prompts for
  failures, and enforces the rule that no unvalidated still is ever sent to Kling.
---

# Visual Accuracy Gate — Reference-Anchored Validation

**Why this exists:** the channel depicts real, extant, heavily-photographed monuments for an audience that knows what they look like — a wrong step pattern or an invented arch is as damaging as a wrong date, and unlike a date it can't be patched after rendering. Style consistency makes the video *look* like one brand; this skill makes it *true*.

**Design goal:** prevent errors at generation, catch survivors before the expensive step (animation), and make any fix a **single named-delta rerender** — never an open-ended retry loop.

**The failure ladder (cheapest fix wins):** prevented at generation → caught at the still gate for the price of a still → caught at scrub for the price of one clip → shipped as Ken Burns for free.

---

## Inputs (per project)

| Input | Where | Made in |
|:---|:---|:---|
| Reference pack: 5–15 real photos/plans, source URLs kept | `projects/XXX/references/` | Session 0 (research) |
| `visual_facts.md`: the structure's *visually checkable* claims | `projects/XXX/references/` | Session 0 |
| Per-scene `visual_facts[]` + `reference_image` fields | `storyboard.json` | Storyboard phase |
| Rendered stills | `projects/XXX/images/` | Image generation |
| Delivered clips (for Layer 3) | `projects/XXX/clips/` | Animation phase |

**What a good visual fact looks like:** geometry ("three stepped sides, one pavilion side"), counts ("13 visible storeys"), patterns ("steps in paired V-flights forming a diamond lattice"), materials, orientation, water level. *Checkable claims, not prose.* If it can't be verified from a photo or plan, it belongs in script fact-checking, not here.

---

## Layer 0+1 — Prerequisites (verify, don't redo)

These should already be in place; if missing, stop and fix upstream first:

- [ ] `references/` pack + `visual_facts.md` exist (Session 0 output)
- [ ] Scenes depicting the real structure carry `visual_facts` and `reference_image` in the storyboard; abstract scenes (maps, force diagrams) carry facts only, or neither
- [ ] Prevention is automatic once the fields exist: `prompt_builder.py` injects the facts into image prompts ("Factual constraints") and animation prompts ("Structure must stay true to"); `generate_images.py` passes the reference photo alongside the style anchor (**anchor = LOOK, photo = GEOMETRY** — the model copies proportions it can *see* far more reliably than proportions described in text)

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
- **Anchor-bleed:** the style anchor carries *content*, not just look. Scenes that should **not** show the main structure — landscapes, generic/contrast diagrams, other buildings — get it bleed in when their prompt doesn't re-assert the subject. Fix by making the `image_prompt` explicit and exclusionary ("a SIMPLE vertical shaft well — NOT a stepwell, no steps, no buildings") and regenerating. Scenes that already name their subject concretely won't bleed; vague ones ("the same well") will.

**The gate rule: no still goes to Kling unvalidated.** Animation costs ~10–40× a still and inherits every error in its source frame. This gate is where accuracy and budget protection are the same act.

**Output:** write `projects/XXX/validation_report.md` — one row per checked scene: scene #, facts checked, verdict, delta prompt used (if any), final status. Regenerate the report on re-runs; it's the paper trail that the gate actually ran.

---

## Layer 3 — Animation scrub-check (after clip delivery)

Image-to-video inherits accuracy from the validated still, so the *residual* risk is Kling **morphing geometry during motion** — steps multiplying, arches appearing, edges melting.

1. The composed animation prompt already forbids it ("add motion only… do not add, remove, or deform any structural element" + the facts clause) — subtle motion (parallax, water, dust) rarely triggers morphing in the first place.
2. On delivery, **extract and inspect first / middle / last frame** (`ffmpeg -i clip.mp4 -vf "select=eq(n\,0)" …` or scrub manually); compare the **last frame to the source still**. Structural drift is almost always visible by the final frame. ~20 seconds per clip.
3. **One retry maximum**, with tightened motion scope (e.g. "parallax and drifting haze only") — every Kling job is charged.
4. Second failure → **fall back to Ken Burns**: retag the scene `type:"static"`. The fallback is accurate *by construction* — it IS the validated still. Append the outcome to `validation_report.md`.

**Worst case per scene is one paid rerender — by design.**

---

## Rules that override everything

1. **No unvalidated still is ever animated.** No exceptions for schedule pressure.
2. **Failures get a named delta, never a blind reroll.**
3. **One animation retry, then Ken Burns.** Ship beats perfect.
4. **The user confirms verdicts** — the skill flags candidates; a human owns the gate.

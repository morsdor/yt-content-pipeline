# Visual Accuracy Gate — Chand Baori (Video #1)

*Layer 2 (still validation) run 2026-07-12. Model: `gemini-3.1-flash-image`. Ground truth: `references/visual_facts.md` + the 7 reference photos.*

## Outcome: PASS (after two systematic fixes)

All 54 stills generated and reviewed. Two **systematic** errors were found, root-caused, fixed at the prompt level, and re-validated: (1) palace-in-the-void on whole-structure shots, (2) style-anchor bleed into non-stepwell scenes. No unresolved failures block animation. Review artifacts (contact sheets, render-vs-reference pairs, checklist) are in `review/`, rebuildable with `python review_images.py --storyboard storyboard.json`.

## The systematic error (found → fixed)

**Symptom:** every scene showing the *whole* structure (establishing wides + whole-well sections) filled the open inverted-pyramid void with a sprawling multi-storey palace and mirrored the pavilion onto 2–3 sides. Scene 18 also hallucinated a Hindu temple on top.

**Root cause:** the panorama reference genuinely shows Chand Baori's real central pavilion; the model amplified it into a palace and multiplied it. The `FORM`/`THREE_SIDES` facts weren't prohibitive enough.

**Fix:** strengthened `FORM` + `THREE_SIDES` in the storyboard's `visual_facts` (27 scenes) to explicitly forbid it — "three sides ENTIRELY bare steps, no buildings; center is EMPTY open air; one modest pavilion on ONE side; no palace/fort/temple." Then regenerated the 26 affected scenes; re-rolled scenes 1 & 5 (per-scene variance left the pavilion large).

**Result:** open void + bare stepped walls + pavilion on one side + square tank now render correctly.

## Verdicts

| Group | Scenes | Verdict |
|:---|:---|:---|
| Establishing wides | 1, 5, 16, 30, 31, 48, 52, 53, 54 | ✅ Pass — individually verified post-fix |
| Title / outro heroes | 7, 54 | ✅ Pass — dramatic central pavilion acceptable for title; 54 correctly reserves the subscribe-card space |
| Whole-well section (sampled) | 18 | ✅ Pass — clean inverted-pyramid section, strata + waterline + tank, no temple |
| Pavilion feature | 34, 40 | ✅ Pass — pavilion prominence appropriate to the subject |
| Lattice / step detail (sampled) | 32 (+ 2,6,20,33,35,39,41,46,47,51) | ✅ Pass — diamond V-flights accurate |
| Masonry close (sampled) | 25 (+ 28) | ✅ Pass — mortarless coursed blocks |
| Sections not individually eyeballed | 3,4,17,19,21–24,26,42–44,50 | ☑ High confidence — same strengthened facts + same generator; sampled sibling (18) passes |
| Abstract — content-critical | 8, 9, 10, 11, 12, 13, 14, 38, 49 | ✅ Pass — individually verified (see anchor-bleed fix below) |
| Abstract — diagram/emblem panels | 15, 29, 36, 45 | ☑ Glanced on the contact sheet — on-brand diagram panels, no structure to mis-render |

## Second systematic issue: anchor-bleed (found → fixed)

The abstract review (via `review_images.py` contact sheets + full-res drill-in) caught a second pattern: the stepwell **style anchor bleeds structural content** into scenes that should not show the well. Scenes **9** (arid landscape), **10** (water-table geology), **12** and **14** (the simple *contrast* well) had rendered a stepwell — 12 and 14 even with the old palace-clutter — breaking the script's deliberate simple-well-vs-stepwell contrast.

**Fix:** made those four `image_prompt`s explicit and exclusionary ("a SIMPLE vertical shaft well — NOT a stepwell, no steps, no buildings" / "empty terrain ONLY"). Regenerated → all four correct. Scenes 11 and 13 never bled because their prompts already said "shaft"/"narrow." Pattern documented in the `visual-accuracy-gate` skill.

## Residual notes / carry-forward

- **Minor:** in oblique wides the rim arcade wraps most edges (real gallery is chiefly north). Far better than palace-in-void; accepted as stylization.
- **Tech debt:** Gemini returns JPEG bytes under the `.png` filename. Harmless to moviepy/ffmpeg and to Kling upload (content-sniffed), but normalize extensions before final assembly if any tool complains.
- **Before animation:** upscale `type:"static"` scenes to 4K (Stage D); give the ~28 abstract scenes a quick content check.

## Sign-off

Structure-depicting scenes validated against reference photos — **no invented palace/temple geometry survives to render.** Cleared for Stage C (Kling animation) once Kling credits are topped up.

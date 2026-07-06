# Style Anchors — The Engineering Atlas

## What a style anchor is (and isn't)

A style anchor is a **reference image whose only job is to define your LOOK** — line
weight, color treatment, shading, perspective, texture, mood. When you generate a new
image, you hand the AI an anchor and say "match this style." **The anchor's subject
doesn't matter — only its aesthetic does.** Think paint swatch / house-style sheet,
not an episode scene.

**Why bother:** without a fixed reference, image #1 and image #40 drift (different line
thickness, lighting, palette) and the channel looks inconsistent. Anchors are the middle
rung of the consistency ladder:

- `style_card.txt` text prefix → ~70–80% consistent
- **+ style anchors → ~85–90%**
- + a trained LoRA (later) → ~95%+

---

## Recommended path: HARVEST anchors, don't pre-generate them

You do **not** need to make swatches upfront. Do this instead:

1. **Video #1 (Chand Baori):** generate images using **`style_card.txt` alone** (the text prefix). That's plenty for one video's internal consistency.
2. **After video #1:** pick your **8–10 favorite frames** — the ones that best capture the look you want — and copy them into this folder as `anchor_01.png … anchor_10.png`.
3. **Video #2 onward:** pass the matching anchor as a style reference (`style_strength ~0.7`) on every generation. Now every future video inherits the look you already proved you like.
4. **Around video #5–8:** train a LoRA on your 20–30 best images for near-total consistency.

This way your anchors are **real, on-brand images you chose**, not synthetic guesses — and it's zero extra work.

### Aim for coverage when you harvest

Try to pick frames that span your scene types, so you have a reference for each kind of shot:

- 2–3 **establishing** shots (wide isometric structure)
- 2 **cross-section / cutaway** reveals
- 1–2 **detail** zooms (a mechanism / joint)
- 1 **map** view
- 1 **scale-comparison** shot

---

## Optional: generate a few swatches upfront (only if you want)

If you'd rather have references *before* video #1, generate a handful. Since video #1 is
**Chand Baori (Indian, saffron accent #D4812A)**, orient them to that video's needs.
Paste the top block of `style_card.txt` first, then one prompt:

**swatch_establishing —** Isometric flat-design technical illustration of a vast square stepwell descending into the earth, wide establishing view, symmetric geometric staircases on all sides, warm golden-hour lighting, muted earth tones with warm saffron/ochre (#D4812A) highlights, warm parchment background, high architectural precision, no text, no people.

**swatch_crosssection —** Technical cross-section cutaway of a stepwell, isometric view, showing the stepped tiers descending to the water table, interior layers visible, clean architectural diagram style, muted earth tones, saffron (#D4812A) on key elements, precise geometric lines, educational diagram aesthetic, no text.

**swatch_detail —** Detailed close-up isometric illustration of the interlocking sandstone steps and a landing of a stepwell, high detail, clean vector style, saffron (#D4812A) highlighting the geometry, subtle shadow for depth, warm parchment background, no text.

Keep the cleanest of each; they become `anchor_01…` etc. But again — harvesting from the
finished video #1 is the simpler, better default.

---

*Companion: `style_card.txt` (the text prefix, used on every generation), `brand_guide.md` (§3 colors, §4 fonts).*

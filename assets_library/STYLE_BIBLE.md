# STYLE BIBLE — The Engineering Atlas asset library

*Extends [`style_card.txt`](../style_card.txt) (the brand source for full SCENES) with the
rules for standalone LIBRARY ASSETS — isolated elements on transparent backgrounds that get
composited and animated in After Effects. Every asset generation follows this file.
Generator: `python generate_asset.py` (repo root). Index of what exists: [INDEX.md](INDEX.md).*

## Core look (inherited from the brand)

Flat-design technical illustration. Clean vector aesthetic, precise geometry,
thick clean **charcoal outlines**, flat fills with soft warm shading.
Warm golden-hour light **from the upper-left**, soft directional shadows on the
subject itself. No text ever baked into an asset. Quietly dramatic, crafted, educational.

## Palette (measured from anchor scene_01)

| Role | Hex | Notes |
|---|---|---|
| Parchment (scene bg) | `#F5F0E8` / `#F8F0E0` | never used as an asset background — assets are transparent |
| Cream (light elements) | `#FAF7F2` | clouds, tunics, highlights |
| Sand light | `#F0D8B0` | stone, walls |
| Sand mid | `#E8D8C0` | stone shading |
| Shadow brown | `#B09878` / `#A89070` | shaded faces, trunks |
| Charcoal (linework) | `#2C2C2C` | ALL outlines |
| Skin (characters) | `#C68B59` (shade `#A9714B`) | one consistent warm tone |
| Vegetation | muted sage `#9C9F77` | desaturated — must sit quietly in the parchment world |
| Accent | per-civilization, see style_card.txt | India = saffron/ochre `#D4812A` |

## Two view conventions — never mix them in one asset

- **`isometric`** — architecture and props (towers, walls, wells, pots, carts).
  Same isometric angle as the scene stills; consistent across every asset so
  anything can sit inside any scene.
- **`flat`** — characters, nature, diagram elements. Straight-on flat 2D
  (front or side profile), Oversimplified-style. Characters composited over
  isometric scenes read as intentional style, not as a mistake — Oversimplified
  does exactly this over maps.

## Character design language (the "Oversimplified move", Atlas edition)

- Simple **round head**, black **dot eyes**, minimal nose or none, expression carried
  by eyebrows + mouth
- **~3 heads tall**, simple block clothing from the palette, **mitten hands** (no fingers)
- Thick charcoal outlines, flat fills, soft upper-left shading — same rendering as everything
- Skin `#C68B59` for every character (consistency gate: same character across scenes = same FILE)
- Expressions come from a separate **heads sheet** asset (3 heads in a row → mask/duplicate in AE)
- Rigging: parenting + puppet pins first; Duik Ángela when walk cycles are needed

## Generation rules (enforced by generate_asset.py)

1. **ONE element per image**, centered, generous margins, never touching a frame edge
2. Background: **one solid uniform flat pure magenta `#FF00FF`** — no gradient, no texture,
   no cast shadow on the background (contact shadows are added in AE as a soft ellipse).
   Magenta because the brand palette contains creams/whites — a white background would
   key out parts of the art.
3. Style anchor image passed on every call (palette + line weight lock); prompt tells the
   model to ignore the anchor's subject and background
4. Declare the view (`isometric` or `flat`) explicitly

## Pipeline (what the script does)

```
Gemini gen (magenta bg) → _raw/<name>_raw.png
  → Real-ESRGAN ×4 (realesrgan-x4plus-anime)      # upscale BEFORE keying = smoother alpha
  → chroma-key magenta → alpha + defringe → trim
  → assets_library/<category>/<name>.png (RGBA, ~4K)
  → row appended to INDEX.md
```

```bash
# batch
python generate_asset.py --batch assets_library/_batches/batch_01.json
# single
python generate_asset.py --category nature --name tree_banyan_01 --view flat \
  "a single large banyan tree with a broad layered canopy"
```

## Naming & filing

`category_name_variant` → stored as `assets_library/<category>/<name>.png`
(e.g. `military/soldier_spear_01.png`). Raws kept in `_raw/` for re-keying.
Check [INDEX.md](INDEX.md) BEFORE generating — reuse beats regenerate, for both
cost and cross-video consistency.

## Asset quality gate (before an asset enters the library)

- [ ] palette + line weight match the anchor (hold it next to scene_01)
- [ ] correct view convention for its category
- [ ] clean alpha edge — no magenta fringe, no chewed outlines
- [ ] geometry plausible (this library is load-bearing across MANY videos —
      a wrong asset ships wrong in every future video)

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

---

# Per-civilization motif kits

*Art-director deliverable. Each kit flavours **content** inside the civilization-neutral base look
(the brand palette + line language never take an accent — brand_guide §2/§3). The scene-composer
cites the kit in plate `subject`s; the asset-planner cites it in asset specs. Every kit entry is
written to be **checkable** (art-director rule 2).*

## Roman — Nemausus / Pont du Gard  *(added 2026-07-24, video 001)*

**Accent — terracotta `#B85C38`** (brand §3). Used **only** on callout text, labels, highlight bars,
key-number emphasis, and diagram annotation strokes. **Never** on depicted stone or water.

**Water color — electric azure `#1CA3E0`** *(resolved here — the blue-vs-terracotta question the
storyboard registry flagged).* All **depicted water** — the channel flow, the *specus*, the Gardon
river, and the aqueduct **route line on maps** (the route *is* water) — renders in this one saturated
azure: the single bright pop against warm stone. It is the thumbnail's blue. Azure and terracotta never
fight because they hold different roles: **azure = the subject (water); terracotta = the annotation
layer (type).** Record azure as video 001's water color; it generalizes to future water topics.

**Motif vocabulary (checkable):**
- **Stone / material:** warm **honey-golden shelly limestone** (real Estel-quarry stone) — flat fills in
  sand-light `#F0D8B0` / sand-mid `#E8D8C0`, shadow-brown `#B09878`, ~6px charcoal `#2C2C2C` outlines.
  Dry-stone **ashlar**: large precisely-cut rectangular blocks, clean tight joints — **not** rubble,
  **not** mortar-smeared, **not** marble-white.
- **Arches:** **semicircular Roman round arches** only — never pointed/Gothic. On the Pont du Gard,
  **three tiers** (bottom 6 · middle 11 · top ~35), **unequal spans** (the largest straddles the river).
- **Signature details:** protruding **stone bosses / putlog stubs** on the piers; the covered **specus**
  running along the very top tier; the aqueduct is mostly **at-grade / buried** — the tall arcade is the
  exception (river crossing), never the whole run (this is the "what most people miss" visual, per
  `references/visual_facts.md`).
- **Vegetation — limestone garrigue:** pale rocky ground, low **sage-green scrub** (`#9C9F77`, desaturated),
  **olive trees**, dark **cypress** verticals; sparse and dry. Sits quietly in the parchment world.
- **Atmosphere:** dry Mediterranean high sun, warm haze in the far distance; the Gardon a calm azure
  ribbon in its gorge.
- **The Frontinus interior** *(new — the framing scenes 01–07, 65–67):* a Roman office by night — an
  older man in a **senatorial toga** (cream wool, broad terracotta `latus clavus` stripe), bent over
  **wax tablets, papyrus scrolls, a bronze pipe-gauge (*calix*), an aqueduct ledger**, lit by a single
  **oil lamp** (a warm pool of light, **still keyed upper-left** per COMP-6). Same isometric projection
  as every scene; intimate and warm against the bright outdoor world. Plain plastered wall behind, muted.
- **Surveying instruments:** **chorobates** (~6 m wooden bench, water groove along the top, plumb-lines
  at each end), **groma** (cross-staff, four plumb-bobs, offset bracket), **dioptra** (sighting tube on a
  stand) — wood + bronze fittings, charcoal outlines, isometric prop convention.

**Anti-reference — must NOT drift into:** gleaming white-marble Hollywood Rome (it's honey limestone,
not marble); gladiator-movie CGI grit or brown murk; medieval castle / Gothic pointed arches;
toga-party cartoon kitsch; Caesars-Palace gold. The target is **an engineering drawing of Rome** —
dry, sun-bleached, precise, warm — not a sword-and-sandal set.

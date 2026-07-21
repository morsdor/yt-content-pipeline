# After Effects Workflow — AI-Assisted, Hand-Animated

*Part of the [pipeline docs](../pipeline_automation.md). This IS the animation stage
(the Narration stage of [production_workflow.md](production_workflow.md)). AI generates the assets
and the instructions; you (and AE's deterministic transforms) produce the motion.
Nothing generative ever touches the moving pixels — that's why it stays sharp.*

## The verdict on the approach

Pre-generating a reusable AI asset library + animating by hand in AE **is the correct
approach** — it's literally how Oversimplified, Kurzgesagt, and RealLifeLore work.
None of them draw per-frame animation. They maintain a library of flat illustrated
assets (characters, trees, forts, arrows, armies) and move them with position / scale /
rotation / puppet-pin keyframes. The style looks "simple" by *design*, because simple
shapes + good easing read as crafted, while complex generative motion reads as slop.

The compounding effect is the real payoff: video 1 might need 40 new assets;
video 10 might need 5, because the library already has soldiers, trees, water tiles,
arrows, and your narrator character.

## Division of labor

| Who | Does |
|---|---|
| **AI (generation)** | Stills, backgrounds, isolated elements on flat backgrounds, character part-sheets |
| **AI (Claude, in-session)** | Motion briefs per scene, exact keyframe recipes, AE **expressions** (copy-paste code), **JSX scripts** that build comps for you, troubleshooting from screenshots |
| **You + AE** | Placing layers, setting keyframes, easing, taste. AE transforms but never redraws → always sharp |

### The three AI levers (know all three — most people only use the first)

1. **Asset generation** — what you already do. The rule: *one element, flat background,
   consistent style anchor* (see generation rules below).
2. **AI as animation director** — per scene, Claude writes the brief: *"Layer stack:
   sky / stepwell / foreground wall. Camera: scale 100→106% over full duration, Easy Ease.
   Water layer: position y +8px oscillation via expression. Nothing else moves."*
   You execute; over time you stop needing the brief.
3. **AI writes code that runs inside AE** — this is the underused one:
   - **Expressions** (Alt-click a property's stopwatch, paste): `wiggle(0.4, 3)` for a
     bobbing boat, `loopOut("pingpong")` for water shimmer, time-driven drift for clouds.
   - **JSX scripts** (`File → Scripts → Run Script File…`): Claude can write a script
     that imports every PNG in a folder, lays out 50 soldiers in ranks with staggered
     bobbing, or builds the layer stack for a scene from a JSON motion brief.
     Repetitive setup should never be done by hand.

---

## Phase 0 — One-time setup (one weekend)

- [ ] Install After Effects (~$23/mo Single App) — or DaVinci Resolve (Fusion) free if trialing
- [ ] Learn exactly six things first, nothing else:
      composition, layer, transform shortcuts (`P` position / `S` scale / `R` rotation /
      `T` opacity / `A` anchor), keyframes + **Easy Ease (F9)**, pre-comps, parenting
- [ ] Install **Duik Ángela** (free) — character rigging, needed later for Rung-3 characters
- [ ] Build a **project template** `template.aep`:
      3840×2160 @ 30fps comp, folder bins (`bg / mid / fg / characters / props / overlays / audio`),
      one adjustment layer with subtle grain, one vignette layer — save, duplicate per video
- [ ] Download free overlay packs once: dust particles, light leaks, film grain, paper texture
      (drop into `assets_library/overlays/`) — set to Screen/Overlay blend mode, 10–20% opacity
- [ ] Watch ~2 hours of a beginner AE course (any "AE in 2 hours" video), then stop watching
      and build a scene — you learn AE by making scene 1, not by finishing courses

## Phase 1 — The asset library (ongoing; AI does the heavy lifting)

**Location:** `assets_library/` at repo root, shared across all videos.

```
assets_library/
  STYLE_BIBLE.md          # palette, line weight, iso angle, light direction
  INDEX.md                # Claude maintains: what exists, so briefs reuse instead of regenerate
  characters/             # part-sheets + rigged .aep per character
  nature/                 # trees, rocks, clouds, water tiles
  architecture/           # forts, walls, wells, temples, houses
  military/               # soldiers, elephants, banners, siege gear
  props/                  # pots, ropes, tools, carts
  diagram/                # arrows, labels, callout boxes, dotted paths (Oversimplified maps)
  overlays/               # dust, grain, light leaks (stock, not AI)
```

- [ ] Write `STYLE_BIBLE.md`: exact palette hexes, line weight, isometric angle (e.g. 30°),
      light from upper-left, texture amount. **Every** generation call references it + the
      anchor image — one off-style asset poisons every video that reuses it
- [ ] **Generation rules** (put these in every asset prompt):
      - ONE element per image, centered, no cropping at edges
      - flat solid background (pure white or green — models can't output true alpha)
      - same isometric angle + light direction as the style bible
      - generous margins (you'll trim), 2048px+ before upscale
- [ ] **Cutout pipeline** per asset: `rembg` (pip install; near-perfect on flat backgrounds)
      → trim → PNG with alpha → Real-ESRGAN 4× (`realesrgan-x4plus-anime`) → into the
      category folder with the naming convention `category_name_variant.png`
      (`military_soldier_spear_01.png`)
- [ ] **Character kits** (the Oversimplified move): generate a character as a *part sheet* —
      body, head (3–5 expressions), separate arms — rig ONCE with Duik or simple
      parenting + puppet pins, save as `characters/name_rig.aep`, reuse forever.
      Simple round-head dot-eye characters are a *feature*: they rig in minutes and
      the audience reads them as intentional style
- [ ] **Backgrounds generated wide** — 20–30% wider than 16:9 framing so camera moves
      never hit the edge; for parallax scenes, also generate clean plates
      ("same scene without the tower" → the tower becomes its own layer)
- [ ] After each generation batch, Claude updates `INDEX.md` — before generating anything
      new, check the index first. Reuse beats regenerate for both cost and consistency

## Phase 2 — Per-video process (the AE build stage of the production workflow)

- [ ] **The board arrives finished** (studio-director chain, `docs/storyboard_schema.md`):
      every scene carries its numeric `camera{}` + `layers[].motion{}` specs
      (motion-director pass) and its `ae_build{}` blueprint — hierarchy, precomps,
      expressions, render spec (ae-director pass). `shot_list.md` is the readable
      session plan. The old post-hoc `--motion-briefs` step is gone: **the board IS
      the brief.** Plates are validated (accuracy gate), assets are in the library,
      the VO is recorded and timings are trued-up — you animate to track.
- [ ] Build scenes in AE using the ladder — never skip rungs:
      - **Rung 1 — camera** (every scene): the board's `camera{}` numbers (push 4–6%,
        pan 40–80 px/s), Easy Ease. This alone ships a full, crafted-looking video
      - **Rung 2 — parallax** (hero scenes): 3–4 separated layers, background moves less
        than foreground (bg 0.25× of fg distance)
      - **Rung 3 — element motion** (2–3 scenes/video max): water level, light sweep,
        flag ripple, character gesture, map arrow drawing on
- [ ] Save each finished **build family** as a **template comp** (`fam_map_route`,
      `fam_plate_push`, `fam_stage`) — next video, duplicate and swap the art. By video 5
      you're assembling, not animating
- [ ] Render scenes → `projects/XXX/clips/scene_NN.mp4` — native 4K, 30fps, **~1s handles
      both ends**. Final conform happens in **Premiere Pro** (the conform stage): clips on the VO
      at their `t_start` marks, trim into the handles, cuts on narration beats

## Phase 3 — Using AI while you're inside AE

- Stuck on a look → describe it or screenshot the comp/timeline; Claude names the exact
  property/effect and values
- Anything repetitive ("bob these 40 layers with random offsets") → ask for a JSX script
  or an expression instead of doing it manually. Scripts live in `ae_scripts/`
  (first one: `build_practice_scene_01.jsx` — assembles the practice establishing shot);
  run via `File → Scripts → Run Script File…`
- Anything mathematical (ease curves, drift speeds, loop periods) → Claude computes
  keyframe values; you type them in
- Keep a running `docs/ae_recipes.md`: every solved problem gets its 3-line recipe.
  After ~10 scenes this becomes your personal AE manual

## Quality gates (extends the visual-accuracy gate)

- [ ] **Asset gate** — before an asset enters the library: style-bible match, geometry
      accurate, clean alpha edge. Library assets are load-bearing across many videos
- [ ] **Motion gate** — per scene: *every* keyframe pair is eased (linear motion = the #1
      amateur tell), max 1–2 moving elements per scene, 0.5–1s hold before and after moves
- [ ] **Consistency gate** — the same character/object across scenes is the same FILE,
      never a fresh generation

## Learning ladder (calibrated expectations)

| When | You can do | Ship? |
|---|---|---|
| Week 1–2 | Rung 1 camera moves + grain overlay | Yes — a full video, already better than generative i2v ever looked |
| Week 3–4 | Rung 2 parallax on 3–5 hero scenes | Yes |
| Month 2 | Rung 3 element motion; first rigged character | Yes |
| Month 3+ | Duik walk cycles, Oversimplified-style map sequences | Yes |

First scene will take ~2 hours. Tenth scene ~15 minutes. That's normal — templates and
the asset library are what flatten the curve, not talent.

---
name: the-engineering-atlas-video
description: >-
  Use when producing a new video for the "The Engineering Atlas" YouTube channel —
  the full per-video pipeline from topic research through publish. Trigger on requests
  like "make a new Engineering Atlas video", "start a video on [topic]", "new episode",
  "next video", or when working inside a projects/NNN_topic folder. Enforces the
  mandatory human gates (research, fact-check, own narration, disclosure) that keep the
  channel monetizable and on-brand.
---

# The Engineering Atlas — Per-Video Production Checklist

The repeatable core process for every video. **2 videos/month, quality over quantity.**
Companion references: `brand_guide.md` (voice + look), `pipeline_automation.md` (tech hub →
links into `docs/`), `animation_upgrade.md` (motion), `channel_strategy.md` (titles, pillars,
topic list). Companion skills: `asset-generation` (Phases 2+3: stills → gate → Kling animation),
`visual-accuracy-gate` (still/clip validation), `thumbnail-workflow` (packaging gate +
candidates + A/B + log).

> **Three rules that override everything:** (1) You research and fact-check — AI drafts, you verify.
> (2) You record your own narration. (3) You add a perspective only you would. These are what keep
> the channel authentic under YouTube's inauthentic-content policy. Never skip them for speed.

---

## Pre-flight (once, before your first video)

- [ ] Fonts installed in `assets/fonts/` (Fraunces, IBM Plex Sans, IBM Plex Mono)
- [ ] Style anchors: **none needed upfront.** Use `style_card.txt` alone for video #1, then promote its 8–10 best frames into `assets/style_anchors/` (see anchor_prompts.md)
- [ ] `style_card.txt` present (master prompt prefix)
- [ ] **Kling MCP** connected (custom connector via `https://kling.ai/mcp`) + **Gemini image API key** in `.env`; mic + Audacity/Adobe Podcast ready
- [ ] `video_assembler.py` runs on the example storyboard without errors

---

## Per-video workflow

### Phase 0 — Topic + Research + Fact-Check  ⏱ 2–4 hrs · HUMAN GATE
- [ ] Pick topic from the 50-topic list (`channel_strategy.md §7`) or a new one; note its **civilization accent color**
- [ ] Gather real sources — books, papers, museum/engineering references — not just an AI summary
- [ ] **Reference pack:** collect 5–15 real photos/plans of the structure into `projects/NNN_topic/references/` (Wikimedia, ASI/UNESCO, papers — keep source URLs) and write `references/visual_facts.md`: the *visually checkable* claims (geometry, counts, patterns, materials, orientation). These feed the storyboard's `visual_facts` fields and the Phase-2 accuracy gate.
- [ ] Write research notes: the **constraint** (why it was hard), the **mechanism** (how it worked), the **numbers** (verified), the **human angle** (who the witness is)
- [ ] Decide the **"what most people miss"** insight — your engineer's-eye take
- [ ] ✅ Gate: every date, tonnage, dimension, name, and mechanism is checked against a real source

### Phase 1 — Script + Storyboard  ⏱ 1–2 hrs

**1a — Script**
- [ ] Claude drafts a 10–12 min script **from your research notes**, following the §6 beat sheet (witness cold-open → problem → how → scale → your-take → callback → sign-off)
- [ ] **You rewrite** the hook and the 2–3 perspective paragraphs in your own voice
- [ ] Confirm the **witness/engineer/wit** braid (brand_guide §5); wit ≈ 1 dry beat / 60–90s, never gags
- [ ] Save `script.md` to `projects/NNN_topic/`

**1b — Storyboard (ONE fully-populated file, `scene_type` prepopulated)  ← REVIEW GATE**
- [ ] Claude writes a **single** `storyboard.json` (~54 scenes) with **every field populated at once** — including `scene_type` from the start. No narrative-only pass, no separate enrich pass, no second file.
- [ ] Each scene stays **lean** — only scene-specific content: `image`, `type` (animated/static), `duration`, `scene_type`, `motion`/`focus` (static only), `image_prompt` (**just the subject — what to draw this scene, no boilerplate**), optional `accent` (where the single highlight goes), `texts[]`, `narration_segment`. **Animated** scenes also carry `animated_clip` + `animation_prompt` (**just the motion**).
- [ ] **Accuracy fields:** scenes depicting the real structure get `visual_facts` (copied from `references/visual_facts.md` — must-be-true claims, not prompts) and `reference_image` (best-matching photo in `references/`). `prompt_builder.py` injects the facts into both image and animation prompts; `generate_images.py` passes the photo as a geometry reference alongside the style anchor (anchor = LOOK, photo = GEOMETRY). Abstract scenes (maps, force diagrams) get facts only, or neither.
- [ ] **Packaging-first gate (`thumbnail-workflow` skill, Stage 1):** before approving the storyboard, write the title + a one-sentence thumbnail concept ("dominant object + 3–4 words"). No compelling thumbnail concept = weak framing — fix the angle now, before any generation spend.
- [ ] The shared boilerplate is **NOT stored in the JSON.** `prompt_builder.py` composes the full prompt at generation time: `style_card.txt` prefix + the `scene_type` recipe (from the storyboard's `scene_recipes`) + the scene's subject + the `accent_hex` **variable** + a composition hint derived from `texts`/`motion`. Keeps every scene of a type consistent, the accent swappable, and the file small.
- [ ] ✅ Gate: read the one file end-to-end — scene order, durations, on-screen `texts`, the ~27/~27 animated/static split, and that each subject + motion reads right. It's one file; change freely.
- [ ] Preview the fully-composed prompts anytime with `python prompt_builder.py <sb>` (writes a readable `prompts.md` into the video folder — gitignored, regenerated on demand, never stored in the JSON). There is **no enrich step** — write the storyboard lean; `prompt_builder.py` + `generate_images.py` do the rest. (Field reference: `docs/storyboard_schema.md`.)

#### Storyboard format (the standard — `scene_type` prepopulated, single pass)

Top-level keys: `civilization`, `accent_hex` (**one variable**, set per video from brand_guide §3 — e.g. Indian `#D4812A`), `style_anchor_strength`, `scene_recipes` (the `scene_type` → recipe map — **this video's source of truth**, editable per video), `base_dir`, `voiceover`, `background_music`, `music_volume`, `scenes[]`. (`prompt_builder.py` reads `scene_recipes` from the storyboard, falling back to built-in defaults only if absent.)

**`scene_type` is a fixed vocabulary; `prompt_builder.py` maps each to its recipe fragment (from the storyboard's `scene_recipes`) when composing that scene's prompt:**

| scene_type | recipe fragment (visual DNA) |
|:---|:---|
| `establishing` | wide view, full structure in frame, sky/horizon context, sense of scale |
| `cross_section` | cutaway/section — ground sliced open, strata + water/level line visible, profile clarity (the channel's signature) |
| `detail` | tight isometric close-up on one element, shallow depth, texture emphasis |
| `scale_comparison` | subject beside a reference (tiny silhouettes / storey markers), measured framing |
| `map` | top-down cartographic schematic, muted region context, thin linework |
| `title` | hero-wide with clean negative space reserved for the wordmark |
| `outro` | calm receding wide with clean space for the subscribe card |

- **Accent is a variable, applied at generation — never hardcoded per scene.** Set `accent_hex` once; the generator highlights each scene's `accent` target with it, **sparingly** (neutral base elsewhere). Re-skinning for another civilization = change one value.
- **Still-first for Kling.** *Every* scene gets a still `image` first (pass a style anchor on each call for cross-scene consistency). For `animated` scenes that still is Kling's **starting frame** — `animation_prompt` adds motion only, never restyles. `static` scenes use Ken Burns via `motion`.
- **`texts` are overlaid by the assembler, not drawn into the image** (`style_card.txt` says "no text in image"). In the prompt, `texts` only dictate where to leave clean negative space.

### Phases 2 + 3 — Asset Generation (stills → gate → animation)  ⏱ 3–5 hrs
**→ Run the `asset-generation` skill** — it owns the whole chain; the stages below are the summary, the skill is the source of truth.
- [ ] **Stage 0 — Preflight:** `.env` key present; Kling MCP `who_am_i` + **credits check (blocking)** — estimate the batch from `--anim-jobs` total seconds before generating anything. Anchor rule: **video #1** = `style_card.txt` only; **video #2+** = pass a style anchor on every call.
- [ ] **Stage A — Stills:** `generate_images.py` — dry-run → scene 1 (eyeball) → rest. Same session, same model version. Scenes with `reference_image` get the real photo as geometry reference automatically.
- [ ] **Stage B — ✅ VISUAL ACCURACY GATE (hard gate):** `visual-accuracy-gate` Layer 2 — vision compare, you confirm, delta-prompt fixes, `validation_report.md`. **No still goes to Kling unvalidated.**
- [ ] **Stage C — Animation via Kling** (`kling-cli` or MCP): `--anim-jobs` prep → **user confirms batch + credits (every job charged, no trial runs)** → per job: upload still → `image_to_video` with **`--model kling-video-v3_0 --resolution 720p --enable_audio false`** (6 cr/s, no audio, best element consistency; 6s-capable) → **log every `generationId`** (no server-side task list — a lost id orphans a charged job) → `query_tasks` → **download within 24h** → scrub-check (Layer 3: accuracy *and* polish) → one retry → Ken Burns fallback (retag `type:"static"`).
- [ ] **Stage C.5 — Flicker hybrid (measure, don't guess):** after the batch, `python flicker_check.py projects/NNN_topic/clips/*.mp4` → **re-generate only the flagged (`flicker_HF > 3`) scenes at `--resolution 1080p`** (8 cr/s). Dense lattice/steps in motion shimmer at 720p and the free upscaler can't fix it; smooth scenes stay 720p. ~⅓ of scenes typically cross → ~1,440 cr/video. Details: [docs/upscaling.md](../docs/upscaling.md).
- [ ] **Stage D:** upscale to 4K locally & free — static stills *and* clips (`python upscale_video.py …`), per [docs/upscaling.md](../docs/upscaling.md). Free substitute for native-4K credits.
- [ ] (After ~5–8 videos: train a LoRA for cross-video brand lock)

### Phase 4 — Particles + Overlays  ⏱ 20 min
- [ ] Tag ~10 scenes for dust/sparks/rain stock overlays (atmosphere, ~20–30% opacity)
- [ ] Confirm text callouts use brand fonts + the video's accent color (brand_guide §4, §7)

### Phase 5 — Record Narration  ⏱ ~30 min · HUMAN GATE
- [ ] Record the fact-checked script yourself; ~140–150 wpm; let key numbers breathe
- [ ] Clean up (noise removal, leveling); splice ElevenLabs clone **only** for pickups
- [ ] End with the consistent sign-off (brand_guide §5)
- [ ] Save `audio/voiceover.mp3`

### Phase 6 — Assemble  ⏱ ~10 min
- [ ] `python video_assembler.py --storyboard ./projects/NNN_topic/storyboard.json --output ./projects/NNN_topic/output/final_video.mp4` — default **1080p** for a fast review render; add **`--resolution 2160p`** for the 4K publish master (feed it the Stage-D 4K clips + stills, else the 4K work is downscaled away). 4K assembly is ~4× slower.
- [ ] Check crossfades, text timing, music at ~8%

### Phase 7 — QA + Disclosure + Publish  ⏱ 30–45 min
- [ ] Watch it **fully** at least once (facts + feel, not just glitches)
- [ ] **Polish pass** (the "does it look sloppy?" gate — full-video version of accuracy-gate Layer 3b): motion reads as intended (no warp/melt/shimmer), cuts land clean, text timing tracks narration, music sits under the voice, pacing doesn't drag. Accurate ≠ not-cheap; this catches cheap.
- [ ] Thumbnails: **run the `thumbnail-workflow` skill, Stages 2–5** — 3 candidates varying ONE axis, 120-px squint test, Fraunces bold added locally (never AI text), YouTube **Test & Compare**, and the `assets/thumbnails_log.md` entry.
- [ ] Title (per formula, `channel_strategy.md §4`) + description (hook → chapters → **sources** → subscribe)
- [ ] Cut **2–3 Shorts** from self-contained beats (cross-section reveal, scale comparison, detail zoom): 9:16 crop, 15–45s, hook overlay in the first second, end-card to the full video. Drip them between uploads; judge by subs gained + long-form click-through, not Shorts views.
- [ ] ✅ **Tick "Altered content"** on upload (AI-assisted visuals/voice)
- [ ] Schedule for your consistent slot (e.g., Saturday AM US)

---

## Definition of Done (the brand test)

Do not publish unless all five are true:

1. **Look** — on-brand palette, fonts, isometric style, consistent across all scenes
2. **Sound** — your real voice, witness+engineer braid, dry wit, clean audio, sign-off
3. **Accuracy** — every fact verified against a real source
4. **Visual truth** — every depiction of the real structure passed the reference-photo check; no invented geometry survived to render
5. **Perspective** — a genuine "what most people miss" insight only you would frame this way

Missing any one = not ready. Quality over the calendar.

---

## Time budget

~8–12 hrs/video → ~16–24 hrs/month for 2 videos (the phases above sum to this; the first 3–5 videos will run longer). Sustainable alongside a full-time job **at this cadence only**.
If a step balloons, cut scope (fewer scenes, more Ken Burns) — never cut the human gates.

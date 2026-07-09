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
Companion references: `brand_guide.md` (voice + look), `pipeline_automation.md` (tech),
`animation_upgrade.md` (motion), `channel_strategy.md` (titles, pillars, topic list).

> **Three rules that override everything:** (1) You research and fact-check — AI drafts, you verify.
> (2) You record your own narration. (3) You add a perspective only you would. These are what keep
> the channel authentic under YouTube's inauthentic-content policy. Never skip them for speed.

---

## Pre-flight (once, before your first video)

- [ ] Fonts installed in `assets/fonts/` (Fraunces, IBM Plex Sans, IBM Plex Mono)
- [ ] Style anchors: **none needed upfront.** Use `style_card.txt` alone for video #1, then promote its 8–10 best frames into `assets/style_anchors/` (see anchor_prompts.md)
- [ ] `style_card.txt` present (master prompt prefix)
- [ ] Kling + Gemini image + filesystem MCPs connected; mic + Audacity/Adobe Podcast ready
- [ ] `video_assembler.py` runs on the example storyboard without errors

---

## Per-video workflow

### Phase 0 — Topic + Research + Fact-Check  ⏱ 2–4 hrs · HUMAN GATE
- [ ] Pick topic from the 50-topic list (`channel_strategy.md §7`) or a new one; note its **civilization accent color**
- [ ] Gather real sources — books, papers, museum/engineering references — not just an AI summary
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
- [ ] The shared boilerplate is **NOT stored in the JSON.** `generate_assets.py` composes the full prompt at generation time: `style_card.txt` prefix + the `scene_type` recipe + the scene's subject + the `accent_hex` **variable** + a composition hint derived from `texts`/`motion`. Keeps every scene of a type consistent, the accent swappable, and the file small.
- [ ] ✅ Gate: read the one file end-to-end — scene order, durations, on-screen `texts`, the ~27/~27 animated/static split, and that each subject + motion reads right. It's one file; change freely.
- [ ] Preview the fully-composed prompts anytime with `python generate_assets.py --storyboard <sb> --dump-prompts` (writes a readable `prompts.md`). There is **no enrich step** — write the storyboard lean; the generator does the rest. (Field reference: `pipeline_automation.md` → Storyboard JSON Schema.)

#### Storyboard format (the standard — `scene_type` prepopulated, single pass)

Top-level keys: `civilization`, `accent_hex` (**one variable**, set per video from brand_guide §3 — e.g. Indian `#D4812A`), `style_anchor_strength`, `base_dir`, `voiceover`, `background_music`, `music_volume`, `scenes[]`. (The `scene_type` recipe table lives in `generate_assets.py` as brand-level config, applied at generation — not copied into every video.)

**`scene_type` is a fixed vocabulary; `generate_assets.py` maps each to a locked recipe fragment when it composes that scene's prompt:**

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

### Phase 2 — Images  ⏱ 1–2 hrs
- [ ] Run `python generate_assets.py --storyboard projects/NNN_topic/storyboard.json --only image` (Gemini "nano banana"; composes prompts from the lean storyboard + `style_card.txt`). Do scene 1 first as the in-video reference, eyeball it, then generate the rest.
- [ ] **Video #1:** `style_card.txt` prefix only (no anchors exist yet). **Video #2+:** also pass a matching style anchor on every call (locks the look)
- [ ] Same session, same model version for within-video consistency
- [ ] Review; regenerate off-style frames; upscale static-scene images to 4K for Ken Burns headroom
- [ ] (After ~5–8 videos: train a LoRA for cross-video brand lock)

### Phase 3 — Animation (~27 scenes)  ⏱ 2–3 hrs
- [ ] For each `animated` scene: upload still to Kling, use the storyboard's animation prompt, get a 5–8s clip
- [ ] **Graceful degradation:** if a clip won't come out right after ~2 tries, retag the scene `static` and let it be Ken Burns + overlay. A clean Ken Burns beats a glitchy animation. You always ship.
- [ ] Save clips to `projects/NNN_topic/clips/`

### Phase 4 — Particles + Overlays  ⏱ 20 min
- [ ] Tag ~10 scenes for dust/sparks/rain stock overlays (atmosphere, ~20–30% opacity)
- [ ] Confirm text callouts use brand fonts + the video's accent color (brand_guide §4, §7)

### Phase 5 — Record Narration  ⏱ ~30 min · HUMAN GATE
- [ ] Record the fact-checked script yourself; ~140–150 wpm; let key numbers breathe
- [ ] Clean up (noise removal, leveling); splice ElevenLabs clone **only** for pickups
- [ ] End with the consistent sign-off (brand_guide §5)
- [ ] Save `audio/voiceover.mp3`

### Phase 6 — Assemble  ⏱ ~10 min
- [ ] `python video_assembler.py --storyboard ./projects/NNN_topic/storyboard.json --output ./projects/NNN_topic/output/final_video.mp4`
- [ ] Check crossfades, text timing, music at ~8%

### Phase 7 — QA + Disclosure + Publish  ⏱ 30–45 min
- [ ] Watch it **fully** at least once (facts + feel, not just glitches)
- [ ] Thumbnail: one hero object 60%+, ≤4 words in Fraunces bold, structure-left/text-right, accent color (brand_guide §7)
- [ ] Title (per formula, `channel_strategy.md §4`) + description (hook → chapters → **sources** → subscribe)
- [ ] ✅ **Tick "Altered content"** on upload (AI-assisted visuals/voice)
- [ ] Schedule for your consistent slot (e.g., Saturday AM US)

---

## Definition of Done (the brand test)

Do not publish unless all four are true:

1. **Look** — on-brand palette, fonts, isometric style, consistent across all scenes
2. **Sound** — your real voice, witness+engineer braid, dry wit, clean audio, sign-off
3. **Accuracy** — every fact verified against a real source
4. **Perspective** — a genuine "what most people miss" insight only you would frame this way

Missing any one = not ready. Quality over the calendar.

---

## Time budget

~5–7 hrs/video → ~10–14 hrs/month for 2 videos. Sustainable alongside a full-time job.
If a step balloons, cut scope (fewer scenes, more Ken Burns) — never cut the four human gates.

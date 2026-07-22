---
name: the-engineering-atlas-video
description: >-
  Use when producing a new video for the "The Engineering Atlas" YouTube channel —
  the full per-video pipeline from topic research through publish. Trigger on requests
  like "make a new Engineering Atlas video", "start a video on [topic]", "new episode",
  "next video", or when working inside a projects/NNN_topic folder. Enforces the
  mandatory human gates (research, fact-check, own narration, disclosure) that keep the
  channel monetizable and on-brand. Pre-production runs through the studio-director
  chain; animation is hand-built in After Effects; final conform in Premiere Pro.
---

# The Engineering Atlas — Per-Video Production Checklist

The repeatable core process for every video. **2 videos/month, quality over quantity.**
Companion references: `brand_guide.md` (voice + look + §5 Motion Identity),
`docs/cinematography.md` (craft canon), `pipeline_automation.md` (tech hub → links into
`docs/`), `docs/after_effects_workflow.md` (motion build), `channel_strategy.md` (titles,
pillars, topic list). Companion skills: **`studio-director`** (pre-production: the seven-pass
board), `asset-generation` (derived generation + prep), `visual-accuracy-gate` (still/asset/
render validation), `thumbnail-workflow` (packaging gate + candidates + A/B + log),
`art-director` (bible keeper — consult when entering a new civilization).

> **Three rules that override everything:** (1) You research and fact-check — AI drafts, you verify.
> (2) You record your own narration. (3) You add a perspective only you would. These are what keep
> the channel authentic under YouTube's inauthentic-content policy. Never skip them for speed.

---

## Pre-flight (once, before your first video)

- [ ] Fonts installed in `assets/fonts/` (Fraunces, IBM Plex Sans, IBM Plex Mono)
- [ ] Style anchors: **none needed upfront.** Use `style_card.txt` alone for video #1, then promote its 8–10 best frames into `assets/style_anchors/` (see anchor_prompts.md)
- [ ] `style_card.txt` present (master prompt prefix)
- [ ] **After Effects** installed (+ Duik Ángela for characters later), `template.aep` built, and `assets_library/` seeded (STYLE_BIBLE + first batch) — see [docs/after_effects_workflow.md](../docs/after_effects_workflow.md) Phase 0
- [ ] **Premiere Pro** ready (final conform lives there — you already know it)
- [ ] **Gemini image API key** in `.env`; mic + Audacity/Adobe Podcast ready
- [ ] `video_assembler.py` runs on the example storyboard (it's the **animatic** tool now)

---

## Per-video workflow

```
PRE-PRODUCTION   PACKAGING (topic from the data · title · thumbnail — LOCKED)
                 → research → script → STUDIO (board)
PRODUCTION       VO + true-up → generate (derived) → animatic → AE build → render QC
DELIVERY         Premiere conform → QA + publish
```

## PRE-PRODUCTION

### Packaging Gate (topic + title + thumbnail, from the data)  ⏱ 30–45 min · ₹0 · HUMAN GATE

*The idea must prove it can be packaged **before** it earns a single production hour —
and topics are **sourced from evidence**, not brainstormed and then justified.*

- [ ] **Start from the database:** refresh if stale (`python3 scripts/weekly_refresh.py`), read the current top patterns (`scripts/tag_outliers.py` report — Claude tags new rows in-session for ₹0), and scan `data/outliers.csv` for breakouts adjacent to our lane (`docs/outlier_system.md`). Study the packaging-benchmark channels that never clear 3× (Johnny Harris, Wendover, Mustard) via their best-*relative* rows in `data/comp_videos.csv`.
- [ ] **Precedent check (hard):** the concept needs a **≥3× outlier precedent** on a comparable channel — in the CSV, or found live via vidIQ. No precedent anywhere → **park it** (back to the `channel_strategy.md §7` list) and pick again. Parked ≠ killed: the weekly refresh promotes late bloomers.
- [ ] **Demand check (both axes):** a precedent proves the *packaging* can lift — also read its `views_per_day`. A high `multiple` at low views/day is a small channel over-performing a niche, not proof the *subject* pulls; prefer precedents strong on **both**. And discount a formula count that's really a channel's house format (base rates in `data/comp_videos.csv` — F12 from an 80%-cutaway channel isn't lift; see `formula_library.md` caveats).
- [ ] **Titles:** ~25 candidates from `formula_library.md` (weighted toward the tagger's top-3 patterns) → adversarial pass as a bored scroller — kill anything that needs context, over-promises, or reads as homework → **3 survivors**
- [ ] **Thumbnail concept:** one sentence — *"dominant object + 3–4 words"* — plus a quick 120-px mock check (`thumbnail-workflow` Stage 1). No compelling thumbnail = weak framing → fix the angle or park the topic.
- [ ] **Lock it:** `projects/NNN_topic/packaging.md` — chosen title (+2 alternates), formula id, precedent rows (video id + multiple from the CSV), thumbnail concept. **No `packaging.md`, no research.**
- [ ] ✅ Gate: precedent shown · title locked · thumbnail articulated — packaging is now the brief the script must serve

### Research + Fact-Check  ⏱ 2–4 hrs · HUMAN GATE
- [ ] Topic arrives **already validated** from the **Packaging** gate (precedent + locked packaging); note its **civilization accent color**
- [ ] If the topic enters a new civilization/visual territory: **consult the `art-director` skill** — motif kit into the bibles before boarding
- [ ] Gather real sources — books, papers, museum/engineering references — not just an AI summary
- [ ] **Reference pack:** collect 5–15 real photos/plans into `projects/NNN_topic/references/` (Wikimedia, ASI/UNESCO, papers — keep source URLs) and write `references/visual_facts.md`: the *visually checkable* claims (geometry, counts, patterns, materials, orientation). These feed the board's `plate.visual_facts` and the accuracy gate.
- [ ] Write research notes: the **constraint** (why it was hard), the **mechanism** (how it worked), the **numbers** (verified), the **human angle** (who the witness is)
- [ ] Decide the **"what most people miss"** insight — your engineer's-eye take
- [ ] ✅ Gate: every date, tonnage, dimension, name, and mechanism is checked against a real source

### Script  ⏱ 1–2 hrs · HUMAN GATE
- [ ] Claude drafts a 10–13 min script **from your research notes**, following the beat sheet (brand_guide §7: witness cold-open → problem → how → scale → your-take → callback → sign-off)
- [ ] **You rewrite** the hook and the 2–3 perspective paragraphs in your own voice
- [ ] Confirm the **witness/engineer/wit** braid (brand_guide §6); wit ≈ 1 dry beat / 60–90s, never gags
- [ ] **Packaging drift check:** the script still delivers what the locked `packaging.md` (from Packaging) promises. If research pulled the story elsewhere, update the packaging *deliberately* — re-run the Packaging checks on the new angle — never let title and video drift apart silently.
- [ ] Save `script.md` to `projects/NNN_topic/` · ✅ Gate: the script is final enough to record

### Studio — the board  ⏱ 2–3 hrs · 3 HUMAN GATES
**→ Run the `studio-director` skill.** Seven passes fill one `storyboard.json` (v2) +
`shot_list.md`: script-analyzer (60–80 timestamped scenes of 8–12s) → film-director
(shots, sequence — **gate**) → storyboard-artist (frames) → scene-composer (plate/assembly
builds + layers — *generation becomes derived here*) → asset-planner (library diff + batch —
**gate, charged**) → motion-director (numeric motion) → ae-director (comp blueprints + JSX
scaffolds — **final board gate**). Schema: `docs/storyboard_schema.md`. Craft:
`docs/cinematography.md`. Nothing is generated during boarding.

## PRODUCTION

### Record Narration + True-Up  ⏱ ~45 min · HUMAN GATE
- [ ] Record the fact-checked script yourself (**before** any AE work — animate to track, `RHYTHM-1`); ~140–150 wpm; let key numbers breathe; consistent sign-off
- [ ] Clean up (noise removal, leveling); ElevenLabs clone **only** for pickups → `audio/voiceover.mp3`
- [ ] **True-up:** measure the real read; correct each scene's `t_start`/`t_end`/`duration`; set `vo_duration`; re-run `--validate`; flag scenes shifted >1.5s for a motion re-pace (studio-director handles)

### Generation (derived from the board)  ⏱ 2–4 hrs
**→ Run the `asset-generation` skill.** It executes what the board specifies — plates from
`plate{}` blocks (`generate_images.py`), library assets from the approved batch
(`generate_asset.py`), 4K upscale, layered-plate prep — and enforces the
**visual-accuracy-gate**: Layer 2 on every plate (vision vs reference + facts, your
verdicts), Layer 2.5 on every library asset. **No unvalidated art proceeds.**

### Animatic  ⏱ ~20 min
- [ ] `python video_assembler.py --storyboard <sb> --output <out>` — stills + VO, 1080p rough cut
- [ ] Watch once, full length. Pacing problems are fixed **in the board** (re-time/merge/cut scenes via studio-director), never at the AE desk (`ANIMATIC-2`)

### AE Build (YOU, hands-on)  ⏱ the craft hours
- [ ] Per scene's `ae_build{}` blueprint + the ae-director's session plan: run JSX scaffolds, build families together, keyframe per the numeric motion specs (brand §5 limits), Rung 1 everywhere / Rung 2 on 3–5 heroes / Rung 3 on 2–3 max
- [ ] Render `clips/scene_NN.mp4` — native 4K 30fps, **~1s handles both ends**
- [ ] Full guide: [docs/after_effects_workflow.md](../docs/after_effects_workflow.md)

### Render QC  ⏱ ~30 min
- [ ] `visual-accuracy-gate` Layer 3 on each render — easing, restraint (≤2 moving), clean first/last frames, asset consistency, continuity registry, comprehension. Fixes are free (tweak comp, re-render); a scene not worth more AE time simplifies to its Rung-1 camera-only version — you always ship.

## DELIVERY

### Premiere Conform  ⏱ ~1 hr
- [ ] New Premiere project: drop `voiceover.mp3` + music (~8%, brand §9) on the timeline; lay `clips/scene_NN.mp4` in order at their `t_start` marks (shot_list has the column); trim into the handles so every cut lands on the narration beat (`RHYTHM-2`)
- [ ] Transitions per the board: cuts default; crossfades only where `transition_in` says so; check the match-cuts align
- [ ] Export the 4K publish master (H.264, YouTube 2160p preset)

### QA + Disclosure + Publish  ⏱ 30–45 min
- [ ] Watch it **fully** at least once (facts + feel, not just glitches)
- [ ] **Polish pass** (the "does it look sloppy?" gate): motion reads as intended (eased, subtle, nothing linear or busy), cuts land clean, text timing tracks narration, music sits under the voice, pacing doesn't drag
- [ ] Thumbnails: **`thumbnail-workflow` Stages 2–5** — 3 candidates varying ONE axis, 120-px squint test, Fraunces bold added locally (never AI text), YouTube **Test & Compare**, log entry
- [ ] Title = the one locked in `packaging.md` back in **Packaging** (formulas: `formula_library.md`; verify it still matches the final cut) + description (hook → chapters → **sources** → subscribe)
- [ ] Cut **2–3 Shorts** from self-contained beats (cross-section reveal, scale comparison, detail zoom): 9:16, 15–45s, hook overlay first second, end-card to the full video
- [ ] ✅ **Tick "Altered content"** on upload (AI-assisted visuals/voice)
- [ ] Schedule for your consistent slot (e.g., Saturday AM US)
- [ ] **Seed where Tier-1 lives** (`channel_strategy.md §4b`): HN / relevant subreddits / engineering Twitter — **never** Indian WhatsApp/LinkedIn (the first viewers train the lookalike model)
- [ ] **Geography check (§4b):** Studio → Audience → Top geographies — US+UK+CA+AU tracking toward **≥50% by ~video 10**; drifting → correct framing/seeding within the next two videos

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

~10–14 hrs/video → ~20–28 hrs/month for 2 videos (research 2–4, script 1–2, board 2–3,
VO ~1, generation 2–4 wall-clock, AE build is the variable craft block, conform+publish ~2;
the first 3–5 videos run longer while template comps accumulate). Sustainable alongside a
full-time job **at this cadence only.** If a step balloons, cut scope — fewer Rung-2/3
scenes, camera-only builds — **never** cut the human gates.

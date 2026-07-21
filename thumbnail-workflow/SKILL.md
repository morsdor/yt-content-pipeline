---
name: thumbnail-workflow
description: >-
  Use when creating, testing, or reviewing thumbnails for an Engineering Atlas video.
  Trigger on "make the thumbnails", "thumbnail candidates", "run the thumbnail
  workflow", "packaging gate", the Thumbnails step of the production workflow, or the
  Packaging gate's check that precedes all research spend. Produces 3 candidates varying one
  axis, applies the 120-px squint test, prepares them for YouTube Test & Compare,
  and logs outcomes to assets/thumbnails_log.md so CTR learning compounds.
---

# Thumbnail Workflow — Packaging as a First-Class Craft

**Why this exists:** at 2 videos/month there are only 24 at-bats a year — each video's CTR is existential. Packaging (thumbnail + title) is the highest-leverage skill in the whole plan, so it gets a procedure and a dataset, not vibes.

Brand rules live in `brand_guide.md` §7; strategy rationale in `channel_strategy.md` §3. This skill is the *executable* version.

---

## Stage 1 — Packaging-first gate (BEFORE research, script, or any other spend)

- [ ] **Precedent first:** the concept has a **≥3× outlier precedent** on a comparable channel (`data/outliers.csv`, or live via vidIQ — see `docs/outlier_system.md`). No precedent → park the topic; don't package it.
- [ ] Write the **title** (from `formula_library.md`, weighted toward the tagger's current top-3 patterns) and a **one-sentence thumbnail concept**: *"dominant object + 3–4 words"* — e.g. "a glowing aqueduct cross-section + 'HOW HIGH?'".
- [ ] **Rule: no compelling thumbnail concept = weak framing.** Don't wordsmith the thumbnail — fix the video's *angle* (or park the topic), then return. This gate blocks research spend.
- [ ] Lock title + concept into `projects/NNN_topic/packaging.md`; the Thumbnails step executes the concept later.

## Stage 2 — Generate 3 candidates (`output/thumb_a/b/c.png`)

- [ ] Base prompt (thumbnails are NOT video-scene prompts — no style card prefix):

```
Dramatic isometric illustration of [key structure/moment], vibrant [accent color],
high contrast, bold composition, single focal point, cinematic lighting,
dark moody background, detailed and eye-catching, thumbnail style
```

- [ ] **Vary ONE axis only** across a/b/c — focal object, crop tightness, OR accent intensity. Vary all three and the A/B test teaches you nothing.
- [ ] A winning video still (already validated for accuracy) is a legitimate candidate base — punch up contrast/saturation rather than generating from scratch.
- [ ] Generate at 1280×720 minimum (YouTube's native thumbnail size), 16:9.

## Stage 3 — The 120-px squint test (every candidate must pass ALL)

Shrink each candidate to inbox size (~120px wide) and check:

- [ ] **One dominant object**, ≥60% of frame, instantly recognizable
- [ ] **≤4 words**, readable at 120px
- [ ] **Focal point survives the shrink** — no fine detail carrying the meaning
- [ ] **Pops against BOTH** YouTube dark and light UI
- [ ] **Curiosity gap intact** — intrigues, doesn't answer

Quick preview: `magick thumb_a.png -resize 120x thumb_a_120.png` — view all three side by side. A candidate that fails goes back to Stage 2; do not "fix it in text."

## Stage 4 — Typography (local, never AI)

- [ ] Text added locally with real fonts — **Fraunces bold** (brand_guide), never AI-generated lettering:

```bash
magick output/thumb_a.png \
  -font Fraunces-Bold -pointsize 120 -fill "#FAF7F2" \
  -stroke "#2C2C2C" -strokewidth 4 \
  -gravity east -annotate +60+0 "HOW\nDEEP?" \
  output/thumb_a.png
```

- [ ] Consistent layout across the channel: structure one side, text the other — same side every video (pick once, stick with it).
- [ ] Accent color = the video's civilization accent (`accent_hex` from the storyboard).

## Stage 5 — Test & Compare + the log

- [ ] Upload **all 3** via YouTube Studio → Thumbnail → **Test & Compare**; YouTube picks the winner by watch-time share (needs ~2 weeks of traffic — let it finish).
- [ ] Log the run in `assets/thumbnails_log.md` (create on first use):

```markdown
| # | Video | Concept ("object + words") | Axis varied | Winner | CTR @7d | CTR @28d | Lesson |
|:--|:------|:---------------------------|:------------|:-------|:--------|:---------|:-------|
| NNN | (video) | glowing aqueduct cutaway + "HOW HIGH?" | crop tightness | b (tight) | 4.2% | 3.8% | e.g. "tighter crop wins in this niche" |
```

- [ ] **The log is the point.** At 24 videos/year it becomes the channel's most valuable dataset — the niche's visual language, learned instead of guessed. Fill in the 7/28-day CTR retroactively (calendar reminder or ask during the next video's Thumbnails step).
- [ ] Recycle losing variants as community-post images and Shorts covers — never waste a validated render.

---

## Rules that override everything

1. **The packaging gate blocks research spend** (it runs first) — no precedent + no concept = no production hours, not even research.
2. **One axis per A/B** — an untestable test is wasted traffic.
3. **Typography is always local and human** — AI text in thumbnails reads as slop at a glance.
4. **Log every run** — a thumbnail without a log entry taught you nothing.

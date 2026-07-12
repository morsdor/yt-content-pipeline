# Production Workflow (2 videos/month)

*Part of the [pipeline docs](../pipeline_automation.md). The agent-driven version of this workflow is the [`the-engineering-atlas-video` skill](../the-engineering-atlas-video/SKILL.md); the accuracy steps are the [`visual-accuracy-gate` skill](../visual-accuracy-gate/SKILL.md).*

Produce videos in a steady rhythm — one focused block per video, ~2 videos worth of work spread across the month. **Do not batch 4–6 in a weekend**; that guarantees either burnout or shallow fact-checking, and the templated-batch signature is what YouTube's inauthentic-content enforcement flags.

## Session 0: Research + Fact-Check (2–4 hours, non-negotiable)

```
For the topic:
  → Gather real sources (books, papers, museum/engineering references), not just AI summary
  → Collect 5–15 REAL photos/plans into projects/XXX/references/ and write
    references/visual_facts.md (see the visual-accuracy-gate skill) — these feed
    the storyboard `visual_facts` fields and the validation gate later
  → Claude drafts the script from your research notes
  → YOU verify every date, tonnage, mechanism, name, and attribution against sources
  → YOU rewrite the hook + 2–3 paragraphs with your own engineering perspective
  → This step is what makes the video authentic, accurate, and monetizable
```

## Session 1: Scripting / Storyboard (1–2 hours)

```
For the topic (using your fact-checked research notes from Session 0):
  → Open Claude Desktop
  → Prompt: "Using these research notes, write a 10-min script about [topic].
     Output storyboard.json with ~54 scenes, tagging ~27 'animated' and ~27 'static'."
  → Claude generates script + storyboard
  → Save to projects/XXX/storyboard.json + script.md
  → You've already fact-checked in Session 0 — here you polish the hook and
    your perspective paragraphs so they're in your voice, not the LLM's.
  → PACKAGING-FIRST GATE: before approving the storyboard, write the title and
    sketch the thumbnail concept (one sentence: "dominant object + 3–4 words").
    If no compelling thumbnail concept exists, the framing is weak — fix the
    angle NOW, before spending on images and animation.
```

## Session 2: Image Generation (1–2 hours, can run while doing other work)

*Sessions 2 + 3 are executable end-to-end as the [`asset-generation` skill](../asset-generation/SKILL.md) — say "generate the assets" after storyboard approval.*

```
For the project:
  → Open Claude Desktop
  → Prompt: "Generate all images for storyboard.json in projects/XXX/,
     passing anchor_01.png as style reference on every call"
     (see docs/image_generation.md → Style Consistency)
  → Claude calls Gemini MCP ~55x (scenes with reference_image also get the real
    photo passed as a geometry reference — automatic via generate_images.py)
  → Review images: accept or regenerate (flag style inconsistencies)
  → VISUAL ACCURACY GATE (hard gate — run the visual-accuracy-gate skill):
     → Claude vision compares each still against its reference photo + visual_facts
     → You confirm the flags (~15–20 min for a full video)
     → Failures: regenerate with a corrective DELTA prompt naming the error —
       one pass usually fixes it
     → NO still goes to Kling unvalidated (animation inherits every still error)
  → Upscale accepted static-scene images to 4K
```

## Session 3: Animation (2–3 hours, semi-automated)

```
For the project:
  → For each "animate" scene in storyboard (~27):
     → Upload VALIDATED still to Kling AI (web UI or API) — never an unvalidated one
     → Set animation prompt from storyboard (carries the "do not add/remove/deform
       structural elements" clause + the scene's visual_facts automatically)
     → Generate clip (bias toward 6s — duration is the main cost lever; a 10s
       clip costs ~2× a 6s one)
     → SCRUB-CHECK (visual-accuracy-gate skill, Layer 3), two passes:
       3a ACCURACY — first / middle / last frame; compare last frame to the
          source still. Kling's residual failure mode is morphing geometry
          mid-motion. ~20 seconds per clip.
       3b POLISH — does it look sloppy? shimmer, uncanny/too-fast motion, cut
          pops, wandering accent. Run `python flicker_check.py clips/*.mp4`;
          scenes scoring >3 (dense lattice/steps in motion) get re-generated at
          1080p — the free upscaler can't fix that shimmer.
     → Review: accept, or ONE retry with tightened motion ("parallax and drifting
       haze only") / a 1080p re-gen for a flicker fail
     → GRACEFUL DEGRADATION: after the one retry, retag that scene as "static"
       and let it be Ken Burns + overlay. The fallback is accurate by
       construction — it IS the validated still. A clean Ken Burns scene beats
       a glitchy animation, and you always ship.
     → Save to projects/XXX/clips/
  → Tip: queue all animations at once, review after all complete
```

## Session 4: Voice Recording (~30 min)

```
For the project:
  → Record narration yourself into your mic (see docs/voice_narration.md)
  → Clean up in Audacity / Adobe Podcast
  → (Optional) splice in ElevenLabs clone pickups for any changed lines
  → Save voiceover.mp3 to projects/XXX/audio/
```

## Session 5: Assembly (automated, ~8 min)

```bash
# review render (fast, 1080p default)
python video_assembler.py \
  --storyboard "./projects/XXX/storyboard.json" \
  --output "./projects/XXX/output/review.mp4"

# publish master (4K — feed the Stage-D 4K clips/stills)
python video_assembler.py \
  --storyboard "./projects/XXX/storyboard.json" \
  --output "./projects/XXX/output/final_video.mp4" --resolution 2160p
```

## Session 5b: Thumbnails (~30–45 min — this is a growth lever, not an afterthought)

*Executable version: the [`thumbnail-workflow` skill](../thumbnail-workflow/SKILL.md).*

```
For the video (concept was already approved at the Session-1 packaging gate):
  → Generate 3 CANDIDATES (thumb_a/b/c.png) from the thumbnail prompt pattern,
    varying ONE axis at a time: focal object, crop tightness, or accent intensity
    (not all three — otherwise the A/B test teaches you nothing)
  → The 120-px squint test on each candidate (shrink it to inbox size):
     □ one dominant object, ≥60% of frame, instantly recognizable
     □ ≤4 words, readable at 120px
     □ focal point survives the shrink (no fine detail carrying the meaning)
     □ pops against BOTH YouTube dark and light UI
     □ curiosity gap intact — intrigues, doesn't answer
  → Text/typography added locally (ImageMagick/Figma) — never AI-generated text
  → Upload all 3 via YouTube "Test & Compare" — it picks the winner by
    watch-time share
  → Log the result in assets/thumbnails_log.md: concept, which variant won,
    CTR at 7 and 28 days. At 24 videos/year this log becomes your most
    valuable dataset — it's how you learn YOUR niche's visual language
    instead of guessing.
```

## Session 6: QA + Disclosure + Publish

```
For the video:
  → Watch it FULLY (not 2x) at least once — you're checking facts and feel, not just glitches
  → Check: animation glitches, audio errors, factual claims, on-screen text
  → FEEL/POLISH (the "does this look sloppy?" pass — the per-clip version was
    Layer 3b): motion reads as intended (no warping/melt), cuts land clean, text
    timing tracks the narration, music sits under the voice, pacing doesn't drag.
    A video can be 100% accurate and still feel cheap — this is where you catch that.
  → On upload: TICK the "Altered content" checkbox (AI-assisted visuals/voice) — required
  → Write title (per formula) + description + tags
  → Publish/schedule on your consistent day/time (e.g., Saturday AM US)
```

**Time per video:** ~8–12 hours end to end, spread across the two-week cycle (that's what the sessions above actually sum to — the first 3–5 videos will run longer while the pipeline shakes out). Two videos ≈ **16–24 hours/month** — sustainable alongside a full-time job *only* at this 2/month cadence; this number is the real reason not to scale up early.

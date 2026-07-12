# The Storyboard JSON Schema

*Part of the [pipeline docs](../pipeline_automation.md). This is the contract between the script stage and the assembly stage.*

```json
{
  "base_dir": "./projects/001_roman_aqueducts",
  "voiceover": "audio/voiceover.mp3",
  "background_music": "audio/ambient.mp3",
  "music_volume": 0.08,
  "scenes": [
    {
      "image": "images/scene_01.png",
      "type": "animated",
      "animated_clip": "clips/scene_01_animated.mp4",
      "duration": 8,
      "texts": [
        { "text": "The Pont du Gard", "start": 1, "end": 4, "position": "center" },
        { "text": "50 km of gravity-fed water flow", "start": 4.5, "end": 7.5, "position": "bottom" }
      ],
      "scene_type": "establishing",
      "visual_facts": [
        "three tiers of arches, the smallest tier on top carrying the water channel",
        "lower tier has 6 arches, middle tier 11, top tier 35"
      ],
      "reference_image": "references/ref_01.jpg",
      "animation_prompt": "subtle parallax, clouds drifting, water visible in channel",
      "narration_segment": "In 19 BCE, Roman engineers completed something..."
    },
    {
      "image": "images/scene_02.png",
      "type": "static",
      "duration": 14,
      "motion": "pan_right",
      "texts": [
        { "text": "Three tiers of arches", "start": 2, "end": 7, "position": "top" },
        { "text": "Each bearing the weight above", "start": 7.5, "end": 13, "position": "bottom" }
      ],
      "scene_type": "cross_section"
    },
    {
      "image": "images/scene_03.png",
      "type": "animated",
      "animated_clip": "clips/scene_03_animated.mp4",
      "duration": 7,
      "texts": [],
      "scene_type": "detail",
      "animation_prompt": "water flowing right-to-left through channel, subtle ripples"
    }
  ]
}
```

## Field Reference

> **Two-pass storyboard.** The storyboard is built in two passes so you lock the *story* before any visual prompts are written:
> - **Pass 1 — Narrative** (what you review first): the structural/story fields only. No generation prompts.
> - **Pass 2 — Generation** (added *after* you approve Pass 1): the image/animation prompts and file paths.
>
> The `Pass` column below shows when each field appears. The assembler ignores the prompt fields (`image_prompt`, `animation_prompt`) — they're instructions for the image/animation steps, not for assembly.
>
> *(Note: the `the-engineering-atlas-video` skill currently writes the storyboard in a single fully-populated pass with lean per-scene fields — the field semantics below are identical either way.)*

| Field | Pass | Type | Required | Description |
|:---|:---|:---|:---|:---|
| `type` | 1 | string | ✅ | `"animated"` or `"static"` |
| `duration` | 1 | number | ✅ | Scene duration in seconds. **Animated: default 6–8s.** Duration is now a *time*-budget lever, not cash — a longer scene costs more AE build/render time ([costs.md](costs.md)); go 10s+ only when the motion needs it (route arrows, slow reveals). **Static (Ken Burns): 10–15s.** Any animated scene not worth AE time falls back to `type:"static"` Ken Burns (accurate by construction, free). |
| `scene_type` | 1 | string | ❌ | `establishing`, `cross_section`, `map`, `detail`, `scale_comparison` |
| `motion` | 1 | string | ❌ | Ken Burns motion for static scenes: `zoom_in`, `zoom_out`, `pan_left`, `pan_right`, `pan_up`, `zoom_detail` |
| `focus_x`, `focus_y` | 1 | number | ❌ | For `zoom_detail` only (0.0–1.0, default center) |
| `texts` | 1 | array | ❌ | Array of text objects: `[{"text": "...", "start": 2, "end": 6, "position": "bottom"}]`. Set to `[]` for no text |
| `narration_segment` | 1 | string | ❌ | Narration text for this scene (reference only) |
| `visual_facts` | 1 | array | ❌ | Must-be-true *visually checkable* claims for this scene, drawn from `references/visual_facts.md` (e.g. `"steps descend in paired V-flights"`). Injected into the image AND animation prompts by `prompt_builder.py`, and doubles as the accuracy checklist at the validation gate. Write these in Pass 1 — they're facts, not prompts. |
| `reference_image` | 2 | string | ❌ | Path to a real photo in `references/` for this scene. `generate_images.py` passes it alongside the style anchor (anchor = LOOK, reference = GEOMETRY) and it's the comparison image at the validation gate. Use for scenes depicting real, verifiable structures; omit for abstract diagrams/maps. |
| `image_prompt` | 2 | string | ❌ | Full still-image prompt (style card + subject + accent + composition). Added after Pass 1 approval. |
| `image` | 2 | string | ✅* | Relative path to the generated scene image (*required at assembly time) |
| `animation_prompt` | 2 | string | ❌ | The scene's **motion intent** — one sentence of what moves, how far, how slow (e.g. `"slow push-in; clouds drift right; water surface breathes"`). `prompt_builder.py --motion-briefs` expands it into the buildable After Effects shot direction, with `visual_facts` as hold-constraints. |
| `animated_clip` | 2 | string | ❌ | Path to the AE-rendered clip (required when type=animated, at assembly time) |
| `particle_overlay` | 2 | string | ❌ | Path to particle overlay clip (dust, sparks, rain) |

#!/usr/bin/env python3
"""
enrich_storyboard.py  —  Pass 1 (narrative) -> Pass 2 (enriched) for The Engineering Atlas.

Reads the narrative-only storyboard and adds, for every scene:
  - image            : path to the still (generated FIRST, for all 54 scenes)
  - image_prompt     : style-card prefix + scene_type recipe + subject + accent + composition
  - animated_clip    : (animated scenes only) Kling output path
  - animation_prompt : (animated scenes only) motion that starts FROM the still

Two consistency locks are applied uniformly here (this is the whole point of the file):
  1. STYLE_PREFIX + ACCENT_HEX are variables, injected identically into every prompt.
     -> the accent is NOT hardcoded per scene; change ACCENT_HEX once to re-skin a video.
  2. SCENE_RECIPES maps each scene_type -> a fixed prompt fragment, so all scenes of a
     given type share one visual DNA (alongside the assets/style_anchors reference image).

Run:  python3 enrich_storyboard.py
"""

import json, os

SRC = "storyboard_pass1_narrative.json"   # Pass-1 input
OUT = "storyboard.json"                    # Pass-2 output

# ── Per-video variables (change these to re-skin for another episode) ─────────
CIVILIZATION = "Indian"
ACCENT_HEX   = "#D4812A"   # saffron/ochre — Indian accent from brand_guide §3
STYLE_ANCHOR_STRENGTH = 0.7

# ── Global style-card prefix (verbatim from style_card.txt) ───────────────────
STYLE_PREFIX = (
    "Isometric flat-design technical illustration. Clean vector aesthetic, warm "
    "parchment background (#F5F0E8), precise geometric lines, charcoal dark elements "
    "(#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway "
    "style where relevant. Warm golden-hour ambient lighting with soft directional "
    "shadows. No humans visible (or tiny silhouettes for scale only). No text in image. "
    "High architectural precision. Educational diagram aesthetic. Quietly dramatic, "
    "awe-inspiring mood."
)

# ── scene_type -> locked recipe fragment (the "extra context" per type) ───────
SCENE_RECIPES = {
    "establishing":     "wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale",
    "cross_section":    "architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity",
    "detail":           "tight isometric close-up on a single element, shallow depth, texture and craft emphasis",
    "scale_comparison": "the structure beside a scale reference (tiny human silhouettes and/or storey markers), measured diagrammatic framing",
    "map":              "top-down cartographic schematic, muted regional context, thin technical linework",
    "title":            "hero-wide composition with generous clean negative space reserved for a title wordmark overlay",
    "outro":            "calm, receding wide composition with clean negative space reserved for a subscribe card overlay",
}

# ── Per-scene authored content, in FILE ORDER (1..54) ─────────────────────────
# key = a unique substring of that scene's narration (guards against drift)
# acc = where the single saffron highlight goes (None = neutral frame)
# anim = motion intent (used only if the scene is 'animated')
SCENE_DATA = [
    {"key":"Every morning","subj":"a lone village woman as a tiny silhouette at the rim of the vast square stepwell at dawn, the great inverted staircase falling away beneath her, first golden light on parchment-toned sandstone","acc":None,"anim":"very slow push-in toward the woman at the rim; soft dawn haze; faint parallax on the steps below"},
    {"key":"Down she goes","subj":"close isometric of the double-flight steps folding back on themselves, a single tiny silhouette a few steps down","acc":None,"anim":"slow downward drift following the descent; shadows shift gently"},
    {"key":"Yesterday it was thirty","subj":"clean sectional diagram of the stepwell with three faint horizontal waterlines marked high, mid and low, small step-count brackets beside each","acc":"the three waterline markers","anim":None},
    {"key":"She is not climbing","subj":"cutaway section of the stepwell, the water surface at mid-height, clearly a movable level meeting the steps","acc":"the water surface line","anim":"the water level glides up and down to 'meet' successive steps; subtle surface shimmer"},
    {"key":"and the staircase, three and a half","subj":"wide establishing view of the entire inverted-pyramid staircase from the rim, the full lattice of steps in golden light","acc":None,"anim":"slow sweeping parallax across the vast step lattice"},
    {"key":"The question was never","subj":"a single carved step edge sharp in the foreground, the deep well softly falling away behind, an open question implied","acc":None,"anim":None},
    {"key":"Title sting","subj":"hero-wide of Chand Baori in golden light with generous clean sky negative space across the top for the wordmark overlay","acc":None,"anim":"gentle slow push-in; dust motes catch the light"},
    {"key":"Here is the constraint","subj":"top-down cartographic schematic of arid north-west India / Rajasthan in tan tones, a small marker at Abhaneri near Jaipur, thin technical linework","acc":"the Abhaneri location marker","anim":None},
    {"key":"For a few weeks a year","subj":"wide arid Rajasthan landscape, a cracked dry riverbed, distant monsoon clouds massing on one horizon","acc":None,"anim":"monsoon clouds sweep in then pass; ground shifts damp-to-parched, time-lapse feel"},
    {"key":"And underground, the water table","subj":"earth cutaway showing the water-table as a distinct boundary between dry upper strata and saturated lower strata","acc":"the water-table line","anim":"the water-table boundary sinks slowly downward through the strata"},
    {"key":"A well is a simple thing","subj":"simple vertical well in section — a narrow shaft to a fixed water level, rope and bucket","acc":None,"anim":None},
    {"key":"But a well makes one assumption","subj":"the same vertical well, water beginning to drop below the fixed shaft bottom","acc":None,"anim":"water level slips downward, leaving the bucket over dry air"},
    {"key":"Dig your well down to the high-water","subj":"a well dug to the high-water mark, now a dry empty shaft in cracked summer strata","acc":"a small dry-hole marker at the shaft base","anim":"water retreats far below the shaft; faint heat shimmer"},
    {"key":"Dig instead to the summer low","subj":"a well dug to the summer low, flooded and overtopped after the monsoon, its draw point submerged","acc":"the drowned draw-point","anim":"water rises and floods over the well mouth"},
    {"key":"A single fixed depth","subj":"a minimalist diagram panel — a single fixed point versus a tall vertical range bracket","acc":"the vertical range bracket","anim":None},
    {"key":"That is the real problem","subj":"wide of Chand Baori sitting quiet in its landscape, the real problem framed","acc":None,"anim":None},
    {"key":"So they stopped trying to reach a point","subj":"concept cutaway — replacing one fixed platform with a continuous stair spanning a full vertical range beside the water column","acc":"the vertical range the stair covers","anim":"a highlight sweeps down the whole range, showing every level is covered"},
    {"key":"Picture the shape","subj":"clean section of the inverted pyramid, square mouth narrowing to the tank","acc":None,"anim":"the section reveals top-down; raking light crosses it"},
    {"key":"Roughly thirty-five metres","subj":"measured section with dimension markers: ~35 m across the mouth and ~20 m / ~13 storeys deep, a tiny human silhouette for scale","acc":"the dimension markers","anim":None},
    {"key":"Three of its four walls","subj":"three walls of double-flight steps meeting at the corners in the tessellated diamond lattice, isometric","acc":None,"anim":None},
    {"key":"And here is the elegant part","subj":"section with a single step highlighted exactly at the waterline","acc":"the active step at the waterline","anim":"as the water level shifts slightly, the highlighted 'active' step tracks to remain at the surface"},
    {"key":"In the flush weeks after the rains","subj":"section with water HIGH near the top after monsoon, a short descent, tiny silhouette near the rim","acc":"the high waterline","anim":"water sits high; the silhouette barely steps down to reach it"},
    {"key":"In the heart of summer","subj":"section with water LOW near the base in high summer, a long descent, tiny silhouette walking far down","acc":"the low waterline","anim":"the silhouette descends deep toward a low water level; dust in low light"},
    {"key":"The building never moves","subj":"section showing the building perfectly fixed while only the water surface moves up and down","acc":"the moving water surface","anim":"structure dead still; only the water level glides up and down"},
    {"key":"There's a second cleverness","subj":"extreme close isometric of dry-laid sandstone blocks with open mortarless joints, precise fit","acc":None,"anim":None},
    {"key":"That sounds like a shortcut","subj":"cutaway of the mortarless wall with fine groundwater threading through the joints into the tank from all sides","acc":"the seeping water threads","anim":"thin water threads trickle inward through the joints; the tank slowly fills"},
    {"key":"so the well fills from the whole body","subj":"section of the whole tank filling from the surrounding earth, not just the base","acc":"the inflow around the perimeter","anim":"water ingress glows around the full perimeter, level rising evenly"},
    {"key":"And a wall with no rigid mortar","subj":"the mortarless wall mid-tremor, blocks shifted a hair but holding, no cracks","acc":None,"anim":None},
    {"key":"No pumps. No moving parts","subj":"a spare diagrammatic emblem — no pump, no gear, a single downward gravity arrow over the well","acc":"the gravity arrow","anim":None},
    {"key":"The machine has exactly one instruction","subj":"wide of the whole machine at rest, one quiet instruction fulfilled","acc":None,"anim":None},
    {"key":"Stand at the rim","subj":"standing-at-the-rim view of the immense step lattice, the full scale landing","acc":None,"anim":"slow parallax as the eye falls into the lattice"},
    {"key":"Thirteen storeys of them","subj":"sweeping close of the hypnotic diamond step geometry, the most-photographed angle","acc":None,"anim":None},
    {"key":"a pattern so exact","subj":"tight on the mathematically exact lattice, near-fractal repetition of steps","acc":"a single highlighted lattice module","anim":None},
    {"key":"The fourth side","subj":"the north face — a tall multi-storey pillared gallery and royal pavilion rising opposite the stepped walls","acc":"the pavilion niche","anim":None},
    {"key":"Because this was never only waterworks","subj":"a tiny silhouette descending into the shaded lower levels where the light cools","acc":None,"anim":"slow descent; light temperature shifts from warm to cool shade"},
    {"key":"At the bottom it holds a temperature","subj":"diagram comparing hot surface air and cool base, a small thermometer motif at the bottom of the shaft","acc":"the cool-base marker","anim":None},
    {"key":"So the well was also a refuge","subj":"the shaded tank level as a communal refuge, tiny silhouettes gathered by the water","acc":None,"anim":None},
    {"key":"and where — beside a well named for a king","subj":"the Harshat Mata temple beside the well, a carved sandstone shrine","acc":"a small shrine highlight","anim":None},
    {"key":"And for most of its life","subj":"tiny silhouettes of women descending the steps at dawn with round water pots","acc":None,"anim":"figures move gently down the steps; long soft shadows lengthen"},
    {"key":"and travellers resting in the cool","subj":"travellers and pilgrims resting in the cool gallery, a calm wide","acc":None,"anim":None},
    {"key":"Here's what I think most people","subj":"a framed 'famous photograph' vignette of the lattice, inviting a second look","acc":None,"anim":None},
    {"key":"We look at Chand Baori and see a staircase","subj":"a reveal that reframes the staircase itself as the machine — the steps read as the working mechanism","acc":"the machine-active steps","anim":"a highlight ripples across every step so the whole stair reads as one mechanism"},
    {"key":"A vertical well solves a fixed-depth","subj":"side-by-side section — a fixed-depth well versus the range-spanning stepwell against a swinging water column","acc":"the swinging water column","anim":"the water column swings up and down; the fixed well fails while the stepwell keeps tracking it"},
    {"key":"Every one of those three and a half","subj":"section with many faint waterline candidates marked across the entire descent, each a potential surface","acc":"the array of potential waterlines","anim":"the waterline candidates light up one after another down the descent"},
    {"key":"It's an adaptive interface","subj":"a quiet endurance emblem — 'zero energy, over a thousand years' as a diagrammatic motif of the well enduring the seasons","acc":"the endurance marker","anim":None},
    {"key":"We tend to file buildings","subj":"a merely-'pretty' framing of the steps, about to be reread as function","acc":None,"anim":None},
    {"key":"But the beauty is a side effect","subj":"the lattice faintly overlaid with implied geometry/arithmetic lines — beauty as a byproduct","acc":"the geometry lines","anim":None},
    {"key":"Which brings us back to the woman","subj":"back to the woman at the rim, smaller now in a familiar wide composition","acc":None,"anim":None},
    {"key":"She doesn't know the phrase","subj":"close on the woman's hands and pot at a worn step edge, generations of wear in the stone","acc":None,"anim":None},
    {"key":"one that has met every generation","subj":"section showing successive generations meeting the water at different seasonal levels over time","acc":"the meeting point at the waterline","anim":"the waterline and a tiny figure shift across seasons, always meeting at a step"},
    {"key":"This morning it's thirty steps","subj":"the woman at 'thirty steps' today, one active step subtly marked","acc":"the marked active step","anim":"a quiet counting feel; light advances one step down"},
    {"key":"That's the quiet genius","subj":"a grand wide of Chand Baori, the quiet genius of it, timeless in golden light","acc":None,"anim":"slow majestic parallax pull-back; dust motes, warm light"},
    {"key":"Built to last","subj":"a final calm wide at golden hour, reflective sign-off mood","acc":None,"anim":None},
    {"key":"Outro card","subj":"a receding wide of the stepwell with clean central negative space reserved for the subscribe card overlay","acc":None,"anim":None},
]

# ── Composition helpers ───────────────────────────────────────────────────────
def negative_space(texts):
    pos = {t.get("position","bottom") for t in texts}
    parts = []
    if "top" in pos:    parts.append("keep the upper third as calm negative space for a callout")
    if "bottom" in pos: parts.append("keep the lower third as calm negative space for a callout")
    if "center" in pos: parts.append("keep the central band uncluttered for a centered callout")
    return "; ".join(parts) if parts else "balanced composition, no callout reserved"

def motion_hint(scene):
    if scene["type"] == "animated":
        return "compose as a still starting-frame that anticipates the described motion (leave room for it to move)"
    m = scene.get("motion","zoom_in")
    return {
        "zoom_detail": f"one clear focal point around ({scene.get('focus_x',0.5)}, {scene.get('focus_y',0.4)}) for a detail zoom",
        "pan_right":   "wide horizontal composition with interest spread across the frame for a lateral pan",
        "pan_left":    "wide horizontal composition with interest spread across the frame for a lateral pan",
        "pan_up":      "tall vertical composition with detail top-to-bottom for an upward pan",
        "zoom_in":     "centered composition with headroom for a slow zoom-in",
        "zoom_out":    "rich full-frame composition that rewards a slow zoom-out",
    }.get(m, "centered composition")

def accent_clause(acc):
    if acc:
        return (f"Accent: saffron {ACCENT_HEX} used sparingly as a single highlight on {acc}; "
                "everything else stays in the neutral base palette.")
    return f"Neutral base palette only (no saffron this frame; the {ACCENT_HEX} accent is reserved for key scenes)."

def build_image_prompt(scene, subj, acc):
    st = scene["scene_type"]
    recipe = SCENE_RECIPES.get(st, "isometric technical illustration")
    return (f"{STYLE_PREFIX} || Scene [{st}] — {recipe}. || Subject: {subj}. || "
            f"{accent_clause(acc)} || Composition: {negative_space(scene.get('texts',[]))}; "
            f"{motion_hint(scene)}. || Consistency: pass a style anchor from "
            f"assets/style_anchors/ (~{STYLE_ANCHOR_STRENGTH} strength); keep palette, "
            f"line-weight and isometric angle identical across all scenes.")

def build_animation_prompt(scene, anim, idx):
    return (f"{anim}. Duration ~{scene['duration']}s. Image-to-video from the generated "
            f"still images/scene_{idx:02d}.png — add motion only, do NOT restyle; keep the "
            f"isometric look, palette and saffron accent locked to the starting frame.")

# ── Enrich ────────────────────────────────────────────────────────────────────
def main():
    sb = json.load(open(SRC))
    scenes = sb["scenes"]
    assert len(scenes) == len(SCENE_DATA), f"scene count mismatch: {len(scenes)} vs {len(SCENE_DATA)}"

    out_scenes = []
    for i, (scene, data) in enumerate(zip(scenes, SCENE_DATA), start=1):
        # drift guard: authored key must appear in this scene's narration
        assert data["key"] in scene["narration_segment"], \
            f"scene {i}: key {data['key']!r} not in narration"

        s = {"image": f"images/scene_{i:02d}.png", "type": scene["type"]}
        if scene["type"] == "animated":
            s["animated_clip"] = f"clips/scene_{i:02d}_animated.mp4"
        s["duration"]   = scene["duration"]
        s["scene_type"] = scene["scene_type"]
        if scene["type"] == "static":
            s["motion"] = scene.get("motion", "zoom_in")
            if scene.get("motion") == "zoom_detail":
                s["focus_x"] = scene.get("focus_x", 0.5)
                s["focus_y"] = scene.get("focus_y", 0.4)
        s["image_prompt"] = build_image_prompt(scene, data["subj"], data["acc"])
        if scene["type"] == "animated":
            s["animation_prompt"] = build_animation_prompt(scene, data["anim"], i)
        s["texts"] = scene.get("texts", [])
        s["narration_segment"] = scene["narration_segment"]
        out_scenes.append(s)

    enriched = {
        "_comment": (
            "PASS 2 — ENRICHED. Generated by enrich_storyboard.py from "
            "storyboard_pass1_narrative.json. Generation protocol: (1) generate ALL 54 stills "
            "first, passing a style anchor (~0.7) on every call for cross-scene consistency; "
            "(2) for each 'animated' scene, feed its still into Kling with animation_prompt "
            "(image-to-video, motion only). Accent is the ACCENT_HEX variable, not per-scene "
            "hardcoded. scene_recipes below are applied uniformly by scene_type."
        ),
        "civilization": CIVILIZATION,
        "accent_hex": ACCENT_HEX,
        "style_anchor_strength": STYLE_ANCHOR_STRENGTH,
        "scene_recipes": SCENE_RECIPES,
        "base_dir": sb.get("base_dir", "."),
        "voiceover": sb.get("voiceover", "audio/voiceover.mp3"),
        "background_music": sb.get("background_music", "audio/ambient.mp3"),
        "music_volume": sb.get("music_volume", 0.08),
        "scenes": out_scenes,
    }
    json.dump(enriched, open(OUT, "w"), indent=2, ensure_ascii=False)
    n_anim = sum(1 for s in out_scenes if s["type"] == "animated")
    print(f"OK: wrote {OUT} — {len(out_scenes)} scenes, {n_anim} animated / {len(out_scenes)-n_anim} static")

if __name__ == "__main__":
    main()

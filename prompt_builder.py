#!/usr/bin/env python3
"""
prompt_builder.py — the single place that turns a LEAN storyboard into full prompts.

Composition = style_card.txt prefix  +  scene_type recipe  +  the scene's subject
              +  accent_hex highlight  +  a composition hint (from texts/motion).

Source-of-truth rules:
  * scene_type recipes come from the storyboard's `scene_recipes` (per-video, editable);
    DEFAULT_SCENE_RECIPES here is only a fallback if a storyboard omits them.
  * the style prefix is read from style_card.txt (single brand source).
  * accent_hex / style_anchor_strength come from the storyboard.

Used two ways:
  1. imported by generate_assets.py  → compose_image_prompt / compose_animation_prompt
  2. run standalone to (re)write a human-readable prompts.md INTO the video's folder:
        python prompt_builder.py projects/001_chand_baori/storyboard.json
        # -> projects/001_chand_baori/prompts.md   (nothing is stored in the JSON)
"""

import argparse, json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
STYLE_ANCHOR_DEFAULT = 0.7

# Fallback recipes (used only if the storyboard has no `scene_recipes`).
DEFAULT_SCENE_RECIPES = {
    "establishing":     "wide establishing view, the full structure in frame with sky/horizon context and a strong sense of scale",
    "cross_section":    "architectural cutaway/section — ground sliced open to reveal strata and the water/level line, shown in clean profile, educational-diagram clarity",
    "detail":           "tight isometric close-up on a single element, shallow depth, texture and craft emphasis",
    "scale_comparison": "the subject beside a scale reference (tiny human silhouettes and/or storey markers), measured diagrammatic framing",
    "map":              "top-down cartographic schematic, muted regional context, thin technical linework",
    "title":            "hero-wide composition with generous clean negative space reserved for a title wordmark overlay",
    "outro":            "calm, receding wide composition with clean negative space reserved for a subscribe card overlay",
}

# Fallback if style_card.txt can't be read.
DEFAULT_STYLE_PREFIX = (
    "Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment "
    "background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream "
    "light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. "
    "Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or "
    "tiny silhouettes for scale only). No text in image. High architectural precision. "
    "Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood."
)


def load_style_prefix(path):
    """Extract the prefix block from style_card.txt (from the 'Isometric...' line
    up to the PER-SCENE ADD-ONS separator)."""
    try:
        body = Path(path).read_text().split("--- PER-SCENE")[0]
    except Exception:
        return DEFAULT_STYLE_PREFIX
    lines = [l.strip() for l in body.splitlines()]
    start = next((i for i, l in enumerate(lines) if l.startswith("Isometric")), None)
    return " ".join(l for l in lines[start:] if l) if start is not None else DEFAULT_STYLE_PREFIX


def context_from(sb, style_card_path):
    """Everything needed to compose, pulled from the storyboard + style card."""
    return {
        "accent_hex": sb.get("accent_hex", "#3D5A80"),
        "anchor": sb.get("style_anchor_strength", STYLE_ANCHOR_DEFAULT),
        "recipes": sb.get("scene_recipes", DEFAULT_SCENE_RECIPES),   # storyboard wins
        "style_prefix": load_style_prefix(style_card_path),
    }


def composition_hint(scene):
    pos = {t.get("position", "bottom") for t in scene.get("texts", [])}
    parts = []
    if "top" in pos:    parts.append("keep the upper third clear for a callout")
    if "bottom" in pos: parts.append("keep the lower third clear for a callout")
    if "center" in pos: parts.append("keep the central band uncluttered for a centered callout")
    neg = "; ".join(parts) if parts else "balanced composition"
    if scene.get("type") == "animated":
        return f"{neg}; compose as a starting frame that anticipates the described motion"
    move = {
        "zoom_detail": f"one clear focal point near ({scene.get('focus_x',0.5)}, {scene.get('focus_y',0.4)})",
        "pan_right":   "wide horizontal composition with interest across the frame",
        "pan_left":    "wide horizontal composition with interest across the frame",
        "pan_up":      "tall vertical composition, detail top-to-bottom",
        "zoom_in":     "centered composition with headroom",
        "zoom_out":    "rich full-frame composition",
    }.get(scene.get("motion", "zoom_in"), "centered composition")
    return f"{neg}; {move}"


def facts_clause(scene):
    """Visual-accuracy constraints from the storyboard's per-scene `visual_facts`
    (verified against the project's references/ pack). Empty string if none."""
    facts = scene.get("visual_facts") or []
    if not facts:
        return ""
    clause = f" || Factual constraints (must be visually accurate): {'; '.join(facts)}."
    if scene.get("reference_image"):
        clause += (" A real reference photo is provided: take GEOMETRY and PROPORTIONS from it, "
                   "take STYLE only from the style anchor.")
    return clause


def compose_image_prompt(scene, ctx):
    st = scene.get("scene_type", "detail")
    recipe = ctx["recipes"].get(st, "isometric technical illustration")
    subject = (scene.get("image_prompt") or "").strip()
    acc = scene.get("accent")
    if acc:
        accent_clause = (f"Accent: {ctx['accent_hex']} used sparingly as a single highlight on "
                         f"{acc}; everything else stays in the neutral base palette.")
    else:
        accent_clause = (f"Neutral base palette only (no accent this frame; the "
                         f"{ctx['accent_hex']} accent is reserved for key scenes).")
    return (f"{ctx['style_prefix']} || Scene [{st}] — {recipe}. || Subject: {subject}."
            f"{facts_clause(scene)} || "
            f"{accent_clause} || Composition: {composition_hint(scene)}. || Consistency: pass a "
            f"style anchor (~{ctx['anchor']} strength); keep palette, line-weight and isometric "
            f"angle identical across all scenes.")


def compose_animation_prompt(scene, idx):
    motion = (scene.get("animation_prompt") or "subtle parallax").strip()
    facts = scene.get("visual_facts") or []
    hold = (f" Structure must stay true to: {'; '.join(facts)}." if facts else "")
    return (f"{motion}. Duration ~{scene['duration']}s. Image-to-video from the generated still "
            f"images/scene_{idx:02d}.png — add motion only, do NOT restyle; do not add, remove, "
            f"or deform any structural element; keep the isometric look, palette and accent "
            f"locked to the starting frame.{hold}")


def write_prompt_sheet(sb, ctx, out_path):
    scenes = sb["scenes"]
    L = [f"# Composed prompt sheet ({len(scenes)} scenes)",
         f"*Generated at runtime by prompt_builder.py from the lean storyboard + style_card.txt "
         f"+ accent {ctx['accent_hex']}. Not stored in the JSON; regenerate anytime.*", ""]
    for i, s in enumerate(scenes, 1):
        L += [f"### Scene {i:02d} — {s['scene_type']} · {s['type']} · {s['duration']}s",
              f"**IMAGE → `{s['image']}`**", "```", compose_image_prompt(s, ctx), "```"]
        if s["type"] == "animated":
            L += [f"**ANIMATION → `{s['animated_clip']}`**", "```", compose_animation_prompt(s, i), "```"]
        L.append("")
    Path(out_path).write_text("\n".join(L))


def anim_jobs(sb):
    """The per-scene Kling image_to_video requests (animated scenes only)."""
    return [{"scene": i, "still": s["image"], "clip": s["animated_clip"],
             "duration": s["duration"], "prompt": compose_animation_prompt(s, i)}
            for i, s in enumerate(sb["scenes"], 1) if s["type"] == "animated"]


def main():
    ap = argparse.ArgumentParser(description="Compose prompts.md — or the Kling animation job list — from a lean storyboard.")
    ap.add_argument("storyboard", help="path to the video's storyboard.json")
    ap.add_argument("--style-card", default=str(SCRIPT_DIR / "style_card.txt"))
    ap.add_argument("--out", default=None, help="output path (default: <project>/prompts.md or anim_jobs.json)")
    ap.add_argument("--anim-jobs", action="store_true",
                    help="emit the Kling MCP animation job list (animated scenes) instead of prompts.md")
    args = ap.parse_args()

    sb_path = Path(args.storyboard).resolve()
    sb = json.loads(sb_path.read_text())
    ctx = context_from(sb, args.style_card)

    if args.anim_jobs:
        jobs = anim_jobs(sb)
        out = Path(args.out) if args.out else sb_path.parent / "anim_jobs.json"
        out.write_text(json.dumps(jobs, indent=2, ensure_ascii=False))
        total = sum(j["duration"] for j in jobs)
        print(f"wrote {out} — {len(jobs)} animation jobs, ~{total}s total to generate via the Kling MCP")
        return

    out = Path(args.out) if args.out else sb_path.parent / "prompts.md"
    write_prompt_sheet(sb, ctx, out)
    print(f"wrote {out} — {len(sb['scenes'])} scenes")


if __name__ == "__main__":
    main()

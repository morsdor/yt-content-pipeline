#!/usr/bin/env python3
"""
prompt_builder.py — the single place that turns the storyboard (the studio's single
accreting production document, schema v2 — see docs/storyboard_schema.md) into composed
plate prompts and human-readable production sheets.

Image composition = style_card.txt prefix  +  scene_type recipe  +  the scene's plate
                    subject  +  accent_hex highlight  +  a composition hint (from the
                    composition block / texts).

Schema v2 (the studio pipeline): scenes carry blocks filled by the seven studio passes
(shot / composition / build+plate+layers / camera+motion / ae_build). The board IS the
motion brief. Legacy v1 boards (type/motion/animation_prompt fields) remain readable
while projects/001 completes its retro-direction.

Source-of-truth rules:
  * scene_type recipes come from the storyboard's `scene_recipes` (per-video, editable);
    DEFAULT_SCENE_RECIPES here is only a fallback if a storyboard omits them.
  * the style prefix is read from style_card.txt (single brand source).
  * accent_hex / style_anchor_strength come from the storyboard.
  * shot_list.md / prompts.md / motion_briefs.md are RENDERED from the JSON — gitignored,
    regenerated anytime, never authored by hand.

Used three ways:
  1. imported by generate_images.py  → compose_image_prompt (+ the v1/v2 accessors)
  2. render sheets:
        python prompt_builder.py <sb>                  # -> prompts.md
        python prompt_builder.py <sb> --shot-list      # -> shot_list.md  (the v2 board mirror)
        python prompt_builder.py <sb> --motion-briefs  # -> motion_briefs.md (v1; v2 → shot list)
  3. validate the board between studio passes:
        python prompt_builder.py <sb> --validate
"""

import argparse, json, re
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


# ---------------------------------------------------------------------------
# v1/v2 accessors — one place that knows where a fact lives in either schema.
# v2 moves the generation fields into blocks: plate{subject, reference_image,
# visual_facts, accent}, shot{scene_type}, composition{...}. v1 keeps them flat.
# ---------------------------------------------------------------------------

def is_v2(sb):
    return sb.get("version", 1) >= 2


def _plate(scene):
    return scene.get("plate") or {}


def scene_subject(scene):
    return (_plate(scene).get("subject") or scene.get("image_prompt") or "").strip()


def scene_facts(scene):
    return _plate(scene).get("visual_facts") or scene.get("visual_facts") or []


def scene_ref(scene):
    return _plate(scene).get("reference_image") or scene.get("reference_image") or ""


def scene_type_of(scene):
    return (scene.get("shot") or {}).get("scene_type") or scene.get("scene_type", "detail")


def scene_accent(scene):
    if "plate" in scene:
        return _plate(scene).get("accent")
    return scene.get("accent")


def scene_build(scene):
    """v2 build track; v1 scenes are all effectively single plates."""
    return scene.get("build", "plate")


def composition_hint(scene):
    comp = scene.get("composition")
    if comp:                                # v2 — the storyboard-artist decided this
        parts = []
        ns = comp.get("negative_space")
        if ns and ns != "none":
            band = {"top": "upper third", "bottom": "lower third", "center": "central band"}.get(ns, ns)
            parts.append(f"keep the {band} clear for a callout")
        if comp.get("focal_point"):
            parts.append(f"single focal point: {comp['focal_point']}")
        # layered subjects are excluded from the plate; the excluded space must read empty
        layered = [l for l in (scene.get("layers") or []) if str(l.get("asset", "")).strip()]
        if scene_build(scene) == "plate+layers" and layered:
            parts.append("leave clean space where separate animated layers will composite")
        cam = (scene.get("camera") or {}).get("move")
        if cam and cam != "none":
            parts.append("compose as a base plate that survives a slow eased camera move (safe margins)")
        return "; ".join(parts) if parts else "balanced composition"
    # ---- v1 fallback ----
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
    """Visual-accuracy constraints from the scene's visual facts (v2: plate.visual_facts;
    v1: flat) — verified against the project's references/ pack. Empty string if none."""
    facts = scene_facts(scene)
    if not facts:
        return ""
    clause = f" || Factual constraints (must be visually accurate): {'; '.join(facts)}."
    if scene_ref(scene):
        clause += (" A real reference photo is provided: take GEOMETRY and PROPORTIONS from it, "
                   "take STYLE only from the style anchor.")
    return clause


def compose_image_prompt(scene, ctx):
    st = scene_type_of(scene)
    recipe = ctx["recipes"].get(st, "isometric technical illustration")
    subject = scene_subject(scene)
    acc = scene_accent(scene)
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


# Old Ken-Burns `motion` enum → a natural-language camera intent. Every scene is an
# AE scene now, so a scene with no explicit animation_prompt still gets a real brief:
# its former Ken-Burns move becomes a keyframed AE camera move.
_KENBURNS = {
    "zoom_in":     "slow eased push-in",
    "zoom_out":    "slow eased pull-back",
    "zoom_detail": "slow eased push toward the focal point",
    "pan_right":   "slow eased pan right across the frame",
    "pan_left":    "slow eased pan left across the frame",
    "pan_up":      "slow eased pan upward",
    "pan_down":    "slow eased pan downward",
}


def _clip_name(scene, idx):
    """The AE render target for this scene. v2: ae_build.render.clip; v1 legacy
    `animated_clip` honoured for continuity."""
    render = ((scene.get("ae_build") or {}).get("render") or {})
    return render.get("clip") or scene.get("animated_clip") or f"clips/scene_{idx:02d}.mp4"


def _motion_intent(scene):
    """This scene's motion intent. Prefer an explicit `animation_prompt`; otherwise
    synthesise a camera move from the (Ken-Burns-era) `motion` + focus fields."""
    ap = (scene.get("animation_prompt") or "").strip()
    if ap:
        return ap
    base = _KENBURNS.get(scene.get("motion", "zoom_in"), "slow eased push-in")
    fx, fy = scene.get("focus_x"), scene.get("focus_y")
    if scene.get("motion") == "zoom_detail" and fx is not None and fy is not None:
        base += f" at ({fx}, {fy})"
    return base


def _camera_line(cam):
    """Render a v2 camera{} block as one spec line."""
    if not cam or cam.get("move") in (None, "none"):
        return "camera: none"
    amt = (f"{cam['amount_pct']}%" if cam.get("amount_pct")
           else f"{cam.get('px_per_s', '?')} px/s")
    holds = f", hold {cam.get('hold_in_s', 0.5)}s/{cam.get('hold_out_s', 0.5)}s"
    return f"camera: {cam['move']} {amt}, ease {cam.get('ease', 'F9')}{holds}"


def _layer_motion_lines(scene):
    """Render each moving v2 layer as `asset: kind params`."""
    out = []
    for l in (scene.get("layers") or []):
        m = l.get("motion")
        if not m or m.get("kind") in (None, "none"):
            continue
        name = Path(str(l.get("asset", "layer"))).stem
        params = ", ".join(f"{k}={v}" for k, v in m.items() if k != "kind" and v is not None)
        out.append(f"{name}: {m['kind']}" + (f" ({params})" if params else ""))
    return out


def compose_motion_brief(scene, idx):
    """One buildable After Effects shot direction. v2 scenes render their numeric
    camera{}/layers[].motion{} blocks (the board IS the brief); v1 scenes expand their
    motion intent. A pure camera move is just the lightest kind of AE scene."""
    facts = scene_facts(scene)
    clip = _clip_name(scene, idx)
    hold = (f" Must stay true to (may not move, deform, or be covered): "
            f"{'; '.join(facts)}." if facts else "")
    if scene.get("camera") is not None:                       # v2 numeric spec
        moving = _layer_motion_lines(scene)
        spec = _camera_line(scene.get("camera"))
        if moving:
            spec += "; moving: " + "; ".join(moving)
        base = (f"base plate images/scene_{idx:02d}.png" if scene.get("image")
                else "assembly — library assets on the stage background")
        return (f"{spec}. Duration {scene['duration']}s over {base} — transforms only, "
                f"never redraw the art; ease every keyframe pair (F9); render "
                f"3840x2160 @ 30fps (+~1s handles) to {clip}.{hold}")
    return (f"{_motion_intent(scene)}. Duration {scene['duration']}s. Build over the validated "
            f"4K still images/scene_{idx:02d}.png — transforms only, never redraw the art; ease "
            f"every keyframe pair (F9); max 1-2 moving elements; 0.5-1s hold at both ends; render "
            f"3840x2160 @ 30fps to {clip}.{hold}")


def write_prompt_sheet(sb, ctx, out_path):
    scenes = sb["scenes"]
    L = [f"# Composed prompt sheet ({len(scenes)} scenes)",
         f"*Generated at runtime by prompt_builder.py from the lean storyboard + style_card.txt "
         f"+ accent {ctx['accent_hex']}. Not stored in the JSON; regenerate anytime.*", ""]
    for i, s in enumerate(scenes, 1):
        tag = f" · {s['type']}" if s.get("type") else f" · {scene_build(s)}"
        L.append(f"### Scene {i:02d} — {scene_type_of(s)}{tag} · {s['duration']}s")
        if scene_build(s) != "assembly" and s.get("image"):
            L += [f"**IMAGE → `{s['image']}`**", "```", compose_image_prompt(s, ctx), "```"]
        else:
            L.append("*(assembly scene — no plate; built from library assets)*")
        L += [f"**MOTION BRIEF → `{_clip_name(s, i)}`**", "```", compose_motion_brief(s, i), "```"]
        L.append("")
    Path(out_path).write_text("\n".join(L))


def motion_briefs(sb):
    """The per-scene After Effects motion briefs. Every scene is an AE scene now —
    from a bare camera push to a fully-populated shot — so every scene gets a brief."""
    return [{"scene": i, "still": s["image"], "clip": _clip_name(s, i),
             "duration": s["duration"], "brief": compose_motion_brief(s, i)}
            for i, s in enumerate(sb["scenes"], 1)]


def write_motion_briefs(sb, out_path):
    rows = motion_briefs(sb)
    total = sum(r["duration"] for r in rows)
    L = [f"# Motion briefs — {len(rows)} AE scenes (~{total}s of built motion)",
         "*Every scene is an After Effects scene: a validated still (± library assets) given "
         "motion in AE, then cut against the VO. Generated by prompt_builder.py from each scene's "
         "`animation_prompt` (motion intent, or a camera move derived from the legacy `motion` "
         "field) + `visual_facts` (hold-constraints). One brief = one buildable AE scene, on the "
         "ladder: camera move → parallax → element motion. "
         "See docs/after_effects_workflow.md; QC per visual-accuracy-gate Layer 3.*", ""]
    for r in rows:
        L += [f"### Scene {r['scene']:02d} — {r['duration']}s → `{r['clip']}`",
              f"- **Base still:** `{r['still']}`",
              f"- **Brief:** {r['brief']}", ""]
    Path(out_path).write_text("\n".join(L))
    return len(rows), total


# ---------------------------------------------------------------------------
# shot_list.md — the human-readable mirror of the v2 board, one section per
# completed studio pass. Rendered from the JSON; regenerate after every pass.
# ---------------------------------------------------------------------------

def _texts_summary(scene):
    return " · ".join(f"“{t['text']}” {t['start']}-{t['end']}s/{t.get('position','?')}"
                      for t in scene.get("texts") or []) or "—"


def write_shot_list(sb, out_path):
    scenes = sb["scenes"]
    passes = sb.get("passes") or {}
    total = sum(s.get("duration", 0) for s in scenes)
    vo = sb.get("vo_duration")
    L = [f"# Shot list — {len(scenes)} scenes · ~{total:.0f}s"
         + (f" (VO {vo:.0f}s)" if vo else " (VO not yet recorded)"),
         "*Rendered by `prompt_builder.py --shot-list` from `storyboard.json` (schema v2) — "
         "the board is the source of truth; regenerate this after every studio pass. "
         "Craft: `docs/cinematography.md` · numbers: `brand_guide.md` §5.*", "",
         "**Passes:** " + " · ".join(f"{k} {'✅ ' + str(v) if v else '—'}"
                                     for k, v in passes.items()), ""]

    def section(title, header, rowfn, want):
        if not any(want(s) for s in scenes):
            return
        L.append(f"## {title}")
        L.append(header)
        L.append("|" + "---|" * (header.count("|") - 1))
        for i, s in enumerate(scenes, 1):
            L.append(rowfn(i, s))
        L.append("")

    section("Pass 1 — Scene breakdown",
            "| id | t | dur | register | purpose | needs |",
            lambda i, s: (f"| {s.get('id', f'scene_{i:02d}')} "
                          f"| {s.get('t_start', '?')}–{s.get('t_end', '?')} | {s['duration']}s "
                          f"| {s.get('register', '?')} | {s.get('purpose', '?')} "
                          f"| {', '.join(s.get('needs') or []) or '—'} |"),
            lambda s: s.get("purpose"))

    section("Pass 2 — Sequence design",
            "| id | size | type | role | transition |",
            lambda i, s: (lambda sh: f"| {s.get('id', i)} | {sh.get('shot_size', '?')} "
                          f"| {sh.get('scene_type', '?')} | {sh.get('progression_role', '?')} "
                          f"| {sh.get('transition_in', 'cut')} |")(s.get("shot") or {}),
            lambda s: s.get("shot"))

    section("Pass 3 — Frames",
            "| id | frame | focal | neg. space |",
            lambda i, s: (lambda c: f"| {s.get('id', i)} | {c.get('frame', '?')} "
                          f"| {c.get('focal_point', '?')} | {c.get('negative_space', '?')} |")
                         (s.get("composition") or {}),
            lambda s: s.get("composition"))

    section("Pass 4 — Builds",
            "| id | build | plate subject / stage | layers |",
            lambda i, s: (f"| {s.get('id', i)} | {scene_build(s)} "
                          f"| {scene_subject(s) or (s.get('composition') or {}).get('frame', '?')} "
                          f"| {'; '.join(str(l.get('asset', '?')) + ' ← ' + str(l.get('role', '?')) for l in s.get('layers') or []) or '—'} |"),
            lambda s: s.get("build"))

    if any(s.get("layers") for s in scenes):
        reused, pending = {}, {}
        for i, s in enumerate(scenes, 1):
            for l in s.get("layers") or []:
                a = str(l.get("asset", ""))
                (pending if a.startswith("generate:") else reused).setdefault(a, []).append(
                    s.get("id", f"scene_{i:02d}"))
        L += ["## Pass 5 — Asset plan",
              f"- **Reused ({len(reused)}):** " + ("; ".join(f"`{a}` ← {', '.join(v)}" for a, v in sorted(reused.items())) or "—"),
              f"- **To generate ({len(pending)}):** " + ("; ".join(f"`{a}` ← {', '.join(v)}" for a, v in sorted(pending.items())) or "— (all resolved)"),
              ""]

    section("Pass 6 — Motion",
            "| id | camera | moving layers | texts | overlay |",
            lambda i, s: (f"| {s.get('id', i)} | {_camera_line(s.get('camera'))} "
                          f"| {'; '.join(_layer_motion_lines(s)) or '—'} | {_texts_summary(s)} "
                          f"| {s.get('particle_overlay') or '—'} |"),
            lambda s: s.get("camera") is not None)

    section("Pass 7 — AE blueprints",
            "| id | hierarchy | render | jsx |",
            lambda i, s: (lambda b: f"| {s.get('id', i)} | {b.get('hierarchy', '?')} "
                          f"| {(b.get('render') or {}).get('clip', '?')} (+{(b.get('render') or {}).get('handles_s', 1)}s handles) "
                          f"| {b.get('jsx') or '—'} |")(s.get("ae_build") or {}),
            lambda s: s.get("ae_build"))

    Path(out_path).write_text("\n".join(L))
    return len(scenes)


# ---------------------------------------------------------------------------
# --validate — the document's continuity supervisor. Run between studio passes.
# ---------------------------------------------------------------------------

PASS_BLOCKS = {  # ledger entry -> per-scene requirement when that pass is stamped
    "script_analyzer": lambda s: all(k in s for k in ("id", "duration", "narration_segment", "purpose", "register")),
    "film_director":   lambda s: bool((s.get("shot") or {}).get("scene_type")),
    "storyboard_artist": lambda s: bool((s.get("composition") or {}).get("frame")),
    "scene_composer":  lambda s: s.get("build") in ("plate", "assembly", "plate+layers")
                                 and (s.get("build") == "assembly" or (scene_subject(s) and s.get("image"))),
    "motion_director": lambda s: s.get("camera") is not None,
    "ae_director":     lambda s: bool(((s.get("ae_build") or {}).get("render") or {}).get("clip")),
}


def validate(sb, sb_path):
    errors, warnings = [], []
    scenes = sb["scenes"]
    if not is_v2(sb):
        warnings.append("legacy v1 board (no \"version\": 2) — only basic checks run")

    # duration + count budgets (cinematography.md RHYTHM-6)
    exempt = {"title", "outro"}
    for i, s in enumerate(scenes, 1):
        d = s.get("duration")
        if d is None:
            errors.append(f"scene {i:02d}: no duration"); continue
        if scene_type_of(s) not in exempt and not 8 <= d <= 12:
            warnings.append(f"scene {i:02d}: duration {d}s outside 8-12s")
        for t in s.get("texts") or []:
            if t.get("end", 0) > d:
                warnings.append(f"scene {i:02d}: text “{t.get('text','')[:30]}” ends at {t['end']}s > scene {d}s")
    if not 60 <= len(scenes) <= 80:
        warnings.append(f"{len(scenes)} scenes (target 60-80)")

    # timestamps contiguous; sum vs VO
    if is_v2(sb) and any("t_start" in s for s in scenes):
        prev_end = 0.0
        for i, s in enumerate(scenes, 1):
            ts, te = s.get("t_start"), s.get("t_end")
            if ts is None or te is None:
                errors.append(f"scene {i:02d}: missing t_start/t_end"); continue
            if abs(ts - prev_end) > 0.05:
                errors.append(f"scene {i:02d}: t_start {ts} != previous t_end {prev_end}")
            if abs((te - ts) - s.get("duration", 0)) > 0.05:
                errors.append(f"scene {i:02d}: duration {s.get('duration')} != t_end-t_start {te - ts:.2f}")
            prev_end = te
        vo = sb.get("vo_duration")
        if vo and abs(prev_end - vo) > 2:
            warnings.append(f"board ends at {prev_end:.1f}s but vo_duration is {vo}s (>2s apart — true-up needed?)")

    # completed passes must have their blocks
    for name, done in (sb.get("passes") or {}).items():
        check = PASS_BLOCKS.get(name)
        if done and check:
            missing = [s.get("id", f"scene_{i:02d}") for i, s in enumerate(scenes, 1) if not check(s)]
            if missing:
                errors.append(f"pass {name} stamped but blocks missing on: {', '.join(missing[:8])}"
                              + (f" (+{len(missing) - 8} more)" if len(missing) > 8 else ""))

    # layer assets resolvable (library file, INDEX row, or pending batch spec)
    lib = SCRIPT_DIR / "assets_library"
    index_text = (lib / "INDEX.md").read_text() if (lib / "INDEX.md").is_file() else ""
    batch_text = " ".join(p.read_text() for p in sorted(lib.glob("_batches/*.json"))) if lib.is_dir() else ""
    planned = bool((sb.get("passes") or {}).get("asset_planner"))
    for i, s in enumerate(scenes, 1):
        for l in s.get("layers") or []:
            a = str(l.get("asset", ""))
            if a.startswith("generate:"):
                name = re.search(r"generate:\s*[\w-]+/([\w-]+)", a)
                known = name and name.group(1) in batch_text
                (errors if planned and not known else warnings).append(
                    f"scene {i:02d}: unresolved asset request “{a[:60]}”"
                    + ("" if not planned else (" (in batch)" if known else " (NOT in any batch)")))
            elif a and not (SCRIPT_DIR / a).is_file() and Path(a).name not in index_text:
                errors.append(f"scene {i:02d}: layer asset not found: {a}")

    # render targets unique
    clips = [_clip_name(s, i) for i, s in enumerate(scenes, 1)]
    dupes = {c for c in clips if clips.count(c) > 1}
    if dupes:
        errors.append(f"duplicate render targets: {', '.join(sorted(dupes))}")

    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description="Compose prompts.md — or the AE motion-brief sheet — from a lean storyboard.")
    ap.add_argument("storyboard", help="path to the video's storyboard.json")
    ap.add_argument("--style-card", default=str(SCRIPT_DIR / "style_card.txt"))
    ap.add_argument("--out", default=None, help="output path (default: <project>/prompts.md or motion_briefs.md)")
    ap.add_argument("--motion-briefs", action="store_true",
                    help="emit motion_briefs.md (the per-scene After Effects shot directions) instead of prompts.md")
    ap.add_argument("--shot-list", action="store_true",
                    help="render shot_list.md — the human-readable mirror of the v2 board (one section per studio pass)")
    ap.add_argument("--validate", action="store_true",
                    help="validate the board (durations, timestamps, pass blocks, asset resolution); exit 1 on errors")
    args = ap.parse_args()

    sb_path = Path(args.storyboard).resolve()
    sb = json.loads(sb_path.read_text())

    if args.validate:
        errors, warnings = validate(sb, sb_path)
        for w in warnings:
            print(f"  WARN  {w}")
        for e in errors:
            print(f"  ERROR {e}")
        print(f"{sb_path.name}: {len(errors)} error(s), {len(warnings)} warning(s)")
        raise SystemExit(1 if errors else 0)

    if args.shot_list:
        out = Path(args.out) if args.out else sb_path.parent / "shot_list.md"
        n = write_shot_list(sb, out)
        print(f"wrote {out} — {n} scenes across the completed passes")
        return

    ctx = context_from(sb, args.style_card)

    if args.motion_briefs:
        out = Path(args.out) if args.out else sb_path.parent / "motion_briefs.md"
        n, total = write_motion_briefs(sb, out)
        print(f"wrote {out} — {n} motion briefs, ~{total}s of motion to build in AE")
        if is_v2(sb):
            print("note: v2 board — the shot list is the richer sheet (--shot-list)")
        return

    out = Path(args.out) if args.out else sb_path.parent / "prompts.md"
    write_prompt_sheet(sb, ctx, out)
    print(f"wrote {out} — {len(sb['scenes'])} scenes")


if __name__ == "__main__":
    main()

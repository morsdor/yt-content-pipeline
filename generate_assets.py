#!/usr/bin/env python3
"""
generate_assets.py — code-driven asset generation for The Engineering Atlas.

storyboard.json is the source of truth, and it stays LEAN: each scene carries only
its *scene-specific* prompt —
    image_prompt      : what to draw in THIS scene (the subject), no boilerplate
    accent (optional) : where the single accent highlight goes
    animation_prompt  : the motion for THIS scene (animated scenes only)
The shared brand boilerplate is applied HERE, at generation time:
    * the style-card prefix is read from style_card.txt (single source of truth)
    * the scene_type recipe comes from SCENE_RECIPES below (brand-level)
    * the accent hex comes from storyboard.json -> accent_hex (per video)
    * composition hints are derived from `texts` + `motion`
So there is no separate "enrich" step and no repeated prefix in the JSON.

Outputs the assembler expects:
    images/scene_NN.png          (all scenes)   — Gemini "nano banana" (Interactions API)
    clips/scene_NN_animated.mp4  (animated)     — Kling image-to-video (REST)

Setup
-----
    pip install google-genai pyjwt requests
    cp .env.example .env    # fill GEMINI_API_KEY, KLING_ACCESS_KEY, KLING_SECRET_KEY

Usage (from repo root)
----------------------
    SB=projects/001_chand_baori/storyboard.json
    python generate_assets.py --storyboard $SB --dump-prompts        # write the composed prompt sheet
    python generate_assets.py --storyboard $SB --only image --scenes 1   # the anchor; eyeball it
    python generate_assets.py --storyboard $SB --only image             # the rest, referencing scene 1
    python generate_assets.py --storyboard $SB --only anim              # Kling clips from the stills
    python generate_assets.py --storyboard $SB --only all --dry-run     # plan + one sample prompt
"""

import argparse, base64, json, os, time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# ── Config (override via env / CLI) ──────────────────────────────────────────
IMAGE_MODEL_DEFAULT = "gemini-3.1-flash-image"          # Nano Banana 2
KLING_BASE          = "https://api-singapore.klingai.com"
KLING_MODEL         = os.environ.get("KLING_MODEL", "kling-v2-6")
POLL_INTERVAL_S     = 10
POLL_TIMEOUT_S      = 600
KLING_RETRIES       = 2                                  # then flag for static fallback

# ── Brand-level visual DNA (applies to EVERY video, not per-scene) ────────────
# scene_type -> the recipe fragment injected into that scene's prompt.
SCENE_RECIPES = {
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


# ── Prompt composition (the "dynamic enhancement" happens here) ──────────────
def load_style_prefix(path):
    """Extract the prefix block from style_card.txt (everything from the
    'Isometric...' line up to the PER-SCENE ADD-ONS separator)."""
    try:
        body = Path(path).read_text().split("--- PER-SCENE")[0]
    except Exception:
        return DEFAULT_STYLE_PREFIX
    lines = [l.strip() for l in body.splitlines()]
    start = next((i for i, l in enumerate(lines) if l.startswith("Isometric")), None)
    if start is None:
        return DEFAULT_STYLE_PREFIX
    return " ".join(l for l in lines[start:] if l)


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


def compose_image_prompt(scene, accent_hex, style_prefix, anchor_strength):
    st = scene.get("scene_type", "detail")
    recipe = SCENE_RECIPES.get(st, "isometric technical illustration")
    subject = (scene.get("image_prompt") or "").strip()
    acc = scene.get("accent")
    if acc:
        accent_clause = (f"Accent: {accent_hex} used sparingly as a single highlight on {acc}; "
                         "everything else stays in the neutral base palette.")
    else:
        accent_clause = (f"Neutral base palette only (no accent this frame; the {accent_hex} "
                         "accent is reserved for key scenes).")
    return (f"{style_prefix} || Scene [{st}] — {recipe}. || Subject: {subject}. || "
            f"{accent_clause} || Composition: {composition_hint(scene)}. || Consistency: pass a "
            f"style anchor (~{anchor_strength} strength); keep palette, line-weight and isometric "
            f"angle identical across all scenes.")


def compose_animation_prompt(scene, idx):
    motion = (scene.get("animation_prompt") or "subtle parallax").strip()
    return (f"{motion}. Duration ~{scene['duration']}s. Image-to-video from the generated still "
            f"images/scene_{idx:02d}.png — add motion only, do NOT restyle; keep the isometric "
            f"look, palette and accent locked to the starting frame.")


# ── .env loader + scene selection ────────────────────────────────────────────
def load_dotenv(*candidates):
    for p in candidates:
        p = Path(p)
        if p.is_file():
            for line in p.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def parse_scene_selection(spec, n):
    """'1,3,5-9' -> set of 1-based indices; None/'' -> all."""
    if not spec:
        return set(range(1, n + 1))
    out = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if "-" in chunk:
            a, b = chunk.split("-"); out.update(range(int(a), int(b) + 1))
        elif chunk:
            out.add(int(chunk))
    return {i for i in out if 1 <= i <= n}


# ── Gemini / nano banana image generation (Interactions API) ─────────────────
def generate_image(prompt, out_path, ref_path=None, model=IMAGE_MODEL_DEFAULT):
    from google import genai  # lazy import so --dry-run/--help need no deps
    client = genai.Client()   # reads GEMINI_API_KEY from env
    if ref_path and Path(ref_path).is_file():
        ref_b64 = base64.b64encode(Path(ref_path).read_bytes()).decode("utf-8")
        payload = [{"type": "text", "text": prompt},
                   {"type": "image", "data": ref_b64, "mime_type": "image/png"}]
    else:
        payload = prompt
    interaction = client.interactions.create(model=model, input=payload)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(interaction.output_image.data))


# ── Kling image-to-video (JWT auth + submit + poll) ──────────────────────────
def kling_token():
    import jwt  # PyJWT
    ak, sk = os.environ["KLING_ACCESS_KEY"], os.environ["KLING_SECRET_KEY"]
    now = int(time.time())
    tok = jwt.encode({"iss": ak, "exp": now + 1800, "nbf": now - 5},
                     sk, algorithm="HS256", headers={"alg": "HS256", "typ": "JWT"})
    return tok.decode() if isinstance(tok, bytes) else tok


def kling_animate(still_path, prompt, duration_s, mode, out_path):
    import requests
    dur = "10" if duration_s > 8 else "5"           # Kling offers 5s / 10s
    img_b64 = base64.b64encode(Path(still_path).read_bytes()).decode("utf-8")
    headers = {"Authorization": f"Bearer {kling_token()}", "Content-Type": "application/json"}
    body = {"model_name": KLING_MODEL, "image": img_b64, "prompt": prompt,
            "duration": dur, "mode": mode}
    r = requests.post(f"{KLING_BASE}/v1/videos/image2video", headers=headers, json=body, timeout=60)
    r.raise_for_status()
    task_id = r.json()["data"]["task_id"]
    deadline = time.time() + POLL_TIMEOUT_S
    while time.time() < deadline:
        time.sleep(POLL_INTERVAL_S)
        g = requests.get(f"{KLING_BASE}/v1/videos/image2video/{task_id}",
                         headers={"Authorization": f"Bearer {kling_token()}"}, timeout=60)
        g.raise_for_status()
        data = g.json()["data"]
        if data.get("task_status") == "succeed":
            url = data["task_result"]["videos"][0]["url"]
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(requests.get(url, timeout=120).content)
            return
        if data.get("task_status") == "failed":
            raise RuntimeError(data.get("task_status_msg", "kling task failed"))
    raise TimeoutError(f"kling task {task_id} did not finish in {POLL_TIMEOUT_S}s")


# ── Human-readable prompt sheet (composed on demand; nothing stored in JSON) ──
def write_prompt_sheet(scenes, accent_hex, anchor_strength, style_prefix, out_path):
    L = [f"# Composed prompt sheet ({len(scenes)} scenes)",
         f"*Built at generation time from lean storyboard + style_card.txt + accent {accent_hex}. "
         "Regenerate with `generate_assets.py --dump-prompts`.*", ""]
    for i, s in enumerate(scenes, 1):
        L += [f"### Scene {i:02d} — {s['scene_type']} · {s['type']} · {s['duration']}s",
              f"**IMAGE → `{s['image']}`**", "```",
              compose_image_prompt(s, accent_hex, style_prefix, anchor_strength), "```"]
        if s["type"] == "animated":
            L += [f"**ANIMATION → `{s['animated_clip']}`**", "```",
                  compose_animation_prompt(s, i), "```"]
        L.append("")
    Path(out_path).write_text("\n".join(L))


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Generate images + Kling clips from a lean storyboard.json")
    ap.add_argument("--storyboard", default="storyboard.json")
    ap.add_argument("--style-card", default=str(SCRIPT_DIR / "style_card.txt"))
    ap.add_argument("--only", choices=["image", "anim", "all"], default="all")
    ap.add_argument("--scenes", default="", help='e.g. "1,3,5-9" (default: all)')
    ap.add_argument("--ref", default="", help="reference image for consistency (default: auto scene 01)")
    ap.add_argument("--model", default=IMAGE_MODEL_DEFAULT, help="image model (e.g. gemini-3-pro-image for hero frames)")
    ap.add_argument("--mode", choices=["std", "pro"], default="std", help="Kling quality/cost mode")
    ap.add_argument("--force", action="store_true", help="regenerate even if the output exists")
    ap.add_argument("--dry-run", action="store_true", help="print the plan + one sample composed prompt; no API calls")
    ap.add_argument("--dump-prompts", nargs="?", const="", default=None,
                    help="write the composed prompt sheet (default: <project>/prompts.md) and exit")
    args = ap.parse_args()

    sb_path = Path(args.storyboard).resolve()
    root = sb_path.parent
    load_dotenv(SCRIPT_DIR / ".env", root / ".env", Path(".env"))
    sb = json.loads(sb_path.read_text())
    scenes = sb["scenes"]
    sel = parse_scene_selection(args.scenes, len(scenes))

    accent_hex = sb.get("accent_hex", "#3D5A80")
    anchor_strength = sb.get("style_anchor_strength", 0.7)
    style_prefix = load_style_prefix(args.style_card)

    # --dump-prompts: compose the full prompts into a review sheet and exit.
    if args.dump_prompts is not None:
        out = Path(args.dump_prompts) if args.dump_prompts else (root / "prompts.md")
        write_prompt_sheet(scenes, accent_hex, anchor_strength, style_prefix, out)
        print(f"wrote {out}")
        return

    manifest_path = root / "assets_manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.is_file() else {}

    # ---- image pass ----
    if args.only in ("image", "all"):
        print(f"== IMAGE PASS ({args.model}) ==")
        sample_shown = False
        for i, s in enumerate(scenes, 1):
            if i not in sel:
                continue
            out = root / s["image"]
            if out.is_file() and not args.force:
                print(f"  scene {i:02d}  skip (exists)"); continue
            ref = args.ref or (str(root / "images/scene_01.png") if i != 1 else "")
            model = s.get("image_model", args.model)     # per-scene override (hero frames)
            prompt = compose_image_prompt(s, accent_hex, style_prefix, anchor_strength)
            print(f"  scene {i:02d}  image -> {s['image']}"
                  + (f"  [ref={Path(ref).name}]" if ref else "  [no ref]")
                  + (f"  [{model}]" if model != args.model else ""))
            if args.dry_run:
                if not sample_shown:
                    print(f"    ── sample composed prompt (scene {i:02d}) ──\n    {prompt}\n")
                    sample_shown = True
                continue
            try:
                generate_image(prompt, out, ref_path=ref, model=model)
                manifest.setdefault(f"scene_{i:02d}", {})["image"] = str(out)
            except Exception as e:
                print(f"    ERROR scene {i:02d} image: {e}")

    # ---- animation pass ----
    if args.only in ("anim", "all"):
        print(f"== ANIM PASS (Kling {KLING_MODEL}, mode={args.mode}) ==")
        for i, s in enumerate(scenes, 1):
            if i not in sel or s["type"] != "animated":
                continue
            still = root / s["image"]
            out = root / s["animated_clip"]
            if out.is_file() and not args.force:
                print(f"  scene {i:02d}  skip (exists)"); continue
            if not still.is_file() and not args.dry_run:
                print(f"  scene {i:02d}  SKIP — still missing ({s['image']}); run image pass first"); continue
            print(f"  scene {i:02d}  animate {s['image']} -> {s['animated_clip']} (~{s['duration']}s)")
            if args.dry_run:
                continue
            for attempt in range(1, KLING_RETRIES + 1):
                try:
                    kling_animate(still, compose_animation_prompt(s, i), s["duration"], args.mode, out)
                    manifest.setdefault(f"scene_{i:02d}", {})["clip"] = str(out)
                    break
                except Exception as e:
                    print(f"    attempt {attempt}/{KLING_RETRIES} failed: {e}")
                    if attempt == KLING_RETRIES:
                        print(f"    GRACEFUL DEGRADATION: leave scene {i:02d} as static "
                              f"(retag type='static' in storyboard.json; Ken Burns will cover it)")

    if not args.dry_run:
        manifest_path.write_text(json.dumps(manifest, indent=2))
        print(f"\nmanifest -> {manifest_path.name}")
    print("done.")


if __name__ == "__main__":
    main()

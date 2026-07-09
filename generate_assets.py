#!/usr/bin/env python3
"""
generate_assets.py — code-driven asset generation for The Engineering Atlas.

storyboard.json is the source of truth and stays LEAN: each scene carries only its
scene-specific `image_prompt` (subject), optional `accent`, and (animated) `animation_prompt`.
The full prompts are composed at generation time by prompt_builder.py
(style_card.txt prefix + scene_recipes + accent_hex + composition) — nothing boilerplate
is stored in the JSON.

Outputs the assembler expects:
    images/scene_NN.png          (all scenes)   — Gemini "nano banana" (Interactions API)
    clips/scene_NN_animated.mp4  (animated)     — Kling image-to-video (REST)

To preview the fully-composed prompts:  python prompt_builder.py <storyboard.json>

Setup
-----
    pip install google-genai pyjwt requests
    cp .env.example .env    # fill GEMINI_API_KEY, KLING_ACCESS_KEY, KLING_SECRET_KEY

Usage (from repo root)
----------------------
    SB=projects/001_chand_baori/storyboard.json
    python generate_assets.py --storyboard $SB --only image --scenes 1   # the anchor; eyeball it
    python generate_assets.py --storyboard $SB --only image             # the rest, referencing scene 1
    python generate_assets.py --storyboard $SB --only anim              # Kling clips from the stills
    python generate_assets.py --storyboard $SB --only all --dry-run     # plan + one sample prompt
"""

import argparse, base64, json, os, time
from pathlib import Path

from prompt_builder import context_from, compose_image_prompt, compose_animation_prompt

SCRIPT_DIR = Path(__file__).resolve().parent

# ── Config (override via env / CLI) ──────────────────────────────────────────
IMAGE_MODEL_DEFAULT = "gemini-3.1-flash-image"          # Nano Banana 2
KLING_BASE          = "https://api-singapore.klingai.com"
KLING_MODEL         = os.environ.get("KLING_MODEL", "kling-v2-6")
POLL_INTERVAL_S     = 10
POLL_TIMEOUT_S      = 600
KLING_RETRIES       = 2                                  # then flag for static fallback


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
    args = ap.parse_args()

    sb_path = Path(args.storyboard).resolve()
    root = sb_path.parent
    load_dotenv(SCRIPT_DIR / ".env", root / ".env", Path(".env"))
    sb = json.loads(sb_path.read_text())
    scenes = sb["scenes"]
    sel = parse_scene_selection(args.scenes, len(scenes))
    ctx = context_from(sb, args.style_card)    # accent_hex + recipes (from storyboard) + style prefix

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
            prompt = compose_image_prompt(s, ctx)
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

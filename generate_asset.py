#!/usr/bin/env python3
"""
generate_asset.py — reusable LIBRARY assets for assets_library/ (The Engineering Atlas).

Each asset: Gemini generates it on a flat magenta background (style anchor passed for
palette/line-weight lock) → Real-ESRGAN x4 (anime model) → magenta chroma-key to a clean
alpha with defringe → trim → assets_library/<category>/<name>.png (RGBA) → INDEX.md row.
Rules live in assets_library/STYLE_BIBLE.md — keep the two in sync.

Usage (from repo root):
    python generate_asset.py --batch assets_library/_batches/batch_01.json
    python generate_asset.py --category nature --name tree_banyan_01 --view flat \
        "a single large banyan tree with a broad layered canopy"
    python generate_asset.py --batch ... --dry-run
"""

import argparse, base64, json, os, subprocess, tempfile
from pathlib import Path

import numpy as np
from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
LIB = SCRIPT_DIR / "assets_library"
RAW = LIB / "_raw"
ANCHOR = SCRIPT_DIR / "projects/001_chand_baori/images/scene_01.png"
IMAGE_MODEL = "gemini-3.1-flash-image"
ESRGAN = SCRIPT_DIR / "tools/realesrgan/realesrgan-ncnn-vulkan"
ESRGAN_MODELS = SCRIPT_DIR / "tools/realesrgan/models"
BG = np.array([255.0, 0.0, 255.0])                      # pure magenta

# Mirrors STYLE_BIBLE.md → "Core look" + palette. Update both together.
STYLE = (
    "Flat-design technical illustration for an educational animation library. Clean vector "
    "aesthetic, thick clean charcoal outlines (#2C2C2C), flat fills with soft warm shading, "
    "warm golden-hour light from the upper-left. Palette: cream #FAF7F2, sand #F0D8B0 / "
    "#E8D8C0, shadow brown #B09878, muted sage green #9C9F77 for any vegetation. "
    "No text anywhere in the image. High precision, crafted, quietly dramatic."
)
VIEW = {
    "isometric": ("True isometric projection, the same isometric angle as an architectural "
                  "cutaway diagram."),
    "flat":      ("Straight-on flat 2D view (front or side profile as described), NOT "
                  "isometric — simple, bold, cartoon-diagram style."),
}
CHARACTER = (
    " Character design language: simple round head, black dot eyes, minimal or no nose, "
    "expression from eyebrows and mouth, about 3 heads tall, mitten hands with no fingers, "
    "warm brown skin #C68B59, simple block clothing from the palette."
)


def load_dotenv(*candidates):
    for p in candidates:
        p = Path(p)
        if p.is_file():
            for line in p.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def compose_prompt(spec):
    view = VIEW[spec.get("view", "flat")]
    character = CHARACTER if spec["category"] in ("characters", "military") else ""
    anchor_clause = (
        " || A style reference image is attached: take the palette, line weight and rendering "
        "style from it, but IGNORE its subject and its parchment background entirely."
        if spec.get("anchor", True) else ""
    )
    return (
        f"{STYLE}{character} || Single isolated asset: {spec['subject'].strip()}. || View: {view} "
        f"|| Background: the ENTIRE background is one solid uniform flat pure magenta (#FF00FF) — "
        f"no gradient, no texture, no vignette, and the subject casts NO shadow on the background. "
        f"Nothing else in frame. The subject is centered, fully inside the frame, with generous "
        f"margins on all sides, never touching an edge.{anchor_clause}"
    )


def generate_raw(prompt, out_path, use_anchor=True):
    from google import genai
    from google.genai import types
    client = genai.Client()                              # GEMINI_API_KEY from env
    parts = [types.Part.from_text(text=prompt)]
    if use_anchor:
        raw = ANCHOR.read_bytes()
        mime = "image/png" if raw[:8] == b"\x89PNG\r\n\x1a\n" else "image/jpeg"
        parts.append(types.Part.from_bytes(data=raw, mime_type=mime))
    resp = client.models.generate_content(model=IMAGE_MODEL, contents=parts)
    for cand in (resp.candidates or []):
        for part in (getattr(cand.content, "parts", None) or []):
            data = getattr(getattr(part, "inline_data", None), "data", None)
            if data:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(base64.b64decode(data) if isinstance(data, str) else data)
                return
    raise RuntimeError("no image returned (output modality / safety block)")


def upscale4x(src):
    """Real-ESRGAN x4 (anime model) BEFORE keying — the alpha edge is cut at 4x resolution."""
    if not ESRGAN.is_file():
        return Image.open(src).convert("RGB")
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
        tmp = Path(tf.name)
    p = subprocess.run([str(ESRGAN), "-i", str(src), "-o", str(tmp),
                        "-n", "realesrgan-x4plus-anime", "-m", str(ESRGAN_MODELS)],
                       capture_output=True, text=True)
    if p.returncode != 0 or not tmp.is_file() or tmp.stat().st_size == 0:
        print(f"    upscale failed (rc={p.returncode}) — keying at native res")
        return Image.open(src).convert("RGB")
    im = Image.open(tmp).convert("RGB")
    tmp.unlink(missing_ok=True)
    return im


def key_magenta(im):
    """Chroma-key the flat magenta bg: smoothstep alpha on RGB distance + defringe,
    then trim to the subject with a 2% margin."""
    a = np.asarray(im, dtype=np.float32)
    corners = np.concatenate([a[:40, :40].reshape(-1, 3), a[:40, -40:].reshape(-1, 3),
                              a[-40:, :40].reshape(-1, 3), a[-40:, -40:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    if np.linalg.norm(bg - BG) > 120:
        print(f"    WARNING: corners are not magenta (got {bg.astype(int)}) — model ignored the "
              f"background instruction; keying against the corner color instead")
    d = np.linalg.norm(a - bg, axis=2)
    t0, t1 = 60.0, 140.0
    alpha = np.clip((d - t0) / (t1 - t0), 0.0, 1.0)
    alpha = alpha * alpha * (3 - 2 * alpha)              # smoothstep
    # defringe: un-blend the bg color out of semi-transparent edge pixels
    mask = (alpha > 0.02) & (alpha < 0.98)
    al = alpha[..., None]
    unmixed = np.clip((a - (1.0 - al) * bg) / np.maximum(al, 1e-3), 0, 255)
    a = np.where(mask[..., None], unmixed, a)
    out = np.dstack([a, alpha[..., None] * 255.0]).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")
    bbox = Image.fromarray((alpha * 255).astype(np.uint8), "L").getbbox()
    if bbox:
        pad = int(0.02 * max(img.size))
        img = img.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad),
                        min(img.width, bbox[2] + pad), min(img.height, bbox[3] + pad)))
    return bleed_edges(img)


def bleed_edges(img, iterations=12):
    """Straight-alpha edge padding: push opaque RGB outward into the transparent zone so
    scaling/blurring in AE never samples the keyed-out magenta as a pink fringe."""
    rgba = np.asarray(img).copy()
    rgb = rgba[..., :3].astype(np.float32)
    filled = rgba[..., 3] > 0
    for _ in range(iterations):
        if filled.all():
            break
        grow = np.zeros_like(rgb)
        cnt = np.zeros(filled.shape, np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nb = np.roll(filled, (dy, dx), (0, 1))
            src = np.roll(rgb, (dy, dx), (0, 1))
            m = nb & ~filled
            grow[m] += src[m]
            cnt[m] += 1
        new = cnt > 0
        rgb[new] = grow[new] / cnt[new][:, None]
        filled |= new
    if not filled.all():                                  # far interior: neutral, not magenta
        rgb[~filled] = rgb[rgba[..., 3] > 0].mean(axis=0)
    rgba[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def index_append(rows):
    idx = LIB / "INDEX.md"
    lines = idx.read_text().splitlines() if idx.is_file() else []
    names = {r["name"] for r in rows}
    lines = [l for l in lines if "*(empty" not in l
             and not any(l.startswith(f"| {n} |") for n in names)]
    lines += [f"| {r['name']} | {r['category']} | {r['category']}/{r['name']}.png "
              f"| {r.get('notes', '')} |" for r in rows]
    idx.write_text("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser(description="Generate transparent library assets (see STYLE_BIBLE.md)")
    ap.add_argument("subject", nargs="?", default="", help="single-asset subject description")
    ap.add_argument("--batch", default="", help="JSON list of {category,name,view,subject,notes}")
    ap.add_argument("--category", default=""); ap.add_argument("--name", default="")
    ap.add_argument("--view", default="flat", choices=list(VIEW))
    ap.add_argument("--no-upscale", action="store_true")
    ap.add_argument("--force", action="store_true", help="regenerate even if the asset exists")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    load_dotenv(SCRIPT_DIR / ".env")
    if args.batch:
        specs = json.loads(Path(args.batch).read_text())
    else:
        if not (args.category and args.name and args.subject):
            ap.error("need --batch, or --category + --name + a subject")
        specs = [{"category": args.category, "name": args.name,
                  "view": args.view, "subject": args.subject}]

    done = []
    for spec in specs:
        out = LIB / spec["category"] / f"{spec['name']}.png"
        raw = RAW / f"{spec['name']}_raw.png"
        tag = f"{spec['category']}/{spec['name']}"
        if out.is_file() and not args.force:
            print(f"  {tag}  skip (exists)"); continue
        prompt = compose_prompt(spec)
        if args.dry_run:
            print(f"  {tag}  [{spec.get('view', 'flat')}]\n    {prompt}\n"); continue
        print(f"  {tag}  generating…")
        try:
            if not raw.is_file():                        # --force reprocesses from the kept raw;
                generate_raw(prompt, raw, spec.get("anchor", True))   # delete the raw to re-bill

            im = Image.open(raw).convert("RGB") if args.no_upscale else upscale4x(raw)
            img = key_magenta(im)
            out.parent.mkdir(parents=True, exist_ok=True)
            img.save(out)
            print(f"    -> {out.relative_to(SCRIPT_DIR)}  {img.width}x{img.height}")
            done.append(spec)
        except Exception as e:
            print(f"    ERROR {tag}: {e}")

    if done:
        index_append(done)
        print(f"\nINDEX.md updated (+{len(done)} assets)")


if __name__ == "__main__":
    main()

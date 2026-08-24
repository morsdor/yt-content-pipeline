#!/usr/bin/env python3
"""
generate_thumbnail.py — A/B thumbnail candidates for The Engineering Atlas.

The packaging gate (thumbnail-workflow SKILL Stage 2) needs 3 thumbnail candidates that
vary ONE axis, generated full-bleed at 16:9. That is neither of the other two generators:
generate_asset.py makes magenta-keyed LIBRARY cutouts (transparent, single subject, no
scene); generate_images.py makes STORYBOARD scene plates (always style-card-prefixed).
A thumbnail is a full-bleed 1280x720 scene with a dark moody background and NO style card.

This tool composes the SKILL's Stage-2 base prompt around a locked concept + accent,
appends exactly ONE varied axis per candidate (crop tightness by default), and writes
<project>/output/thumb_{a,b,c}.png. Text is NEVER generated — typography is added locally
in Stage 4 (Fraunces Bold), because AI lettering reads as slop (SKILL rule 3).

Charged (Gemini image model, same one the plate pass uses). Gated: --dry-run previews the
composed prompts with no API call; a real run requires --yes.

Usage (from repo root)
----------------------
    P=projects/001_roman_aqueduct
    python generate_thumbnail.py --project $P \
        --subject "a monumental ancient Roman aqueduct ..." \
        --accent "electric cyan-blue #22B8E0" --vary crop --dry-run
    python generate_thumbnail.py --project $P --subject "..." --accent "..." --vary crop --yes
"""

import argparse, base64, os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
IMAGE_MODEL_DEFAULT = "gemini-3.1-flash-image"          # same model as the plate pass

# A/B axes. Vary exactly ONE across a/b/c, or the test teaches nothing (SKILL rule 2).
VARIATIONS = {
    "crop": [
        ("a", "Framing: wide establishing shot — the structure recedes across a vast "
              "landscape to a distant vanishing point, emphasizing sheer scale and distance."),
        ("b", "Framing: medium shot — the structure fills the lower two-thirds of the frame, "
              "its strong leading line drawing the eye to the vanishing point."),
        ("c", "Framing: tight dramatic crop on the nearest edge of the structure with heavy "
              "foreshortening, the leading line rushing away to a distant vanishing point."),
    ],
}

# SKILL Stage-2 base prompt — deliberately NO style-card prefix.
BASE = (
    "Dramatic isometric illustration of {subject}. {palette} High contrast, bold "
    "composition, one clear focal point, cinematic lighting, deep moody dark background, "
    "extremely detailed and eye-catching, YouTube thumbnail style, 16:9 aspect ratio, "
    "1280x720. {composition} {variation} "
    "Absolutely NO text, letters, numbers, watermarks or logos anywhere in the image."
)

# Per-channel look. The two channels are deliberately opposite palettes — running EA's
# warm-parchment clause for the software channel silently produces off-brand plates, and
# you only find out after paying for them. See brand_guide.md vs brand_guide_software.md §3.
BRANDS = {
    "ea": {
        "accent": "electric cyan-blue #22B8E0",
        "palette": "Vibrant {accent} as the single pop colour against warm tan and ochre stone;",
        "composition": "",
        "why": "The Engineering Atlas — warm parchment, daylight, stone.",
    },
    "depthfirst": {
        "accent": "electric blue #4DA3FF",
        "palette": (
            "Near-black blue-black ground (#0B0E14) with cold graphite structure; vibrant "
            "{accent} as the single pop colour, carried only by glowing windows, rim-light "
            "and power-line arcs. NO warm tan, NO ochre, NO parchment, NO daylight, no warm "
            "sunset tones. Schematic and disciplined like a drafting table, not a glossy "
            "product render."
        ),
        # The layout convention is locked for every video on this channel
        # (brand_guide_software.md §2 / thumbnail.md): subject right, type left.
        "composition": (
            "Composition: place the subject in the RIGHT two-thirds of the frame. Keep the "
            "LEFT third clean, dark and near-empty — typography is composited there later. "
            "Keep the lower-left foreground an uncluttered dark plane with nothing important "
            "in it — a graphic element is composited there later."
        ),
        "why": "Depth First — ink-black, schematic, high-contrast (brand_guide_software.md §3).",
    },
}


def load_dotenv(*candidates):
    for p in candidates:
        p = Path(p)
        if p.is_file():
            for line in p.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def generate_image(prompt, out_path, model=IMAGE_MODEL_DEFAULT):
    """Text-to-image via google-genai `models.generate_content`. No reference images: a
    thumbnail is its own look, not anchored to the scene plates."""
    from google import genai                 # lazy import so --dry-run/--help need no deps
    from google.genai import types
    client = genai.Client()                  # reads GEMINI_API_KEY from env
    resp = client.models.generate_content(
        model=model, contents=[types.Part.from_text(text=prompt)])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    for cand in (resp.candidates or []):
        for part in (getattr(cand.content, "parts", None) or []):
            data = getattr(getattr(part, "inline_data", None), "data", None)
            if data:
                out_path.write_bytes(base64.b64decode(data) if isinstance(data, str) else data)
                return
    raise RuntimeError("no image returned (check model output modality / safety block)")


def main():
    ap = argparse.ArgumentParser(description="Generate 3 A/B thumbnail candidates (Gemini). See thumbnail-workflow SKILL Stage 2.")
    ap.add_argument("--project", required=True, help="project dir, e.g. projects/001_roman_aqueduct")
    ap.add_argument("--subject", required=True, help="the locked thumbnail concept's dominant object, described")
    ap.add_argument("--brand", default="ea", choices=list(BRANDS),
                    help="which channel's look to compose (default: ea). 'depthfirst' = the software channel")
    ap.add_argument("--accent", default=None, help="the single pop colour (default: the brand's)")
    ap.add_argument("--vary", default="crop", choices=list(VARIATIONS), help="the ONE axis to A/B")
    ap.add_argument("--model", default=IMAGE_MODEL_DEFAULT, help="image model (gemini-3-pro-image for a hero re-render)")
    ap.add_argument("--force", action="store_true", help="regenerate even if the output exists")
    ap.add_argument("--dry-run", action="store_true", help="print composed prompts; no API call, no charge")
    ap.add_argument("--yes", action="store_true", help="confirm the CHARGED batch (required to actually generate)")
    args = ap.parse_args()

    load_dotenv(SCRIPT_DIR / ".env", Path(args.project) / ".env", Path(".env"))
    out_dir = Path(args.project) / "output"
    brand = BRANDS[args.brand]
    accent = args.accent or brand["accent"]
    prompts = [(tag, BASE.format(subject=args.subject.strip(),
                                 palette=brand["palette"].format(accent=accent),
                                 composition=brand["composition"],
                                 variation=v))
               for tag, v in VARIATIONS[args.vary]]

    print(f"== THUMBNAIL PASS ({args.model}) — brand: {args.brand} — vary: {args.vary} ==")
    print(f"   {brand['why']}  accent: {accent}")
    for tag, _ in prompts:
        print(f"  thumb_{tag} -> {out_dir}/thumb_{tag}.png")

    if args.dry_run:
        print("\n-- composed prompts (dry-run — no API calls, nothing billed) --")
        for tag, prompt in prompts:
            print(f"\n[thumb_{tag}]\n{prompt}")
        return

    if not args.yes:
        print(f"\n⚠ CHARGED: {len(prompts)} images on {args.model}. Re-run with --yes to submit, "
              f"or --dry-run to preview the prompts. Nothing generated.")
        return

    done = 0
    for tag, prompt in prompts:
        out = out_dir / f"thumb_{tag}.png"
        if out.is_file() and not args.force:
            print(f"  thumb_{tag}  skip (exists — use --force to redo)"); continue
        try:
            generate_image(prompt, out, args.model)
            print(f"    -> {out.relative_to(SCRIPT_DIR) if out.is_absolute() else out}")
            done += 1
        except Exception as e:
            print(f"    ERROR thumb_{tag}: {e}")
    print(f"\ndone (+{done} candidates). Next: 120px squint test, then add text locally "
          f"(Fraunces Bold, Stage 4), then YouTube Test & Compare + log in assets/thumbnails_log.md.")


if __name__ == "__main__":
    main()

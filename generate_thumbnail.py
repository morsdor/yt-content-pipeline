#!/usr/bin/env python3
"""
generate_thumbnail.py — A/B thumbnail candidates for The Engineering Atlas.

The packaging gate (thumbnail-workflow SKILL Stage 2) needs 3 thumbnail candidates that
vary ONE axis, generated full-bleed at 16:9. That is neither of the other two generators:
generate_asset.py makes magenta-keyed LIBRARY cutouts (transparent, single subject, no
scene); generate_images.py makes STORYBOARD scene plates (always style-card-prefixed).
A thumbnail is a full-bleed 1280x720 scene with a dark moody background and NO style card.

This tool composes the SKILL's Stage-2 base prompt around a locked concept + accent,
appends exactly ONE varied axis per candidate (--vary: crop | pairing), and writes
<project>/output/thumb_{a,b,c}.png. Text is NEVER generated — typography is added locally
in Stage 4 by add_thumbnail_text.py (EA: Fraunces Bold · Depth First: Archivo Black),
because AI lettering reads as slop (SKILL rule 3). Same rule kills AI-drawn logos.

Charged. Defaults to gemini-3-pro-image — deliberately NOT the plate pass's flash model;
see the note by IMAGE_MODEL_DEFAULT. Gated: --dry-run previews the composed prompts with
no API call; a real run requires --yes.

Usage (from repo root)
----------------------
    # The Engineering Atlas — a linear structure, so vary the crop
    P=projects/001_roman_aqueduct
    python generate_thumbnail.py --project $P --brand ea \
        --subject "a monumental ancient Roman aqueduct ..." --vary crop --dry-run

    # Depth First — a two-object relationship, so vary the pairing
    P=projects/s001_ai_physical_cost
    python generate_thumbnail.py --project $P --brand depthfirst \
        --subject "a colossal nuclear cooling tower ... wired to a hyperscale datacenter" \
        --vary pairing --dry-run
    # ... then re-run with --yes to submit (CHARGED)
"""

import argparse, base64, os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# ⚠ This pass DELIBERATELY diverges from generate_images.py / generate_asset.py, which
# default to gemini-3.1-flash-image. Do not "fix" this back for consistency.
#   - The plate pass generates ~60 images/video; flash is what keeps that at ~₹450.
#   - This pass generates 3, and they are the only images that decide whether anyone
#     ever sees the other 60. Pro costs ~$0.134 vs ~$0.086 — a ~₹13 delta on a batch.
#   - The real reason is prompt adherence, not polish: the composed prompt stacks three
#     spatial constraints (subject right two-thirds · left third clear for type · lower-left
#     foreground clear for the phone composite). A dropped constraint isn't a slightly worse
#     thumbnail, it's an unusable one — and a re-run costs more than the upgrade.
# 1K and 2K are priced identically, so ask for 2K and downscale to 1280x720 — free sharpness.
IMAGE_MODEL_DEFAULT = "gemini-3-pro-image"

# A/B axes. Vary exactly ONE across a/b/c, or the test teaches nothing (SKILL rule 2).
VARIATIONS = {
    # Written for LINEAR structures (aqueducts, bridges) — a single subject whose leading
    # line carries the frame. Wrong axis for a two-object composition; see "pairing".
    "crop": [
        ("a", "Framing: wide establishing shot — the structure recedes across a vast "
              "landscape to a distant vanishing point, emphasizing sheer scale and distance."),
        ("b", "Framing: medium shot — the structure fills the lower two-thirds of the frame, "
              "its strong leading line drawing the eye to the vanishing point."),
        ("c", "Framing: tight dramatic crop on the nearest edge of the structure with heavy "
              "foreshortening, the leading line rushing away to a distant vanishing point."),
    ],
    # For concepts whose hook is a RELATIONSHIP between two objects (s001: the machine that
    # answers vs. the machine that powers it). Varies how the two are weighed against each
    # other — i.e. how much scale-shock wins in this niche — not how tightly they're cropped.
    "pairing": [
        ("a", "Framing: the power source dominates — it towers over the frame while the "
              "computing facility sits small and bright at its foot, dwarfed by what feeds it."),
        ("b", "Framing: the two structures stand side by side at equal visual weight, "
              "explicitly joined by the heavy cable run between them, so the frame reads as "
              "a single wired circuit."),
        ("c", "Framing: a whole horizon of identical computing facilities recedes into the "
              "distance, all of them converging by cable on the one power source — the fleet, "
              "not the building."),
    ],
}

# SKILL Stage-2 base prompt — deliberately NO style-card prefix.
BASE = (
    "Dramatic isometric illustration of {subject}. {palette} High contrast, bold "
    "composition, one clear focal point, cinematic lighting, deep moody dark background, "
    "extremely detailed and eye-catching, YouTube thumbnail style, 16:9 aspect ratio, "
    "1280x720. {composition} {variation} {facts} "
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
            "and illuminated cable runs. NO warm tan, NO ochre, NO parchment, NO daylight, no warm "
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
    ap.add_argument("--facts", default="", help="physical-accuracy constraints the model gets wrong "
                    "unprompted (the thumbnail's visual_facts). Stated as positives + explicit negatives.")
    ap.add_argument("--only", default=None, help="regenerate just these candidates, e.g. 'b' or 'a,c' "
                    "— so fixing one does not pay for three")
    ap.add_argument("--model", default=IMAGE_MODEL_DEFAULT, help="image model (default: pro — see the note by IMAGE_MODEL_DEFAULT; gemini-3.1-flash-image to economise)")
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
                                 variation=v,
                                 facts=args.facts.strip()))
               for tag, v in VARIATIONS[args.vary]]
    if args.only:
        keep = {t.strip() for t in args.only.split(",") if t.strip()}
        prompts = [(t, pr) for t, pr in prompts if t in keep]
        if not prompts:
            raise SystemExit(f"--only {args.only!r} matched no candidate in --vary {args.vary}")

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

#!/usr/bin/env python3
"""add_thumbnail_text.py — Stage-4 local typography for Engineering Atlas thumbnails.

`thumbnail-workflow` SKILL Stage 4: thumbnail text is stamped on LOCALLY with the channel's
real font (Fraunces Bold), and is **NEVER** produced by the image model — AI lettering reads
as slop and breaks the brand. This is the second half of the thumbnail toolchain:
`generate_thumbnail.py` renders the text-free plate (Stage 2); this stamps the locked words
(from `packaging.md`) onto it. Pure Pillow — local, ₹0, no network, no API.

The word goes over CLEAN DARK SPACE, opposite the subject: pick the corner with `--corner`
(tl/tr/bl/br) after eyeballing the plate. A soft drop-shadow keeps white type legible even
where the background is only mostly-dark.

Usage
-----
    python add_thumbnail_text.py \
        --input  projects/001_roman_aqueduct/output/thumb_a.png \
        --output projects/001_roman_aqueduct/output/thumb_a_text.png \
        --hero "2.5 cm" --sub "across this bridge" --corner tr
"""
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
FONT_DEFAULT = SCRIPT_DIR / "assets" / "fonts" / "Fraunces-Bold.ttf"


def render(inp, outp, hero, sub, corner, font_path, color, shadow_rgba):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    img = Image.open(inp).convert("RGBA")
    W, H = img.size
    hero_px = max(24, int(H * 0.155))
    sub_px = max(14, int(H * 0.052))
    margin = int(W * 0.045)
    gap = int(hero_px * 0.22)

    hero_font = ImageFont.truetype(str(font_path), hero_px)
    sub_font = ImageFont.truetype(str(font_path), sub_px) if sub else None

    measure = ImageDraw.Draw(img)
    def size(text, font):
        l, t, r, b = measure.textbbox((0, 0), text, font=font)
        return r - l, b - t, l, t          # width, height, left-bearing, top-bearing
    hw, hh, hlx, hty = size(hero, hero_font)
    sw, sh, slx, sty = size(sub, sub_font) if sub else (0, 0, 0, 0)

    block_w = max(hw, sw)
    block_h = hh + (gap + sh if sub else 0)
    right = corner in ("tr", "br")
    bottom = corner in ("bl", "br")
    x0 = (W - margin - block_w) if right else margin
    y0 = (H - margin - block_h) if bottom else margin

    hx = (x0 + block_w - hw) if right else x0     # align each line to the block edge
    sx = (x0 + block_w - sw) if right else x0
    hpos = (hx - hlx, y0 - hty)                    # cancel the glyph bbox offset
    spos = (sx - slx, y0 + hh + gap - sty)

    off = max(2, int(hero_px * 0.045))
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.text((hpos[0] + off, hpos[1] + off), hero, font=hero_font, fill=shadow_rgba)
    if sub:
        sd.text((spos[0] + off, spos[1] + off), sub, font=sub_font, fill=shadow_rgba)
    shadow = shadow.filter(ImageFilter.GaussianBlur(max(2, int(hero_px * 0.06))))
    img = Image.alpha_composite(img, shadow)

    d = ImageDraw.Draw(img)
    d.text(hpos, hero, font=hero_font, fill=color)
    if sub:
        d.text(spos, sub, font=sub_font, fill=color)

    Path(outp).parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(outp, "PNG")
    return W, H, hero_px, sub_px


def main():
    ap = argparse.ArgumentParser(description="Stamp Stage-4 typography on a thumbnail plate (local, Fraunces Bold — never AI text).")
    ap.add_argument("--input", required=True, help="the text-free plate from generate_thumbnail.py")
    ap.add_argument("--output", required=True, help="where to write the captioned thumbnail")
    ap.add_argument("--hero", required=True, help="the big headline word/number (short reads best)")
    ap.add_argument("--sub", default="", help="optional smaller line under the hero")
    ap.add_argument("--corner", default="tr", choices=["tl", "tr", "bl", "br"],
                    help="corner to place text — over clean dark space, opposite the subject")
    ap.add_argument("--font", default=str(FONT_DEFAULT), help="TTF (default: assets/fonts/Fraunces-Bold.ttf)")
    ap.add_argument("--color", default="white", help="hero colour: 'white' or 'R,G,B'")
    args = ap.parse_args()

    if args.color.lower() == "white":
        color = (255, 255, 255, 255)
    else:
        r, g, b = (int(x) for x in args.color.split(","))
        color = (r, g, b, 255)

    if not Path(args.font).is_file():
        raise SystemExit(f"font not found: {args.font} (Stage 4 needs the real font — no AI text)")

    W, H, hpx, spx = render(args.input, args.output, args.hero, args.sub, args.corner,
                            args.font, color, (0, 0, 0, 235))
    print(f"✓ {args.output}  ({W}x{H}, hero {hpx}px + sub {spx}px, corner {args.corner})")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""review_images.py — build review artifacts for the visual-accuracy gate.

Turns the manual "open 54 files one by one" review into a few labeled montages an
agent (or you) can scan in a handful of looks. Read-only: it never calls an API and
never regenerates — it only composites what generate_images.py already produced.

Outputs into <project>/review/:
    contact_sheet_N.png   labeled grid(s) of the selected scene stills
    pairs/scene_NN.png     render | reference-photo, for scenes with a reference_image
                           (the geometry check — put them side by side)
    review_checklist.md    per-scene subject + facts + ref + an empty Verdict column

Usage (from repo root):
    SB=projects/001_chand_baori/storyboard.json
    python review_images.py --storyboard $SB                # all scenes
    python review_images.py --storyboard $SB --scenes 8-15  # a subset (one sheet)

Companion to the `visual-accuracy-gate` skill: build the sheets, then eyeball each
render against its facts (checklist) and reference photo (pairs), and fill verdicts.
"""
import argparse, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = Path(__file__).resolve().parent
BG   = (245, 240, 232)   # parchment (brand)
INK  = (44, 44, 44)      # charcoal
CELL_W, PAD, LABEL_H, COLS, PER_SHEET = 380, 10, 34, 3, 15

_FONTS = {}
def font(size):
    if size in _FONTS:
        return _FONTS[size]
    cands = sorted((SCRIPT_DIR / "assets/fonts").glob("*.tt[fc]")) if (SCRIPT_DIR / "assets/fonts").is_dir() else []
    cands += [Path("/System/Library/Fonts/Helvetica.ttc"), Path("/System/Library/Fonts/Supplemental/Arial.ttf")]
    for p in cands:
        try:
            _FONTS[size] = ImageFont.truetype(str(p), size); return _FONTS[size]
        except Exception:
            continue
    _FONTS[size] = ImageFont.load_default(); return _FONTS[size]


def parse_sel(spec, n):
    if not spec:
        return list(range(1, n + 1))
    out = set()
    for c in (x.strip() for x in spec.split(",")):
        if "-" in c:
            a, b = c.split("-"); out.update(range(int(a), int(b) + 1))
        elif c:
            out.add(int(c))
    return sorted(i for i in out if 1 <= i <= n)


def fit(path, w, h):
    """Open (content-sniffed, so a JPEG-in-.png is fine), fit into w×h, letterbox on parchment."""
    canvas = Image.new("RGB", (w, h), BG)
    if path and Path(path).is_file():
        im = Image.open(path).convert("RGB")
        im.thumbnail((w, h))
        canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    else:
        ImageDraw.Draw(canvas).text((8, h // 2), "(missing)", fill=INK, font=font(15))
    return canvas


def cell(path, label, w):
    h = int(w * 9 / 16)
    c = Image.new("RGB", (w, h + LABEL_H), INK)
    c.paste(fit(path, w, h), (0, 0))
    ImageDraw.Draw(c).text((6, h + 8), label, fill=BG, font=font(15))
    return c


def build_sheets(sel, scenes, root, out):
    cells = []
    for i in sel:
        s = scenes[i - 1]
        tag = "".join(t for t, k in (("F", "visual_facts"), ("R", "reference_image")) if s.get(k))
        cells.append(cell(root / s["image"],
                          f"{i:02d} {s.get('type','')[:4]}/{s.get('scene_type','')}" + (f"  [{tag}]" if tag else ""),
                          CELL_W))
    made = []
    for p in range(0, len(cells), PER_SHEET):
        chunk = cells[p:p + PER_SHEET]
        rows = (len(chunk) + COLS - 1) // COLS
        cw, ch = CELL_W, chunk[0].height
        sheet = Image.new("RGB", (COLS * cw + (COLS + 1) * PAD, rows * ch + (rows + 1) * PAD), BG)
        for idx, c in enumerate(chunk):
            r, col = divmod(idx, COLS)
            sheet.paste(c, (PAD + col * (cw + PAD), PAD + r * (ch + PAD)))
        fp = out / f"contact_sheet_{p // PER_SHEET + 1}.png"
        sheet.save(fp); made.append(fp)
    return made


def build_pairs(sel, scenes, root, out):
    pdir = out / "pairs"; pdir.mkdir(parents=True, exist_ok=True)
    made = []
    for i in sel:
        s = scenes[i - 1]
        if not s.get("reference_image"):
            continue
        w = 520; h = int(w * 9 / 16)
        pair = Image.new("RGB", (2 * w + 3 * PAD, h + 2 * PAD + LABEL_H), INK)
        pair.paste(fit(root / s["image"], w, h), (PAD, PAD))
        pair.paste(fit(root / s["reference_image"], w, h), (2 * PAD + w, PAD))
        d = ImageDraw.Draw(pair)
        d.text((PAD + 6, h + PAD + 8), f"scene {i:02d}  RENDER", fill=BG, font=font(15))
        d.text((2 * PAD + w + 6, h + PAD + 8), f"REFERENCE {Path(s['reference_image']).name}", fill=BG, font=font(15))
        fp = pdir / f"scene_{i:02d}.png"; pair.save(fp); made.append(fp)
    return made


def build_checklist(sel, scenes, out):
    rows = ["# Review checklist", "",
            "*Render vs. `visual_facts` (this file) and the reference photo (`pairs/`). Fill the Verdict column.*", "",
            "| Scene | type / scene_type | subject | facts | ref photo | Verdict |",
            "|:--|:--|:--|:--|:--|:--|"]
    for i in sel:
        s = scenes[i - 1]
        subj = (s.get("image_prompt", "")[:64]).replace("|", "/").replace("\n", " ")
        ref = Path(s["reference_image"]).name if s.get("reference_image") else "—"
        rows.append(f"| {i:02d} | {s.get('type','')}/{s.get('scene_type','')} | {subj}… | {len(s.get('visual_facts') or []) or '—'} | {ref} |  |")
    (out / "review_checklist.md").write_text("\n".join(rows) + "\n")


def main():
    ap = argparse.ArgumentParser(description="Build contact sheets + reference pairs + checklist for the accuracy gate")
    ap.add_argument("--storyboard", required=True)
    ap.add_argument("--scenes", default="", help='e.g. "8-15,29" (default: all)')
    args = ap.parse_args()
    sb_path = Path(args.storyboard).resolve(); root = sb_path.parent
    sb = json.loads(sb_path.read_text()); scenes = sb["scenes"]
    sel = parse_sel(args.scenes, len(scenes))
    out = root / "review"; out.mkdir(parents=True, exist_ok=True)
    sheets = build_sheets(sel, scenes, root, out)
    pairs = build_pairs(sel, scenes, root, out)
    build_checklist(sel, scenes, out)
    print(f"reviewed {len(sel)} scenes -> {len(sheets)} contact sheet(s), {len(pairs)} reference pair(s)")
    for s in sheets:
        print("  ", s.relative_to(root))
    print("   checklist ->", (out / "review_checklist.md").relative_to(root))


if __name__ == "__main__":
    main()

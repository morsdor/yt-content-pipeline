#!/usr/bin/env python3
"""flicker_check.py — measure temporal flicker of Kling clips; flag the ones to re-gen at 1080p.

Kling's 720p i2v shimmers on *dense repeating geometry in motion* (our step-lattice) — and
the per-frame 4K upscale amplifies it ~another 17%. It's structural aliasing, not filterable
noise (temporal denoise doesn't touch it). The fix is native 1080p on those scenes only.

But you can't tell which scenes flicker from the storyboard keyword (a "lattice" establishing
shot can be perfectly smooth if the lattice is small/far and the motion gentle). So MEASURE the
720p output and upgrade only what crosses the line — that's the cheapest correct hybrid.

  flicker_HF : mean |Δ(high-pass frame)| over the clip — fine-detail shimmer with the intended
               slow motion filtered out. Measured at 480p so resolution doesn't bias it.

Observed (Chand Baori, v3_0 720p): smooth scenes ~0.3–1.0; dense-lattice-in-motion ~8–10.
Nothing lands between — so a threshold of ~3 cleanly separates "fine at 720p" from "needs 1080p".

Usage:
    python flicker_check.py projects/NNN/clips/*.mp4            # table + flags
    python flicker_check.py projects/NNN/clips --threshold 3.0
"""
import argparse, subprocess, tempfile, shutil, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter


def flicker_hf(mp4, w=480):
    tmp = Path(tempfile.mkdtemp())
    try:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4),
                        "-vf", f"scale={w}:-1,format=gray", str(tmp / "%05d.png")], check=True)
        hps = []
        for f in sorted(tmp.glob("*.png")):
            im = Image.open(f).convert("L")
            g = np.asarray(im, dtype=np.float32)
            gb = np.asarray(im.filter(ImageFilter.GaussianBlur(2)), dtype=np.float32)
            hps.append(g - gb)
        if len(hps) < 2:
            return 0.0
        return float(np.mean(np.abs(np.diff(np.stack(hps), axis=0))))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description="Measure clip flicker; flag ones to re-gen at 1080p")
    ap.add_argument("paths", nargs="+", help="clip files or a directory")
    ap.add_argument("--threshold", type=float, default=3.0, help="flicker_HF above this → re-gen at 1080p (default 3.0)")
    a = ap.parse_args()
    clips = []
    for p in map(Path, a.paths):
        clips += sorted(p.glob("*.mp4")) if p.is_dir() else [p]
    clips = [c for c in clips if c.is_file()]
    if not clips:
        print("no clips found"); sys.exit(1)
    print(f"{'clip':>34} {'flicker_HF':>11}   verdict")
    flagged = []
    for c in clips:
        hf = flicker_hf(c)
        flag = hf > a.threshold
        if flag:
            flagged.append(c)
        print(f"{c.name:>34} {hf:>11.3f}   {'⚠ RE-GEN AT 1080p' if flag else 'ok (720p→4K)'}")
    print(f"\n{len(flagged)} of {len(clips)} clips exceed {a.threshold} → re-generate at 1080p:")
    for c in flagged:
        print("  ", c.name)


if __name__ == "__main__":
    main()

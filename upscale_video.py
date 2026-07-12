#!/usr/bin/env python3
"""upscale_video.py — AI-upscale a video to 4K locally with Real-ESRGAN (free, offline).

Extracts frames, runs `realesr-animevideov3` (the anime/illustration *video* model —
temporally stable, purpose-built for line art like our isometric scenes), then
re-encodes at the source fps. No audio is added: Engineering Atlas clips are silent
by design (narration + music are mixed at assembly).

Companion to the accuracy gate's Stage D. Free alternative to native-4K Kling credits:
generate at 720p, upscale here. On flat illustrated content the result is ~indistinguishable
from native 1080p/4K.

Usage (from repo root):
    python upscale_video.py in.mp4 out.mp4                    # 720p -> 4K (x3, then fit 3840x2160)
    python upscale_video.py in.mp4 out.mp4 --scale 4 --crf 14 # sharper/heavier
    python upscale_video.py in.mp4 out.mp4 --target none      # keep the raw xN size

Requires: ffmpeg/ffprobe on PATH, and the Real-ESRGAN ncnn-vulkan bundle under
tools/realesrgan/ (binary + models/). See docs for the one-time install.
"""
import argparse, subprocess, tempfile, shutil, time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REBIN    = SCRIPT_DIR / "tools" / "realesrgan" / "realesrgan-ncnn-vulkan"
REMODELS = SCRIPT_DIR / "tools" / "realesrgan" / "models"


def probe_fps(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=r_frame_rate", "-of", "default=nk=1:nw=1", str(path)]
    ).decode().strip()
    return out if "/" in out else f"{out}/1"


def main():
    ap = argparse.ArgumentParser(description="AI-upscale a video to 4K with Real-ESRGAN (local, free)")
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--scale", type=int, default=3, choices=[2, 3, 4], help="AI upscale factor (default 3: 720p->~4K)")
    ap.add_argument("--model", default="realesr-animevideov3", help="realesr-animevideov3 | realesrgan-x4plus-anime | realesrgan-x4plus")
    ap.add_argument("--target", default="3840x2160", help="final WxH via lanczos, or 'none' to keep the raw xN size")
    ap.add_argument("--crf", type=int, default=16, help="x264 quality (lower=better, 14-18 sensible)")
    ap.add_argument("--bin", default=str(REBIN))
    ap.add_argument("--models", default=str(REMODELS))
    ap.add_argument("--jobs", default="2:4:4", help="realesrgan load:proc:save threads")
    a = ap.parse_args()

    inp, outp = Path(a.input), Path(a.output)
    if not inp.is_file():
        raise SystemExit(f"input not found: {inp}")
    if not Path(a.bin).is_file():
        raise SystemExit(f"Real-ESRGAN binary not found: {a.bin}\n  install the ncnn-vulkan bundle under tools/realesrgan/")
    outp.parent.mkdir(parents=True, exist_ok=True)
    fps = probe_fps(inp)
    tmp = Path(tempfile.mkdtemp(prefix="upscale_"))
    fdir, udir = tmp / "in", tmp / "out"
    fdir.mkdir(); udir.mkdir()
    t0 = time.time()
    try:
        print(f"[1/3] extracting frames @ {fps} ...")
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", str(inp),
                               "-vsync", "0", str(fdir / "%08d.png")])
        n = len(list(fdir.glob("*.png")))
        print(f"      {n} frames")
        print(f"[2/3] upscaling x{a.scale} with {a.model} (slow step; CPU-bound under Rosetta) ...")
        subprocess.check_call([a.bin, "-i", str(fdir), "-o", str(udir),
                               "-n", a.model, "-s", str(a.scale), "-m", a.models,
                               "-j", a.jobs, "-f", "png"])
        vf = [] if a.target == "none" else ["-vf", f"scale={a.target.replace('x', ':')}:flags=lanczos"]
        print(f"[3/3] encoding {'raw xN' if a.target=='none' else a.target} h264 crf{a.crf} @ {fps} ...")
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", fps,
                               "-i", str(udir / "%08d.png"), *vf,
                               "-c:v", "libx264", "-crf", str(a.crf),
                               "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(outp)])
        print(f"done -> {outp}  ({n} frames in {time.time()-t0:.0f}s, {(time.time()-t0)/max(n,1):.2f}s/frame)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()

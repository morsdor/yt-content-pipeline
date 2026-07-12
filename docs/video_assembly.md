# Video Assembly

*Part of the [pipeline docs](../pipeline_automation.md). Assembly is fully local and AI-free: `video_assembler.py` (ffmpeg/moviepy).*

## Running the Assembler

```bash
cd "/Users/mritunjaymohitesh/dev/yt video ideas"

# Fast review render (default 1080p)
python video_assembler.py \
  --storyboard ./projects/001_roman_aqueducts/storyboard.json \
  --output ./projects/001_roman_aqueducts/output/review.mp4

# Publish master — 4K. Feed it the 4K-upscaled clips + 4K stills (Stage D).
python video_assembler.py \
  --storyboard ./projects/001_roman_aqueducts/storyboard.json \
  --output ./projects/001_roman_aqueducts/output/final_video.mp4 \
  --resolution 2160p
```

**`--resolution`** — `1080p` (default, fast) · `2160p`/`4k` (publish master) · `1440p`. This is the last mile of the [upscaling](upscaling.md) strategy: upscaling clips/stills to 4K only reaches the viewer if the master is rendered at **2160p** — at 1080p the assembler downscales your 4K assets away. Font size, Ken Burns headroom, text offsets and the encode bitrate (8 Mbps → 40 Mbps at 4K) all scale with the chosen resolution, so overlays stay correctly proportioned. 4K assembly is ~4× the pixels — notably slower in moviepy, so render 1080p while iterating and 2160p once for the upload.

## What the Assembler Does

For each scene in the storyboard:
1. Loads the image and scales it up (adds zoom headroom)
2. Applies the specified Ken Burns motion (or auto-cycles through motions)
3. Adds staggered/timed text overlays with semi-transparent dark background bars based on the `texts` array
4. Applies 0.5-second crossfade to next scene

After all scenes:
5. Concatenates all scene clips
6. Mixes voiceover audio (full volume)
7. Mixes background music (8% volume by default)
8. Exports h264 MP4 at the `--resolution` (default 1080p; `2160p` for the publish master)

## Motion Types

| Motion | Effect | Best for |
|:---|:---|:---|
| `zoom_in` | Slow zoom into center | Establishing shots, wide views |
| `zoom_out` | Start tight, pull back | Reveals, "big picture" moments |
| `pan_left` | Slide right → left | Timelines, sequences |
| `pan_right` | Slide left → right | Following a path, flow |
| `pan_up` | Slide bottom → top | Tall structures, vertical reveals |
| `zoom_detail` | Zoom into specific point (x, y) | Callouts, mechanism close-ups |

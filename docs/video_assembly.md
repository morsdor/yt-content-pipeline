# Video Assembly

*Part of the [pipeline docs](../pipeline_automation.md). Assembly is fully local and AI-free: `video_assembler.py` (ffmpeg/moviepy).*

## Running the Assembler

```bash
cd "/Users/mritunjaymohitesh/dev/yt video ideas"

python video_assembler.py \
  --storyboard ./projects/001_roman_aqueducts/storyboard.json \
  --output ./projects/001_roman_aqueducts/output/final_video.mp4
```

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
8. Exports as 1080p h264 MP4

## Motion Types

| Motion | Effect | Best for |
|:---|:---|:---|
| `zoom_in` | Slow zoom into center | Establishing shots, wide views |
| `zoom_out` | Start tight, pull back | Reveals, "big picture" moments |
| `pan_left` | Slide right → left | Timelines, sequences |
| `pan_right` | Slide left → right | Following a path, flow |
| `pan_up` | Slide bottom → top | Tall structures, vertical reveals |
| `zoom_detail` | Zoom into specific point (x, y) | Callouts, mechanism close-ups |

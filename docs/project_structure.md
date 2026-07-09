# Project Folder Structure

*Part of the [pipeline docs](../pipeline_automation.md). Each video is a self-contained project folder.*

```
yt video ideas/
├── video_assembler.py          ← the assembly script
├── style_card.txt              ← master prompt prefix (see strategy doc)
├── example_storyboard.json     ← template
│
├── projects/
│   ├── 001_roman_aqueducts/
│   │   ├── storyboard.json     ← scene list + metadata (~54 scenes)
│   │   ├── script.md           ← full narration script
│   │   ├── references/         ← REAL photos/plans of the actual structure (Wikimedia etc.)
│   │   │   ├── visual_facts.md ← verifiable visual claims (geometry, materials, orientation)
│   │   │   ├── ref_01.jpg
│   │   │   └── ...
│   │   ├── images/             ← AI-generated stills (~55 images)
│   │   │   ├── scene_01.png
│   │   │   └── ...
│   │   ├── images_4k/          ← upscaled versions (static scenes only)
│   │   │   └── ...
│   │   ├── clips/              ← AI-animated clips (~27 clips)
│   │   │   ├── scene_01_animated.mp4
│   │   │   └── ...
│   │   ├── particles/          ← particle overlay videos
│   │   │   ├── dust_overlay.mp4
│   │   │   └── sparks_overlay.mp4
│   │   ├── audio/
│   │   │   ├── voiceover.mp3
│   │   │   └── ambient.mp3
│   │   ├── output/
│   │   │   ├── final_video.mp4
│   │   │   ├── thumb_a.png     ← 3 thumbnail candidates for Test & Compare
│   │   │   ├── thumb_b.png
│   │   │   └── thumb_c.png
│   │   └── metadata.json       ← title, description, tags for upload
│   │
│   ├── 002_mohenjo_daro/
│   │   └── ...
│   └── ...
│
└── assets/
    ├── style_anchors/           ← 8-10 reference images defining visual brand
    ├── music/                   ← ambient background tracks (royalty-free)
    ├── particles/               ← reusable particle overlay clips
    ├── fonts/                   ← custom fonts for text overlays
    └── thumbnails_log.md        ← per-video thumbnail concepts, A/B winners, CTR at 7/28 days
```

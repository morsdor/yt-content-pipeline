#!/usr/bin/env python3
"""
video_assembler.py — Automated Ken Burns + Text Overlay Video Assembly

Takes a storyboard.json + images + voiceover audio → produces a finished video.

Dependencies:
    pip install moviepy pillow

Also requires:
    - ffmpeg installed (brew install ffmpeg)
    - ImageMagick installed for text rendering (brew install imagemagick)

Usage:
    python video_assembler.py --storyboard storyboard.json --output final_video.mp4
"""

import json
import argparse
import os
from moviepy.editor import (
    ImageClip, TextClip, CompositeVideoClip, 
    concatenate_videoclips, AudioFileClip, 
    ColorClip, vfx, VideoFileClip
)
import numpy as np


# ── Style Constants ──────────────────────────────────────────────────────────

RESOLUTION = (1920, 1080)
FPS = 30
FONT = "Arial-Bold"          # change to your preferred font
FONT_SIZE = 42
FONT_COLOR = "white"
TEXT_BG_COLOR = (0, 0, 0)    # black background for text
TEXT_BG_OPACITY = 0.6
CROSSFADE_DURATION = 0.5     # seconds of crossfade between scenes


# ── Motion Functions ─────────────────────────────────────────────────────────
# Each function returns a transform(get_frame, t) for moviepy's .fl() method

def motion_zoom_in(duration, intensity=0.15):
    """Slow zoom into center of image."""
    def transform(get_frame, t):
        frame = get_frame(t)
        h, w = frame.shape[:2]
        zoom = 1 + intensity * (t / duration)
        new_w, new_h = int(w / zoom), int(h / zoom)
        x1 = (w - new_w) // 2
        y1 = (h - new_h) // 2
        cropped = frame[y1:y1+new_h, x1:x1+new_w]
        from PIL import Image
        img = Image.fromarray(cropped).resize((w, h), Image.LANCZOS)
        return np.array(img)
    return transform


def motion_zoom_out(duration, intensity=0.15):
    """Start zoomed in, slowly pull out."""
    def transform(get_frame, t):
        frame = get_frame(t)
        h, w = frame.shape[:2]
        zoom = 1 + intensity * (1 - t / duration)
        new_w, new_h = int(w / zoom), int(h / zoom)
        x1 = (w - new_w) // 2
        y1 = (h - new_h) // 2
        cropped = frame[y1:y1+new_h, x1:x1+new_w]
        from PIL import Image
        img = Image.fromarray(cropped).resize((w, h), Image.LANCZOS)
        return np.array(img)
    return transform


def motion_pan_left(duration, pan_fraction=0.15):
    """Pan from right to left across image."""
    def transform(get_frame, t):
        frame = get_frame(t)
        h, w = frame.shape[:2]
        crop_w = int(w * (1 - pan_fraction))
        max_x = w - crop_w
        x1 = int(max_x * (1 - t / duration))
        cropped = frame[:, x1:x1+crop_w]
        from PIL import Image
        img = Image.fromarray(cropped).resize((w, h), Image.LANCZOS)
        return np.array(img)
    return transform


def motion_pan_right(duration, pan_fraction=0.15):
    """Pan from left to right across image."""
    def transform(get_frame, t):
        frame = get_frame(t)
        h, w = frame.shape[:2]
        crop_w = int(w * (1 - pan_fraction))
        max_x = w - crop_w
        x1 = int(max_x * (t / duration))
        cropped = frame[:, x1:x1+crop_w]
        from PIL import Image
        img = Image.fromarray(cropped).resize((w, h), Image.LANCZOS)
        return np.array(img)
    return transform


def motion_pan_up(duration, pan_fraction=0.12):
    """Pan from bottom to top."""
    def transform(get_frame, t):
        frame = get_frame(t)
        h, w = frame.shape[:2]
        crop_h = int(h * (1 - pan_fraction))
        max_y = h - crop_h
        y1 = int(max_y * (1 - t / duration))
        cropped = frame[y1:y1+crop_h, :]
        from PIL import Image
        img = Image.fromarray(cropped).resize((w, h), Image.LANCZOS)
        return np.array(img)
    return transform


def motion_zoom_detail(duration, focus_x=0.5, focus_y=0.4, start_zoom=1.0, end_zoom=1.8):
    """Zoom into a specific region of the image."""
    def transform(get_frame, t):
        frame = get_frame(t)
        h, w = frame.shape[:2]
        zoom = start_zoom + (end_zoom - start_zoom) * (t / duration)
        new_w, new_h = int(w / zoom), int(h / zoom)
        cx, cy = int(w * focus_x), int(h * focus_y)
        x1 = max(0, min(cx - new_w // 2, w - new_w))
        y1 = max(0, min(cy - new_h // 2, h - new_h))
        cropped = frame[y1:y1+new_h, x1:x1+new_w]
        from PIL import Image
        img = Image.fromarray(cropped).resize((w, h), Image.LANCZOS)
        return np.array(img)
    return transform


# ── Motion Registry ──────────────────────────────────────────────────────────

MOTIONS = {
    "zoom_in":     motion_zoom_in,
    "zoom_out":    motion_zoom_out,
    "pan_left":    motion_pan_left,
    "pan_right":   motion_pan_right,
    "pan_up":      motion_pan_up,
    "zoom_detail": motion_zoom_detail,
}

DEFAULT_MOTION_CYCLE = ["zoom_in", "pan_right", "zoom_out", "pan_left", "pan_up", "zoom_in"]


# ── Scene Builder ────────────────────────────────────────────────────────────

def build_scene(scene: dict, index: int, base_dir: str) -> CompositeVideoClip:
    """Build a single scene clip from a storyboard entry."""
    
    scene_type = scene.get("type", "static")
    duration = scene.get("duration", 10)
    
    # 1. Load base clip (Video for animated, Image for static)
    if scene_type == "animated" and "animated_clip" in scene:
        clip_path = os.path.join(base_dir, scene["animated_clip"])
        base_clip = VideoFileClip(clip_path).resize(RESOLUTION)
        # Handle cases where the clip is shorter than requested duration
        if base_clip.duration < duration:
            base_clip = base_clip.fx(vfx.loop, duration=duration)
        else:
            base_clip = base_clip.subclip(0, duration)
    else:
        image_path = os.path.join(base_dir, scene["image"])
        motion_type = scene.get("motion", DEFAULT_MOTION_CYCLE[index % len(DEFAULT_MOTION_CYCLE)])
        
        img_clip = (
            ImageClip(image_path)
            .set_duration(duration)
            .resize(height=RESOLUTION[1] + 200)
        )
        if img_clip.w < RESOLUTION[0] + 200:
            img_clip = img_clip.resize(width=RESOLUTION[0] + 200)
        
        # 2. Apply Ken Burns motion
        motion_kwargs = {}
        if motion_type == "zoom_detail":
            motion_kwargs = {
                "focus_x": scene.get("focus_x", 0.5),
                "focus_y": scene.get("focus_y", 0.4),
            }
        
        motion_fn = MOTIONS.get(motion_type, motion_zoom_in)
        base_clip = img_clip.fl(motion_fn(duration, **motion_kwargs), apply_to="mask")
        base_clip = base_clip.resize(RESOLUTION)
    
    # 3. Build layers
    layers = [base_clip]
    
    # Support both old single `text` and new `texts` array formats
    texts = scene.get("texts", [])
    if not texts and scene.get("text"):
        texts = [{
            "text": scene.get("text"),
            "start": 0.5,
            "end": duration - 0.5,
            "position": scene.get("text_position", "bottom")
        }]
        
    for txt_info in texts:
        text_str = txt_info.get("text")
        if not text_str:
            continue
            
        t_start = txt_info.get("start", 0.5)
        t_end = txt_info.get("end", duration - 0.5)
        t_pos = txt_info.get("position", "bottom")
        t_dur = t_end - t_start
        
        if t_dur <= 0:
            continue

        txt_clip = (
            TextClip(
                text_str, fontsize=FONT_SIZE, color=FONT_COLOR, font=FONT,
                size=(RESOLUTION[0] - 200, None), method="caption", align="center",
            )
            .set_duration(t_dur)
            .set_start(t_start)
            .crossfadein(0.3)
            .crossfadeout(0.3)
        )
        
        if t_pos == "bottom":
            txt_clip = txt_clip.set_position(("center", RESOLUTION[1] - 120))
        elif t_pos == "top":
            txt_clip = txt_clip.set_position(("center", 40))
        elif t_pos == "center":
            txt_clip = txt_clip.set_position("center")
        
        txt_bg = (
            ColorClip(size=(RESOLUTION[0], txt_clip.h + 30), color=TEXT_BG_COLOR)
            .set_opacity(TEXT_BG_OPACITY)
            .set_duration(t_dur)
            .set_start(t_start)
            .set_position(("center", txt_clip.pos(0)[1] - 15))
            .crossfadein(0.3)
            .crossfadeout(0.3)
        )
        layers.extend([txt_bg, txt_clip])
    
    return CompositeVideoClip(layers, size=RESOLUTION).set_duration(duration)


# ── Main Assembly ────────────────────────────────────────────────────────────

def assemble_video(storyboard_path: str, output_path: str):
    """Assemble a full video from a storyboard JSON file."""
    
    with open(storyboard_path, "r") as f:
        storyboard = json.load(f)
    
    base_dir = storyboard.get("base_dir", os.path.dirname(storyboard_path))
    scenes = storyboard["scenes"]
    voiceover_path = storyboard.get("voiceover", None)
    music_path = storyboard.get("background_music", None)
    music_volume = storyboard.get("music_volume", 0.08)
    
    print(f"Loaded storyboard: {len(scenes)} scenes")
    
    clips = []
    for i, scene in enumerate(scenes):
        print(f"  Building scene {i+1}/{len(scenes)}: {scene.get('text', 'no text')[:50]}...")
        clip = build_scene(scene, i, base_dir)
        clips.append(clip)
    
    print("Concatenating scenes...")
    if CROSSFADE_DURATION > 0 and len(clips) > 1:
        final = concatenate_videoclips(clips, method="compose", padding=-CROSSFADE_DURATION)
    else:
        final = concatenate_videoclips(clips, method="compose")
    
    if voiceover_path and os.path.exists(os.path.join(base_dir, voiceover_path)):
        print("Adding voiceover...")
        voice = AudioFileClip(os.path.join(base_dir, voiceover_path))
        final = final.set_audio(voice.set_duration(final.duration))
    
    if music_path and os.path.exists(os.path.join(base_dir, music_path)):
        print("Mixing background music...")
        music = (
            AudioFileClip(os.path.join(base_dir, music_path))
            .volumex(music_volume)
            .set_duration(final.duration)
        )
        if final.audio:
            from moviepy.audio.AudioClip import CompositeAudioClip
            final = final.set_audio(CompositeAudioClip([final.audio, music]))
        else:
            final = final.set_audio(music)
    
    print(f"Rendering to {output_path}...")
    final.write_videofile(
        output_path, fps=FPS, codec="libx264", audio_codec="aac",
        bitrate="8000k", preset="medium", threads=4,
    )
    print(f"Done! Output: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assemble video from storyboard JSON")
    parser.add_argument("--storyboard", required=True, help="Path to storyboard.json")
    parser.add_argument("--output", default="output.mp4", help="Output video path")
    args = parser.parse_args()
    assemble_video(args.storyboard, args.output)

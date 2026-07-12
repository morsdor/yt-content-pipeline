# 4K Upscaling (local, free)

*Part of the [pipeline docs](../pipeline_automation.md). Stage D of the [asset-generation](../asset-generation/SKILL.md) flow.*

We generate Kling clips at **720p** (6 cr/s — the cheapest good rate) and stills at model resolution, then upscale to **4K locally with Real-ESRGAN** for free. On flat isometric line art the result ~matches native 1080p/4K, so paying Kling credits for higher native resolution buys little. Uploading 4K to YouTube is worth it regardless of source res — YouTube allocates 4K uploads more bitrate, so even 1080p playback looks cleaner.

**Model:** `realesr-animevideov3` — Real-ESRGAN's temporally-stable *video* model for anime/illustration. Ideal for our clean-line isometric style (far better than photographic upscalers here, and it reduces frame-to-frame flicker). For stills, `realesrgan-x4plus-anime`.

---

## One-time install (macOS / arm64)

The binary + weights live in `tools/realesrgan/` (git-ignored, ~76 MB, re-downloadable).

> **⚠️ The gotcha that cost an hour — get the models from the RIGHT release.**
> There are two upstream repos, and the obvious one ships a **binary with no model weights**:
> - ❌ `xinntao/Real-ESRGAN-ncnn-vulkan` releases (the "-ncnn-vulkan" fork): the v0.2.0 macOS zip is **~8 MB, binary only — no `models/` folder.** The binary runs (`-h` works) but has nothing to upscale with. The repo has no `models/` dir and the weights are **not** at `raw.githubusercontent.com/.../models/*.param` (that path 404s → 14-byte "Not Found" files).
> - ✅ **`xinntao/Real-ESRGAN` (the MAIN repo) releases, tag `v0.2.5.0`:** `realesrgan-ncnn-vulkan-20220424-macos.zip` is **~50 MB and INCLUDES `models/`** (realesr-animevideov3 x2/x3/x4, realesrgan-x4plus, realesrgan-x4plus-anime). This is the one to download.

```bash
mkdir -p tools/realesrgan && cd tools/realesrgan
curl -sL -o full.zip \
  "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-macos.zip"
unzip -oq full.zip && rm full.zip
xattr -cr .                         # clear Gatekeeper quarantine (unsigned binary)
chmod +x realesrgan-ncnn-vulkan
ls models/                          # expect the .param/.bin pairs
```

**Runtime notes (Apple Silicon):** the 2022 binary is x86_64 and runs under **Rosetta 2 on CPU** — Vulkan/Metal isn't exposed, so it's CPU-bound at **~0.6 s/frame** in directory mode (model loads once; the per-image `-h` test is slower because it re-pays model load). A 7 s clip ≈ 170 frames ≈ ~110 s. Fine as a background/overnight pass; not real-time.

---

## Usage

**Video** — `upscale_video.py` (repo root) does extract-frames → AI-upscale → re-encode, silent, source fps preserved:

```bash
python upscale_video.py projects/NNN/clips/scene_NN_animated.mp4 \
                        projects/NNN/clips_4k/scene_NN_4k.mp4
# defaults: --scale 3  --target 3840x2160  --model realesr-animevideov3  --crf 16
```

- `--scale {2,3,4}` — AI factor. 720p × 3 = exactly ~4K; × 4 then downscale is sharper but heavier.
- `--target 3840x2160` — final lanczos fit (or `none` to keep the raw ×N size).
- `--crf` — x264 quality (14–18 sensible; lower = larger/better).

**Stills** — call the binary directly with the anime model:

```bash
tools/realesrgan/realesrgan-ncnn-vulkan -i in.png -o out_4k.png \
  -n realesrgan-x4plus-anime -s 4 -m tools/realesrgan/models
```

---

## Resolution hybrid: flicker on dense geometry

720p→4K ~matches native 1080p/4K on *smooth* content — but **breaks on dense repeating geometry in motion** (the step-lattice). Measured on Chand Baori (`v3_0`, `flicker_HF` = fine-detail shimmer, intended motion filtered out):

| Variant (lattice scene 31) | flicker_HF |
|:--|:--:|
| 1080p native | 7.8 (smoothest) |
| 1080p→4K | 9.1 |
| 720p native | 9.9 |
| **720p→4K** | **11.6 (worst)** |

Two compounding effects: Kling's **720p generation** flickers ~25% more than 1080p on dense lattice (smooth scenes show *no* difference), and the **per-frame 4K upscale adds a further ~17%** — structural aliasing (fine lines reconstructed slightly differently each frame), **not filterable**: `hqdn3d` and `atadenoise` temporal denoise both moved it <0.3%.

**The rule (data-driven hybrid — measure, don't guess):**
1. Generate everything at **720p** (6 cr/s).
2. `python flicker_check.py projects/NNN/clips/*.mp4` — smooth scenes score ~0.3–1.0, dense-lattice-in-motion ~8–10, **nothing lands between** (threshold 3.0 separates cleanly).
3. **Re-generate only the flagged (>3) scenes at 1080p** (8 cr/s). Don't pre-classify by scene type — a "lattice" establishing shot can be perfectly smooth (scene 5 was; scene 31 wasn't).
4. Upscale all to 4K.

Typically ~⅓ of animated scenes cross the line → ~1,440 cr/video, still ~2 videos/mo. Kling's native 4K (VIP) stays not-worth-it. See [costs.md](costs.md) for the full credit math.

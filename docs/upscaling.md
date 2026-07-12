# 4K Upscaling (local, free)

*Part of the [pipeline docs](../pipeline_automation.md). Stage C.4 of the
[asset-generation](../asset-generation/SKILL.md) flow.*

Stills are generated at model resolution (~1–2K) and upscaled to **4K locally with
Real-ESRGAN** for free. Every accepted still gets this pass, because both downstream
consumers want the headroom:

- **AE comps are 3840×2160** — a scene still is the comp's base plate, and camera
  push-ins crop into it; low-res plates go soft exactly when the shot gets interesting.
  (`generate_asset.py` runs the same upscale automatically inside the library-asset pipeline.)
- **The assembler's Ken Burns** zooms crop into static-scene images the same way.

AE renders come out at native 4K, so **no video upscaling is needed in the pipeline**.
(`upscale_video.py` still exists for one-off legacy 720p clips; it's not a pipeline stage.)

**Model:** `realesrgan-x4plus-anime` — ideal for clean-line flat illustration (far better
than photographic upscalers here).

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

**Runtime notes (Apple Silicon):** the 2022 binary is x86_64 and runs under **Rosetta 2 on
CPU** — Vulkan/Metal isn't exposed, so it's CPU-bound. Directory mode amortizes the model
load; a full video's stills are a coffee-break batch, not an overnight job.

---

## Usage

**Single still:**

```bash
tools/realesrgan/realesrgan-ncnn-vulkan -i in.png -o out_4k.png \
  -n realesrgan-x4plus-anime -s 4 -m tools/realesrgan/models
```

**A whole video's stills (directory mode — model loads once):**

```bash
mkdir -p projects/NNN/images_4k
tools/realesrgan/realesrgan-ncnn-vulkan \
  -i projects/NNN/images -o projects/NNN/images_4k \
  -n realesrgan-x4plus-anime -s 4 -m tools/realesrgan/models
```

Transparent PNGs (library assets) pass through with alpha preserved — but prefer
`generate_asset.py`, which sequences upscale → key → edge-bleed correctly on its own.

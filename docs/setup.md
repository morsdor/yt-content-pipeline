# One-Time Setup

*Part of the [pipeline docs](../pipeline_automation.md). Do this once, before video #1.*

## Prerequisites

```bash
# Core tools
brew install ffmpeg imagemagick
pip install moviepy pillow numpy google-genai rembg

# Node.js (for MCP servers)
brew install node
```

**After Effects (the animation stage):**
1. Adobe Creative Cloud → After Effects **Single App** plan (~₹2,000/mo). Free alternative
   while trialing: DaVinci Resolve (Fusion page) — concepts transfer 1:1.
2. Install **Duik Ángela** (free, rainboxlab.org) — character rigging for later.
3. Build `template.aep` per [after_effects_workflow.md](after_effects_workflow.md) Phase 0:
   3840×2160 @ 30fps comp, folder bins, grain adjustment layer, vignette.
4. Seed the asset library: `assets_library/STYLE_BIBLE.md` + the first batch
   (`python generate_asset.py --batch assets_library/_batches/batch_01.json`).
5. Comp-builder scripts live in `ae_scripts/` — run via AE `File → Scripts → Run Script File…`.

**Real-ESRGAN (4K still upscaling):** vendored in `tools/realesrgan/` — install per
[upscaling.md](upscaling.md) (mind the model-bundle gotcha documented there).

## API Keys

| Service | Where to get it | Cost |
|:---|:---|:---|
| **Google AI Studio** | [aistudio.google.com](https://aistudio.google.com) → "Get API key" | **Paid tier required for image models** (no free tier — see [costs.md](costs.md)) |
| **ElevenLabs** (optional) | [elevenlabs.io](https://elevenlabs.io) → Settings → API Key | Free tier fine (pickups only) |
| **Anthropic** (optional, for headless scripting) | [console.anthropic.com](https://console.anthropic.com) | Pay-per-use |

> [!IMPORTANT]
> Your Google AI Plus subscription does NOT provide API access. The API key comes from
> Google AI Studio, which is separate — and the key's project needs billing enabled for
> image generation. Your Claude Pro subscription gives you Claude Desktop with MCP
> support — that's the orchestrator.

Put the Gemini key in `.env` at the repo root (`GEMINI_API_KEY=...`) — it's git-ignored.

## Claude Desktop MCP Configuration

**File:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "gemini-image": {
      "command": "npx",
      "args": ["-y", "@anthropic/gemini-mcp-server"],
      "env": {
        "GOOGLE_API_KEY": "AIza..."
      }
    },
    "elevenlabs-voice": {
      "command": "npx",
      "args": ["-y", "elevenlabs-mcp-server"],
      "env": {
        "ELEVENLABS_API_KEY": "sk_..."
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/mritunjaymohitesh/dev/yt video ideas"
      ]
    }
  }
}
```

After editing, restart Claude Desktop. The tools will appear in your "Search and Tools" menu.

## Voice Clone Setup (One-Time, optional)

1. Go to ElevenLabs → Voices → "Add Voice" → "Instant Voice Cloning"
2. Record a 30–60 second sample of yourself reading narration (calm, measured, ~140 wpm)
3. Upload and name it (e.g., "Channel Narrator")
4. Note the `voice_id` — pickups only; you record the actual narration yourself

## File Reference

| File | Purpose |
|:---|:---|
| `video_assembler.py` | The **animatic**: stills + VO rough cut for pacing checks before AE (the publish master is conformed in **Premiere Pro**) |
| `prompt_builder.py` | Composes plate prompts from the board; renders `shot_list.md` (`--shot-list`) and `prompts.md`; validates between studio passes (`--validate`) |
| `generate_images.py` | Plate generation via Gemini (style anchor + geometry reference; skips `assembly` scenes) |
| `generate_asset.py` | Library-asset generation → transparent PNGs into `assets_library/` (STYLE_BIBLE rules) |
| `review_images.py` | Builds the accuracy-gate review artifacts (contact sheets, render-vs-reference pairs) |
| `ae_scripts/*.jsx` | AE comp builders — run via `File → Scripts → Run Script File…` |
| `style_card.txt` | Master prompt prefix for scene stills (single brand source) |
| `assets_library/STYLE_BIBLE.md` | Asset-generation rules (palette, views, character language, cutout pipeline) |
| `example_storyboard.json` | Template storyboard |

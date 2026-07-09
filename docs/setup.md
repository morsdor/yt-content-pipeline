# One-Time Setup

*Part of the [pipeline docs](../pipeline_automation.md). Do this once, before video #1.*

## Prerequisites

```bash
# Core tools
brew install ffmpeg imagemagick
pip install moviepy pillow numpy

# Node.js (for MCP servers)
brew install node
```

## API Keys

| Service | Where to get it | Cost |
|:---|:---|:---|
| **Google AI Studio** | [aistudio.google.com](https://aistudio.google.com) → "Get API key" | Free tier (generous daily limits) |
| **ElevenLabs** | [elevenlabs.io](https://elevenlabs.io) → Settings → API Key | Starter plan ~$5/month |
| **Anthropic** (optional, for headless scripting) | [console.anthropic.com](https://console.anthropic.com) | $5 free credit, then pay-per-use |

> [!IMPORTANT]
> Your Google AI Plus subscription (₹400/mo) does NOT provide API access. The API key comes from Google AI Studio, which is free and completely separate. Your Claude Pro subscription (₹2,000/mo) gives you Claude Desktop with MCP support — that's the part you use.

## Claude Desktop MCP Configuration

**File:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mcp-kling": {
      "command": "npx",
      "args": ["-y", "mcp-kling@latest"],
      "env": {
        "KLING_ACCESS_KEY": "YOUR_ACCESS_KEY_HERE",
        "KLING_SECRET_KEY": "YOUR_SECRET_KEY_HERE"
      }
    },
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

## Voice Clone Setup (One-Time)

1. Go to ElevenLabs → Voices → "Add Voice" → "Instant Voice Cloning"
2. Record a 30–60 second sample of yourself reading narration (calm, measured, ~140 wpm)
3. Upload and name it (e.g., "Channel Narrator")
4. Note the `voice_id` — this goes into your pipeline config

## File Reference

| File | Purpose |
|:---|:---|
| `video_assembler.py` | Final assembly: Ken Burns, text overlays, audio mix → MP4 |
| `prompt_builder.py` | Composes full image/animation prompts from the lean storyboard (also emits `prompts.md` / `anim_jobs.json`) |
| `generate_images.py` | Still-image generation via Gemini (style anchor + geometry reference) |
| `style_card.txt` | Master prompt prefix (single brand source) |
| `example_storyboard.json` | Template storyboard |

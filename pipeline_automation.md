# Video Pipeline — Hub

> **This is the index.** The pipeline reference now lives in focused files under `docs/`, and the two agent-executed procedures are skills. Start here, follow the links.

---

## Operating assumptions (the decisions that shape everything)

**Revised July 6, 2026** (see `strategy_review.md`):
- **Cadence: 2 videos/month**, not 8 — no self-hosted video model needed at this volume (revisit only at 30+ videos/month full-time).
- **Narration is your own recorded voice** from day 1; the AI clone is a pickup-only fallback.
- **Two mandatory human steps:** a real fact-check pass, and the "Altered content" disclosure on upload — these keep the channel monetizable under YouTube's 2026 inauthentic-content policy.
- **Graceful degradation:** any failed animation falls back to Ken Burns + text overlay (pure ffmpeg). You always ship.

**Corrected July 10, 2026** (second review):
- **Visual accuracy is a gated step:** per-project `references/` pack + `visual_facts`, injected into prompts; **no still goes to Kling unvalidated** → [`visual-accuracy-gate` skill](visual-accuracy-gate/SKILL.md).
- **Kling budget corrected ~2×:** Pro tier needed (~₹2,050–3,100/mo); all-in **~₹5,000–7,000/mo** → [docs/costs.md](docs/costs.md).
- **Time per video: ~8–12 hrs** (16–24 hrs/month), not 5–7 → [docs/production_workflow.md](docs/production_workflow.md).
- **Thumbnails are a first-class session** (packaging-first gate, 3 candidates, Test & Compare) → Session 5b in the workflow.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                               │
│              Claude Desktop (Pro plan)                        │
│                                                               │
│  You type a topic. Claude handles everything via MCP tools:   │
│                                                               │
│  Step 1: Claude drafts script from YOUR fact-checked notes    │
│  Step 2: Generate ~55 still images via Gemini MCP             │
│         └─ VISUAL ACCURACY GATE (hard gate — skill)           │
│  Step 3: Animate ~27 validated stills via Kling MCP           │
│         └─ scrub-check → 1 retry → Ken Burns fallback         │
│  Step 4: YOU record narration (AI clone = pickup fallback)    │
│  Step 5: Output assembler commands                            │
│                                                               │
│  Connected MCP Servers:                                       │
│  ┌────────────────────┐ ┌─────────────────┐ ┌──────────────┐│
│  │ 🎨 Gemini Image   │ │ 🎙️ ElevenLabs  │ │ 📂 Filesystem ││
│  │ (Nano Banana)      │ │ (Voice Clone)   │ │              ││
│  │                    │ │                 │ │              ││
│  │ generate_image()   │ │ text_to_speech()│ │ read/write   ││
│  └────────────────────┘ └─────────────────┘ └──────────────┘│
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    ANIMATION (50% of scenes)                  │
│              Kling AI (via the Kling MCP)                     │
│                                                               │
│  For ~27 "animate" scenes:                                   │
│  Validated still → parallax/element motion → 6–10s clip      │
│  Download animated clips to clips/ folder                     │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    ASSEMBLY                                   │
│              video_assembler.py (local)                       │
│                                                               │
│  Static scenes: Ken Burns + text overlays                    │
│  Animated scenes: import clips + text overlays               │
│  Particle overlays composited on ~10 scenes                  │
│  Voiceover + ambient music mixed                             │
│  Crossfade transitions → final_video.mp4                     │
└──────────────────────────────────────────────────────────────┘
```

---

## The docs

| Doc | What's in it | Read it when |
|:---|:---|:---|
| [docs/setup.md](docs/setup.md) | Prerequisites, API keys, MCP config, voice-clone setup, file reference | Once, before video #1 |
| [docs/project_structure.md](docs/project_structure.md) | The per-video folder layout (`references/`, `images/`, `clips/`, `output/`…) | Starting a new project folder |
| [docs/storyboard_schema.md](docs/storyboard_schema.md) | The storyboard JSON contract + full field reference (`visual_facts`, `reference_image`, …) | Writing or reviewing a storyboard |
| [docs/image_generation.md](docs/image_generation.md) | Prompt structure, resolution/upscaling, style-consistency tiers (prefix → anchors → LoRA) | Generating stills; style drift problems |
| [docs/video_assembly.md](docs/video_assembly.md) | Running `video_assembler.py`, what it does, Ken Burns motion types | Assembling; adding motion to static scenes |
| [docs/upscaling.md](docs/upscaling.md) | 4K upscaling via Real-ESRGAN (`upscale_video.py`), install + the model-bundle gotcha | Stage D — upscaling stills/clips to 4K |
| [docs/voice_narration.md](docs/voice_narration.md) | Self-recording workflow, ElevenLabs pickup fallback + settings | Recording narration |
| [docs/costs.md](docs/costs.md) | Per-video + monthly budget (corrected), cost levers | Budget questions; plan sizing |
| [docs/production_workflow.md](docs/production_workflow.md) | Sessions 0–6: research → storyboard → images → animation → voice → assembly → thumbnails → publish | The month-to-month operating rhythm |

## The skills (agent-executed procedures)

| Skill | What it does | Invoked when |
|:---|:---|:---|
| [`the-engineering-atlas-video`](the-engineering-atlas-video/SKILL.md) | The full per-video production checklist with human gates | "Start a new video…" (see `new_video_prompt_template.md`) |
| [`asset-generation`](asset-generation/SKILL.md) | Phases 2+3 end-to-end: `generate_images.py` stills → accuracy gate → Kling MCP animation (`file_upload` → `image_to_video` → `query_tasks`), with credits preflight, cost confirmation, scrub-check, one-retry, Ken Burns fallback | After storyboard approval — "generate the assets" |
| [`visual-accuracy-gate`](visual-accuracy-gate/SKILL.md) | Validates renders against real reference photos + `visual_facts`; delta-prompt fixes; clip scrub-check; enforces "no unvalidated still goes to Kling" | Between image generation and animation (mandatory), and after clip delivery |
| [`thumbnail-workflow`](thumbnail-workflow/SKILL.md) | Packaging-first gate → 3 candidates (one axis varied) → 120-px squint test → local typography → Test & Compare → `thumbnails_log.md` | At storyboard approval (gate), and Session 5b (production) |

> **Skills work in both environments:** claude.ai co-work picks them up from these root-level folders when the project folder is connected; Claude Code discovers the same skills via symlinks in `.claude/skills/`. One source of truth, two runtimes.

---

## The one-paragraph version

Research and fact-check yourself (Session 0, incl. the reference pack) → lean storyboard with `visual_facts` + a packaging-first thumbnail gate → `generate_images.py` makes ~55 stills (style anchor = look, reference photo = geometry) → **accuracy gate: no still to Kling unvalidated** → Kling animates ~27 validated stills (`v3_0` 720p no-audio = 6 cr/s, 6s bias, scrub-check, 1 retry, Ken Burns fallback) → **4K upscale locally (free)** → record your own narration → `video_assembler.py` → 3 thumbnails + Test & Compare → full watch, "Altered content" disclosure, publish. **~₹450 marginal cash + ~8–12 hrs per video; ~₹5–6K/month all-in (Claude + Kling Pro + images) at 2 videos/month.**

---

*Last updated: July 10, 2026 — restructured into a hub + `docs/` reference files + the `visual-accuracy-gate` skill. Content revisions: July 10 (visual accuracy, thumbnails, corrected Kling budget + hours), July 6 (2/month cadence, self-narration, fact-check + disclosure gates — see `strategy_review.md`).*

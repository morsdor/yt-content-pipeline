# Video Pipeline — Hub

> **This is the index.** The pipeline reference lives in focused files under `docs/`, and the agent-executed procedures are skills. Start here, follow the links.

---

## Operating assumptions (the decisions that shape everything)

**Revised July 12, 2026 — the animation pivot:**
- **Motion is hand-built in After Effects from AI stills.** Generative image-to-video was dropped after measurement: it softens crisp lines, warps precise geometry, and adds uninvited camera moves on our flat isometric style (~70% of a full batch failed the quality bar). AE transforms the art but never redraws it — sharp by construction. → [docs/after_effects_workflow.md](docs/after_effects_workflow.md)
- **A reusable cross-video asset library** (`assets_library/` — characters, nature, architecture, military, props, diagram elements) feeds AE. AI generates the assets; `STYLE_BIBLE.md` locks the look; `INDEX.md` tracks what exists so nothing is generated twice. Assets compound: video 1 needs ~40, video 10 needs ~5.
- **AI's three levers in AE:** (1) generating assets, (2) writing per-scene motion briefs + keyframe recipes, (3) writing AE expressions and JSX scripts (`ae_scripts/`) that build comps programmatically.
- **Animation is now free at the margin** — no per-clip credits, no charged retries. The budget shifted from credits to *your AE time*, controlled by templates and the three-rung ladder (camera moves → parallax → element motion).

**Revised July 6, 2026** (see `strategy_review.md`):
- **Cadence: 2 videos/month**, not 8 — quality over volume, sustainable alongside a full-time job.
- **Narration is your own recorded voice** from day 1; the AI clone is a pickup-only fallback.
- **Two mandatory human steps:** a real fact-check pass, and the "Altered content" disclosure on upload — these keep the channel monetizable under YouTube's 2026 inauthentic-content policy.
- **Graceful degradation:** any scene not worth AE time falls back to Ken Burns + text overlay (pure ffmpeg). You always ship.

**Corrected July 10, 2026** (second review):
- **Visual accuracy is a gated step:** per-project `references/` pack + `visual_facts`, injected into prompts; **no still is animated unvalidated** → [`visual-accuracy-gate` skill](visual-accuracy-gate/SKILL.md).
- **Time per video: ~8–12 hrs** (16–24 hrs/month) → [docs/production_workflow.md](docs/production_workflow.md).
- **Thumbnails are a first-class session** (packaging-first gate, 3 candidates, Test & Compare) → Session 5b in the workflow.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                               │
│              Claude (Desktop / Code)                          │
│                                                               │
│  You type a topic. Claude drives everything scriptable:       │
│                                                               │
│  Step 1: Claude drafts script from YOUR fact-checked notes    │
│  Step 2: Generate ~55 still images via Gemini                 │
│         └─ VISUAL ACCURACY GATE (hard gate — skill)           │
│  Step 3: Prep animation — per-scene MOTION BRIEFS +           │
│         asset-library shopping list + JSX comp builders       │
│  Step 4: YOU record narration (AI clone = pickup fallback)    │
│  Step 5: Output assembler commands                            │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│              ANIMATION (~27 scenes) — AFTER EFFECTS           │
│                    (hand-built, by YOU)                       │
│                                                               │
│  Validated 4K still + assets_library/ elements                │
│    → build per the motion brief (camera / parallax / element  │
│      motion), JSX scripts do the repetitive setup             │
│    → transforms only, art never redrawn = always sharp        │
│    → render clips/scene_NN_animated.mp4 (native 4K)           │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    ASSEMBLY                                   │
│              video_assembler.py (local)                       │
│                                                               │
│  Static scenes: Ken Burns + text overlays                     │
│  Animated scenes: import AE clips + text overlays             │
│  Particle overlays composited on ~10 scenes                   │
│  Voiceover + ambient music mixed                              │
│  Crossfade transitions → final_video.mp4                      │
└──────────────────────────────────────────────────────────────┘
```

---

## The docs

| Doc | What's in it | Read it when |
|:---|:---|:---|
| [docs/setup.md](docs/setup.md) | Prerequisites, API keys, After Effects + Duik install, file reference | Once, before video #1 |
| [docs/project_structure.md](docs/project_structure.md) | The per-video folder layout (`references/`, `images/`, `clips/`, `output/`…) | Starting a new project folder |
| [docs/storyboard_schema.md](docs/storyboard_schema.md) | The storyboard JSON contract + full field reference (`visual_facts`, `animation_prompt` = motion intent, …) | Writing or reviewing a storyboard |
| [docs/image_generation.md](docs/image_generation.md) | Prompt structure, resolution/upscaling, style-consistency tiers (prefix → anchors → LoRA) | Generating stills; style drift problems |
| [docs/after_effects_workflow.md](docs/after_effects_workflow.md) | **The animation stage**: asset library, motion briefs, the three-rung ladder, JSX/expressions, quality gates, learning curve | Building animated scenes; anything AE |
| [assets_library/STYLE_BIBLE.md](assets_library/STYLE_BIBLE.md) | Asset-generation rules: palette, view conventions, character design language, cutout pipeline | Generating library assets |
| [docs/video_assembly.md](docs/video_assembly.md) | Running `video_assembler.py`, what it does, Ken Burns motion types | Assembling; adding motion to static scenes |
| [docs/upscaling.md](docs/upscaling.md) | 4K still upscaling via Real-ESRGAN — install + the model-bundle gotcha | Upscaling stills for Ken Burns headroom / AE |
| [docs/voice_narration.md](docs/voice_narration.md) | Self-recording workflow, ElevenLabs pickup fallback + settings | Recording narration |
| [docs/costs.md](docs/costs.md) | Per-video + monthly budget, cost levers | Budget questions; plan sizing |
| [docs/production_workflow.md](docs/production_workflow.md) | Sessions 0–6: research → storyboard → images → animation → voice → assembly → thumbnails → publish | The month-to-month operating rhythm |

## The skills (agent-executed procedures)

| Skill | What it does | Invoked when |
|:---|:---|:---|
| [`the-engineering-atlas-video`](the-engineering-atlas-video/SKILL.md) | The full per-video production checklist with human gates | "Start a new video…" (see `new_video_prompt_template.md`) |
| [`asset-generation`](asset-generation/SKILL.md) | Phases 2+3 prep end-to-end: `generate_images.py` stills → accuracy gate → motion briefs + asset-library shopping list + JSX scaffolds → render QC when AE clips land | After storyboard approval — "generate the assets" |
| [`visual-accuracy-gate`](visual-accuracy-gate/SKILL.md) | Validates renders against real reference photos + `visual_facts`; delta-prompt fixes; motion-craft QC on AE renders; enforces "no unvalidated still is animated" | Between image generation and animation (mandatory), and after AE renders land |
| [`thumbnail-workflow`](thumbnail-workflow/SKILL.md) | Packaging-first gate → 3 candidates (one axis varied) → 120-px squint test → local typography → Test & Compare → `thumbnails_log.md` | At storyboard approval (gate), and Session 5b (production) |

> **Skills work in both environments:** claude.ai co-work picks them up from these root-level folders when the project folder is connected; Claude Code discovers the same skills via symlinks in `.claude/skills/`. One source of truth, two runtimes.

---

## The one-paragraph version

Research and fact-check yourself (Session 0, incl. the reference pack) → lean storyboard with `visual_facts` + a packaging-first thumbnail gate → `generate_images.py` makes ~55 stills (style anchor = look, reference photo = geometry) → **accuracy gate: no still is animated unvalidated** → upscale stills to 4K locally (free) → Claude writes **per-scene motion briefs** + generates any missing `assets_library/` elements → **you build the ~27 animated scenes in After Effects** (camera moves → parallax → element motion; JSX does the repetitive setup; transforms only, so the art stays sharp) → record your own narration → `video_assembler.py` (1080p review, `--resolution 2160p` publish master) → 3 thumbnails + Test & Compare → full watch, "Altered content" disclosure, publish. **~₹450 marginal cash + ~8–12 hrs per video; ~₹5,000/month all-in (Claude + After Effects + images) at 2 videos/month.**

---

*Last updated: July 12, 2026 — the animation pivot: generative image-to-video removed from the pipeline; animation is now hand-built in After Effects from AI stills + a reusable asset library. Previous revisions: July 10 (visual accuracy, thumbnails, corrected budget + hours), July 6 (2/month cadence, self-narration, fact-check + disclosure gates — see `strategy_review.md`).*

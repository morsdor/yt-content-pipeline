# Costs & Budget

*Part of the [pipeline docs](../pipeline_automation.md). Revised July 12, 2026 for the
animation pivot: generative image-to-video (credit-metered) is out; animation is hand-built
in After Effects (flat subscription, ₹0 marginal). The budget's shape changed — from
"credits per clip" to "images + your time."*

## Per-Video Cost Breakdown

| Component | Unit Cost | Quantity | Total |
|:---|:---|:---|:---|
| Script draft (Claude via Pro plan) | Included in sub | 1 | ₹0 |
| Images (Gemini 3.1 Flash Image / Nano Banana 2) | **~₹7.4/image (~$0.086)** — measured Jul 2026 | ~54 + ~10–15% gate regens | **~₹450** |
| New `assets_library/` elements | ~₹7.4/asset | video 1: ~40 · video 10: ~5 (library compounds) | **~₹50–300, falling** |
| Animation (After Effects, hand-built) | ₹0 marginal — sub is monthly, below | every scene (60–80) | ₹0 |
| Upscaling stills to 4K (Real-ESRGAN, local) | ₹0 | all scenes | ₹0 |
| Voice (self-recorded) | ₹0 | 1 | ₹0 |
| Particle overlays (stock) | ₹0 | ~10 | ₹0 |
| ffmpeg/moviepy assembly · royalty-free music | ₹0 | 1 | ₹0 |
| **Marginal cash per video** | | | **~₹500–750** |
| ⏱️ **Your time per video** (the real cost) | | **~10–14 hrs** | *research + fact-check + gate + the 3–5 hr AE session + narration + QA + thumbnails; falls toward 8–10 hrs as template comps and the asset library accumulate* |

> **Your time is the binding constraint, not cash — more than ever.** Animation used to be
> the biggest cash line and is now ₹0 marginal; what it costs instead is the AE session.
> Four levers keep that session short: **(1) the board** (every scene arrives with numeric
> motion specs + an AE blueprint from the studio chain — no figuring out what to build),
> **(2) the animatic** (pacing fixed before AE, so no scene is built twice), **(3) the
> asset library** (reuse beats regenerate; check `assets_library/INDEX.md` before any new
> generation), **(4) template comps + JSX scaffolds** (a build family made once is a
> ~15-minute art-swap forever after). There are no charged retries anywhere in animation
> anymore — iteration costs minutes, not money. The studio chain itself is ₹0: the only
> charged step it triggers is the asset batch, behind a human gate.
>
> **Image cost, measured (Jul 2026, on the first — since scrapped — project):** ₹640 for 87 successful
> generations = **~₹7.4/image (~$0.086)**, because Nano Banana 2 emits larger, higher-token
> images (~1,400 output tokens each). That first run was ~87 gens because two *systematic*
> prompt issues were found and fixed (space-filling; style-anchor bleed); with those fixes
> baked into `visual_facts` + the gate skill, **steady state is ~60 gens ≈ ₹450/video.**
> ⚠️ **There is no free tier for image models** — the API key's project must have billing
> enabled (free tier returns `429 limit: 0`; a key restricted to the wrong service returns
> `403 API_KEY_SERVICE_BLOCKED`). Create the key in **AI Studio** on a **billing-enabled**
> project (or use Vertex via ADC).

## Monthly Cost Summary (at 2 videos/month)

| Expense | Cost |
|:---|:---|
| Claude Pro (orchestrator + script drafts) | ₹2,000/mo |
| **Adobe After Effects** (Single App plan) | **~₹2,000/mo (~$23)** — the animation stage; DaVinci Resolve (Fusion) is a free alternative while trialing |
| Google AI Studio images (~130/mo incl. library assets — **paid tier required, no free tier**) | ~₹1,000/mo (~$12) |
| ElevenLabs (optional, pickup fallback only) | Free tier or skip |
| Self-recorded voice, ffmpeg/moviepy, royalty-free music, Real-ESRGAN upscaling, Duik Ángela (rigging) | Free |
| **Total** | **~₹5,000/mo (~$60)** |

> The pivot swapped a credit-metered animation subscription for a flat AE subscription at
> a similar monthly price — but removed *all* variable animation cost and all charged
> retries. The number that actually scales with ambition now is **hours in AE**, which the
> library + templates push down every video. Self-hosting video models stays irrelevant:
> there is no generative video in the pipeline at all.

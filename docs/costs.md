# Costs & Budget

*Part of the [pipeline docs](../pipeline_automation.md). Figures corrected July 10, 2026 (Kling ~2× up from the original estimate; time 8–12 hrs, not 5–7).*

## Per-Video Cost Breakdown (50% Animation)

| Component | Unit Cost | Quantity | Total |
|:---|:---|:---|:---|
| Script draft (Claude via Pro plan) | Included in sub | 1 | $0.00 |
| Images (Nano Banana 2 / Gemini 3.1 Flash Image) | **~$0.086/image (~₹7.4)** — measured Jul 2026, not estimated | ~54 + ~10–15% gate regens | **~$5 (~₹450)** |
| AI animation (Kling `v3_0`, i2v **720p, no native audio**) | **6 cr/s** → 36–48 cr per 6–8s clip (measured: 7s = **42 cr**) | 27 clips + a few retries | **~1,300–1,500 credits** |
| Upscaling to 4K (Real-ESRGAN, local — stills *and* clips) | $0.00 | all scenes | $0.00 |
| Voice (self-recorded) | $0.00 | 1 | $0.00 |
| Particle overlays (stock) | $0.00 | ~10 | $0.00 |
| ffmpeg/moviepy assembly | $0.00 | 1 | $0.00 |
| Background music (royalty-free) | $0.00 | 1 | $0.00 |
| **Marginal cash per video** | | | **~₹450 (images)** — Kling animation is credit-metered under the flat Pro sub (below), not per-clip cash |
| ⏱️ **Your time per video** (the real cost) | | **~8–12 hrs** | *research + fact-check + accuracy gate + narration + QA + thumbnails* |

> **Your time is the binding constraint, not cash.** Kling is a flat monthly sub, so the only per-video cash is images (~₹450); the real budget is **credits**. Two levers keep a video inside ~1,300–1,500 credits: **(1) 720p + no native audio** (`v3_0`, `enable_audio=false`) = **6 cr/s** — turning audio off saves 2 cr/s vs. 8, and we add narration/music at assembly anyway; **(2) bias animated scenes toward 6s** — a 10s clip costs ~2× a 6s one. Then **upscale 720p→4K locally for free** rather than paying for native 1080p (8 cr/s) or Kling 4K (VIP) — **except dense-lattice-in-motion scenes**, which visibly shimmer at 720p and get 1080p (identified by measurement, not guesswork — see [upscaling.md](upscaling.md)); that hybrid runs ~1,440 cr/video, still ~2/mo. Measured rates (Jul 2026, GUI-confirmed):
>
> | | 720p | 1080p |
> |:--|:--:|:--:|
> | **no native audio** (`v3_0`, our default) | **6 cr/s** | 8 cr/s |
> | native audio on / `v3_0_turbo` | 8 cr/s | 10 cr/s |
>
> ⚠️ **Do not use `kling-video-v3_0_turbo`** — despite the name it bakes in audio (can't disable) and bills at the pricier 10 cr/s. Use **`v3_0` with `enable_audio=false`**, which also has *better element consistency* (less morphing).
>
> **Image cost, re-measured (Jul 2026, video #1 — Chand Baori):** ₹640 for 87 successful generations = **~₹7.4/image (~$0.086)** — ~4× the old ~$0.02 estimate, because Nano Banana 2 (Gemini 3.1 Flash Image) emits larger, higher-token images (~1,400 output tokens each). That first run was ~87 gens because two *systematic* prompt issues were found and fixed (palace-in-void; style-anchor bleed); with those fixes baked into `visual_facts` + the gate skill, **steady state is ~60 gens ≈ ₹450/video.** ⚠️ **There is no free tier for image models** — the API key's project must have billing enabled (free tier returns `limit: 0`).

## Monthly Cost Summary (at 2 videos/month)

| Expense | Cost |
|:---|:---|
| Claude Pro (orchestrator + script drafts) | ₹2,000/mo |
| Kling AI **Pro plan** (3,000 credits/mo) — at 720p no-audio (6 cr/s) a video ≈ 1,300–1,500 cr, so **~2 videos/mo fit** | ~₹2,050/mo (annual) – ₹3,100/mo (monthly) |
| Google AI Studio images (~120/mo, Gemini 3.1 Flash Image — **paid tier required, no free tier**) | **~₹900/mo (~$10.5)** |
| ElevenLabs (optional, pickup fallback only) | Free tier or skip |
| Self-recorded voice, ffmpeg/moviepy, royalty-free music, **4K upscaling (Real-ESRGAN local)** | Free |
| **Total** | **~₹5,000–6,000/mo (~$60–72)** |

> At 2 videos/month you generate ~110 images and ~54 clips. The Kling **Standard** plan (660 credits) is nowhere near enough — a 720p no-audio clip is ~36–48 cr, so a video's ~30 clips (incl. retries) is ~1,300–1,500 cr. Budget for **Pro** and hold the levers that keep 2 videos inside 3,000 cr: **720p + no native audio (6 cr/s)**, **6s duration bias**, and the [validated-still gate](../visual-accuracy-gate/SKILL.md) + one-retry rule to cap wasted rerenders — then upscale to 4K for free ([upscaling.md](upscaling.md)). **Self-hosting is still not warranted:** even at ~₹3,000/mo variable cost, Wan/Hunyuan on RunPod (~$2.4–2.9/hr) remains a false economy until you're at 30+ videos/month.
>
> ⚠️ **Gemini image billing (learned the hard way, Jul 2026):** image models have **no free tier** — a free-tier project returns `429 limit: 0` and an API key restricted to the wrong service returns `403 API_KEY_SERVICE_BLOCKED`. Create the key in **AI Studio** on a **billing-enabled** project (or use Vertex via ADC). Images are ~₹900/mo here — small vs. Kling, but no longer "free."

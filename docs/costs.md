# Costs & Budget

*Part of the [pipeline docs](../pipeline_automation.md). Figures corrected July 10, 2026 (Kling ~2× up from the original estimate; time 8–12 hrs, not 5–7).*

## Per-Video Cost Breakdown (50% Animation)

| Component | Unit Cost | Quantity | Total |
|:---|:---|:---|:---|
| Script draft (Claude via Pro plan) | Included in sub | 1 | $0.00 |
| Images (Nano Banana 2 / Gemini 3.1 Flash Image) | **~$0.086/image (~₹7.4)** — measured Jul 2026, not estimated | ~54 + ~10–15% gate regens | **~$5 (~₹450)** |
| AI animation (Kling AI, image-to-video 6–10s) | ~30–60 credits ≈ $0.35–0.75/clip | 27 clips + ~10 retries | **~$13–25** |
| Upscaling (Real-ESRGAN, local) | $0.00 | 27 static scenes | $0.00 |
| Voice (self-recorded) | $0.00 | 1 | $0.00 |
| Particle overlays (stock) | $0.00 | ~10 | $0.00 |
| ffmpeg/moviepy assembly | $0.00 | 1 | $0.00 |
| Background music (royalty-free) | $0.00 | 1 | $0.00 |
| **Cash cost per video** | | | **~$18–31** |
| ⏱️ **Your time per video** (the real cost) | | **~8–12 hrs** | *research + fact-check + accuracy gate + narration + QA + thumbnails* |

> **The dollar cost is still small; your time is the binding constraint.** The earlier "$7/video, 5–7 hrs" figures didn't survive scrutiny: Kling image-to-video at 6–10s costs $0.35–0.75/clip (the $0.15 figure was 5s text-to-video), and the production sessions genuinely sum to 8–12 hours. Duration is the main animation cost lever — **bias animated scenes toward 6s**; a 10s clip costs ~2× a 6s one. Never optimize the ~$20 at the expense of the human hours — they're what makes the video monetizable and good.
>
> **Image cost, re-measured (Jul 2026, video #1 — Chand Baori):** ₹640 for 87 successful generations = **~₹7.4/image (~$0.086)** — ~4× the old ~$0.02 estimate, because Nano Banana 2 (Gemini 3.1 Flash Image) emits larger, higher-token images (~1,400 output tokens each). That first run was ~87 gens because two *systematic* prompt issues were found and fixed (palace-in-void; style-anchor bleed); with those fixes baked into `visual_facts` + the gate skill, **steady state is ~60 gens ≈ ₹450/video.** ⚠️ **There is no free tier for image models** — the API key's project must have billing enabled (free tier returns `limit: 0`).

## Monthly Cost Summary (at 2 videos/month)

| Expense | Cost |
|:---|:---|
| Claude Pro (orchestrator + script drafts) | ₹2,000/mo |
| Kling AI **Pro plan** (3,000 credits — ~54 i2v clips/mo at 6–10s incl. retries needs 3,000–4,400 credits) | ~₹2,050/mo (annual) – ₹3,100/mo (monthly), + occasional top-up |
| Google AI Studio images (~120/mo, Gemini 3.1 Flash Image — **paid tier required, no free tier**) | **~₹900/mo (~$10.5)** |
| ElevenLabs (optional, pickup fallback only) | Free tier or skip |
| Self-recorded voice, ffmpeg/moviepy, royalty-free music | Free |
| **Total** | **~₹5,500–8,000/mo (~$65–95)** |

> At 2 videos/month you generate ~110 images and ~54 clips. The Kling **Standard** plan (660 credits) is nowhere near enough at this spec — a 6–10s image-to-video clip runs ~30–60 credits, so a video's ~37 clips (incl. retries) is ~1,500–2,200 credits. Budget for **Pro**, and pull the two levers that keep you inside it: bias animated scenes toward 6s, and let the [validated-still gate](../visual-accuracy-gate/SKILL.md) + one-retry rule cap wasted rerenders. **Self-hosting is still not warranted:** even at the corrected ~₹3,000/mo variable cost, Wan/Hunyuan on RunPod (~$2.4–2.9/hr) remains a false economy until you're at 30+ videos/month.
>
> ⚠️ **Gemini image billing (learned the hard way, Jul 2026):** image models have **no free tier** — a free-tier project returns `429 limit: 0` and an API key restricted to the wrong service returns `403 API_KEY_SERVICE_BLOCKED`. Create the key in **AI Studio** on a **billing-enabled** project (or use Vertex via ADC). Images are ~₹900/mo here — small vs. Kling, but no longer "free."

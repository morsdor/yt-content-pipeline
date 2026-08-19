# s001 · The Physical Cost of AI

**Pilot video (001) of a new, second channel: software-engineering *storytelling*** — narrative,
high-craft, few-but-polished videos, distinct from The Engineering Atlas (this repo's main channel).
The channel is not yet named or brand-guided; this project is its first concrete deliverable.

## Why this exists (the evidence trail)

1. **Idea:** can a software-engineering *storytelling* channel (not a coding-tutorial channel) grow?
2. **Scanned the lane:** `data/comp_channels_software.yaml` → `data/outliers_software.csv`
   (42 outliers ≥3× across 16 comps, 2026-08-09). Control group: `data/comp_videos_software.csv`.
3. **Hottest, highest-velocity vein:** AI/LLM. Second was evergreen algorithms-as-animation
   (3B1B/Reducible lane — needs a Manim capability we don't have). Third: incident stories
   (Kevin Fang lane — pilot #2 candidate).
4. **Concept chosen:** the *physical/industrial cost of AI* — the one AI angle that (a) rides the
   strongest replicable precedent (Computerphile *Why AI Tokens are so Expensive*, 14.2×/22.8) and
   (b) renders as **cinematic AI stills + camera/parallax motion**, no Manim-style procedural
   animation required. *(Originally justified as "fits the existing AE pipeline"; AE was retired
   2026-08-17 and the build is now Remotion — the reasoning survives the switch intact, since
   plate-plus-camera is `PlatePush`, the simplest composition family we have.)*
5. **Packaging gate:** passed — see `packaging.md` (locked title + thumbnail + 4-precedent evidence).

## Status

- ✅ Packaging locked (`packaging.md`, 2026-08-09)
- ✅ **Phase-0 research done** (`research.md`, 2026-08-10) — hero number resolved (energy ~0.3 Wh solid;
  water ~10–15 mL all-in but contested). Thumbnail **unblocked**. Two changes: water-bet runner-up title
  **killed** (500 mL/query is false); thumbnail number pivots per-query → **machine/aggregate scale**
  (recommended: the Three Mile Island reactor restart).
- ✅ **Thumbnail direction locked** — A, "the reactor" (Three Mile Island / 835 MW), 2026-08-10.
- 🟡 **Script — DRAFT v2** (`script.md`, 2026-08-10): ~12 min, dazzle ladder (rack→plant→fab→nation→reactor).
  v2 rebalanced **off water** (electricity is the spine — power = 3 of 5 tentpoles + climax; water = 1 tight
  beat; chip beat = silicon/manufacturing) and **cut the finger-pointing** (reflection beat is wonder, not
  media-criticism). **Next: your read-pass / lock.**
- 🟡 **Thumbnail — Stage-4 typography done** (`thumbnail.md` + `output/`, study): real local type (Arial
  Black / IBM Plex) in 3 hero options (835 MW · **A NUCLEAR REACTOR** ⭐ · 1 BILLION A DAY) over a **stand-in**
  plate. **Open:** pick the hero text; then the **charged gate** — generate the real Stage-2 AI plate.
- ✅ **Channel brand guide written** (`brand_guide_software.md`, 2026-08-17) — identity, color, type,
  and a §5 motion spec compiled into `remotion/src/brand/tokens.ts`. **One decision still open: the
  channel name** (§0 — recommended *Load Bearing*). It blocks the wordmark, the channel art, and this
  video's **thumbnail typography**.
- ⬜ Then: studio board → VO → generation → **Remotion build** → conform. Same production spine as 001
  with one change: **After Effects was retired 2026-08-17** — pass 7 is now `remotion-director`
  writing `remotion_build{}`, and 001 is the last AE video.

## Format decision — storytelling, not personality (2026-08-10)

Considered and **rejected** the personality/challenge-entertainment lane (ref: **commonLuke** —
@commonLuke, ~51k subs in 8 months on "I Tried to [learn/build] X" videos, 243k median views). It grows
fast, but its moat is a charismatic on-camera human — the one thing we *can't* AI-leverage — and it needs
on-camera charisma + faster cadence. That's the opposite of the "few, high-craft, AI-leveraged, off-camera"
intent. Kept as an **audience-lane reference** (same dev-curious viewer, different format), not a model to
copy. Fireship-style "blend" (voice/personality + tech, faceless) remains a possible future lever.

## Open channel-level decisions

- 🔴 **Channel name — the one live blocker.** Brand guide §0 recommends **Load Bearing**; alternates
  are The Stack Trace and Blast Radius. Everything in the guide except §1–§2 is name-independent, so
  this blocks only the wordmark, the channel art, and **this video's thumbnail typography** — which is
  exactly where the thumbnail thread is parked.
- ✅ **Brand guide — written** (`brand_guide_software.md`, 2026-08-17). The Engineering Atlas
  `brand_guide.md` does not transfer; this is its sister document.
- **Visual language** — cinematic/industrial (this concept) vs conceptual-animation (the algorithms
  vein). This pilot deliberately picks cinematic because it is the cheapest to build; revisit if the
  channel leans toward the 3B1B/Reducible lane later.

## Files
- `packaging.md` — the locked Stage-1 gate deliverable (founding document).
- `research.md` — Phase-0 research + fact-check (hero number, industrial chain, honest counter-framing, dazzle spine).
- `script.md` — DRAFT v2 VO script (~12 min); written in EA's witness/engineer registers — **re-check
  against `brand_guide_software.md` §6** ("The Insider and the Translator"), which now supersedes them.
- `teleprompter.html` — standalone offline teleprompter for the read (double-click to open; electric-blue palette). Regenerate from `script.md` if the script changes.
- `thumbnail.md` + `output/thumb_*` — Stage-4 typography study (real local type over a stand-in plate; real AI plate = separate charged gate).
- `monetization.md` — channel-level earnings model (AdSense / sponsorships / product); migrate to the
  channel brand doc once the channel gets its own home.
- Channel-level docs at repo root: `brand_guide_software.md` (identity, color, type, §5 motion spec),
  `docs/comp_deep_dive_codesource.md` (the comp that shaped the format).
- Shared research assets live at repo root: `data/comp_channels_software.yaml`,
  `data/outliers_software.csv`, `data/comp_videos_software.csv`.

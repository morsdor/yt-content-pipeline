# Packaging System Audit — Task 0 Findings

*July 13, 2026. Pre-build audit for the packaging-research work: each section verifies
(or corrects) a task premise against the actual repo, with file:line evidence. Nothing
was edited to produce this report. Verdict table at the end.*

---

## 1. Does an automated outlier / title-research system exist?

**No.** Searched `outlier`, `vidiq`, `youtube api`, `googleapis`, `fetch_outliers`,
`data/*.csv`, and any YouTube Data API usage across all `.md`/`.py`/`.yaml`/`.json`:

- The only "outlier" hit is prose — `strategy_review.md:61` ("The 50K figure is a
  top-decile outlier"). No tooling.
- No `data/` directory, no `scripts/` directory, no competitor list with channel IDs
  anywhere. (Competitors are *named* in `channel_strategy.md` §1/§3, IDs never recorded.)
- The only CSVs/JSONLs in the repo are Kling submission logs under
  `projects/001_chand_baori/clips/` — unrelated, historical.
- vidIQ is never mentioned in any document.

What *does* exist on the title side: 5 prose title patterns (`channel_strategy.md:244–250`)
and per-project `packaging.md` files (001's is complete and well-formed). Evidence layer:
none. → **Task 1 is a genuine gap. Build.**

## 2. Where exactly is packaging validated today?

At **script/storyboard approval — after research and scripting hours are already spent.**
And the three governing docs disagree among themselves on which gate:

| Source | Quote | Gate it names |
|:---|:---|:---|
| `channel_strategy.md:191` | "**Packaging-first gate (at storyboard approval, before any production spend):** write the title and a one-sentence thumbnail concept" | storyboard approval |
| `thumbnail-workflow/SKILL.md:20,85` | "Stage 1 — Packaging-first gate (**at storyboard approval**, BEFORE any production spend)" · "The packaging gate **blocks storyboard approval**" | storyboard approval |
| `the-engineering-atlas-video/SKILL.md:62` | "**Packaging-first gate** (…): title + one-sentence thumbnail concept **before anything is boarded**" — listed under *Phase 1 — Script* | script approval |
| `new_video_prompt_template.md` (step 3) | "give me the title + a one-sentence thumbnail concept with it — **no thumbnail concept, no approval**" | storyboard approval |

Two observations:

1. "Before any production spend" in these docs means **cash** (image generation), not
   **hours**. Phase 0 research (2–4 hrs) and Phase 1 script (1–2 hrs) run before any
   packaging validation. The task's premise stands: nothing validates the promise before
   research/scripting spend.
2. The script-vs-storyboard disagreement is an artifact of the July 13 studio pivot
   (the skill moved the gate earlier; strategy + thumbnail docs weren't retimed).
   **Task 3 resolves both problems with one answer:** validation at Phase −1 (topic
   selection), execution at thumbnail production — every doc retimed consistently.
   → **Build.**

## 3. Is there an enforced Tier-1 geographic-targeting rule?

**No — projections only.** The economics *assume* a Tier-1 shift but nothing makes it happen:

- `channel_strategy.md:50` (§1 caveat): "a new, India-based channel covering global topics
  **will skew India / Tier-2/3 for the first 6–12 months** … Tier-1 RPM is *earned* as your
  audience mix shifts" — descriptive, not enforced.
- `channel_strategy.md` §5 tier table (20% → 60%+ Tier 1 over 24 months) — a forecast with
  no mechanism attached.
- `strategy_review.md` §1 — same observation, same gap.
- Zero hits for launch seeding, Hacker News, subreddits, or any geography check in the
  publish phases (`the-engineering-atlas-video/SKILL.md` Phase 9,
  `docs/production_workflow.md` Session 7 — neither has a geo item).

→ **Task 4 builds** (as §4b, next to the §4a non-negotiables, + a publish-phase checkbox).

## 4. Narration consistency check

**Consistent — no contradiction, no change needed.**

- `channel_strategy.md:56` (§2): "Self-narration from **day 1**."
- `the-engineering-atlas-video/SKILL.md:75` (Phase 3): "Record the fact-checked script
  yourself (**before** any AE work — animate to track, `RHYTHM-1`)."
- `docs/voice_narration.md:5,27`: "record your own narration (from day 1)" · the ElevenLabs
  clone is "a convenience tool, **never the narration source**."

Nothing anywhere implies AI narration as default; the clone is pickups-only, consistently.

## Premise corrections (minor, none block a task)

- **`assets/thumbnails_log.md` does not exist yet** — by design: `thumbnail-workflow/SKILL.md:70`
  says "(create on first use)" and no video has published. Not a gap.
- **GitHub remote exists** (`github.com/morsdor/yt-content-pipeline`), so the weekly Action
  can actually run — once you add `YOUTUBE_API_KEY` (and optionally `ANTHROPIC_API_KEY`)
  as repo secrets. Until then it's a harmless no-op.
- **No `strategy/` directory** — strategy docs live at repo root (`channel_strategy.md`,
  `strategy_review.md`). The formula library will therefore be root-level
  **`formula_library.md`**, not `strategy/formula_library.md` (per "trust the repo").
- **Conventions Task 1 will reuse:** the hand-rolled `load_dotenv()` helper
  (`generate_images.py:38`); stdlib `urllib` for HTTP (repo has no `requests`); `pyyaml`
  added to `requirements.txt`; no Anthropic API usage exists yet, so `tag_outliers.py`
  lazy-imports `anthropic` with an install hint and gates the charged call behind `--yes`.

## Verdicts

| Task | Verdict |
|:---|:---|
| 1 — Outlier database + title research | **Build** — nothing exists |
| 2 — Formula library | **Build** — reconcile §4's five house patterns into it (one canonical list) |
| 3 — Phase −1 packaging gate | **Build** — also fixes the 3-way gate-timing inconsistency |
| 4 — Tier-1 geo rule | **Build** — projections exist, enforcement doesn't |
| Narration contradiction | **No action** — docs are consistent |

---

*Produced without edits to any audited file. Build plan: branch `feat/packaging-research-system`, one reviewed commit per task.*

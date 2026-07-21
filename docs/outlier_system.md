# The Outlier System — Competitor Research on Autopilot

*Part of the [pipeline docs](../pipeline_automation.md). Added July 13, 2026 with the
packaging-research system. This is the **evidence base for the Packaging gate**:
before a topic earns research hours, it must show a ≥3× precedent — a video on a
comparable channel that broke out well above that channel's normal performance.*

## What it does

Fifteen competitor channels (`data/comp_channels.yaml` — format, topic, audience, and
packaging lanes) are scanned via the **free YouTube Data API v3**. For each channel:

1. Pull the last ~30 **long-form** uploads (Shorts excluded by duration ≤ 3:00; live entries skipped).
2. The channel's **median views** over that window = its baseline.
3. Every video with `views ÷ baseline ≥ 3.0` is an **outlier** → a row in `data/outliers.csv`.
4. Claude then tags each outlier with the [formula](../formula_library.md) its title uses
   (`formula_tag`) and one sentence on why it earned clicks (`why`).

The multiple — *not* raw views — is the signal: 40M views on RealLifeLore is a Tuesday;
900K on Plainly Difficult is a breakout worth studying.

## The three scripts

| Script | What it does | Cost |
|:---|:---|:---|
| `scripts/fetch_outliers.py` | Full scan, builds/refreshes the CSV. Idempotent — reruns update views in place, never duplicate. `--only mustard` for a quick test. | ₹0 (free quota) |
| `scripts/weekly_refresh.py` | Same scan restricted to the last 30 days + a "what's new" summary. The Monday habit. | ₹0 |
| `scripts/tag_outliers.py` | Labels untagged rows against `formula_library.md`; prints the **top-3 patterns** among ≥5× outliers of the last 90 days. | **charged** (~$0.02/50 rows on Haiku) — gated behind `--dry-run` / `--yes` |

> [!TIP]
> **The ₹0 tagging path:** in a Claude Code session, Claude *is* the model — it tags new
> rows directly (same contract: F-ids from the library or `none`, one-line `why`) at no
> extra cost. The script's API path exists only for **unattended** runs (the weekly
> Action), and even there it self-skips without a key; untagged rows simply accumulate
> until the next working session.

## Setup (one-time)

1. [console.cloud.google.com](https://console.cloud.google.com) → create/select a project
   → **APIs & Services → Library →** enable **"YouTube Data API v3"** → **Credentials →
   Create credentials → API key**.
2. Add `YOUTUBE_API_KEY=...` to `.env` at the repo root.
   ⚠️ This is a **different key** from the Gemini one: the YouTube Data API's free tier
   (10,000 units/day) needs **no billing**. Don't reuse the AI Studio key.
3. Optional (unattended tagging only): `ANTHROPIC_API_KEY` in `.env` + `pip install
   anthropic`. Skip this if Claude tags in-session (the ₹0 path above).
4. First run: `python3 scripts/fetch_outliers.py` — **eyeball the channel-resolution
   table it prints** (handle → channel title): a wrong handle would silently track the
   wrong channel forever. Resolutions are cached in `data/.channels_cache.json`
   (delete it if a handle changes).
5. Optional CI: add `YOUTUBE_API_KEY` (and optionally `ANTHROPIC_API_KEY`) as **repo
   secrets** on GitHub — `.github/workflows/weekly_outliers.yml` then refreshes the CSV
   every Monday and commits it. Without secrets the workflow no-ops harmlessly.

## Quota math (why this is free forever)

Per full run: ~15 handle resolutions (first run only) + per channel ~1–2
`playlistItems.list` pages + 1–2 `videos.list` batches ≈ **~50–80 units**. The free
daily quota is **10,000**. Even daily runs would use <1% — `search.list` (100 units/call)
is deliberately never used.

## Reading `outliers.csv`

Columns: `id, date_added, channel, title, url, published, views, baseline, multiple,
thumbnail_url, duration, formula_tag, why`.

- **`multiple` is the whole point** — how far above the channel's own normal this video
  performed. ≥3× = audience pulled it beyond the subscriber base; ≥5× = the packaging
  itself did heavy lifting.
- **Young-video bias:** a video published days ago hasn't accumulated views yet, so its
  multiple is *understated*. Outliers surface reliably ~2–4 weeks after publish — the
  weekly refresh updates numbers in place, so late bloomers get promoted automatically.
- `formula_tag`/`why` are the human-value columns — never overwritten by refreshes.
- Rows are never deleted; a row whose multiple later sinks below 3× stays as a record.

## Division of labor: vidIQ vs this system

- **vidIQ (browser) = discovery.** Interactive keyword research, search volume,
  competition scores, browsing outliers *outside* the fixed comp set. Use it while
  hunting for new topic angles.
- **This system = monitoring + evidence.** A permanent, self-owned, queryable record of
  what breaks out across *your named competitors*, refreshed weekly, tagged by formula.
  vidIQ shows you a moment; the CSV accumulates a dataset the channel owns.

## How Packaging consumes it

At the packaging gate (`the-engineering-atlas-video` Packaging):

1. **Precedent check** — search the CSV for the concept's subject/mechanism keywords
   (`grep -i "canal" data/outliers.csv`). A ≥3× hit on a comparable channel = precedent;
   none (and none in vidIQ either) → **park the topic**.
2. **Formula pick** — start title generation from the current top-3 patterns that
   `tag_outliers.py` prints, then broaden across `formula_library.md`.
3. **Thumbnail scan** — open the `thumbnail_url`s of the precedent rows at 120px; note
   what survives the shrink before writing our own concept.

## Compliance & scope

Read-only requests against **public** YouTube data via the official Data API, within the
free quota, for channels we don't own — no scraping, no private metrics (their analytics
stay theirs; the view count is public). The only numbers we act on are our own Studio
analytics (§4b geography check) and public counts.

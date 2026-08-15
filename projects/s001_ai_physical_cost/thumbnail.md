# s001 · Thumbnail — Stage-4 Typography (study)

> `thumbnail-workflow` SKILL Stage 4 (local typography, **never AI lettering**). Locked direction:
> **A · "The Asymmetry / the reactor"** (`packaging.md` + `research.md` §6). Type here is **real and final-
> quality** (rendered locally with Pillow); the **background is a STAND-IN** — the real AI plate (Stage 2)
> is a separate **charged** image-gen gate, not yet run. Outputs in `output/`.

## What's decided vs. still open
- ✅ **Direction:** A — the reactor (Three Mile Island / 835 MW), phone-vs-machine asymmetry.
- ✅ **Layout convention (provisional for this channel):** **subject on the RIGHT, hero type on the LEFT**
  over clean dark space. Pick once, keep every video (like 001's structure-left / text-right).
- 🟡 **Hero text — pick one** (rendered as A/B/C below).
- 🟡 **Display face — provisional.** Rendered in **Arial Black** (max 120-px punch) + one **IBM Plex Sans
  Bold** comparison (`thumb_B_reactor_plex.png`; IBM Plex is bundled and reads "tech/software"). This
  channel has **no brand guide yet** — the font locks when the brand does.
- 🔴 **Blocked on a charged gate:** the real Stage-2 AI plate (glowing datacenter wired to a reactor +
  tiny phone). Needs your go-ahead before any image-gen spend. Until then the type sits on the placeholder.

## The rendered options (all locked-reactor direction)
| File | Hero | Read |
|:--|:--|:--|
| `thumb_A_835mw.png` | **835 MW** | Number-led; biggest punch, but "MW" leans on the image to explain it |
| `thumb_B_reactor.png` | **A NUCLEAR / REACTOR** | ⭐ Plain-language shock; legible even at 120 px; needs no jargon — **recommended** |
| `thumb_C_fleet.png` | **1 BILLION / A DAY** | The fleet-scale alt (research §6 alternate); a different angle, kept for the A/B test |
| `thumb_B_reactor_plex.png` | same as B, **IBM Plex Sans** | Font comparison (softer/tech vs Arial Black's punch) |

Each has a `_120.png` squint sibling; `thumb_contact_sheet.png` shows all three full + squint. Subs are
intentionally small (they vanish at 120 px — the hero must carry the frame alone; Stage-3 rule).

## Re-stamp onto the REAL plate (once Stage 2 is generated — the house tool, ₹0)
When the real `thumb_plate.png` exists, drop the placeholder and stamp with the house Stage-4 tool
(`add_thumbnail_text.py` — Pillow, local, never AI text). Example for the recommended hero:

```bash
python add_thumbnail_text.py \
  --input  projects/s001_ai_physical_cost/output/thumb_plate.png \
  --output projects/s001_ai_physical_cost/output/thumb_reactor_text.png \
  --hero "A NUCLEAR REACTOR" --sub "to keep the answers coming" \
  --corner tl \
  --font "/System/Library/Fonts/Supplemental/Arial Black.ttf"
```

(The study renderer that made these placeholders lives in the session scratchpad:
`build_s001_thumb_typo.py` — a stand-in generator, not committed; the house tool above is the real path.)

## Stage-3 squint check (recorded)
- [x] One dominant object ≥60% (the machine, right) — ✅ in the stand-in; must hold in the real plate.
- [x] ≤4 words readable at 120 px — ✅ "A NUCLEAR REACTOR" and "835 MW" both survive; sub does not (by design).
- [x] Pops on dark UI — ✅ white hero + dark stroke. ⚠ Re-check on a **light** UI once the real plate lands.
- [x] Curiosity gap — ✅ tiny "hi" vs a reactor is the whole hook; the words don't answer *why*.

## Next
1. **You pick the hero text** (A / B⭐ / C) and font feel (Arial Black vs IBM Plex).
2. **Gate: generate the real Stage-2 plate?** (charged image-gen) — on your go-ahead only.
3. Then re-stamp with the command above → 120-px re-check on light+dark → Test & Compare + log.

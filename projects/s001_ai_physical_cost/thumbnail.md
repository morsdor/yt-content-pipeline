# s001 · Thumbnail — Stage-4 Typography

> `thumbnail-workflow` SKILL Stage 4 (local typography, **never AI lettering**). Locked direction:
> **A · "The Asymmetry / the reactor"** (`packaging.md` + `research.md` §6). Type here is **real and
> final-quality** (rendered locally with Pillow); the **background is a STAND-IN** — the real AI plate
> (Stage 2) is a separate **charged** image-gen gate, not yet run. Outputs in `output/`.

## Decided

- ✅ **Direction:** A — the reactor (Three Mile Island / 835 MW), phone-vs-machine asymmetry.
- ✅ **Layout convention (this channel, all videos):** **subject on the RIGHT, hero type on the LEFT**
  over clean dark space. Same discipline as 001's structure-left / text-right.
- ✅ **Hero text (2026-08-20): `835 MW`, alone.** No kicker. Reasoning in `packaging.md` — short
  version: the image is a cooling tower, so the picture already says "nuclear reactor"; the number is
  the one thing it can't say. This reverses the ⭐ the earlier study put on "A NUCLEAR REACTOR".
- ✅ **Display face (2026-08-20): Archivo Black**, now vendored at `assets/fonts/ArchivoBlack-Regular.ttf`
  (OFL). The channel brand exists as of 2026-08-17, so the font is no longer provisional — this
  supersedes the Arial Black / IBM Plex Sans study below.
- ✅ **The §4 rule collision, settled by test.** `brand_guide_software.md` §4 says *thumbnail hero →
  Archivo Black* **and** *numbers are always mono*. `835 MW` is a number, so both applied. Rendered
  head-to-head (`thumb_D_font_contact_sheet.png`): **Archivo Black wins decisively.** Mono's uniform
  advance width forces wide sidebearings — at 120px the lockup spreads wider at lower stroke density
  and fragments "835" and "MW" into two words instead of one mark. §4 now carries an explicit
  thumbnail carve-out so this doesn't get re-litigated per video. **In-frame numbers stay mono.**

## Open

- 🟡 **Hero colour — deliberately deferred to the real plate.** Signal amber `#FFB020` is the brand
  anchor (§3: "the single most important number in any frame"), but in the study **bone `#E8E6E1`
  reads harder at 120px** against the stand-in's blue-dominant field. That result is a property of the
  *placeholder*, not of the design — amber-on-blue is high hue contrast but close in luminance. Do not
  lock this until the real plate exists; re-squint both then.
- 🟡 **A/B variant B (reactor + AI model logos)** — approved as the A/B axis, not yet built. See
  `packaging.md`. Logos must be local vector assets, never image-model output.
- 🔴 **Blocked on a charged gate:** the real Stage-2 AI plate. Needs explicit go-ahead before any
  image-gen spend. Until then the type sits on the placeholder.

## Plate-prompt requirement carried into Stage 2

**The foreground device must read as an assistant-chat interface, not a text message.** A phone with a
generic SMS bubble reads as *texting*; at 120px it collapses to a dark sliver and the thumbnail scans
as an energy/infrastructure video rather than an AI video. Use the recognisable chat-UI silhouette with
"hi" in it. This is the one defect the current direction has, and it is fixed in the prompt, not the
typography.

## Current renders (locked hero, brand faces)

| File | Face / colour | Read |
|:--|:--|:--|
| `thumb_D_835mw_archivo_amber.png` | Archivo Black / amber | ⭐ On-brand default. Dense, tight, one solid mark at 120px |
| `thumb_D_835mw_archivo_bone.png` | Archivo Black / bone | Highest raw contrast on the stand-in — the colour A/B |
| `thumb_D_835mw_plexmono_amber.png` | IBM Plex Mono Bold / amber | The rejected mono test. Visibly lighter and wider; fragments at squint |

Each has a `_120.png` squint sibling; `thumb_D_font_contact_sheet.png` shows all three full + squint.

<details>
<summary>Superseded — the 2026-08-13 study (pre-brand, pre-hero-lock)</summary>

Rendered before the channel had a brand guide or a name, in Arial Black + one IBM Plex Sans comparison,
across three candidate heroes. Kept for the record; **do not build from these.**

| File | Hero | Then-verdict |
|:--|:--|:--|
| `thumb_A_835mw.png` | 835 MW | "leans on the image to explain MW" — now the locked hero |
| `thumb_B_reactor.png` | A NUCLEAR / REACTOR | ⭐ then-recommended — now rejected (restates the image; 5 words vs the ≤4 budget) |
| `thumb_C_fleet.png` | 1 BILLION / A DAY | fleet-scale alt; still a title-level alternate only |
| `thumb_B_reactor_plex.png` | as B, IBM Plex Sans | font comparison, superseded by the Archivo test |

</details>

## Re-stamp onto the REAL plate (once Stage 2 is generated — the house tool, ₹0)

When the real `thumb_plate.png` exists, drop the placeholder and stamp with the house Stage-4 tool
(`add_thumbnail_text.py` — Pillow, local, never AI text). Note the `--font` flag is **required** for
this channel: the tool's default is Fraunces, which is The Engineering Atlas's face.

```bash
python add_thumbnail_text.py \
  --input  projects/s001_ai_physical_cost/output/thumb_plate.png \
  --output projects/s001_ai_physical_cost/output/thumb_835mw_text.png \
  --hero "835 MW" \
  --corner tl \
  --color "255,176,32" \
  --font assets/fonts/ArchivoBlack-Regular.ttf
```

Swap `--color "232,230,225"` for the bone comparison, then squint both at 120px and lock the colour.

*(The study driver that produced the stand-in renders lives in the session scratchpad:
`build_s001_thumb_typo_v2.py` — it imports `add_thumbnail_text.render`, so the type is stamped by the
real house tool; only the 120px siblings and contact sheet are scratchpad code.)*

## Stage-3 squint check (recorded, on the stand-in)

- [x] One dominant object ≥60% (the machine, right) — ✅ in the stand-in; **must hold in the real plate**.
- [x] ≤4 words readable at 120 px — ✅ `835 MW` survives cleanly at 2 words.
- [ ] **AI signal legible at 120px — ❌ FAILS on the stand-in.** The phone vanishes. Fixed by the
      chat-UI plate-prompt requirement above; re-check on the real plate.
- [x] Pops on dark UI — ✅. ⚠ Re-check on a **light** UI once the real plate lands.
- [x] Curiosity gap — ✅ tiny "hi" vs a reactor is the whole hook; the number doesn't answer *why*.

## Next

1. **Gate: generate the real Stage-2 plate?** (charged image-gen) — on your go-ahead only. Prompt must
   carry the chat-UI requirement.
2. Re-stamp with the command above → lock hero colour (amber vs bone) at 120px on light + dark.
3. Build variant B (logos) → Test & Compare → log the result.

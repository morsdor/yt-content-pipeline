# The Engineering Atlas — Brand Guide

*The single source of truth for identity, voice, and look. Every video, thumbnail, and script conforms to this. Version 1.0 — July 6, 2026.*

---

## 1. Identity

**Channel name:** The Engineering Atlas
**Handle:** `@TheEngineeringAtlas` (verify availability on YouTube, and grab the matching X/Instagram/TikTok handle even if unused). If taken, fallbacks: `@EngineeringAtlas`, `@TheEngAtlas`.

**One-line positioning:** *How civilizations solved hard engineering problems — cutaways through history, from an engineer's eye.*

**Tagline (pick one, use consistently):**
- **"How the world was built."** ← recommended: short, universal, curiosity-forward
- "The engineering behind history."
- "Cutaways through time."

**What it is:** engineering education through historical case studies, global in scope (India, the Islamic world, China, Europe, the Americas), delivered with narrative pull and technical authority.

**What it is NOT:** a generic history channel, a Eurocentric channel, a current-events channel, a personality vlog, or a low-effort AI-slop channel.

---

## 2. Logo & Channel Art

**Wordmark concept:** "The Engineering Atlas" set in a refined serif (see typography), with the **A** in "Atlas" subtly formed as a **keystone arch** — the two legs of the A meeting at a wedge-shaped keystone. It reads as a normal A at a glance, and as an arch on a second look. This ties the logo to the single most universal engineering motif in your content (§ the arch video).

**Alternate mark (for avatar / favicon):** a circular badge — a simplified isometric **cross-section** (three arch tiers, or a keystone) in charcoal on parchment, thin technical linework, optional compass-rose tick marks around the rim to signal "atlas / global."

**Channel banner:** a wide isometric "atlas plate" — several of your civilization structures (aqueduct, stepwell, pagoda, pyramid) lined up small along a warm parchment field, wordmark left-aligned, tagline beneath. Muted, elegant, not busy.

**Brand-anchor color for logo/channel art:** **Steel blue `#3D5A80`** (the cross-civ neutral) or **charcoal `#2C2C2C`** on **parchment `#F5F0E8`**. The per-civilization accent colors are for *video content*, not the fixed brand marks — keep the logo civilization-neutral.

---

## 3. Color System

Reuse the "Architectural Atlas" palette already defined in `channel_strategy.md`. Consolidated reference:

**Base palette (every video):**

| Role | Color | Hex |
|:---|:---|:---|
| Background | Warm parchment | `#F5F0E8` |
| Dark elements / text | Charcoal | `#2C2C2C` |
| Light elements | Cream | `#FAF7F2` |
| Grid / diagram lines | Soft grey | `#B8B0A4` |
| **Brand anchor** (logo, channel art, neutral topics) | Steel blue | `#3D5A80` |

**Per-civilization accent (signals region without being heavy-handed):**

| Civilization | Accent | Hex |
|:---|:---|:---|
| Indian | Warm saffron / ochre | `#D4812A` |
| Islamic / Arabian | Deep teal | `#1A7A6D` |
| Chinese | Jade green | `#4A7C59` |
| European / Roman | Terracotta | `#B85C38` |
| Mesoamerican | Obsidian purple | `#5C3D6E` |
| General / CS / cross-civ | Steel blue | `#3D5A80` |

**Rule:** one accent per video, chosen by the topic's region. Text-overlay highlight bars and key callouts use that accent; everything else stays in the neutral base.

---

## 4. Typography

Two free, engineering-appropriate type families. Consistency here is 30% of "looking like a real brand."

| Use | Font | Why |
|:---|:---|:---|
| **Wordmark & video titles** | **Fraunces** (or Spectral) — a warm, high-contrast serif | Atlas / editorial / authoritative, not generic |
| **On-screen labels & callouts** | **IBM Plex Sans** | Clean, technical, excellent legibility at small sizes |
| **Data / measurements / mono callouts** | **IBM Plex Mono** | Signals "engineering / precision" — use for numbers, dimensions, dates |

- All three are free (Google Fonts). Download into `assets/fonts/`.
- **On-screen text rules:** charcoal text on a semi-transparent cream/parchment bar, or cream text on a semi-transparent charcoal bar. Never raw text on a busy image. Accent color only for the single most important word/number in a callout.

---

## 5. Narration Style — "The Witness and the Engineer"

> This is the heart of the brand and the answer to "storytelling without losing authority." It braids two registers. **Story frames, engineering explains, wit seasons.**

### The two registers

**1. The Witness (narrative / story).**
Each video opens with — and periodically returns to — a person of the era who *encountered* the thing being built: an anonymous water-slave watching Roman arches rise across a valley; a mason cutting the tenth descending step of a stepwell; a Song-dynasty clerk tallying six million bushels of rice moving up a canal. This is the CGP-Grey / OverSimplified narrative pull — a human stake that makes an engineering problem *matter*. It can be one recurring witness or a small set across the video.

**2. The Engineer (authority / explanation).**
When it's time to explain *how*, step back into a calm, precise voice — real numbers, real mechanisms, the actual constraint. First-person engineering asides are welcome and are your differentiation: *"The real problem wasn't lifting the stone. It was lifting it the same way, ten thousand times, without a single failure."* This is where channel authority lives.

### Wit — dry, not comic

Roughly **one raised-eyebrow beat every 60–90 seconds**, always in service of the point. It lives in *phrasing*, never in gags, memes, or anachronism.
- ✅ *"The Romans had no word for 'hydraulic gradient.' They had something better: a finished aqueduct."*
- ✅ *"It should have fallen down. It has now not fallen down for nine hundred years."*
- ❌ Pop-culture jokes, sound-effect gags, "and then everything went wrong lol," fake character dialogue played for laughs.

### Why this does NOT degrade authority

Authority comes from **accuracy and clarity**, not from being humorless. Real Engineering, Practical Engineering, and CGP Grey are all witty *and* authoritative. The guardrails that protect authority:

1. **The witness is a framing device, never a source of facts.** You never put an invented claim in a character's mouth. If a detail is speculative, say so ("we don't know his name, but someone did this work").
2. **Wit is in phrasing, never mockery** of the people or cultures.
3. **The engineering explanation is always delivered straight** — no jokes inside the load-path.
4. **Every fact is verified** (see the production skill's fact-check gate). Wit on top of wrong facts is fatal; wit on top of rigor is charm.

### Delivery spec

- **Voice:** your own, recorded (AI clone = pickup fallback only).
- **Pace:** ~140–150 wpm. Let key numbers *breathe* — a short pause after "fifty kilometres" lands harder than rushing on.
- **Tone:** curious, not lecturing. "Here's something fascinating," never "let me teach you."
- **Sign-off (consistent every video):** pick one and keep it.
  - **"Built to last — or built to teach us why it didn't. I'll see you in the next one."** ← recommended
  - "That's the engineering. See you in the next cutaway."

---

## 6. Video Structure Template (~10–12 min, ~54 scenes)

A repeatable beat sheet. Keeps every video recognizable and paced.

| Beat | ~Time | What | Register |
|:---|:---|:---|:---|
| **Cold-open vignette** | 0:00–0:30 | The witness. A human moment that poses the problem. End on a hook question. | Witness |
| **Title sting** | 0:30–0:35 | 2–3s wordmark + topic title. Minimal audio sting. | — |
| **The stakes / the problem** | 0:35–2:00 | Why this was hard. The constraint, in plain terms. | Engineer |
| **How they solved it** | 2:00–6:00 | The core. Cross-section reveal(s), mechanism, the clever bit. | Engineer |
| **The scale / the payoff** | 6:00–8:00 | Scale comparison, consequence, what it enabled. | Both |
| **What most people miss** | 8:00–10:00 | YOUR perspective — the systems/engineering insight only you frame this way. | Engineer (first person) |
| **Callback + close** | 10:00–11:00 | Return to the witness; resolve the opening. Sign-off. | Witness → sign-off |
| **Outro card** | last 5–8s | Subscribe + next-video thumbnail. | — |

- **Retention rule (from `animation_upgrade.md`):** no visual element static >5s; a scene change or new callout at least every 8s.
- **CTA:** one subscribe ask, woven in naturally around the 60–70% mark or at the outro — never a hard mid-roll beg.

---

## 7. Thumbnail Conventions

Fixed rules so your thumbnails are recognizable as a set:

- **One dominant object** filling 60%+ of the frame (the hero structure/mechanism).
- **Max 3–4 words** of text, in **Fraunces bold** (title font), high contrast.
- **Fixed layout:** structure on the **left**, text on the **right** (pick this and never flip).
- **Higher saturation** than video frames; dark moody background; single focal point; cinematic light.
- **Accent color** = the video's civilization accent, used on the text or a highlight.
- Curiosity gap: show enough to intrigue, never enough to answer.

---

## 8. Audio & Music

- **Background music:** ambient, low, non-distracting; **8% volume** under narration (per assembler default). Sourced royalty-free (Pixabay, Uppbeat, YouTube Audio Library). Keep a small consistent palette of 3–4 tracks so the channel has a sonic identity.
- **Title sting:** one short, consistent 2–3s musical/audio motif on every intro.
- **Silence is allowed.** Let a dramatic reveal sit without music for a beat.

---

## 9. Metadata & Consistency

- **Episode naming:** internal project folders `NNN_topic` (e.g., `001_roman_aqueducts`). Public titles follow the §4 title formulas in `channel_strategy.md`.
- **Description template:** 2–3 sentence hook → chapter timestamps → sources/further reading → subscribe line → social links. (Sources build authority and trust — always cite.)
- **"Altered content" disclosure:** ticked on every upload (AI-assisted visuals/voice).
- **Upload rhythm:** consistent day/time (e.g., Saturday AM US), 2 videos/month.

---

## 10. The One-Sentence Brand Test

Before publishing, ask: *"Does this look, sound, and think like The Engineering Atlas — a real engineer telling a real story, accurately, with a dry smile?"* If any of {look, sound, accuracy, perspective} is missing, it's not ready.

---

*Companion docs: `channel_strategy.md` (niche, projections, business phases), `pipeline_automation.md` (production tech), `animation_upgrade.md` (motion), `strategy_review.md` (the critical review these were revised from). Per-video execution: the `the-engineering-atlas-video` skill.*

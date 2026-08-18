# Load Bearing — Brand Guide (software/technical documentaries)

*The identity document for the **second channel** — technical documentaries told visually. Sister to
`brand_guide.md` (The Engineering Atlas), which does **not** transfer: different subject, different
viewer, different visual language. Written 2026-08-17, after the @CodeSource comp deep dive
(`docs/comp_deep_dive_codesource.md`) and the Remotion pipeline decision.*

> **§5 Motion Identity is not prose — it is the spec for `src/brand/motion.ts`.** Under the AE pipeline
> a brand guide was a document a human had to remember to obey. Under Remotion it compiles. Every
> number in §5 becomes a typed constant, and a scene that violates one fails review because it
> physically cannot be expressed. That is the whole reason this guide is worth writing before scene one.

---

## 0. The one open decision — the name

Everything below is name-independent except §1–§2. **Recommended: "Load Bearing."**

| Candidate | Case | Risk |
|:--|:--|:--|
| **Load Bearing** ⭐ | Instantly legible to non-engineers (*load-bearing wall*) and precise to engineers (*the dependency everything rests on*). Covers all four lanes — what became load-bearing (breakthroughs), what failed (blunders), what carries the weight (architecture). Carries your Engineering Atlas heritage into software, which is a position nobody else in this niche has. Deep cultural resonance with devs via xkcd 2347. | Two words; must never be written "Loadbearing" |
| The Stack Trace | The record of how something failed, read backwards to find the cause — literally the channel's method. Devs get it instantly. | Reads incident-only; weak for origin stories. Slightly insider |
| Blast Radius | Punchy, dramatic, perfect for the failure lane | Too narrow if you ever do architecture or breakthroughs |

**Lock the name before the wordmark, the channel art, or any thumbnail typography ships.** Everything
else in this guide can proceed today.

---

## 1. Identity

**What it is:** technical documentaries — breakthroughs, blunders, and the architecture underneath —
told so precisely that engineers respect them and so clearly that non-engineers finish them.

**The promise:** *the thing you depend on has a story, and it is more fragile and more human than you
think.*

**Who it is for, in order:**
1. Working developers and infrastructure people — the ones who'll pay attention to whether you got it right.
2. Technically curious non-practitioners — the growth audience. They must never need a prerequisite.
3. Recruiters of your credibility — sponsors, collaborators, employers.

**The two rules that define the channel:**

- **Technical subject, human stakes.** The subject can be as deep as you like; the *stakes* must be
  legible to anyone. A story about a race condition is a story about two things arriving in the wrong
  order — and about the people who found out at 3am.
- **Never explain by simplifying. Explain by re-framing.** Dumbing down loses register 1. A good
  physical analogy keeps both.

**Not this channel:** tutorials, "top 10", news reaction, hot takes, framework advocacy, anything
where the value expires.

---

## 2. Wordmark & Channel Art

- **Wordmark:** the name set in the display face (§4), letter-spaced +2%, on near-black. One
  structural rule mark — a single horizontal line *under* the word, weight 3px at 1080p, in the
  brand accent — reading as the load it carries. Nothing else. No icon, no gradient, no bevel.
- **Avatar:** the underline mark alone on near-black, or the initials. Must survive 48px.
- **Banner:** near-black ground, the wordmark left of centre, one line of positioning text below it
  in mono. No collage of video thumbnails.

---

## 3. Color System

Deliberately opposite to The Engineering Atlas. EA is warm parchment and daylight; this is **dark,
schematic, high-contrast** — software's native environment, disciplined like a drafting table rather
than glossy like a render.

**Base palette (every video):**

| Role | Color | Hex | Notes |
|:--|:--|:--|:--|
| Ground | Ink black | `#0B0E14` | Slightly blue-black, never pure `#000` — pure black crushes on OLED and kills depth |
| Surface / panel | Slate | `#161B26` | Cards, code panels, callout bars |
| Primary text | Bone | `#E8E6E1` | Warm off-white, never pure white |
| Secondary text / labels | Ash | `#8B94A7` | Annotations, axis labels, timestamps |
| Rule / grid / schematic line | Graphite | `#2A3240` | Diagram lines, dividers, grid |
| **Brand anchor** | Signal amber | `#FFB020` | The wordmark, the underline, the single most important number in any frame |

**Per-domain accent** — one per video, chosen by subject. (Structurally the same idea as EA's
per-civilization accent, so the studio chain treats it identically.)

| Domain | Accent | Hex |
|:--|:--|:--|
| Infrastructure / networking | Electric cyan | `#22D3EE` |
| Security / cryptography | Acid green | `#4ADE80` |
| Data / databases | Violet | `#A78BFA` |
| AI / compute | Signal amber | `#FFB020` |
| **Failure / incident** | Alert red | `#FF4D4D` |
| Languages / tooling | Sky | `#60A5FA` |

**Rules.**
- **Amber is reserved.** It is the brand anchor and the "this is the number that matters" color. If
  everything is amber, nothing is. **Maximum one amber element per frame.**
- Alert red is *only* for the failure lane and only on the beat where something breaks. Using it
  decoratively destroys its meaning.
- The domain accent carries callouts, key strokes in diagrams, and the thumbnail hero word. Everything
  else stays base.
- **Never put a saturated accent on more than ~10% of the frame.** Contrast is the asset.

---

## 4. Typography

| Use | Font | Why |
|:--|:--|:--|
| **Wordmark, titles, thumbnail hero** | **Archivo Black** (fallback: Arial Black) | Dense, industrial, engineered — punches at 120px, which is the only test that matters. Distinct from EA's warm Fraunces serif |
| **On-screen labels, callouts, body** | **IBM Plex Sans** | Already bundled locally, reads "technical" without costume. Weights 400 / 600 only |
| **Numbers, code, data, timestamps, filenames** | **IBM Plex Mono** | Every figure, every identifier. Mono *is* the channel's signal of precision |

- Free; keep in `assets/fonts/` and load into Remotion via `staticFile()` + `@remotion/fonts`.
- **Numbers are always mono.** This is the single most identity-defining typographic rule here — a
  metric in a proportional face immediately looks like a generic explainer.
- **On-screen text sits on a surface**, never raw on imagery: `#161B26` at 85% opacity, 8px radius,
  16px padding, 1px `#2A3240` border. Bone text. Accent on one word maximum.
- **Minimum on-screen size: 36px at 4K** (≈ 1.7% of frame height). Below that it is decoration, not
  information — cut it.

---

## 5. Motion Identity — the spec for `src/brand/motion.ts`

> EA moves like *a surveyor* — slow, weighted, geological. **Load Bearing moves like a system
> executing**: precise, purposeful, arriving exactly on time and then completely still. Snappier than
> EA. Never bouncy. Stillness is the default state; motion is an event that means something.

**Frame spec (every scene):** `3840×2160 @ 30fps` · rendered with **1s handles** both ends · target
`clips/scene_NN.mp4` (contract unchanged from the AE pipeline — Premiere conform stays trim-only).

### Easing — the two curves, and only two

```ts
export const EASE = {
  //          cubic-bezier          use
  standard: [0.4, 0.0, 0.2, 1.0],   // everything that enters, moves, or settles
  exit:     [0.4, 0.0, 1.0, 1.0],   // everything that leaves (accelerates away, no deceleration)
} as const;
```

**Springs are banned** except one sanctioned case: a diagram node landing into a locked position, and
only with `damping ≥ 200` (i.e. no visible overshoot). If a viewer can perceive the bounce, it's wrong.
Nothing in this brand wobbles.

### Camera (over a still plate)

| Move | Spec | Budget |
|:--|:--|:--|
| Push-in (default) | **3–5%** scale over the scene | Default; one move per scene, full duration |
| Pull-back (reveal) | **6–9%** | **2–3 per video max** — this is the scale-payoff move |
| Pan | **40–70 px/s** at 4K | Wide compositions only; direction persists across adjacent scenes |
| Static hold | 0% | **Mandatory on the hardest technical beat of every video.** When the idea is heavy, the frame stops moving |

Every camera move starts and ends at rest, with a **0.5s hold** at both ends inside the handles.

### Elements

| Class | Spec |
|:--|:--|
| Diagram build-on | Each element **250ms** in, **80ms** stagger between siblings, `EASE.standard` |
| Connecting line / flow | Draw-on **400–700ms**; a flowing packet/pulse travels **200–400 px/s** |
| Data counter | Counts up over **600–900ms**, `EASE.standard`, lands and **stops** — never idles or loops |
| Highlight / focus pull | Non-focus elements drop to **35% opacity** over 250ms; focus element unchanged (never scale-up to emphasise) |
| Ambient drift (smoke, heat, field) | **3–10 px/s**, ≤1.5° rotation, de-synced loop phases |
| Moving-element budget | **≤2** moving elements per scene, camera excluded |

### Text

- **In:** 250ms fade + **12px rise**. **Out:** 150ms fade, no movement.
- Emphasis is **color** (§3) or **weight**, never motion, never scale.
- On screen **≥2.5s**; clears **≥0.5s before the cut**.
- Forbidden: typewriter, per-word cascade, bounce, blur-in, counter-rotation, any preset that performs.

### Transitions

- **Cut** ≥90%. **Dip-to-black 300ms** = a chapter boundary only (≤4 per video). **Match-cut** =
  concept link, 2–3 per video.
- Forbidden: whips, glitches, zoom-blurs, page turns, light leaks, anything that says "template."

### The physics of the brand

1. Nothing overshoots. Nothing wobbles. Nothing idles.
2. Motion is **information** — if a move doesn't tell the viewer something, delete it.
3. **Stillness is a tool.** The most important frame in every video should be completely static.

---

## 6. Narration — "The Insider and the Translator"

The central tension of this genre: technical enough that engineers respect it, human enough that
everyone else finishes it. Two registers, braided.

**1. The Insider (authority — your differentiation).**
First-person practitioner. This is the register CodeSource structurally cannot do, and it's the
entire reason you have a right to this channel. It sounds like someone who has *been there*:
> *"If you've ever watched a migration run past its window with the rollback already failing, you
> know exactly what the next four hours looked like for them."*

Use it for judgement calls, for what the docs don't say, for why a decision that looks obviously
wrong was reasonable at the time.

**2. The Translator (access — your growth audience).**
Re-frames a mechanism in physical terms without losing precision. Never *"basically it's just…"* —
that signals you're about to lose the engineers. Instead, give the analogy and then immediately
give the real thing back:
> *"Every request waits in one line for one clerk. That clerk is a single thread — and the moment
> the clerk pauses to check something on disk, the entire line stops."*

**Wit:** one dry beat every 60–90s, in *phrasing*, never gags, memes, or snark at people. Failure
stories especially: the engineers in them were smart people having a bad day. Contempt is off-brand
and it reads as cheap.

**Guardrails (non-negotiable — same discipline as EA):**
1. **Never invent internal dialogue or motive.** For failures, this crosses into defamation risk fast.
   Say "the postmortem records that…", not "he panicked."
2. **Name the uncertainty.** *"The public postmortem doesn't say why."* Admitting the gap builds more
   authority than filling it.
3. **The explanation is always delivered straight.** No jokes inside a mechanism.
4. **Cite in-video for contested numbers**, and always in the description.

**Delivery spec.** Your own voice, recorded. **145–155 wpm** (slightly faster than EA — the subject
is contemporary, not geological). Let numbers breathe. Tone: *"here's what actually happened,"* never
*"let me teach you."*

**Sign-off — pick one and never change it:**
> **"Everything's holding something up. See you in the next one."** ⭐

---

## 7. Structure Template (~12–15 min)

Runtime target is **12–15 min**, not 10–13 — the comp data is unambiguous: CodeSource's 12–20 min
bucket medians **82,197** views against **48,213** for 8–12 min.

| Beat | ~Time | What | Register |
|:--|:--|:--|:--|
| **Cold open** | 0:00–0:45 | A specific moment, dated and located. *"Moscow. December 12, 2019."* No channel branding, no "hey guys." Ends on the question the video answers | Insider |
| **Title card** | 0:45–0:50 | Wordmark + topic. 2–3s. One audio motif | — |
| **The stakes** | 0:50–2:30 | Why this thing matters / how much rests on it. The load it bears | Translator |
| **Sponsor** | 2:30–3:15 | **After the hook has closed, never before.** Empirically where CodeSource places it across 63 sponsored videos | — |
| **The mechanism** | 3:15–8:00 | How it actually works. Diagrams, the clever bit, the constraint | Both |
| **The turn** | 8:00–11:00 | The breakthrough, or the failure and its blast radius | Insider |
| **What most people miss** | 11:00–13:00 | **Your** read. The judgement only a practitioner offers. This beat is the channel's moat | Insider |
| **Callback + close** | 13:00–14:00 | Resolve the cold open. Sign-off | Translator → sign-off |

- **Scene budget:** 60–80 scenes of **8–12s**, cut against pre-recorded VO.
- **Retention rule:** no visual configuration unchanged >8s.
- **One subscribe ask**, woven in ~60–70%. Never a hard beg.

---

## 8. Thumbnail Conventions

**The finding that governs this section:** across CodeSource's catalog, **the title and the thumbnail
make different promises.** Title = stable, searchable, evergreen. Thumbnail = the conflict hook.
Their titles all read "The Untold Story of X" while the thumbnails read "WRITE ONCE, SUE FOREVER."
The thumbnail is not a restatement of the title — it's the second, sharper promise.

- **Layout is fixed: hero type LEFT, subject RIGHT.** Pick it once, never flip (already provisional in
  `projects/s001_ai_physical_cost/thumbnail.md`).
- **≤4 words**, Archivo Black, bone or accent. Must survive the **120px squint test** — the only gate.
- **One dominant object**, 55–65% of frame. Dark ground, single light source, hard falloff.
- **One number, in mono, if the story has one.** The number does what the image can't.
- **A recurring visual anchor.** CodeSource's red/blue desk figure carried two years of thumbnails at
  near-zero cost. Decide yours during the first three videos and then keep it — this is the cheapest
  channel-recognition lever that exists.
- **Never** put a sponsor's product or logo in a thumbnail. Their one attempt (DeepAgent) was their
  second-worst video of 64.

Log every thumbnail to `assets/thumbnails_log.md` so CTR learning compounds.

---

## 9. Audio

- **Music:** sparse, tonal, low. **8%** under narration. Keep **3–4 recurring tracks** so the channel
  has a sonic signature.
- **One title motif**, 2–3s, on every video, unchanged.
- **Silence is a tool.** The beat where the thing breaks should have no music at all.
- **No sound effects on text.** Whooshes are the fastest way to look like a template.

---

## 10. Metadata

- **Projects:** `projects/sNNN_topic/` (the `s` prefix keeps these out of EA's `NNN` globs).
- **Title:** evergreen and searchable — the subject's proper noun must appear. Save the conflict for
  the thumbnail.
- **Description:** 2–3 sentence hook → chapters → **sources** → subscribe → socials. Always cite; in
  this genre sources *are* the authority.
- **"Altered content" disclosure ticked on every upload** (AI-assisted visuals). Non-negotiable —
  monetization depends on it.
- **Cadence:** 2/month. Sustainable beats fast; the comp set proves the plateau isn't fatal but a
  gap is.

---

## 11. Where each section lives in code

The point of writing this before scene one — every rule below has exactly one home, so it is enforced
rather than remembered.

| Guide section | Lives in |
|:--|:--|
| §3 Color · §4 Type · §5 Motion | `remotion/src/brand/tokens.ts` — `BASE`, `DOMAIN_ACCENT`, `FONT`, `TYPE_SCALE`, `EASE`, `CAMERA`, `TIMING` |
| §4 Font loading | `remotion/src/brand/fonts.ts` (`@remotion/google-fonts`) |
| §5 Frame spec | `<Composition width={3840} height={2160} fps={30}>`, `HANDLE_FRAMES = 30` |
| §5 Camera | `families/PlatePush.tsx`, `push` typed as `PushPercent` (a closed union, not `number`) |
| **Enforcement** | `remotion/scripts/check-brand.mjs` → `npm run brand:check`, wired into `npm run lint` |
| §7 Structure | `storyboard.json` scene skeletons (script-analyzer, pass 1) |
| §8 Thumbnails | `generate_thumbnail.py` + `add_thumbnail_text.py` → `assets/thumbnails_log.md` |

> [!IMPORTANT]
> **Corrected 2026-08-17 after building it — tokens are the spec and the validator, NOT runtime
> imports.** Remotion Studio only makes a style canvas-interactive (click-select, drag, editable
> keyframes, edits written back to code) when **every value in `style` is an inline literal**.
> `color: BASE.amber` greys the control out and silently costs the exact capability the pipeline was
> chosen for. So scene and family files **hardcode** brand literals, and `brand:check` scans them
> against `tokens.ts` and fails the build on drift.
>
> Enforcement therefore happens at **lint time, not import time** — which is strictly better: a lint
> catches drift that has already been written, while an import only prevents it by destroying
> interactivity. Verified catching all of: off-brand hex, non-brand easing curve, spring under
> damping 200, sub-36px type, and CSS `transition` (which never renders).

**Two tiers of tunability**, and the split is deliberate:

| Tier | What | How the user edits it |
|:--|:--|:--|
| **Canvas-interactive** | The 5–10 hero scenes per video. Written standalone, all literals, wrapped in `Interactive.Div` with `name` props | Click, drag, keyframe directly in Studio; edits write back to the file. Reference: `src/scenes/TitleCard.tsx` |
| **Props-editor tunable** | The other 50–70 mechanical scenes. Built from families taking props | Props panel writes back to code when `defaultProps` is an inline object literal on `<Composition>` |

**Clamp at the type level wherever possible.** `push: number` invites 40%; `PushPercent` is a closed
union of `0 | 3 | 4 | 5 | 6 | 7 | 8 | 9`. That is the difference between a brand guide and a brand.

---

## 12. The one-sentence test

Before publishing: *"Would an engineer who works on this exact system watch it without wincing — and
would their non-technical partner watch it to the end?"*

Both, or it isn't ready.

---

*Companions: `docs/comp_deep_dive_codesource.md` (the evidence behind §7 runtime and §8) ·
`brand_guide.md` (The Engineering Atlas — the sister channel, deliberately different) ·
`docs/cinematography.md` (craft canon behind §5) · the `studio-director` chain for per-video execution.*

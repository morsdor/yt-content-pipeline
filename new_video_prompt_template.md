# New Video — Kickoff Prompt Template

Copy the block below into a **new chat** (with the `yt video ideas` folder connected),
replace the `{{...}}` placeholders, and send. The `the-engineering-atlas-video` skill
carries the full structure; this prompt just aims it and enforces the review gates.

---

## Template (copy this)

```
Start a new video for The Engineering Atlas: {{VIDEO_TITLE}} ({{ONE_LINE_HOOK}}).
Use the `the-engineering-atlas-video` skill and follow `brand_guide.md` and `style_card.txt`.
Civilization / accent: {{CIVILIZATION}} ({{ACCENT_HEX}}).

Work through it in gated steps and STOP for my sign-off at each gate — don't run ahead:
1. Phase 0 — research + fact-check: show me your sources and the key facts
   ({{KEY_FACTS_TO_VERIFY}}) so I can verify BEFORE you write anything.
   Also build the reference pack: 5–15 real photos/plans into references/ (with
   source URLs) + references/visual_facts.md with the visually checkable claims.
2. Script: draft it in the witness + engineer + wit voice; I'll rewrite the hook
   and my perspective paragraphs.
3. Storyboard (~54 scenes): populate visual_facts + reference_image on every scene
   that depicts the real structure, and give me the title + a one-sentence
   thumbnail concept with it — no thumbnail concept, no approval.

Save to projects/{{PROJECT_FOLDER}}/. I'll generate the images (with the accuracy
gate before any animation) and record narration myself.
```

### Placeholder key
- `{{VIDEO_TITLE}}` — the working title, e.g. *"The 3,500-Step Staircase Built Into the Earth"*
- `{{ONE_LINE_HOOK}}` — the curiosity angle in a phrase, e.g. *"how India built a 13-story inverted staircase to reach water"*
- `{{CIVILIZATION}}` / `{{ACCENT_HEX}}` — region + its accent from brand_guide §3 (e.g. Indian / `#D4812A`)
- `{{KEY_FACTS_TO_VERIFY}}` — the specific numbers/claims to check (dates, depth, dimensions, mechanism)
- `{{PROJECT_FOLDER}}` — `NNN_shortname`, e.g. `001_chand_baori`

---

## Filled example — Video #1 (Chand Baori)

```
Start a new video for The Engineering Atlas: The 3,500-Step Staircase Built Into the Earth
(how India built a ~13-story inverted staircase to reach the water table).
Use the `the-engineering-atlas-video` skill and follow `brand_guide.md` and `style_card.txt`.
Civilization / accent: Indian (#D4812A).

Work through it in gated steps and STOP for my sign-off at each gate — don't run ahead:
1. Phase 0 — research + fact-check: show me your sources and the key facts
   (build date/era, depth and number of steps, dimensions, the water-table engineering,
   the geometry) so I can verify BEFORE you write anything.
   Also build the reference pack: 5–15 real photos/plans into references/ (with
   source URLs) + references/visual_facts.md (e.g. "three stepped sides, one pavilion
   side", "steps in paired V-flights forming a diamond lattice", "13 visible storeys").
2. Script: draft it in the witness + engineer + wit voice; I'll rewrite the hook
   and my perspective paragraphs.
3. Storyboard (~54 scenes): populate visual_facts + reference_image on every scene
   that depicts the real stepwell, and give me the title + a one-sentence
   thumbnail concept with it — no thumbnail concept, no approval.

Save to projects/001_chand_baori/. I'll generate the images (with the accuracy
gate before any animation) and record narration myself.
```

---

## Short version (once you're comfortable)

After a few videos you can skip the detail — the skill remembers all of it:

```
New Engineering Atlas video: {{VIDEO_TITLE}}. Two-pass storyboard, stop at each gate.
Save to projects/{{PROJECT_FOLDER}}/.
```

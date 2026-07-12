# Chand Baori — Visual Facts (ground truth for the accuracy gate)

*The visually checkable claims about the real structure. These are copied into the storyboard's `visual_facts` fields and are what the [`visual-accuracy-gate`](../../../visual-accuracy-gate/SKILL.md) compares each render against. A claim here must be **verifiable from the reference photos in this folder** — not from prose. If a render violates one of these, it fails the gate and gets a corrective delta re-render before animation.*

Sources for the numbers: `../research_notes.md` (§4–7). Sources for the geometry: the 7 reference photos in this folder.

---

## The reference photos and what each one locks down

| File | Establishes |
|:---|:---|
| `Chand_Baori_perspective_panorama_(July_2022) (1).jpg` | **Master shot.** Three stepped sides + one pavilion side; inverted-pyramid form; green tank at bottom; human figures for scale. Use for all wide/establishing scenes. |
| `Abhaneri-Chand_Baori-12-Stufenbrunnen-2018-gje.jpg` | The **north pavilion** — central multi-tier projecting structure descending toward the water, flanked by two stepped sides. |
| `Chand_Baori_07.jpg` | **Clearest diamond lattice** — paired double-flight V-steps tessellating across ~10+ terraces. Use for step/lattice detail scenes. |
| `Chand_Baori_2.jpg` | **Corner condition** — how two stepped walls meet; also shows the *modern* zig-zag access stair + white railing (a thing to EXCLUDE). |
| `Chand_Baori_2,_Abaneri.jpg` | Oblique — stepped sides meeting the ochre pavilion; the square green tank + railing at the base. |
| `Chand_Baori,Rajasthan.jpg` | The north **arched colonnade** — the cusped-arch verandah gallery (the later, ornate side). |
| `Chand_Baori_04.jpg` | **Waterline close-up** — corbelled/coursed stepped masonry framing the green tank; mortarless block joints. |

---

## Must-be-true facts (the checklist)

**FORM** — Square plan (~35 m per side), an inverted pyramid open to the sky: widest at the top rim, narrowing to a small square water tank at the bottom.

**THREE_SIDES** — Exactly **three** sides are stepped; the **fourth (north) side is a multi-storey pillared pavilion/gallery, NOT steps.** (A render with four stepped sides, or the pavilion on more than one side, is wrong.)

**LATTICE** — The stepped sides are **double flights of steps in a tessellated zig-zag "diamond" lattice** — paired V-flights repeating across the terraces. Ordered, near-fractal geometry; not random, not a single straight staircase.

**DEPTH** — ~**3,500 steps**, about **13 storeys / ~20 m** deep — many stacked horizontal terrace landings. (Use ~20 m, not the overstated "30 m / 100 ft" — see research_notes §5.)

**MORTARLESS** — Dry-laid **mortarless** sandstone: rectangular coursed blocks with visible open joints, **no mortar or cement**.

**PAVILION** — North pavilion: **warm ochre sandstone**, multi-storey, **cusped/pointed arched galleries** with a central projecting multi-tier pavilion stepping down toward the water — visibly more ornate than the plain stepped sides.

**TANK** — A single small **square** water tank at the very bottom center, small relative to the wide top opening.

---

## Must-NOT-appear (exclusions — also checkable)

**NO_MODERN** — No modern **white pipe safety railings** and no **diagonal metal access stair** (both are present in today's photos but are modern additions — omit them in the period/narrative scenes).

**NOT_ROUND** — Square, **not round**. Discrete **steps**, not a smooth ramp. **No arches on the stepped sides** — arches belong only to the north pavilion.

**COLOR** — Stepped sides read cooler grey-brown stone; the north pavilion reads warmer ochre/yellow sandstone. Overall arid, warm-toned. (Real standing water is green/algae — our stylized renders may show it cleaner, but the tank stays square and small.)

---

## What is NOT bound by these facts

Scenes that are **abstract or not the stepwell** carry none of the above — applying them would be a bug:

- The **generic vertical well** (script's deliberate contrast, scenes 11–14) is a plain shaft — it must *not* get stepwell geometry.
- The **map** of Rajasthan, the **arid landscape**, the **water-table strata** cutaway, the pure **diagram panels** (fixed-point-vs-range, gravity arrow, thermometer, endurance emblem), and the **Harshat Mata temple** (a different building, no reference photo) get no `visual_facts`.
- **Cutaway sections *of* the stepwell** get the proportional facts (FORM, DEPTH, TANK) but **no `reference_image`** — they are deliberately clean diagrams, and pushing a 3D photo at them would fight the section look.

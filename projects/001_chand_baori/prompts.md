# Chand Baori — Image & Animation Prompt Sheet

*Generated from `storyboard.json` (Pass 2). Civilization: **Indian** · accent `#D4812A` · style anchor ~0.7 on every image call.*

**Workflow:** (1) generate all 54 stills into `images/` (pass a style anchor every call). (2) For each animated scene, feed its still into Kling with the animation prompt (image-to-video, motion only). (3) `texts` are overlaid later by the assembler — do **not** bake them into images.

---

### Scene 01 — establishing · animated · 7s
- Callouts: "Abhaneri, Rajasthan" (bottom, 3–6s)
- Narration: Every morning, before the sun clears the rooftops of Abhaneri, a woman walks to the edge of a great square pit cut into the earth — and she begins to count.

**IMAGE → `images/scene_01.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [establishing] — wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale. || Subject: a lone village woman as a tiny silhouette at the rim of the vast square stepwell at dawn, the great inverted staircase falling away beneath her, first golden light on parchment-toned sandstone. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: keep the lower third as calm negative space for a callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_01_animated.mp4`** (Kling i2v from the still)
```
very slow push-in toward the woman at the rim; soft dawn haze; faint parallax on the steps below. Duration ~7s. Image-to-video from the generated still images/scene_01.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 02 — detail · animated · 7s
- Callouts: none
- Narration: Down she goes: one step, then another, into a staircase that folds back on itself like a puzzle. And she counts, because the number matters.

**IMAGE → `images/scene_02.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: close isometric of the double-flight steps folding back on themselves, a single tiny silhouette a few steps down. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_02_animated.mp4`** (Kling i2v from the still)
```
slow downward drift following the descent; shadows shift gently. Duration ~7s. Image-to-video from the generated still images/scene_02.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 03 — scale_comparison · static · 13s
- Ken Burns: `zoom_detail` @ (0.5,0.55)
- Callouts: "After the monsoon: ~10 steps" (top, 3–7s); "Peak summer: ~130 steps" (bottom, 8–12s)
- Narration: Yesterday it was thirty steps before her clay pot touched water. In the flush weeks after the monsoon, it was barely ten. By the cruelest stretch of summer, it will be nearly a hundred and thirty.

**IMAGE → `images/scene_03.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [scale_comparison] — the structure beside a scale reference (tiny human silhouettes and/or storey markers), measured diagrammatic framing. || Subject: clean sectional diagram of the stepwell with three faint horizontal waterlines marked high, mid and low, small step-count brackets beside each. || Accent: saffron #D4812A used sparingly as a single highlight on the three waterline markers; everything else stays in the neutral base palette. || Composition: keep the upper third as calm negative space for a callout; keep the lower third as calm negative space for a callout; one clear focal point around (0.5, 0.55) for a detail zoom. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 04 — cross_section · animated · 6s
- Callouts: none
- Narration: She is not climbing down to the water. The water is rising and falling to meet her —

**IMAGE → `images/scene_04.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: cutaway section of the stepwell, the water surface at mid-height, clearly a movable level meeting the steps. || Accent: saffron #D4812A used sparingly as a single highlight on the water surface line; everything else stays in the neutral base palette. || Composition: balanced composition, no callout reserved; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_04_animated.mp4`** (Kling i2v from the still)
```
the water level glides up and down to 'meet' successive steps; subtle surface shimmer. Duration ~6s. Image-to-video from the generated still images/scene_04.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 05 — establishing · animated · 7s
- Callouts: "3,500 steps" (center, 3–6s)
- Narration: — and the staircase, three and a half thousand steps of it, was built, stone by stone, around that one stubborn fact.

**IMAGE → `images/scene_05.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [establishing] — wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale. || Subject: wide establishing view of the entire inverted-pyramid staircase from the rim, the full lattice of steps in golden light. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: keep the central band uncluttered for a centered callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_05_animated.mp4`** (Kling i2v from the still)
```
slow sweeping parallax across the vast step lattice. Duration ~7s. Image-to-video from the generated still images/scene_05.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 06 — detail · static · 7s
- Ken Burns: `zoom_in`
- Callouts: "Why a staircase — not a well?" (center, 1–6s)
- Narration: The question was never how they dug this deep. It's why they built a staircase instead of a well.

**IMAGE → `images/scene_06.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: a single carved step edge sharp in the foreground, the deep well softly falling away behind, an open question implied. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: keep the central band uncluttered for a centered callout; centered composition with headroom for a slow zoom-in. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 07 — title · animated · 5s
- Callouts: "THE ENGINEERING ATLAS" (top, 0.5–4.5s); "Chand Baori" (center, 1.5–4.5s)
- Narration: (Title sting — 2–3s wordmark + topic, music motif only, no narration.)

**IMAGE → `images/scene_07.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [title] — hero-wide composition with generous clean negative space reserved for a title wordmark overlay. || Subject: hero-wide of Chand Baori in golden light with generous clean sky negative space across the top for the wordmark overlay. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: keep the upper third as calm negative space for a callout; keep the central band uncluttered for a centered callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_07_animated.mp4`** (Kling i2v from the still)
```
gentle slow push-in; dust motes catch the light. Duration ~5s. Image-to-video from the generated still images/scene_07.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 08 — map · static · 10s
- Ken Burns: `pan_right`
- Callouts: "Rajasthan" (top, 1–5s); "8th–9th century" (bottom, 6–9s)
- Narration: Here is the constraint the builders of Abhaneri were handed, sometime in the eighth or ninth century. This is Rajasthan — one of the most arid corners of the Indian subcontinent.

**IMAGE → `images/scene_08.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [map] — top-down cartographic schematic, muted regional context, thin technical linework. || Subject: top-down cartographic schematic of arid north-west India / Rajasthan in tan tones, a small marker at Abhaneri near Jaipur, thin technical linework. || Accent: saffron #D4812A used sparingly as a single highlight on the Abhaneri location marker; everything else stays in the neutral base palette. || Composition: keep the upper third as calm negative space for a callout; keep the lower third as calm negative space for a callout; wide horizontal composition with interest spread across the frame for a lateral pan. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 09 — establishing · animated · 10s
- Callouts: none
- Narration: For a few weeks a year the monsoon arrives and the ground drinks its fill. Then, for the long remainder, almost nothing. The rivers thin to ribbons of sand.

**IMAGE → `images/scene_09.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [establishing] — wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale. || Subject: wide arid Rajasthan landscape, a cracked dry riverbed, distant monsoon clouds massing on one horizon. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_09_animated.mp4`** (Kling i2v from the still)
```
monsoon clouds sweep in then pass; ground shifts damp-to-parched, time-lapse feel. Duration ~10s. Image-to-video from the generated still images/scene_09.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 10 — cross_section · animated · 10s
- Callouts: "The water table" (top, 1–5s)
- Narration: And underground, the water table — the depth at which you finally strike water — sinks, slowly and relentlessly, through the dry months.

**IMAGE → `images/scene_10.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: earth cutaway showing the water-table as a distinct boundary between dry upper strata and saturated lower strata. || Accent: saffron #D4812A used sparingly as a single highlight on the water-table line; everything else stays in the neutral base palette. || Composition: keep the upper third as calm negative space for a callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_10_animated.mp4`** (Kling i2v from the still)
```
the water-table boundary sinks slowly downward through the strata. Duration ~10s. Image-to-video from the generated still images/scene_10.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 11 — cross_section · static · 8s
- Ken Burns: `zoom_in`
- Callouts: "A simple well" (bottom, 1–5s)
- Narration: A well is a simple thing: dig a hole to where the water is, drop a rope, done.

**IMAGE → `images/scene_11.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: simple vertical well in section — a narrow shaft to a fixed water level, rope and bucket. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: keep the lower third as calm negative space for a callout; centered composition with headroom for a slow zoom-in. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 12 — cross_section · animated · 8s
- Callouts: none
- Narration: But a well makes one assumption it has no right to make — that the water will stay put. In Abhaneri, it doesn't.

**IMAGE → `images/scene_12.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: the same vertical well, water beginning to drop below the fixed shaft bottom. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_12_animated.mp4`** (Kling i2v from the still)
```
water level slips downward, leaving the bucket over dry air. Duration ~8s. Image-to-video from the generated still images/scene_12.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 13 — cross_section · animated · 9s
- Callouts: "Summer: a dry hole" (bottom, 3–8s)
- Narration: Dig your well down to the high-water mark and, by peak summer, the water has dropped metres below your reach: a dry hole.

**IMAGE → `images/scene_13.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: a well dug to the high-water mark, now a dry empty shaft in cracked summer strata. || Accent: saffron #D4812A used sparingly as a single highlight on a small dry-hole marker at the shaft base; everything else stays in the neutral base palette. || Composition: keep the lower third as calm negative space for a callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_13_animated.mp4`** (Kling i2v from the still)
```
water retreats far below the shaft; faint heat shimmer. Duration ~9s. Image-to-video from the generated still images/scene_13.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 14 — cross_section · animated · 9s
- Callouts: "Monsoon: draw point drowned" (bottom, 3–8s)
- Narration: Dig instead to the summer low, and the monsoon floods the well and drowns your draw point under water you can't stand on.

**IMAGE → `images/scene_14.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: a well dug to the summer low, flooded and overtopped after the monsoon, its draw point submerged. || Accent: saffron #D4812A used sparingly as a single highlight on the drowned draw-point; everything else stays in the neutral base palette. || Composition: keep the lower third as calm negative space for a callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_14_animated.mp4`** (Kling i2v from the still)
```
water rises and floods over the well mouth. Duration ~9s. Image-to-video from the generated still images/scene_14.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 15 — detail · static · 7s
- Ken Burns: `zoom_detail` @ (0.5,0.45)
- Callouts: "A fixed depth loses to a moving target" (center, 1–6s)
- Narration: A single fixed depth always loses to a moving one.

**IMAGE → `images/scene_15.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: a minimalist diagram panel — a single fixed point versus a tall vertical range bracket. || Accent: saffron #D4812A used sparingly as a single highlight on the vertical range bracket; everything else stays in the neutral base palette. || Composition: keep the central band uncluttered for a centered callout; one clear focal point around (0.5, 0.45) for a detail zoom. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 16 — establishing · static · 9s
- Ken Burns: `pan_up`
- Callouts: none
- Narration: That is the real problem at Chand Baori. Not depth. Not even thirst. It's that the thing they needed to reach would not hold still.

**IMAGE → `images/scene_16.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [establishing] — wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale. || Subject: wide of Chand Baori sitting quiet in its landscape, the real problem framed. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; tall vertical composition with detail top-to-bottom for an upward pan. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 17 — cross_section · animated · 7s
- Callouts: "Build for a range, not a point" (top, 1–6s)
- Narration: So they stopped trying to reach a point, and built for a range.

**IMAGE → `images/scene_17.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: concept cutaway — replacing one fixed platform with a continuous stair spanning a full vertical range beside the water column. || Accent: saffron #D4812A used sparingly as a single highlight on the vertical range the stair covers; everything else stays in the neutral base palette. || Composition: keep the upper third as calm negative space for a callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_17_animated.mp4`** (Kling i2v from the still)
```
a highlight sweeps down the whole range, showing every level is covered. Duration ~7s. Image-to-video from the generated still images/scene_17.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 18 — cross_section · animated · 8s
- Callouts: none
- Narration: Picture the shape: an enormous inverted pyramid cut into the ground — square at the mouth, narrowing as it drops.

**IMAGE → `images/scene_18.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: clean section of the inverted pyramid, square mouth narrowing to the tank. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_18_animated.mp4`** (Kling i2v from the still)
```
the section reveals top-down; raking light crosses it. Duration ~8s. Image-to-video from the generated still images/scene_18.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 19 — scale_comparison · static · 12s
- Ken Burns: `zoom_out`
- Callouts: "~35 m per side" (top, 1–5s); "~20 m deep · ~13 storeys" (bottom, 6–11s)
- Narration: Roughly thirty-five metres to a side, and about twenty metres deep; call it thirteen storeys, straight down.

**IMAGE → `images/scene_19.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [scale_comparison] — the structure beside a scale reference (tiny human silhouettes and/or storey markers), measured diagrammatic framing. || Subject: measured section with dimension markers: ~35 m across the mouth and ~20 m / ~13 storeys deep, a tiny human silhouette for scale. || Accent: saffron #D4812A used sparingly as a single highlight on the dimension markers; everything else stays in the neutral base palette. || Composition: keep the upper third as calm negative space for a callout; keep the lower third as calm negative space for a callout; rich full-frame composition that rewards a slow zoom-out. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 20 — detail · static · 10s
- Ken Burns: `pan_right`
- Callouts: "Three sides · double flights of steps" (bottom, 2–8s)
- Narration: Three of its four walls aren't walls at all. They're staircases — double flights of steps zig-zagging down in a tight lattice, landing after landing after landing.

**IMAGE → `images/scene_20.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: three walls of double-flight steps meeting at the corners in the tessellated diamond lattice, isometric. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: keep the lower third as calm negative space for a callout; wide horizontal composition with interest spread across the frame for a lateral pan. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 21 — cross_section · animated · 8s
- Callouts: "Always a step at the waterline" (center, 2–7s)
- Narration: And here is the elegant part. Because the steps cover the entire descent, there is always — always — a step sitting right at the waterline.

**IMAGE → `images/scene_21.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: section with a single step highlighted exactly at the waterline. || Accent: saffron #D4812A used sparingly as a single highlight on the active step at the waterline; everything else stays in the neutral base palette. || Composition: keep the central band uncluttered for a centered callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_21_animated.mp4`** (Kling i2v from the still)
```
as the water level shifts slightly, the highlighted 'active' step tracks to remain at the surface. Duration ~8s. Image-to-video from the generated still images/scene_21.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 22 — cross_section · animated · 8s
- Callouts: "After monsoon: water high" (top, 1–6s)
- Narration: In the flush weeks after the rains, the water is high and you barely climb down at all.

**IMAGE → `images/scene_22.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: section with water HIGH near the top after monsoon, a short descent, tiny silhouette near the rim. || Accent: saffron #D4812A used sparingly as a single highlight on the high waterline; everything else stays in the neutral base palette. || Composition: keep the upper third as calm negative space for a callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_22_animated.mp4`** (Kling i2v from the still)
```
water sits high; the silhouette barely steps down to reach it. Duration ~8s. Image-to-video from the generated still images/scene_22.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 23 — cross_section · animated · 8s
- Callouts: "Peak summer: water low" (top, 1–6s)
- Narration: In the heart of summer, the water has retreated deep into the earth, and you walk down, and down, to meet it.

**IMAGE → `images/scene_23.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: section with water LOW near the base in high summer, a long descent, tiny silhouette walking far down. || Accent: saffron #D4812A used sparingly as a single highlight on the low waterline; everything else stays in the neutral base palette. || Composition: keep the upper third as calm negative space for a callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_23_animated.mp4`** (Kling i2v from the still)
```
the silhouette descends deep toward a low water level; dust in low light. Duration ~8s. Image-to-video from the generated still images/scene_23.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 24 — cross_section · animated · 9s
- Callouts: none
- Narration: The building never moves. The water moves. And the staircase quietly guarantees that wherever the water is, a dry footing is waiting for you exactly there.

**IMAGE → `images/scene_24.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: section showing the building perfectly fixed while only the water surface moves up and down. || Accent: saffron #D4812A used sparingly as a single highlight on the moving water surface; everything else stays in the neutral base palette. || Composition: balanced composition, no callout reserved; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_24_animated.mp4`** (Kling i2v from the still)
```
structure dead still; only the water level glides up and down. Duration ~9s. Image-to-video from the generated still images/scene_24.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 25 — detail · static · 8s
- Ken Burns: `zoom_detail` @ (0.5,0.5)
- Callouts: "Laid without mortar" (bottom, 2–7s)
- Narration: There's a second cleverness in the stonework, and you'd miss it if you weren't looking. The blocks are laid without mortar — nothing binding them.

**IMAGE → `images/scene_25.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: extreme close isometric of dry-laid sandstone blocks with open mortarless joints, precise fit. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: keep the lower third as calm negative space for a callout; one clear focal point around (0.5, 0.5) for a detail zoom. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 26 — cross_section · animated · 10s
- Callouts: none
- Narration: That sounds like a shortcut. It's the opposite. A mortarless wall lets groundwater seep through the stone into the tank from every side,

**IMAGE → `images/scene_26.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: cutaway of the mortarless wall with fine groundwater threading through the joints into the tank from all sides. || Accent: saffron #D4812A used sparingly as a single highlight on the seeping water threads; everything else stays in the neutral base palette. || Composition: balanced composition, no callout reserved; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_26_animated.mp4`** (Kling i2v from the still)
```
thin water threads trickle inward through the joints; the tank slowly fills. Duration ~10s. Image-to-video from the generated still images/scene_26.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 27 — cross_section · animated · 6s
- Callouts: none
- Narration: so the well fills from the whole body of earth around it, not just the bottom.

**IMAGE → `images/scene_27.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: section of the whole tank filling from the surrounding earth, not just the base. || Accent: saffron #D4812A used sparingly as a single highlight on the inflow around the perimeter; everything else stays in the neutral base palette. || Composition: balanced composition, no callout reserved; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_27_animated.mp4`** (Kling i2v from the still)
```
water ingress glows around the full perimeter, level rising evenly. Duration ~6s. Image-to-video from the generated still images/scene_27.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 28 — detail · static · 8s
- Ken Burns: `zoom_in`
- Callouts: "Flexes — doesn't shatter" (bottom, 2–7s)
- Narration: And a wall with no rigid mortar can shift a little without shattering — one reason stepwells have ridden out earthquakes that flattened prouder buildings.

**IMAGE → `images/scene_28.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: the mortarless wall mid-tremor, blocks shifted a hair but holding, no cracks. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: keep the lower third as calm negative space for a callout; centered composition with headroom for a slow zoom-in. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 29 — detail · static · 7s
- Ken Burns: `zoom_out`
- Callouts: "No pumps. No power. Just gravity." (center, 1–6s)
- Narration: No pumps. No moving parts. No power source but gravity and the seasons.

**IMAGE → `images/scene_29.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: a spare diagrammatic emblem — no pump, no gear, a single downward gravity arrow over the well. || Accent: saffron #D4812A used sparingly as a single highlight on the gravity arrow; everything else stays in the neutral base palette. || Composition: keep the central band uncluttered for a centered callout; rich full-frame composition that rewards a slow zoom-out. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 30 — establishing · static · 6s
- Ken Burns: `zoom_in`
- Callouts: none
- Narration: The machine has exactly one instruction, and it has never once stopped obeying it.

**IMAGE → `images/scene_30.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [establishing] — wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale. || Subject: wide of the whole machine at rest, one quiet instruction fulfilled. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; centered composition with headroom for a slow zoom-in. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 31 — establishing · animated · 8s
- Callouts: "3,500 steps" (center, 3–7s)
- Narration: Stand at the rim and the scale finally lands. Three thousand five hundred steps.

**IMAGE → `images/scene_31.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [establishing] — wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale. || Subject: standing-at-the-rim view of the immense step lattice, the full scale landing. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: keep the central band uncluttered for a centered callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_31_animated.mp4`** (Kling i2v from the still)
```
slow parallax as the eye falls into the lattice. Duration ~8s. Image-to-video from the generated still images/scene_31.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 32 — detail · static · 10s
- Ken Burns: `pan_left`
- Callouts: "13 storeys" (top, 1–5s)
- Narration: Thirteen storeys of them, folded into that hypnotic diamond geometry that's made Chand Baori one of the most photographed staircases on Earth —

**IMAGE → `images/scene_32.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: sweeping close of the hypnotic diamond step geometry, the most-photographed angle. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: keep the upper third as calm negative space for a callout; wide horizontal composition with interest spread across the frame for a lateral pan. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 33 — detail · static · 8s
- Ken Burns: `zoom_detail` @ (0.5,0.5)
- Callouts: ""a mathematical marvel"" (center, 1–6s)
- Narration: a pattern so exact that one historian simply called it 'a mathematical marvel.'

**IMAGE → `images/scene_33.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: tight on the mathematically exact lattice, near-fractal repetition of steps. || Accent: saffron #D4812A used sparingly as a single highlight on a single highlighted lattice module; everything else stays in the neutral base palette. || Composition: keep the central band uncluttered for a centered callout; one clear focal point around (0.5, 0.5) for a detail zoom. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 34 — establishing · static · 10s
- Ken Burns: `pan_up`
- Callouts: "North face: gallery + royal pavilion" (bottom, 2–8s)
- Narration: The fourth side — the north — breaks the rhythm: a tall pillared gallery rising several storeys, with a pavilion where the local rulers could sit above the water.

**IMAGE → `images/scene_34.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [establishing] — wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale. || Subject: the north face — a tall multi-storey pillared gallery and royal pavilion rising opposite the stepped walls. || Accent: saffron #D4812A used sparingly as a single highlight on the pavilion niche; everything else stays in the neutral base palette. || Composition: keep the lower third as calm negative space for a callout; tall vertical composition with detail top-to-bottom for an upward pan. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 35 — detail · animated · 8s
- Callouts: none
- Narration: Because this was never only waterworks. Descend those steps on a blistering afternoon and something else happens — the air cools.

**IMAGE → `images/scene_35.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: a tiny silhouette descending into the shaded lower levels where the light cools. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_35_animated.mp4`** (Kling i2v from the still)
```
slow descent; light temperature shifts from warm to cool shade. Duration ~8s. Image-to-video from the generated still images/scene_35.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 36 — scale_comparison · static · 8s
- Ken Burns: `zoom_in`
- Callouts: "5–6 °C cooler at the bottom" (center, 1–6s)
- Narration: At the bottom it holds a temperature five to six degrees cooler than the surface.

**IMAGE → `images/scene_36.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [scale_comparison] — the structure beside a scale reference (tiny human silhouettes and/or storey markers), measured diagrammatic framing. || Subject: diagram comparing hot surface air and cool base, a small thermometer motif at the bottom of the shaft. || Accent: saffron #D4812A used sparingly as a single highlight on the cool-base marker; everything else stays in the neutral base palette. || Composition: keep the central band uncluttered for a centered callout; centered composition with headroom for a slow zoom-in. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 37 — establishing · static · 8s
- Ken Burns: `pan_up`
- Callouts: none
- Narration: So the well was also a refuge: a shaded room at the bottom of the heat, where the village gathered,

**IMAGE → `images/scene_37.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [establishing] — wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale. || Subject: the shaded tank level as a communal refuge, tiny silhouettes gathered by the water. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; tall vertical composition with detail top-to-bottom for an upward pan. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 38 — detail · static · 8s
- Ken Burns: `pan_right`
- Callouts: "Harshat Mata temple" (bottom, 2–7s)
- Narration: and where — beside a well named for a king — a temple to Harshat Mata, the goddess of joy, still stands.

**IMAGE → `images/scene_38.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: the Harshat Mata temple beside the well, a carved sandstone shrine. || Accent: saffron #D4812A used sparingly as a single highlight on a small shrine highlight; everything else stays in the neutral base palette. || Composition: keep the lower third as calm negative space for a callout; wide horizontal composition with interest spread across the frame for a lateral pan. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 39 — detail · animated · 8s
- Callouts: none
- Narration: And for most of its life, the people who kept this place alive were women, walking these steps at dawn and dusk with pots on their hips,

**IMAGE → `images/scene_39.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: tiny silhouettes of women descending the steps at dawn with round water pots. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_39_animated.mp4`** (Kling i2v from the still)
```
figures move gently down the steps; long soft shadows lengthen. Duration ~8s. Image-to-video from the generated still images/scene_39.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 40 — establishing · static · 7s
- Ken Burns: `zoom_out`
- Callouts: none
- Narration: and travellers resting in the cool before the next stretch of road.

**IMAGE → `images/scene_40.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [establishing] — wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale. || Subject: travellers and pilgrims resting in the cool gallery, a calm wide. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; rich full-frame composition that rewards a slow zoom-out. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 41 — detail · static · 6s
- Ken Burns: `zoom_in`
- Callouts: none
- Narration: Here's what I think most people walk straight past when they see those famous photographs.

**IMAGE → `images/scene_41.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: a framed 'famous photograph' vignette of the lattice, inviting a second look. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; centered composition with headroom for a slow zoom-in. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 42 — cross_section · animated · 9s
- Callouts: "The staircase IS the machine" (center, 2–8s)
- Narration: We look at Chand Baori and see a staircase — a beautiful, punishing way down to the water. But the staircase isn't the route to the machine. The staircase is the machine.

**IMAGE → `images/scene_42.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: a reveal that reframes the staircase itself as the machine — the steps read as the working mechanism. || Accent: saffron #D4812A used sparingly as a single highlight on the machine-active steps; everything else stays in the neutral base palette. || Composition: keep the central band uncluttered for a centered callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_42_animated.mp4`** (Kling i2v from the still)
```
a highlight ripples across every step so the whole stair reads as one mechanism. Duration ~9s. Image-to-video from the generated still images/scene_42.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 43 — cross_section · animated · 11s
- Callouts: "A moving-boundary problem" (top, 1–6s)
- Narration: A vertical well solves a fixed-depth problem. Chand Baori solves a moving-boundary problem — a water surface that swings up and down through the year — and it solves it with nothing but geometry.

**IMAGE → `images/scene_43.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: side-by-side section — a fixed-depth well versus the range-spanning stepwell against a swinging water column. || Accent: saffron #D4812A used sparingly as a single highlight on the swinging water column; everything else stays in the neutral base palette. || Composition: keep the upper third as calm negative space for a callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_43_animated.mp4`** (Kling i2v from the still)
```
the water column swings up and down; the fixed well fails while the stepwell keeps tracking it. Duration ~11s. Image-to-video from the generated still images/scene_43.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 44 — cross_section · animated · 10s
- Callouts: "Every step = a potential waterline" (bottom, 2–8s)
- Narration: Every one of those three and a half thousand steps is a potential waterline, so the structure automatically offers a fresh, dry edge at whatever height the water happens to be that week.

**IMAGE → `images/scene_44.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: section with many faint waterline candidates marked across the entire descent, each a potential surface. || Accent: saffron #D4812A used sparingly as a single highlight on the array of potential waterlines; everything else stays in the neutral base palette. || Composition: keep the lower third as calm negative space for a callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_44_animated.mp4`** (Kling i2v from the still)
```
the waterline candidates light up one after another down the descent. Duration ~10s. Image-to-video from the generated still images/scene_44.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 45 — scale_comparison · static · 9s
- Ken Burns: `zoom_out`
- Callouts: "Zero energy · 1,000+ years" (center, 1–7s)
- Narration: It's an adaptive interface, drawn in stone, running on zero energy — and it's been running for over a thousand years.

**IMAGE → `images/scene_45.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [scale_comparison] — the structure beside a scale reference (tiny human silhouettes and/or storey markers), measured diagrammatic framing. || Subject: a quiet endurance emblem — 'zero energy, over a thousand years' as a diagrammatic motif of the well enduring the seasons. || Accent: saffron #D4812A used sparingly as a single highlight on the endurance marker; everything else stays in the neutral base palette. || Composition: keep the central band uncluttered for a centered callout; rich full-frame composition that rewards a slow zoom-out. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 46 — detail · static · 6s
- Ken Burns: `pan_left`
- Callouts: none
- Narration: We tend to file buildings like this under 'beautiful' and move on.

**IMAGE → `images/scene_46.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: a merely-'pretty' framing of the steps, about to be reread as function. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; wide horizontal composition with interest spread across the frame for a lateral pan. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 47 — detail · static · 8s
- Ken Burns: `zoom_detail` @ (0.5,0.5)
- Callouts: "The lattice is doing arithmetic" (center, 1–6s)
- Narration: But the beauty is a side effect. The lattice is doing arithmetic.

**IMAGE → `images/scene_47.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: the lattice faintly overlaid with implied geometry/arithmetic lines — beauty as a byproduct. || Accent: saffron #D4812A used sparingly as a single highlight on the geometry lines; everything else stays in the neutral base palette. || Composition: keep the central band uncluttered for a centered callout; one clear focal point around (0.5, 0.5) for a detail zoom. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 48 — establishing · static · 7s
- Ken Burns: `zoom_in`
- Callouts: none
- Narration: Which brings us back to the woman at the top of the steps, counting.

**IMAGE → `images/scene_48.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [establishing] — wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale. || Subject: back to the woman at the rim, smaller now in a familiar wide composition. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; centered composition with headroom for a slow zoom-in. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 49 — detail · static · 10s
- Ken Burns: `zoom_in`
- Callouts: none
- Narration: She doesn't know the phrase 'hydraulic gradient,' and she doesn't need it. She has something better: a machine her ancestors cut into the ground before anyone thought to write down its date —

**IMAGE → `images/scene_49.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: close on the woman's hands and pot at a worn step edge, generations of wear in the stone. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; centered composition with headroom for a slow zoom-in. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 50 — cross_section · animated · 8s
- Callouts: none
- Narration: one that has met every generation of her family at the water's edge, wherever that edge happened to fall.

**IMAGE → `images/scene_50.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [cross_section] — architectural cutaway/section — ground sliced open to reveal earth strata and the water-table line, the stepwell shown in clean profile, educational-diagram clarity. || Subject: section showing successive generations meeting the water at different seasonal levels over time. || Accent: saffron #D4812A used sparingly as a single highlight on the meeting point at the waterline; everything else stays in the neutral base palette. || Composition: balanced composition, no callout reserved; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_50_animated.mp4`** (Kling i2v from the still)
```
the waterline and a tiny figure shift across seasons, always meeting at a step. Duration ~8s. Image-to-video from the generated still images/scene_50.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 51 — detail · animated · 8s
- Callouts: "Thirty steps this morning" (bottom, 2–7s)
- Narration: This morning it's thirty steps. Tomorrow, maybe thirty-one. And the staircase will be there for every one of them.

**IMAGE → `images/scene_51.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [detail] — tight isometric close-up on a single element, shallow depth, texture and craft emphasis. || Subject: the woman at 'thirty steps' today, one active step subtly marked. || Accent: saffron #D4812A used sparingly as a single highlight on the marked active step; everything else stays in the neutral base palette. || Composition: keep the lower third as calm negative space for a callout; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_51_animated.mp4`** (Kling i2v from the still)
```
a quiet counting feel; light advances one step down. Duration ~8s. Image-to-video from the generated still images/scene_51.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 52 — establishing · animated · 9s
- Callouts: none
- Narration: That's the quiet genius of Chand Baori. Not that they dug deep — that they built something which never has to be told where the water went.

**IMAGE → `images/scene_52.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [establishing] — wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale. || Subject: a grand wide of Chand Baori, the quiet genius of it, timeless in golden light. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; compose as a still starting-frame that anticipates the described motion (leave room for it to move). || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```
**ANIMATION → `clips/scene_52_animated.mp4`** (Kling i2v from the still)
```
slow majestic parallax pull-back; dust motes, warm light. Duration ~9s. Image-to-video from the generated still images/scene_52.png — add motion only, do NOT restyle; keep the isometric look, palette and saffron accent locked to the starting frame.
```

### Scene 53 — establishing · static · 8s
- Ken Burns: `zoom_out`
- Callouts: none
- Narration: Built to last — or built to teach us why it didn't. I'll see you in the next one.

**IMAGE → `images/scene_53.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [establishing] — wide establishing view, the full stepwell in frame with sky/horizon context and a strong sense of scale. || Subject: a final calm wide at golden hour, reflective sign-off mood. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: balanced composition, no callout reserved; rich full-frame composition that rewards a slow zoom-out. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

### Scene 54 — outro · static · 6s
- Ken Burns: `zoom_in`
- Callouts: "Subscribe — The Engineering Atlas" (center, 0.5–5.5s)
- Narration: (Outro card — subscribe + next-video thumbnail, no narration.)

**IMAGE → `images/scene_54.png`**
```
Isometric flat-design technical illustration. Clean vector aesthetic, warm parchment background (#F5F0E8), precise geometric lines, charcoal dark elements (#2C2C2C), cream light elements (#FAF7F2). Architectural cross-section / cutaway style where relevant. Warm golden-hour ambient lighting with soft directional shadows. No humans visible (or tiny silhouettes for scale only). No text in image. High architectural precision. Educational diagram aesthetic. Quietly dramatic, awe-inspiring mood. || Scene [outro] — calm, receding wide composition with clean negative space reserved for a subscribe card overlay. || Subject: a receding wide of the stepwell with clean central negative space reserved for the subscribe card overlay. || Neutral base palette only (no saffron this frame; the #D4812A accent is reserved for key scenes). || Composition: keep the central band uncluttered for a centered callout; centered composition with headroom for a slow zoom-in. || Consistency: pass a style anchor from assets/style_anchors/ (~0.7 strength); keep palette, line-weight and isometric angle identical across all scenes.
```

import { Composition } from 'remotion';
import './brand/fonts'; // module-level font loads — must be imported once, here
import { Diagram } from './families/Diagram';
import { MapRoute } from './families/MapRoute';
import { PlatePush } from './families/PlatePush';
import { TitleCard } from './scenes/TitleCard';
import { Scene24 } from './scenes/Scene24';
import { Scene31 } from './scenes/Scene31';
import { Scene44 } from './scenes/Scene44';
import { Scene55 } from './scenes/Scene55';
import { Scene59 } from './scenes/Scene59';
import { Scene63 } from './scenes/Scene63';
import { Scene69 } from './scenes/Scene69';
import { Scene73 } from './scenes/Scene73';
import { Scene77 } from './scenes/Scene77';

/**
 * Depth First — composition registry.
 *
 * s001 · Why AI Is So Expensive to Run — 77 scenes, 26,652 frames.
 *
 * Generated once from projects/s001_ai_physical_cost/storyboard.json (remotion-director,
 * pass 7) and HAND-EDITABLE from here. Studio's Props editor writes visual edits back into
 * the `defaultProps` literals below, so do not regenerate this file over the top of them.
 *
 * Frame spec is fixed by brand_guide_software.md §5: 3840×2160 @ 30fps, every scene
 * rendered with 30 frames of handles at BOTH ends (Premiere conform stays trim-only).
 * durationInFrames = round(seconds × 30) + 60 — this pass owns that single conversion.
 * Content therefore starts at frame 30, which is why entry animations are offset by it.
 */

export const RemotionRoot: React.FC = () => {
  return (
    <>

      {/* scene_01 · detail · the hook: the weightlessness the whole video will dismantle */}
      <Composition
        id="scene-01"
        component={PlatePush}
        durationInFrames={270}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_01.png',
          push: 3 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_02 · scale_comparison · plant the honest small number so the payoff can't be called a ch */}
      <Composition
        id="scene-02"
        component={Diagram}
        durationInFrames={357}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['0.3 Wh — one answer', '2 seconds of a microwave'],
          layout: 'bars' as const,
          weights: [0.54, 1.0],
        }}
      />

      {/* scene_03 · establishing · state the contract: a question the viewer now wants answered */}
      <Composition
        id="scene-03"
        component={PlatePush}
        durationInFrames={309}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_03.png',
          push: 0 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_04 · establishing · the tease — name the reactor without explaining it */}
      <Composition
        id="scene-04"
        component={PlatePush}
        durationInFrames={297}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_04.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_05 · narrative · make it human and specific before it becomes industrial */}
      <Composition
        id="scene-05"
        component={PlatePush}
        durationInFrames={345}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_05.png',
          push: 3 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_06 · narrative · breadth — this is everyone, not a niche */}
      <Composition
        id="scene-06"
        component={PlatePush}
        durationInFrames={384}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_06.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_07 · detail · name the illusion explicitly — the thesis in one word: weightles */}
      <Composition
        id="scene-07"
        component={PlatePush}
        durationInFrames={369}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_07.png',
          push: 3 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_08 · scale_comparison · concede the honest point up front — earns trust for the escalati */}
      <Composition
        id="scene-08"
        component={Diagram}
        durationInFrames={309}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['one question', 'cost: ~nothing'],
          layout: 'row' as const,
        }}
      />

      {/* scene_09 · map · the pivot: singular to fleet. The whole argument turns here */}
      <Composition
        id="scene-09"
        component={MapRoute}
        durationInFrames={309}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          drawOnFrames: 16,
          label: '~1,000,000,000 / day',
        }}
      />

      {/* scene_10 · cross_section · the wire — introduce the through-line the video literally follow */}
      <Composition
        id="scene-10"
        component={Diagram}
        durationInFrames={309}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['your question', '→ something enormous'],
          layout: 'row' as const,
        }}
      />

      {/* scene_11 · establishing · state the method: we follow one query backwards */}
      <Composition
        id="scene-11"
        component={PlatePush}
        durationInFrames={396}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_11.png',
          push: 0 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_12 · title · title card — Why AI Is So Expensive to Run */}
      <Composition
        id="scene-12"
        component={TitleCard}
        durationInFrames={210}
        fps={30}
        width={3840}
        height={2160}
      />

      {/* scene_13 · cross_section · deliver the hero small number cleanly and without spin */}
      <Composition
        id="scene-13"
        component={Diagram}
        durationInFrames={396}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['0.3 Wh'],
          layout: 'row' as const,
        }}
      />

      {/* scene_14 · scale_comparison · anchor 0.3 Wh to a body-scale referent, then raise the myth */}
      <Composition
        id="scene-14"
        component={PlatePush}
        durationInFrames={357}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_14.png',
          push: 3 as const,
          direction: 'in' as const,
          label: 'a couple of minutes of this',
        }}
      />

      {/* scene_15 · scale_comparison · correct the myth generously — credit the engineers, no scolding */}
      <Composition
        id="scene-15"
        component={Diagram}
        durationInFrames={369}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['2023 estimate', 'today — ~10× lower'],
          layout: 'bars' as const,
          weights: [1.0, 0.1],
        }}
      />

      {/* scene_16 · cross_section · show the number is a floor, not a ceiling */}
      <Composition
        id="scene-16"
        component={Diagram}
        durationInFrames={396}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['0.3 Wh', '~2.5 Wh', '~40 Wh'],
          layout: 'bars' as const,
          weights: [0.0075, 0.0625, 1.0],
        }}
      />

      {/* scene_17 · scale_comparison · the 100x spread — the first real jolt */}
      <Composition
        id="scene-17"
        component={PlatePush}
        durationInFrames={297}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_17.png',
          push: 5 as const,
          direction: 'in' as const,
          label: 'one hard question',
        }}
      />

      {/* scene_18 · detail · re-frame: the thesis is not per-query guilt */}
      <Composition
        id="scene-18"
        component={Diagram}
        durationInFrames={345}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['0.3'],
          layout: 'row' as const,
        }}
      />

      {/* scene_19 · map · hand off to the ladder — 'follow the wire' is the spine cue */}
      <Composition
        id="scene-19"
        component={MapRoute}
        durationInFrames={384}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          drawOnFrames: 16,
          label: 'follow the wire',
        }}
      />

      {/* scene_20 · establishing · first scale-shock: the query's destination is a building */}
      <Composition
        id="scene-20"
        component={PlatePush}
        durationInFrames={384}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_20.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_21 · detail · hero the chip — the physical object doing the thinking */}
      <Composition
        id="scene-21"
        component={PlatePush}
        durationInFrames={345}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_21.png',
          push: 4 as const,
          direction: 'in' as const,
          label: 'NVIDIA H100 · ~700 W',
        }}
      />

      {/* scene_22 · cross_section · one chip is already absurd — and it is never one */}
      <Composition
        id="scene-22"
        component={PlatePush}
        durationInFrames={309}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_22.png',
          push: 4 as const,
          direction: 'in' as const,
          label: '×8 per tray',
        }}
      />

      {/* scene_23 · scale_comparison · convert watts into homes — the unit the viewer feels */}
      <Composition
        id="scene-23"
        component={Diagram}
        durationInFrames={333}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['one tray ≈ 10 kW', '≈ 5 homes'],
          layout: 'bars' as const,
          weights: [1.0, 1.0],
        }}
      />

      {/* scene_24 · scale_comparison · the multiply: rack to hall to town */}
      <Composition
        id="scene-24"
        component={Scene24}
        durationInFrames={333}
        fps={30}
        width={3840}
        height={2160}
      />

      {/* scene_25 · establishing · name the concealment — the emotional core of the video */}
      <Composition
        id="scene-25"
        component={PlatePush}
        durationInFrames={369}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_25.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_26 · cross_section · the physics turn that opens the water beat */}
      <Composition
        id="scene-26"
        component={Diagram}
        durationInFrames={396}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['electricity in', 'heat out'],
          layout: 'row' as const,
        }}
      />

      {/* scene_27 · establishing · set up cost #2 as inevitable, not incidental */}
      <Composition
        id="scene-27"
        component={PlatePush}
        durationInFrames={369}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_27.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_28 · establishing · why water — it is a heat problem, not a thirst problem */}
      <Composition
        id="scene-28"
        component={PlatePush}
        durationInFrames={357}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_28.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_29 · detail · the on-site number, honestly small */}
      <Composition
        id="scene-29"
        component={PlatePush}
        durationInFrames={321}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_29.png',
          push: 3 as const,
          direction: 'in' as const,
          label: 'a few mL — one answer',
        }}
      />

      {/* scene_30 · map · the misdirection: the water is upstream, not here */}
      <Composition
        id="scene-30"
        component={MapRoute}
        durationInFrames={282}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          drawOnFrames: 16,
          label: 'most of the water is NOT here',
        }}
      />

      {/* scene_31 · establishing · the grid's own water cost — the hidden second boundary */}
      <Composition
        id="scene-31"
        component={Scene31}
        durationInFrames={408}
        fps={30}
        width={3840}
        height={2160}
      />

      {/* scene_32 · map · connect the two boundaries into one chain */}
      <Composition
        id="scene-32"
        component={MapRoute}
        durationInFrames={345}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          drawOnFrames: 16,
          label: 'power →',
        }}
      />

      {/* scene_33 · scale_comparison · deliver ~15 mL and immediately flag its uncertainty */}
      <Composition
        id="scene-33"
        component={Diagram}
        durationInFrames={396}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['on-site: a few mL', 'grid: ~10 mL', '≈ 15 mL'],
          layout: 'bars' as const,
          weights: [0.33, 0.67, 1.0],
        }}
      />

      {/* scene_34 · detail · the humility beat — credibility with the expert viewer */}
      <Composition
        id="scene-34"
        component={Diagram}
        durationInFrames={321}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['≈ 15 mL', '± depends on site & cooling'],
          layout: 'row' as const,
        }}
      />

      {/* scene_35 · narrative · re-arm the fleet refrain and hand off to silicon */}
      <Composition
        id="scene-35"
        component={PlatePush}
        durationInFrames={321}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_35.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_36 · detail · reframe the chip from component to artefact */}
      <Composition
        id="scene-36"
        component={PlatePush}
        durationInFrames={333}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_36.png',
          push: 3 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_37 · cross_section · the precision — awe, not statistics */}
      <Composition
        id="scene-37"
        component={Diagram}
        durationInFrames={321}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['a human hair', 'a virus', 'the features on this chip'],
          layout: 'row' as const,
        }}
      />

      {/* scene_38 · establishing · the ASML fact — a genuine jaw-drop, kept about the machine */}
      <Composition
        id="scene-38"
        component={PlatePush}
        durationInFrames={321}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_38.png',
          push: 4 as const,
          direction: 'in' as const,
          label: 'one manufacturer on Earth',
        }}
      />

      {/* scene_39 · establishing · the fab as its own industrial appetite */}
      <Composition
        id="scene-39"
        component={PlatePush}
        durationInFrames={396}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_39.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_40 · scale_comparison · the fab's power AND water in one line — the ladder's 4th rung */}
      <Composition
        id="scene-40"
        component={Diagram}
        durationInFrames={309}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['the power of a small city', 'the water of a small town'],
          layout: 'bars' as const,
          weights: [0.85, 0.7],
        }}
      />

      {/* scene_41 · scale_comparison · make the volume physical */}
      <Composition
        id="scene-41"
        component={Diagram}
        durationInFrames={396}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['millions of gallons — every day'],
          layout: 'row' as const,
        }}
      />

      {/* scene_42 · map · TSMC vs countries — then the wit line that lands the beat */}
      <Composition
        id="scene-42"
        component={MapRoute}
        durationInFrames={396}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          drawOnFrames: 16,
          label: 'one company',
        }}
      />

      {/* scene_43 · scale_comparison · summarise the three costs and cue the multiply */}
      <Composition
        id="scene-43"
        component={Diagram}
        durationInFrames={396}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['build', 'cool', 'make', '× ?'],
          layout: 'row' as const,
        }}
      />

      {/* scene_44 · map · recap the ladder and return to the spine */}
      <Composition
        id="scene-44"
        component={Scene44}
        durationInFrames={345}
        fps={30}
        width={3840}
        height={2160}
      />

      {/* scene_45 · scale_comparison · pose the aggregate question in the viewer's own terms */}
      <Composition
        id="scene-45"
        component={Diagram}
        durationInFrames={309}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['one query', '× 1,000,000,000 / day'],
          layout: 'bars' as const,
          weights: [0.001, 1.0],
        }}
      />

      {/* scene_46 · cross_section · growth rate — the number that makes it a trend, not a snapshot */}
      <Composition
        id="scene-46"
        component={Diagram}
        durationInFrames={408}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['data centres +15%/yr', 'everything else'],
          layout: 'bars' as const,
          weights: [1.0, 0.24],
        }}
      />

      {/* scene_47 · map · Ireland: the abstraction becomes a country */}
      <Composition
        id="scene-47"
        component={MapRoute}
        durationInFrames={384}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          drawOnFrames: 16,
          label: '23% of the national grid',
        }}
      />

      {/* scene_48 · scale_comparison · make 23% concrete: halls instead of homes */}
      <Composition
        id="scene-48"
        component={Diagram}
        durationInFrames={357}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['homes', 'server halls', '+518% in a decade'],
          layout: 'row' as const,
        }}
      />

      {/* scene_49 · map · a state had to say no — the first hard consequence */}
      <Composition
        id="scene-49"
        component={MapRoute}
        durationInFrames={345}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          drawOnFrames: 16,
          label: 'no new connections',
        }}
      />

      {/* scene_50 · scale_comparison · the planetary figure, framed as projection */}
      <Composition
        id="scene-50"
        component={Diagram}
        durationInFrames={369}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['~3% of all power humanity generates', 'by 2030'],
          layout: 'bars' as const,
          weights: [0.03, 1.0],
        }}
      />

      {/* scene_51 · scale_comparison · beat heavy industry — the comparison that lands hardest */}
      <Composition
        id="scene-51"
        component={PlatePush}
        durationInFrames={321}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_51.png',
          push: 5 as const,
          direction: 'in' as const,
          label: 'aluminium · steel · cement · chemicals',
        }}
      />

      {/* scene_52 · cross_section · set up the training-vs-inference inversion */}
      <Composition
        id="scene-52"
        component={Diagram}
        durationInFrames={369}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['training — once'],
          layout: 'row' as const,
        }}
      />

      {/* scene_53 · scale_comparison · the inversion: running it beat building it */}
      <Composition
        id="scene-53"
        component={Diagram}
        durationInFrames={321}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['training — once', 'running it — forever'],
          layout: 'bars' as const,
          weights: [0.3, 1.0],
        }}
      />

      {/* scene_54 · establishing · the hinge into the climax */}
      <Composition
        id="scene-54"
        component={PlatePush}
        durationInFrames={297}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_54.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_55 · establishing · the reveal — a name that carries its own dread */}
      <Composition
        id="scene-55"
        component={Scene55}
        durationInFrames={420}
        fps={30}
        width={3840}
        height={2160}
      />

      {/* scene_56 · narrative · the history, precisely — Unit 2 melted, Unit 1 survived */}
      <Composition
        id="scene-56"
        component={PlatePush}
        durationInFrames={345}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_56.png',
          push: 4 as const,
          direction: 'in' as const,
          label: '1979',
        }}
      />

      {/* scene_57 · detail · the death of the plant — the low before the turn */}
      <Composition
        id="scene-57"
        component={PlatePush}
        durationInFrames={297}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_57.png',
          push: 3 as const,
          direction: 'in' as const,
          label: '2019 — shut down',
        }}
      />

      {/* scene_58 · narrative · the turn — resurrection, and for whom */}
      <Composition
        id="scene-58"
        component={PlatePush}
        durationInFrames={357}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_58.png',
          push: 4 as const,
          direction: 'in' as const,
          label: '2024 — restart',
        }}
      />

      {/* scene_59 · scale_comparison · the hero number the thumbnail promised: 835 MW */}
      <Composition
        id="scene-59"
        component={Scene59}
        durationInFrames={357}
        fps={30}
        width={3840}
        height={2160}
      />

      {/* scene_60 · detail · the cost, then convert MW into something human */}
      <Composition
        id="scene-60"
        component={Diagram}
        durationInFrames={345}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['20-year agreement', '> $1 billion'],
          layout: 'row' as const,
        }}
      />

      {/* scene_61 · scale_comparison · 800k homes, re-routed to one customer — the asymmetry made visua */}
      <Composition
        id="scene-61"
        component={PlatePush}
        durationInFrames={309}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_61.png',
          push: 5 as const,
          direction: 'in' as const,
          label: '~750,000 homes',
        }}
      />

      {/* scene_62 · detail · close the loop opened in scene 3 */}
      <Composition
        id="scene-62"
        component={PlatePush}
        durationInFrames={270}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_62.png',
          push: 3 as const,
          direction: 'in' as const,
          label: 'one question',
        }}
      />

      {/* scene_63 · establishing · THE title payoff — held on the towers, one continuous move */}
      <Composition
        id="scene-63"
        component={Scene63}
        durationInFrames={432}
        fps={30}
        width={3840}
        height={2160}
      />

      {/* scene_64 · detail · hand the honest counter-argument to the viewer, unprompted */}
      <Composition
        id="scene-64"
        component={PlatePush}
        durationInFrames={420}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_64.png',
          push: 3 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_65 · scale_comparison · concede fully, then turn */}
      <Composition
        id="scene-65"
        component={Diagram}
        durationInFrames={396}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          labels: ['one query', '≈ a few seconds of TV'],
          layout: 'bars' as const,
          weights: [0.8, 1.0],
        }}
      />

      {/* scene_66 · map · the thesis in one sentence — concentration, not per-prompt guilt */}
      <Composition
        id="scene-66"
        component={MapRoute}
        durationInFrames={396}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          drawOnFrames: 16,
        }}
      />

      {/* scene_67 · establishing · relocate the weight — and turn to wonder */}
      <Composition
        id="scene-67"
        component={PlatePush}
        durationInFrames={369}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_67.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_68 · establishing · begin the roll-call of the hidden chain */}
      <Composition
        id="scene-68"
        component={PlatePush}
        durationInFrames={297}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_68.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_69 · cross_section · the collapse — civilisation-scale to a cursor */}
      <Composition
        id="scene-69"
        component={Scene69}
        durationInFrames={357}
        fps={30}
        width={3840}
        height={2160}
      />

      {/* scene_70 · detail · the house line — echoes 001's 'no monument to a gradient' */}
      <Composition
        id="scene-70"
        component={PlatePush}
        durationInFrames={333}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_70.png',
          push: 0 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_71 · narrative · the emotional peak — the thesis as a closing aphorism */}
      <Composition
        id="scene-71"
        component={PlatePush}
        durationInFrames={357}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_71.png',
          push: 5 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_72 · detail · return to the phone — the callback frame */}
      <Composition
        id="scene-72"
        component={PlatePush}
        durationInFrames={357}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_72.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_73 · cross_section · the ladder recited back, one continuous pull */}
      <Composition
        id="scene-73"
        component={Scene73}
        durationInFrames={408}
        fps={30}
        width={3840}
        height={2160}
      />

      {/* scene_74 · establishing · land the chain on the reactor — final rung */}
      <Composition
        id="scene-74"
        component={PlatePush}
        durationInFrames={321}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_74.png',
          push: 4 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_75 · establishing · the closing line — held */}
      <Composition
        id="scene-75"
        component={PlatePush}
        durationInFrames={270}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_75.png',
          push: 0 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_76 · detail · sign-off */}
      <Composition
        id="scene-76"
        component={PlatePush}
        durationInFrames={309}
        fps={30}
        width={3840}
        height={2160}
        defaultProps={{
          domain: 'infrastructure' as const,
          plate: 'plates/scene_76.png',
          push: 3 as const,
          direction: 'in' as const,
        }}
      />

      {/* scene_77 · outro · outro card — subscribe + next video, title sting reprise */}
      <Composition
        id="scene-77"
        component={Scene77}
        durationInFrames={240}
        fps={30}
        width={3840}
        height={2160}
      />

    </>
  );
};

import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from 'remotion';
import type { Domain } from '../brand/tokens';

/**
 * Diagram — schematic build-on family (brand_guide_software.md §5 "Elements").
 *
 * The workhorse for every scene whose content is a *drawing*, not a photograph: bars,
 * ladders, chains, block flows. Elements arrive one at a time — 8 frames in, 3 frames of
 * stagger between siblings — and then STOP. Nothing idles, nothing loops.
 *
 * Why this is a component and not a plate: an image model cannot draw a bar chart to
 * scale, cannot animate a build-on, and costs money to get wrong. 35 of this video's 77
 * scenes are built here for ₹0. (scene-composer, pass 4.)
 *
 * Tier: props-editor tunable. Hero diagrams are written standalone — see src/scenes/.
 */

export type DiagramProps = {
  /** Node captions, drawn in order. Mono per §4 — these are usually numbers. */
  labels: string[];
  domain: Domain;
  /** 'row' for chains and ladders, 'bars' for magnitude comparisons. */
  layout?: 'row' | 'bars';
  /**
   * Relative bar heights 0–1, used when layout is 'bars'. REQUIRED for any bars
   * diagram — omitting them draws every bar the same height, which is a chart
   * that contradicts its own labels. Derive them from the real figures.
   */
  weights?: number[];
};

const ACCENT: Record<Domain, string> = {
  infrastructure: '#22D3EE',
  security: '#4ADE80',
  data: '#A78BFA',
  ai: '#FFB020',
  failure: '#FF4D4D',
  languages: '#60A5FA',
};

export const Diagram: React.FC<DiagramProps> = ({
  labels,
  domain,
  layout = 'row',
  weights,
}) => {
  const frame = useCurrentFrame();
  const accent = ACCENT[domain];

  return (
    <AbsoluteFill name="Scene" style={{ backgroundColor: '#0B0E14' }}>
      <AbsoluteFill
        name="Diagram"
        style={{
          alignItems: 'flex-end',
          justifyContent: 'center',
          gap: 160,
          flexDirection: 'row',
          paddingBottom: 360,
        }}
      >
        {labels.map((label, i) => {
          // §5: 8 frames in, 3 frames of stagger, EASE.standard, then still.
          // Offset by the 30-frame head handle — frame 30 is where the scene really
          // starts, so this is what makes the build-on land with the narration.
          const start = 30 + i * 3;
          const enter = interpolate(frame, [start, start + 8], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.bezier(0.4, 0, 0.2, 1),
          });
          // A bar's height IS its claim. The 60px floor keeps a tiny value visible
          // without flattening a 100x gap into a 2x one — the ratio still reads.
          // 1240 + the 360 padding + the label keeps the tallest bar inside COMP-5's
          // 90% title-safe area; going bigger clipped the 1,000,000,000 bar (scene_45).
          const height =
            layout === 'bars' ? 60 + (weights?.[i] ?? 1) * 1240 : 300;
          const last = i === labels.length - 1;

          return (
            <div
              key={label}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: 40,
                opacity: enter,
                transform: `translateY(${(1 - enter) * 12}px)`,
              }}
            >
              <div
                style={{
                  width: 320,
                  height,
                  backgroundColor: last ? accent : '#2A3240',
                  borderRadius: 8,
                }}
              />
              <div
                style={{
                  color: last ? accent : '#8B94A7',
                  fontFamily: 'IBM Plex Mono',
                  fontSize: 64,
                  textAlign: 'center',
                  maxWidth: 560,
                }}
              >
                {label}
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

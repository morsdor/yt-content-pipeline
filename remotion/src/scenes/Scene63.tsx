import { AbsoluteFill, Img, Interactive, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';

/**
 * Scene63 — hero scene, canvas-interactive tier (brand_guide_software.md §11).
 *
 * THE TITLE PAYOFF — and the video's mandatory static beat (§5: 'the most important frame in
 * every video should be completely static'). After eleven minutes of escalation the camera stops.
 * The only motion permitted is the plume's ambient drift. Do not add a push here.
 *
 * Every style value is a hardcoded literal so Studio can select, drag and keyframe each
 * element and write the edit straight back into this file. Validated by `npm run brand:check`.
 */

export const Scene63: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // §5 MANDATORY STATIC BEAT — no camera move at all. `frame` drives only the plume.

  return (
    <AbsoluteFill name="Scene 63" style={{ backgroundColor: '#0B0E14' }}>
      <Interactive.Div
        name="Plate"
        style={{
          width: '100%',
          height: '100%',
          scale: 1,
        }}
      >
        <Img
          src={staticFile('plates/scene_63.png')}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </Interactive.Div>

      {/* §5 ambient drift 4 px/s — the single permitted moving element here. */}
      <Interactive.Div
        name="Plume drift"
        style={{
          position: 'absolute',
          inset: 0,
          backgroundColor: 'transparent',
          translate: `${interpolate(frame, [15, durationInFrames - 15], [0, 4 * (durationInFrames / 30)], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          })}px 0px`,
        }}
      />
    </AbsoluteFill>
  );
};

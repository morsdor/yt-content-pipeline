import { AbsoluteFill, Easing, Img, Interactive, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';

/**
 * Scene24 — hero scene, canvas-interactive tier (brand_guide_software.md §11).
 *
 * Pull-back 1 of 3 (CAM-4 budget). Three scale tiers nested in one frame — a rack, the
 * hall behind it, a town beyond. The pull is the argument: it is bigger than you thought.
 *
 * Every style value is a hardcoded literal so Studio can select, drag and keyframe each
 * element and write the edit straight back into this file. Validated by `npm run brand:check`.
 */

export const Scene24: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // §5: pull-back 7%, resting at both ends. This is a rationed move.
  const scale = interpolate(frame, [15, durationInFrames - 15], [1.07, 1.0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(0.4, 0, 0.2, 1),
  });

  return (
    <AbsoluteFill name="Scene 24" style={{ backgroundColor: '#0B0E14' }}>
      <Interactive.Div
        name="Plate"
        style={{
          width: '100%',
          height: '100%',
          scale,
        }}
      >
        <Img
          src={staticFile('plates/scene_24.png')}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </Interactive.Div>

      <Interactive.Div
        name="Callout: one rack"
        style={{
          position: 'absolute',
          left: 240,
          top: 200,
          backgroundColor: '#161B26',
          border: '1px solid #2A3240',
          borderLeft: '6px solid #22D3EE',
          borderRadius: 8,
          padding: '16px 28px',
          color: '#E8E6E1',
          fontFamily: 'IBM Plex Mono',
          fontSize: 72,
          opacity: interpolate(frame, [15, 23, 155, 160], [0, 1, 1, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.bezier(0.4, 0, 0.2, 1),
          }),
        }}
      >
        one rack
      </Interactive.Div>

      <Interactive.Div
        name="Callout: one town"
        style={{
          position: 'absolute',
          left: 240,
          top: 200,
          backgroundColor: '#161B26',
          border: '1px solid #2A3240',
          borderLeft: '6px solid #22D3EE',
          borderRadius: 8,
          padding: '16px 28px',
          color: '#E8E6E1',
          fontFamily: 'IBM Plex Mono',
          fontSize: 72,
          opacity: interpolate(frame, [145, 153, 260, 265], [0, 1, 1, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.bezier(0.4, 0, 0.2, 1),
          }),
        }}
      >
        one town
      </Interactive.Div>
    </AbsoluteFill>
  );
};

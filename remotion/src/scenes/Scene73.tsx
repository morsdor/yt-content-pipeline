import { AbsoluteFill, Easing, Img, Interactive, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';

/**
 * Scene73 — hero scene, canvas-interactive tier (brand_guide_software.md §11).
 *
 * Pull-back 3 of 3, the widest move in the film: the whole chain in one continuous frame —
 * phone, datacenter, cooling towers, power station, fab, reactor — joined by glowing conductors.
 *
 * Every style value is a hardcoded literal so Studio can select, drag and keyframe each
 * element and write the edit straight back into this file. Validated by `npm run brand:check`.
 */

export const Scene73: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // §5: pull-back 9%, resting at both ends. This is a rationed move.
  const scale = interpolate(frame, [15, durationInFrames - 15], [1.09, 1.0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(0.4, 0, 0.2, 1),
  });

  return (
    <AbsoluteFill name="Scene 73" style={{ backgroundColor: '#0B0E14' }}>
      <Interactive.Div
        name="Plate"
        style={{
          width: '100%',
          height: '100%',
          scale,
        }}
      >
        <Img
          src={staticFile('plates/scene_73.png')}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </Interactive.Div>

      {/* §5 ambient drift 3 px/s — the single permitted moving element here. */}
      <Interactive.Div
        name="Plume drift"
        style={{
          position: 'absolute',
          inset: 0,
          backgroundColor: 'transparent',
          translate: `${interpolate(frame, [15, durationInFrames - 15], [0, 3 * (durationInFrames / 30)], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          })}px 0px`,
        }}
      />
    </AbsoluteFill>
  );
};

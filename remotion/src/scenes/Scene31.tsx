import { AbsoluteFill, Easing, Img, Interactive, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';

/**
 * Scene31 — hero scene, canvas-interactive tier (brand_guide_software.md §11).
 *
 * MATCH-CUT 1 of 3. The incoming half: the datacenter's rooftop plume (scene_28) becomes a
 * POWER STATION's hyperbolic towers. Same silhouette, bigger scale — the match IS the argument,
 * because the water was never at the datacenter. Pan LEFT: we are following power back upstream
 * (continuity_registry.sides.power_flow).
 *
 * Every style value is a hardcoded literal so Studio can select, drag and keyframe each
 * element and write the edit straight back into this file. Validated by `npm run brand:check`.
 */

export const Scene31: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // §5: pan 45 px/s at 4K, left — direction set by continuity_registry.sides.
  const x = interpolate(frame, [15, durationInFrames - 15], [0, -45 * (durationInFrames / 30)], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(0.4, 0, 0.2, 1),
  });

  return (
    <AbsoluteFill name="Scene 31" style={{ backgroundColor: '#0B0E14' }}>
      <Interactive.Div
        name="Plate"
        style={{
          width: '100%',
          height: '100%',
          scale: 1.06,
          translate: `${x}px 0px`,
        }}
      >
        <Img
          src={staticFile('plates/scene_31.png')}
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

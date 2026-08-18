import { AbsoluteFill, Easing, Interactive, interpolate, useCurrentFrame } from 'remotion';

/**
 * TitleCard — the §7 beat at 0:45, on every video, unchanged.
 *
 * This file is also the HOUSE REFERENCE for a fully canvas-interactive scene: every
 * value in every `style` is a hardcoded literal, so Studio can select, drag and keyframe
 * each element and write the edit back into this file. Compare `families/PlatePush.tsx`,
 * which trades that for reusability.
 *
 * Brand literals used (validated by `npm run brand:check`):
 *   #0B0E14 ink · #E8E6E1 bone · #FFB020 amber · Easing.bezier(0.4, 0, 0.2, 1)
 */

export const TitleCard: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      name="Title card"
      style={{
        backgroundColor: '#0B0E14',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
      }}
    >
      <Interactive.Div
        name="Wordmark"
        style={{
          fontFamily: 'Archivo Black',
          fontSize: 260,
          letterSpacing: '0.02em',
          color: '#E8E6E1',
          opacity: interpolate(frame, [0, 8], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.bezier(0.4, 0, 0.2, 1),
          }),
          translate: interpolate(frame, [0, 8], ['0px 12px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.bezier(0.4, 0, 0.2, 1),
          }),
        }}
      >
        LOAD BEARING
      </Interactive.Div>

      {/* §2: one structural rule mark — the line it carries. Draws on, then holds. */}
      <Interactive.Div
        name="Rule"
        style={{
          height: 10,
          backgroundColor: '#FFB020',
          marginTop: 36,
          width: interpolate(frame, [6, 24], ['0px', '900px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.bezier(0.4, 0, 0.2, 1),
          }),
        }}
      />

      <Interactive.Div
        name="Topic"
        style={{
          fontFamily: 'IBM Plex Sans',
          fontWeight: 400,
          fontSize: 72,
          color: '#8B94A7',
          marginTop: 48,
          opacity: interpolate(frame, [14, 22], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.bezier(0.4, 0, 0.2, 1),
          }),
        }}
      >
        The Physical Cost of AI
      </Interactive.Div>
    </AbsoluteFill>
  );
};

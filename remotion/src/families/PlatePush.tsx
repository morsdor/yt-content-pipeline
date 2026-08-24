import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import type { Domain, PushPercent } from '../brand/tokens';
import { DOMAIN_ACCENT } from '../brand/tokens';

/**
 * PlatePush — the workhorse family (brand_guide_software.md §5).
 *
 * A validated still plate given one slow camera move for the scene's full duration.
 * The majority of a 60–80 scene board is this component plus a props row.
 *
 * ── Interactivity tier ──────────────────────────────────────────────────────
 * Families take props, and Remotion Studio can only make a style CANVAS-interactive
 * (drag, resize, editable keyframes) when every value in `style` is an inline literal.
 * Props are therefore tunable in the **Props editor** — which does write back to code
 * when `defaultProps` is an inline object literal on `<Composition>` — but not by
 * dragging on the canvas.
 *
 * That is the intended trade:
 *   • Mechanical scenes  → this family. Fast, consistent, Props-editor tunable.
 *   • The 5–10 hero scenes → written standalone with hardcoded literals and
 *     `Interactive.Div`, so they are fully hand-tunable on the canvas.
 * (remotion-director Procedure step 5 makes the same split.)
 */

export type PlatePushProps = {
  /** Path under public/, e.g. "plates/scene_04.png". Omit to render the ink ground. */
  plate?: string;
  /** Scene domain — selects the accent (§3). One accent per video. */
  domain: Domain;
  /** Push-in 3–5%, pull-back 6–9%, or 0 for the mandatory static beat. */
  push: PushPercent;
  /** `in` = push in (grows), `out` = pull back (shrinks to reveal). */
  direction?: 'in' | 'out';
  /** Optional bottom-left scene label. Set in mono per §4. */
  label?: string;
};

export const PlatePush: React.FC<PlatePushProps> = ({
  plate,
  domain,
  push,
  direction = 'in',
  label,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // §5: every camera move starts and ends at rest. The scale range is derived from the
  // `push` prop, so this property is Props-editor tunable rather than canvas-draggable.
  const from = direction === 'in' ? 1 : 1 + push / 100;
  const to = direction === 'in' ? 1 + push / 100 : 1;

  return (
    <AbsoluteFill name="Scene" style={{ backgroundColor: '#0B0E14' }}>
      {plate ? (
        <Img
          name="Plate"
          src={staticFile(plate)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            // §5: CAMERA.holdFrames = 15 at both ends, so the clip starts and ends
            // at rest and Premiere's trim lands on a still frame.
            scale: interpolate(frame, [15, durationInFrames - 15], [from, to], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
              easing: Easing.bezier(0.4, 0, 0.2, 1),
              output: 'perceptual-scale',
            }),
          }}
        />
      ) : (
        // Placeholder ground so the board previews before plates are generated.
        <AbsoluteFill
          name="Plate placeholder"
          style={{
            backgroundColor: '#161B26',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#2A3240',
            fontFamily: 'IBM Plex Mono',
            fontSize: 56,
          }}
        >
          no plate
        </AbsoluteFill>
      )}

      {label ? (
        <AbsoluteFill
          name="Scene label"
          style={{ alignItems: 'flex-start', justifyContent: 'flex-end', padding: 160 }}
        >
          <div
            style={{
              backgroundColor: '#161B26',
              border: '1px solid #2A3240',
              borderRadius: 8,
              padding: '16px 28px',
              color: '#8B94A7',
              fontFamily: 'IBM Plex Mono',
              fontSize: 44,
              opacity: interpolate(frame, [30, 38], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
                easing: Easing.bezier(0.4, 0, 0.2, 1),
              }),
              borderLeft: `6px solid ${DOMAIN_ACCENT[domain]}`,
            }}
          >
            {label}
          </div>
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};

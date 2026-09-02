import { Easing, interpolate, useCurrentFrame } from 'remotion';

/**
 * Shared chrome for the short-form reels — the parts that are identical in every
 * one of them: the pinned header, the step label, the mono readout strip, the
 * progress bar, and the fade primitive.
 *
 * ── Why these live outside the reel file ────────────────────────────────────
 * The Studio-interactivity doctrine (brand_guide_software.md §11) says scene files
 * hardcode style literals so Studio can make them click-editable. That still holds
 * for the parts of a reel you would actually tweak on the canvas — the visualisation
 * itself. It does not earn its keep for the chrome, which is fixed by the format and
 * would only rot into five slightly-different copies. The literals still live in one
 * place, so `brand:check` still polices them.
 *
 * NOTE: `Shazam.tsx` (r001) predates this file and carries its own copies. It is
 * shipped and approved, so it was left alone rather than refactored for tidiness —
 * migrate it the next time it needs a real change.
 */

export const FPS = 30;
export const REEL_W = 1080;
export const REEL_H = 1920;

/** The only two sanctioned curves (brand_guide_software.md §5). */
const E: [number, number, number, number] = [0.4, 0, 0.2, 1];
export const ease = {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
  easing: Easing.bezier(...E),
} as const;

/** Seconds -> frames. Reels carry no handles: content starts at frame 0. */
export const t = (s: number) => s * FPS;

export const fmt = (n: number) => n.toLocaleString('en-US');

/** 8f fade + 12px rise in, 5f fade out with no movement. */
export const Fade: React.FC<{
  from: number;
  to?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ from, to, children, style }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [from, from + 8], [0, 1], ease);
  const out = to === undefined ? 1 : interpolate(frame, [to - 5, to], [1, 0], ease);
  const rise = interpolate(frame, [from, from + 8], [12, 0], ease);
  return (
    <div style={{ ...style, opacity: Math.min(o, out), transform: `translateY(${rise}px)` }}>
      {children}
    </div>
  );
};

/**
 * The title is on screen from the first frame to the last — a scroller landing six
 * seconds in still has to know what they are watching.
 *
 * The big-to-small handoff is SEQUENTIAL, not a crossfade: two different type sizes
 * dissolving through each other in the same place reads as a double exposure.
 */
export const ReelHeader: React.FC<{
  big: React.ReactNode;
  small: React.ReactNode;
  out: [number, number];
  in_: [number, number];
}> = ({ big, small, out, in_ }) => {
  const frame = useCurrentFrame();
  const bigO = interpolate(frame, [t(out[0]), t(out[1])], [1, 0], ease);
  const smallO = interpolate(frame, [t(in_[0]), t(in_[1])], [0, 1], ease);
  return (
    <>
      <div
        style={{
          position: 'absolute',
          top: 120,
          left: 60,
          width: 960,
          textAlign: 'center',
          opacity: bigO,
          fontFamily: 'Archivo Black',
          fontSize: 76,
          lineHeight: 1.1,
          color: '#E8E6E1',
          letterSpacing: -1,
        }}
      >
        {big}
      </div>
      <div
        style={{
          position: 'absolute',
          top: 150,
          left: 60,
          width: 960,
          textAlign: 'center',
          opacity: smallO,
          fontFamily: 'Archivo Black',
          fontSize: 54,
          color: '#E8E6E1',
          letterSpacing: -0.5,
        }}
      >
        {small}
      </div>
    </>
  );
};

/** Step number + claim + one plain-English line. Same slot every beat. */
export const StepLabel: React.FC<{
  n: string;
  title: string;
  sub: string;
  from: number;
  to: number;
}> = ({ n, title, sub, from, to }) => (
  <Fade from={from} to={to} style={{ position: 'absolute', top: 300, left: 60, width: 960 }}>
    <div
      style={{
        fontFamily: 'IBM Plex Mono',
        fontSize: 38,
        color: '#8B94A7',
        letterSpacing: 3,
        marginBottom: 10,
      }}
    >
      {n}
    </div>
    <div style={{ fontFamily: 'IBM Plex Sans', fontWeight: 600, fontSize: 60, color: '#E8E6E1' }}>
      {title}
    </div>
    <div style={{ fontFamily: 'IBM Plex Sans', fontSize: 42, color: '#8B94A7', marginTop: 8 }}>
      {sub}
    </div>
  </Fade>
);

/** Instrumentation straight from the run — free authority, the numbers already exist. */
export const Readout: React.FC<{
  from: number;
  to: number;
  top?: number;
  rows: [string, string][];
}> = ({ from, to, top = 1196, rows }) => (
  <Fade from={from} to={to} style={{ position: 'absolute', top, left: 60, width: 960 }}>
    {rows.map(([k, v]) => (
      <div
        key={k}
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          borderTop: '2px solid #2A3240',
          padding: '14px 4px',
          fontFamily: 'IBM Plex Mono',
          fontSize: 40,
        }}
      >
        <span style={{ color: '#8B94A7' }}>{k}</span>
        <span style={{ color: '#E8E6E1' }}>{v}</span>
      </div>
    ))}
  </Fade>
);

export const Progress: React.FC<{ seconds: number }> = ({ seconds }) => {
  const frame = useCurrentFrame();
  const p = Math.min(1, frame / (seconds * FPS));
  return (
    <div style={{ position: 'absolute', top: 1790, left: 60, width: 960, height: 6 }}>
      <div style={{ position: 'absolute', width: 960, height: 6, background: '#2A3240' }} />
      <div style={{ position: 'absolute', width: 960 * p, height: 6, background: '#22D3EE' }} />
    </div>
  );
};

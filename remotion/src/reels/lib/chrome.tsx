import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from 'remotion';

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

/**
 * ── Instagram safe area ─────────────────────────────────────────────────────
 * Instagram paints its OWN chrome over the video: the status bar and "Reels"
 * header across the top, the caption / username / audio strip across the bottom,
 * and the like/comment/share rail down the right. Anything we put underneath is
 * simply not read.
 *
 * r001 was authored to the raw 1080x1920 canvas, so its title sat at y=120 —
 * entirely inside Instagram's top bar. Confirmed in the app 2026-09-02. The
 * numbers below are the correction, and every reel from r002 on is laid out
 * against them rather than against the canvas.
 *
 * Render `<SafeZones />` over any reel to check it before posting.
 */
export const SAFE = { top: 270, bottom: 380, side: 60, rail: 210 } as const;

/** First y-coordinate Instagram does not cover. */
export const SAFE_TOP = SAFE.top;                          // 270
/** Last y-coordinate Instagram does not cover. */
export const SAFE_BOTTOM = REEL_H - SAFE.bottom;           // 1540
/** Usable height. This — not 1920 — is the canvas a reel is composed on. */
export const SAFE_H = SAFE_BOTTOM - SAFE_TOP;              // 1270
/** Full-bleed content width, for text that never reaches the action rail. */
export const CONTENT_W = REEL_W - SAFE.side * 2;           // 960
/** Width that also clears the right-hand action rail. Wide elements use this. */
export const SAFE_W = REEL_W - SAFE.side - SAFE.rail;      // 810
/** Centre-line of the rail-safe band. Wide elements centre on this, not 540. */
export const SAFE_CX = SAFE.side + SAFE_W / 2;             // 465

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
          top: 290,
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
          top: 320,
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
  <Fade from={from} to={to} style={{ position: 'absolute', top: 470, left: 60, width: 960 }}>
    <div
      style={{
        fontFamily: 'IBM Plex Mono',
        fontSize: 38,
        color: '#81A2C4',
        letterSpacing: 3,
        marginBottom: 10,
      }}
    >
      {n}
    </div>
    <div style={{ fontFamily: 'IBM Plex Sans', fontWeight: 600, fontSize: 60, color: '#E8E6E1' }}>
      {title}
    </div>
    <div style={{ fontFamily: 'IBM Plex Sans', fontSize: 42, color: '#81A2C4', marginTop: 8 }}>
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
}> = ({ from, to, top = 1240, rows }) => (
  <Fade from={from} to={to} style={{ position: 'absolute', top, left: 60, width: 960 }}>
    {rows.map(([k, v]) => (
      <div
        key={k}
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          borderTop: '2px solid #274064',
          padding: '14px 4px',
          fontFamily: 'IBM Plex Mono',
          fontSize: 40,
        }}
      >
        <span style={{ color: '#81A2C4' }}>{k}</span>
        <span style={{ color: '#E8E6E1' }}>{v}</span>
      </div>
    ))}
  </Fade>
);

export const Progress: React.FC<{ seconds: number }> = ({ seconds }) => {
  const frame = useCurrentFrame();
  const p = Math.min(1, frame / (seconds * FPS));
  return (
    <div style={{ position: 'absolute', top: SAFE_BOTTOM - 6, left: 60, width: 960, height: 6 }}>
      <div style={{ position: 'absolute', width: 960, height: 6, background: '#274064' }} />
      <div style={{ position: 'absolute', width: 960 * p, height: 6, background: '#00D6F7' }} />
    </div>
  );
};

/**
 * Debug overlay: paints Instagram's chrome zones over a reel so a layout can be
 * checked before it is posted. Red = covered by IG. Amber = the action rail.
 * Never rendered in a shipped composition — see the `*-safe` compositions in
 * Root.tsx, which exist purely to eyeball this.
 */
export const SafeZones: React.FC = () => (
  <>
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: REEL_W,
        height: SAFE_TOP,
        background: 'rgba(255,77,77,0.45)',
        borderBottom: '4px solid #FF4D4D',
      }}
    />
    <div
      style={{
        position: 'absolute',
        top: SAFE_BOTTOM,
        left: 0,
        width: REEL_W,
        height: SAFE.bottom,
        background: 'rgba(255,77,77,0.45)',
        borderTop: '4px solid #FF4D4D',
      }}
    />
    <div
      style={{
        position: 'absolute',
        top: 1050,
        left: REEL_W - SAFE.rail,
        width: SAFE.rail,
        height: SAFE_BOTTOM - 1050,
        background: 'rgba(255,176,32,0.38)',
      }}
    />
  </>
);

/**
 * The reel ground — brand guide §3a.
 *
 * A flat near-black fill leaves ~83% of the safe band empty and ~90% of the frame
 * effectively greyscale, which is what made the first two reels read as pale. This
 * replaces it with the drafting table §3 has always described in prose: a faint
 * measured grid, masked so it is densest behind the content and gone by the frame
 * edge, over a wide accent glow that gives the ground depth without competing with
 * anything drawn on top.
 *
 * Every reel uses this instead of a bare `backgroundColor` fill. The accent is the
 * reel's DOMAIN_ACCENT, so the ground is tinted by subject.
 */
export const ReelGround: React.FC<{ accent: string }> = ({ accent }) => {
  const mask =
    'radial-gradient(ellipse 68% 52% at 50% 46%, rgba(0,0,0,1) 0%, ' +
    'rgba(0,0,0,0.45) 55%, rgba(0,0,0,0) 100%)';
  return (
    <>
      <AbsoluteFill style={{ backgroundColor: '#040E1F' }} />
      <AbsoluteFill
        style={{
          opacity: 0.11,
          backgroundImage: `radial-gradient(ellipse 78% 58% at 50% 46%, ${accent} 0%, transparent 70%)`,
        }}
      />
      <AbsoluteFill
        style={{
          backgroundImage:
            'repeating-linear-gradient(0deg, #0D1F3C 0 2px, transparent 2px 90px),' +
            'repeating-linear-gradient(90deg, #0D1F3C 0 2px, transparent 2px 90px)',
          maskImage: mask,
          WebkitMaskImage: mask,
        }}
      />
    </>
  );
};

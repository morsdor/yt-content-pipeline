import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import { HIST, HIT, LINKS, MISS, PEAKS, STATS, WAVE } from './data/shazam';

/**
 * r001 — "How Shazam names a song in 3 seconds"  ·  1080x1920, 24s, Instagram/Shorts.
 *
 * ── Why this scene is computed, not drawn ───────────────────────────────────
 * Every mark on screen is real output from projects/r001_shazam/fingerprint.py: a genuine
 * STFT, genuine local-maxima peaks, genuine (f1,f2,dt) hashes, and a genuine match whose
 * recovered offset (4.18s) lands one STFT frame away from where the query was actually cut
 * (4.20s). Nothing is keyframed to "look like" the algorithm working — the algorithm ran,
 * and this composition plays back its state.
 *
 * That is the whole method: the animation is the program's intermediate values, so it
 * cannot drift out of sync with the explanation, and the on-screen numbers are free.
 *
 * ── The hook rule ───────────────────────────────────────────────────────────
 * The title never says "audio fingerprinting" or "constellation hashing". It opens on a
 * thing anyone has done — holding a phone up in a café — because the two reels that broke
 * out on the comp account both opened on a civilian object and every reel that opened on a
 * developer noun died at 2-17k views (docs/comp_deep_dive_equationverse.md §2).
 *
 * ── Beats ───────────────────────────────────────────────────────────────────
 *   0.0- 5.2s  HOOK        the 3-second recording, as a waveform. Useless on its own.
 *   5.4-11.8s  SPECTROGRAM the sound becomes a picture (real STFT wipes in).
 *  12.0-18.6s  PEAKS       keep only the loudest point per cell — 224 survive the noise.
 *  18.8-25.4s  HASHES      pair them into (f1, f2, dt) triples — 1,633 numbers.
 *  25.6-34.0s  MATCH       the payoff. Wrong song = a cloud. Right song = a straight line.
 *  33.9-40.0s  ANSWER      the offset histogram spikes; 41 ms, from 3 seconds of noise.
 *
 * Each beat = label alone (1.5s) -> animation (2.2-3.1s) -> hold on the result (~2s).
 *
 * ── The camera ──────────────────────────────────────────────────────────────
 * There isn't one. It never moves, for the entire 40 seconds. The comp account's two hits
 * have zero camera moves between them; what carries the frame is that the thing on screen
 * is executing. No handles either — a reel is the final deliverable, not a Premiere conform.
 */

// ── canvas ──────────────────────────────────────────────────────────────────
const W = 1080;
const HGT = 1920;
const FPS = 30;

const E: [number, number, number, number] = [0.4, 0, 0.2, 1];
const ease = {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
  easing: Easing.bezier(...E),
} as const;

/** Seconds -> frames. No head handle: content starts at frame 0. */
const t = (s: number) => s * FPS;


/**
 * Beat timing, in seconds. Every time value in this file lives here.
 *
 * Retimed after the first cut played "too fast to understand anything". The 24s
 * version gave each step ~4s to introduce a concept AND finish animating it, so the
 * viewer was still reading the label while the motion completed. Three rules now
 * govern the pacing, and they are why this runs 40s rather than 24s:
 *
 *   1. The label lands ALONE for ~1.5s before its animation starts.
 *   2. Each transformation runs 2.2-3.1s, not 0.6-1.6s.
 *   3. Every beat ends holding its finished state for ~2s with nothing moving.
 *
 * Rule 3 is the one the first cut missed entirely — a completed diagram that is
 * immediately wiped never gets read.
 */
const T = {
  // beat 1 · the recording ................................. 0.0 - 5.2
  cafe: [0.9, 5.0],
  waveDraw: [1.4, 3.4],
  waveOut: [4.4, 5.0],
  stat: [3.7, 5.1],
  titleOut: [4.4, 4.8],
  titleIn: [4.8, 5.15],

  // beat 2 · spectrogram ................................... 5.4 - 11.8
  s1Label: [5.4, 11.8],
  specWipe: [6.9, 9.1],
  s1Read: [9.3, 11.8],

  // beat 3 · constellation ................................ 12.0 - 18.6
  s2Label: [12.0, 18.6],
  specDim: [13.5, 14.6],
  peaksStart: 13.5,
  peaksSpan: 3.0,
  s2Read: [14.4, 18.6],

  // beat 4 · hashes ....................................... 18.8 - 25.4
  s3Label: [18.8, 25.4],
  links: [20.3, 23.4],
  s3Read: [20.7, 25.4],
  chip: [23.6, 25.4],
  constOut: [25.4, 26.0],

  // beat 5 · the match .................................... 25.6 - 34.0
  s4Label: [25.6, 34.0],
  panelA: 27.0,
  panelB: 29.2,
  ignite: 31.3,
  panelsOut: 34.0,
  s4Caption: [32.6, 34.0],

  // beat 6 · the answer ................................... 33.9 - 40.0
  s5Label: [33.9, 40.0],
  hist: 34.2,
  answer: 35.9,
  closing: 37.4,
} as const;

export const DURATION_SECONDS = 40;

// The stage every beat draws inside — one rectangle, so nothing jumps between beats.
const SX = 60;
const SY = 548;
const SW = 960;
const SH = 560;

const fmt = (n: number) => n.toLocaleString('en-US');

// ── small building blocks ───────────────────────────────────────────────────

/** Board text choreography: 8f fade + 12px rise in, 5f fade out, no exit movement. */
const Fade: React.FC<{
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

/** The persistent header — present from the first frame to the last, per the reel rule. */
const Header: React.FC<{ frame: number }> = ({ frame }) => {
  // The hook owns the big centred title; afterwards it shrinks to a permanent bar.
  const big = interpolate(frame, [t(T.titleOut[0]), t(T.titleOut[1])], [1, 0], ease);
  const small = interpolate(frame, [t(T.titleIn[0]), t(T.titleIn[1])], [0, 1], ease);
  return (
    <>
      <div
        style={{
          position: 'absolute',
          top: 120,
          left: 60,
          width: 960,
          textAlign: 'center',
          opacity: big,
          fontFamily: 'Archivo Black',
          fontSize: 76,
          lineHeight: 1.1,
          color: '#E8E6E1',
          letterSpacing: -1,
        }}
      >
        How Shazam names
        <br />a song in <span style={{ color: '#00D6F7' }}>3 seconds</span>
      </div>
      <div
        style={{
          position: 'absolute',
          top: 150,
          left: 60,
          width: 960,
          textAlign: 'center',
          opacity: small,
          fontFamily: 'Archivo Black',
          fontSize: 54,
          color: '#E8E6E1',
          letterSpacing: -0.5,
        }}
      >
        How Shazam names a song in <span style={{ color: '#00D6F7' }}>3 seconds</span>
      </div>
    </>
  );
};

/** Step label + one-line plain-English claim. Same slot every beat. */
const StepLabel: React.FC<{ n: string; title: string; sub: string; from: number; to: number }> = ({
  n,
  title,
  sub,
  from,
  to,
}) => (
  <Fade from={from} to={to} style={{ position: 'absolute', top: 300, left: 60, width: 960 }}>
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

/** Mono readout strip under the stage — the instrumentation, straight from the run. */
const Readout: React.FC<{ from: number; to: number; rows: [string, string][] }> = ({
  from,
  to,
  rows,
}) => (
  <Fade from={from} to={to} style={{ position: 'absolute', top: 1196, left: 60, width: 960 }}>
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

// ── beat 1: the recording ───────────────────────────────────────────────────

const Waveform: React.FC<{ frame: number }> = ({ frame }) => {
  const draw = interpolate(frame, [t(T.waveDraw[0]), t(T.waveDraw[1])], [0, 1], ease);
  const fade = interpolate(frame, [t(T.waveOut[0]), t(T.waveOut[1])], [1, 0], ease);
  const n = Math.max(2, Math.floor(WAVE.length * draw));
  const midY = SY + SH / 2;
  const pts = WAVE.slice(0, n)
    .map((v, i) => `${SX + (i / (WAVE.length - 1)) * SW},${midY - v * (SH / 2 - 40)}`)
    .join(' ');
  const headX = SX + (n / (WAVE.length - 1)) * SW;
  return (
    <svg width={W} height={HGT} style={{ position: 'absolute', opacity: fade }}>
      <line x1={SX} y1={midY} x2={SX + SW} y2={midY} stroke="#274064" strokeWidth={2} />
      <polyline points={pts} fill="none" stroke="#00D6F7" strokeWidth={3} />
      {draw < 1 ? (
        <line
          x1={headX}
          y1={SY + 20}
          x2={headX}
          y2={SY + SH - 20}
          stroke="#FFB020"
          strokeWidth={3}
        />
      ) : null}
    </svg>
  );
};

// ── beats 2-4: spectrogram, constellation, hashes ───────────────────────────

const Spectrogram: React.FC<{ frame: number }> = ({ frame }) => {
  const wipe = interpolate(frame, [t(T.specWipe[0]), t(T.specWipe[1])], [0, 1], ease);
  // Dims once the peaks arrive: the constellation, not the picture, is the point.
  const dim = interpolate(frame, [t(T.specDim[0]), t(T.specDim[1])], [1, 0.26], ease);
  const gone = interpolate(frame, [t(T.constOut[0]), t(T.constOut[1])], [1, 0], ease);
  return (
    <div
      style={{
        position: 'absolute',
        left: SX,
        top: SY,
        width: SW,
        height: SH,
        opacity: dim * gone,
        clipPath: `inset(0 ${(1 - wipe) * 100}% 0 0)`,
      }}
    >
      <Img
        src={staticFile('reels/r001_spectrogram.png')}
        style={{ width: SW, height: SH, objectFit: 'fill' }}
      />
    </div>
  );
};

const Constellation: React.FC<{ frame: number }> = ({ frame }) => {
  const gone = interpolate(frame, [t(T.constOut[0]), t(T.constOut[1])], [1, 0], ease);
  if (frame < t(T.peaksStart) || gone <= 0) return null;

  // Peaks arrive left-to-right, so the eye reads it as scanning the clip.
  const px = (p: { t: number; f: number }) => SX + p.t * SW;
  const py = (p: { t: number; f: number }) => SY + (1 - p.f) * SH;

  const linkOn = interpolate(frame, [t(T.links[0]), t(T.links[1])], [0, 1], ease);
  const nLinks = Math.floor(DRAWN_LINKS * linkOn);

  return (
    <svg width={W} height={HGT} style={{ position: 'absolute', opacity: gone }}>
      {LINKS.slice(0, nLinks).map(([a, b], i) => {
        const A = PEAKS[a];
        const B = PEAKS[b];
        if (!A || !B) return null;
        return (
          <line
            key={i}
            x1={px(A)}
            y1={py(A)}
            x2={px(B)}
            y2={py(B)}
            stroke={peakColor((A.f + B.f) / 2)}
            strokeWidth={1}
            opacity={0.3}
          />
        );
      })}
      {PEAKS.map((p, i) => {
        // 224 peaks over 3s, ordered by time — a slow scan you can actually follow.
        const at = t(T.peaksStart) + (i / PEAKS.length) * T.peaksSpan * FPS;
        const o = interpolate(frame, [at, at + 6], [0, 1], ease);
        const r = interpolate(frame, [at, at + 6], [9, 4], ease);
        if (o <= 0) return null;
        return (
          <circle key={i} cx={px(p)} cy={py(p)} r={r} fill={peakColor(p.f)} opacity={o} />
        );
      })}
    </svg>
  );
};

/** The hash triple, shown as the thing the pairs literally become. */
const HashChip: React.FC<{ frame: number }> = ({ frame }) => {
  const o = interpolate(frame, [t(T.chip[0]), t(T.chip[0] + 0.5)], [0, 1], ease);
  const out = interpolate(frame, [t(T.chip[1] - 0.4), t(T.chip[1])], [1, 0], ease);
  if (o <= 0) return null;
  return (
    <div
      style={{
        position: 'absolute',
        top: SY + SH + 6,
        left: 60,
        width: 960,
        textAlign: 'center',
        opacity: o * out,
        fontFamily: 'IBM Plex Mono',
        fontSize: 46,
        color: '#FFB020',
      }}
    >
      (f₁, f₂, Δt) → one 32-bit number
    </div>
  );
};

// ── beat 5: the match ───────────────────────────────────────────────────────


/**
 * Peak colour encodes FREQUENCY BAND. The constellation is the one beat where the
 * viewer has to believe these 224 dots still carry the song, and a single flat cyan
 * throws away the one property that makes them a fingerprint — where in the spectrum
 * they sit. Low notes read green, mids cyan, highs violet, so the chord structure
 * survives into the abstraction instead of being flattened out of it.
 *
 * Built as rgb() from the data, not as hex literals: this is a data channel.
 */
const PEAK_STOPS: [number, [number, number, number]][] = [
  [0.0, [61, 223, 125]],   // #3DDF7D — low
  [0.35, [0, 214, 247]],  // #00D6F7 — mid
  [0.7, [81, 164, 255]],   // #51A4FF
  [1.0, [173, 136, 255]],  // #AD88FF — high
];

const peakColor = (f: number): string => {
  let a = PEAK_STOPS[0];
  let b = PEAK_STOPS[PEAK_STOPS.length - 1];
  for (let k = 0; k < PEAK_STOPS.length - 1; k++) {
    if (f >= PEAK_STOPS[k][0] && f <= PEAK_STOPS[k + 1][0]) {
      a = PEAK_STOPS[k];
      b = PEAK_STOPS[k + 1];
      break;
    }
  }
  const u = b[0] === a[0] ? 0 : (f - a[0]) / (b[0] - a[0]);
  const c = a[1].map((ch, k) => Math.round(ch + (b[1][k] - ch) * u));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
};

/**
 * The emitted link set is already stride-sampled across the whole clip
 * (fingerprint.py), so draw all of it — slicing a prefix here was what bunched every
 * line into the left sixth of the frame.
 */
const DRAWN_LINKS = LINKS.length;

const PANEL_W = 960;
const PANEL_H = 250;
const DB_MAX = 500;
const Q_MAX = 126;

const ScatterPanel: React.FC<{
  frame: number;
  top: number;
  title: string;
  note: string;
  pts: [number, number][];
  from: number;
  to: number;
  highlightOffset: number | null;
  igniteAt: number;
}> = ({ frame, top, title, note, pts, from, to, highlightOffset, igniteAt }) => {
  const o =
    interpolate(frame, [from, from + 8], [0, 1], ease) *
    interpolate(frame, [to - 6, to], [1, 0], ease);
  if (o <= 0) return null;
  // 1.33s: slow enough that the cloud reads as points ARRIVING, not as a texture cut in.
  const fill = interpolate(frame, [from, from + 40], [0, 1], ease);
  const n = Math.floor(pts.length * fill);
  const ignite = interpolate(frame, [igniteAt, igniteAt + 30], [0, 1], ease);

  const x = (db: number) => (db / DB_MAX) * PANEL_W;
  const y = (q: number) => PANEL_H - (q / Q_MAX) * PANEL_H;

  const on = highlightOffset === null ? [] : pts.filter(([a, b]) => a - b === highlightOffset);

  return (
    <div style={{ position: 'absolute', left: 60, top, width: PANEL_W, opacity: o }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          marginBottom: 12,
          fontFamily: 'IBM Plex Mono',
          fontSize: 38,
        }}
      >
        <span style={{ color: '#E8E6E1' }}>{title}</span>
        <span style={{ color: highlightOffset === null ? '#81A2C4' : '#FFB020' }}>{note}</span>
      </div>
      <svg width={PANEL_W} height={PANEL_H} style={{ background: '#0E213E' }}>
        {pts.slice(0, n).map(([a, b], i) => (
          <circle key={i} cx={x(a)} cy={y(b)} r={4} fill="#81A2C4" opacity={0.75} />
        ))}
        {ignite > 0 && highlightOffset !== null ? (
          <>
            <line
              x1={x(highlightOffset)}
              y1={y(0)}
              x2={x(highlightOffset + Q_MAX)}
              y2={y(Q_MAX)}
              stroke="#FFB020"
              strokeWidth={4}
              opacity={ignite * 0.9}
            />
            {on.slice(0, Math.floor(on.length * ignite)).map(([a, b], i) => (
              <circle key={`h${i}`} cx={x(a)} cy={y(b)} r={7} fill="#FFB020" />
            ))}
          </>
        ) : null}
      </svg>
    </div>
  );
};

// ── beat 6: the offset histogram + the answer ───────────────────────────────

const Histogram: React.FC<{ frame: number }> = ({ frame }) => {
  const from = t(T.hist);
  const o = interpolate(frame, [from, from + 8], [0, 1], ease);
  if (o <= 0) return null;
  const grow = interpolate(frame, [from + 6, from + 44], [0, 1], ease);
  const maxV = Math.max(...HIST.map((h) => h[1]));
  const bw = PANEL_W / HIST.length;
  const hh = 330;
  return (
    <div style={{ position: 'absolute', left: 60, top: 548, width: PANEL_W, opacity: o }}>
      <div
        style={{
          fontFamily: 'IBM Plex Mono',
          fontSize: 38,
          color: '#81A2C4',
          marginBottom: 12,
        }}
      >
        votes per time offset
      </div>
      <svg width={PANEL_W} height={hh}>
        <line x1={0} y1={hh} x2={PANEL_W} y2={hh} stroke="#274064" strokeWidth={3} />
        {HIST.map(([off, v], i) => {
          const win = off === STATS.best_offset_frames;
          const h = (v / maxV) * (hh - 10) * grow;
          return (
            <rect
              key={i}
              x={i * bw}
              y={hh - h}
              width={Math.max(1.5, bw - 1)}
              height={h}
              fill={win ? '#FFB020' : '#274064'}
            />
          );
        })}
      </svg>
    </div>
  );
};

// ── progress ────────────────────────────────────────────────────────────────

const Progress: React.FC<{ frame: number }> = ({ frame }) => {
  const p = Math.min(1, frame / (DURATION_SECONDS * FPS));
  return (
    <div style={{ position: 'absolute', top: 1790, left: 60, width: 960, height: 6 }}>
      <div style={{ position: 'absolute', width: 960, height: 6, background: '#274064' }} />
      <div style={{ position: 'absolute', width: 960 * p, height: 6, background: '#00D6F7' }} />
    </div>
  );
};

// ── the reel ────────────────────────────────────────────────────────────────

export const Shazam: React.FC = () => {
  const frame = useCurrentFrame();

  // Counters tick up and STOP — they never idle.
  const nPeaks = Math.round(
    interpolate(frame, [t(T.peaksStart), t(T.peaksStart + T.peaksSpan)], [0, STATS.peaks], ease),
  );
  const nHash = Math.round(
    interpolate(frame, [t(T.links[0]), t(T.links[1])], [0, STATS.query_hashes], ease),
  );

  return (
    <AbsoluteFill style={{ backgroundColor: '#040E1F' }}>
      <Audio src={staticFile('reels/r001_audio.wav')} />
      <Header frame={frame} />

      {/* ── 1. the recording ─────────────────────────────────────────────── */}
      <Fade
        from={t(T.cafe[0])}
        to={t(T.cafe[1])}
        style={{
          position: 'absolute',
          top: 462,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Sans',
          fontSize: 46,
          color: '#81A2C4',
        }}
      >
        You hold your phone up in a noisy café.
      </Fade>
      {frame < t(T.waveOut[1]) ? <Waveform frame={frame} /> : null}
      <Fade
        from={t(T.stat[0])}
        to={t(T.stat[1])}
        style={{
          position: 'absolute',
          top: SY + SH + 40,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Mono',
          fontSize: 40,
          color: '#E8E6E1',
        }}
      >
        3.00 s · {fmt(STATS.samples)} samples · unrecognisable
      </Fade>

      {/* ── 2. spectrogram ───────────────────────────────────────────────── */}
      <StepLabel
        n="STEP 1"
        title="The sound becomes a picture"
        sub="Frequency up, time across."
        from={t(T.s1Label[0])}
        to={t(T.s1Label[1])}
      />
      <Spectrogram frame={frame} />
      <Readout
        from={t(T.s1Read[0])}
        to={t(T.s1Read[1])}
        rows={[
          ['stft', '1024-sample window · 256 hop'],
          ['grid', `${STATS.stft_frames} frames × ${STATS.freq_bins} bins`],
        ]}
      />

      {/* ── 3. constellation ─────────────────────────────────────────────── */}
      <StepLabel
        n="STEP 2"
        title="Keep only the loudest points"
        sub="The café noise isn't loudest anywhere. It dies here."
        from={t(T.s2Label[0])}
        to={t(T.s2Label[1])}
      />
      <Constellation frame={frame} />
      <Readout
        from={t(T.s2Read[0])}
        to={t(T.s2Read[1])}
        rows={[
          ['peaks kept', fmt(nPeaks)],
          ['everything else', 'discarded'],
        ]}
      />

      {/* ── 4. hashing ───────────────────────────────────────────────────── */}
      <StepLabel
        n="STEP 3"
        title="Join each point to the next few"
        sub="Every pair becomes one number."
        from={t(T.s3Label[0])}
        to={t(T.s3Label[1])}
      />
      <HashChip frame={frame} />
      <Readout
        from={t(T.s3Read[0])}
        to={t(T.s3Read[1])}
        rows={[
          ['hashes from 3 s', fmt(nHash)],
          ['hashes in the track', fmt(STATS.db_hashes)],
        ]}
      />

      {/* ── 5. the match ─────────────────────────────────────────────────── */}
      <StepLabel
        n="STEP 4"
        title="Do the numbers line up?"
        sub="Compare every hash against the library."
        from={t(T.s4Label[0])}
        to={t(T.s4Label[1])}
      />
      <ScatterPanel
        frame={frame}
        top={548}
        title="A DIFFERENT SONG"
        note={`${STATS.miss_pairs} stray hits`}
        pts={MISS}
        from={t(T.panelA)}
        to={t(T.panelsOut)}
        highlightOffset={null}
        igniteAt={t(99)}
      />
      <ScatterPanel
        frame={frame}
        top={908}
        title="THE RIGHT SONG"
        note={`${fmt(STATS.matched_pairs)} hits`}
        pts={HIT}
        from={t(T.panelB)}
        to={t(T.panelsOut)}
        highlightOffset={STATS.best_offset_frames}
        igniteAt={t(T.ignite)}
      />
      <Fade
        from={t(T.s4Caption[0])}
        to={t(T.s4Caption[1])}
        style={{
          position: 'absolute',
          top: 1268,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Sans',
          fontWeight: 600,
          fontSize: 50,
          color: '#FFB020',
        }}
      >
        A cloud means nothing. A straight line means the same song.
      </Fade>

      {/* ── 6. the answer ────────────────────────────────────────────────── */}
      <StepLabel
        n="STEP 5"
        title="One offset wins"
        sub="That spike is where in the track you were standing."
        from={t(T.s5Label[0])}
        to={t(T.s5Label[1])}
      />
      <Histogram frame={frame} />
      <Fade
        from={t(T.answer)}
        style={{
          position: 'absolute',
          top: 968,
          left: 60,
          width: 960,
          textAlign: 'center',
        }}
      >
        <div style={{ fontFamily: 'Archivo Black', fontSize: 132, color: '#FFB020' }}>
          {STATS.best_offset_seconds.toFixed(2)} s
        </div>
        <div
          style={{
            fontFamily: 'IBM Plex Sans',
            fontSize: 44,
            color: '#81A2C4',
            marginTop: 4,
          }}
        >
          into the song — found in {STATS.matched_pairs} matching hashes
        </div>
      </Fade>
      <Fade
        from={t(T.closing)}
        style={{
          position: 'absolute',
          top: 1300,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Sans',
          fontWeight: 600,
          fontSize: 52,
          color: '#E8E6E1',
        }}
      >
        Your phone did that to 3 seconds
        <br />
        of a noisy room.
      </Fade>

      <Progress frame={frame} />
    </AbsoluteFill>
  );
};

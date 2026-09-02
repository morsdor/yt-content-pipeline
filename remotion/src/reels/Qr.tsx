import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import {
  Fade,
  Progress,
  ReelGround,
  ReelHeader,
  StepLabel,
  ease,
  t,
} from './lib/chrome';
import {
  BLOB,
  BLOB_CX,
  BLOB_CY,
  FUNC,
  MATRIX,
  N,
  OWNER,
  SPECKLE,
  SPECKLE_ORDER,
  STATS,
  type Step,
} from './data/qr';

/**
 * r003 · "How much of this can you destroy?"  (backlog I01)
 *
 * Every number and every damaged module here is measured output from
 * projects/r003_qr/qr_damage.py, which encodes a real QR, rebuilds the
 * module -> codeword -> Reed-Solomon block mapping from the spec, proves it by
 * reconstructing the payload byte for byte, then damages the code and asks
 * OpenCV whether it still reads. Nothing on screen is drawn by hand.
 *
 * The code on screen is live: it encodes https://instagram.com/thedepthfirst,
 * so a viewer who pauses and scans it lands on the account.
 */

export const DURATION_SECONDS = 45;

const T = {
  qrIn: 0.5,
  titleOut: [4.4, 4.8] as [number, number],
  titleIn: [4.8, 5.15] as [number, number],

  s1Label: [5.2, 13.6] as [number, number],
  blobRun: [7.1, 10.4] as [number, number],
  s1Verdict: 10.6,
  s1Out: 13.5,

  s2Label: [13.6, 22.2] as [number, number],
  blockRun: [15.6, 18.4] as [number, number],
  s2Read: 19.0,
  s2Out: 22.1,

  s3Label: [22.2, 31.0] as [number, number],
  speckRun: [24.3, 27.0] as [number, number],
  s3Verdict: 27.2,
  s3Out: 30.9,

  s4Label: [31.0, 39.0] as [number, number],
  cornerRun: [32.8, 34.4] as [number, number],
  s4Verdict: 34.6,
  s4Out: 38.9,

  answer: 39.2,
  caveat: 41.6,
};

// ── geometry: 37 modules at 17px = 629, centred in the rail-safe band ────────
const CELL = 17;
const QW = N * CELL;
// Centred on the FRAME (540), not on the rail-safe band — at 657px total the
// code's right edge lands at 868, still inside the 870 rail limit, so it clears
// the action buttons without looking 75px off-centre.
const QX = 540 - (QW + 28) / 2;
const QY = 690;
const PAD = 14;

/**
 * The accent darkened for a highlighted block's DARK modules. Computed rather
 * than a new hex, so the palette stays closed — same rule the r001/r002 data
 * ramps follow (brand_guide_software.md §3a).
 */
const ACCENT = [173, 136, 255] as const; // #AD88FF
const ACCENT_DARK = `rgb(${ACCENT.map((v) => Math.round(v * 0.42)).join(',')})`;

const at = (r: number, c: number) => r * N + c;
const isDark = (r: number, c: number) => MATRIX[at(r, c)] === '1';
const isFunc = (r: number, c: number) => FUNC[at(r, c)] === '1';

/** The measured verdict at a given damage level — read from the sweep, not assumed. */
const verdictAt = (steps: Step[], pct: number): boolean => {
  let ok = true;
  for (const s of steps) if (s.pct <= pct) ok = s.ok;
  return ok;
};

// ── damage models, recomputed exactly as qr_damage.py generated them ─────────
const blobDamaged = (pct: number): Set<number> => {
  const out = new Set<number>();
  if (pct <= 0) return out;
  const n = Math.round((STATS.dataModules * pct) / 100);
  const rad2 = n / Math.PI;
  for (let r = 0; r < N; r++) {
    for (let c = 0; c < N; c++) {
      if (isFunc(r, c)) continue;
      const d = (r - BLOB_CY) ** 2 + (c - BLOB_CX) ** 2;
      if (d <= rad2) out.add(at(r, c));
    }
  }
  return out;
};

const speckleDamaged = (pct: number): Set<number> => {
  const n = Math.round((STATS.dataModules * pct) / 100);
  const out = new Set<number>();
  for (let i = 0; i < n && i < SPECKLE_ORDER.length; i++) {
    const [r, c] = SPECKLE_ORDER[i];
    out.add(at(r, c));
  }
  return out;
};

/** The nine modules inside a finder corner — 0.7% of the code, and fatal. */
const CORNER: number[] = (() => {
  const out: number[] = [];
  for (let r = 2; r < 5; r++) for (let c = 2; c < 5; c++) out.push(at(r, c));
  return out;
})();

// ── the code itself ─────────────────────────────────────────────────────────

const Code: React.FC<{
  damaged: Set<number>;
  highlightBlock: number | null;
  blockReveal: number;
  markCorner: number;
}> = ({ damaged, highlightBlock, blockReveal, markCorner }) => {
  const cells: React.ReactNode[] = [];
  for (let r = 0; r < N; r++) {
    for (let c = 0; c < N; c++) {
      const i = at(r, c);
      const dark = isDark(r, c);
      const hit = damaged.has(i);
      let fill = dark ? '#040E1F' : '#E8E6E1';
      if (highlightBlock !== null && OWNER[i] === String(highlightBlock)) {
        // reveal this block's modules in reading order, so you watch one
        // Reed-Solomon block scatter itself across the whole square
        const rank = (r * N + c) / (N * N);
        if (rank <= blockReveal) fill = dark ? ACCENT_DARK : '#AD88FF';
      }
      if (hit) fill = '#040E1F';
      cells.push(
        <rect key={i} x={c * CELL} y={r * CELL} width={CELL} height={CELL} fill={fill} />,
      );
    }
  }
  return (
    <svg width={QW + PAD * 2} height={QW + PAD * 2} style={{ display: 'block' }}>
      <rect width={QW + PAD * 2} height={QW + PAD * 2} fill="#E8E6E1" />
      <g transform={`translate(${PAD},${PAD})`}>
        {cells}
        {markCorner > 0 ? (
          <rect
            x={2 * CELL - 5}
            y={2 * CELL - 5}
            width={3 * CELL + 10}
            height={3 * CELL + 10}
            fill="none"
            stroke="#FF4D4D"
            strokeWidth={5}
            opacity={markCorner}
          />
        ) : null}
      </g>
    </svg>
  );
};

/** The independent decoder's answer. This is OpenCV's verdict, not ours. */
const Verdict: React.FC<{ from: number; to?: number; ok: boolean; note: string }> = ({
  from,
  to,
  ok,
  note,
}) => (
  <Fade
    from={t(from)}
    to={to === undefined ? undefined : t(to)}
    style={{ position: 'absolute', top: 1358, left: 60, width: 960, textAlign: 'center' }}
  >
    <div
      style={{
        fontFamily: 'Archivo Black',
        fontSize: 60,
        color: ok ? '#3DDF7D' : '#FF4D4D',
        letterSpacing: -0.5,
      }}
    >
      {ok ? 'STILL SCANS' : "DOESN'T SCAN"}
    </div>
    <div
      style={{
        fontFamily: 'IBM Plex Mono',
        fontSize: 38,
        color: '#81A2C4',
        marginTop: 12,
      }}
    >
      {note}
    </div>
  </Fade>
);

// ── the reel ────────────────────────────────────────────────────────────────

export const Qr: React.FC = () => {
  const frame = useCurrentFrame();

  const blobPct = interpolate(
    frame,
    [t(T.blobRun[0]), t(T.blobRun[1])],
    [0, STATS.blobMax],
    ease,
  );
  const speckPct = interpolate(
    frame,
    [t(T.speckRun[0]), t(T.speckRun[1])],
    [0, STATS.speckleMax + 2],
    ease,
  );
  const blockReveal = interpolate(
    frame,
    [t(T.blockRun[0]), t(T.blockRun[1])],
    [0, 1],
    ease,
  );

  // Each beat's visual outlives its label by half a second, so the code is never
  // bare on screen while one step label hands over to the next. Without this the
  // stage empties for ~0.2s at every seam — the same dead-beat bug r001 shipped.
  const HOLD = 0.5;
  const inBlob = frame >= t(T.blobRun[0]) && frame < t(T.s1Out + HOLD);
  const inBlocks = frame >= t(T.blockRun[0]) && frame < t(T.s2Out + HOLD);
  const inSpeck = frame >= t(T.speckRun[0]) && frame < t(T.s3Out + HOLD);
  const inCorner = frame >= t(T.cornerRun[0]) && frame < t(T.s4Out);

  let damaged = new Set<number>();
  if (inBlob) damaged = blobDamaged(blobPct);
  else if (inSpeck) damaged = speckleDamaged(speckPct);
  else if (inCorner) {
    const k = Math.round(
      interpolate(frame, [t(T.cornerRun[0]), t(T.cornerRun[1])], [0, 9], ease),
    );
    damaged = new Set(CORNER.slice(0, k));
  }

  const qrOpacity = interpolate(
    frame,
    [t(T.qrIn), t(T.qrIn + 0.6), t(T.answer - 0.4), t(T.answer)],
    [0, 1, 1, 0],
    ease,
  );

  return (
    <AbsoluteFill>
      <ReelGround accent="#AD88FF" />

      <ReelHeader
        big={
          <>
            How much of this
            <br />
            can you <span style={{ color: '#AD88FF' }}>destroy</span>?
          </>
        }
        small={
          <>
            How much of this can you <span style={{ color: '#AD88FF' }}>destroy</span>?
          </>
        }
        out={T.titleOut}
        in_={T.titleIn}
      />

      <div style={{ position: 'absolute', top: QY, left: QX, opacity: qrOpacity }}>
        <Code
          damaged={damaged}
          highlightBlock={inBlocks ? 0 : null}
          blockReveal={blockReveal}
          markCorner={
            inCorner
              ? interpolate(frame, [t(T.cornerRun[0]), t(T.cornerRun[0] + 0.5)], [0, 1], ease)
              : 0
          }
        />
      </div>

      {/* ── 1. spill something on it ──────────────────────────────────────── */}
      <StepLabel
        n="STEP 1"
        title="Spill coffee on it"
        sub="A stain grows over the code. Keep scanning."
        from={t(T.s1Label[0])}
        to={t(T.s1Label[1])}
      />
      <Verdict
        from={T.s1Verdict}
        to={T.s1Out}
        ok={verdictAt(BLOB, STATS.blobMax)}
        note={`${STATS.blobMax}% of the code covered`}
      />

      {/* ── 2. why it survives ────────────────────────────────────────────── */}
      <StepLabel
        n="STEP 2"
        title="Nothing is stored in one place"
        sub="One block of the data, lit up where it actually lives."
        from={t(T.s2Label[0])}
        to={t(T.s2Label[1])}
      />
      <Fade
        from={t(T.s2Read)}
        to={t(T.s2Out)}
        style={{
          position: 'absolute',
          top: 1358,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Sans',
          fontSize: 44,
          color: '#E8E6E1',
          lineHeight: 1.3,
        }}
      >
        {STATS.blocks} blocks, each smeared across the whole square.
        <br />
        <span style={{ fontFamily: 'IBM Plex Mono', color: '#81A2C4' }}>
          any {STATS.correctsPerBlock} of {STATS.blockTotal} can be wrong
        </span>
      </Fade>

      {/* ── 3. the same damage, scattered ─────────────────────────────────── */}
      <StepLabel
        n="STEP 3"
        title="Now scatter the same damage"
        sub="Confetti instead of a stain. Far less of it."
        from={t(T.s3Label[0])}
        to={t(T.s3Label[1])}
      />
      <Verdict
        from={T.s3Verdict}
        to={T.s3Out}
        ok={verdictAt(SPECKLE, STATS.speckleMax + 2)}
        note={`dead at ${STATS.speckleMax}% — ${Math.round(
          STATS.blobMax / STATS.speckleMax,
        )}x less than the stain`}
      />

      {/* ── 4. the part nobody expects ────────────────────────────────────── */}
      <StepLabel
        n="STEP 4"
        title="Now touch the corner"
        sub="Nine squares. Not one of them holds your data."
        from={t(T.s4Label[0])}
        to={t(T.s4Label[1])}
      />
      <Verdict
        from={T.s4Verdict}
        to={T.s4Out}
        ok={STATS.cornerOk}
        note={`${STATS.cornerModules} modules — ${STATS.cornerPct}% of the code`}
      />

      {/* ── 5. the answer ─────────────────────────────────────────────────── */}
      <Fade
        from={t(T.answer)}
        style={{
          position: 'absolute',
          top: 780,
          left: 60,
          width: 960,
          textAlign: 'center',
        }}
      >
        <div style={{ fontFamily: 'Archivo Black', fontSize: 92, color: '#AD88FF' }}>
          {STATS.blobMax}% survives
        </div>
        <div
          style={{
            fontFamily: 'IBM Plex Sans',
            fontSize: 48,
            color: '#E8E6E1',
            marginTop: 26,
            lineHeight: 1.35,
          }}
        >
          Most of the square is optional.
          <br />
          Three corners are not.
        </div>
      </Fade>
      <Fade
        from={t(T.caveat)}
        style={{
          position: 'absolute',
          top: 1160,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Sans',
          fontSize: 42,
          color: '#81A2C4',
          lineHeight: 1.35,
        }}
      >
        Measured on a real code at the highest of four
        <br />
        error-correction levels. Your menu is probably lower.
      </Fade>

      <Progress seconds={DURATION_SECONDS} />
    </AbsoluteFill>
  );
};

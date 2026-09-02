import { AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame } from 'remotion';
import {
  Fade,
  Progress,
  ReelGround,
  SAFE_W,
  Readout,
  ReelHeader,
  StepLabel,
  ease,
  fmt,
  t,
} from './lib/chrome';
import {
  CANDIDATES,
  DISTANCE,
  EDITS,
  GRID,
  PATH,
  STATS,
  TARGET,
  TYPO,
} from './data/autocorrect';

/**
 * r002 — "How your phone knows what you meant"  ·  1080x1920, 43s, Instagram/Shorts.
 *
 * ── Computed, not drawn ─────────────────────────────────────────────────────
 * Every number on screen is real output from projects/r002_autocorrect/editdistance.py,
 * run against the real macOS system dictionary at /usr/share/dict/words — 234,454 unique
 * alphabetic words, scanned in 1,035 ms. The 11x11 matrix is a genuine Levenshtein DP
 * table; the highlighted route is a genuine backtrace of the optimal alignment.
 *
 * The typo was chosen BY the data, not for the story. `recieve` was the obvious candidate
 * and was rejected: plain edit distance ranks `relieve` (1) above `receive` (2) and gets
 * the answer wrong. `definately` returns a unique distance-1 match with everything else
 * at 2 — so the reel can be honest and still land.
 *
 * ── The hook rule ───────────────────────────────────────────────────────────
 * The title never says "Levenshtein", "edit distance" or "dynamic programming". It opens
 * on a typo everyone has made (docs/comp_deep_dive_equationverse.md §2: every comp reel
 * that opened on a developer noun died at 2-17k views).
 *
 * ── Pacing ──────────────────────────────────────────────────────────────────
 * Every beat is label-alone (~1.5s) -> animation (2-6s) -> hold on the finished state
 * (~2s). r001's first cut ran all three at once and was unreadable; see the
 * `explainer-pacing-read-animate-hold` note. The table gets 16s because it is the reel.
 *
 * ── The camera ──────────────────────────────────────────────────────────────
 * There isn't one. Locked for all 43 seconds.
 */

export const DURATION_SECONDS = 43;

/** Beat timing in seconds. Every time value in this file lives here. */
const T = {
  // beat 1 · the typo ....................................... 0.0 - 5.6
  typeWord: [0.7, 2.6],
  squiggle: [3.0, 3.6],
  notAWord: [3.9, 5.9],
  titleOut: [4.7, 5.1],
  titleIn: [5.1, 5.45],

  // beat 2 · it isn't a word ................................ 5.8 - 13.4
  s1Label: [5.75, 13.4],
  scan: [7.3, 10.3],
  noMatch: [10.8, 13.4],
  s1Read: [10.8, 13.4],

  // beat 3 · the table ..................................... 13.6 - 29.5
  s2Label: [13.6, 29.5],
  gridIn: [15.1, 16.0],
  seed: [16.2, 17.2],
  fill: [17.4, 23.4],
  path: [23.9, 25.7],
  corner: [26.0, 26.6],
  tableOut: [29.5, 30.1],

  // beat 4 · the ranking ................................... 29.7 - 36.5
  s3Label: [29.7, 36.5],
  ranks: 31.2,
  rankOut: 36.5,

  // beat 5 · the answer .................................... 36.7 - 43.0
  s4Label: [36.7, 43.0],
  answer: 38.2,
  caveat: 40.2,
} as const;

// ── table geometry ──────────────────────────────────────────────────────────
// 12 visual columns: one row-letter gutter + 11 number columns (j = 0..10).
// Sized against the Instagram safe area, not the canvas: 12 columns of 58 is
// 696px, which centres inside SAFE_W (810) leaving the right-hand action rail
// clear, and stacks 12 rows from TY=690 to 1386 — inside SAFE_BOTTOM (1540)
// with room for the "One substitution" line beneath it. The +26 is the
// row-letter gutter.
const CELL = 58;
const TX = 60 + (SAFE_W - CELL * 12) / 2 + 26;
const TY = 690;
const cx = (j: number) => TX + (j + 1) * CELL;
const cy = (i: number) => TY + (i + 1) * CELL;


/**
 * Cell colour encodes the distance VALUE, which is what a DP table is actually for:
 * the low-value valley running down the diagonal IS the answer's shape, and in one
 * flat colour you have to read 121 numbers to find it.
 *
 * The stops are the brand's own accents (green -> cyan -> blue -> receding), built as
 * rgb() rather than hex literals, because this is a data channel and not a palette
 * addition — which is also why `brand:check` has nothing to say about it.
 */
const STOPS: [number, [number, number, number]][] = [
  [0, [61, 223, 125]], // #3DDF7D — identical prefixes
  [2, [0, 214, 247]], // #00D6F7
  [5, [81, 164, 255]], // #51A4FF
  [10, [39, 64, 100]], // receding into the grid
];

const heat = (v: number): string => {
  let a = STOPS[0];
  let b = STOPS[STOPS.length - 1];
  for (let k = 0; k < STOPS.length - 1; k++) {
    if (v >= STOPS[k][0] && v <= STOPS[k + 1][0]) {
      a = STOPS[k];
      b = STOPS[k + 1];
      break;
    }
  }
  const f = b[0] === a[0] ? 0 : (v - a[0]) / (b[0] - a[0]);
  const c = a[1].map((ch, k) => Math.round(ch + (b[1][k] - ch) * f));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
};

/** Only the low end gets a filled block, so the valley reads as a shape. */
const heatAlpha = (v: number) => Math.max(0, 0.62 * (1 - v / 6) ** 1.15);

/** The one position where the two words diverge (0-indexed into each word). */
const DIFF = EDITS[0].i - 1;

// ── beat 1 ──────────────────────────────────────────────────────────────────

const TypedWord: React.FC<{ frame: number }> = ({ frame }) => {
  const n = Math.floor(
    interpolate(frame, [t(T.typeWord[0]), t(T.typeWord[1])], [0, TYPO.length], ease),
  );
  const out = interpolate(frame, [t(T.notAWord[1] - 0.4), t(T.notAWord[1])], [1, 0], ease);
  const sq = interpolate(frame, [t(T.squiggle[0]), t(T.squiggle[1])], [0, 1], ease);
  const caret = frame < t(T.typeWord[1]) && Math.floor(frame / 8) % 2 === 0;

  // A spellcheck squiggle, drawn rather than dotted-bordered so it can draw ON.
  const w = 560;
  const x0 = (1080 - w) / 2;
  const wave = Array.from({ length: 60 }, (_, k) => {
    const x = x0 + (k / 59) * w * sq;
    return `${x},${784 + (k % 2 === 0 ? -5 : 5)}`;
  }).join(' ');

  return (
    <div style={{ position: 'absolute', opacity: out }}>
      <div
        style={{
          position: 'absolute',
          top: 840,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Mono',
          fontSize: 78,
          color: '#E8E6E1',
          letterSpacing: 4,
        }}
      >
        {TYPO.slice(0, n)}
        <span style={{ color: '#FFB020', opacity: caret ? 1 : 0 }}>|</span>
      </div>
      {sq > 0 ? (
        <svg width={1080} height={1920} style={{ position: 'absolute' }}>
          <polyline points={wave} fill="none" stroke="#FFB020" strokeWidth={5} />
        </svg>
      ) : null}
    </div>
  );
};

// ── beat 2 ──────────────────────────────────────────────────────────────────

const DictScan: React.FC<{ frame: number }> = ({ frame }) => {
  const o = interpolate(frame, [t(T.scan[0]), t(T.scan[0] + 0.4)], [0, 1], ease);
  const out = interpolate(frame, [t(T.s1Label[1] - 0.5), t(T.s1Label[1])], [1, 0], ease);
  if (o <= 0) return null;
  const p = interpolate(frame, [t(T.scan[0]), t(T.scan[1])], [0, 1], ease);
  const seen = Math.round(p * STATS.dict_size);
  return (
    <div style={{ position: 'absolute', opacity: o * out }}>
      <div
        style={{
          position: 'absolute',
          top: 810,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Mono',
          fontSize: 96,
          color: '#00D6F7',
        }}
      >
        {fmt(seen)}
      </div>
      <div
        style={{
          position: 'absolute',
          top: 940,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Sans',
          fontSize: 42,
          color: '#81A2C4',
        }}
      >
        words checked
      </div>
      <div style={{ position: 'absolute', top: 1030, left: 160, width: 760, height: 8 }}>
        <div style={{ position: 'absolute', width: 760, height: 8, background: '#274064' }} />
        <div style={{ position: 'absolute', width: 760 * p, height: 8, background: '#00D6F7' }} />
      </div>
    </div>
  );
};

// ── beat 3 · the DP table ───────────────────────────────────────────────────

const Table: React.FC<{ frame: number }> = ({ frame }) => {
  const o = interpolate(frame, [t(T.gridIn[0]), t(T.gridIn[1])], [0, 1], ease);
  const out = interpolate(frame, [t(T.tableOut[0]), t(T.tableOut[1])], [1, 0], ease);
  if (o <= 0 || out <= 0) return null;

  const seedP = interpolate(frame, [t(T.seed[0]), t(T.seed[1])], [0, 1], ease);
  const fillP = interpolate(frame, [t(T.fill[0]), t(T.fill[1])], [0, 1], ease);
  const pathP = interpolate(frame, [t(T.path[0]), t(T.path[1])], [0, 1], ease);
  const cornerP = interpolate(frame, [t(T.corner[0]), t(T.corner[1])], [0, 1], ease);

  const nPath = Math.floor(PATH.length * pathP);
  const onPath = new Set(PATH.slice(0, nPath).map((p) => `${p.i},${p.j}`));
  const editKey = `${EDITS[0].i},${EDITS[0].j}`;

  const cells = [];
  for (let i = 0; i <= 10; i++) {
    for (let j = 0; j <= 10; j++) {
      const isSeed = i === 0 || j === 0;
      // Seeds are the base case — they appear together. Computed cells fill
      // row by row, left to right, which is the real evaluation order.
      const vis = isSeed
        ? seedP
        : ((i - 1) * 10 + (j - 1)) / 100 <= fillP
          ? 1
          : 0;
      if (vis <= 0) continue;
      const key = `${i},${j}`;
      const lit = onPath.has(key);
      const isEdit = key === editKey && pathP > 0;
      const isCorner = i === 10 && j === 10;
      cells.push(
        <g key={key} opacity={vis}>
          {heatAlpha(GRID[i][j]) > 0.01 ? (
            <rect
              x={cx(j) - CELL / 2 + 3}
              y={cy(i) - CELL / 2 + 3}
              width={CELL - 6}
              height={CELL - 6}
              fill={heat(GRID[i][j])}
              opacity={heatAlpha(GRID[i][j])}
            />
          ) : null}
          {lit ? (
            <rect
              x={cx(j) - CELL / 2 + 3}
              y={cy(i) - CELL / 2 + 3}
              width={CELL - 6}
              height={CELL - 6}
              fill={isEdit ? '#FFB020' : 'transparent'}
              stroke={isEdit ? '#FFB020' : '#E8E6E1'}
              strokeWidth={3}
              opacity={isEdit ? 0.95 : 0.85}
            />
          ) : null}
          {isCorner && cornerP > 0 ? (
            <rect
              x={cx(j) - CELL / 2 + 3}
              y={cy(i) - CELL / 2 + 3}
              width={CELL - 6}
              height={CELL - 6}
              fill="#FFB020"
              opacity={cornerP * 0.9}
            />
          ) : null}
          <text
            x={cx(j)}
            y={cy(i) + 14}
            textAnchor="middle"
            fontFamily="IBM Plex Mono"
            fontSize={38}
            fill={
              isEdit || (isCorner && cornerP > 0.5)
                ? '#040E1F'
                : isSeed
                  ? '#81A2C4'
                  : heat(GRID[i][j])
            }
          >
            {GRID[i][j]}
          </text>
        </g>,
      );
    }
  }

  return (
    <svg width={1080} height={1920} style={{ position: 'absolute', opacity: o * out }}>
      {/* the two words, as row and column headers */}
      {TARGET.split('').map((ch, k) => (
        <text
          key={`c${k}`}
          x={cx(k + 1)}
          y={TY + 14}
          textAnchor="middle"
          fontFamily="IBM Plex Mono"
          fontSize={40}
          fill={k === DIFF ? '#FFB020' : '#00D6F7'}
        >
          {ch}
        </text>
      ))}
      {TYPO.split('').map((ch, k) => (
        <text
          key={`r${k}`}
          x={TX}
          y={cy(k + 1) + 14}
          textAnchor="middle"
          fontFamily="IBM Plex Mono"
          fontSize={40}
          fill={k === DIFF ? '#FFB020' : '#E8E6E1'}
        >
          {ch}
        </text>
      ))}
      {cells}
    </svg>
  );
};

// ── beat 4 · the ranking ────────────────────────────────────────────────────

const Ranking: React.FC<{ frame: number }> = ({ frame }) => {
  const out = interpolate(frame, [t(T.rankOut - 0.5), t(T.rankOut)], [1, 0], ease);
  if (frame < t(T.ranks) || out <= 0) return null;
  return (
    <div style={{ position: 'absolute', top: 750, left: 60, width: 960, opacity: out }}>
      {CANDIDATES.map((c, k) => {
        const at = t(T.ranks) + k * 7;
        const o = interpolate(frame, [at, at + 8], [0, 1], ease);
        if (o <= 0) return null;
        const win = k === 0;
        return (
          <div
            key={c.word}
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              opacity: o,
              background: win ? '#0E213E' : 'transparent',
              borderLeft: win ? '6px solid #FFB020' : '6px solid #274064',
              padding: '20px 28px',
              marginBottom: 12,
            }}
          >
            <span
              style={{
                fontFamily: 'IBM Plex Mono',
                fontSize: 52,
                color: win ? '#FFB020' : '#81A2C4',
              }}
            >
              {c.word}
            </span>
            <span
              style={{
                fontFamily: 'IBM Plex Mono',
                fontSize: 52,
                color: win ? '#FFB020' : '#81A2C4',
              }}
            >
              {c.d}
            </span>
          </div>
        );
      })}
    </div>
  );
};

// ── the reel ────────────────────────────────────────────────────────────────

export const Autocorrect: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill>
      <ReelGround accent="#00D6F7" />
      <Audio src={staticFile('reels/r002_audio.wav')} />
      <ReelHeader
        big={
          <>
            How your phone knows
            <br />
            what you <span style={{ color: '#00D6F7' }}>meant</span>
          </>
        }
        small={
          <>
            How your phone knows what you <span style={{ color: '#00D6F7' }}>meant</span>
          </>
        }
        out={[T.titleOut[0], T.titleOut[1]]}
        in_={[T.titleIn[0], T.titleIn[1]]}
      />

      {/* ── 1. the typo ──────────────────────────────────────────────────── */}
      {frame < t(T.notAWord[1]) ? <TypedWord frame={frame} /> : null}
      <Fade
        from={t(T.notAWord[0])}
        to={t(T.notAWord[1])}
        style={{
          position: 'absolute',
          top: 1010,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Sans',
          fontSize: 46,
          color: '#81A2C4',
        }}
      >
        You have typed this. You did not mean it.
      </Fade>

      {/* ── 2. it isn't a word ───────────────────────────────────────────── */}
      <StepLabel
        n="STEP 1"
        title="It isn't a word"
        sub="Your phone checks every word it knows."
        from={t(T.s1Label[0])}
        to={t(T.s1Label[1])}
      />
      <DictScan frame={frame} />
      <Fade
        from={t(T.noMatch[0])}
        to={t(T.noMatch[1])}
        style={{
          position: 'absolute',
          top: 1110,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Sans',
          fontWeight: 600,
          fontSize: 56,
          color: '#FFB020',
        }}
      >
        No match.
      </Fade>
      <Readout
        from={t(T.s1Read[0])}
        to={t(T.s1Read[1])}
        rows={[
          ['dictionary', `${fmt(STATS.dict_size)} words`],
          ['scan time', `${STATS.search_ms} ms`],
        ]}
      />

      {/* ── 3. the table ─────────────────────────────────────────────────── */}
      <StepLabel
        n="STEP 2"
        title="How far is it from a real word?"
        sub="Count the single-letter edits, one prefix at a time."
        from={t(T.s2Label[0])}
        to={t(T.s2Label[1])}
      />
      <Table frame={frame} />
      <Fade
        from={t(T.corner[1])}
        to={t(T.s2Label[1])}
        style={{
          position: 'absolute',
          top: 1420,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Sans',
          fontWeight: 600,
          fontSize: 50,
          color: '#FFB020',
        }}
      >
        One substitution. Distance {DISTANCE}.
      </Fade>

      {/* ── 4. the ranking ───────────────────────────────────────────────── */}
      <StepLabel
        n="STEP 3"
        title="Rank every word within two edits"
        sub="Out of 234,454, only five come close."
        from={t(T.s3Label[0])}
        to={t(T.s3Label[1])}
      />
      <Ranking frame={frame} />

      {/* ── 5. the answer ────────────────────────────────────────────────── */}
      <StepLabel
        n="STEP 4"
        title="One letter away"
        sub="And nothing else is."
        from={t(T.s4Label[0])}
        to={t(T.s4Label[1])}
      />
      <Fade
        from={t(T.answer)}
        style={{
          position: 'absolute',
          top: 850,
          left: 60,
          width: 960,
          textAlign: 'center',
        }}
      >
        <div style={{ fontFamily: 'Archivo Black', fontSize: 96, color: '#FFB020' }}>
          {TARGET}
        </div>
        <div
          style={{
            fontFamily: 'IBM Plex Mono',
            fontSize: 44,
            color: '#81A2C4',
            marginTop: 18,
          }}
        >
          {TYPO} → {TARGET}
        </div>
      </Fade>
      <Fade
        from={t(T.caveat)}
        style={{
          position: 'absolute',
          top: 1230,
          left: 60,
          width: 960,
          textAlign: 'center',
          fontFamily: 'IBM Plex Sans',
          fontSize: 46,
          color: '#E8E6E1',
          lineHeight: 1.35,
        }}
      >
        Distance gets you the shortlist.
        <br />
        <span style={{ color: '#81A2C4' }}>
          How often people actually type a word picks the winner.
        </span>
      </Fade>

      <Progress seconds={DURATION_SECONDS} />
    </AbsoluteFill>
  );
};

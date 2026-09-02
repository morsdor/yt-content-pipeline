"""
r001 — "How Shazam names a song in 3 seconds"

A real audio-fingerprinting implementation (Wang 2003, the Shazam paper) whose
intermediate state is dumped to JSON so the Remotion reel can draw the algorithm
actually running, rather than an illustration of it running.

Nothing here is faked for the video: the spectrogram is a real STFT, the peaks are
real local maxima, the hashes are real (f1, f2, dt) triples, and the diagonal that
appears in the final beat is the genuine scatter of matched-hash time pairs.

No audio files are read — the "song" is synthesised, so the reel carries no
copyright risk and the whole pipeline is reproducible from this one file.

    python3 fingerprint.py            # writes shazam_data.json
"""

import json
import math
import pathlib
import time

import numpy as np

SR = 11025          # sample rate — Shazam works fine on heavily downsampled audio
N_FFT = 1024
HOP = 256
RNG = np.random.default_rng(7)

# ── 1. synthesise a "song" ───────────────────────────────────────────────────
# Sustained harmonic chords give horizontal spectrogram lines; percussion gives
# vertical ones. That mix is what makes a spectrogram legible at a glance.

def _adsr(n, attack=0.01, release=0.3):
    env = np.ones(n)
    a = int(attack * SR)
    r = int(release * SR)
    if a: env[:a] = np.linspace(0, 1, a)
    if r: env[-r:] = np.linspace(1, 0, r)
    return env


def _tone(freq, dur, amp=1.0, harmonics=5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for h in range(1, harmonics + 1):
        sig += (amp / h ** 1.4) * np.sin(2 * np.pi * freq * h * t)
    return sig * _adsr(n)


def _kick(dur=0.18):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 110 * np.exp(-28 * t)                       # pitch drop
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-22 * t)


def _hat(dur=0.06):
    n = int(dur * SR)
    return RNG.normal(0, 1, n) * np.exp(-70 * np.arange(n) / SR) * 0.5


def synth_song(chords, melody, beats, seconds):
    """chords: list of (root_hz, start_s, dur_s); melody: (hz, start, dur)."""
    out = np.zeros(int(seconds * SR))

    def add(sig, start):
        i = int(start * SR)
        j = min(len(out), i + len(sig))
        out[i:j] += sig[: j - i]

    for root, st, dur in chords:
        for ratio, amp in ((1.0, 0.5), (1.25, 0.38), (1.5, 0.34)):  # major triad
            add(_tone(root * ratio, dur, amp), st)
    for hz, st, dur in melody:
        add(_tone(hz, dur, 0.55, harmonics=7), st)
    for st, kind in beats:
        add(_kick() * 0.9 if kind == "k" else _hat() * 0.7, st)

    return out / (np.max(np.abs(out)) + 1e-9)


def track_a(seconds=12.0):
    prog = [220.0, 261.63, 196.0, 246.94]           # A  C  G  B
    chords = [(prog[i % 4], i * 1.5, 1.45) for i in range(int(seconds / 1.5))]
    scale = [440.0, 523.25, 587.33, 659.25, 493.88, 392.0]
    melody = [(scale[i % 6], 0.35 + i * 0.5, 0.45) for i in range(int(seconds / 0.5) - 1)]
    beats = []
    t = 0.0
    while t < seconds:
        beats.append((t, "k"))
        beats.append((t + 0.375, "h"))
        beats.append((t + 0.75, "h"))
        t += 0.75
    return synth_song(chords, melody, beats, seconds)


def track_b(seconds=12.0):
    """A different song — used to show what a NON-match scatter looks like."""
    prog = [174.61, 233.08, 155.56, 207.65]
    chords = [(prog[i % 4], i * 1.1, 1.05) for i in range(int(seconds / 1.1))]
    scale = [349.23, 415.30, 466.16, 311.13, 392.0]
    melody = [(scale[i % 5], 0.2 + i * 0.62, 0.5) for i in range(int(seconds / 0.62) - 1)]
    beats = [(t, "k" if i % 2 == 0 else "h")
             for i, t in enumerate(np.arange(0, seconds, 0.55))]
    return synth_song(chords, melody, beats, seconds)


# ── 2. STFT → spectrogram ────────────────────────────────────────────────────

F_MAX_BIN = 224          # ~2.4 kHz — above this the synth track is near-silent


def spectrogram(x):
    win = np.hanning(N_FFT)
    frames = 1 + (len(x) - N_FFT) // HOP
    S = np.empty((N_FFT // 2 + 1, frames), dtype=np.float32)
    for i in range(frames):
        seg = x[i * HOP: i * HOP + N_FFT] * win
        S[:, i] = np.abs(np.fft.rfft(seg))
    return 20 * np.log10(S[:F_MAX_BIN] + 1e-6)   # dB, band-limited


# ── 3. constellation map — local maxima in the time-frequency plane ──────────

def find_peaks(S, f_bins=14, t_bins=9, min_db=None):
    """A point is a peak if it is the loudest cell in its (f_bins x t_bins) box."""
    if min_db is None:
        min_db = np.percentile(S, 62)
    peaks = []
    nf, nt = S.shape
    for f0 in range(0, nf, f_bins):
        for t0 in range(0, nt, t_bins):
            box = S[f0:f0 + f_bins, t0:t0 + t_bins]
            if box.size == 0:
                continue
            idx = np.unravel_index(np.argmax(box), box.shape)
            val = box[idx]
            if val >= min_db:
                peaks.append((int(t0 + idx[1]), int(f0 + idx[0]), float(val)))
    peaks.sort()
    return peaks


# ── 4. hashing — anchor point paired into a forward target zone ──────────────

FAN = 8
DT_MIN, DT_MAX = 1, 40
DF_MAX = 70


def hashes(peaks):
    """Returns {hash: [t_anchor,...]} plus the (anchor,target) links for drawing."""
    table, links = {}, []
    for i, (t1, f1, _) in enumerate(peaks):
        paired = 0
        for j in range(i + 1, len(peaks)):
            t2, f2, _ = peaks[j]
            dt = t2 - t1
            if dt < DT_MIN:
                continue
            if dt > DT_MAX:
                break
            if abs(f2 - f1) > DF_MAX:
                continue
            # 32-bit-ish packed triple, exactly the Wang 2003 shape
            h = (f1 & 0x3FF) << 22 | (f2 & 0x3FF) << 12 | (dt & 0xFFF)
            table.setdefault(h, []).append(t1)
            links.append((i, j))
            paired += 1
            if paired >= FAN:
                break
    return table, links


# ── 5. matching — histogram of (database_time - query_time) offsets ──────────

def match(db, q):
    pairs, offsets = [], {}
    for h, q_times in q.items():
        if h not in db:
            continue
        for dt_db in db[h]:
            for dt_q in q_times:
                pairs.append((int(dt_db), int(dt_q)))
                o = int(dt_db - dt_q)
                offsets[o] = offsets.get(o, 0) + 1
    if not offsets:
        return pairs, None, 0, offsets
    best = max(offsets, key=offsets.get)
    return pairs, best, offsets[best], offsets


# ── 6. run it ────────────────────────────────────────────────────────────────

def main():
    t_wall = time.perf_counter()

    song = track_a(12.0)
    other = track_b(12.0)

    # the query: 3 seconds recorded in a noisy room
    q_start = 4.2
    clip = song[int(q_start * SR): int((q_start + 3.0) * SR)].copy()
    noise = RNG.normal(0, 0.11, len(clip))
    rumble = np.cumsum(RNG.normal(0, 0.02, len(clip)))          # pink-ish café hum
    rumble /= np.max(np.abs(rumble)) + 1e-9
    query = clip * 0.80 + noise + rumble * 0.22
    query /= np.max(np.abs(query)) + 1e-9

    S_song, S_other, S_query = spectrogram(song), spectrogram(other), spectrogram(query)
    p_song, p_other, p_query = find_peaks(S_song), find_peaks(S_other), find_peaks(S_query)
    db_a, links_a = hashes(p_song)
    db_b, _ = hashes(p_other)
    q_tab, links_q = hashes(p_query)

    hit_pairs, offset, votes, hist = match(db_a, q_tab)
    miss_pairs, _, miss_votes, _ = match(db_b, q_tab)

    elapsed_ms = (time.perf_counter() - t_wall) * 1000.0

    # ---- pack for the renderer -------------------------------------------------
    def grid(S, max_t=170, max_f=110):
        """Downsample to a drawable grid, normalised 0..1."""
        nf, nt = S.shape
        fi = np.linspace(0, nf - 1, max_f).astype(int)
        ti = np.linspace(0, nt - 1, min(max_t, nt)).astype(int)
        g = S[np.ix_(fi, ti)]
        lo, hi = np.percentile(g, 58), np.percentile(g, 99.7)
        g = np.clip((g - lo) / (hi - lo + 1e-9), 0, 1)
        return np.round(g, 3).tolist(), len(ti), len(fi)

    q_grid, q_nt, q_nf = grid(S_query)
    nf_full = S_query.shape[0]
    nt_full = S_query.shape[1]

    peaks_norm = [
        {"t": round(t / max(nt_full - 1, 1), 4),
         "f": round(f / max(nf_full - 1, 1), 4),
         "db": round(v, 1)}
        for t, f, v in p_query
    ]
    # keep link list drawable
    # Stride-sample rather than take a prefix: links are generated anchor-by-anchor
    # in time order, so [:600] is the first ~75 peaks — i.e. only the LEFT THIRD of
    # the frame. Striding spreads the drawn subset across the whole clip.
    step = max(1, len(links_q) // 340)
    links_draw = [[a, b] for a, b in links_q[::step]][:340]

    hz_per_bin = (SR / 2) / (N_FFT // 2)
    sec_per_frame = HOP / SR

    data = {
        "meta": {
            "sample_rate": SR, "n_fft": N_FFT, "hop": HOP,
            "hz_per_bin": round(hz_per_bin, 2),
            "sec_per_frame": round(sec_per_frame, 5),
            "query_seconds": 3.0,
            "query_offset_true": q_start,
            "elapsed_ms": round(elapsed_ms, 1),
            "fan": FAN, "dt_min": DT_MIN, "dt_max": DT_MAX, "df_max": DF_MAX,
        },
        "stats": {
            "samples": int(len(query)),
            "stft_frames": nt_full,
            "freq_bins": nf_full,
            "peaks": len(p_query),
            "query_hashes": len(q_tab),
            "db_hashes": len(db_a),
            "db_hashes_other": len(db_b),
            "matched_pairs": len(hit_pairs),
            "miss_pairs": len(miss_pairs),
            "best_offset_frames": offset,
            "best_offset_seconds": round((offset or 0) * sec_per_frame, 2),
            "votes": votes,
            "miss_votes": miss_votes,
        },
        "waveform": np.round(
            query[:: max(1, len(query) // 480)][:480].astype(float), 4
        ).tolist(),
        "spectrogram": {"grid": q_grid, "nt": q_nt, "nf": q_nf},
        "peaks": peaks_norm,
        "links": links_draw,
        "scatter_hit": [[int(a), int(b)] for a, b in hit_pairs][:900],
        "scatter_miss": [[int(a), int(b)] for a, b in miss_pairs][:900],
        "histogram": sorted(([int(k), int(v)] for k, v in hist.items()), key=lambda r: r[0]),
    }

    out = pathlib.Path(__file__).with_name("shazam_data.json")
    out.write_text(json.dumps(data))

    print(f"query           : {q_start:.1f}s .. {q_start + 3:.1f}s of track A + noise")
    print(f"STFT            : {nt_full} frames x {nf_full} bins ({sec_per_frame*1000:.1f} ms/frame, {hz_per_bin:.1f} Hz/bin)")
    print(f"peaks (query)   : {len(p_query)}")
    print(f"hashes  query   : {len(q_tab)}   db(A) {len(db_a)}   db(B) {len(db_b)}")
    print(f"MATCH vs A      : {len(hit_pairs)} pairs, best offset {offset} frames "
          f"({(offset or 0)*sec_per_frame:.2f}s, true {q_start}s), {votes} votes")
    print(f"match vs B      : {len(miss_pairs)} pairs, best cluster {miss_votes} votes")
    print(f"wall clock      : {elapsed_ms:.1f} ms")
    print(f"wrote {out.name} ({out.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()

"""Audio bed for r002 — synthesised, so the reel carries no licensing risk.

Deliberately a BED, not a score: a low drone that resolves major at the answer,
keyboard clicks under the typing, and one soft marker per DP row as the table fills.
Everything sits well under the visuals — a reel that is silent underperforms on
Instagram, but a reel whose audio competes with a 121-cell table is worse.
"""
import wave
import numpy as np

SR = 22050
DUR = 43.0
n = int(DUR * SR)
tt = np.arange(n) / SR
rng = np.random.default_rng(11)
out = np.zeros(n)


def add(sig, at):
    i = int(at * SR)
    j = min(n, i + len(sig))
    out[i:j] += sig[: j - i]


def click(dur=0.045, hz=1900):
    m = int(dur * SR)
    e = np.exp(-90 * np.arange(m) / SR)
    return (rng.normal(0, 0.5, m) * 0.5 + np.sin(2 * np.pi * hz * np.arange(m) / SR)) * e


def tone(hz, dur, amp=0.1, attack=0.4, release=1.2):
    m = int(dur * SR)
    x = np.arange(m) / SR
    env = np.ones(m)
    a, r = int(attack * SR), int(release * SR)
    if a:
        env[:a] = np.linspace(0, 1, a)
    if r:
        env[-r:] = np.linspace(1, 0, r)
    return amp * (np.sin(2 * np.pi * hz * x) + 0.32 * np.sin(4 * np.pi * hz * x)) * env


# ── drone: A2 + E3, unresolved, for most of the reel ────────────────────────
add(tone(110.0, 38.5, 0.085, attack=1.6, release=3.0), 0.4)
add(tone(164.81, 38.5, 0.055, attack=2.4, release=3.0), 0.4)

# ── beat 1: ten keystrokes, matching T.typeWord [0.7, 2.6] ──────────────────
for k in range(10):
    add(click() * 0.30, 0.7 + k * (1.9 / 10))
# the squiggle — a soft low "that's wrong"
add(tone(87.31, 1.1, 0.10, attack=0.02, release=0.9), 3.0)

# ── beat 2: the dictionary scan, 7.3 -> 10.3 ────────────────────────────────
for k in range(26):
    add(click(0.02, 3200) * 0.06, 7.3 + k * (3.0 / 26))
add(tone(98.0, 1.4, 0.10, attack=0.02, release=1.2), 10.8)     # "no match"

# ── beat 3: one soft marker per DP row as the fill sweeps, 17.4 -> 23.4 ─────
for k in range(10):
    add(tone(392.0 + k * 16, 0.22, 0.030, attack=0.01, release=0.2), 17.4 + k * 0.6)
add(tone(523.25, 1.6, 0.075, attack=0.02, release=1.4), 26.0)   # the corner lands

# ── beat 5: the drone resolves major under the answer ───────────────────────
for hz, amp in ((110.0, 0.085), (138.59, 0.06), (164.81, 0.06), (220.0, 0.045)):
    add(tone(hz, 5.0, amp, attack=0.6, release=3.4), 37.9)

out /= np.max(np.abs(out)) + 1e-9
out *= 0.72
out[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))

pcm = (np.clip(out, -1, 1) * 32000).astype(np.int16)
path = "../../remotion/public/reels/r002_audio.wav"
with wave.open(path, "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(f"wrote {path}  {DUR}s @ {SR} Hz  ({len(pcm)*2/1024:.0f} KB)")

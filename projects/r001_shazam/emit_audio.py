"""Render the reel's audio bed from the same synthesiser the fingerprinter used.

The arc mirrors the picture: you first hear what the PHONE hears — 3 seconds of a
noisy room — and at the moment the spectrogram resolves, it crossfades to the clean
track. Because both come from fingerprint.py's synthesiser, the audio under the reel
is literally the signal being fingerprinted on screen, and it is synthesised rather
than sampled, so the reel carries no music licensing risk.
"""
import wave
import numpy as np
import fingerprint as fp

OUT_SR = 22050
DUR = 40.0
SWAP = 6.9          # matches T.specWipe[0] in Shazam.tsx
XF = 0.35

song = fp.track_a(40.0)                       # clean, long enough for the whole reel
rng = np.random.default_rng(7)

clip = song[int(4.2 * fp.SR): int(7.2 * fp.SR)].copy()
noise = rng.normal(0, 0.11, len(clip))
rumble = np.cumsum(rng.normal(0, 0.02, len(clip)))
rumble /= np.max(np.abs(rumble)) + 1e-9
noisy = clip * 0.80 + noise + rumble * 0.22
noisy /= np.max(np.abs(noisy)) + 1e-9

n = int(DUR * fp.SR)
out = np.zeros(n)

# beat 1 — the room recording, held under the title
head = int((SWAP + XF) * fp.SR)
rep = int(np.ceil(head / len(noisy)))
out[:head] = np.tile(noisy, rep)[:head] * 0.85

# beats 2-6 — the clean track, from the point the query was cut
tail_src = np.tile(song, 3)[int(4.2 * fp.SR):]
tail = tail_src[: n - int(SWAP * fp.SR)]
out[int(SWAP * fp.SR):] += tail * 0.55

# crossfade the seam
a, b = int(SWAP * fp.SR), int((SWAP + XF) * fp.SR)
ramp = np.linspace(1, 0, b - a)
out[a:b] *= 0.55 + 0.45 * (1 - ramp)

# gentle fade at the very end so the reel doesn't clip on loop
f = int(0.6 * fp.SR)
out[-f:] *= np.linspace(1, 0, f)
out /= np.max(np.abs(out)) + 1e-9

# resample to OUT_SR and write 16-bit mono
idx = np.linspace(0, len(out) - 1, int(DUR * OUT_SR))
res = np.interp(idx, np.arange(len(out)), out)
pcm = (np.clip(res, -1, 1) * 32000).astype(np.int16)

path = "../../remotion/public/reels/r001_audio.wav"
with wave.open(path, "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(OUT_SR)
    w.writeframes(pcm.tobytes())
print(f"wrote {path}  {DUR}s @ {OUT_SR} Hz  ({len(pcm)*2/1024:.0f} KB)")

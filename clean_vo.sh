#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# clean_vo.sh — local, ₹0 VO cleanup + finishing for The Engineering Atlas.
#
# Chain:  high-pass → de-click → denoise → de-ess → gentle compression
#         → EBU R128 loudness normalize to -14 LUFS (two-pass, YouTube target)
#
# ⚠ IMPORTANT — what ffmpeg CAN'T do:
#   • REVERB / room echo  — ffmpeg has no true de-reverb. A boxy/echoey take
#     will still sound roomy after this. Fix reverb FIRST with an AI pass:
#       - Adobe Podcast "Enhance Speech" (free, web) or Premiere's Enhance Speech
#       - or a local model: resemble-enhance  (ask Claude to set it up, stays ₹0)
#     …then run THIS script on the result to denoise-tidy + hit -14 LUFS.
#   • One-off sounds (a passing car, a bird) — steady-noise denoisers won't
#     remove them; de-click catches taps/mouth-clicks, not traffic.
#
# So the recommended pipeline for a reverby/traffic take is:
#     raw.m4a  --(Adobe/resemble-enhance: de-reverb + heavy denoise)-->  enhanced.wav
#     enhanced.wav  --(this script: tidy + de-ess + -14 LUFS)-->  final.wav
# On a clean, quiet take you can just run this script on the raw file.
#
# Usage:
#   ./clean_vo.sh input.m4a [output.wav] [--strong] [--gentle]
#                  [--denoise DB] [--no-declick] [--lufs -14]
#
# Examples:
#   ./clean_vo.sh "Voice Memo.m4a"                 # -> "Voice Memo.clean.wav"
#   ./clean_vo.sh raw.wav vo_final.wav --strong    # more aggressive denoise/de-ess
#   ./clean_vo.sh enhanced.wav final.wav --gentle  # after an AI pass: just finish
#
# Output: 48 kHz / 24-bit WAV (edit-ready). Prints before/after loudness.
# ---------------------------------------------------------------------------
set -euo pipefail

die() { printf 'clean_vo: %s\n' "$1" >&2; exit 1; }
command -v ffmpeg >/dev/null 2>&1 || die "ffmpeg not found on PATH."
command -v python3 >/dev/null 2>&1 || die "python3 not found on PATH."

# ---- defaults -------------------------------------------------------------
NR=12                 # denoise strength in dB (afftdn nr)
DEESS=0.35            # de-ess intensity 0..1
DECLICK=1            # run adeclick (taps / mouth clicks)
LUFS=-14             # integrated loudness target (YouTube ≈ -14)
TP=-1.0              # true-peak ceiling (dBTP)
IN=""; OUT=""

# ---- parse args -----------------------------------------------------------
while [ $# -gt 0 ]; do
  case "$1" in
    --strong)     NR=24; DEESS=0.5 ;;
    --gentle)     NR=6;  DEESS=0.25 ;;
    --denoise)    NR="${2:?--denoise needs a dB value}"; shift ;;
    --no-declick) DECLICK=0 ;;
    --lufs)       LUFS="${2:?--lufs needs a value}"; shift ;;
    -h|--help)    sed -n '2,40p' "$0"; exit 0 ;;
    -*)           die "unknown option: $1" ;;
    *)            if [ -z "$IN" ]; then IN="$1"; elif [ -z "$OUT" ]; then OUT="$1"; else die "too many args"; fi ;;
  esac
  shift
done

[ -n "$IN" ] || die "no input file. Try: ./clean_vo.sh input.m4a"
[ -f "$IN" ] || die "input not found: $IN"
if [ -z "$OUT" ]; then OUT="${IN%.*}.clean.wav"; fi

# ---- build the filter chain (same chain used in both loudnorm passes) -----
CHAIN="highpass=f=75"
[ "$DECLICK" -eq 1 ] && CHAIN="${CHAIN},adeclick"
CHAIN="${CHAIN},afftdn=nr=${NR}:nf=-25:tn=1"
CHAIN="${CHAIN},deesser=i=${DEESS}"
CHAIN="${CHAIN},acompressor=threshold=-20dB:ratio=2.5:attack=20:release=250"

LN="I=${LUFS}:TP=${TP}:LRA=11"
LOG="$(mktemp -t clean_vo.XXXXXX)"; trap 'rm -f "$LOG"' EXIT

printf '→ input : %s\n→ output: %s\n→ chain : %s\n\n' "$IN" "$OUT" "$CHAIN"

# ---- pass 1: measure loudness of the post-filter signal -------------------
echo "· pass 1/2 — measuring loudness…"
ffmpeg -hide_banner -nostats -i "$IN" \
  -af "${CHAIN},loudnorm=${LN}:print_format=json" -f null - 2> "$LOG" || die "pass 1 failed (see errors above)"

# extract the measured values from loudnorm's JSON block
read -r MI MTP MLRA MTHR OFF < <(python3 - "$LOG" <<'PY'
import sys, json
t = open(sys.argv[1]).read()
i, j = t.rfind('{'), t.rfind('}')
try:
    d = json.loads(t[i:j+1])
    print(d["input_i"], d["input_tp"], d["input_lra"], d["input_thresh"], d["target_offset"])
except Exception:
    print("NA NA NA NA NA")
PY
)

# ---- pass 2: apply, using the measured values for an accurate 2-pass ------
echo "· pass 2/2 — cleaning + normalizing…"
if [ "$MI" = "NA" ]; then
  echo "  (measurement unavailable — falling back to single-pass loudnorm)"
  ffmpeg -hide_banner -loglevel error -y -i "$IN" \
    -af "${CHAIN},loudnorm=${LN}" \
    -ar 48000 -c:a pcm_s24le "$OUT" || die "pass 2 failed"
else
  ffmpeg -hide_banner -loglevel error -y -i "$IN" \
    -af "${CHAIN},loudnorm=${LN}:measured_I=${MI}:measured_TP=${MTP}:measured_LRA=${MLRA}:measured_thresh=${MTHR}:offset=${OFF}:linear=true" \
    -ar 48000 -c:a pcm_s24le "$OUT" || die "pass 2 failed"
fi

printf '\n✓ done.\n'
printf '  loudness in : %s LUFS  (true-peak %s dBTP)\n' "${MI:-?}" "${MTP:-?}"
printf '  loudness out: ~%s LUFS (target, true-peak ≤ %s dBTP)\n' "$LUFS" "$TP"
printf '  wrote: %s\n' "$OUT"

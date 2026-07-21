#!/usr/bin/env python3
"""
tag_outliers.py — classify outlier titles against the formula library (Claude API).

Reads untagged rows (empty formula_tag) from data/outliers.csv, sends them to
Claude in batches with the formula table from formula_library.md, and writes
back a formula_tag (F1..Fn, or "none") plus a one-sentence "why it worked".
Then prints the top-3 winning formulas among big outliers (>=5x, last 90 days)
— the "what's working right now" read for the Packaging gate.

!! CHARGED STEP — this calls the Anthropic API (pay-per-use). The cost is tiny
   (~$0.02 / 50 rows on Haiku) but per house rules nothing charged runs without
   an explicit gate: use --dry-run first, then --yes to actually call.

Usage:
    python3 scripts/tag_outliers.py --dry-run    # show batch, prompt and cost — no API call
    python3 scripts/tag_outliers.py --yes        # tag untagged rows
    python3 scripts/tag_outliers.py --yes --model claude-sonnet-5

Setup: ANTHROPIC_API_KEY in .env (console.anthropic.com) + `pip install anthropic`.
"""

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_outliers import CSV_PATH, ROOT, load_dotenv, read_csv, write_csv  # noqa: E402

LIBRARY_PATH = ROOT / "formula_library.md"
BATCH_SIZE = 50
DEFAULT_MODEL = "claude-haiku-4-5"           # cheap classifier tier — this is a labeling job
USD_PER_MTOK = {                             # (input, output) — docs/costs.md uses Rs.84/$
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-sonnet-5": (3.00, 15.00),
    "claude-opus-4-8": (5.00, 25.00),
}

SCHEMA = {
    "type": "object",
    "properties": {
        "rows": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "formula_tag": {"type": "string"},
                    "why": {"type": "string"},
                },
                "required": ["id", "formula_tag", "why"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["rows"],
    "additionalProperties": False,
}


def load_formulas():
    """Parse the F-id table rows out of formula_library.md -> [(id, name, pattern)]."""
    if not LIBRARY_PATH.is_file():
        sys.exit("formula_library.md not found at the repo root — the tagger needs the "
                 "formula library (Task 2 of the packaging-research work) before it can label rows.")
    formulas = []
    for line in LIBRARY_PATH.read_text().splitlines():
        m = re.match(r"^\|\s*(F\d+)\s*\|([^|]+)\|([^|]+)\|", line)
        if m:
            formulas.append((m.group(1), m.group(2).strip(), m.group(3).strip()))
    if not formulas:
        sys.exit("No `| F<n> | ... |` table rows found in formula_library.md — is the table intact?")
    return formulas


def build_prompt(formulas, batch):
    lines = [
        "You classify YouTube titles from engineering/history/geography channels against a",
        "library of title formulas. For each row, pick the ONE formula id that best matches",
        'the title\'s hook mechanics (or "none" if nothing fits), and write ONE short sentence',
        "(max ~20 words) on WHY this title earned clicks — name the curiosity mechanism",
        "(open question, impossible-sounding scale, stakes, hidden system...), don't restate the title.",
        "",
        "FORMULA LIBRARY:",
    ]
    lines += [f"  {fid}  {name}  —  {pattern}" for fid, name, pattern in formulas]
    lines += ["", "ROWS (id | channel | multiple | title):"]
    lines += [f"  {r['id']} | {r['channel']} | {r['multiple']}x | {r['title']}" for r in batch]
    lines += ["", 'Return JSON: {"rows": [{"id", "formula_tag", "why"}]} — one entry per row, same ids.']
    return "\n".join(lines)


def estimate_cost(model, n_rows, prompt_chars):
    inp = prompt_chars // 4 + 200                # ~4 chars/token + schema overhead
    out = 60 * n_rows
    usd_in, usd_out = USD_PER_MTOK.get(model, USD_PER_MTOK["claude-opus-4-8"])
    usd = inp / 1e6 * usd_in + out / 1e6 * usd_out
    return inp, out, usd


def tag_batch(client, model, formulas, batch):
    import anthropic
    prompt = build_prompt(formulas, batch)
    try:
        resp = client.messages.create(
            model=model,
            max_tokens=8000,
            output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.AuthenticationError:
        sys.exit("Anthropic API key invalid/missing — set ANTHROPIC_API_KEY in .env (console.anthropic.com).")
    except anthropic.RateLimitError as e:
        retry = e.response.headers.get("retry-after", "60")
        sys.exit(f"Rate limited — retry after {retry}s. Nothing was written.")
    except anthropic.APIStatusError as e:
        sys.exit(f"Anthropic API error {e.status_code}: {e.message}")
    except anthropic.APIConnectionError:
        sys.exit("Network error reaching the Anthropic API — nothing was written.")

    text = next((b.text for b in resp.content if b.type == "text"), "")
    tags = {r["id"]: r for r in json.loads(text).get("rows", [])}
    return tags, resp.usage


def print_top_patterns(rows, formulas):
    names = dict((fid, name) for fid, name, _ in formulas)
    cutoff = (date.today() - timedelta(days=90)).isoformat()
    hot = [r for r in rows
           if r["formula_tag"] and r["formula_tag"] != "none"
           and float(r["multiple"] or 0) >= 5.0 and r["published"] >= cutoff]
    if not hot:
        print("\nNo tagged >=5x outliers in the last 90 days yet — patterns report will appear as data accrues.")
        return
    counts = {}
    for r in hot:
        counts.setdefault(r["formula_tag"], []).append(r)
    print("\nTOP PATTERNS right now (>=5x outliers, published in the last 90 days):")
    for fid, rs in sorted(counts.items(), key=lambda kv: len(kv[1]), reverse=True)[:3]:
        best = max(rs, key=lambda r: float(r["multiple"]))
        print(f"  {fid} {names.get(fid, '?'):28s} x{len(rs)}   e.g. {float(best['multiple']):.1f}x  \"{best['title']}\"")


def main():
    ap = argparse.ArgumentParser(description="Tag outlier titles with formula ids (charged API call)")
    ap.add_argument("--csv", default=str(CSV_PATH))
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--dry-run", action="store_true", help="show what would be sent + cost; no API call")
    ap.add_argument("--yes", action="store_true", help="confirm the charged API call")
    a = ap.parse_args()

    load_dotenv(ROOT / ".env")
    formulas = load_formulas()
    rows = read_csv(Path(a.csv))
    if not rows:
        sys.exit(f"{a.csv} is empty or missing — run scripts/fetch_outliers.py first.")
    untagged = [r for r in rows if not r["formula_tag"].strip()]

    if not untagged:
        print("All rows already tagged.")
        print_top_patterns(rows, formulas)
        return

    prompt_preview = build_prompt(formulas, untagged[:BATCH_SIZE])
    inp, out, usd = estimate_cost(a.model, len(untagged), len(prompt_preview) * -(-len(untagged) // BATCH_SIZE))
    print(f"{len(untagged)} untagged rows -> {-(-len(untagged) // BATCH_SIZE)} batch(es) on {a.model}")
    print(f"Estimated: ~{inp:,} in / ~{out:,} out tokens  ~=  ${usd:.3f} (~Rs.{usd * 84:.1f})")

    if a.dry_run:
        print("\n--- PROMPT (first batch) ---\n" + prompt_preview)
        print("\nDry run — no API call made. Re-run with --yes to tag.")
        return
    if not a.yes:
        sys.exit("Charged step: re-run with --yes to confirm (or --dry-run to inspect first).")

    try:
        import anthropic
    except ImportError:
        sys.exit("The anthropic SDK is not installed:  pip install anthropic")
    client = anthropic.Anthropic()

    total_in = total_out = 0
    for i in range(0, len(untagged), BATCH_SIZE):
        batch = untagged[i:i + BATCH_SIZE]
        tags, usage = tag_batch(client, a.model, formulas, batch)
        valid_ids = {fid for fid, _, _ in formulas} | {"none"}
        for r in batch:
            t = tags.get(r["id"])
            if t:
                r["formula_tag"] = t["formula_tag"] if t["formula_tag"] in valid_ids else "none"
                r["why"] = t["why"].strip()
        total_in += usage.input_tokens
        total_out += usage.output_tokens
        print(f"  batch {i // BATCH_SIZE + 1}: tagged {len(batch)} rows")

    write_csv(Path(a.csv), rows)
    usd_in, usd_out = USD_PER_MTOK.get(a.model, USD_PER_MTOK["claude-opus-4-8"])
    actual = total_in / 1e6 * usd_in + total_out / 1e6 * usd_out
    print(f"Done: {len(untagged)} rows tagged. Actual usage {total_in:,} in / {total_out:,} out "
          f"~= ${actual:.3f} (~Rs.{actual * 84:.1f}).")
    print_top_patterns(rows, formulas)


if __name__ == "__main__":
    main()

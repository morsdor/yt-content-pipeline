#!/usr/bin/env python3
"""
weekly_refresh.py — the Monday pass over the competitor set.

Same scan as fetch_outliers.py, restricted to videos published in the last
30 days: appends newly-detected outliers, refreshes view counts on existing
rows, and prints a "what's new" summary. Run weekly (locally, or via
.github/workflows/weekly_outliers.yml).

Usage:
    python3 scripts/weekly_refresh.py           # last 30 days
    python3 scripts/weekly_refresh.py --days 60
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_outliers import run  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Weekly outlier refresh (recent uploads only)")
    ap.add_argument("--days", type=int, default=30)
    a = ap.parse_args()

    new_rows, updated = run(days=a.days)

    print("\n" + "=" * 62)
    if new_rows:
        print(f"WHAT'S NEW this week ({len(new_rows)} outlier{'s' if len(new_rows) != 1 else ''}):")
        for r in sorted(new_rows, key=lambda r: float(r["multiple"]), reverse=True):
            print(f"  {float(r['multiple']):5.1f}x  {r['channel']:22s}  {r['title']}")
            print(f"         {r['url']}")
        print("\nNext: tag them ->  python3 scripts/tag_outliers.py --dry-run")
    else:
        print(f"No new outliers in the last {a.days} days ({updated} existing rows refreshed).")


if __name__ == "__main__":
    main()

"""
r002 — "How your phone knows what you meant"

A real Levenshtein edit-distance implementation over the real macOS system
dictionary (/usr/share/dict/words, 235,976 entries), whose intermediate state is
dumped to JSON so the Remotion reel can draw the DP table actually filling rather
than an illustration of it filling.

Nothing is chosen for the video: the candidate ranking below is whatever the
dictionary returns. `definately` was picked over `recieve`, `wierd` and `acheive`
precisely BECAUSE the data was clean — for `recieve`, plain edit distance ranks
`relieve` (1) above `receive` (2) and gets the answer wrong.

    python3 editdistance.py        # writes autocorrect_data.json
"""

import json
import pathlib
import time

TYPO = "definately"
DICT = pathlib.Path("/usr/share/dict/words")


def load_words():
    raw = DICT.read_text().split()
    return sorted({w.strip().lower() for w in raw if w.strip().isalpha()})


def table(a: str, b: str):
    """Full DP matrix. rows = a (the typo) + empty prefix, cols = b + empty prefix."""
    m = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        m[i][0] = i
    for j in range(len(b) + 1):
        m[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            m[i][j] = min(
                m[i - 1][j] + 1,                              # delete
                m[i][j - 1] + 1,                              # insert
                m[i - 1][j - 1] + (a[i - 1] != b[j - 1]),     # substitute / keep
            )
    return m


def backtrace(m, a: str, b: str):
    """Walk the optimal alignment back from the corner. This IS the correction."""
    i, j = len(a), len(b)
    path = []
    while i > 0 or j > 0:
        path.append({"i": i, "j": j, "v": m[i][j], "op": None})
        if i > 0 and j > 0 and m[i][j] == m[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            path[-1]["op"] = "keep" if a[i - 1] == b[j - 1] else "substitute"
            i, j = i - 1, j - 1
        elif i > 0 and m[i][j] == m[i - 1][j] + 1:
            path[-1]["op"] = "delete"
            i -= 1
        else:
            path[-1]["op"] = "insert"
            j -= 1
    path.append({"i": 0, "j": 0, "v": 0, "op": "start"})
    return list(reversed(path))


def fast_distance(a, b, limit):
    """Row-wise Levenshtein with early exit — 234k comparisons need the cutoff."""
    if abs(len(a) - len(b)) > limit:
        return limit + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        best = i
        for j, cb in enumerate(b, 1):
            v = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
            cur.append(v)
            best = min(best, v)
        if best > limit:
            return limit + 1
        prev = cur
    return prev[-1]


def main():
    words = load_words()
    wordset = set(words)

    t0 = time.perf_counter()
    scored = []
    for w in words:
        d = fast_distance(TYPO, w, 2)
        if d <= 2:
            scored.append((d, w))
    scored.sort()
    search_ms = (time.perf_counter() - t0) * 1000

    target = scored[0][1]
    m = table(TYPO, target)
    path = backtrace(m, TYPO, target)

    # The one cell where the words actually diverge.
    edits = [p for p in path if p["op"] in ("substitute", "insert", "delete")]

    data = {
        "typo": TYPO,
        "target": target,
        "in_dictionary": TYPO in wordset,
        "dict_size": len(words),
        "dict_raw_lines": len(DICT.read_text().splitlines()),
        "grid": m,
        "rows": len(TYPO) + 1,
        "cols": len(target) + 1,
        "distance": m[-1][-1],
        "path": path,
        "edits": edits,
        "candidates": [{"word": w, "d": d} for d, w in scored[:6]],
        "search_ms": round(search_ms, 1),
        "comparisons": len(words),
    }
    out = pathlib.Path(__file__).with_name("autocorrect_data.json")
    out.write_text(json.dumps(data))

    print(f"typo          : {TYPO!r}  in dictionary: {TYPO in wordset}")
    print(f"dictionary    : {len(words):,} unique alphabetic words")
    print(f"scan          : {len(words):,} comparisons in {search_ms:.0f} ms")
    print(f"grid          : {len(TYPO)+1} x {len(target)+1}  ->  distance {m[-1][-1]}")
    print(f"best match    : {target!r}")
    print(f"edit(s)       : {[(e['op'], e['i'], e['j']) for e in edits]}")
    print("ranked        :")
    for d, w in scored[:6]:
        print(f"                {d}  {w}")
    print(f"wrote {out.name} ({out.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()

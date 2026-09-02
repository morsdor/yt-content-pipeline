"""
r003 · "A QR code you've destroyed still scans"  (backlog I01)

Runs the real thing. No drawing, no faking:

  1. Encodes a genuine QR (segno, version 5, error level H) carrying the channel's
     own Instagram URL — the code on screen is scannable.
  2. Rebuilds the module -> codeword -> Reed-Solomon block mapping from the spec
     (placement zigzag, mask removal, block de-interleaving) and PROVES it by
     reconstructing the payload byte for byte.
  3. Destroys the code in three different ways and, at every step, asks an
     INDEPENDENT decoder (OpenCV) whether it still reads.

Everything the reel shows is measured here. Numbers on screen are this script's
output, which is the whole point: they cannot drift from the truth.
"""
import json
import numpy as np
import segno
import cv2

PAYLOAD = 'https://instagram.com/thedepthfirst'
V, N, MASK, ECL = 5, 37, 3, 'H'
# 5-H: 4 RS blocks — 2x(33 total, 11 data) + 2x(34, 12), 22 EC codewords each.
BLOCK_DATA = [11, 11, 12, 12]
EC_PER_BLOCK = 22
SEED = 7

MASKFN = {
    0: lambda i, j: (i + j) % 2 == 0,       1: lambda i, j: i % 2 == 0,
    2: lambda i, j: j % 3 == 0,             3: lambda i, j: (i + j) % 3 == 0,
    4: lambda i, j: (i // 2 + j // 3) % 2 == 0,
    5: lambda i, j: (i * j) % 2 + (i * j) % 3 == 0,
    6: lambda i, j: ((i * j) % 2 + (i * j) % 3) % 2 == 0,
    7: lambda i, j: ((i + j) % 2 + (i * j) % 3) % 2 == 0,
}


def functional_mask():
    """The modules that carry no data: finders, separators, timing, alignment, format."""
    f = np.zeros((N, N), bool)
    for r0, c0 in ((0, 0), (0, N - 8), (N - 8, 0)):
        f[r0:r0 + 8, c0:c0 + 8] = True          # finder + separator
    f[6, :] = True
    f[:, 6] = True                              # timing
    f[8, 0:9] = True
    f[0:9, 8] = True
    f[8, N - 8:] = True
    f[N - 7:, 8] = True                         # format info
    f[28:33, 28:33] = True                      # alignment (v5: centre 30,30)
    f[N - 8, 8] = True                          # dark module
    return f


def placement_order(f):
    """Spec zigzag: 2-column strips right to left, skipping the timing column."""
    order, col, up = [], N - 1, True
    while col > 0:
        if col == 6:
            col -= 1
        for i in range(N):
            row = N - 1 - i if up else i
            for c in (col, col - 1):
                if not f[row, c]:
                    order.append((row, c))
        up = not up
        col -= 2
    return order


def deinterleave(codewords):
    """5-H interleaves data across 4 blocks, then EC across the same 4."""
    blocks = [[] for _ in BLOCK_DATA]
    idx = 0
    for i in range(max(BLOCK_DATA)):
        for b, size in enumerate(BLOCK_DATA):
            if i < size:
                blocks[b].append(codewords[idx])
                idx += 1
    ecs = [[] for _ in BLOCK_DATA]
    for _ in range(EC_PER_BLOCK):
        for b in range(len(BLOCK_DATA)):
            ecs[b].append(codewords[idx])
            idx += 1
    return blocks, ecs, idx


def render(matrix, scale=12, quiet=4):
    """Modules -> a real image an independent decoder can look at."""
    img = np.kron((1 - matrix) * 255, np.ones((scale, scale), np.uint8))
    return cv2.copyMakeBorder(img, quiet * scale, quiet * scale, quiet * scale,
                              quiet * scale, cv2.BORDER_CONSTANT, value=255)


def decodes(matrix):
    """Ask OpenCV — not us — whether the damaged code still reads."""
    txt, *_ = cv2.QRCodeDetector().detectAndDecode(render(matrix))
    return txt == PAYLOAD


def main():
    q = segno.make(PAYLOAD, error=ECL, boost_error=False, version=V, mask=MASK)
    M = np.array(q.matrix, dtype=np.uint8)
    f = functional_mask()
    order = placement_order(f)
    assert len(order) == 1079, len(order)      # 134 codewords x 8 + 7 remainder bits

    # ── prove the mapping by reconstructing the payload ──────────────────────
    bits = [int(M[r, c]) ^ (1 if MASKFN[MASK](r, c) else 0) for r, c in order]
    cws = [int(''.join(map(str, bits[i * 8:i * 8 + 8])), 2) for i in range(134)]
    blocks, ecs, used = deinterleave(cws)
    stream = ''.join(f'{b:08b}' for blk in blocks for b in blk)
    length = int(stream[4:12], 2)
    text = ''.join(chr(int(stream[12 + i * 8:20 + i * 8], 2)) for i in range(length))
    assert text == PAYLOAD, text
    assert used == 134

    # module -> which RS block owns it (the "smeared across the square" reveal)
    owner = -np.ones((N, N), int)
    pos = 0
    for i in range(max(BLOCK_DATA)):
        for b, size in enumerate(BLOCK_DATA):
            if i < size:
                for k in range(8):
                    r, c = order[pos * 8 + k]
                    owner[r, c] = b
                pos += 1
    for _ in range(EC_PER_BLOCK):
        for b in range(len(BLOCK_DATA)):
            for k in range(8):
                r, c = order[pos * 8 + k]
                owner[r, c] = b
            pos += 1

    rng = np.random.default_rng(SEED)
    data_cells = np.argwhere(~f)
    perm = rng.permutation(len(data_cells))

    def sweep(kind, label):
        """Damage the code progressively; ask OpenCV at every step."""
        rows = []
        for pct in range(0, 61, 2):
            dmg = np.zeros((N, N), bool)
            n = int(round(len(data_cells) * pct / 100))
            if kind == 'speckle':
                # One fixed permutation, so damage ACCUMULATES as the sweep runs
                # and the reel can replay the identical sequence from an index.
                for r, c in data_cells[perm[:n]]:
                    dmg[r, c] = True
            else:  # one growing blob, like a stain or a torn-off sticker
                cy, cx = 22.0, 20.0
                rad = np.sqrt(n / np.pi) if n else 0.0
                yy, xx = np.mgrid[0:N, 0:N]
                dmg = ((yy - cy) ** 2 + (xx - cx) ** 2) <= rad ** 2
                dmg &= ~f
            hit = M.copy()
            hit[dmg] = 1                        # black it out
            ok = decodes(hit)
            rows.append({'pct': pct, 'modules': int(dmg.sum()), 'ok': bool(ok)})
        last = max((r['pct'] for r in rows if r['ok']), default=0)
        print(f'  {label:22} survives to {last}% of the data area')
        return rows, last

    print(f'QR {N}x{N}, version {V}-{ECL}, payload verified: {PAYLOAD!r}')
    print(f'  {int(f.sum())} functional modules, {len(data_cells)} data/EC modules')
    print(f'  4 RS blocks, {EC_PER_BLOCK} EC codewords each -> corrects 11 of 33')
    blob, blob_max = sweep('blob', 'contiguous stain')
    speck, speck_max = sweep('speckle', 'random speckle')

    # ── and the part everyone gets wrong: the corners are NOT protected ──────
    corner = M.copy()
    corner[2:5, 2:5] = 1 - corner[2:5, 2:5]     # 9 modules inside one finder
    corner_ok = decodes(corner)
    frac = 9 / (N * N)
    print(f'  finder corner: {9} modules ({frac:.1%} of the code) -> '
          f'{"still reads" if corner_ok else "DEAD"}')

    json.dump({
        'payload': PAYLOAD, 'n': N, 'version': V, 'ecl': ECL,
        'matrix': M.tolist(), 'functional': f.astype(int).tolist(),
        'owner': owner.tolist(),
        'blob': blob, 'speckle': speck,
        'blob_max': blob_max, 'speckle_max': speck_max,
        'corner_modules': 9, 'corner_ok': bool(corner_ok),
        'data_modules': int(len(data_cells)), 'functional_modules': int(f.sum()),
        'blocks': len(BLOCK_DATA), 'ec_per_block': EC_PER_BLOCK,
        'blob_centre': [22.0, 20.0],
        'speckle_order': [[int(r), int(c)] for r, c in data_cells[perm]],
    }, open('projects/r003_qr/qr_data.json', 'w'))
    print('wrote projects/r003_qr/qr_data.json')


if __name__ == '__main__':
    main()

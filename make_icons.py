"""Generate PWA PNG icons (stdlib only). Run: python make_icons.py"""
import struct
import zlib
from pathlib import Path

OUT = Path(__file__).parent / "icons"
OUT.mkdir(exist_ok=True)


def write_png(path, w, h, rgba):
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    rows = b""
    for y in range(h):
        rows += b"\x00" + rgba[y * w * 4 : (y + 1) * w * 4]
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    data = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(rows, 9))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(data)


def lerp(a, b, t):
    return int(a + (b - a) * t)


def fill(size, maskable=False):
    pad = int(size * (0.22 if maskable else 0.10))
    w = h = size
    px = [0, 0, 0, 255] * (w * h)
    bg = (10, 12, 16)

    def setp(x, y, c):
        if 0 <= x < w and 0 <= y < h:
            i = (y * w + x) * 4
            px[i : i + 4] = [c[0], c[1], c[2], 255]

    for y in range(h):
        for x in range(w):
            setp(x, y, bg)

    s = size - pad * 2
    ox, oy = pad, pad + int(s * 0.08)
    cx, cy = ox + s // 2, oy + s // 2

    g1, g2, g3, dirt = (45, 138, 45), (92, 184, 92), (36, 110, 36), (61, 40, 23)

    for y in range(h):
        for x in range(w):
            lx, ly = x - cx, y - cy
            # top diamond
            if abs(lx) / (s * 0.48) + abs(ly - s * 0.02) / (s * 0.22) < 1.0 and ly < s * 0.08:
                setp(x, y, g1)
            # right face
            elif lx > 0 and ly >= -s * 0.05 and ly < s * 0.42 and lx / (s * 0.5) + (ly + s * 0.05) / (s * 0.45) < 1.1:
                setp(x, y, g2)
            # left face
            elif lx <= 0 and ly >= -s * 0.05 and ly < s * 0.42 and -lx / (s * 0.5) + (ly + s * 0.05) / (s * 0.45) < 1.1:
                setp(x, y, g3)
            # dirt patch
            if (x - ox) ** 2 + (y - (oy + int(s * 0.55))) ** 2 < (s * 0.08) ** 2:
                setp(x, y, dirt)

    # glow under block
    for y in range(h):
        for x in range(w):
            dy = y - (oy + int(s * 0.88))
            dx = x - cx
            if dy > 0 and dy < s * 0.12 and abs(dx) < s * 0.42:
                t = 1 - dy / (s * 0.12)
                setp(x, y, (lerp(10, 255, t * 0.55), lerp(12, 158, t * 0.45), lerp(16, 54, t * 0.35)))

    return px


for fname, sz, mask in [
    ("icon-192.png", 192, False),
    ("icon-512.png", 512, False),
    ("icon-512-maskable.png", 512, True),
]:
    p = OUT / fname
    write_png(p, sz, sz, fill(sz, mask))
    print("wrote", p)

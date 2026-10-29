"""Roofs for top-down 3/4 buildings: clay tiles, slate and thatch, ridges, bargeboards and chimneys.

Projection rules (Stardew / Graveyard Keeper style): a slope facing the viewer is drawn as a rectangle,
courses run horizontally; slopes that run away from the viewer (either side of a front gable) are drawn
as parallelograms, their courses run vertically. Light comes from the top left.
"""
import random
from PIL import Image, ImageDraw

INK = (43, 29, 26)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def _bbox(poly):
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)


def _paste(im, tex, poly, x0, y0):
    mask = Image.new("L", tex.size, 0)
    ImageDraw.Draw(mask).polygon([(x - x0, y - y0) for x, y in poly], fill=255)
    im.paste(tex, (x0, y0), mask)


def _courses(w, h, base, rnd, ch, tw, kind, gradient=True):
    """A texture of overlapping courses (horizontal rows), each tile slightly different."""
    tex = Image.new("RGBA", (w, h), base + (255,))
    d = ImageDraw.Draw(tex)
    for row, y in enumerate(range(0, h, ch)):
        off = (row % 2) * (tw // 2)
        for x in range(-off, w, tw):
            f = rnd.choice([0.93, 0.97, 1.0, 1.03, 1.07]) if kind != "thatch" else 1.0
            c = shade(base, f)
            d.rectangle((x, y, x + tw - 1, y + ch - 1), fill=c)
            if kind == "tile":           # clay tile: shadow from the course above, lit left half, rounded lower corners
                d.rectangle((x, y, x + tw - 1, y + 1), fill=shade(c, 0.72))
                d.line([(x + 1, y + 2), (x + tw // 2, y + 2)], fill=shade(c, 1.16))
                d.line([(x + tw - 1, y + 2), (x + tw - 1, y + ch - 1)], fill=shade(c, 0.8))
                d.point((x, y + ch - 1), fill=shade(c, 0.7)); d.point((x + tw - 1, y + ch - 1), fill=shade(c, 0.7))
            elif kind == "slate":        # slate: thin, flat, crisp gaps
                d.rectangle((x, y, x + tw - 1, y), fill=shade(c, 0.7))
                d.line([(x + tw - 1, y + 1), (x + tw - 1, y + ch - 1)], fill=shade(c, 0.75))
                d.point((x + 1, y + 1), fill=shade(c, 1.2))
            elif kind == "thatch":       # straw: short strokes, each layer darker at its foot
                for sx in range(x, x + tw):
                    top = y + rnd.randrange(0, 2)
                    col = shade(base, rnd.choice([0.86, 0.94, 1.0, 1.08]))
                    d.line([(sx, top), (sx, y + ch - 1)], fill=col)
                    d.point((sx, y + ch - 1), fill=shade(col, 0.72))
                    if rnd.random() < 0.3:
                        d.point((sx, y + ch - 2), fill=shade(col, 0.8))
    if gradient:                         # a touch lighter on the left (lit side)
        px = tex.load()
        for x in range(w):
            f = 1.06 - 0.12 * x / max(1, w - 1)
            for yy in range(h):
                r, g, b, a = px[x, yy]
                px[x, yy] = (min(255, int(r * f)), min(255, int(g * f)), min(255, int(b * f)), a)
    return tex


SPEC = {"tile": (6, 8), "slate": (4, 7), "thatch": (5, 4)}


def slope(im, poly, base, kind="tile", vertical=False, light=1.0, seed=1):
    """Fill a roof plane. vertical=True for slopes that run away from the viewer (courses run up the screen)."""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = _bbox(poly)
    w, h = x1 - x0 + 1, y1 - y0 + 1
    ch, tw = SPEC[kind]
    base = shade(base, light)
    if vertical:
        tex = _courses(h, w, base, rnd, ch, tw, kind, gradient=False).transpose(Image.ROTATE_270)
    else:
        tex = _courses(w, h, base, rnd, ch, tw, kind)
    _paste(im, tex, poly, x0, y0)
    ImageDraw.Draw(im).polygon(poly, outline=INK)


def ridge(im, x0, x1, y, base, kind="tile"):
    """Half-round ridge tiles (or a slate/lead ridge) along the top of a slope."""
    d = ImageDraw.Draw(im)
    if kind == "tile":
        for x in range(x0, x1, 9):
            d.chord((x, y - 4, x + 10, y + 6), 180, 360, fill=shade(base, 0.92), outline=INK)
            d.line([(x + 2, y - 2), (x + 5, y - 3)], fill=shade(base, 1.25))
        d.line([(x0, y + 1), (x1, y + 1)], fill=shade(base, 0.6), width=2)
    else:
        d.rectangle((x0, y - 2, x1, y + 2), fill=shade(base, 0.85), outline=INK)
        d.line([(x0 + 1, y - 1), (x1 - 1, y - 1)], fill=shade(base, 1.2))


def eave(im, x0, x1, y, base):
    """Fascia board and drip edge under the lowest course."""
    d = ImageDraw.Draw(im)
    d.rectangle((x0, y, x1, y + 3), fill=shade(base, 0.55), outline=INK)
    d.line([(x0 + 1, y + 1), (x1 - 1, y + 1)], fill=shade(base, 0.75))


def verge(im, x, y0, y1, base, side):
    """The visible thickness of a gable end at the left or right edge of a front slope."""
    d = ImageDraw.Draw(im)
    if side == "l":
        d.rectangle((x - 3, y0, x, y1), fill=shade(base, 1.12), outline=INK)
    else:
        d.rectangle((x, y0, x + 3, y1), fill=shade(base, 0.62), outline=INK)


def bargeboards(im, left, apex, right, oak=(84, 56, 38)):
    """Thick carved bargeboards along a front gable, with a pendant at the apex."""
    d = ImageDraw.Draw(im)
    for a, b in ((left, apex), (apex, right)):
        d.line([a, b], fill=INK, width=7)
        d.line([a, b], fill=oak, width=5)
        d.line([(a[0], a[1] - 2), (b[0], b[1] - 2)], fill=shade(oak, 1.45), width=1)
    # small carved notches along the boards
    for t in (0.2, 0.4, 0.6, 0.8):
        for a, b in ((left, apex), (apex, right)):
            x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            d.point((round(x), round(y) + 1), fill=shade(oak, 0.6))
    ax, ay = apex
    d.rectangle((ax - 2, ay, ax + 2, ay + 8), fill=oak, outline=INK)          # pendant
    d.polygon([(ax - 2, ay + 8), (ax + 2, ay + 8), (ax, ay + 12)], fill=oak, outline=INK)
    d.polygon([(ax - 2, ay - 2), (ax + 2, ay - 2), (ax, ay - 8)], fill=oak, outline=INK)   # finial


def chimney(im, x0, x1, top, base_y, stone=(152, 142, 128), seed=3, smoke=True):
    """A stone stack rising out of a roof: front face, cap with a lit top and dark flue, lead flashing, shadow."""
    rnd = random.Random(seed)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).polygon([(x1 + 1, top + 8), (x1 + 13, top + 16), (x1 + 13, base_y + 8), (x1 + 1, base_y)], fill=(34, 22, 46, 95))
    im.alpha_composite(layer)
    d = ImageDraw.Draw(im)
    d.rectangle((x0, top, x1, base_y), fill=stone, outline=INK)
    for y in range(top + 6, base_y, 5):
        off = (y // 5 % 2) * 4
        d.line([(x0 + 1, y), (x1 - 1, y)], fill=shade(stone, 0.78))
        for x in range(x0 + 2 + off, x1 - 1, 8):
            d.line([(x, y - 4), (x, y - 1)], fill=shade(stone, 0.8))
            d.line([(x + 1, y - 4), (x + 5, y - 4)], fill=shade(stone, rnd.choice([1.08, 1.14])))
    d.line([(x0 + 1, top + 5), (x0 + 1, base_y - 1)], fill=shade(stone, 1.15))
    d.line([(x1 - 1, top + 5), (x1 - 1, base_y - 1)], fill=shade(stone, 0.72))
    d.rectangle((x0 - 2, top - 4, x1 + 2, top + 2), fill=shade(stone, 0.95), outline=INK)      # cap
    d.rectangle((x0 - 1, top - 3, x1 + 1, top - 2), fill=shade(stone, 1.2))
    d.rectangle((x0 + 3, top - 3, x1 - 3, top - 2), fill=(30, 24, 26))                         # flue
    d.rectangle((x0 - 2, base_y - 2, x1 + 2, base_y + 1), fill=(120, 124, 132), outline=INK)    # lead flashing
    if smoke:
        for i, (dx, dy, r) in enumerate(((2, -10, 4), (6, -18, 5), (12, -26, 6))):
            cx = (x0 + x1) // 2 + dx
            d.ellipse((cx - r, top + dy - r, cx + r, top + dy + r), fill=(232, 232, 236))
            d.ellipse((cx - r + 2, top + dy - r + 1, cx + r - 1, top + dy + r - 2), fill=(244, 244, 246))

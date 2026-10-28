"""Helpers for 256x256 dialogue portraits: scaled coordinates, eyes and tapered eyebrows."""
from PIL import ImageDraw

K = 2  # portraits are laid out on a 128 grid and drawn at 256


def k(*v):
    return tuple(int(round(x * K)) for x in v)


def kp(points):
    return [k(x, y) for x, y in points]


def mirror(p, w=256):
    return (w - 1 - p[0], p[1])


def dots(im, points, col, size=2):
    """Freckles / flour: small square dots at 128-grid positions."""
    d = ImageDraw.Draw(im)
    for x, y in points:
        X, Y = k(x, y)
        d.rectangle((X, Y, X + size - 1, Y + size - 1), fill=col + (255,))


def brow(im, inner, outer, arch, t_in, t_out, col, light=None):
    """Tapered, curved eyebrow: thick at the inner end, thin at the outer end."""
    (x0, y0), (x2, y2) = inner, outer
    cx, cy = (x0 + x2) / 2, (y0 + y2) / 2 - arch
    top, bot = [], []
    n = 24
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x2
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y2
        th = t_in * (1 - t) + t_out * t
        top.append((x, y - th * 0.6))
        bot.append((x, y + th * 0.4))
    d = ImageDraw.Draw(im)
    d.polygon(top + bot[::-1], fill=col + (255,))
    if light:  # a few lighter hairs along the top edge
        for i in range(3, n - 4, 5):
            x, y = top[i]
            d.point((round(x), round(y) + 1), fill=light + (255,))


def eye(im, part, cx, cy, w, h, iris, iris_dark, ink, skin, lid=3, crease=False, lashes=True, outer_right=True):
    """A pixel-art eye: sclera, two-tone iris, pupil, highlights, upper lid, lashes, lower lid."""
    sclera = ((150, 120, 112), (228, 222, 214), (248, 245, 240), (248, 245, 240))
    part(im, lambda d: d.ellipse((cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2), fill=255), sclera, shade=(0, 0), light_top=0)
    d = ImageDraw.Draw(im)
    iw = int(w * 0.5)
    d.ellipse((cx - iw // 2, cy - h // 2, cx + iw // 2, cy + h // 2), fill=iris + (255,))
    d.chord((cx - iw // 2, cy - h // 2, cx + iw // 2, cy + h // 2), 180, 360, fill=iris_dark + (255,))
    d.ellipse((cx - iw // 5, cy - h // 4, cx + iw // 5, cy + h // 4), fill=ink + (255,))
    d.rectangle((cx - iw // 3, cy - h // 3, cx - iw // 3 + 3, cy - h // 3 + 3), fill=(255, 255, 255, 255))
    d.rectangle((cx + iw // 5, cy + h // 6, cx + iw // 5 + 1, cy + h // 6 + 1), fill=(255, 255, 255, 255))
    box = (cx - w // 2 - 2, cy - h // 2 - 1, cx + w // 2 + 2, cy + h // 2 + 8)
    d.arc(box, 192, 348, fill=ink + (255,), width=lid)
    if crease:  # tired, heavy-lidded look
        d.arc((box[0] + 2, box[1] - 5, box[2] - 2, box[3] - 6), 200, 340, fill=skin[1] + (255,), width=2)
    if lashes:
        ox = cx + w // 2 + 1 if outer_right else cx - w // 2 - 1
        sx = 1 if outer_right else -1
        d.line([(ox - sx, cy - h // 3), (ox + 3 * sx, cy - h // 2 - 2)], fill=ink + (255,), width=2)  # one small outer lash
    d.arc((cx - w // 2 + 2, cy - h // 2, cx + w // 2 - 2, cy + h // 2 + 3), 30, 150, fill=skin[1] + (255,), width=2)

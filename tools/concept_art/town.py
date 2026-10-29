"""Concept sprites for the whole town of Hollowmere: one front-facing 32x64 sprite per person,
each with their own body, outfit, hair, hat and something they're doing.

Run: python3 tools/concept_art/town.py
Writes docs/concept-art/town/ (lineup sheet, single sprites, a strip, and CAST.md).
Concept quality: a reference for an artist and placeholder art for prototypes.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mira_hd import part, put  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "concept-art" / "town"
INK = (43, 29, 26)
WHITE = (250, 248, 242)


def ramp(c, out=0.42):
    """(outline, shadow, base, light) from a base colour."""
    return (tuple(int(v * out) for v in c), tuple(int(v * 0.8) for v in c), c,
            tuple(min(255, int(v + (255 - v) * 0.25)) for v in c))


SKIN = {
    "light": (236, 190, 158), "fair": (242, 198, 176), "olive": (214, 170, 124),
    "tan": (196, 144, 102), "brown": (154, 102, 68), "dark": (106, 68, 46),
}
HAIRC = {
    "lightbrown": (160, 116, 76), "darkbrown": (88, 56, 38), "black": (42, 36, 40), "ginger": (196, 98, 50),
    "blonde": (224, 188, 112), "grey": (164, 160, 156), "white": (232, 230, 226), "auburn": (126, 56, 38),
    "saltpepper": (112, 106, 102),
}
EYES = {"green": (70, 140, 72), "brown": (110, 70, 44), "blue": (70, 110, 170), "grey": (120, 128, 136), "dark": (52, 36, 30)}

HEIGHTS = {  # head top, head height, head width, arm scale
    "tall": (2, 18, 16, 1.0), "adult": (5, 18, 16, 1.0), "short": (8, 17, 16, 0.95), "teen": (6, 17, 15, 1.0),
    "kid12": (13, 16, 15, 0.8), "kid10": (15, 16, 15, 0.75), "kid7": (16, 16, 15, 0.72),
}
BUILDS = {"slim": 12, "normal": 14, "stocky": 16, "big": 18}


class Body:
    def __init__(self, c):
        self.c = c
        T, HH, HW, self.f = HEIGHTS[c.get("height", "adult")]
        self.T, self.HH, self.HW = T, HH, HW
        self.x0, self.x1 = 16 - HW // 2, 15 + HW // 2
        self.y0, self.y1 = T, T + HH
        self.S = self.y1 - 1
        self.W = self.S + round(11 * (0.85 if self.f < 1 else 1))
        bw = BUILDS[c.get("build", "normal")]
        if self.f < 1:
            bw = min(bw, 12)
        self.L, self.R = 16 - bw // 2, 15 + bw // 2
        self.eye_y = self.y0 + round(HH * (0.5 if self.f < 1 else 0.47))
        self.mouth_y = self.y1 - (3 if self.f < 1 else 4)
        self.skin = ramp(SKIN[c["skin"]], 0.5)
        self.hair = ramp(HAIRC[c.get("hair_color", "darkbrown")])
        self.hands = {}


# ---------------------------------------------------------------- body parts
def legs(im, b):
    c = b.c
    shoe = ramp(c.get("shoes", (70, 46, 32)))
    part(im, lambda d: d.rounded_rectangle((b.L, 56, 15, 62), 2, fill=255), shoe, light_top=0)
    part(im, lambda d: d.rounded_rectangle((16, 56, b.R, 62), 2, fill=255), shoe, light_top=0)
    low, col = c["lower"]
    r = ramp(col)
    if low == "dress":
        part(im, lambda d: d.polygon([(b.L, b.W), (b.R, b.W), (b.R + 3, 57), (b.L - 3, 57)], fill=255), r)
        put(im, [(b.L + 3, y) for y in range(b.W + 7, 55)] + [(b.R - 3, y) for y in range(b.W + 9, 55)], r[1])
    elif low == "robe":
        part(im, lambda d: d.polygon([(b.L, b.W), (b.R, b.W), (b.R + 4, 60), (b.L - 4, 60)], fill=255), r)
        put(im, [(16, y) for y in range(b.W + 6, 59)], r[1])
    elif low in ("trousers", "breeches", "skirt"):
        knee = b.W + (57 - b.W) // 2 + 1
        if low == "skirt":
            part(im, lambda d: d.polygon([(b.L, b.W), (b.R, b.W), (b.R + 2, knee), (b.L - 2, knee)], fill=255), r)
        if low != "trousers":
            sock = ramp(c.get("socks", (206, 198, 184)))
            part(im, lambda d: d.rectangle((b.L + 1, knee - 1, 14, 57), fill=255), sock, shade=(0, 0), light_top=0)
            part(im, lambda d: d.rectangle((17, knee - 1, b.R - 1, 57), fill=255), sock, shade=(0, 0), light_top=0)
        if low != "skirt":
            bottom = 57 if low == "trousers" else knee
            part(im, lambda d: (d.rectangle((b.L, b.W, 15, bottom), fill=255), d.rectangle((16, b.W, b.R, bottom), fill=255),
                                d.rectangle((b.L, b.W, b.R, b.W + 5), fill=255)), r)
            put(im, [(15, y) for y in range(b.W + 6, bottom)], r[0])


def torso(im, b):
    c = b.c
    up, col = c["upper"]
    r = ramp(col)
    big = c.get("build") == "big"
    hem = b.W + (4 if up in ("tunic", "vest", "coat", "armor") and c["lower"][0] in ("trousers", "breeches") else 2)
    part(im, lambda d: d.polygon([(b.L, b.S), (b.R, b.S), (b.R + (2 if big else 1), hem), (b.L - (2 if big else 1), hem)], fill=255), r)
    if big:
        part(im, lambda d: d.ellipse((b.L - 2, b.S + 4, b.R + 2, hem + 2), fill=255), r)
    if up == "vest":
        v = ramp(c.get("vest", (110, 70, 44)))
        part(im, lambda d: d.polygon([(b.L, b.S + 1), (14, b.S + 1), (14, hem), (b.L - 1, hem)], fill=255), v)
        part(im, lambda d: d.polygon([(17, b.S + 1), (b.R, b.S + 1), (b.R + 1, hem), (17, hem)], fill=255), v)
    if up == "coat":
        sh = ramp(c.get("shirt", WHITE))
        part(im, lambda d: d.rectangle((14, b.S, 17, b.W + 1), fill=255), sh, shade=(0, 0), light_top=0)
        part(im, lambda d: d.polygon([(b.L - 1, b.W), (14, b.W), (13, 51), (b.L - 3, 51)], fill=255), r)
        part(im, lambda d: d.polygon([(17, b.W), (b.R + 1, b.W), (b.R + 3, 51), (18, 51)], fill=255), r)
        put(im, [(13, b.S + 3), (13, b.S + 6), (13, b.S + 9)], (214, 176, 80))
    if up == "armor":
        t = ramp(c.get("tabard", (60, 80, 140)))
        put(im, [(x, y) for x in range(b.L + 1, b.R) for y in range(b.S + 1, hem) if (x + y) % 2 == 0], r[1])
        part(im, lambda d: d.rectangle((12, b.S + 2, 19, b.W + 7), fill=255), t)
        put(im, [(15, b.S + 5), (16, b.S + 5), (15, b.S + 6), (16, b.S + 6), (14, b.S + 6), (17, b.S + 6), (15, b.S + 7), (16, b.S + 7)], (232, 226, 210))
    neck = c.get("neck", "v")
    if neck == "v":
        part(im, lambda d: d.polygon([(13, b.S), (18, b.S), (15, b.S + 4)], fill=255), ramp(c.get("shirt", (236, 228, 210))), shade=(0, 0), light_top=0)
    elif neck == "collar":
        part(im, lambda d: d.rectangle((12, b.S - 1, 19, b.S + 1), fill=255), ramp(WHITE), shade=(0, 0), light_top=0)
    elif neck == "priest":
        part(im, lambda d: d.rectangle((14, b.S - 1, 17, b.S + 1), fill=255), ramp(WHITE), shade=(0, 0), light_top=0)


def overlays_body(im, b):
    c = b.c
    for ov in c.get("over", []):
        kind, *arg = ov if isinstance(ov, tuple) else (ov,)
        col = arg[0] if arg else None
        if kind == "apron":
            a = ramp(col or (238, 230, 212))
            bottom = min(55, b.W + 16)
            part(im, lambda d: (d.rectangle((11, b.S + 3, 20, b.W + 1), fill=255),
                                d.polygon([(10, b.W), (21, b.W), (22, bottom), (9, bottom)], fill=255)), a, shade=(2, 0))
        elif kind == "shawl":
            part(im, lambda d: d.polygon([(b.L - 1, b.S), (b.R + 1, b.S), (b.R + 1, b.S + 4), (16, b.S + 10), (b.L - 1, b.S + 4)], fill=255), ramp(col))
        elif kind == "belt":
            part(im, lambda d: d.rectangle((b.L, b.W, b.R, b.W + 1), fill=255), ramp(col or (70, 46, 30)), shade=(0, 0), light_top=0)
        elif kind == "rope":
            put(im, [(x, b.W) for x in range(b.L, b.R + 1)] + [(14, b.W + 1), (14, b.W + 2), (14, b.W + 3), (14, b.W + 4)], (200, 176, 120))
        elif kind == "sash":
            dr = ImageDraw.Draw(im)
            dr.line([(b.L + 1, b.S + 1), (b.R - 1, b.W)], fill=(176, 40, 44, 255), width=2)
        elif kind == "medals":
            put(im, [(18, b.S + 4), (20, b.S + 4)], (220, 180, 70)); put(im, [(18, b.S + 3), (20, b.S + 3)], (176, 40, 44))
            put(im, [(19, b.S + 6)], (220, 180, 70)); put(im, [(19, b.S + 5)], (60, 90, 170))
        elif kind == "tape":
            put(im, [(13, y) for y in range(b.S, b.S + 10)] + [(18, y) for y in range(b.S, b.S + 8)], (226, 196, 80))
            put(im, [(13, b.S + 3), (13, b.S + 7), (18, b.S + 4)], INK)
        elif kind == "suspenders":
            part(im, lambda d: d.rectangle((12, b.S, 13, b.W + 2), fill=255), ramp((66, 42, 28)), shade=(0, 0), light_top=0)
            part(im, lambda d: d.rectangle((18, b.S, 19, b.W + 2), fill=255), ramp((66, 42, 28)), shade=(0, 0), light_top=0)
        elif kind == "leather_apron":
            part(im, lambda d: d.polygon([(11, b.S + 2), (20, b.S + 2), (22, 54), (9, 54)], fill=255), ramp((120, 76, 44)), shade=(2, 0))
        elif kind == "pouches":
            part(im, lambda d: d.rectangle((b.L - 1, b.W, b.R + 1, b.W + 1), fill=255), ramp((90, 60, 36)), shade=(0, 0), light_top=0)
            part(im, lambda d: d.rectangle((b.R - 3, b.W + 1, b.R, b.W + 4), fill=255), ramp((120, 140, 80)), shade=(0, 0), light_top=0)
        elif kind == "sword":
            part(im, lambda d: d.rectangle((b.L - 3, b.W - 1, b.L - 2, 50), fill=255), ramp((70, 46, 32)), shade=(0, 0), light_top=0)
            put(im, [(b.L - 4, b.W - 1), (b.L - 1, b.W - 1)], (210, 176, 80))
        elif kind == "sling":
            part(im, lambda d: d.polygon([(b.L - 1, b.S + 1), (18, b.S + 11), (b.L - 1, b.S + 14)], fill=255), ramp(WHITE), shade=(0, 0), light_top=0)


def back_items(im, b):
    c = b.c
    for ov in c.get("over", []):
        kind = ov[0] if isinstance(ov, tuple) else ov
        if kind == "cloak":
            part(im, lambda d: d.polygon([(b.L - 1, b.S), (b.R + 1, b.S), (b.R + 4, 54), (b.L - 4, 54)], fill=255), ramp(ov[1]))
        if kind == "quiver":
            part(im, lambda d: d.polygon([(b.R - 2, b.S - 6), (b.R + 2, b.S - 7), (b.R + 3, b.W - 2), (b.R, b.W - 1)], fill=255), ramp((110, 70, 40)))
            put(im, [(b.R - 1, b.S - 8), (b.R + 1, b.S - 9), (b.R + 3, b.S - 8)], (200, 60, 50))
    if c.get("hair") in ("long", "longwild"):
        part(im, lambda d: d.rounded_rectangle((b.x0 - 2, b.y0 + 3, b.x1 + 2, b.S + 9), 3, fill=255), b.hair)


ARM_POSES = {}


def arm(im, b, side, pose):
    """Draw one arm; record the hand position."""
    c = b.c
    sleeve = ramp(c.get("sleeve", c["upper"][1]))
    rolled = c.get("rolled", False)
    f = b.f
    s = -1 if side == "l" else 1
    x0, x1 = (b.L - 4, b.L) if side == "l" else (b.R, b.R + 4)
    S = b.S
    a1, a2 = round(9 * f), round(9 * f)
    fore = b.skin if rolled else sleeve
    if pose == "down":
        part(im, lambda d: d.rounded_rectangle((x0, S + 2, x1, S + 2 + a1), 2, fill=255), sleeve)
        part(im, lambda d: d.rectangle((x0 + 1, S + 1 + a1, x1 - 1, S + 1 + a1 + a2), fill=255), fore, light_top=0)
        hy = S + a1 + a2 + 1
        part(im, lambda d: d.ellipse((x0, hy - 2, x1, hy + 3), fill=255), b.skin, light_top=0)
        b.hands[side] = ((x0 + x1) // 2, hy)
    elif pose == "front":
        part(im, lambda d: d.rounded_rectangle((x0, S + 2, x1, S + 2 + a1), 2, fill=255), sleeve)
        ex, ey = (x0 + x1) // 2, S + 1 + a1
        hx = 14 if side == "l" else 17
        part(im, lambda d: d.polygon([(ex - 2, ey - 1), (ex + 2, ey - 1), (hx + 2 * s, ey + 3), (hx - 2 * s, ey + 4)], fill=255), fore, light_top=0)
        part(im, lambda d: d.ellipse((hx - 2, ey + 1, hx + 2, ey + 5), fill=255), b.skin, light_top=0)
        b.hands[side] = (hx, ey + 3)
    elif pose == "raise":
        part(im, lambda d: d.rounded_rectangle((x0, S - 4, x1, S + 4), 2, fill=255), sleeve)
        part(im, lambda d: d.rectangle((x0 + 1, S - 9, x1 - 1, S - 3), fill=255), fore, light_top=0)
        part(im, lambda d: d.ellipse((x0, S - 13, x1, S - 8), fill=255), b.skin, light_top=0)
        b.hands[side] = ((x0 + x1) // 2, S - 11)
    elif pose == "hip":
        ox = x0 - 2 if side == "l" else x0 + 2
        part(im, lambda d: d.polygon([(x0, S + 1), (x1, S + 1), (ox + 4, S + 7), (ox, S + 8)], fill=255), sleeve)
        hx = b.L if side == "l" else b.R
        part(im, lambda d: d.polygon([(ox, S + 7), (ox + 4, S + 7), (hx + 2, S + 12), (hx - 2, S + 12)], fill=255), fore, light_top=0)
        part(im, lambda d: d.ellipse((hx - 2, S + 10, hx + 2, S + 14), fill=255), b.skin, light_top=0)
        b.hands[side] = (hx, S + 12)
    elif pose == "pray":
        part(im, lambda d: d.rounded_rectangle((x0, S + 2, x1, S + 2 + a1 - 2), 2, fill=255), sleeve)
        ex, ey = (x0 + x1) // 2, S + a1 - 1
        part(im, lambda d: d.polygon([(ex - 2, ey), (ex + 2, ey), (16 + 2 * s, S + 7), (16, S + 9)], fill=255), sleeve)
        if side == "r":
            part(im, lambda d: d.ellipse((14, S + 1, 17, S + 8), fill=255), b.skin, light_top=0)
        b.hands[side] = (16, S + 5)
    elif pose == "sling":
        part(im, lambda d: d.rounded_rectangle((x0, S + 2, x1, S + 2 + a1 - 3), 2, fill=255), sleeve)
        part(im, lambda d: d.rectangle((x0 + 1, S + a1 - 1, 17, S + a1 + 3), fill=255), sleeve, light_top=0)
        part(im, lambda d: d.ellipse((16, S + a1 - 1, 20, S + a1 + 3), fill=255), b.skin, light_top=0)
        b.hands[side] = (18, S + a1 + 1)
    elif pose == "shoulder":  # hand up on the shoulder, holding something there
        part(im, lambda d: d.rounded_rectangle((x0, S + 1, x1, S + 7), 2, fill=255), sleeve)
        part(im, lambda d: d.rectangle((x0, S - 3, x1 - 1, S + 2), fill=255), fore, light_top=0)
        part(im, lambda d: d.ellipse((x0 - 1, S - 6, x1 - 1, S - 1), fill=255), b.skin, light_top=0)
        b.hands[side] = (x0 + 1, S - 3)


# ---------------------------------------------------------------- head
def head_back(im, b):
    st = b.c.get("hair")
    hood = b.c.get("hat", (None,))[0] == "hood"
    if hood:
        part(im, lambda d: d.ellipse((b.x0 - 3, b.y0 - 3, b.x1 + 3, b.y1 + 3), fill=255), ramp(b.c["hat"][1]))
    if st in (None, "bald", "tonsure") or hood:
        return
    if st == "bob":
        part(im, lambda d: d.rounded_rectangle((b.x0 - 2, b.y0 - 2, b.x1 + 2, b.y1 - 1), 4, fill=255), b.hair)
    elif st == "pigtails":
        part(im, lambda d: d.ellipse((b.x0 - 5, b.y0 + 6, b.x0, b.y1 + 2), fill=255), b.hair)
        part(im, lambda d: d.ellipse((b.x1, b.y0 + 6, b.x1 + 5, b.y1 + 2), fill=255), b.hair)
        part(im, lambda d: d.ellipse((b.x0 - 2, b.y0 - 2, b.x1 + 2, b.y0 + b.HH * 0.7), fill=255), b.hair)
    elif st in ("wild", "longwild"):
        part(im, lambda d: (d.ellipse((b.x0 - 5, b.y0 + 1, b.x0 + 4, b.y1 + 1), fill=255), d.ellipse((b.x1 - 4, b.y0 + 1, b.x1 + 5, b.y1 + 1), fill=255)), b.hair)
    elif st == "topknot":
        part(im, lambda d: d.ellipse((13, b.y0 - 5, 18, b.y0 + 1), fill=255), b.hair)
        part(im, lambda d: d.ellipse((b.x0 - 1, b.y0 - 2, b.x1 + 1, b.y0 + b.HH * 0.7), fill=255), b.hair)
    else:
        part(im, lambda d: d.ellipse((b.x0 - 2, b.y0 - 2, b.x1 + 2, b.y0 + b.HH * 0.75), fill=255), b.hair)


def face(im, b):
    c = b.c
    part(im, lambda d: d.rectangle((13, b.y1 - 5, 18, b.S + 1), fill=255), b.skin, shade=(0, 0), light_top=0)
    if c.get("ears", True) and c.get("hair") not in ("bob", "long", "longwild") and c.get("hat", (None,))[0] not in ("hood", "coif", "bonnet"):
        part(im, lambda d: d.ellipse((b.x0 - 2, b.eye_y - 1, b.x0 + 1, b.eye_y + 4), fill=255), b.skin, shade=(0, 0), light_top=0)
        part(im, lambda d: d.ellipse((b.x1 - 1, b.eye_y - 1, b.x1 + 2, b.eye_y + 4), fill=255), b.skin, shade=(0, 0), light_top=0)
    part(im, lambda d: d.ellipse((b.x0, b.y0, b.x1, b.y1), fill=255), b.skin, shade=(3, 0), light_top=0)
    y = b.eye_y
    iris = EYES[c.get("eyes", "dark")]
    elder = c.get("age", 30) >= 60
    for ex in (b.x0 + 3, b.x1 - 4):
        if c.get("eyes_closed"):
            put(im, [(ex, y + 1), (ex + 1, y + 1)], INK)
            continue
        if elder:
            put(im, [(ex, y), (ex + 1, y)], INK); put(im, [(ex, y + 1)], iris); put(im, [(ex + 1, y + 1)], INK)
            put(im, [(ex - 1 if ex < 16 else ex + 2, y + 1)], b.skin[1])
        else:
            put(im, [(ex, y), (ex + 1, y)], INK)
            put(im, [(ex, y + 1), (ex, y + 2), (ex + 1, y + 2)], iris)
            put(im, [(ex + 1, y + 1)], WHITE)
        if c.get("lashes"):
            put(im, [(ex - 1 if ex < 16 else ex + 2, y - 1)], INK)
    if c.get("glasses"):
        g = (90, 80, 70)
        for ex in (b.x0 + 2, b.x1 - 5):
            put(im, [(ex + i, y - 1) for i in range(4)] + [(ex + i, y + 3) for i in range(4)] + [(ex, y + j) for j in range(4)] + [(ex + 3, y + j) for j in range(4)], g)
        put(im, [(14, y), (15, y), (16, y), (17, y)], g)
    brow = b.hair[1] if c.get("hair") not in (None, "bald") else b.skin[0]
    if c.get("brows", "normal") == "stern":
        put(im, [(b.x0 + 2, y - 2), (b.x0 + 3, y - 2), (b.x0 + 4, y - 1), (b.x1 - 5, y - 1), (b.x1 - 4, y - 2), (b.x1 - 3, y - 2)], brow)
    elif c.get("brows") == "worried":
        put(im, [(b.x0 + 2, y - 1), (b.x0 + 3, y - 2), (b.x0 + 4, y - 2), (b.x1 - 5, y - 2), (b.x1 - 4, y - 2), (b.x1 - 3, y - 1)], brow)
    else:
        put(im, [(b.x0 + 2, y - 2), (b.x0 + 3, y - 2), (b.x0 + 4, y - 2), (b.x1 - 5, y - 2), (b.x1 - 4, y - 2), (b.x1 - 3, y - 2)], brow)
    put(im, [(16, y + 3)], b.skin[1])                                   # nose
    if c.get("blush", True):
        put(im, [(b.x0 + 2, y + 4), (b.x0 + 3, y + 4), (b.x1 - 3, y + 4), (b.x1 - 2, y + 4)], (226, 150, 132) if c["skin"] in ("light", "fair", "olive") else (176, 96, 80))
    if c.get("freckles"):
        put(im, [(b.x0 + 4, y + 4), (b.x1 - 5, y + 4), (14, y + 3), (18, y + 3)], b.skin[1])
    if elder:
        put(im, [(b.x0 + 2, b.mouth_y - 1), (b.x1 - 2, b.mouth_y - 1)], b.skin[1])
    m = (150, 74, 64)
    my = b.mouth_y
    mood = c.get("mouth", "smile")
    if mood == "smile":
        put(im, [(14, my), (17, my), (15, my + 1), (16, my + 1)], m)
    elif mood == "grin":
        put(im, [(13, my), (18, my)], m); put(im, [(14, my), (15, my), (16, my), (17, my)], WHITE); put(im, [(14, my + 1), (15, my + 1), (16, my + 1), (17, my + 1)], m)
    elif mood == "frown":
        put(im, [(14, my + 1), (17, my + 1), (15, my), (16, my)], m)
    elif mood == "o":
        put(im, [(15, my), (16, my), (15, my + 1), (16, my + 1)], (110, 46, 44))
    elif mood == "smug":
        put(im, [(14, my), (15, my), (16, my), (17, my - 1)], m)
    else:
        put(im, [(14, my), (15, my), (16, my), (17, my)], m)
    if c.get("sweat"):
        put(im, [(b.x1, b.y0 + 3), (b.x1, b.y0 + 4), (b.x1 + 1, b.y0 + 5)], (140, 190, 230))


def hair_front(im, b):
    st = b.c.get("hair")
    h = b.hair
    x0, x1, y0, y1, HH = b.x0, b.x1, b.y0, b.y1, b.HH
    if b.c.get("hat", (None,))[0] == "hood":
        return
    if st == "bun" or st == "updo" or st == "long" or st == "braid":
        part(im, lambda d: d.polygon([(x0 - 1, y0 + 10), (x0 - 1, y0 + 3), (x0 + 2, y0 - 1), (x0 + 6, y0 - 2), (x1 - 5, y0 - 2), (x1 - 1, y0 - 1), (x1 + 1, y0 + 3), (x1 + 1, y0 + 10),
                                      (x1 - 1, y0 + 10), (x1 - 2, y0 + 5), (x1 - 5, y0 + 3), (16, y0 + 3), (15, y0 + 3), (x0 + 5, y0 + 3), (x0 + 2, y0 + 5), (x0 + 1, y0 + 10)], fill=255), h, shade=(2, 0))
        put(im, [(15, y0 - 1), (15, y0), (15, y0 + 1), (16, y0 + 2)], h[1])
        put(im, [(x0 + 3, y0), (x1 - 3, y0 - 1)], h[3])
        if st == "braid":
            part(im, lambda d: d.rounded_rectangle((x1 - 2, y1 - 6, x1 + 1, b.S + 12), 1, fill=255), h)
            put(im, [(x1 - 1, y) for y in range(y1 - 4, b.S + 12, 3)], h[0])
    elif st == "short" or st == "curtains":
        part(im, lambda d: d.polygon([(x0 - 1, y0 + 8), (x0, y0 + 1), (x0 + 4, y0 - 2), (x1 - 4, y0 - 2), (x1, y0 + 1), (x1 + 1, y0 + 8), (x1, y0 + 8),
                                      (x1 - 1, y0 + 4), (x1 - 4, y0 + 3), (x1 - 7, y0 + 5), (x0 + 6, y0 + 3), (x0 + 2, y0 + 4), (x0, y0 + 8)], fill=255), h, shade=(2, 0))
        put(im, [(x0 + 3, y0), (x0 + 5, y0 - 1), (x1 - 4, y0)], h[3])
    elif st == "messy":
        part(im, lambda d: d.polygon([(x0 - 1, y0 + 9), (x0 - 1, y0 + 3), (x0 + 3, y0 - 1), (x0 + 6, y0 - 2), (x0 + 7, y0 - 6), (x0 + 9, y0 - 2), (x1 - 2, y0 - 1), (x1 + 1, y0 + 3),
                                      (x1 + 1, y0 + 8), (x1 - 1, y0 + 5), (x1 - 3, y0 + 7), (x1 - 5, y0 + 4), (x0 + 8, y0 + 6), (x0 + 6, y0 + 4), (x0 + 4, y0 + 7), (x0 + 2, y0 + 4), (x0 + 1, y0 + 9)], fill=255), h, shade=(2, 0))
        put(im, [(x0 + 3, y0 + 1), (x0 + 7, y0 - 4), (x1 - 3, y0 + 1)], h[3])
    elif st == "bob":
        part(im, lambda d: d.polygon([(x0 - 2, y0 + 7), (x0, y0), (x0 + 4, y0 - 2), (x1 - 4, y0 - 2), (x1, y0), (x1 + 2, y0 + 7), (x1, y0 + 5), (x0, y0 + 5)], fill=255), h, shade=(2, 0))
        put(im, [(x0 + 3, y0), (x1 - 4, y0 - 1)], h[3])
    elif st == "curly":
        part(im, lambda d: [d.ellipse((x0 - 2 + i * 4, y0 - 3 + (i % 2), x0 + 3 + i * 4, y0 + 3 + (i % 2)), fill=255) for i in range(5)] +
             [d.ellipse((x0 - 3, y0 + 1, x0 + 2, y0 + 9), fill=255), d.ellipse((x1 - 2, y0 + 1, x1 + 3, y0 + 9), fill=255)], h, shade=(2, 0))
        put(im, [(x0 + 1 + i * 4, y0 - 1) for i in range(5)], h[3])
    elif st == "pigtails":
        part(im, lambda d: d.polygon([(x0 - 1, y0 + 7), (x0, y0), (x0 + 4, y0 - 2), (x1 - 4, y0 - 2), (x1, y0), (x1 + 1, y0 + 7), (x1 - 1, y0 + 4), (16, y0 + 3), (x0 + 1, y0 + 4)], fill=255), h, shade=(2, 0))
        put(im, [(x0 - 1, y0 + 6), (x0 - 2, y0 + 6), (x1 + 1, y0 + 6), (x1 + 2, y0 + 6)], (200, 60, 70))
    elif st == "ponytail":
        part(im, lambda d: d.polygon([(x0 - 1, y0 + 8), (x0, y0 + 1), (x0 + 4, y0 - 2), (x1 - 4, y0 - 2), (x1 + 1, y0 + 2), (x1 + 1, y0 + 8), (x1, y0 + 4), (x0 + 5, y0 + 3), (x0 + 1, y0 + 5)], fill=255), h, shade=(2, 0))
        part(im, lambda d: d.polygon([(x1, y0 + 1), (x1 + 4, y0 + 3), (x1 + 4, y0 + 13), (x1 + 1, y0 + 9)], fill=255), h, shade=(0, 0))
    elif st == "slick":
        part(im, lambda d: d.chord((x0 - 1, y0 - 2, x1 + 1, y0 + 14), 180, 360, fill=255), h, shade=(2, 0))
        part(im, lambda d: d.polygon([(x0 - 1, y0 + 6), (x0 + 6, y0 + 2), (x1 + 1, y0 + 4), (x1 + 1, y0 + 7), (x0 + 6, y0 + 5), (x0, y0 + 9)], fill=255), h, shade=(0, 0))
        put(im, [(x0 + 3, y0 + 1), (x0 + 5, y0), (x1 - 3, y0 + 1)], h[3]); put(im, [(x0 + 5, y0 + 2), (x0 + 5, y0 + 3)], h[1])
    elif st == "buzz":
        part(im, lambda d: d.chord((x0, y0 - 1, x1, y0 + 12), 180, 360, fill=255), h, shade=(0, 0), light_top=0)
    elif st == "balding":
        part(im, lambda d: (d.rectangle((x0 - 1, y0 + 4, x0 + 1, y0 + 10), fill=255), d.rectangle((x1 - 1, y0 + 4, x1 + 1, y0 + 10), fill=255)), h, shade=(0, 0))
        put(im, [(x0 + 4, y0 + 1), (x0 + 5, y0 + 1)], b.skin[3])
    elif st == "bald":
        put(im, [(x0 + 4, y0 + 1), (x0 + 5, y0 + 1), (x0 + 4, y0 + 2)], b.skin[3])
    elif st == "tonsure":
        part(im, lambda d: d.chord((x0 - 1, y0 - 1, x1 + 1, y0 + 14), 180, 360, fill=255), h, shade=(0, 0))
        part(im, lambda d: d.ellipse((x0 + 3, y0 - 1, x1 - 3, y0 + 4), fill=255), b.skin, shade=(0, 0), light_top=0)
    elif st in ("wild", "longwild"):
        part(im, lambda d: d.chord((x0 - 1, y0 - 1, x1 + 1, y0 + 10), 180, 360, fill=255), h, shade=(0, 0))
    elif st == "topknot":
        part(im, lambda d: d.chord((x0 - 1, y0 - 2, x1 + 1, y0 + 12), 180, 360, fill=255), h, shade=(2, 0))
        put(im, [(15, y0 - 1), (15, y0), (16, y0 + 1)], h[1])
    elif st == "fringe":  # long fringe over one eye
        part(im, lambda d: d.polygon([(x0 - 1, y0 + 9), (x0, y0 + 1), (x0 + 4, y0 - 2), (x1 - 3, y0 - 2), (x1 + 1, y0 + 2), (x1 + 1, y0 + 9), (x1 - 1, y0 + 6),
                                      (x1 - 4, y0 + 4), (x0 + 6, y0 + 4), (x0 + 5, b.eye_y + 2), (x0 + 1, b.eye_y + 1), (x0, y0 + 9)], fill=255), h, shade=(2, 0))


def beard(im, b):
    st = b.c.get("beard")
    if not st:
        return
    hc = ramp(HAIRC[b.c.get("beard_color", b.c.get("hair_color", "darkbrown"))])
    x0, x1, y1, my = b.x0, b.x1, b.y1, b.mouth_y
    if st in ("full", "long", "short"):
        bottom = y1 + {"full": 2, "long": 12, "short": 0}[st]
        part(im, lambda d: d.polygon([(x0, b.eye_y + 3), (x0 + 2, b.eye_y + 3), (x0 + 3, my - 2), (x1 - 3, my - 2), (x1 - 2, b.eye_y + 3), (x1, b.eye_y + 3),
                                      (x1, y1 - 3), (16, bottom), (15, bottom), (x0, y1 - 3)], fill=255), hc, shade=(2, 0))
        put(im, [(14, my), (15, my), (16, my), (17, my)], (120, 60, 52))
        if st == "long":
            put(im, [(15, y) for y in range(y1, bottom, 2)] + [(13, y1 + 2), (18, y1 + 3)], hc[1])
    if st in ("mustache", "handlebar", "full", "long", "short", "thin"):
        w = {"thin": 1}.get(st, 2)
        put(im, [(x, my - 1) for x in range(13, 19)] + ([(x, my - 2) for x in range(14, 18)] if w == 2 else []), hc[2] if st != "thin" else hc[1])
        if st == "handlebar":
            put(im, [(12, my - 1), (11, my - 2), (19, my - 1), (20, my - 2)], hc[2])
    if st == "mutton":
        part(im, lambda d: (d.rectangle((x0, b.eye_y + 1, x0 + 2, my + 1), fill=255), d.rectangle((x1 - 2, b.eye_y + 1, x1, my + 1), fill=255)), hc, shade=(0, 0))
        put(im, [(x, my - 1) for x in range(x0 + 2, x1 - 1)], hc[2])
    if st == "stubble":
        put(im, [(x, y) for x in range(x0 + 2, x1 - 1) for y in range(my - 1, y1) if (x + y) % 2 == 0 and not (13 <= x <= 18 and y in (my, my + 1))], b.skin[1])


def hat(im, b):
    kind, *rest = b.c.get("hat", (None,))
    if not kind:
        return
    col = ramp(rest[0]) if rest else None
    x0, x1, y0 = b.x0, b.x1, b.y0
    if kind == "felt":
        part(im, lambda d: d.rounded_rectangle((x0, y0 - 5, x1, y0 + 4), 5, fill=255), col, shade=(3, 0))
        part(im, lambda d: d.rectangle((x0, y0 + 1, x1, y0 + 3), fill=255), ramp((66, 42, 28)), shade=(0, 0), light_top=0)
        part(im, lambda d: d.ellipse((x0 - 5, y0 + 2, x1 + 5, y0 + 7), fill=255), col, shade=(3, 0), light_top=0)
        if len(rest) > 1 and rest[1] == "wheat":
            put(im, [(x1 - 1, y0 - 2), (x1, y0 - 3), (x1 + 1, y0 - 4), (x1 - 1, y0)], (226, 186, 92))
    elif kind == "cap":
        part(im, lambda d: d.chord((x0 - 1, y0 - 3, x1 + 1, y0 + 9), 180, 360, fill=255), col, shade=(2, 0))
        part(im, lambda d: d.rectangle((x0 + 1, y0 + 2, x1 - 1, y0 + 4), fill=255), col, shade=(0, 0), light_top=0)
    elif kind == "wizard":
        part(im, lambda d: d.polygon([(x0 - 1, y0 + 3), (x1 + 1, y0 + 3), (x1 - 3, y0 - 6), (x1 + 4, y0 - 15), (x1 - 6, y0 - 9), (x0 + 3, y0 - 3)], fill=255), col, shade=(2, 0))
        part(im, lambda d: d.ellipse((x0 - 5, y0 + 1, x1 + 5, y0 + 6), fill=255), col, shade=(3, 0), light_top=0)
        put(im, [(x0 + 4, y0 - 1), (x1 - 4, y0 - 6), (x1, y0 - 11)], (240, 216, 110))
    elif kind == "captain":
        part(im, lambda d: d.polygon([(x0 - 5, y0 + 3), (x0 + 2, y0 - 4), (x1 - 2, y0 - 4), (x1 + 5, y0 + 3), (x1, y0 + 4), (x0, y0 + 4)], fill=255), col, shade=(3, 0))
        put(im, [(x, y0 + 3) for x in range(x0 - 3, x1 + 4)], (214, 176, 80))
        part(im, lambda d: d.polygon([(x0 + 1, y0 - 3), (x0 - 2, y0 - 10), (x0 + 3, y0 - 8), (x0 + 5, y0 - 3)], fill=255), ramp(WHITE), shade=(0, 0))
        put(im, [(16, y0 - 1), (15, y0 - 1)], (214, 176, 80))
    elif kind == "helmet":
        part(im, lambda d: d.chord((x0 - 1, y0 - 4, x1 + 1, y0 + 12), 180, 360, fill=255), col, shade=(3, 0))
        part(im, lambda d: d.ellipse((x0 - 5, y0 + 2, x1 + 5, y0 + 6), fill=255), col, shade=(3, 0), light_top=0)
        put(im, [(x0 + 4, y0 - 2), (x0 + 5, y0 - 2)], (230, 232, 236))
    elif kind == "pot":
        part(im, lambda d: d.chord((x0 - 3, y0 - 5, x1 + 3, y0 + 15), 180, 360, fill=255), col, shade=(3, 0))
        part(im, lambda d: d.rectangle((x0 - 3, y0 + 4, x1 + 3, y0 + 6), fill=255), col, shade=(0, 0), light_top=0)
        put(im, [(x0 + 2, y0 - 2), (x0 + 3, y0 - 3)], (230, 232, 236))
    elif kind == "straw":
        part(im, lambda d: d.rounded_rectangle((x0 + 1, y0 - 4, x1 - 1, y0 + 3), 4, fill=255), col, shade=(3, 0))
        part(im, lambda d: d.ellipse((x0 - 7, y0 + 1, x1 + 7, y0 + 6), fill=255), col, shade=(3, 0), light_top=0)
        put(im, [(x, y0 + 1) for x in range(x0 + 2, x1 - 1)], (176, 60, 50))
    elif kind in ("coif", "bonnet"):
        part(im, lambda d: d.chord((x0 - 2, y0 - 3, x1 + 2, y0 + 20), 180, 360, fill=255), col, shade=(2, 0))
        part(im, lambda d: (d.rectangle((x0 - 2, y0 + 8, x0 + 1, b.y1 - 4), fill=255), d.rectangle((x1 - 1, y0 + 8, x1 + 2, b.y1 - 4), fill=255)), col, shade=(0, 0))
        if kind == "bonnet":
            put(im, [(x, y0 + 7 + (x % 2)) for x in range(x0 - 1, x1 + 2)], (250, 240, 236))
            put(im, [(x1 + 1, b.y1 - 3), (x1 + 2, b.y1 - 2), (x1 + 2, b.y1 - 1)], col[2])
    elif kind == "hood":
        part(im, lambda d: d.chord((x0 - 3, y0 - 3, x1 + 3, y0 + 12), 180, 360, fill=255), col, shade=(3, 0))
        put(im, [(x, y0 + 4) for x in range(x0, x1 + 1)], col[0])
    elif kind == "maid":
        part(im, lambda d: d.rectangle((x0 + 1, y0 - 3, x1 - 1, y0 + 1), fill=255), ramp(WHITE), shade=(0, 0))
        put(im, [(x, y0 - 4) for x in range(x0 + 1, x1, 2)], WHITE)
        put(im, [(x, y0 + 1) for x in range(x0 + 1, x1)], (40, 40, 48))
    elif kind == "kerchief":
        part(im, lambda d: d.chord((x0 - 2, y0 - 3, x1 + 2, y0 + 14), 180, 360, fill=255), col, shade=(2, 0))
        part(im, lambda d: d.polygon([(x1, y0 + 1), (x1 + 5, y0 - 2), (x1 + 5, y0 + 3), (x1 + 1, y0 + 4)], fill=255), col, shade=(0, 0))
    elif kind == "beret":
        part(im, lambda d: d.ellipse((x0 - 2, y0 - 4, x1 + 3, y0 + 3), fill=255), col, shade=(3, 0))
        put(im, [(16, y0 - 5)], col[0])
    elif kind == "bandana":
        part(im, lambda d: d.rectangle((x0 - 1, y0 + 1, x1 + 1, y0 + 4), fill=255), col, shade=(0, 0))
        part(im, lambda d: d.polygon([(x1, y0 + 2), (x1 + 5, y0 + 6), (x1 + 3, y0 + 8), (x1, y0 + 4)], fill=255), col, shade=(0, 0))
    elif kind == "miller":
        part(im, lambda d: d.ellipse((x0 - 1, y0 - 4, x1 + 4, y0 + 5), fill=255), col, shade=(3, 0))
        part(im, lambda d: d.rectangle((x0, y0 + 2, x1, y0 + 4), fill=255), col, shade=(0, 0), light_top=0)
    elif kind == "ribbon":
        put(im, [(x1 - 1, y0 + 1), (x1, y0), (x1 + 1, y0 + 1), (x1, y0 + 2), (x1 + 2, y0), (x1 + 2, y0 + 2)], col[2])
        put(im, [(x1 + 1, y0 + 1)], col[0])
    elif kind == "clip":
        put(im, [(x0 + 2, y0 + 2), (x0 + 3, y0 + 1), (x0 + 4, y0 + 2), (x0 + 3, y0 + 3)], col[2])
    elif kind == "bandage":
        part(im, lambda d: d.rectangle((x0, y0 + 1, x1, y0 + 4), fill=255), ramp(WHITE), shade=(0, 0))
        put(im, [(x1 - 3, y0 + 2), (x1 - 4, y0 + 3)], (190, 70, 70))


# ---------------------------------------------------------------- props
def prop(im, b, p=None, side="r"):
    p = p or b.c.get("prop")
    if not p:
        return
    hr = b.hands.get(side, (0, 0))
    hl = b.hands.get("l", (0, 0))
    d = ImageDraw.Draw(im)
    if p == "lantern":
        x, y = hr
        part(im, lambda dd: dd.rectangle((x - 2, y + 2, x + 2, y + 8), fill=255), ramp((70, 60, 50)), shade=(0, 0))
        put(im, [(x - 1, y + 4), (x, y + 4), (x + 1, y + 4), (x - 1, y + 5), (x, y + 5), (x + 1, y + 5), (x, y + 6)], (255, 214, 100))
        put(im, [(x, y + 1)], (70, 60, 50))
    elif p == "tankard":
        x, y = hr
        part(im, lambda dd: dd.rectangle((x - 2, y - 7, x + 2, y - 1), fill=255), ramp((150, 100, 56)), shade=(0, 0))
        put(im, [(x - 2, y - 8), (x - 1, y - 9), (x, y - 8), (x + 1, y - 9), (x + 2, y - 8)], WHITE)
    elif p in ("book", "ledger", "redbook"):
        x, y = hl if p == "redbook" else (16, hr[1])
        col = {"book": (120, 60, 40), "ledger": (40, 90, 60), "redbook": (160, 40, 44)}[p]
        w = 5 if p == "ledger" else 4
        part(im, lambda dd: dd.rectangle((x - w, y - 4, x + w - 1, y + 2), fill=255), ramp(col), shade=(0, 0))
        put(im, [(x - w + 1, y - 3 + i) for i in range(0, 5, 2)], (230, 214, 160))
    elif p in ("staff", "pitchfork", "spear", "cane", "broom"):
        x, y = hr
        top = {"staff": 4, "pitchfork": 2, "spear": 0, "cane": y - 2, "broom": 6}[p]
        part(im, lambda dd: dd.rectangle((x, top, x + 1, 61), fill=255), ramp((120, 84, 50)), shade=(0, 0), light_top=0)
        if p == "staff":
            part(im, lambda dd: dd.ellipse((x - 2, top - 5, x + 3, top + 1), fill=255), ramp((120, 190, 230)), shade=(0, 0))
            put(im, [(x - 1, top - 4)], WHITE); put(im, [(x - 3, top - 6), (x + 4, top - 3)], (180, 230, 250))
        if p == "pitchfork":
            put(im, [(x - 2, y) for y in range(top - 5, top + 1)] + [(x + 3, y) for y in range(top - 5, top + 1)] + [(x, y) for y in range(top - 6, top)] + [(x - 2 + i, top) for i in range(6)], (150, 150, 156))
        if p == "spear":
            part(im, lambda dd: dd.polygon([(x - 1, top), (x + 2, top), (x + 0.5, top - 6)], fill=255), ramp((190, 190, 196)), shade=(0, 0))
        if p == "cane":
            put(im, [(x - 1, top), (x - 2, top), (x - 2, top + 1)], (120, 84, 50))
        part(im, lambda dd: dd.ellipse((x - 2, y - 2, x + 3, y + 2), fill=255), b.skin, light_top=0)
    elif p == "duster":
        x, y = hr
        put(im, [(x, y + i) for i in range(-6, 1)], (120, 84, 50))
        part(im, lambda dd: dd.ellipse((x - 3, y - 13, x + 3, y - 5), fill=255), ramp((196, 120, 150)), shade=(0, 0))
    elif p == "hammer":
        x, y = hr
        put(im, [(x, y - i) for i in range(1, 8)], (120, 84, 50))
        part(im, lambda dd: dd.rectangle((x - 3, y - 11, x + 3, y - 8), fill=255), ramp((110, 110, 118)), shade=(0, 0))
    elif p == "wooden_sword":
        x, y = hr
        part(im, lambda dd: dd.rectangle((x, y - 15, x + 1, y - 2), fill=255), ramp((176, 132, 84)), shade=(0, 0), light_top=0)
        put(im, [(x - 2, y - 2), (x - 1, y - 2), (x + 2, y - 2), (x + 3, y - 2)], (120, 84, 50))
    elif p == "orb":
        x, y = hr
        d.ellipse((x - 3, y - 9, x + 3, y - 3), fill=(160, 120, 240, 255))
        put(im, [(x - 1, y - 8), (x, y - 8)], (240, 230, 255))
        put(im, [(x - 5, y - 11), (x + 5, y - 9), (x + 4, y - 13), (x - 4, y - 4)], (210, 190, 255))
    elif p == "slingshot":
        x, y = hr
        put(im, [(x, y - 1), (x, y - 2), (x, y - 3), (x - 1, y - 4), (x - 2, y - 5), (x + 1, y - 4), (x + 2, y - 5)], (120, 84, 50))
        put(im, [(x - 2, y - 6), (x, y - 5), (x + 2, y - 6)], (180, 60, 50))
    elif p == "apple":
        x, y = 16, hr[1]
        part(im, lambda dd: dd.ellipse((x - 3, y - 4, x + 2, y + 1), fill=255), ramp((200, 50, 50)), shade=(0, 0))
        put(im, [(x - 1, y - 5)], (90, 140, 60))
    elif p in ("basket_bread", "basket_apples", "basket"):
        x, y = 16, hr[1]
        part(im, lambda dd: dd.rounded_rectangle((x - 6, y - 3, x + 5, y + 4), 2, fill=255), ramp((176, 132, 80)), shade=(0, 0))
        fill = {"basket_bread": (214, 160, 96), "basket_apples": (200, 50, 50), "basket": (230, 220, 200)}[p]
        put(im, [(x - 4, y - 4), (x - 2, y - 5), (x, y - 4), (x + 2, y - 5), (x + 3, y - 4), (x - 3, y - 3), (x + 1, y - 3)], fill)
        put(im, [(x - 6 + i, y) for i in range(0, 12, 2)], (130, 92, 54))
    elif p == "purse":
        x, y = 16, hr[1]
        part(im, lambda dd: dd.ellipse((x - 3, y - 3, x + 3, y + 3), fill=255), ramp((120, 84, 50)), shade=(0, 0))
        put(im, [(x - 1, y - 4), (x, y - 4), (x + 4, y - 1), (x + 5, y)], (230, 196, 90))
    elif p == "yarn":
        x, y = 16, hr[1]
        part(im, lambda dd: dd.ellipse((x - 3, y - 3, x + 2, y + 2), fill=255), ramp((180, 80, 110)), shade=(0, 0))
        put(im, [(x - 5, y - 5), (x - 4, y - 4), (x + 4, y - 5), (x + 3, y - 4)], (200, 200, 206))
    elif p == "tray":
        x, y = 16, hr[1]
        part(im, lambda dd: dd.rectangle((x - 8, y - 1, x + 7, y), fill=255), ramp((150, 110, 70)), shade=(0, 0))
        for mx in (x - 5, x + 2):
            part(im, lambda dd, mx=mx: dd.rectangle((mx, y - 6, mx + 3, y - 2), fill=255), ramp((150, 100, 56)), shade=(0, 0))
            put(im, [(mx, y - 7), (mx + 1, y - 7), (mx + 2, y - 7), (mx + 3, y - 7)], WHITE)
    elif p == "ladle":
        x, y = hr
        put(im, [(x, y - i) for i in range(1, 9)], (150, 150, 156))
        part(im, lambda dd: dd.ellipse((x - 2, y - 12, x + 2, y - 8), fill=255), ramp((150, 150, 156)), shade=(0, 0))
    elif p == "sack":
        x, y = hr
        part(im, lambda dd: dd.ellipse((x - 3, y - 9, x + 9, y + 2), fill=255), ramp((222, 206, 170)), shade=(3, 0))
        put(im, [(x + 1, y - 6), (x + 4, y - 4), (x + 2, y - 2)], WHITE)
    elif p == "bucket":
        x, y = hr
        part(im, lambda dd: dd.polygon([(x - 3, y + 2), (x + 3, y + 2), (x + 2, y + 8), (x - 2, y + 8)], fill=255), ramp((140, 104, 70)), shade=(0, 0))
        put(im, [(x - 2, y + 3), (x - 1, y + 3), (x, y + 3), (x + 1, y + 3)], (110, 160, 210))
    elif p == "bow":
        x, y = hl
        d.arc((x - 6, y - 16, x + 2, y + 10), 100, 260, fill=(120, 84, 50, 255), width=2)
        put(im, [(x, y - 13 + i) for i in range(0, 23)], (210, 206, 196))
    elif p == "shield":
        x, y = hl
        part(im, lambda dd: dd.ellipse((x - 7, y - 9, x + 3, y + 3), fill=255), ramp((150, 60, 50)), shade=(2, 0))
        part(im, lambda dd: dd.ellipse((x - 3, y - 5, x - 1, y - 1), fill=255), ramp((180, 180, 186)), shade=(0, 0))
    elif p == "mortar":
        x, y = 16, hr[1]
        part(im, lambda dd: dd.chord((x - 4, y - 5, x + 3, y + 3), 0, 180, fill=255), ramp((150, 140, 130)), shade=(0, 0))
        put(im, [(x + 1, y - 5), (x + 2, y - 6), (x + 3, y - 7)], (180, 170, 160)); put(im, [(x - 2, y - 2), (x - 1, y - 2)], (110, 160, 80))
    elif p == "watering_can":
        x, y = hr
        part(im, lambda dd: dd.rectangle((x - 3, y + 2, x + 3, y + 7), fill=255), ramp((120, 140, 150)), shade=(0, 0))
        put(im, [(x + 4, y + 3), (x + 5, y + 2), (x + 6, y + 1)], (120, 140, 150)); put(im, [(x + 7, y + 2), (x + 7, y + 4)], (140, 190, 230))
    elif p == "teapot":
        x, y = 16, hr[1]
        part(im, lambda dd: dd.ellipse((x - 4, y - 4, x + 3, y + 2), fill=255), ramp((236, 236, 240)), shade=(0, 0))
        put(im, [(x + 4, y - 2), (x + 5, y - 3), (x - 5, y - 2), (x - 5, y - 1), (x, y - 5)], (200, 200, 210)); put(im, [(x - 1, y - 2), (x + 1, y - 1)], (90, 120, 190))
    elif p == "scroll":
        x, y = 16, hr[1]
        part(im, lambda dd: dd.rectangle((x - 5, y - 3, x + 4, y + 1), fill=255), ramp((236, 222, 186)), shade=(0, 0))
        put(im, [(x - 3, y - 2), (x - 1, y - 2), (x + 1, y - 2), (x - 2, y), (x + 2, y)], (120, 100, 80))
        put(im, [(x + 5, y - 6), (x + 4, y - 5), (x + 3, y - 4)], WHITE)
    elif p == "toy_horse":
        x, y = 16, hr[1]
        part(im, lambda dd: dd.polygon([(x - 4, y), (x + 2, y), (x + 4, y - 4), (x + 2, y - 5), (x + 1, y - 2), (x - 4, y - 2)], fill=255), ramp((196, 150, 96)), shade=(0, 0))
        put(im, [(x - 3, y + 1), (x + 1, y + 1)], (120, 84, 50))
    elif p == "rattle":
        x, y = hr
        put(im, [(x, y - 1), (x, y - 2)], (200, 200, 206)); part(im, lambda dd: dd.ellipse((x - 2, y - 6, x + 2, y - 2), fill=255), ramp((230, 120, 120)), shade=(0, 0))
    elif p == "sword":
        x, y = hr
        part(im, lambda dd: dd.rectangle((x, y + 2, x + 1, y + 16), fill=255), ramp((196, 200, 206)), shade=(0, 0), light_top=0)
        put(im, [(x - 2, y + 2), (x - 1, y + 2), (x + 2, y + 2), (x + 3, y + 2)], (150, 120, 60)); put(im, [(x, y - 2), (x + 1, y - 2)], (150, 120, 60))
    elif p == "torch":
        x, y = hr
        put(im, [(x, y + i) for i in range(-2, 6)], (110, 76, 46))
        d.ellipse((x - 3, y - 9, x + 3, y - 1), fill=(236, 120, 40, 255)); d.ellipse((x - 1, y - 6, x + 2, y - 2), fill=(255, 220, 110, 255))
        put(im, [(x, y - 11), (x + 1, y - 10), (x - 2, y - 10)], (210, 70, 40))
    elif p == "candle":
        x, y = hr
        part(im, lambda dd: dd.rectangle((x - 1, y - 7, x, y - 1), fill=255), ramp((240, 236, 222)), shade=(0, 0), light_top=0)
        put(im, [(x - 1, y - 9), (x, y - 9), (x, y - 10)], (255, 214, 100)); put(im, [(x - 1, y - 8)], (240, 140, 50))
    elif p == "lamp":
        x, y = hr
        put(im, [(x, y + 1), (x, y + 2)], (90, 80, 70))
        part(im, lambda dd: dd.rectangle((x - 2, y + 3, x + 2, y + 9), fill=255), ramp((210, 226, 230)), shade=(0, 0), light_top=0)
        put(im, [(x - 1, y + 5), (x, y + 5), (x + 1, y + 5), (x, y + 4), (x, y + 6), (x - 1, y + 6), (x + 1, y + 6)], (255, 214, 100))
        part(im, lambda dd: dd.rectangle((x - 3, y + 9, x + 3, y + 11), fill=255), ramp((190, 150, 70)), shade=(0, 0), light_top=0)
    elif p == "herbs":
        x, y = 16, hr[1]
        for i, col in enumerate([(110, 140, 70), (140, 110, 60), (90, 120, 80), (150, 130, 160), (110, 140, 70)]):
            put(im, [(x - 4 + i * 2, y - 6 + (i % 2)), (x - 4 + i * 2, y - 5 + (i % 2)), (x - 3 + i * 2, y - 4)], col)
        put(im, [(x - 1, y - 3), (x, y - 3), (x + 1, y - 3), (x, y - 2), (x, y - 1)], (120, 84, 50)); put(im, [(x - 1, y - 2), (x + 1, y - 2)], (176, 50, 44))
    elif p == "potlid":
        x, y = hl
        part(im, lambda dd: dd.ellipse((x - 6, y - 6, x + 2, y + 2), fill=255), ramp((160, 160, 168)), shade=(2, 0))
        put(im, [(x - 2, y - 2), (x - 3, y - 2)], (90, 90, 96))
    elif p == "finger":
        x, y = hr
        put(im, [(x, y - 3), (x, y - 4), (x, y - 5)], b.skin[2]); put(im, [(x + 1, y - 4), (x + 1, y - 5)], b.skin[0])
    elif p == "shovel":
        x, y = hr
        part(im, lambda dd: dd.rectangle((x, 26, x + 1, 56), fill=255), ramp((120, 84, 50)), shade=(0, 0), light_top=0)
        part(im, lambda dd: dd.rounded_rectangle((x - 2, 54, x + 3, 61), 2, fill=255), ramp((150, 150, 156)), shade=(0, 0))
        part(im, lambda dd: dd.ellipse((x - 2, y - 2, x + 3, y + 2), fill=255), b.skin, light_top=0)


def bless_hand(im, b):
    """Aldous's right hand raised in blessing, two fingers up."""
    x, y = b.hands["r"]
    put(im, [(x - 1, y - 3), (x, y - 4), (x + 1, y - 3)], b.skin[2])


# ---------------------------------------------------------------- character
def baby(c):
    im = Image.new("RGBA", (32, 64), (0, 0, 0, 0))
    skin, hair = ramp(SKIN[c["skin"]], 0.5), ramp(HAIRC[c["hair_color"]])
    part(im, lambda d: d.ellipse((7, 48, 25, 62), fill=255), ramp((236, 214, 140)), shade=(3, 0))
    part(im, lambda d: d.ellipse((6, 54, 12, 61), fill=255), skin, shade=(0, 0), light_top=0)
    part(im, lambda d: d.ellipse((20, 54, 26, 61), fill=255), skin, shade=(0, 0), light_top=0)
    part(im, lambda d: d.ellipse((6, 46, 11, 51), fill=255), skin, light_top=0)
    part(im, lambda d: d.ellipse((8, 32, 24, 49), fill=255), skin, shade=(3, 0), light_top=0)
    put(im, [(15, 32), (16, 31), (17, 32), (14, 33), (13, 32)], hair[2])
    put(im, [(12, 40), (13, 40), (19, 40), (20, 40)], INK); put(im, [(12, 41), (19, 41)], EYES["blue"])
    put(im, [(11, 43), (21, 43)], (226, 150, 132)); put(im, [(15, 45), (16, 45)], (150, 74, 64))
    put(im, [(8, 44), (8, 43)], (200, 200, 206)); part(im, lambda d: d.ellipse((5, 38, 10, 43), fill=255), ramp((230, 120, 120)), shade=(0, 0))
    return im


def character(c):
    if c.get("baby"):
        return baby(c)
    b = Body(c)
    im = Image.new("RGBA", (32, 64), (0, 0, 0, 0))
    back_items(im, b)
    legs(im, b)
    torso(im, b)
    overlays_body(im, b)
    pl, pr = c.get("pose", ("down", "down"))
    order = [("l", pl), ("r", pr)]
    behind = [o for o in order if o[1] in ("down", "shoulder")]
    front = [o for o in order if o not in behind]
    for side, pose in behind:
        arm(im, b, side, pose)
    head_back(im, b)
    face(im, b)
    hair_front(im, b)
    beard(im, b)
    hat(im, b)
    for side, pose in front:
        arm(im, b, side, pose)
    if c.get("bless"):
        bless_hand(im, b)
    prop(im, b)
    if c.get("prop2"):
        prop(im, b, c["prop2"], "l")
    for ov in c.get("over", []):
        kind = ov[0] if isinstance(ov, tuple) else ov
        if kind == "crow":  # a crow perched on the left shoulder
            x, y = b.L - 3, b.S - 2
            part(im, lambda dd: (dd.ellipse((x - 3, y - 6, x + 3, y), fill=255), dd.ellipse((x - 4, y - 10, x, y - 5), fill=255),
                                 dd.polygon([(x + 1, y - 2), (x + 6, y + 3), (x + 3, y)], fill=255)), ramp((58, 58, 80), 0.3), shade=(2, 0))
            put(im, [(x - 1, y - 4), (x, y - 3), (x + 1, y - 4)], (110, 112, 150))   # wing sheen
            put(im, [(x - 5, y - 8), (x - 6, y - 8)], (210, 170, 70)); put(im, [(x - 3, y - 8)], (240, 230, 120))
        if kind == "charms":  # bone charms on a cord
            put(im, [(13, b.S + 1), (14, b.S + 2), (15, b.S + 3), (16, b.S + 3), (17, b.S + 2), (18, b.S + 1)], (90, 70, 50))
            put(im, [(14, b.S + 3), (16, b.S + 4), (16, b.S + 5), (18, b.S + 2)], (232, 224, 200))
    stage_overlays(im, b)
    if c.get("streak"):
        put(im, [(b.x1 - 3, b.y0 + i) for i in range(-1, 6)] + [(b.x1 + 1, b.y0 + 8 + i) for i in range(0, 14)], (196, 194, 192))
    return im


def stage_overlays(im, b):
    """Wear and care: rags, dirt and soot for the rescued; small personal accents for the hopeful."""
    c = b.c
    rnd = __import__("random").Random(len(c["name"]))
    px = im.load()
    for ov in c.get("over", []):
        kind, *arg = ov if isinstance(ov, tuple) else (ov,)
        if kind == "tatters":       # ragged hem and sleeves
            for x in range(4, 28):
                for y in range(48, 60):
                    if px[x, y][3] and y >= 52 + (x * 7 % 5) and px[x, y][:3] not in [ramp(b.c.get("shoes", (70, 46, 32)))[k] for k in range(4)]:
                        if y < 56:
                            px[x, y] = (0, 0, 0, 0)
            for (x, y) in ((b.L - 3, b.S + 9), (b.R + 3, b.S + 10), (b.L + 2, b.W + 3)):
                if 0 <= x < 32 and px[x, y][3]:
                    px[x, y] = (0, 0, 0, 0)
            for x in range(1, 31):     # re-outline the torn edge so it reads as cloth, not as a gap
                for y in range(46, 58):
                    if px[x, y][3] and not px[x, y + 1][3]:
                        r, g, bb, al = px[x, y]
                        px[x, y] = (int(r * 0.45), int(g * 0.45), int(bb * 0.45), al)
        elif kind == "dirt":
            for _ in range(22):
                x, y = rnd.randrange(b.L - 3, b.R + 4), rnd.randrange(b.S, 57)
                if 0 <= x < 32 and px[x, y][3]:
                    r, g, bb, a = px[x, y]
                    px[x, y] = (int(r * 0.7 + 30), int(g * 0.68 + 20), int(bb * 0.6 + 10), a)
            for (x, y) in ((b.x0 + 3, b.eye_y + 4), (b.x1 - 4, b.eye_y + 5), (b.x0 + 5, b.mouth_y + 1)):
                put(im, [(x, y)], b.skin[1])
        elif kind == "soot":
            put(im, [(b.x0 + 3, b.eye_y + 4), (b.x0 + 4, b.eye_y + 4), (b.x1 - 3, b.y0 + 3), (b.L + 2, b.S + 6), (b.R - 2, b.S + 9)], (70, 66, 66))
        elif kind == "tired":
            put(im, [(b.x0 + 3, b.eye_y + 3), (b.x0 + 4, b.eye_y + 3), (b.x1 - 4, b.eye_y + 3), (b.x1 - 3, b.eye_y + 3)], b.skin[1])
        elif kind == "patches":
            for (x, y) in ((b.L + 1, b.W + 6), (b.R - 4, b.S + 4)):
                put(im, [(x + i, y + j) for i in range(3) for j in range(3) if px[x + i, y + j][3]], (150, 130, 100))
                put(im, [(x, y), (x + 2, y + 2)], (90, 70, 50))
        elif kind == "flower":      # tucked behind the ear / in the hair band
            col = arg[0]
            put(im, [(b.x1, b.y0 + 3), (b.x1 + 1, b.y0 + 2), (b.x1 + 1, b.y0 + 4), (b.x1 + 2, b.y0 + 3)], col)
            put(im, [(b.x1 + 1, b.y0 + 3)], (250, 230, 140))
        elif kind == "scarf":
            col = ramp(arg[0])
            put(im, [(x, b.S) for x in range(12, 20)] + [(x, b.S + 1) for x in range(12, 20)], col[2])
            put(im, [(18, b.S + 2), (18, b.S + 3), (19, b.S + 4), (18, b.S + 5)], col[1])
        elif kind == "brooch":      # a small gold token: a Hope anchor they wear
            put(im, [(b.L + 3, b.S + 3), (b.L + 4, b.S + 3), (b.L + 3, b.S + 4), (b.L + 4, b.S + 4)], (226, 190, 96))
            put(im, [(b.L + 3, b.S + 3)], (255, 236, 170))
        elif kind == "tinmedal":    # a medal hammered out of a tin lid by Pip
            put(im, [(b.R - 3, b.S + 2), (b.R - 2, b.S + 2)], (176, 60, 60))
            put(im, [(b.R - 4, b.S + 3), (b.R - 3, b.S + 3), (b.R - 2, b.S + 3), (b.R - 1, b.S + 3), (b.R - 3, b.S + 4), (b.R - 2, b.S + 4)], (186, 190, 198))
        elif kind == "wristribbon":
            x, y = b.hands.get("l", (b.L - 2, b.S + 19))
            put(im, [(x - 1, y - 2), (x, y - 2), (x + 1, y - 2), (x + 2, y - 1)], arg[0])


# ---------------------------------------------------------------- the town
TOWN = [
    # Pells / Wainwrights / Cobbs
    dict(name="Father Aldous", family="Pell", age=72, job="Priest", start="town", build="slim", skin="light",
         hair="balding", hair_color="white", eyes="grey", upper=("dress", (40, 38, 48)), lower=("robe", (40, 38, 48)), neck="priest",
         over=[("rope",)], pose=("front", "raise"), prop="finger", prop2="redbook", mouth="frown", brows="stern", blush=False,
         look="gaunt, white fringe of hair, black cassock and white collar", doing="raising a finger in warning, scripture clutched to his chest"),
    dict(name="Hester Pell", family="Pell", age=68, job="Retired midwife", start="wild", height="short", skin="light",
         hair="topknot", hair_color="grey", eyes="brown", upper=("dress", (96, 68, 108)), lower=("dress", (96, 68, 108)), neck="v",
         over=[("shawl", (120, 132, 152))], pose=("down", "down"), prop="cane", mouth="flat", brows="stern",
         look="grey topknot, plum dress, blue-grey shawl", doing="leaning on a cane, seeing through everyone"),
    dict(name="Mira Wainwright", family="Wainwright", age=34, job="Baker", start="you", skin="light", hair="bun", hair_color="lightbrown",
         eyes="brown", upper=("dress", (80, 122, 118)), lower=("dress", (80, 122, 118)), neck="v", hat=("felt", (124, 60, 68), "wheat"),
         pose=("front", "front"), prop="basket", mouth="flat", lashes=True,
         look="light brown low bun, plain teal dress, felt hat with a wheat sprig (outdoors)", doing="carrying a basket of salvage"),
    dict(name="Edric Wainwright", family="Wainwright", age=36, job="Carpenter, toymaker", start="dun", height="tall", skin="olive",
         hair="curtains", hair_color="darkbrown", beard="short", eyes="green", upper=("vest", (236, 228, 210)), vest=(110, 70, 44),
         lower=("trousers", (78, 78, 86)), rolled=True, sleeve=(236, 228, 210), pose=("front", "front"), prop="toy_horse", mouth="smile",
         look="dark brown hair parted in the middle, short beard, green eyes, leather vest, rolled sleeves", doing="holding a wooden horse he carved"),
    dict(name="Pip Wainwright", family="Wainwright", age=7, job="Sprout's best friend", start="you", height="kid7", skin="light",
         hair="messy", hair_color="lightbrown", eyes="green", upper=("tunic", (184, 96, 64)), lower=("breeches", (104, 76, 54)),
         over=["suspenders"], freckles=True, pose=("down", "down"), prop="lantern", mouth="grin",
         look="messy light brown hair (Mira), green eyes (Edric), rust tunic, suspenders", doing="carrying the lantern for the window"),
    dict(name="Martha Cobb", family="Cobb", age=38, job="Seamstress, town gossip", start="wild", build="stocky", skin="light",
         hair="curly", hair_color="lightbrown", eyes="brown", upper=("dress", (204, 160, 70)), lower=("dress", (204, 160, 70)),
         hat=("bonnet", (196, 112, 130)), over=[("shawl", (176, 90, 110)), ("tape",)], pose=("hip", "hip"), mouth="grin", lashes=True,
         look="light brown curls, rose bonnet, mustard dress, tape measure round her neck", doing="hands on hips, mid-gossip"),
    dict(name="Hamish Cobb", family="Cobb", age=42, job="Provisioner", start="town", build="big", skin="fair", hair="balding",
         hair_color="ginger", beard="handlebar", eyes="blue", upper=("vest", WHITE), vest=(70, 110, 70), lower=("trousers", (96, 72, 52)),
         over=[("apron", (150, 110, 70))], pose=("front", "front"), prop="purse", mouth="smug",
         look="ginger handlebar moustache, big belly, green waistcoat, shop apron", doing="clutching his coin purse"),
    dict(name="Kit Cobb", family="Cobb", age=12, job="Troublemaker (twin)", start="wild", height="kid12", skin="fair", hair="messy",
         hair_color="ginger", eyes="blue", upper=("tunic", (70, 100, 160)), lower=("breeches", (96, 72, 52)), freckles=True,
         hat=("cap", (110, 90, 70)), pose=("down", "raise"), prop="slingshot", mouth="grin",
         look="ginger, freckles, flat cap, blue tunic", doing="aiming a slingshot"),
    dict(name="Kat Cobb", family="Cobb", age=12, job="Troublemaker (twin)", start="wild", height="kid12", skin="fair", hair="pigtails",
         hair_color="ginger", eyes="blue", upper=("dress", (90, 140, 90)), lower=("skirt", (90, 140, 90)), socks=(236, 230, 220),
         freckles=True, pose=("front", "front"), prop="apple", mouth="grin", lashes=True,
         look="ginger pigtails with red ribbons, freckles, green dress", doing="holding a stolen apple"),
    # Dunmores / Brannocks
    dict(name="Ambrose Dunmore", family="Dunmore", age=74, job="Miller", start="town", height="short", skin="brown", hair="short",
         hair_color="white", beard="full", beard_color="white", eyes="brown", upper=("tunic", (226, 220, 206)), lower=("trousers", (110, 84, 60)),
         hat=("miller", (240, 236, 228)), rolled=True, pose=("down", "shoulder"), prop="sack", mouth="smile",
         look="white beard, floppy miller's cap, everything dusted in flour", doing="carrying a flour sack on his shoulder"),
    dict(name="Hilde Dunmore", family="Dunmore", age=72, job="Miller", start="town", height="short", skin="brown", hair="bun",
         hair_color="grey", eyes="brown", upper=("dress", (150, 130, 172)), lower=("dress", (150, 130, 172)), hat=("coif", (240, 236, 228)),
         over=[("apron",)], pose=("front", "front"), prop="yarn", mouth="smile",
         look="white linen coif, lavender dress, apron", doing="knitting (it's still Harvest Fair night for her)"),
    dict(name="Nell Brannock", family="Brannock", age=45, job="Brewer, cook", start="town", build="stocky", skin="brown", hair="bun",
         hair_color="black", eyes="brown", upper=("dress", (140, 60, 60)), lower=("dress", (140, 60, 60)), hat=("kerchief", (90, 130, 80)),
         rolled=True, over=[("apron",)], pose=("down", "raise"), prop="ladle", mouth="smile",
         look="green kerchief, red dress, rolled sleeves, apron", doing="waving a ladle"),
    dict(name="Gus Brannock", family="Brannock", age=48, job="Innkeeper", start="town", height="tall", build="big", skin="dark",
         hair="bald", beard="mutton", beard_color="saltpepper", eyes="dark", upper=("tunic", (236, 228, 210)), lower=("trousers", (96, 72, 52)),
         rolled=True, over=[("apron", (226, 214, 190))], pose=("down", "raise"), prop="tankard", mouth="grin",
         look="bald, big grey mutton chops, rolled sleeves, apron", doing="raising a tankard"),
    dict(name="Tilly Brannock", family="Brannock", age=16, job="Barmaid", start="dun", height="teen", build="slim", skin="brown",
         hair="ponytail", hair_color="black", eyes="brown", upper=("vest", WHITE), vest=(176, 56, 56), lower=("dress", (60, 70, 110)),
         hat=("ribbon", (200, 50, 60)), pose=("front", "front"), prop="tray", mouth="smile", lashes=True,
         look="black ponytail with a red ribbon, red bodice, navy skirt", doing="carrying a tray of mugs"),
    # Varrs
    dict(name="Capt. Percival Varr", family="Varr", age=40, job="Captain of the guard", start="dun", height="tall", skin="fair",
         hair="slick", hair_color="black", beard="thin", eyes="grey", upper=("coat", (40, 60, 110)), shirt=WHITE, lower=("trousers", (236, 232, 222)),
         shoes=(30, 26, 30), hat=("captain", (34, 40, 70)), over=[("sash",), ("medals",), ("sword",)], pose=("hip", "hip"), mouth="smug", brows="stern",
         look="slicked black hair, thin moustache, navy coat, medals, plumed hat", doing="hands on hips, chest out, giving a speech"),
    dict(name="Cordelia Varr", family="Varr", age=37, job="Town treasurer", start="wild", build="slim", skin="fair", hair="updo",
         hair_color="black", eyes="grey", glasses=True, upper=("dress", (40, 80, 64)), lower=("dress", (40, 80, 64)), neck="collar",
         pose=("front", "front"), prop="ledger", mouth="flat", brows="stern",
         look="neat black updo, spectacles, high-collared green dress", doing="holding the town ledger"),
    dict(name="Winnie Crane", family="Varr household", age=29, job="Maid (hireable)", start="town", build="slim", skin="tan",
         hair="bob", hair_color="darkbrown", eyes="brown", upper=("dress", (44, 44, 54)), lower=("dress", (44, 44, 54)), neck="collar",
         hat=("maid", WHITE), over=[("apron",)], pose=("down", "raise"), prop="duster", mouth="smug", lashes=True,
         look="dark bob, frilled maid's cap, black dress, white apron", doing="brandishing a feather duster"),
    # Thornes
    dict(name="Ignatius Thorne", family="Thorne", age=80, job="Arcanist", start="town", height="short", skin="olive", hair="wild",
         hair_color="white", beard="long", beard_color="white", eyes="blue", glasses=True, upper=("dress", (50, 60, 130)), lower=("robe", (50, 60, 130)),
         hat=("wizard", (70, 50, 120)), over=[("belt", (200, 170, 90))], pose=("down", "down"), prop="staff", mouth="smile",
         look="wild white hair, long beard, spectacles, starry robe, pointed hat", doing="leaning on a staff with a glowing crystal"),
    dict(name="Rowan Thorne", family="Thorne", age=39, job="Farmer", start="dun", height="tall", skin="olive", hair="short",
         hair_color="darkbrown", beard="stubble", eyes="brown", upper=("vest", (226, 214, 186)), vest=(90, 110, 70), lower=("trousers", (110, 84, 60)),
         rolled=True, hat=("straw", (220, 190, 120)), pose=("down", "down"), prop="pitchfork", mouth="smile",
         look="straw hat, stubble, green vest, rolled sleeves", doing="holding a pitchfork"),
    dict(name="Elsa Thorne", family="Thorne", age=36, job="Farmer, orchard keeper", start="wild", skin="light", hair="braid",
         hair_color="blonde", eyes="blue", upper=("dress", (110, 150, 190)), lower=("dress", (110, 150, 190)), over=[("apron", (150, 110, 70))],
         pose=("front", "front"), prop="basket_apples", mouth="smile", lashes=True,
         look="blonde braid over her shoulder, light blue dress, brown apron", doing="carrying a basket of apples"),
    dict(name="Juniper Thorne", family="Thorne", age=10, job="Pip's best friend", start="wild", height="kid10", skin="olive",
         hair="bob", hair_color="darkbrown", eyes="brown", upper=("dress", (130, 90, 160)), lower=("skirt", (130, 90, 160)), socks=(70, 60, 90),
         hat=("clip", (240, 210, 90)), pose=("down", "raise"), prop="orb", mouth="o", lashes=True,
         look="dark bob with a star clip, purple dress", doing="holding up a little spark of magic"),
    dict(name="Bram Thorne", family="Thorne", age=1, job="Baby", start="wild", baby=True, skin="olive", hair_color="blonde",
         look="wisp of blonde hair, yellow romper", doing="sitting with a rattle"),
    # Fletchers
    dict(name="Garrick Fletcher", family="Fletcher", age=62, job="Stablemaster", start="town", skin="dark", hair="short",
         hair_color="grey", beard="short", beard_color="grey", eyes="dark", upper=("vest", (160, 70, 56)), vest=(110, 76, 50),
         lower=("trousers", (70, 70, 80)), hat=("cap", (90, 76, 60)), pose=("down", "raise"), prop="torch", mouth="flat",
         look="grey beard, flat cap, red shirt, leather vest", doing="holding up a torch in the dark stable"),
    dict(name="Wren Fletcher", family="Fletcher", age=26, job="Hunter", start="you", build="slim", skin="dark", hair="braid",
         hair_color="black", eyes="dark", upper=("tunic", (96, 110, 70)), lower=("trousers", (80, 66, 50)), hat=("hood", (60, 90, 60)),
         over=[("quiver",), ("belt",)], pose=("down", "down"), prop="bow", mouth="flat", brows="stern",
         look="green hood, olive tunic, quiver on her back", doing="holding a bow, watching the treeline"),
    dict(name="Tam Fletcher", family="Fletcher", age=17, job="Wants to be a hero", start="dun", height="teen", skin="dark", hair="buzz",
         hair_color="black", eyes="dark", upper=("armor", (226, 214, 186)), tabard=(176, 60, 50), lower=("trousers", (80, 66, 50)),
         hat=("pot", (150, 150, 158)), pose=("down", "raise"), prop="wooden_sword", prop2="potlid", mouth="grin",
         look="a cooking pot for a helmet, padded vest", doing="wooden sword and a pot-lid shield"),
    # Hammersleys
    dict(name="Bruna Hammersley", family="Hammersley", age=50, job="Master smith", start="dun", build="stocky", skin="fair", hair="short",
         hair_color="auburn", eyes="brown", upper=("tunic", (130, 130, 136)), lower=("trousers", (70, 60, 56)), rolled=True,
         hat=("bandana", (176, 50, 44)), over=[("leather_apron",)], pose=("down", "raise"), prop="hammer", mouth="grin", brows="stern",
         look="red bandana, short auburn hair, bare forearms, leather apron", doing="raising her hammer"),
    dict(name="Dag Hammersley", family="Hammersley", age=52, job="Armorer", start="wild", build="stocky", skin="tan", hair="bald",
         beard="full", beard_color="darkbrown", eyes="brown", upper=("armor", (150, 150, 158)), tabard=(90, 70, 50), lower=("trousers", (70, 60, 56)),
         pose=("down", "down"), prop="shield", mouth="smile",
         look="bald, full dark beard, mail shirt", doing="carrying a shield he's mending"),
    dict(name="Oswin", family="Hammersley (foster)", age=19, job="Smith's apprentice (injured)", start="you", build="slim", skin="light",
         hair="short", hair_color="blonde", eyes="blue", upper=("tunic", (186, 160, 120)), lower=("trousers", (90, 80, 70)),
         hat=("bandage",), over=[("sling",)], pose=("sling", "down"), mouth="frown", brows="worried",
         look="blond, head bandaged, arm in a sling", doing="wincing; shouldn't be up yet"),
    # Marshes
    dict(name="Sabine Marsh", family="Marsh", age=47, job="Herbalist, healer, soothsayer", start="town", build="slim", skin="brown",
         hair="long", hair_color="black", streak=True, eyes="grey", upper=("dress", (36, 44, 40)), lower=("dress", (36, 44, 40)), neck="none",
         over=[("shawl", (56, 40, 60)), ("pouches",), ("charms",), ("crow",)], pose=("front", "front"), prop="herbs", mouth="flat", brows="stern", blush=False,
         look="long black hair with a white streak, pale grey eyes, near-black dress, bone charms, a crow named Parson", doing="holding a bundle of dried grave-herbs"),
    dict(name="Linden Marsh", family="Marsh", age=19, job="Herb gardener", start="wild", build="slim", skin="brown", hair="fringe",
         hair_color="darkbrown", eyes="brown", upper=("tunic", (150, 180, 120)), lower=("trousers", (96, 80, 60)), rolled=True,
         over=[("apron", (120, 100, 70))], pose=("down", "down"), prop="watering_can", mouth="flat",
         look="long fringe over one eye, pale green shirt, garden apron", doing="carrying a watering can (and a crush on Tilly)"),
    # Barrows
    dict(name="Sgt. Holt Barrow", family="Barrow", age=55, job="Guard sergeant", start="wild", height="tall", build="stocky", skin="tan",
         hair="short", hair_color="grey", beard="short", beard_color="grey", eyes="grey", upper=("armor", (150, 150, 158)), tabard=(60, 80, 140),
         lower=("trousers", (70, 70, 80)), hat=("helmet", (150, 150, 158)), pose=("down", "down"), prop="sword", prop2="shield", mouth="flat", brows="stern",
         look="kettle helmet, grey beard, mail and a blue town tabard", doing="sword and shield, standing between his people and the dark"),
    dict(name="Lewin Barrow", family="Barrow", age=50, job="Teacher, scribe, town chronicler", start="wild", skin="dark", hair="short", hair_color="grey",
         eyes="dark", glasses=True, upper=("coat", (120, 84, 56)), shirt=(236, 228, 210), lower=("trousers", (70, 70, 80)),
         hat=("beret", (130, 40, 50)), pose=("down", "down"), prop="lamp", mouth="smile",
         look="wine beret, spectacles, long brown coat", doing="carrying an oil lamp to write by"),
    # Abbey
    dict(name="Brother Fennick", family="Abbey", age=22, job="Novice", start="town", build="slim", skin="fair", hair="tonsure",
         hair_color="lightbrown", eyes="blue", upper=("dress", (110, 84, 60)), lower=("robe", (110, 84, 60)), neck="none", over=[("rope",)],
         pose=("pray", "pray"), prop="candle", mouth="frown", brows="worried", sweat=True,
         look="tonsure, brown habit with a rope belt", doing="praying over a candle, nervously"),
    # You
    dict(name="You", family="Your household", age=35, job="The player", start="you", skin="tan", hair="short", hair_color="darkbrown",
         eyes="brown", upper=("coat", (50, 84, 70)), shirt=(236, 228, 210), lower=("trousers", (60, 56, 60)), shoes=(50, 34, 26),
         pose=("down", "down"), prop="shovel", mouth="smile",
         look="good green coat over a waistcoat (customisable later)", doing="holding a shovel, ready to rebuild"),
    dict(name="Dorrit", family="Your household", age=66, job="Your housekeeper", start="town", height="short", build="stocky", skin="light",
         hair="topknot", hair_color="white", eyes="blue", upper=("dress", (60, 70, 100)), lower=("dress", (60, 70, 100)), neck="collar",
         over=[("apron",)], pose=("front", "front"), prop="teapot", mouth="smile",
         look="white topknot, navy dress, lace collar, apron", doing="bringing a pot of tea"),
]

START = {"you": ((63, 127, 200), "with you"), "town": ((212, 138, 28), "hiding in town"),
         "wild": ((79, 154, 79), "in the wilds"), "dun": ((138, 63, 176), "in the dungeon")}
FAMILY_TINT = {"Pell": (232, 222, 200), "Wainwright": (232, 222, 200), "Cobb": (232, 222, 200), "Dunmore": (226, 218, 230),
               "Brannock": (226, 218, 230), "Varr": (218, 226, 236), "Varr household": (218, 226, 236), "Thorne": (222, 234, 218),
               "Fletcher": (236, 226, 214), "Hammersley": (230, 222, 222), "Hammersley (foster)": (230, 222, 222), "Marsh": (222, 232, 228),
               "Barrow": (228, 228, 222), "Abbey": (236, 230, 214), "Your household": (220, 230, 238)}


def slug(n):
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in n).strip("_").replace("__", "_")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "sprites").mkdir(exist_ok=True)
    sprites = []
    for c in TOWN:
        im = character(c)
        im.save(OUT / "sprites" / f"{slug(c['name'])}.png")
        sprites.append(im)
    strip = Image.new("RGBA", (32 * len(sprites), 64), (0, 0, 0, 0))
    for i, im in enumerate(sprites):
        strip.paste(im, (i * 32, 0))
    strip.save(OUT / "town_strip_32x64.png")

    bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 15)
    reg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    ita = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf", 11)
    title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 28)
    cols, cw, chh = 7, 224, 352
    rows = (len(TOWN) + cols - 1) // cols
    W, H = 30 * 2 + cols * cw, 110 + rows * chh
    sheet = Image.new("RGBA", (W, H), (243, 234, 214, 255))
    d = ImageDraw.Draw(sheet)
    d.text((30, 22), "Hollowmere: the townsfolk", font=title, fill=(58, 42, 26))
    d.text((30, 62), "Concept sprites, 32x64 shown at 3x · dot = where they are when the game starts:", font=reg, fill=(90, 74, 58))
    lx = 545
    for k_, (col, label) in START.items():
        d.ellipse((lx, 63, lx + 11, 74), fill=col); d.text((lx + 16, 62), label, font=reg, fill=(90, 74, 58)); lx += 130

    def wrap(text, font, width):
        words, lines, cur = text.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=font) <= width:
                cur = t
            else:
                lines.append(cur); cur = w
        if cur:
            lines.append(cur)
        return lines

    for i, (c, im) in enumerate(zip(TOWN, sprites)):
        x = 30 + (i % cols) * cw
        y = 100 + (i // cols) * chh
        d.rounded_rectangle((x + 4, y, x + cw - 8, y + chh - 12), 10, fill=FAMILY_TINT.get(c["family"], (236, 230, 216)), outline=(190, 172, 140))
        sheet.alpha_composite(im.resize((96, 192), Image.NEAREST), (x + (cw - 96) // 2 - 2, y + 6))
        ty = y + 202
        d.ellipse((x + 14, ty + 4, x + 25, ty + 15), fill=START[c["start"]][0])
        d.text((x + 31, ty), c["name"], font=bold, fill=(42, 30, 20))
        ty += 22
        d.text((x + 14, ty), f"{c['job']}", font=reg, fill=(60, 46, 34))
        ty += 16
        age = "baby" if c["age"] < 2 else f"{c['age']}"
        d.text((x + 14, ty), f"{c['family']} · {age}", font=reg, fill=(110, 94, 78))
        ty += 18
        for line in wrap(c["doing"][:1].upper() + c["doing"][1:], ita, cw - 34)[:4]:
            d.text((x + 14, ty), line, font=ita, fill=(84, 70, 58)); ty += 14
    sheet.save(OUT / "town_lineup.png")

    lines = ["# Hollowmere townsfolk: looks", "",
             "Generated by `tools/concept_art/town.py` together with the sprites, so it always matches them.", "",
             "![Town lineup](town_lineup.png)", "",
             "| | Name | Job | Family | Age | Look | Doing | At the start |", "|---|---|---|---|---|---|---|---|"]
    for c in TOWN:
        age = "baby" if c["age"] < 2 else str(c["age"])
        lines.append(f"| ![](sprites/{slug(c['name'])}.png) | **{c['name']}** | {c['job']} | {c['family']} | {age} | {c['look']} | {c['doing']} | {START[c['start']][1]} |")
    (OUT / "CAST.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

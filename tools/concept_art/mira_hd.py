"""Higher-resolution concept art for Mira Wainwright: 32x64 walk sprites and 128x128 portraits.

Two outfits: everyday (felt hat, belted dress) and baker (same + apron, once she agrees to bake again).

Run: python3 tools/concept_art/mira_hd.py   (writes to docs/concept-art/mira/)
Built from shaded, outlined shapes (each material has its own outline colour). Concept quality.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[2] / "docs" / "concept-art" / "mira"

# material ramps: outline, shadow, base, light
SKIN = ((126, 72, 58), (208, 148, 118), (236, 190, 158), (248, 212, 186))
HAIR = ((52, 26, 20), (86, 44, 33), (116, 62, 45), (152, 88, 62))
SCARF = ((108, 72, 22), (172, 124, 44), (208, 158, 66), (232, 194, 108))
DRESS = ((34, 56, 60), (58, 90, 92), (80, 122, 118), (112, 154, 146))
APRON = ((146, 130, 106), (210, 197, 172), (240, 232, 214), (252, 249, 240))
BOOTS = ((38, 24, 16), (62, 40, 28), (90, 60, 42), (120, 84, 58))
INK = (43, 29, 26)
MOUTH = (160, 82, 70)
LIP = (204, 126, 108)
BLUSH = (228, 160, 140)
FLOUR = (250, 247, 240)
IRIS = (104, 122, 74)
HAT = ((56, 26, 32), (94, 44, 52), (124, 60, 68), (156, 86, 92))
BAND = ((40, 24, 16), (66, 42, 28), (88, 58, 38), (110, 76, 52))
BELT = BAND
LINEN = ((150, 136, 112), (214, 203, 180), (236, 228, 210), (248, 244, 232))
WHEAT = (226, 186, 92)
WHEAT_D = (176, 136, 56)


def part(canvas, shapes, ramp, shade=(2, 0), shade_bottom=0, light_top=1):
    """Draw a shaded, outlined shape onto canvas. shapes(draw) fills a mask with 255."""
    w, h = canvas.size
    mask = Image.new("L", (w, h), 0)
    shapes(ImageDraw.Draw(mask))
    m = mask.load()
    inside = lambda x, y: 0 <= x < w and 0 <= y < h and m[x, y] > 0
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = layer.load()
    out, sh, base, li = ramp
    for y in range(h):
        for x in range(w):
            if not inside(x, y):
                continue
            if not all(inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                c = out
            elif shade[0] and not inside(x + shade[0], y):
                c = sh
            elif shade_bottom and not inside(x, y + shade_bottom):
                c = sh
            elif light_top and not inside(x, y - 1 - light_top):
                c = li
            else:
                c = base
            px[x, y] = c + (255,)
    canvas.alpha_composite(layer)


def put(img, pts, col):
    for x, y in pts:
        if 0 <= x < img.width and 0 <= y < img.height:
            img.putpixel((x, y), col + (255,))


# ---------------------------------------------------------------- 32x64 sprites
def hat_front(im, by, back=False):
    part(im, lambda d: d.rounded_rectangle((8, 0 + by, 23, 9 + by), 5, fill=255), HAT, shade=(3, 0))
    part(im, lambda d: d.rectangle((8, 6 + by, 23, 8 + by), fill=255), BAND, shade=(0, 0), light_top=0)
    part(im, lambda d: d.ellipse((3, 7 + by, 28, 12 + by), fill=255), HAT, shade=(3, 0), light_top=0)
    if not back:  # a wheat sprig tucked in the band
        put(im, [(22, 3 + by), (23, 2 + by), (24, 1 + by), (22, 5 + by), (23, 4 + by)], WHEAT)
        put(im, [(21, 5 + by), (24, 2 + by)], WHEAT_D)


def sprite_front(step=0, back=False, apron=False):
    im = Image.new("RGBA", (32, 64), (0, 0, 0, 0))
    by = 1 if step else 0          # body bob on step frames
    lb, rb = (step, -step)         # boot offsets
    part(im, lambda d: d.rounded_rectangle((9, 56 + lb, 15, 62 + max(lb, 0)), 2, fill=255), BOOTS, light_top=0)
    part(im, lambda d: d.rounded_rectangle((16, 56 + rb, 22, 62 + max(rb, 0)), 2, fill=255), BOOTS, light_top=0)
    part(im, lambda d: d.polygon([(9, 33 + by), (22, 33 + by), (25, 57 + by), (6, 57 + by)], fill=255), DRESS)
    put(im, [(12, y + by) for y in range(40, 55)] + [(19, y + by) for y in range(42, 55)], DRESS[1])  # skirt folds
    for side, (x0, x1) in (("l", (5, 9)), ("r", (22, 26))):
        sw = step if side == "l" else -step
        part(im, lambda d, x0=x0, x1=x1: d.rounded_rectangle((x0, 24 + by, x1, 33 + by), 2, fill=255), DRESS)
        part(im, lambda d, x0=x0, x1=x1: d.rectangle((x0 + 1, 32 + by, x1 - 1, 41 + by + sw), fill=255), SKIN, light_top=0)
        part(im, lambda d, x0=x0, x1=x1: d.ellipse((x0, 39 + by + sw, x1, 44 + by + sw), fill=255), SKIN, light_top=0)
    part(im, lambda d: d.rounded_rectangle((9, 22 + by, 22, 36 + by), 3, fill=255), DRESS)
    part(im, lambda d: d.rectangle((9, 33 + by, 22, 35 + by), fill=255), BELT, shade=(0, 0), light_top=0)
    if not back:
        put(im, [(15, 34 + by), (16, 34 + by)], (196, 168, 96))                      # buckle
        part(im, lambda d: d.polygon([(12, 22 + by), (19, 22 + by), (15, 27 + by)], fill=255), LINEN, shade=(0, 0), light_top=0)
        put(im, [(15, 28 + by), (15, 30 + by)], DRESS[0])                             # laces
    if apron and not back:
        part(im, lambda d: d.polygon([(10, 35 + by), (21, 35 + by), (23, 53 + by), (8, 53 + by)], fill=255), APRON, shade=(2, 0))
        part(im, lambda d: d.rectangle((11, 25 + by, 20, 35 + by), fill=255), APRON)
        part(im, lambda d: d.rectangle((12, 40 + by, 19, 45 + by), fill=255), APRON, shade=(0, 0), light_top=0)
        put(im, [(14, 48 + by), (17, 46 + by), (19, 50 + by), (13, 29 + by)], FLOUR)
    if apron and back:
        part(im, lambda d: d.rectangle((11, 23 + by, 12, 33 + by), fill=255), APRON, shade=(0, 0), light_top=0)
        part(im, lambda d: d.rectangle((19, 23 + by, 20, 33 + by), fill=255), APRON, shade=(0, 0), light_top=0)
        part(im, lambda d: d.polygon([(13, 34 + by), (18, 34 + by), (19, 41 + by), (16, 38 + by), (12, 41 + by)], fill=255), APRON, shade=(0, 0), light_top=0)
    part(im, lambda d: d.rectangle((13, 18 + by, 18, 23 + by), fill=255), SKIN, shade=(0, 0), light_top=0)
    put(im, [(x, 19 + by) for x in range(14, 18)] + [(x, 20 + by) for x in range(14, 18)], SKIN[1])
    if back:
        part(im, lambda d: d.ellipse((5, 3 + by, 26, 26 + by), fill=255), HAIR)
        put(im, [(x, y + by) for x in (11, 16, 21) for y in range(13, 22)], HAIR[1])
    else:  # bob: crown plus straight locks beside the face (none under the chin)
        part(im, lambda d: (d.ellipse((5, 3 + by, 26, 19 + by), fill=255), d.rectangle((5, 10 + by, 9, 21 + by), fill=255), d.rectangle((22, 10 + by, 26, 21 + by), fill=255)), HAIR)
        part(im, lambda d: d.ellipse((8, 5 + by, 23, 23 + by), fill=255), SKIN, shade=(3, 0), light_top=0)
        part(im, lambda d: d.polygon([(7, 9 + by), (24, 9 + by), (24, 12 + by), (21, 11 + by), (18, 13 + by), (15, 11 + by), (12, 13 + by), (9, 11 + by), (7, 14 + by)], fill=255), HAIR, light_top=0)
        y = 13 + by
        for ex in (11, 19):
            put(im, [(ex, y), (ex + 1, y), (ex, y + 1), (ex + 1, y + 1), (ex, y + 2), (ex + 1, y + 2)], INK)
            put(im, [(ex, y)], (255, 255, 255))
            put(im, [(ex - 1, y - 1), (ex + 2, y - 1)], INK)  # heavy upper lid
        put(im, [(16, 16 + by), (16, 17 + by)], SKIN[1])
        put(im, [(14, 19 + by), (15, 19 + by), (16, 19 + by), (17, 19 + by)], MOUTH)
        put(im, [(10, 17 + by), (11, 17 + by), (20, 17 + by), (21, 17 + by)], BLUSH)
        if apron:
            put(im, [(9, 18 + by), (10, 19 + by)], FLOUR)
    hat_front(im, by, back)
    put(im, [(x, 12 + by) for x in range(9, 23)] if not back else [], SKIN[1])  # shadow under the brim
    return im


def sprite_side(step=0, apron=False):
    """Facing right."""
    im = Image.new("RGBA", (32, 64), (0, 0, 0, 0))
    by = 1 if step else 0
    fx = {0: (0, 0), 1: (-3, 3), -1: (1, -1)}[step]
    part(im, lambda d: d.rounded_rectangle((11 + fx[0], 56, 17 + fx[0], 62), 2, fill=255), BOOTS, light_top=0)
    part(im, lambda d: d.rounded_rectangle((15 + fx[1], 56, 22 + fx[1], 62), 2, fill=255), BOOTS, light_top=0)
    part(im, lambda d: d.polygon([(10, 33 + by), (21, 33 + by), (24, 57 + by), (8, 57 + by)], fill=255), DRESS)
    put(im, [(15, y + by) for y in range(41, 55)], DRESS[1])
    part(im, lambda d: d.rounded_rectangle((10, 22 + by, 21, 36 + by), 3, fill=255), DRESS)
    part(im, lambda d: d.rectangle((10, 33 + by, 21, 35 + by), fill=255), BELT, shade=(0, 0), light_top=0)
    if apron:
        part(im, lambda d: d.polygon([(19, 35 + by), (22, 35 + by), (25, 53 + by), (20, 53 + by)], fill=255), APRON, shade=(0, 0))
        part(im, lambda d: d.rectangle((19, 24 + by, 21, 35 + by), fill=255), APRON, shade=(0, 0))
    sw = {0: 0, 1: 2, -1: -2}[step]
    part(im, lambda d: d.rounded_rectangle((12, 24 + by, 17, 33 + by), 2, fill=255), DRESS)
    part(im, lambda d: d.rectangle((13 + sw // 2, 32 + by, 16 + sw // 2, 41 + by), fill=255), SKIN, light_top=0)
    part(im, lambda d: d.ellipse((12 + sw, 39 + by, 17 + sw, 44 + by), fill=255), SKIN, light_top=0)
    part(im, lambda d: d.rectangle((14, 18 + by, 18, 23 + by), fill=255), SKIN, shade=(0, 0), light_top=0)
    part(im, lambda d: d.ellipse((6, 3 + by, 23, 25 + by), fill=255), HAIR)
    part(im, lambda d: (d.ellipse((10, 5 + by, 24, 23 + by), fill=255), d.rectangle((23, 13 + by, 25, 15 + by), fill=255)), SKIN, shade=(0, 0), light_top=0)
    part(im, lambda d: d.polygon([(9, 9 + by), (24, 9 + by), (24, 11 + by), (21, 12 + by), (18, 10 + by), (15, 12 + by), (12, 11 + by), (12, 18 + by), (9, 16 + by)], fill=255), HAIR, light_top=0)
    put(im, [(14, 13 + by), (14, 14 + by), (15, 15 + by)], SKIN[1])  # ear hint
    put(im, [(20, 13 + by), (21, 13 + by), (20, 14 + by), (21, 14 + by), (20, 15 + by), (21, 15 + by)], INK)
    put(im, [(21, 13 + by)], (255, 255, 255))
    put(im, [(19, 12 + by), (22, 12 + by)], INK)
    put(im, [(21, 19 + by), (22, 19 + by)], MOUTH)
    put(im, [(18, 17 + by), (19, 17 + by)], BLUSH)
    part(im, lambda d: d.rounded_rectangle((8, 0 + by, 22, 9 + by), 5, fill=255), HAT, shade=(3, 0))
    part(im, lambda d: d.rectangle((8, 6 + by, 22, 8 + by), fill=255), BAND, shade=(0, 0), light_top=0)
    part(im, lambda d: d.ellipse((4, 7 + by, 28, 11 + by), fill=255), HAT, shade=(3, 0), light_top=0)
    put(im, [(9, 3 + by), (8, 2 + by), (7, 1 + by), (9, 5 + by)], WHEAT)
    put(im, [(x, 12 + by) for x in range(17, 24)], SKIN[1])
    return im


# ---------------------------------------------------------------- 128x128 portrait
def portrait(expr, apron=False):
    im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    part(im, lambda d: d.ellipse((8, 100, 120, 176), fill=255), DRESS, shade=(5, 0))
    part(im, lambda d: d.polygon([(46, 100), (82, 100), (64, 122)], fill=255), LINEN, shade=(0, 0), light_top=0)
    part(im, lambda d: d.polygon([(52, 100), (76, 100), (64, 114)], fill=255), SKIN, shade=(0, 0), light_top=0)
    d = ImageDraw.Draw(im)
    for i in range(3):  # laces on the bodice
        d.line([(60, 118 + i * 3), (68, 120 + i * 3)], fill=BAND[1] + (255,))
    if apron:
        for x0 in (36, 80):
            part(im, lambda d, x0=x0: d.rectangle((x0, 104, x0 + 11, 127), fill=255), APRON, shade=(3, 0))
        put(im, [(40, 110), (43, 113), (41, 117), (86, 108), (89, 112)], FLOUR)
    part(im, lambda d: d.rectangle((50, 76, 77, 104), fill=255), SKIN, shade=(5, 0), light_top=0)
    put(im, [(x, y) for x in range(51, 77) for y in range(80, 86)], SKIN[1])
    part(im, lambda d: (d.ellipse((24, 18, 104, 98), fill=255), d.rectangle((24, 58, 36, 94), fill=255), d.rectangle((92, 58, 104, 90), fill=255)), HAIR, shade=(4, 0))
    part(im, lambda d: d.ellipse((31, 54, 41, 70), fill=255), SKIN, shade=(0, 0), light_top=0)
    part(im, lambda d: d.ellipse((87, 54, 97, 70), fill=255), SKIN, shade=(0, 0), light_top=0)
    part(im, lambda d: d.ellipse((35, 24, 93, 96), fill=255), SKIN, shade=(6, 0), light_top=0)
    part(im, lambda d: d.polygon([(33, 36), (95, 36), (95, 46), (88, 43), (82, 50), (76, 42), (68, 47), (60, 41), (52, 48), (46, 42), (40, 50), (33, 56)], fill=255), HAIR, shade=(3, 0), light_top=0)
    d = ImageDraw.Draw(im)
    for a, b in (((50, 40), (46, 42)), ((62, 40), (60, 41)), ((74, 40), (76, 42)), ((86, 40), (88, 43))):
        d.line([a, b], fill=HAIR[1] + (255,))
    for cx in (52, 76):
        part(im, lambda d, cx=cx: d.ellipse((cx - 7, 56, cx + 7, 64), fill=255), ((120, 96, 90), (226, 220, 212), (246, 242, 236), (246, 242, 236)), shade=(0, 0), light_top=0)
        d.ellipse((cx - 3, 56, cx + 3, 64), fill=IRIS + (255,))
        d.rectangle((cx - 1, 58, cx + 1, 62), fill=INK + (255,))
        d.rectangle((cx - 2, 57, cx - 1, 58), fill=(255, 255, 255, 255))
        d.line([(cx - 8, 55), (cx + 8, 55)], fill=INK + (255,), width=2)
        put(im, [(cx + 8, 54), (cx + 9, 53)] if cx > 64 else [(cx - 8, 54), (cx - 9, 53)], INK)
        d.line([(cx - 5, 66), (cx + 5, 66)], fill=SKIN[1] + (255,))
    bc = HAIR[1] + (255,)
    if expr == "neutral":
        d.line([(43, 50), (59, 50)], fill=bc, width=2); d.line([(69, 50), (85, 50)], fill=bc, width=2)
    elif expr == "stern":
        d.line([(43, 48), (59, 52)], fill=bc, width=3); d.line([(69, 52), (85, 48)], fill=bc, width=3)
    else:
        d.line([(43, 50), (59, 48)], fill=bc, width=2); d.line([(69, 48), (85, 50)], fill=bc, width=2)
    d.line([(66, 60), (67, 72)], fill=SKIN[1] + (255,))
    put(im, [(61, 74), (62, 75), (67, 75), (68, 74), (64, 76), (65, 76)], SKIN[1])
    put(im, [(63, 66), (63, 67), (63, 68)], SKIN[3])
    d.ellipse((40, 70, 52, 76), fill=BLUSH + (255,)); d.ellipse((76, 70, 88, 76), fill=BLUSH + (255,))
    put(im, [(58, 69), (61, 71), (69, 70), (72, 68), (56, 72)], SKIN[1])
    if apron:
        put(im, [(42, 78), (44, 77), (43, 80), (46, 79), (45, 81), (41, 81)], FLOUR)
    if expr == "neutral":
        d.line([(57, 84), (71, 84)], fill=MOUTH + (255,)); d.line([(59, 85), (69, 85)], fill=LIP + (255,))
    elif expr == "stern":
        d.line([(58, 84), (70, 84)], fill=MOUTH + (255,)); put(im, [(57, 85), (56, 86), (71, 85), (72, 86)], MOUTH)
        d.line([(60, 86), (68, 86)], fill=LIP + (255,))
    else:
        d.line([(59, 85), (69, 85)], fill=MOUTH + (255,)); put(im, [(58, 84), (57, 83), (70, 84), (71, 83)], MOUTH)
        d.line([(61, 86), (67, 86)], fill=LIP + (255,))
    # felt hat: rounded crown, band with a wheat sprig, wide soft brim
    part(im, lambda d: d.rounded_rectangle((36, 2, 92, 38), 18, fill=255), HAT, shade=(5, 0), light_top=2)
    d = ImageDraw.Draw(im)
    d.line([(52, 6), (50, 26)], fill=HAT[1] + (255,)); d.line([(64, 4), (64, 24)], fill=HAT[1] + (255,))
    part(im, lambda d: d.rectangle((36, 26, 92, 33), fill=255), BAND, shade=(0, 0), light_top=1)
    for i in range(5):  # wheat sprig
        put(im, [(84 + i, 22 - i * 3), (85 + i, 23 - i * 3), (86 + i, 21 - i * 3)], WHEAT)
        put(im, [(83 + i, 24 - i * 3)], WHEAT_D)
    d.line([(82, 30), (88, 12)], fill=WHEAT_D + (255,))
    part(im, lambda d: d.ellipse((16, 28, 112, 46), fill=255), HAT, shade=(5, 0), light_top=1)
    put(im, [(x, 47) for x in range(36, 92)] + [(x, 48) for x in range(40, 88)], SKIN[1])  # brim shadow
    bg = Image.new("RGBA", (128, 128), (233, 216, 180, 255))
    ImageDraw.Draw(bg).rectangle((0, 0, 127, 127), outline=(185, 160, 120))
    bg.alpha_composite(im)
    return bg


def walk_frames(apron):
    fr = {
        "down": [sprite_front(0, apron=apron), sprite_front(1, apron=apron), sprite_front(-1, apron=apron)],
        "up": [sprite_front(0, True, apron), sprite_front(-1, True, apron), sprite_front(1, True, apron)],
        "right": [sprite_side(0, apron), sprite_side(1, apron), sprite_side(-1, apron)],
    }
    fr["left"] = [im.transpose(Image.FLIP_LEFT_RIGHT) for im in fr["right"]]
    return fr


ORDER = ["down", "left", "right", "up"]


def save_sheets(fr, ports, tag):
    sheet = Image.new("RGBA", (32 * 3, 64 * 4), (0, 0, 0, 0))
    for r, name in enumerate(ORDER):
        for c, im in enumerate(fr[name]):
            sheet.paste(im, (c * 32, r * 64))
    sheet.save(OUT / f"mira_hd_{tag}_walk_32x64.png")
    ps = Image.new("RGBA", (128 * len(ports), 128))
    for i, p in enumerate(ports):
        ps.paste(p, (i * 128, 0))
    ps.save(OUT / f"mira_hd_{tag}_portraits_128.png")
    gif = []
    for name in ORDER:
        a, b, c = fr[name]
        for im in (a, b, a, c):
            f = Image.new("RGBA", (32, 64), (243, 234, 214, 255))
            f.alpha_composite(im)
            gif.append(f.resize((32 * 5, 64 * 5), Image.NEAREST).convert("P"))
    gif[0].save(OUT / f"mira_hd_{tag}_walk.gif", save_all=True, append_images=gif[1:], duration=160, loop=0)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in ("mira_hd_walk_32x64.png", "mira_hd_portraits_128.png", "mira_hd_walk.gif"):
        (OUT / old).unlink(missing_ok=True)
    exprs = ["neutral", "stern", "soft"]
    every = walk_frames(False)
    baker = walk_frames(True)
    every_p = [portrait(e) for e in exprs]
    baker_p = [portrait(e, apron=True) for e in exprs]
    save_sheets(every, every_p, "everyday")
    save_sheets(baker, baker_p, "baker")

    serif_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 22)
    serif = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 15)
    ink, sub = (58, 42, 26), (90, 74, 58)
    pv = Image.new("RGBA", (1620, 760), (243, 234, 214, 255))
    d = ImageDraw.Draw(pv)
    d.text((30, 20), "Mira Wainwright: felt hat, everyday and baker outfits", font=serif_b, fill=ink)
    d.text((30, 52), "Everyday outfit: 32x64 walk cycle (idle, step, step) in 4 directions · shown at 4x", font=serif, fill=sub)
    x = 30
    for name in ORDER:
        d.text((x, 85), name, font=serif, fill=sub)
        for c, im in enumerate(every[name]):
            pv.alpha_composite(im.resize((128, 256), Image.NEAREST), (x + c * 128, 110))
        x += 3 * 128 + 10
    y0 = 400
    d.text((30, y0), "Everyday portraits (128x128, shown at 2x)", font=serif, fill=sub)
    for i, (p, e) in enumerate(zip(every_p, exprs)):
        pv.alpha_composite(p.resize((256, 256), Image.NEAREST), (30 + i * 270, y0 + 28))
        d.text((30 + i * 270, y0 + 292), e, font=serif, fill=sub)
    bx = 860
    d.text((bx, y0), "Baker outfit: the apron goes on when she agrees to bake again", font=serif, fill=sub)
    for c, name in enumerate(["down", "right", "up"]):
        pv.alpha_composite(baker[name][0].resize((128, 256), Image.NEAREST), (bx + c * 128, y0 + 28))
    pv.alpha_composite(baker_p[2].resize((256, 256), Image.NEAREST), (bx + 400, y0 + 28))
    d.text((bx + 400, y0 + 292), "soft, with flour", font=serif, fill=sub)
    pv.save(OUT / "mira_hd_preview.png")


if __name__ == "__main__":
    main()

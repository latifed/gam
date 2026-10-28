"""Concept art for Pip Wainwright (7): 32x64 walk sprites and 128x128 portraits.

Light brown hair from Mira, green eyes from Edric. Rust tunic, suspenders, knee breeches.
Run: python3 tools/concept_art/pip.py   (writes to docs/concept-art/pip/)
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mira_hd import part, put, SKIN, HAIR, BOOTS, INK, MOUTH, BLUSH, BAND, LINEN, sprite_front as mira_front  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "docs" / "concept-art" / "pip"

TUNIC = ((96, 40, 28), (150, 70, 48), (184, 96, 64), (212, 130, 92))
BREECHES = ((48, 34, 24), (78, 56, 40), (104, 76, 54), (130, 100, 72))
SOCKS = ((120, 112, 100), (178, 170, 156), (206, 198, 184), (226, 220, 208))
GREEN = (84, 150, 80)
GREEN_D = (52, 104, 56)
DIRT = (150, 112, 80)
MOUTH_D = (112, 48, 46)


# ---------------------------------------------------------------- 32x64 sprites
def sprite_front(step=0, back=False):
    im = Image.new("RGBA", (32, 64), (0, 0, 0, 0))
    by = 1 if step else 0
    lb, rb = step, -step
    part(im, lambda d: d.rounded_rectangle((10, 57 + lb, 15, 62 + max(lb, 0)), 2, fill=255), BOOTS, light_top=0)
    part(im, lambda d: d.rounded_rectangle((16, 57 + rb, 21, 62 + max(rb, 0)), 2, fill=255), BOOTS, light_top=0)
    part(im, lambda d: d.rectangle((11, 50 + by, 14, 57 + lb), fill=255), SOCKS, shade=(0, 0), light_top=0)
    part(im, lambda d: d.rectangle((17, 50 + by, 20, 57 + rb), fill=255), SOCKS, shade=(0, 0), light_top=0)
    part(im, lambda d: (d.rectangle((10, 43 + by, 15, 51 + by), fill=255), d.rectangle((16, 43 + by, 21, 51 + by), fill=255),
                        d.rectangle((10, 43 + by, 21, 47 + by), fill=255)), BREECHES)
    for side, (x0, x1) in (("l", (5, 8)), ("r", (23, 26))):
        sw = step if side == "l" else -step
        part(im, lambda d, x0=x0, x1=x1: d.rounded_rectangle((x0, 33 + by, x1, 41 + by + sw), 2, fill=255), TUNIC)
        part(im, lambda d, x0=x0, x1=x1, sw=sw: d.ellipse((x0, 40 + by + sw, x1, 44 + by + sw), fill=255), SKIN, light_top=0)
    part(im, lambda d: d.polygon([(9, 32 + by), (22, 32 + by), (23, 46 + by), (8, 46 + by)], fill=255), TUNIC)
    if back:
        dr = ImageDraw.Draw(im)
        dr.line([(11, 33 + by), (20, 43 + by)], fill=BAND[1] + (255,), width=2)
        dr.line([(20, 33 + by), (11, 43 + by)], fill=BAND[1] + (255,), width=2)
    else:
        part(im, lambda d: d.rectangle((11, 32 + by, 12, 44 + by), fill=255), BAND, shade=(0, 0), light_top=0)
        part(im, lambda d: d.rectangle((19, 32 + by, 20, 44 + by), fill=255), BAND, shade=(0, 0), light_top=0)
        part(im, lambda d: d.polygon([(13, 32 + by), (18, 32 + by), (15, 36 + by)], fill=255), LINEN, shade=(0, 0), light_top=0)
        put(im, [(18, 40 + by), (17, 41 + by)], TUNIC[0])  # a mended tear
    part(im, lambda d: d.rectangle((13, 29 + by, 18, 33 + by), fill=255), SKIN, shade=(0, 0), light_top=0)
    if back:
        part(im, lambda d: (d.ellipse((7, 13 + by, 24, 30 + by), fill=255), d.polygon([(14, 14 + by), (16, 9 + by), (18, 14 + by)], fill=255),
                            d.polygon([(9, 27 + by), (11, 32 + by), (13, 29 + by), (16, 32 + by), (18, 29 + by), (20, 32 + by), (22, 27 + by)], fill=255)), HAIR)
        dr = ImageDraw.Draw(im)
        for a, b in (((11, 16), (10, 26)), ((15, 14), (14, 28)), ((19, 15), (20, 26))):
            dr.line([(a[0], a[1] + by), (b[0], b[1] + by)], fill=HAIR[1] + (255,))
        put(im, [(13, 15 + by), (18, 16 + by)], HAIR[3])
        return im
    part(im, lambda d: d.ellipse((7, 14 + by, 24, 26 + by), fill=255), HAIR)
    part(im, lambda d: d.ellipse((6, 21 + by, 9, 27 + by), fill=255), SKIN, shade=(0, 0), light_top=0)    # ears
    part(im, lambda d: d.ellipse((22, 21 + by, 25, 27 + by), fill=255), SKIN, shade=(0, 0), light_top=0)
    part(im, lambda d: d.ellipse((8, 15 + by, 23, 32 + by), fill=255), SKIN, shade=(3, 0), light_top=0)
    # messy hair with a cowlick
    part(im, lambda d: d.polygon([(7, 24 + by), (7, 18 + by), (10, 14 + by), (14, 13 + by), (15, 9 + by), (17, 13 + by), (21, 14 + by), (24, 18 + by),
                                  (24, 23 + by), (22, 20 + by), (20, 22 + by), (18, 19 + by), (16, 21 + by), (14, 19 + by), (12, 22 + by), (10, 19 + by), (9, 24 + by)], fill=255),
         HAIR, shade=(2, 0))
    put(im, [(11, 16 + by), (13, 15 + by), (19, 16 + by), (15, 11 + by)], HAIR[3])
    y = 23 + by
    for ex in (11, 19):  # big green eyes
        put(im, [(ex, y), (ex + 1, y)], INK)
        put(im, [(ex, y + 1), (ex, y + 2), (ex + 1, y + 2)], GREEN_D)
        put(im, [(ex + 1, y + 1)], (255, 255, 255))
    put(im, [(10, 27 + by), (11, 27 + by), (20, 27 + by), (21, 27 + by)], BLUSH)
    put(im, [(13, 26 + by), (18, 26 + by), (14, 27 + by), (17, 27 + by)], SKIN[1])        # freckles
    put(im, [(14, 29 + by), (17, 29 + by)], MOUTH); put(im, [(15, 30 + by), (16, 30 + by)], MOUTH)  # grin
    return im


def sprite_side(step=0):
    """Facing right."""
    im = Image.new("RGBA", (32, 64), (0, 0, 0, 0))
    by = 1 if step else 0
    fx = {0: (0, 0), 1: (-3, 3), -1: (1, -1)}[step]
    part(im, lambda d: d.rounded_rectangle((11 + fx[0], 57, 17 + fx[0], 62), 2, fill=255), BOOTS, light_top=0)
    part(im, lambda d: d.rounded_rectangle((15 + fx[1], 57, 22 + fx[1], 62), 2, fill=255), BOOTS, light_top=0)
    part(im, lambda d: d.rectangle((12 + fx[0], 50 + by, 15 + fx[0], 57), fill=255), SOCKS, shade=(0, 0), light_top=0)
    part(im, lambda d: d.rectangle((16 + fx[1], 50 + by, 19 + fx[1], 57), fill=255), SOCKS, shade=(0, 0), light_top=0)
    part(im, lambda d: d.rectangle((11, 43 + by, 20, 51 + by), fill=255), BREECHES)
    part(im, lambda d: d.polygon([(10, 32 + by), (21, 32 + by), (22, 46 + by), (9, 46 + by)], fill=255), TUNIC)
    part(im, lambda d: d.rectangle((18, 32 + by, 19, 44 + by), fill=255), BAND, shade=(0, 0), light_top=0)
    sw = {0: 0, 1: 2, -1: -2}[step]
    part(im, lambda d: d.rounded_rectangle((13 + sw // 2, 33 + by, 17 + sw // 2, 41 + by), 2, fill=255), TUNIC)
    part(im, lambda d: d.ellipse((13 + sw, 40 + by, 17 + sw, 44 + by), fill=255), SKIN, light_top=0)
    part(im, lambda d: d.rectangle((14, 29 + by, 18, 33 + by), fill=255), SKIN, shade=(0, 0), light_top=0)
    part(im, lambda d: d.ellipse((7, 13 + by, 22, 29 + by), fill=255), HAIR)
    part(im, lambda d: (d.ellipse((9, 15 + by, 23, 32 + by), fill=255), d.rectangle((23, 24 + by, 24, 26 + by), fill=255)), SKIN, shade=(0, 0), light_top=0)
    part(im, lambda d: d.polygon([(7, 26 + by), (6, 18 + by), (9, 14 + by), (13, 13 + by), (13, 9 + by), (16, 13 + by), (21, 14 + by), (24, 18 + by),
                                  (24, 20 + by), (21, 19 + by), (19, 21 + by), (17, 19 + by), (15, 23 + by), (14, 27 + by), (10, 28 + by)], fill=255), HAIR, shade=(0, 0))
    put(im, [(15, 23 + by), (15, 24 + by), (16, 24 + by), (15, 25 + by)], SKIN[1])  # ear
    put(im, [(10, 17 + by), (13, 15 + by), (18, 16 + by)], HAIR[3])
    put(im, [(20, 23 + by), (21, 23 + by)], INK); put(im, [(20, 24 + by), (20, 25 + by), (21, 25 + by)], GREEN_D); put(im, [(21, 24 + by)], (255, 255, 255))
    put(im, [(19, 27 + by), (20, 27 + by)], BLUSH); put(im, [(22, 26 + by)], SKIN[1])
    put(im, [(21, 29 + by), (22, 29 + by)], MOUTH)
    return im


# ---------------------------------------------------------------- 128x128 portrait
def portrait(expr):
    im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    part(im, lambda d: d.ellipse((14, 102, 114, 172), fill=255), TUNIC, shade=(5, 0))
    for x0 in (36, 84):
        part(im, lambda d, x0=x0: d.rectangle((x0, 106, x0 + 8, 127), fill=255), BAND, shade=(0, 0), light_top=0)
    part(im, lambda d: d.polygon([(54, 102), (74, 102), (64, 114)], fill=255), LINEN, shade=(0, 0), light_top=0)
    part(im, lambda d: d.rectangle((52, 84, 76, 106), fill=255), SKIN, shade=(5, 0), light_top=0)
    put(im, [(x, y) for x in range(53, 76) for y in range(88, 93)], SKIN[1])
    part(im, lambda d: d.ellipse((28, 14, 100, 70), fill=255), HAIR, shade=(4, 0))
    part(im, lambda d: d.ellipse((25, 54, 39, 76), fill=255), SKIN, shade=(0, 0), light_top=0)   # ears that stick out a bit
    part(im, lambda d: d.ellipse((89, 54, 103, 76), fill=255), SKIN, shade=(0, 0), light_top=0)
    put(im, [(30, 62), (31, 64), (31, 66), (97, 62), (96, 64), (96, 66)], SKIN[1])
    part(im, lambda d: d.ellipse((32, 28, 96, 100), fill=255), SKIN, shade=(6, 0), light_top=0)
    # messy hair with tufts and a cowlick
    part(im, lambda d: d.polygon([(30, 62), (28, 44), (32, 30), (40, 21), (50, 16), (56, 6), (62, 15), (70, 4), (74, 14), (84, 17), (94, 26), (100, 40), (100, 60),
                                  (95, 60), (93, 48), (88, 46), (84, 53), (78, 44), (72, 51), (66, 42), (60, 49), (54, 43), (48, 51), (42, 45), (37, 54), (35, 62)], fill=255),
         HAIR, shade=(4, 0), light_top=1)
    d = ImageDraw.Draw(im)
    for a, b in (((56, 14), (50, 30)), ((70, 12), (68, 30)), ((46, 24), (42, 40)), ((82, 22), (86, 40)), ((62, 22), (60, 40))):
        d.line([a, b], fill=HAIR[1] + (255,))
    for a, b in (((52, 18), (46, 28)), ((74, 18), (80, 28)), ((60, 10), (58, 18))):
        d.line([a, b], fill=HAIR[3] + (255,))
    # big green eyes, two sparkles each
    for cx in (50, 78):
        part(im, lambda d, cx=cx: d.ellipse((cx - 8, 58, cx + 8, 71), fill=255), ((120, 96, 90), (226, 220, 212), (248, 245, 240), (248, 245, 240)), shade=(0, 0), light_top=0)
        d.ellipse((cx - 5, 58, cx + 5, 71), fill=GREEN + (255,))
        d.ellipse((cx - 5, 58, cx + 5, 62), fill=GREEN_D + (255,))
        d.rectangle((cx - 2, 61, cx + 1, 67), fill=INK + (255,))
        d.rectangle((cx - 3, 60, cx - 1, 62), fill=(255, 255, 255, 255))
        put(im, [(cx + 2, 67), (cx + 3, 67)], (255, 255, 255))
        d.line([(cx - 8, 57), (cx + 8, 57)], fill=INK + (255,))
    bc = HAIR[1] + (255,)
    if expr == "happy":
        d.line([(41, 51), (46, 49), (57, 50)], fill=bc, width=2); d.line([(71, 50), (82, 49), (87, 51)], fill=bc, width=2)
    elif expr == "curious":
        d.line([(41, 50), (57, 50)], fill=bc, width=2); d.line([(71, 48), (80, 45), (87, 47)], fill=bc, width=2)
    else:  # worried
        d.line([(41, 52), (57, 48)], fill=bc, width=2); d.line([(71, 48), (87, 52)], fill=bc, width=2)
    # button nose, freckles, rosy cheeks, a smudge of dirt
    put(im, [(66, 77), (67, 78), (63, 79), (64, 80), (65, 80), (66, 79)], SKIN[1]); put(im, [(63, 76)], SKIN[3])
    d.ellipse((35, 76, 48, 83), fill=BLUSH + (255,)); d.ellipse((80, 76, 93, 83), fill=BLUSH + (255,))
    put(im, [(55, 74), (58, 76), (61, 73), (70, 74), (73, 76), (68, 72), (44, 74), (84, 74), (52, 77), (76, 77)], SKIN[1])
    put(im, [(86, 87), (88, 86), (87, 89), (89, 88)], DIRT)
    if expr == "happy":   # big grin with a missing tooth
        d.chord((54, 82, 74, 96), 0, 180, fill=MOUTH_D + (255,))
        d.rectangle((57, 89, 71, 90), fill=(250, 248, 242, 255))
        put(im, [(64, 89), (65, 89), (64, 90), (65, 90)], MOUTH_D)
        d.arc((54, 82, 74, 96), 0, 180, fill=MOUTH + (255,))
        d.line([(54, 89), (74, 89)], fill=MOUTH + (255,))
    elif expr == "curious":
        d.ellipse((60, 87, 68, 95), fill=MOUTH_D + (255,)); d.ellipse((60, 87, 68, 95), outline=MOUTH + (255,))
    else:
        d.line([(58, 91), (61, 89), (64, 90), (67, 89), (70, 91)], fill=MOUTH + (255,))
    bg = Image.new("RGBA", (128, 128), (233, 216, 180, 255))
    ImageDraw.Draw(bg).rectangle((0, 0, 127, 127), outline=(185, 160, 120))
    bg.alpha_composite(im)
    return bg


ORDER = ["down", "left", "right", "up"]
EXPRS = ["happy", "curious", "worried"]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fr = {
        "down": [sprite_front(s) for s in (0, 1, -1)],
        "up": [sprite_front(s, True) for s in (0, -1, 1)],
        "right": [sprite_side(s) for s in (0, 1, -1)],
    }
    fr["left"] = [im.transpose(Image.FLIP_LEFT_RIGHT) for im in fr["right"]]
    sheet = Image.new("RGBA", (32 * 3, 64 * 4), (0, 0, 0, 0))
    for r, name in enumerate(ORDER):
        for c, im in enumerate(fr[name]):
            sheet.paste(im, (c * 32, r * 64))
    sheet.save(OUT / "pip_walk_32x64.png")
    ports = [portrait(e) for e in EXPRS]
    ps = Image.new("RGBA", (128 * 3, 128))
    for i, p in enumerate(ports):
        ps.paste(p, (i * 128, 0))
    ps.save(OUT / "pip_portraits_128.png")
    gif = []
    for name in ORDER:
        a, b, c = fr[name]
        for im in (a, b, a, c):
            f = Image.new("RGBA", (32, 64), (243, 234, 214, 255))
            f.alpha_composite(im)
            gif.append(f.resize((160, 320), Image.NEAREST).convert("P"))
    gif[0].save(OUT / "pip_walk.gif", save_all=True, append_images=gif[1:], duration=150, loop=0)

    serif_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 22)
    serif = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 15)
    ink, sub = (58, 42, 26), (90, 74, 58)
    pv = Image.new("RGBA", (1560, 680), (243, 234, 214, 255))
    d = ImageDraw.Draw(pv)
    d.text((30, 20), "Pip Wainwright (7): light brown hair from Mira, green eyes from Edric", font=serif_b, fill=ink)
    d.text((30, 52), "32x64 walk cycle (idle, step, step) in 4 directions · shown at 3x", font=serif, fill=sub)
    x = 30
    for name in ORDER:
        d.text((x, 85), name, font=serif, fill=sub)
        for c, im in enumerate(fr[name]):
            pv.alpha_composite(im.resize((96, 192), Image.NEAREST), (x + c * 98, 110))
        x += 3 * 98 + 20
    y0 = 330
    d.text((30, y0), "128x128 portraits · shown at 2x", font=serif, fill=sub)
    for i, (p, e) in enumerate(zip(ports, EXPRS)):
        pv.alpha_composite(p.resize((256, 256), Image.NEAREST), (30 + i * 276, y0 + 28))
        d.text((30 + i * 276, y0 + 292), e, font=serif, fill=sub)
    mx = 880
    d.text((mx, y0), "with his mother (same scale)", font=serif, fill=sub)
    pv.alpha_composite(mira_front(0, False, False, False).resize((128, 256), Image.NEAREST), (mx, y0 + 28))
    pv.alpha_composite(fr["down"][0].resize((128, 256), Image.NEAREST), (mx + 110, y0 + 28))
    pv.save(OUT / "pip_preview.png")


if __name__ == "__main__":
    main()

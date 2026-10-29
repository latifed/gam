"""The Gilded Tankard in three world states: Harvest Fair (before), Ruined (after the Shift), Reclaimed (the new normal).

Run: python3 tools/concept_art/world_states.py   (writes docs/concept-art/world/)
Concept quality. Shows how one building reads in each state, with townsfolk sprites for scale.
"""
import colorsys
import random
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import town  # noqa: E402
import roofs  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "docs" / "concept-art" / "world"
W, H = 256, 264
INK = (43, 29, 26)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def grade(im, sat=1.0, bright=1.0, tint=(1.0, 1.0, 1.0)):
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            r2, g2, b2 = colorsys.hls_to_rgb(h, min(1, l * bright), min(1, s * sat))
            px[x, y] = (int(min(255, r2 * 255 * tint[0])), int(min(255, g2 * 255 * tint[1])), int(min(255, b2 * 255 * tint[2])), a)


SHADOW = (34, 22, 46)


def veil(im, draw, color=SHADOW, alpha=90):
    """Draw translucent shapes (shadow or light) onto im. draw(d, rgba)."""
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw(ImageDraw.Draw(layer), color + (alpha,))
    im.alpha_composite(layer)


def band(im, x0, x1, y0, y1, a0, a1, color=SHADOW):
    """Vertical gradient band from alpha a0 at y0 to a1 at y1."""
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for i, y in enumerate(range(y0, y1)):
        t = i / max(1, y1 - y0 - 1)
        ld.line([(x0, y), (x1, y)], fill=color + (int(a0 + (a1 - a0) * t),))
    im.alpha_composite(layer)


def gothic_arch(x0, x1, y_spring, y_bottom):
    """Points for a pointed (lancet) arch opening: springs at y_spring, apex above it."""
    w = x1 - x0
    apex = y_spring - int(w * 0.62)
    pts = [(x0, y_bottom), (x0, y_spring)]
    for t in (0.18, 0.38, 0.6, 0.82):
        pts.append((x0 + int(w * 0.5 * t), y_spring - int((y_spring - apex) * (1 - (1 - t) ** 2))))
    pts.append(((x0 + x1) // 2, apex))
    for t in (0.82, 0.6, 0.38, 0.18):
        pts.append((x1 - int(w * 0.5 * t), y_spring - int((y_spring - apex) * (1 - (1 - t) ** 2))))
    pts += [(x1, y_spring), (x1, y_bottom)]
    return pts


def glass_pane(im, shape, glass, lead, frame):
    """Diamond-pane leaded glass inside any polygon (clipped to it)."""
    xs, ys = [p[0] for p in shape], [p[1] for p in shape]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    w, h = x1 - x0 + 1, y1 - y0 + 1
    pane = Image.new("RGBA", (w, h), glass + (255,))
    pd = ImageDraw.Draw(pane)
    for k in range(-h, w + h, 5):
        pd.line([(k, h), (k + h, 0)], fill=lead); pd.line([(k, 0), (k + h, h)], fill=lead)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon([(x - x0, y - y0) for x, y in shape], fill=255)
    im.paste(pane, (x0, y0), mask)
    ImageDraw.Draw(im).polygon(shape, outline=frame)


def scene(state):
    rnd = random.Random(7)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(im)
    ruined, before, after = state == "ruined", state == "before", state == "reclaimed"

    # ---------------- ground and cobbles
    grass = (108, 132, 84) if not ruined else (120, 112, 104)
    d.rectangle((0, 0, W, H), fill=grass)
    for _ in range(1000):
        x, y = rnd.randrange(W), rnd.randrange(H)
        c = shade(grass, rnd.choice([0.85, 0.92, 1.08]))
        if ruined and rnd.random() < 0.3:
            c = (96, 84, 76)
        if after and y > 236 and (x < 50 or x > 206) and rnd.random() < 0.5:
            c = rnd.choice([(150, 110, 170), (176, 136, 196)])                      # tamed purple border
        d.point((x, y), fill=c); d.point((x, y - 1), fill=c)
    cob = (168, 160, 148) if not ruined else (128, 122, 116)
    d.polygon([(96, 206), (160, 206), (182, H), (74, H)], fill=shade(cob, 0.7))
    for yy in range(208, H, 6):                                                    # irregular cobbles
        for xx in range(70 + (yy // 6 % 2) * 4, 190, 8):
            t = (yy - 206) / (H - 206)
            if 96 - 22 * t < xx < 158 + 22 * t:
                d.rounded_rectangle((xx, yy, xx + rnd.randrange(5, 8), yy + 4), 2, fill=shade(cob, rnd.choice([0.92, 1.0, 1.08])))

    # ---------------- palette: limewashed ochre plaster, dark oak, red clay tiles, rubble stone
    plaster = (214, 198, 164) if not ruined else (176, 164, 140)
    oak = (84, 56, 38) if not ruined else (62, 48, 40)
    stone = (152, 142, 128)
    roof = (146, 86, 66) if not ruined else (118, 64, 54)
    shutter = (94, 108, 96)

    # ground floor: rubble stone
    d.rectangle((48, 152, 208, 204), fill=stone, outline=INK)
    for y in range(154, 204, 6):
        x = 50 + (y // 6 % 2) * 5
        while x < 206:
            w = rnd.randrange(7, 14)
            d.rounded_rectangle((x, y, min(206, x + w), y + 4), 1, outline=shade(stone, 0.75), fill=shade(stone, rnd.choice([0.95, 1.0, 1.05])))
            x += w + 2
    # pointed-arch door with stone voussoirs and iron strap hinges
    d.polygon(gothic_arch(108, 148, 172, 204), fill=shade(stone, 1.15), outline=INK)
    door = gothic_arch(113, 143, 174, 204)
    if ruined:
        d.polygon(door, fill=(28, 22, 24), outline=INK)
        d.polygon([(143, 176), (158, 186), (158, 210), (143, 204)], fill=(100, 64, 40), outline=INK)
    else:
        d.polygon(door, fill=(118, 74, 42), outline=INK)
        for x in (120, 128, 136):
            d.line([(x, 166), (x, 203)], fill=(92, 58, 34))
        for y in (178, 194):
            d.line([(114, y), (138, y)], fill=(40, 36, 36), width=2); d.point((139, y - 1), fill=(40, 36, 36))
        d.ellipse((137, 186, 140, 189), fill=(60, 56, 56))
    d.rectangle((100, 204, 156, 210), fill=shade(stone, 1.08), outline=INK)
    # pointed ground-floor windows with painted shutters
    for x0 in (62, 166):
        arch = gothic_arch(x0, x0 + 26, 176, 196)
        d.polygon(gothic_arch(x0 - 3, x0 + 29, 176, 198), fill=shade(stone, 1.15), outline=INK)
        if ruined:
            d.polygon(arch, fill=(36, 30, 34), outline=INK)
            d.polygon([(x0 + 2, 186), (x0 + 9, 186), (x0 + 4, 194)], fill=(150, 170, 180))
            d.polygon([(x0 - 12, 178), (x0 - 2, 182), (x0 - 4, 204), (x0 - 14, 200)], fill=shade(shutter, 0.7), outline=INK)  # shutter fallen
        else:
            glass_pane(im, arch, (232, 198, 132), (150, 110, 60), INK)
            sh = shutter if not (after and x0 == 62) else (196, 160, 110)        # one fresh, unpainted shutter
            d.rectangle((x0 - 12, 170, x0 - 3, 198), fill=sh, outline=INK); d.rectangle((x0 + 29, 170, x0 + 38, 198), fill=shutter, outline=INK)
            for xx in (x0 - 9, x0 + 32):
                d.line([(xx, 174), (xx, 194)], fill=shade(sh, 0.8))
    # ivy up the left corner
    ivy = (70, 130, 60) if not ruined else (110, 90, 60)
    for _ in range(70):
        x, y = rnd.randrange(44, 62), rnd.randrange(130, 204)
        d.rectangle((x, y, x + 2, y + 1), fill=rnd.choice([ivy, shade(ivy, 0.8)]))
    if after:
        for _ in range(6):
            x, y = rnd.randrange(46, 60), rnd.randrange(140, 200)
            d.point((x, y), fill=(190, 150, 240))

    # jettied upper floor: overhangs the stone ground floor
    d.rectangle((38, 100, 218, 150), fill=plaster, outline=INK)
    d.rectangle((38, 148, 218, 153), fill=oak, outline=INK)                       # jetty beam
    for bx in (48, 92, 164, 208):
        sag = 3 if ruined and bx == 208 else 0
        d.polygon([(bx - 3, 153), (bx + 3, 153), (bx, 160 + sag)], fill=oak, outline=INK)   # brackets
    d.rectangle((40, 154, 216, 156), fill=(60, 44, 34))                            # shadow under the jetty
    for x in (38, 74, 104, 152, 182, 218):                                         # posts
        d.rectangle((x - 2, 100, x + 2, 150), fill=oak)
    d.rectangle((38, 99, 218, 102), fill=oak)
    for (x0, x1) in ((104, 152),):                                                 # St Andrew's cross panel
        d.line([(x0 + 2, 102), (x1 - 2, 148)], fill=oak, width=3); d.line([(x1 - 2, 102), (x0 + 2, 148)], fill=oak, width=3)
    d.line([(76, 146), (102, 104)], fill=oak, width=3); d.line([(154, 104), (180, 146)], fill=oak, width=3)   # braces
    # leaded casement windows, flower boxes
    for x0 in (46, 186):
        box = (x0, 112, x0 + 24, 134)
        if ruined:
            d.rectangle(box, fill=(36, 30, 34), outline=INK)
            if x0 == 186:
                for i, dy in enumerate((4, 11, 17)):
                    d.line([(x0 - 3, 112 + dy + i), (x0 + 27, 112 + dy - 3 + i)], fill=(140, 100, 64), width=4)
        else:
            glass_pane(im, [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])], (232, 198, 132), (150, 110, 60), oak)
            d.rectangle(box, outline=oak, width=2)
        bc = (120, 84, 50) if not ruined else (80, 60, 44)
        d.rectangle((x0 - 3, 135, x0 + 27, 140), fill=bc, outline=INK)
        if before:
            for i in range(6):
                d.ellipse((x0 - 2 + i * 5, 131, x0 + 2 + i * 5, 135), fill=rnd.choice([(164, 84, 74), (196, 170, 108), (170, 124, 132)]))
        if after:
            for i in range(5):
                d.line([(x0 + 1 + i * 6, 135), (x0 + 1 + i * 6, 129)], fill=(70, 120, 80))
                d.ellipse((x0 - 1 + i * 6, 125, x0 + 3 + i * 6, 129), fill=rnd.choice([(150, 120, 176), (116, 164, 158)]))

    # ---------------- roof, top-down 3/4: front slope + a front gable whose slopes run away from us
    roofs.slope(im, [(24, 34), (232, 34), (232, 104), (24, 104)], roof, "tile", seed=2)
    roofs.verge(im, 24, 32, 104, roof, "l"); roofs.verge(im, 232, 32, 104, roof, "r")
    for _ in range(40 if not ruined else 110):                                    # moss on the lowest courses
        x = rnd.randrange(28, 228); y = rnd.randrange(86, 103)
        if not 92 < x < 164:
            d.point((x, y), fill=(98, 124, 60)); d.point((x + 1, y), fill=(84, 110, 52))
    hole = [(176, 46), (206, 46), (206, 52), (214, 52), (214, 64), (220, 64), (220, 82), (204, 82), (204, 88), (186, 88), (186, 82), (172, 82), (172, 64), (168, 64), (168, 52), (176, 52)]   # follows the tile courses
    if ruined:   # a hole through tiles and battens down to the rafters
        d.polygon(hole, fill=(22, 18, 22), outline=INK)
        for x in (180, 196, 210):                                                 # rafters run eave to ridge
            d.line([(x, 47), (x, 87)], fill=(96, 64, 42), width=3); d.line([(x - 1, 47), (x - 1, 87)], fill=(126, 88, 58))
        for y in (58, 72):                                                        # broken battens
            d.line([(173, y), (205, y + 1)], fill=(120, 84, 52), width=2)
        for _ in range(26):                                                       # loose and missing tiles
            x, y = rnd.randrange(40, 226), rnd.randrange(40, 100)
            if 92 < x < 164:
                continue
            d.rectangle((x, y, x + 7, y + 4), fill=(26, 22, 26)); d.line([(x, y + 2), (x + 7, y + 2)], fill=(90, 62, 42))
    if after:    # patched with second-hand slate and a few new tiles
        roofs.slope(im, hole, (112, 108, 136), "slate", seed=9)
        for (x, y) in ((60, 64), (68, 64), (64, 70)):
            d.rectangle((x, y, x + 7, y + 5), fill=(206, 104, 76), outline=shade((206, 104, 76), 0.6))
    roofs.ridge(im, 22, 234, 34, roof)
    roofs.chimney(im, 54, 70, 12, 56, stone, smoke=not ruined)
    roofs.slope(im, [(96, 107), (128, 56), (128, 40), (96, 91)], roof, "tile", vertical=True, light=1.1, seed=4)
    roofs.slope(im, [(160, 107), (128, 56), (128, 40), (160, 91)], roof, "tile", vertical=True, light=0.74, seed=5)
    d.line([(96, 91), (128, 40), (160, 91)], fill=shade(roof, 0.45), width=2)    # valleys
    roofs.eave(im, 22, 96, 103, roof); roofs.eave(im, 160, 234, 103, roof)
    # gable wall: limewash, king post and collar, pointed window
    d.polygon([(100, 104), (156, 104), (128, 62)], fill=plaster, outline=INK)
    d.line([(128, 64), (128, 103)], fill=oak, width=3)
    d.line([(112, 89), (144, 89)], fill=oak, width=3)
    d.line([(103, 101), (112, 89)], fill=oak, width=2); d.line([(153, 101), (144, 89)], fill=oak, width=2)
    win = gothic_arch(121, 135, 96, 104)
    if ruined:
        d.polygon(gothic_arch(122, 134, 82, 88), fill=(36, 30, 34), outline=INK)
    else:
        glass_pane(im, gothic_arch(122, 134, 82, 88), (232, 198, 132), (150, 110, 60), INK)
    roofs.bargeboards(im, (96, 107), (128, 58), (160, 107), oak)

    # ---------------- wrought-iron sign bracket with a scroll, hanging board
    iron = (44, 40, 44)
    d.line([(48, 158), (16, 158)], fill=iron, width=3)
    d.line([(48, 170), (30, 158)], fill=iron, width=2)
    d.arc((14, 150, 24, 160), 90, 360, fill=iron, width=2)
    if ruined:
        d.line([(20, 158), (14, 172)], fill=(120, 120, 126))
        d.polygon([(2, 172), (26, 178), (22, 198), (0, 192)], fill=(140, 96, 60), outline=INK)
    else:
        d.line([(20, 158), (20, 164)], fill=(120, 120, 126)); d.line([(40, 158), (40, 164)], fill=(120, 120, 126))
        board = (150, 104, 64) if before else (110, 140, 120)
        d.rectangle((14, 164, 46, 190), fill=board, outline=INK)
        d.rectangle((23, 170, 33, 185), fill=(220, 180, 80) if before else (240, 220, 170), outline=INK)
        d.rectangle((33, 173, 36, 181), outline=INK)

    # ---------------- props: barrels, trough, bench, rubble
    for bx in (186, 202):
        c = (140, 96, 58) if not ruined else (96, 70, 50)
        if ruined and bx == 202:
            d.rectangle((204, 222, 228, 234), fill=c, outline=INK)
            continue
        d.rectangle((bx, 192, bx + 14, 214), fill=c, outline=INK)
        for yy in (196, 209):
            d.line([(bx, yy), (bx + 14, yy)], fill=(80, 80, 86), width=2)
    d.rectangle((10, 216, 42, 228), fill=(120, 84, 50) if not ruined else (80, 60, 44), outline=INK)   # water trough
    d.rectangle((13, 218, 39, 222), fill=(110, 160, 210) if not ruined else (70, 60, 80))
    if not ruined:
        d.rectangle((60, 206, 96, 210), fill=(140, 96, 58), outline=INK)
        d.rectangle((62, 210, 65, 218), fill=(110, 76, 46)); d.rectangle((91, 210, 94, 218), fill=(110, 76, 46))
    if ruined:
        for _ in range(28):
            x, y = rnd.randrange(44, 236), rnd.randrange(208, 256)
            if 92 < x < 164 and y < 222:
                continue
            d.rectangle((x, y, x + rnd.randrange(3, 7), y + rnd.randrange(2, 5)), fill=rnd.choice([(150, 146, 140), (120, 116, 110), (140, 100, 64)]), outline=INK)
        for (cx, cy, r) in ((70, 124, 14), (196, 170, 12), (140, 120, 10)):
            d.ellipse((cx - r, cy - r // 2, cx + r, cy + r // 2), fill=(60, 54, 52))
        d.ellipse((172, 12, 182, 20), fill=(40, 40, 52)); d.ellipse((168, 9, 174, 15), fill=(40, 40, 52)); d.point((167, 12), fill=(210, 170, 70))
    # iron lanterns either side of the door
    for lx in (98, 158):
        if ruined:
            d.rectangle((lx - 3, 172, lx + 3, 180), outline=(70, 66, 64))
            continue
        if after:
            d.ellipse((lx - 9, 165, lx + 9, 187), fill=(255, 226, 150))
        d.rectangle((lx - 3, 172, lx + 3, 180), fill=(232, 198, 132) if before else (255, 200, 90), outline=INK)
        d.polygon([(lx - 4, 172), (lx + 4, 172), (lx, 168)], fill=iron)
    # harvest fair decorations
    if before:
        for i, x in enumerate(range(30, 226, 10)):
            y = 156 + int(4 * abs((x - 128) / 98))
            d.polygon([(x, y), (x + 8, y), (x + 4, y + 7)], fill=[(164, 84, 74), (196, 170, 108), (98, 116, 140), (112, 134, 98)][i % 4])
        for wx in (92, 164):
            for k in range(5):
                d.line([(wx + k - 2, 214), (wx + k * 2 - 4, 198)], fill=(214, 176, 80))
            d.ellipse((wx - 6, 192, wx + 6, 202), fill=(226, 190, 96))
            d.line([(wx - 4, 206), (wx + 4, 206)], fill=(140, 70, 60), width=2)
        d.rectangle((196, 228, 218, 240), fill=(196, 150, 96), outline=INK)
        for k in range(4):
            d.ellipse((198 + k * 4, 224, 202 + k * 4, 228), fill=(160, 74, 62))
    if after:
        d.line([(116, 180), (116, 192)], fill=(240, 236, 228), width=2); d.point((116, 193), fill=(214, 176, 80))
        d.line([(140, 178), (140, 186)], fill=(90, 70, 50)); d.rectangle((139, 186, 141, 190), fill=(232, 224, 200))
        for _ in range(18):
            x, y = rnd.randrange(30, 230), rnd.randrange(60, 240)
            d.point((x, y), fill=(255, 226, 140)); d.point((x, y - 1), fill=(255, 240, 190))

    detail_pass(im, state, rnd)

    # ---------------- people, for scale
    byname = {c["name"]: c for c in town.TOWN}
    people = {"before": [("Gus Brannock", 112, 178), ("Tilly Brannock", 60, 188), ("Kit Cobb", 176, 196), ("Hamish Cobb", 6, 192)],
              "ruined": [],
              "reclaimed": [("Gus Brannock", 112, 178), ("Pip Wainwright", 60, 196), ("Mira Wainwright", 176, 190)]}[state]
    for name, x, y in people:
        c = dict(byname[name])
        if name == "Mira Wainwright" and after:
            c["over"] = [("apron",)]
        veil(im, lambda d, col, x=x, y=y: d.ellipse((x + 7, y + 59, x + 30, y + 66), fill=col), alpha=80)   # contact shadow
        im.alpha_composite(town.character(c), (x, y))

    # ---------------- mood grading
    if before:
        grade(im, sat=0.8, bright=1.0, tint=(1.03, 1.0, 0.94))
    elif ruined:
        grade(im, sat=0.32, bright=0.84, tint=(0.94, 0.96, 1.06))
    else:
        grade(im, sat=0.7, bright=0.98, tint=(1.02, 0.99, 0.97))
    if ruined:  # the strange world creeping in stays vivid against the grey
        d = ImageDraw.Draw(im)
        prnd = random.Random(11)
        for _ in range(800):
            x, y = prnd.randrange(W), prnd.randrange(H)
            if not (y > 212 or x < 36 or x > 220) or (90 < x < 166 and y > 206 and prnd.random() < 0.7):
                continue
            c = prnd.choice([(150, 100, 180), (124, 84, 160), (176, 130, 206)])
            d.point((x, y), fill=c); d.point((x, y - 1), fill=c)
    return im


def detail_pass(im, state, rnd):
    """Shadows, texture and small lived-in details on top of the Tankard. Light comes from the top left."""
    ruined, before, after = state == "ruined", state == "before", state == "reclaimed"
    d = ImageDraw.Draw(im)
    oak = (84, 56, 38) if not ruined else (62, 48, 40)
    # plaster texture between the beams (limewash is never flat)
    for _ in range(500):
        x, y = rnd.randrange(40, 216), rnd.randrange(103, 148)
        r, g, b, a = im.getpixel((x, y))
        if r > 160:
            f = rnd.choice([0.94, 0.97, 1.03])
            d.point((x, y), fill=(int(r * f), int(g * f), int(b * f)))
    if ruined:   # cracks and water stains
        for x0, y0 in ((60, 104), (160, 112), (110, 130)):
            pts = [(x0, y0)]
            for _ in range(6):
                pts.append((pts[-1][0] + rnd.choice([-2, -1, 1, 2]), pts[-1][1] + 3))
            d.line(pts, fill=(96, 88, 80))
        veil(im, lambda dd, c: (dd.rectangle((130, 104, 150, 146), fill=c), dd.rectangle((182, 104, 196, 140), fill=c)), color=(70, 60, 50), alpha=50)
    # wood grain and a highlight on the left edge of every post
    for x in (38, 74, 104, 152, 182, 218):
        for _ in range(10):
            y = rnd.randrange(102, 146)
            d.line([(x - 1 + rnd.choice([0, 1]), y), (x - 1 + rnd.choice([0, 1]), y + 3)], fill=shade(oak, 0.75))
        d.line([(x - 2, 102), (x - 2, 148)], fill=shade(oak, 1.35))
    # cast shadow of the eaves on the upper wall, and of the bargeboards on the gable
    band(im, 38, 218, 104, 116, 150, 0)
    veil(im, lambda dd, c: dd.line([(102, 103), (127, 66)], fill=c, width=3), alpha=70)
    # shadow under the jetty on the stone ground floor (deep), and under the brackets
    band(im, 48, 208, 157, 172, 160, 0)
    for bx in (48, 92, 164, 208):
        veil(im, lambda dd, c, bx=bx: dd.polygon([(bx + 1, 160), (bx + 5, 160), (bx + 6, 166)], fill=c), alpha=110)
    # upper windows: recessed reveals (top and left in shade), glass reflections, sill shadows
    for x0 in (46, 186):
        veil(im, lambda dd, c, x0=x0: (dd.rectangle((x0 + 2, 114, x0 + 22, 116), fill=c), dd.rectangle((x0 + 2, 114, x0 + 4, 132), fill=c)), alpha=120)
        if not ruined:
            veil(im, lambda dd, c, x0=x0: dd.line([(x0 + 8, 132), (x0 + 20, 116)], fill=c, width=2), color=(255, 250, 230), alpha=110)
        band(im, x0 - 3, x0 + 27, 141, 147, 140, 0)
    # ground-floor windows and door: deep stone reveals, shutter shadows, threshold shadow
    for x0 in (62, 166):
        veil(im, lambda dd, c, x0=x0: (dd.line([(x0 + 1, 194), (x0 + 1, 166), (x0 + 6, 160), (x0 + 13, 157)], fill=c, width=3)), alpha=130)
        if not ruined:
            veil(im, lambda dd, c, x0=x0: dd.line([(x0 + 7, 194), (x0 + 19, 170)], fill=c, width=2), color=(255, 250, 230), alpha=100)
            veil(im, lambda dd, c, x0=x0: (dd.rectangle((x0 - 2, 172, x0 - 1, 200), fill=c), dd.rectangle((x0 + 39, 172, x0 + 40, 200), fill=c),
                                          dd.rectangle((x0 - 11, 199, x0 - 2, 200), fill=c), dd.rectangle((x0 + 30, 199, x0 + 39, 200), fill=c)), alpha=110)
        band(im, x0 - 3, x0 + 29, 198, 203, 120, 0)
    veil(im, lambda dd, c: dd.line([(114, 203), (114, 176), (119, 168), (127, 163)], fill=c, width=4), alpha=150)
    if not ruined:
        for y in range(170, 204, 6):                                                # iron studs on the door
            for x in (117, 124, 132, 139):
                if y > 172 or 121 < x < 136:
                    d.point((x, y), fill=(52, 48, 50))
        d.ellipse((134, 184, 141, 191), outline=(60, 56, 56))                       # ring handle
        for _ in range(16):
            x, y = rnd.randrange(115, 142), rnd.randrange(170, 203)
            d.line([(x, y), (x, y + 2)], fill=(96, 60, 34))
        # hops garland over the door, a chalkboard by the step
        for i in range(13):
            x = 104 + i * 4; y = 160 - int(5 * (1 - ((i - 6) / 6) ** 2))
            d.ellipse((x, y, x + 4, y + 4), fill=(110, 150, 70)); d.point((x + 2, y + 4), fill=(200, 210, 150))
        d.polygon([(160, 214), (170, 194), (180, 214)], fill=(90, 64, 44), outline=INK)
        d.rectangle((163, 198, 177, 210), fill=(48, 56, 52), outline=INK)
        for k, yy in enumerate((201, 204, 207)):
            d.line([(165, yy), (172 + k, yy)], fill=(224, 224, 210))
    # stones: lit top edges, mossy base, ambient occlusion where the wall meets the ground
    for _ in range(140):
        x, y = rnd.randrange(50, 206), rnd.randrange(160, 200)
        r, g, b, a = im.getpixel((x, y))
        if 120 < r < 200 and abs(r - g) < 20:
            d.line([(x, y), (x + 3, y)], fill=shade((r, g, b), 1.12))
    for _ in range(60):
        d.point((rnd.randrange(50, 206), rnd.randrange(198, 204)), fill=(96, 126, 64) if not ruined else (90, 92, 70))
    band(im, 48, 208, 196, 204, 0, 90)
    # the building's cast shadow on the ground to the right and below
    veil(im, lambda dd, c: dd.polygon([(218, 106), (234, 116), (234, 214), (210, 214), (208, 206), (218, 200)], fill=c), alpha=70)
    band(im, 100, 156, 210, 216, 110, 0)
    # props: shadows to the lower right
    veil(im, lambda dd, c: (dd.ellipse((186, 210, 222, 220), fill=c), dd.ellipse((12, 226, 48, 234), fill=c),
                            dd.polygon([(16, 190), (30, 194), (36, 216), (22, 214)], fill=c)), alpha=70)
    if not ruined:
        veil(im, lambda dd, c: dd.rectangle((62, 216, 98, 220), fill=c), alpha=70)
        veil(im, lambda dd, c: dd.ellipse((160, 210, 186, 218), fill=c), alpha=60)
        # warm lantern light pooling on the wall and cobbles
        for lx in (98, 158):
            veil(im, lambda dd, c, lx=lx: dd.ellipse((lx - 14, 162, lx + 14, 196), fill=c), color=(255, 200, 110), alpha=40)
            veil(im, lambda dd, c, lx=lx: dd.ellipse((lx - 18, 206, lx + 18, 222), fill=c), color=(255, 210, 130), alpha=35)
            d.rectangle((lx - 2, 173, lx + 2, 179), fill=(255, 230, 150))
    # rain barrel with a downspout on the right corner
    d.line([(214, 104), (214, 170)], fill=(110, 110, 118), width=3)
    d.rectangle((208, 170, 224, 194), fill=(130, 90, 54) if not ruined else (90, 66, 48), outline=INK)
    for yy in (174, 189):
        d.line([(208, yy), (224, yy)], fill=(80, 80, 86), width=2)
    if not ruined:
        d.rectangle((210, 170, 222, 172), fill=(110, 160, 210))
    veil(im, lambda dd, c: dd.ellipse((210, 190, 232, 198), fill=c), alpha=70)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    states = [("before", "1 · Before: Harvest Fair (prologue only)", "the liveliest it gets (still muted): crowded, bunting along the jetty, flowers, wheat, smoke, lit windows"),
              ("ruined", "2 · Ruined: after the Shift", "desaturated and cold; roof hole, broken leaded glass, fallen shutter, sagging jetty bracket, sign on one chain, dead ivy, purple grass"),
              ("reclaimed", "3 · Reclaimed: the new normal", "patched, not restored: slate patch on the tiles, one fresh unpainted shutter, strange plants, gold Hope lanterns, both charms on the door")]
    S = 2
    bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 17)
    reg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 26)
    sheet = Image.new("RGBA", (30 + 3 * (W * S + 24), 110 + H * S + 80), (243, 234, 214, 255))
    d = ImageDraw.Draw(sheet)
    d.text((30, 22), "The Gilded Tankard in three world states", font=title, fill=(58, 42, 26))
    d.text((30, 60), "High-medieval European, a little gothic, a little rustic: stone ground floor, pointed arches, jettied half-timbered upper floor, steep tiled roof, iron sign. Same building in every state.", font=reg, fill=(90, 74, 58))
    for i, (st, label, sub) in enumerate(states):
        im = scene(st)
        im.save(OUT / f"tankard_{st}.png")
        x = 30 + i * (W * S + 24)
        sheet.alpha_composite(im.resize((W * S, H * S), Image.NEAREST), (x, 96))
        d.text((x, 104 + H * S), label, font=bold, fill=(42, 30, 20))
        lines, cur = [], ""
        for w in sub.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=reg) <= W * S:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
        for j, line in enumerate(lines):
            d.text((x, 128 + H * S + j * 17), line, font=reg, fill=(90, 74, 58))
    sheet.save(OUT / "tankard_states.png")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------- the architectural range
def ground(d, rnd, grass=(108, 132, 84)):
    d.rectangle((0, 0, W, H), fill=grass)
    for _ in range(1000):
        x, y = rnd.randrange(W), rnd.randrange(H)
        c = shade(grass, rnd.choice([0.85, 0.92, 1.08]))
        d.point((x, y), fill=c); d.point((x, y - 1), fill=c)


def cottage():
    """Mira's cottage: rustic, thatched, wattle-and-daub, with a bread oven."""
    rnd = random.Random(3)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(im)
    ground(d, rnd)
    path = (196, 170, 120)
    d.polygon([(112, 206), (140, 206), (150, H), (102, H)], fill=path)
    # vegetable patch and wattle fence
    d.rectangle((10, 212, 70, 250), fill=(120, 86, 56))
    for y in range(216, 250, 8):
        for x in range(14, 68, 8):
            d.ellipse((x, y, x + 5, y + 4), fill=rnd.choice([(92, 120, 76), (106, 132, 84)]))
    for x in range(4, 252, 6):
        if 98 < x < 154:
            continue
        d.line([(x, 246), (x, 258)], fill=(120, 84, 50), width=2)
    d.line([(4, 250), (98, 250)], fill=(150, 110, 70), width=2); d.line([(154, 250), (252, 250)], fill=(150, 110, 70), width=2)
    stone = (150, 142, 128)
    # walls: daub over wattle, oak posts, stone plinth
    daub = (236, 222, 196)
    oak = (84, 56, 38)
    d.rectangle((56, 132, 200, 206), fill=daub, outline=INK)
    d.rectangle((56, 196, 200, 206), fill=stone, outline=INK)
    for x in (56, 104, 152, 200):
        d.rectangle((x - 2, 132, x + 2, 196), fill=oak)
    d.line([(58, 194), (102, 140)], fill=oak, width=3); d.line([(198, 194), (154, 140)], fill=oak, width=3)
    # round-topped door painted blue, small shuttered windows
    d.rounded_rectangle((114, 152, 142, 206), 12, fill=(88, 102, 118), outline=INK)
    for x in (121, 128, 135):
        d.line([(x, 156), (x, 204)], fill=(74, 86, 100))
    d.ellipse((136, 180, 139, 183), fill=(60, 56, 56))
    for x0 in (70, 162):
        d.rectangle((x0, 156, x0 + 24, 178), fill=(232, 198, 132), outline=INK)
        d.line([(x0 + 12, 156), (x0 + 12, 178)], fill=oak, width=2); d.line([(x0, 167), (x0 + 24, 167)], fill=oak, width=2)
        d.rectangle((x0 - 9, 154, x0 - 2, 180), fill=(128, 84, 72), outline=INK); d.rectangle((x0 + 26, 154, x0 + 33, 180), fill=(128, 84, 72), outline=INK)
        d.rectangle((x0 - 2, 179, x0 + 26, 184), fill=(120, 84, 50), outline=INK)
        for i in range(5):
            d.ellipse((x0 + i * 5, 175, x0 + i * 5 + 4, 179), fill=rnd.choice([(164, 84, 74), (196, 170, 108), (170, 124, 132)]))
    # thatch, top-down 3/4: a deep front slope with softened corners, a block-cut ridge and a thick eave roll
    thatch = (198, 162, 94)
    roofs.slope(im, [(38, 62), (44, 50), (56, 44), (200, 44), (212, 50), (218, 62), (220, 128), (36, 128)], thatch, "thatch", seed=6)
    for _ in range(34):                                                            # moss and darker weathering
        x, y = rnd.randrange(42, 214), rnd.randrange(96, 126)
        d.point((x, y), fill=(98, 124, 60)); d.point((x + 1, y), fill=(120, 110, 70))
    # eyebrow dormer: the thatch rolls up and over Pip's window
    roofs.slope(im, [(104, 112), (110, 98), (120, 92), (136, 92), (146, 98), (152, 112)], shade(thatch, 1.08), "thatch", seed=8)
    d.rectangle((118, 102, 138, 116), fill=(232, 198, 132), outline=INK)
    d.line([(128, 102), (128, 116)], fill=(84, 56, 38), width=2)
    d.ellipse((121, 106, 126, 111), fill=(255, 240, 170))                         # the lantern
    d.line([(116, 101), (140, 101)], fill=shade(thatch, 0.55), width=2)            # shadow under the eyebrow
    # block-cut ridge with scalloped edge and crossed hazel spars
    ridge_c = shade(thatch, 0.88)
    d.rounded_rectangle((48, 36, 208, 50), 6, fill=ridge_c, outline=INK)
    for x in range(52, 204, 10):
        d.chord((x, 44, x + 10, 56), 0, 180, fill=ridge_c, outline=INK)
    for x in range(54, 204, 8):
        d.line([(x, 39), (x + 6, 47)], fill=shade(ridge_c, 0.7)); d.line([(x + 6, 39), (x, 47)], fill=shade(ridge_c, 0.7))
    d.line([(52, 38), (204, 38)], fill=shade(ridge_c, 1.2))
    # eave roll: the thick, rounded lower edge of the thatch, with its shadow on the wall
    roofs.slope(im, [(32, 126), (224, 126), (226, 132), (222, 138), (34, 138), (30, 132)], shade(thatch, 0.92), "thatch", seed=7)
    d.line([(34, 139), (222, 139)], fill=shade(thatch, 0.5), width=2)
    band(im, 56, 200, 140, 150, 140, 0)
    roofs.chimney(im, 62, 78, 22, 64, stone, seed=5)
    # clay bread oven
    d.chord((204, 170, 246, 220), 180, 360, fill=(184, 112, 76), outline=INK)
    d.rectangle((204, 194, 246, 206), fill=(150, 142, 128), outline=INK)
    d.chord((216, 182, 234, 204), 180, 360, fill=(40, 30, 28))
    d.point((224, 190), fill=(255, 160, 80)); d.point((226, 192), fill=(255, 200, 100))
    # woodpile, a cat
    for i in range(3):
        for j in range(4 - i):
            d.ellipse((10 + j * 10 + i * 5, 190 - i * 8, 20 + j * 10 + i * 5, 198 - i * 8), fill=(150, 104, 64), outline=INK)
    byname = {c["name"]: c for c in town.TOWN}
    for name, x, y in (("Mira Wainwright", 150, 188), ("Pip Wainwright", 84, 196)):
        c = dict(byname[name])
        if name == "Mira Wainwright":
            c["hat"] = (None,)
        im.alpha_composite(town.character(c), (x, y))
    grade(im, sat=0.78, bright=1.0, tint=(1.03, 1.0, 0.95))
    return im


def abbey():
    """The Abbey: the town's gothic anchor. Stone, pointed portal, rose window, buttresses, bell-cote."""
    rnd = random.Random(5)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(im)
    ground(d, rnd)
    stone, dark = (164, 160, 166), (120, 116, 124)
    slate = (86, 92, 118)
    # slate roof, top-down 3/4: the nave runs away from us, so both slopes are parallelograms
    roofs.slope(im, [(56, 96), (128, 40), (128, 6), (56, 62)], slate, "slate", vertical=True, light=1.12, seed=11)
    roofs.slope(im, [(200, 96), (128, 40), (128, 6), (200, 62)], slate, "slate", vertical=True, light=0.72, seed=12)
    d.rectangle((126, 6, 130, 40), fill=(110, 116, 128), outline=INK)            # lead ridge with cresting
    for y in range(9, 39, 5):
        d.point((128, y), fill=(170, 176, 186))
    d.line([(56, 62), (56, 96)], fill=shade(slate, 0.5), width=2); d.line([(200, 62), (200, 96)], fill=shade(slate, 0.5), width=2)   # eaves
    # facade with a pointed gable
    face = [(60, 214), (60, 92), (128, 40), (196, 92), (196, 214)]
    d.polygon(face, fill=stone, outline=INK)
    for y in range(96, 214, 7):                                                    # ashlar courses
        for x in range(62 + (y // 7 % 2) * 7, 196, 14):
            d.rectangle((x, y, x + 12, y + 5), outline=shade(stone, 0.86))
    d.line([(60, 92), (128, 40), (196, 92)], fill=shade(stone, 1.15), width=4)      # coping
    # bell-cote with the Abbey bell (a Hope anchor)
    d.rectangle((116, 14, 140, 44), fill=stone, outline=INK)
    d.polygon(gothic_arch(121, 135, 30, 42), fill=(40, 36, 44), outline=INK)
    d.chord((122, 28, 134, 42), 180, 360, fill=(214, 176, 80)); d.rectangle((122, 35, 134, 37), fill=(214, 176, 80))
    d.polygon([(112, 16), (144, 16), (128, 0)], fill=slate, outline=INK)
    d.polygon([(126, 0), (130, 0), (128, -6)], fill=(60, 56, 60))
    # buttresses with pinnacles and gargoyles
    for bx in (48, 194):
        d.polygon([(bx, 216), (bx, 120), (bx + 4, 110), (bx + 10, 110), (bx + 14, 120), (bx + 14, 216)], fill=dark, outline=INK)
        d.polygon([(bx + 2, 112), (bx + 12, 112), (bx + 7, 90)], fill=dark, outline=INK)
        d.ellipse((bx + 4, 120, bx + 12, 126), fill=(70, 66, 74))                   # gargoyle head
        d.point((bx + (2 if bx < 128 else 12), 123), fill=(70, 66, 74))
    # rose window with stained glass
    cx, cy, r = 128, 104, 22
    d.ellipse((cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3), fill=shade(stone, 1.12), outline=INK)
    cols = [(140, 74, 72), (78, 92, 128), (184, 158, 96), (88, 118, 96)]
    for i in range(12):
        d.pieslice((cx - r, cy - r, cx + r, cy + r), i * 30, i * 30 + 30, fill=cols[i % 4], outline=(50, 46, 50))
    d.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=(240, 220, 150), outline=(50, 46, 50))
    # lancet windows with stained glass
    for x0 in (74, 168):
        for dx in (0, 10):
            glass_pane(im, gothic_arch(x0 + dx, x0 + dx + 8, 150, 176), (70, 100, 170), (50, 46, 56), INK)
            d.rectangle((x0 + dx + 2, 162, x0 + dx + 5, 166), fill=(190, 60, 60))
    # great portal: recessed pointed arches, double oak doors
    for i, c in enumerate((shade(stone, 1.18), stone, shade(stone, 1.1))):
        d.polygon(gothic_arch(98 + i * 5, 158 - i * 5, 176, 214), fill=c, outline=INK)
    doors = gothic_arch(113, 143, 180, 214)
    d.polygon(doors, fill=(104, 66, 40), outline=INK)
    d.line([(128, 166), (128, 214)], fill=INK)
    for y in (186, 202):
        d.line([(115, y), (126, y)], fill=(40, 36, 36), width=2); d.line([(130, y), (141, y)], fill=(40, 36, 36), width=2)
    d.rectangle((90, 214, 166, 222), fill=shade(stone, 1.1), outline=INK)
    d.rectangle((82, 222, 174, 230), fill=shade(stone, 1.05), outline=INK)
    # herb beds and a stone cross
    for x0 in (8, 204):
        d.rectangle((x0, 226, x0 + 44, 254), fill=(120, 86, 56), outline=INK)
        for _ in range(24):
            x, y = rnd.randrange(x0 + 3, x0 + 41), rnd.randrange(229, 252)
            d.point((x, y), fill=rnd.choice([(100, 126, 84), (138, 120, 156), (196, 180, 128)]))
    d.rectangle((20, 180, 26, 214), fill=dark, outline=INK); d.rectangle((14, 188, 32, 194), fill=dark, outline=INK)
    byname = {c["name"]: c for c in town.TOWN}
    for name, x, y in (("Father Aldous", 104, 168), ("Brother Fennick", 144, 172), ("Sabine Marsh", 216, 178)):
        im.alpha_composite(town.character(byname[name]), (x, y))
    grade(im, sat=0.78, bright=0.98, tint=(1.01, 1.0, 1.0))
    return im


def range_sheet():
    S = 2
    bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 17)
    reg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 26)
    panels = [
        (cottage(), "Rustic · Mira's cottage", "thatch, wattle-and-daub between oak posts, stone plinth, painted door and shutters, clay bread oven, wattle fence, veg patch"),
        (scene("before"), "Town · the Gilded Tankard", "rubble-stone ground floor with pointed arches, jettied half-timbered upper floor in ochre limewash, steep red tiles, iron sign"),
        (abbey(), "Gothic · the Abbey", "dressed stone, steep slate roof, pointed portal, rose window and lancets in stained glass, buttresses, gargoyles, bell-cote"),
    ]
    sheet = Image.new("RGBA", (30 + 3 * (W * S + 24), 110 + H * S + 80), (243, 234, 214, 255))
    d = ImageDraw.Draw(sheet)
    d.text((30, 22), "Hollowmere's architecture: rustic to gothic", font=title, fill=(58, 42, 26))
    d.text((30, 60), "High-medieval northern Europe (Rothenburg, Colmar, York's Shambles, Bruges). Muted, earthy palette: life comes from detail, light and people, not saturation.", font=reg, fill=(90, 74, 58))
    for i, (im, label, sub) in enumerate(panels):
        x = 30 + i * (W * S + 24)
        sheet.alpha_composite(im.resize((W * S, H * S), Image.NEAREST), (x, 96))
        d.text((x, 104 + H * S), label, font=bold, fill=(42, 30, 20))
        lines, cur = [], ""
        for w in sub.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=reg) <= W * S:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
        for j, line in enumerate(lines):
            d.text((x, 128 + H * S + j * 17), line, font=reg, fill=(90, 74, 58))
    sheet.save(OUT / "architecture_range.png")


if __name__ == "__main__":
    range_sheet()

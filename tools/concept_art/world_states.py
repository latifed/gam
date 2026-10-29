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

OUT = Path(__file__).resolve().parents[2] / "docs" / "concept-art" / "world"
W, H = 256, 232
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


def scene(state):
    rnd = random.Random(7)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(im)
    ruined, before, after = state == "ruined", state == "before", state == "reclaimed"

    # ---------------- ground
    grass = (110, 168, 80) if not ruined else (120, 112, 104)
    d.rectangle((0, 0, W, H), fill=grass)
    for _ in range(900):
        x, y = rnd.randrange(W), rnd.randrange(H)
        c = shade(grass, rnd.choice([0.85, 0.92, 1.08]))
        if ruined and rnd.random() < 0.3:
            c = (96, 84, 76)                                                         # dead patches
        if after and y > 196 and (x < 40 or x > 216) and rnd.random() < 0.5:
            c = rnd.choice([(150, 110, 170), (176, 136, 196)])                      # tamed purple border
        d.point((x, y), fill=c)
        if rnd.random() < 0.3:
            d.point((x, y - 1), fill=c)
    # path to the door
    path = (196, 170, 120) if not ruined else (150, 132, 110)
    d.polygon([(108, 182), (148, 182), (164, H), (92, H)], fill=path)
    for _ in range(80):
        x, y = rnd.randrange(96, 160), rnd.randrange(184, H)
        d.point((x, y), fill=shade(path, rnd.choice([0.85, 1.1])))

    # ---------------- building
    plaster = (238, 224, 190) if not ruined else (186, 176, 160)
    beam = (96, 64, 44) if not ruined else (70, 52, 42)
    stone = (150, 146, 140)
    roof = (168, 72, 56) if not ruined else (120, 64, 56)
    # chimney
    d.rectangle((176, 6, 194, 40), fill=stone, outline=INK)
    for y in range(10, 40, 6):
        d.line([(177, y), (193, y)], fill=shade(stone, 0.8))
    # walls
    d.rectangle((40, 64, 216, 178), fill=plaster, outline=INK)
    d.rectangle((40, 150, 216, 178), fill=stone, outline=INK)                     # stone footing
    for y in range(154, 178, 6):
        for x in range(42 + (y // 6 % 2) * 6, 216, 12):
            d.rectangle((x, y, x + 10, y + 4), outline=shade(stone, 0.78))
    for x in (40, 84, 128, 172, 216):                                              # timber frame
        d.rectangle((x - 2, 64, x + 2, 150), fill=beam)
    for y in (64, 110, 148):
        d.rectangle((40, y - 2, 216, y + 2), fill=beam)
    for x0 in (40, 172):
        d.line([(x0 + 2, 108), (x0 + 42, 68)], fill=beam, width=3)
    # windows (upper and lower)
    lit = (255, 214, 110)
    for (x0, y0) in ((52, 74), (176, 74), (52, 118), (176, 118)):
        w, h = 28, 26
        glass = lit if before or after else (40, 34, 40)
        d.rectangle((x0, y0, x0 + w, y0 + h), fill=glass, outline=INK)
        d.line([(x0 + w // 2, y0), (x0 + w // 2, y0 + h)], fill=beam, width=2)
        d.line([(x0, y0 + h // 2), (x0 + w, y0 + h // 2)], fill=beam, width=2)
        if ruined:
            d.polygon([(x0 + 2, y0 + 2), (x0 + 9, y0 + 2), (x0 + 4, y0 + 10)], fill=(150, 170, 180))   # jagged glass
            d.polygon([(x0 + w - 2, y0 + h - 2), (x0 + w - 10, y0 + h - 2), (x0 + w - 3, y0 + h - 9)], fill=(150, 170, 180))
            if (x0, y0) in ((52, 118), (176, 74)):                                   # boarded up
                for i, dy in enumerate((6, 14, 20)):
                    d.line([(x0 - 3, y0 + dy + i), (x0 + w + 3, y0 + dy - 3 + i)], fill=(140, 100, 64), width=4)
        if after and (x0, y0) == (52, 118):
            d.rectangle((x0 - 1, y0 - 1, x0 + w + 1, y0 + h + 1), outline=(176, 132, 84), width=2)   # new frame, fresh wood
        # flower boxes under the lower windows
        if y0 == 118:
            box = (120, 84, 50) if not ruined else (80, 60, 44)
            d.rectangle((x0 - 2, y0 + h + 1, x0 + w + 2, y0 + h + 6), fill=box, outline=INK)
            if before:
                for i in range(6):
                    d.ellipse((x0 + i * 5, y0 + h - 3, x0 + i * 5 + 4, y0 + h + 1), fill=rnd.choice([(220, 60, 60), (240, 200, 70), (230, 120, 160)]))
            if after:  # strange plants: glowing bulbs
                for i in range(5):
                    d.line([(x0 + 3 + i * 6, y0 + h + 1), (x0 + 3 + i * 6, y0 + h - 5)], fill=(70, 120, 80))
                    d.ellipse((x0 + 1 + i * 6, y0 + h - 9, x0 + 5 + i * 6, y0 + h - 5), fill=rnd.choice([(170, 120, 230), (110, 210, 200)]))
    # upper middle round window
    d.ellipse((116, 76, 140, 100), fill=lit if not ruined else (40, 34, 40), outline=INK)
    d.line([(128, 76), (128, 100)], fill=beam, width=2); d.line([(116, 88), (140, 88)], fill=beam, width=2)
    # door
    if ruined:
        d.rectangle((110, 124, 146, 178), fill=(30, 24, 26), outline=INK)            # dark doorway
        d.polygon([(146, 124), (160, 132), (160, 182), (146, 178)], fill=(110, 70, 44), outline=INK)   # door hanging off
    else:
        d.rectangle((110, 124, 146, 178), fill=(120, 76, 44), outline=INK)
        for x in (118, 128, 138):
            d.line([(x, 126), (x, 176)], fill=(96, 60, 36))
        d.ellipse((139, 150, 142, 153), fill=(214, 176, 80))
    d.rectangle((102, 178, 154, 184), fill=shade(stone, 1.05), outline=INK)       # step

    # ---------------- roof
    d.polygon([(26, 70), (230, 70), (204, 18), (52, 18)], fill=roof, outline=INK)
    for i, y in enumerate(range(22, 70, 7)):
        t = (y - 18) / 52
        xl, xr = 52 - 26 * t, 204 + 26 * t
        d.line([(xl, y), (xr, y)], fill=shade(roof, 0.75))
        for x in range(int(xl) + (i % 2) * 6, int(xr), 12):
            d.line([(x, y), (x, y + 6)], fill=shade(roof, 0.8))
    d.line([(52, 18), (204, 18)], fill=shade(roof, 1.25), width=2)
    if ruined:  # hole in the roof with broken rafters
        d.polygon([(110, 26), (150, 30), (156, 52), (120, 58), (100, 44)], fill=(24, 20, 22), outline=INK)
        for x0, x1 in ((112, 140), (106, 150)):
            d.line([(x0, 38), (x1, 44)], fill=(90, 60, 40), width=2)
        for _ in range(14):
            x, y = rnd.randrange(60, 200), rnd.randrange(24, 66)
            d.rectangle((x, y, x + 3, y + 2), fill=(24, 20, 22))
    if after:  # patched with mismatched new shingles and a slate patch
        d.polygon([(110, 26), (150, 30), (156, 52), (120, 58), (100, 44)], fill=(120, 110, 140), outline=INK)
        for y in range(30, 58, 6):
            d.line([(104, y), (154, y)], fill=(96, 88, 118))
        d.rectangle((60, 40, 76, 50), fill=(196, 96, 72), outline=INK)

    # ---------------- sign: a tankard on a board
    d.line([(40, 126), (18, 126)], fill=INK, width=3)
    if ruined:   # hanging by one chain
        d.line([(20, 126), (16, 140)], fill=(120, 120, 126))
        d.polygon([(6, 140), (30, 146), (26, 168), (2, 160)], fill=(140, 96, 60), outline=INK)
    else:
        d.line([(20, 126), (20, 132)], fill=(120, 120, 126)); d.line([(36, 126), (36, 132)], fill=(120, 120, 126))
        board = (150, 104, 64) if before else (110, 140, 120)
        d.rectangle((14, 132, 42, 156), fill=board, outline=INK)
        d.rectangle((22, 138, 32, 152), fill=(220, 180, 80) if before else (240, 220, 170), outline=INK)
        d.rectangle((32, 141, 35, 148), outline=INK)

    # ---------------- props
    # barrels by the door
    for bx in (186, 202):
        c = (140, 96, 58) if not ruined else (96, 70, 50)
        d.rectangle((bx, 160, bx + 14, 182), fill=c, outline=INK)
        for yy in (164, 177):
            d.line([(bx, yy), (bx + 14, yy)], fill=(80, 80, 86), width=2)
    if ruined:   # second barrel tipped over, rubble, scorch
        d.rectangle((200, 186, 222, 198), fill=(96, 70, 50), outline=INK)
        for _ in range(24):
            x, y = rnd.randrange(44, 230), rnd.randrange(176, 220)
            if 96 < x < 160 and y < 190:
                continue
            d.rectangle((x, y, x + rnd.randrange(3, 7), y + rnd.randrange(2, 5)), fill=rnd.choice([(150, 146, 140), (120, 116, 110), (140, 100, 64)]), outline=INK)
        for (cx, cy, r) in ((70, 100, 14), (190, 136, 12), (150, 70, 10)):
            d.ellipse((cx - r, cy - r // 2, cx + r, cy + r // 2), fill=(60, 54, 52))
    # bench
    if not ruined:
        d.rectangle((48, 170, 92, 174), fill=(140, 96, 58), outline=INK)
        d.rectangle((50, 174, 53, 182), fill=(110, 76, 46)); d.rectangle((87, 174, 90, 182), fill=(110, 76, 46))

    # lanterns either side of the door
    for lx in (100, 152):
        if ruined:
            d.rectangle((lx - 3, 140, lx + 3, 148), outline=(70, 66, 64))
            continue
        glow = (255, 214, 110) if before else (255, 200, 90)
        if after:
            d.ellipse((lx - 9, 133, lx + 9, 155), fill=(255, 226, 150))            # gold Hope glow (anchor)
        d.rectangle((lx - 3, 140, lx + 3, 148), fill=glow, outline=INK)

    # chimney smoke
    if not ruined:
        for i, (sx, sy, r) in enumerate(((186, 2, 5), (180, -6, 6), (190, -12, 4))):
            d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(226, 226, 230))

    # harvest fair decorations
    if before:
        for i, x in enumerate(range(30, 226, 10)):                                 # bunting along the eaves
            y = 74 + int(6 * ((x - 128) / 98) ** 2) * -1 + 6
            d.polygon([(x, y), (x + 8, y), (x + 4, y + 7)], fill=[(220, 60, 60), (240, 200, 70), (70, 130, 200), (90, 170, 90)][i % 4])
        for wx in (96, 158):                                                       # wheat sheaves
            for k in range(5):
                d.line([(wx + k - 2, 182), (wx + k * 2 - 4, 166)], fill=(214, 176, 80))
            d.ellipse((wx - 6, 160, wx + 6, 170), fill=(226, 190, 96))
            d.line([(wx - 4, 174), (wx + 4, 174)], fill=(176, 50, 44), width=2)
        d.rectangle((60, 186, 80, 198), fill=(196, 150, 96), outline=INK)          # crate of apples
        for k in range(4):
            d.ellipse((62 + k * 4, 182, 66 + k * 4, 186), fill=(210, 50, 50))
    if after:   # both sides of the soil feud on the door: Abbey ribbon and Sabine's bone charm
        d.line([(114, 130), (114, 142)], fill=(240, 236, 228), width=2); d.point((114, 143), fill=(214, 176, 80))
        d.line([(142, 128), (142, 136)], fill=(90, 70, 50)); d.rectangle((141, 136, 143, 140), fill=(232, 224, 200))
        for _ in range(16):                                                        # gold hope motes
            x, y = rnd.randrange(30, 230), rnd.randrange(60, 200)
            d.point((x, y), fill=(255, 226, 140)); d.point((x, y - 1), fill=(255, 240, 190))
    if ruined:   # a crow on the roof
        d.ellipse((168, 12, 178, 20), fill=(40, 40, 52)); d.ellipse((164, 9, 170, 15), fill=(40, 40, 52)); d.point((163, 12), fill=(210, 170, 70))

    # ---------------- people (32x64 sprites, for scale)
    byname = {c["name"]: c for c in town.TOWN}
    people = {"before": [("Gus Brannock", 120, 150), ("Tilly Brannock", 66, 158), ("Kit Cobb", 170, 166), ("Hamish Cobb", 20, 160)],
              "ruined": [],
              "reclaimed": [("Gus Brannock", 120, 150), ("Pip Wainwright", 62, 166), ("Mira Wainwright", 170, 160)]}[state]
    for name, x, y in people:
        c = dict(byname[name])
        if name == "Mira Wainwright" and after:
            c["over"] = [("apron",)]
        im.alpha_composite(town.character(c), (x, y))

    # ---------------- mood grading
    if before:
        grade(im, sat=1.12, bright=1.03, tint=(1.04, 1.0, 0.94))
    elif ruined:
        grade(im, sat=0.45, bright=0.86, tint=(0.92, 0.95, 1.08))
    else:
        grade(im, sat=0.95, bright=1.0, tint=(1.02, 0.99, 1.0))
    if ruined:  # the strange world creeping in stays vivid against the grey
        d = ImageDraw.Draw(im)
        prnd = random.Random(11)
        for _ in range(700):
            x, y = prnd.randrange(W), prnd.randrange(H)
            near_wall = 172 < y < 186 and 36 < x < 220
            if not (y > 184 or x < 36 or x > 220 or near_wall) or (96 < x < 160 and y > 182 and prnd.random() < 0.7):
                continue
            c = prnd.choice([(150, 100, 180), (124, 84, 160), (176, 130, 206)])
            d.point((x, y), fill=c); d.point((x, y - 1), fill=c)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    states = [("before", "1 · Before: Harvest Fair (prologue only)", "warm, saturated, crowded; bunting, flowers, smoke, lit windows"),
              ("ruined", "2 · Ruined: after the Shift", "desaturated and cold; roof hole, boarded and broken glass, sign on one chain, rubble, purple grass"),
              ("reclaimed", "3 · Reclaimed: the new normal", "patched, not restored: mismatched roof, strange plants, gold Hope lanterns, both charms on the door")]
    S = 2
    bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 17)
    reg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 26)
    sheet = Image.new("RGBA", (30 + 3 * (W * S + 24), 110 + H * S + 80), (243, 234, 214, 255))
    d = ImageDraw.Draw(sheet)
    d.text((30, 22), "The Gilded Tankard in three world states", font=title, fill=(58, 42, 26))
    d.text((30, 60), "Same building, same layout; the state changes overlays, props, people and colour grading.", font=reg, fill=(90, 74, 58))
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

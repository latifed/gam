"""Concept pixel art for Mira Wainwright: 16x32 walk sprites and 64x64 portraits.

Run: python3 tools/concept_art/mira.py   (writes to docs/concept-art/mira/)
Placeholder/concept quality: a style reference, not final game art.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[2] / "docs" / "concept-art" / "mira"

PAL = {
    ".": None,
    "O": (43, 29, 26),     # outline
    "H": (110, 59, 44),    # hair
    "h": (143, 80, 56),    # hair highlight
    "K": (201, 151, 60),   # kerchief
    "k": (160, 116, 40),   # kerchief shadow
    "S": (234, 184, 153),  # skin
    "s": (201, 143, 114),  # skin shadow
    "R": (224, 154, 134),  # cheek
    "M": (168, 87, 74),    # mouth
    "D": (77, 116, 112),   # dress
    "d": (57, 87, 90),     # dress shadow
    "A": (239, 228, 207),  # apron
    "a": (205, 191, 166),  # apron shadow
    "F": (255, 255, 255),  # flour
    "B": (74, 48, 34),     # boots
}

FRONT = """
................
.....OOOOOO.....
....OKKKKKKO....
...OKKKKKKKKO...
...OKKKKKKKKO...
..OHkkkkkkkkHO..
..OHHhHHHHhHHO..
..OHSSSSSSSSHO..
..OHSOSSSSOSHO..
..OHSOSSSSOSHO..
..OHRSSSSSSRHO..
...OSSSMMSSSO...
...OsSSSSSSsO...
....OssSSssO....
.....OOssOO.....
....OdDssDdO....
...ODDAAAADDO...
..ODDDAAAADDDO..
..ODdDAAAADdDO..
..ODdOAAAAOdDO..
..OSSOAAAAOSSO..
..OSSOAaFAOSSO..
..OssOAAAAOssO..
...OODAAAADOO...
....ODAAAADO....
....ODaAAaDO....
....ODDaaDDO....
....OdDDDDdO....
....OBBOOBBO....
....OBBOOBBO....
....OOOOOOOO....
................
"""

BACK = """
................
.....OOOOOO.....
....OKKKKKKO....
...OKKKKKKKKO...
...OKKKkkKKKO...
..OHkkkKKkkkHO..
..OHHHHkkHHHHO..
..OHHhHHHHhHHO..
..OHHhHHHHhHHO..
..OHHhHHHHhHHO..
..OHHHHHHHHHHO..
...OHHHHHHHHO...
...OHHHHHHHHO...
....OHHHHHHO....
.....OOssOO.....
....OdDDDDdO....
...ODDADDADDO...
..ODDDADDADDDO..
..ODdDADDADdDO..
..ODdOADDAOdDO..
..OSSOAAAAOSSO..
..OSSODAADOSSO..
..OssODDDDOssO..
...OODDDDDDOO...
....ODDDDDDO....
....ODDDDDDO....
....OdDDDDdO....
....OdDDDDdO....
....OBBOOBBO....
....OBBOOBBO....
....OOOOOOOO....
................
"""

SIDE = """
................
......OOOOO.....
.....OKKKKKO....
....OKKKKKKKO...
...OkKKKKKKKO...
..OkkkkkkkkkO...
..OOHHHHhHHHO...
...OHHHHSSSSO...
...OHHHSSSOSO...
...OHHHSSSOSO...
...OHHSSSRSSSO..
...OHHSSSSSMO...
....OHsSSSSSO...
.....OssSSsO....
......OssO......
.....OdDDdO.....
....ODDDDDAO....
....ODdDDDAO....
....ODdDDDAAO...
....ODSSDDAAO...
....ODSSDDAAO...
....ODssDDAAO...
....ODDDDDAAO...
....ODDDDDAAO...
....ODDDDDaAO...
....OdDDDDaAO...
....OdDDDDDaO...
....OOdDDDDOO...
.....OBBOBBBO...
.....OBBOBBBO...
.....OOOOOOOO...
................
"""

def rows(s):
    r = [l for l in s.strip("\n").split("\n")]
    assert len(r) == 32, len(r)
    for l in r:
        assert len(l) == 16, (len(l), l)
    return r

def with_feet(r, feet):
    r = list(r)
    r[28:31] = feet
    return r

FRONT_FEET_A = ["....OBBOOBBO....", "....OBBOOOOO....", "....OOOO........"]
FRONT_FEET_B = ["....OBBOOBBO....", "....OOOOOBBO....", "........OOOO...."]
SIDE_FEET_A = ["....OBBO.OBBBO..", "....OBBO.OBBBO..", "....OOOO.OOOOO.."]
SIDE_FEET_B = [".....OBBBBBO....", ".....OBBBBBO....", ".....OOOOOOO...."]

def bob(r):
    """Shift the upper body down 1px (walk bounce), keep the feet."""
    r = list(r)
    return ["." * 16] + r[0:27] + r[28:]

def to_img(r):
    im = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
    for y, line in enumerate(r):
        for x, ch in enumerate(line):
            c = PAL[ch]
            if c:
                im.putpixel((x, y), c + (255,))
    return im

def frames():
    f, b, s = rows(FRONT), rows(BACK), rows(SIDE)
    down = [f, bob(with_feet(f, FRONT_FEET_A)), bob(with_feet(f, FRONT_FEET_B))]
    up = [b, bob(with_feet(b, FRONT_FEET_B)), bob(with_feet(b, FRONT_FEET_A))]
    right = [s, bob(with_feet(s, SIDE_FEET_A)), bob(with_feet(s, SIDE_FEET_B))]
    out = {}
    for name, fr in (("down", down), ("up", up), ("right", right)):
        out[name] = [to_img(x) for x in fr]
    out["left"] = [im.transpose(Image.FLIP_LEFT_RIGHT) for im in out["right"]]
    return out

# ---------------- portrait ----------------
def portrait(expr):
    P = {k: v for k, v in PAL.items() if v}
    im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # shoulders, dress, apron straps
    d.ellipse((6, 50, 58, 80), fill=P["D"])
    d.rectangle((20, 52, 25, 63), fill=P["A"]); d.rectangle((39, 52, 44, 63), fill=P["A"])
    d.rectangle((26, 58, 38, 63), fill=P["A"])
    # neck
    d.rectangle((27, 40, 37, 53), fill=P["S"]); d.rectangle((27, 44, 37, 46), fill=P["s"])
    # hair behind the head, loose strands
    d.ellipse((13, 11, 51, 47), fill=P["H"])
    d.rectangle((14, 26, 19, 44), fill=P["H"]); d.rectangle((45, 26, 50, 42), fill=P["H"])
    # face
    d.ellipse((19, 13, 45, 46), fill=P["S"])
    # face shading on the right
    for y in range(13, 47):
        for x in range(38, 46):
            if im.getpixel((x, y))[:3] == P["S"] and im.getpixel((min(x + 2, 63), y))[:3] != P["S"]:
                im.putpixel((x, y), P["s"] + (255,))
    # fringe
    d.polygon([(19, 20), (24, 17), (32, 19), (40, 16), (45, 21), (45, 25), (40, 21), (33, 24), (26, 21), (19, 26)], fill=P["H"])
    d.line([(26, 20), (31, 22)], fill=P["h"]); d.line([(37, 19), (41, 21)], fill=P["h"])
    # kerchief
    d.chord((15, 5, 49, 29), 180, 360, fill=P["K"])
    d.rectangle((15, 15, 49, 16), fill=P["k"])
    d.polygon([(47, 10), (53, 7), (54, 12), (49, 14)], fill=P["K"])
    d.polygon([(48, 13), (54, 16), (51, 19), (47, 16)], fill=P["k"])
    for x, y in ((23, 10), (31, 8), (39, 10), (27, 13), (43, 13)):
        im.putpixel((x, y), P["k"] + (255,))
    # eyes
    for ex in (25, 36):
        d.rectangle((ex, 29, ex + 3, 31), fill=P["O"])
        im.putpixel((ex + 1, 29), (255, 255, 255, 255))
        d.line([(ex - 1, 28), (ex + 4, 28)], fill=P["O"])  # upper lid: a sharp, tired look
    # brows
    if expr == "neutral":
        d.line([(24, 25), (29, 25)], fill=P["H"], width=1); d.line([(35, 25), (40, 25)], fill=P["H"])
    elif expr == "stern":
        d.line([(24, 24), (29, 26)], fill=P["O"]); d.line([(35, 26), (40, 24)], fill=P["O"])
        d.line([(24, 25), (28, 27)], fill=P["H"]); d.line([(36, 27), (40, 25)], fill=P["H"])
    else:  # soft
        d.line([(24, 25), (29, 24)], fill=P["H"]); d.line([(35, 24), (40, 25)], fill=P["H"])
    # nose
    im.putpixel((32, 33), P["s"] + (255,)); im.putpixel((32, 34), P["s"] + (255,)); im.putpixel((33, 35), P["s"] + (255,))
    # cheeks + flour smudge
    d.rectangle((22, 34, 24, 35), fill=P["R"]); d.rectangle((40, 34, 42, 35), fill=P["R"])
    for x, y in ((21, 37), (23, 38), (22, 39)):
        im.putpixel((x, y), (248, 244, 236, 255))
    # mouth
    if expr == "neutral":
        d.line([(29, 39), (35, 39)], fill=P["M"])
    elif expr == "stern":
        d.line([(29, 39), (35, 39)], fill=P["M"]); im.putpixel((28, 40), P["M"] + (255,)); im.putpixel((36, 40), P["M"] + (255,))
    else:
        d.line([(30, 40), (34, 40)], fill=P["M"]); im.putpixel((29, 39), P["M"] + (255,)); im.putpixel((35, 39), P["M"] + (255,))
    # outline around the whole figure
    px = im.load(); edge = []
    for y in range(64):
        for x in range(64):
            if px[x, y][3] == 0 and any(0 <= x + dx < 64 and 0 <= y + dy < 64 and px[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                edge.append((x, y))
    for x, y in edge:
        px[x, y] = P["O"] + (255,)
    bg = Image.new("RGBA", (64, 64), (233, 216, 180, 255))
    bg.alpha_composite(im)
    return bg

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fr = frames()
    order = ["down", "left", "right", "up"]
    sheet = Image.new("RGBA", (16 * 3, 32 * 4), (0, 0, 0, 0))
    for r, name in enumerate(order):
        for c, im in enumerate(fr[name]):
            sheet.paste(im, (c * 16, r * 32))
    sheet.save(OUT / "mira_walk_16x32.png")
    exprs = ["neutral", "stern", "soft"]
    ports = [portrait(e) for e in exprs]
    psheet = Image.new("RGBA", (64 * 3, 64))
    for i, p in enumerate(ports):
        psheet.paste(p, (i * 64, 0))
    psheet.save(OUT / "mira_portraits_64.png")

    # preview sheet, scaled up for viewing
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 22)
    small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 15)
    S = 6
    W, H = 1500, 680
    pv = Image.new("RGBA", (W, H), (243, 234, 214, 255))
    d = ImageDraw.Draw(pv)
    d.text((30, 20), "Mira Wainwright: concept sprites", font=font, fill=(58, 42, 26))
    d.text((30, 52), "16x32 walk cycle (idle, step, step) in 4 directions · shown at 6x", font=small, fill=(90, 74, 58))
    x = 30
    for name in order:
        d.text((x, 85), name, font=small, fill=(90, 74, 58))
        for c, im in enumerate(fr[name]):
            pv.alpha_composite(im.resize((16 * S, 32 * S), Image.NEAREST), (x + c * (16 * S + 6), 110))
        x += 3 * (16 * S + 6) + 26
    y0 = 110 + 32 * S + 40
    d.text((30, y0), "64x64 dialogue portraits · shown at 4x", font=small, fill=(90, 74, 58))
    for i, (p, e) in enumerate(zip(ports, exprs)):
        pv.alpha_composite(p.resize((256, 256), Image.NEAREST), (30 + i * 280, y0 + 28))
        d.text((30 + i * 280, y0 + 292), e, font=small, fill=(90, 74, 58))
    # actual size + palette
    ax = 900
    d.text((ax, y0), "actual size", font=small, fill=(90, 74, 58))
    for c, name in enumerate(order):
        pv.alpha_composite(fr[name][0], (ax + c * 22, y0 + 30))
    pv.alpha_composite(ports[0], (ax, y0 + 75))
    d.text((ax, y0 + 160), "palette", font=small, fill=(90, 74, 58))
    for i, (k, v) in enumerate((k, v) for k, v in PAL.items() if v):
        d.rectangle((ax + (i % 8) * 34, y0 + 185 + (i // 8) * 34, ax + (i % 8) * 34 + 28, y0 + 185 + (i // 8) * 34 + 28), fill=v, outline=(58, 42, 26))
    pv.save(OUT / "mira_preview.png")

    # walk-cycle GIF: idle, step, idle, step in each direction
    gif = []
    for name in order:
        a, b, c = fr[name]
        for im in (a, b, a, c):
            f = Image.new("RGBA", (16, 32), (243, 234, 214, 255))
            f.alpha_composite(im)
            gif.append(f.resize((16 * 8, 32 * 8), Image.NEAREST).convert("P"))
    gif[0].save(OUT / "mira_walk.gif", save_all=True, append_images=gif[1:], duration=160, loop=0)

if __name__ == "__main__":
    main()

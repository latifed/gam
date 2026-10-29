"""Townsfolk progression: Rescued -> Purpose -> Hope, shown on six characters.

Rescued: ragged, dirty, washed-out, no tools.  Purpose: working clothes and the tools of their trade,
muted colours.  Hope: they look after themselves again: clean, mended, their own colours back, and a
personal accent that usually came from someone else in town.
Run: python3 tools/concept_art/stages.py   (writes docs/concept-art/town/stages.png)
"""
import colorsys
import sys
from copy import deepcopy
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import town  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "docs" / "concept-art" / "town"
BY = {c["name"]: c for c in town.TOWN}


def saturate(im, f, warm=1.0):
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            r2, g2, b2 = colorsys.hls_to_rgb(h, l, min(1, s * f))
            px[x, y] = (min(255, int(r2 * 255 * warm)), int(g2 * 255), int(b2 * 255 / warm), a)
    return im


def stage(name, **changes):
    c = deepcopy(BY[name])
    over = changes.pop("over_add", [])
    drop = changes.pop("over_drop", [])
    c["over"] = [o for o in c.get("over", []) if (o[0] if isinstance(o, tuple) else o) not in drop] + over
    c.update(changes)
    return c


RESCUED = dict(prop=None, prop2=None, pose=("down", "down"), mouth="flat", brows="worried", blush=False)
SHOWN = [
    ("Mira Wainwright", "Mira", [
        (stage("Mira Wainwright", **RESCUED, hat=(None,), hair="messy", over_add=["tatters", "dirt", "tired"]),
         "Day 1: torn dress, hair loose, no hat; she won't sit down"),
        (stage("Mira Wainwright", hat=(None,), prop="basket_bread", pose=("front", "front"), over_add=[("apron",), "soot"]),
         "Baking again: apron on, flour and oven soot, a basket of bread"),
        (stage("Mira Wainwright", prop="basket_bread", pose=("front", "front"), mouth="smile", over_add=[("apron",), ("flower", (236, 220, 120))]),
         "Hope: her felt hat back, and the paper flower Pip made her"),
    ]),
    ("Oswin", "Oswin", [
        (stage("Oswin", over_add=["tatters", "dirt", "tired"]), "Carried home: bandaged, arm in a sling"),
        (stage("Oswin", hat=(None,), over_drop=["sling"], pose=("down", "raise"), prop="hammer", mouth="flat", brows="stern",
               over_add=[("leather_apron",), "soot"]), "The forge relit: leather apron, hammer, soot"),
        (stage("Oswin", hat=("bandana", (176, 50, 44)), over_drop=["sling"], pose=("down", "raise"), prop="hammer", mouth="grin", brows="normal",
               over_add=[("leather_apron",), "brooch"]), "Hope: Bruna's red bandana, and a charm he forged himself"),
    ]),
    ("Gus Brannock", "Gus", [
        (stage("Gus Brannock", **RESCUED, over_drop=["apron"], beard="full", beard_color="saltpepper", over_add=["dirt", "patches", "tired"]),
         "Out of the cellar: overgrown beard, dusty, no apron"),
        (stage("Gus Brannock"), "The Tankard reopens: apron, tankard raised"),
        (stage("Gus Brannock", upper=("vest", (236, 228, 210)), vest=(70, 104, 76), over_add=[("wristribbon", (200, 60, 60))]),
         "Hope: his good waistcoat, and Tilly's ribbon tied round his wrist"),
    ]),
    ("Tilly Brannock", "Tilly", [
        (stage("Tilly Brannock", **RESCUED, hat=(None,), hair="long", over_add=["tatters", "dirt", "tired"]),
         "Out of the Granary: rags, hair down, chafed wrists"),
        (stage("Tilly Brannock"), "Behind the bar again: bodice, ribbon, a tray of mugs"),
        (stage("Tilly Brannock", mouth="grin", over_add=[("flower", (170, 130, 220)), ("scarf", (110, 150, 120))]),
         "Hope: a strange flower from Linden in her hair (she kept it)"),
    ]),
    ("Capt. Percival Varr", "Percival", [
        (stage("Capt. Percival Varr", **RESCUED, hat=(None,), beard="stubble", hair="messy", over_drop=["medals", "sash", "sword"],
               over_add=["tatters", "dirt", "tired"]), "Rescued for real: the navy coat in rags, no medals, no hat"),
        (stage("Capt. Percival Varr", upper=("armor", (150, 150, 158)), tabard=(60, 80, 140), lower=("trousers", (70, 70, 80)), hat=(None,),
               over_drop=["medals", "sash"], pose=("down", "down"), prop="spear", mouth="flat", brows="normal"),
         "Purpose: a plain gate guard in the town tabard; apologises to everyone"),
        (stage("Capt. Percival Varr", upper=("armor", (150, 150, 158)), tabard=(60, 80, 140), lower=("trousers", (70, 70, 80)),
               hat=("helmet", (150, 150, 158)), over_drop=["medals", "sash"], pose=("down", "down"), prop="spear", mouth="smile",
               brows="normal", over_add=["tinmedal"]), "Hope: one medal, hammered from a tin lid by Pip. He wears it every day"),
    ]),
    ("Sabine Marsh", "Sabine", [
        (stage("Sabine Marsh", **RESCUED, over_drop=["pouches"], over_add=["tatters", "dirt", "tired"]),
         "Out of the crypt: weeks of dust; Parson never left her"),
        (stage("Sabine Marsh"), "Her craft again: herb pouches, grave-herbs, charms"),
        (stage("Sabine Marsh", mouth="smug", over_add=[("flower", (150, 110, 200)), "brooch"]),
         "Hope: still grim, but a strange flower in her hair and the ghost of a smile"),
    ]),
]
STAGES = [("Rescued", 0.42, 0.96), ("Purpose", 0.8, 1.0), ("Hope", 1.05, 1.03)]


def main():
    bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 16)
    head = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 18)
    reg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 26)
    cw, rh, lw = 300, 230, 130
    W, H = 30 + lw + 3 * cw + 20, 130 + len(SHOWN) * rh
    sheet = Image.new("RGBA", (W, H), (243, 234, 214, 255))
    d = ImageDraw.Draw(sheet)
    d.text((30, 20), "Townsfolk progression: Rescued → Purpose → Hope", font=title, fill=(58, 42, 26))
    d.text((30, 56), "Colour is a reward: rescued people are washed-out and ragged; purpose brings work clothes and tools;", font=reg, fill=(90, 74, 58))
    d.text((30, 72), "hope brings their own colours back and a personal touch, usually a gift from someone else in town.", font=reg, fill=(90, 74, 58))
    for k, (label, _, _) in enumerate(STAGES):
        d.text((30 + lw + k * cw, 96), label, font=head, fill=(42, 30, 20))
    for i, (name, short, rows) in enumerate(SHOWN):
        y = 120 + i * rh
        d.rounded_rectangle((24, y, W - 16, y + rh - 10), 10, fill=(236, 226, 206), outline=(196, 178, 146))
        d.text((36, y + 90), short, font=bold, fill=(42, 30, 20))
        for k, ((c, cap), (label, sat, warm)) in enumerate(zip(rows, STAGES)):
            im = saturate(town.character(c), sat, warm)
            x = 30 + lw + k * cw
            sheet.alpha_composite(im.resize((96, 192), Image.NEAREST), (x, y + 6))
            words, lines, cur = cap.split(), [], ""
            for w in words:
                t = (cur + " " + w).strip()
                if d.textlength(t, font=reg) <= cw - 116:
                    cur = t
                else:
                    lines.append(cur); cur = w
            lines.append(cur)
            for j, line in enumerate(lines[:7]):
                d.text((x + 104, y + 60 + j * 16), line, font=reg, fill=(70, 56, 44))
    sheet.save(OUT / "stages.png")


if __name__ == "__main__":
    main()

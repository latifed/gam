# Art plan (draft)

## 1. Style guide (to lock early)
| | Proposal |
|---|---|
| Tiles | **16×16 px** (Stardew scale). Graveyard Keeper's denser detail costs a lot more per asset. |
| Characters | **16×32 px**, 4 directions: idle, walk, tool use; fighters also get attack, dodge, hurt and death. |
| Enemies | Same scale, with **clear wind-up frames** (combat is harder, so attacks must be readable). |
| Portraits | 64×64 px for dialogue, 3–4 expressions. **Main cast only** at first (you, Mira, Pip, Wren, Oswin, Aldous, Percival, Winnie). |
| Palette | One **limited palette** (32–64 colours, e.g. from Lospec) for the whole game, so assets from different sources look like one game. |
| Mood | Warm, cozy colours in town; purple and wrong-feeling colours outside the walls; gold for Hope. |
| Lighting | Unity URP **2D lights**: day/night, lanterns, Pip's window, the Hope glow drifting down the roots. Lighting does a lot of the mood for cheap. |

## 2. Where the art comes from: in phases
1. **Prototype: placeholders and asset packs.** Squares, or ready-made packs. Good fits:
   - *Kenney* (kenney.nl): free CC0 packs such as Tiny Town / Tiny Dungeon. Fine for grey-boxing.
   - *Mana Seed* (Seliel the Shaper, itch.io): farming-RPG packs very close to the Stardew look, with a paper-doll character system; paid, commercial use allowed (check the licence of each pack).
   - Other cozy farming packs on itch.io. **Always check the licence** (some free packs are non-commercial only).
2. **Style target: commission a pixel artist** for one small, finished scene: the starting area, You + Mira + Pip, one Roots tunnel with a goblin. This sets the look everyone else follows and becomes the first screenshots.
3. **Production:** that artist (or 2–3 artists working from the style guide) makes the rest. Packs can stay for background props if they match the palette.
4. **Key art / Steam capsule:** commissioned separately (often a painted illustration, not pixel art). It's the single most important image for wishlists.

## 3. Options and honest trade-offs
| Route | Pros | Cons |
|---|---|---|
| Asset packs | Cheap, instant | Other games use them too; harder to look unique; may not cover strange-world things (metal vines, hope glow, the DM). |
| Hire pixel artist(s) | Unique, consistent, professional | The biggest cost of the project. A Stardew-scale game needs thousands of sprites and animation frames. Get quotes; rates vary hugely. |
| Draw it yourself (Aseprite) | Free, full control | Slow; ConcernedApe spent years on Stardew's art. Fine if you enjoy it. |
| AI-generated art | Fast concepts and mood boards | Pixel output is usually inconsistent (no clean pixel grid, drifting palette), needs heavy cleanup; **Steam requires disclosing AI-generated content**; cozy/indie players can react badly. Best kept to early concepts. |

**Recommendation:** packs for the prototype → commission a style-target scene once the prototype is fun → artist(s) for production, with key art commissioned separately.

## 4. Asset list for the Day 1 prototype / vertical slice
- **Tiles:** grass, dirt, path, purple strange grass, rubble, fences, town wall, Postern gate, the small Strange Garden (soil + blessed border), Old Graveyard (prologue), Roots tunnel (dirt walls, roots, metal vines).
- **Buildings:** your house and Mira's house (outside + inside), ruined buildings as backdrops.
- **Characters:** You (walk, hoe, water, carry, sword swing, dodge), Mira, Pip, Sprout, Wren (walk + fight), Oswin (in bed), Percival (prologue), the Dungeon Master (shadow/silhouette).
- **Enemies:** 2 goblin types, a root creature, wraith, zombie, skeleton.
- **Crops:** 2–3 normal + 2 strange crops, 4–5 growth stages each.
- **Items/icons:** ~40 (tools, seeds, crops, food, bandages, lantern...).
- **UI:** energy, Hope meter, health/stamina, inventory, dialogue box, 4–5 portraits.
- **Effects:** Hope glow, lantern light, hit flashes, dust, the green flash of the Shift.

# Adventure Capital — Design Notes (brainstorm v0.2)

> **Platform decision:** a premium (buy-once) **Steam** game, no Web3. The Robinhood Chain notes were dropped in v0.2.

> Status: brainstorm. Anything marked **[?]** is an open question to settle together.

## 1. Pitch

A dungeon has opened under the town of **Hollowmere**, and its Dungeon Master's
monsters spill out a little more every night. Everyone is panicking except **you**,
a wealthy resident having an ale at the *Gilded Tankard*. The innkeeper tells you how
bad things are. You smile and say: *"Sounds like a business opportunity."*

You don't fight. You **invest**: hire a warrior, buy him the basics, send him down,
and take your share of whatever he hauls back.

**Genre:** idle / incremental dungeon crawler with an active decision layer.
**Tone:** fantasy with a dry, capitalist sense of humour (the investor stays at the inn; the hero does the bleeding).
**Working title ideas:** *Adventure Capital*, *Dungeon Ventures Ltd.*, *Hired Steel*, *The Delve Dividend*.

## 2. Core loop

```
 INN (meta / hire / contracts)
   │
   ▼
 TOWN ── heal · eat · buy provisions, keys, stones · upgrade gear
   │                                    ▲
   ▼                                    │ walk out or teleport stone
 DUNGEON ── hero walks the tunnel, fights by himself (idle)
   │            you set the stance, react to events (active)
   ├── dies ──► ABBEY: resurrect (time, or gold, or premium)
   └── loot is only BANKED when the hero gets back to town alive
```

**The key tension:** loot the hero is carrying is at risk until he's back in town.
Push deeper for better loot, or go home now and keep what you've got?
That's the push-your-luck engine behind the "non-idle" part.

## 3. The hero in the dungeon

### 3.1 Stances
| Stance | Damage dealt | Damage taken | Descent speed | Loot multiplier | Notes |
|---|---|---|---|---|---|
| Defensive | low | very low | slow | ×0.8 | safe for AFK / offline |
| Normal | base | base | base | ×1.0 | default |
| Aggressive | high | high, **plus HP drain over time** | fast | ×1.5 + crit chance | will kill him if left on; needs retreat or a stance change |

- Aggressive is the way to farm fast, but **you** have to watch it.
- Ideas **[?]**: a *Berserk* stance unlocked later (huge damage, can't retreat), stance-specific skills.

### 3.2 Survival resources
- **HP**: heals in town (healer costs gold) or with potions in the dungeon.
- **Stamina / hunger**: drains as he walks. Provisions (rations, ale, jerky) refill it. At 0 his stats drop and HP regen stops.
- **Light (torches)** **[?]**: optional. Deeper tiers are dark and need torches/lanterns, or the hero is ambushed more often.
- **Keys**: open locked doors (shortcuts, side vaults) and chests.
- **Teleport stones**: instant exit to town with all carried loot. The only safe way out mid-run.

### 3.3 Leaving the dungeon
1. **Walk back**: free, but takes time and the return trip has encounters.
2. **Teleport stone**: instant, costs a stone (bought with gold; rare drops).
3. **Death**: carried loot is lost (all of it, or a percentage **[?]**), the hero goes to the Abbey.

### 3.4 Death and the Abbey
Resurrection options:
- **Wait**: free, long timer (scales with depth or hero level).
- **Donation**: gold, shorter timer.
- **Blessing**: premium currency, instant.
- Ideas: death leaves a **"corpse run"** marker so the next run can try to recover part of the lost loot. Repeated deaths cause a temporary *Shaken* debuff (morale).

### 3.5 Standing Orders (makes the idle part work)
Rules the hero follows when you're not watching:
- "If HP < 30%, switch to Defensive."
- "If HP < 15% and I have a teleport stone, use it."
- "Eat when stamina < 40%."
- "Return to town when bags are full."
Start with 1–2 rule slots; unlock more (the *Quartermaster* upgrade). Offline progress
runs on these rules. Good orders make idle play safe; manual play does better than them.

### 3.6 Active layer (why you check in)
- **Timed events** that fall back to Standing Orders if you're away:
  - Mysterious chest: open it (could be a mimic) or leave it?
  - Fork in the tunnel: shortcut (needs a key) or the long way?
  - Wounded stranger: help (costs a potion, chance of a recruit) or ignore?
  - Ambush: pick a stance for the fight.
- **Boss fights** with phases; switching stance at the right time makes a big difference.
- **Rally / Cheer** button on a cooldown (a messenger raven from the investor) for a short buff.
- Optional: tap to land crits / parry windows **[?]** (risky: can turn the game into a clicker).

## 4. Town

Each building is a shop and an upgrade track. Many start **closed** because of the
monster threat and reopen as you clear tiers, so the town visibly comes back to life.

| Building | Function |
|---|---|
| **Gilded Tankard (Inn)** | Story, hiring, contracts/bounties, innkeeper hints. Your HQ. |
| **Blacksmith** | Weapons; upgrade/reforge. |
| **Armorer** | Armor, shields. |
| **Apothecary / Healer** | Healing in town, potions, antidotes. |
| **Provisioner** | Food, ale, torches, rope. |
| **Locksmith** | Keys, lockpicks. |
| **Arcanist** | Teleport stones, enchantments, scrolls. |
| **Abbey** | Resurrection, blessings, curse removal. |
| **Counting House** | Your ledger: income, the hero's wages, investments, town bonds **[?]**. |
| **Guild Hall** (later) | Hire more adventurers and classes; run parties. |

### 4.1 Business layer (the "investor" fantasy)
- The hero takes a **cut** (wage % or a fixed fee per run). Pay him badly and his morale/loyalty drops.
- **Reinvest** profits into shops (discounts, better stock) and town defences.
- **Town Threat meter:** if no one pushes the dungeon, monsters raid the town (shops close, prices go up). Pushing deeper lowers the threat. A soft meta clock that gives the idle game some stakes.
- Later: a roster of several heroes on different floors, and hero classes (Rogue for traps/keys, Cleric for sustain, Mage for AoE).

## 5. The Dungeon: tiers and look

**View:** a 2D side-on tunnel. The hero walks left to right and enemies come in from the right.
Parallax layers (back wall, mid props, foreground beams/roots), HP bars, floating damage numbers.
Every tier changes the wall tileset, lighting, props, music and enemies.

| Tier | Name | Walls / look | Enemies | Boss (DM's lieutenant) |
|---|---|---|---|---|
| 1 | **Goblin Warrens** | dirt tunnels, roots, wooden supports, torches | puny goblins, giant rats, kobold slingers | *Gnashgut the Goblin Chief* |
| 2 | **Forgotten Crypts** | cut stone, cobwebs, sarcophagi, candles | skeletons, ghouls, crypt bats | *The Bone Warden* |
| 3 | **Fungal Depths** | wet rock, glowing mushrooms, spore haze | myconids, cave spiders, trolls | *Mother Mycelia* |
| 4 | **Drowned Mines** | flooded shafts, rusted rails, lanterns | drowned miners, eels, rust golems | *The Foreman* |
| 5 | **Obsidian Forge** | basalt, lava channels, chains | fire imps, salamanders, magma golems | *Forgemaster Kragg* |
| 6 | **Abyssal Cathedral** | bone-and-black-marble, red glow | demons, cultists, nightmares | *The High Inquisitor* |
| ∞ | **The Dungeon Master's Sanctum** | shifting, "game-board" walls | everything; the DM changes the rules | **The Dungeon Master** |

- **Structure:** each tier has ~10 floors; floor 5 is a mini-boss, floor 10 the tier boss. Beating a boss unlocks a **waystone checkpoint** you can teleport to (costs a stone).
- **Flavour idea:** the Dungeon Master is a showman who "narrates" and taunts your hero (and you, the investor) through the walls. Later he starts *adjusting the dungeon* in response to your strategy (more traps if you farm aggressively, etc.).
- After the finale: **prestige** (the DM "rebuilds the dungeon" deeper and harder; you keep some permanent bonuses).

## 6. Items and progression
- **Gear slots:** weapon, offhand, head, body, legs, boots, trinket ×2.
- **Rarity:** common / uncommon / rare / epic / legendary. Affixes like *+lifesteal*, *+loot find*, *aggressive stance drain −20%*.
- **Hero level and skills:** small passive tree (Endurance, Brutality, Survival, Greed).
- **Investor upgrades** (permanent, account-wide): bag capacity, Standing Order slots, shop discounts, offline-progress cap.

## 7. Currencies (Steam version)
| Currency | Source | Use |
|---|---|---|
| **Gold** | loot sold in town | everything day to day |
| **Abbey Favor** | boss kills, achievements, deep floors (earned only, not bought) | instant resurrect, rerolls, rare shop stock |
| **Renown** (prestige) | prestige resets | permanent investor upgrades |

The death cost is time, gold, or Favor the player has earned. **No real-money microtransactions**; if anything,
cosmetic DLC or an expansion tier later.

## 8. Steam: what changes
- **Business model:** premium, roughly $5–15 price range **[?]**. Demo / Next Fest build with Tier 1 to build wishlists.
- **Idle on desktop:** many Steam idlers (*Melvor Idle*, *Idle Champions*, *Nodebuster*, *Rusty's Retirement*) are played in a small window **or docked at the bottom/side of the screen** while you do something else. Idea: a **"tavern window" mode**, a thin always-on-top strip that shows just the tunnel and the HP bar. That suits a game where you watch a hero walk a horizontal tunnel very well.
- **Offline progress:** computed from timestamps on launch, capped (upgradeable). Single-player, local saves, so cheating doesn't matter much; no server needed.
- **Steam features:** achievements (boss kills, "never died in Tier 2", "won a fight on Aggressive with 1 HP"), Cloud saves, Steam Deck verified (the menus need to work with a controller), trading cards later.
- **Leaderboards [?]:** "deepest floor this week", "most gold banked in one run". A weekly **"Dungeon Master's Challenge"** with a fixed seed and modifiers is good for replay value and streams.
- **Hero memorial / "service record":** what the NFT idea did, but just as fun: a wall in the inn for retired and fallen heroes with their stats and how they died.

## 9. Tech sketch (proposal)
- **Engine options:**
  - **Godot 4**: free, great at 2D, exports to Windows/Linux/macOS/Steam Deck, has GodotSteam for Steam integration. **Recommended.**
  - Unity: fine, but heavier for a 2D idle game.
  - Web stack (TypeScript + Phaser/PixiJS) packaged with Electron/Tauri: fast to prototype and fine for idlers, but larger builds and more work on the Steam integration.
- **Deterministic combat sim** (seeded RNG, fixed tick) kept separate from rendering. The same code runs live, in fast-forward for offline progress, and in balance-testing scripts.
- **Data-driven content:** enemies, items, tiers and events in JSON/resources so balancing doesn't need code changes.
- **Art:** pixel art, ~16–32 px characters, one tileset and enemy pack per tier. Start with placeholders.

## 10. MVP / vertical slice (proposal)
1. Town with Inn, Healer, Provisioner, Blacksmith, Abbey (simple menus).
2. One hero, warrior class, 3 stances, HP/stamina, teleport stones, death and resurrection.
3. **Tier 1 only** (Goblin Warrens, 10 floors, Gnashgut boss), side-scrolling tunnel scene.
4. 2 Standing Order slots, offline progress.
5. 3–4 timed events.
6. Save/load. No Steam integration yet; that comes with the demo build.

## 11. Open questions for us
1. Engine: Godot (recommended), Unity, or a web stack wrapped for Steam?
2. Window: a normal window plus a docked "tavern strip" mode, or only one of them?
3. One hero at the start, or a roster early on? When do other classes unlock?
4. On death, lose all carried loot or a percentage?
5. Art direction: pixel art (which resolution?) or hand-drawn 2D?
6. How "active" should it be: decisions only, or also timing/parry mechanics?
7. Run length: how long is a typical dive? (proposal: 5–15 min active, hours on Standing Orders)
8. Is the Dungeon Master a talking character with lots of dialogue, or mostly in the background?
9. Does the town's Threat meter ever actually punish you (raids that close shops), or is it only flavour?
10. Names: the town, the inn, the starting warrior, the game.

## 12. Competitors and references

| Game | Closest overlap | What to learn / how we differ |
|---|---|---|
| **Soda Dungeon 1 & 2** | **Closest match.** A tavern recruits adventurers, the party auto-fights through a side-scrolling dungeon, you decide when to go home. | Proves the concept. It's a party of throwaway recruits and lighter on decisions; we invest in **one hero**, with stances, Standing Orders and the investor fantasy. |
| **Moonlighter** | You keep loot only if you get out; you pay to teleport out (the pendant); run the shop in town. | Same loot-at-risk loop and teleport-stone idea. It's an action game, not idle. |
| **Loop Hero** | Hero runs a route by himself; retreating early keeps more resources than dying. | Their split (keep everything at camp, 60% on retreat, 30% on death) is a good reference for our death-loss rule. |
| **Darkest Dungeon** | Hire heroes in town, push your luck or retreat, upgrade the hamlet, a narrator who comments on everything. | The narrator is a model for the Dungeon Master's voice. Not idle; we're lighter and funnier. |
| **Melvor Idle** | Buy-once Steam idle game; combat with food, auto-eat, gear progression. | Steam idle players accept deep systems and spreadsheets. Its auto-eat upgrade is a simple version of our Standing Orders. |
| **Idle Slayer** | Side-scrolling hero, idle with active bursts. | Very close to the look we want; the active part there is reflexes, ours is decisions. |
| **Idle Champions of the Forgotten Realms** | Idle fantasy party, the biggest name in the genre on Steam. | Free-to-play with heavy monetisation; we're buy-once, single hero, story-driven. |
| **Rusty's Retirement** (+ desktop pets like Bongo Cat) | Docked idle game in a strip of your desktop. | Shows the "tavern strip" docked-window mode can sell. |
| **Shop Titans / Recettear** | You profit from adventurers as a shopkeeper. | Similar "businessman, not hero" fantasy. |

**Our edge (draft):** a single hero you're invested in; three stances plus loot that's at risk until he's home (push your luck); Standing Orders as a light way to program the hero; a dockable tunnel window; a town that comes back to life; investor humour and a talking Dungeon Master.

## 13. Inspirations and the cozy direction (v0.3)

Reference games the player loves: **Majesty**, **Dungeon Siege**, **Stardew Valley**, **Graveyard Keeper**.

### 13.1 From Majesty: indirect control and gold that flows back to you
- In Majesty you never command heroes. You place **bounty flags** and they decide for themselves, depending on personality and greed.
- Heroes **spend their pay in your town's shops**, so you earn it back. That's exactly the investor fantasy: hire, equip, take a cut, and then sell the hero his own potions.
- Ideas:
  - **Bounty board** at the inn ("100g for Gnashgut's head", "50g per goblin ear").
  - **Hero personality** (brave, greedy, cautious, drunk) decides how well he follows your stance and Standing Orders. A greedy hero ignores retreat orders when there's a chest nearby.
  - Later, a **roster** of heroes with Majesty-style classes who choose their own bounties.

### 13.2 From Dungeon Siege: fun to just watch
- The fun is **watching** them fight: readable combat, visible gear on the character, satisfying hits, loot popping out.
- **Pack mule**: a donkey that follows the hero and carries the loot. Bag capacity is literally the mule. Upgrade or name the mule; if the mule dies or panics, the loot is dropped. The mule could walk loot back to town by itself (an alternative to teleport stones).
- Every new item you buy **shows on the hero's sprite**.
- The world feels continuous: the tunnel goes deeper without loading screens and the walls change as you descend.

### 13.3 From Stardew / Graveyard Keeper: the cozy "non-idle" loop
**Big idea:** the active part of the game is **your own life in town** while the hero idles in the dungeon. You actually walk around Hollowmere as the investor.

- **Your stuff:** a house or a run-down manor you restore, and a **brewery / kitchen / garden** where you make the provisions and ale the hero eats (cheaper and better than buying them).
- **Townsfolk with relationships:** the innkeeper, the blacksmith, the abbess, the locksmith's apprentice. Gifts and favours unlock discounts, recipes and side quests. Heart events.
- **Day/night cycle:** the hero works in the dungeon while you work in town. At **night** monsters get bolder (more Threat in town, better loot down below).
- **Graveyard Keeper's dark humour** fits the cynical-investor tone perfectly: you profit from a disaster, and the Abbey charges for resurrections.
- **Seasons / festivals:** a Harvest Fair, the "Day of the Fallen Heroes", a festival when you beat a dungeon boss. The town decorates as it recovers.
- **Restoring the town** = Stardew's community center: shops reopen (blacksmith, arcanist, guild hall) as you clear tiers and invest.
- **Fixed-camera window**: you can always see the hero in the dungeon in a frame (a picture-in-picture "tavern scrying glass"), so you watch him while you farm.

### 13.4 What this changes
- The game moves from "idle with menus" to a **cozy town sim plus idle dungeon**. It's more original and fits the Steam cozy audience (which is large), but it's **much bigger to build**.
- How do we keep the idle part meaningful? Proposal: in-game days are short (~10–15 real minutes), and the hero's progress and your town progress feed each other (his loot → your crafting materials; your food/ale → his buffs).
- Offline: the hero keeps working on Standing Orders, but the town (your crops, your brewery) doesn't progress, or only partly.

### 13.5 Open questions (cozy direction)
1. Does the player walk around town in top-down Stardew style while the dungeon is shown side-on in a window? Or is the whole thing side-on?
2. How much farming/crafting do we want: a small garden + brewery, or a full Stardew-size crafting system?
3. One hero you're attached to (Dungeon Siege), or many heroes acting on their own (Majesty)? Or one hero at first and the Majesty system later?
4. Real-time idle (progress while the game is closed) vs. in-game days (like Stardew)? Both together is possible but needs careful design.

## 14. Story draft (v0.4)

### 14.1 One-line premise
*One night the whole town of Hollowmere is pulled into a strange, hostile world. You lead everyone into the nearby dungeon to end the threat quickly, get ambushed, and come home to ruins. Now you rebuild, slowly and properly.*

### 14.2 Prologue (playable intro, ~10 minutes)

**Beat 1: An ordinary evening.**
Harvest Fair night in Hollowmere. You're the town's richest and proudest resident, enjoying an ale at the *Gilded Tankard*. Short tutorial: walk around, talk to a few townsfolk (the innkeeper, the blacksmith, the abbess, a kid). Just enough that you'll miss them later.

**Beat 2: The Shift.**
A green flash and a deep hum. In the morning the fields end in purple grass, the sky has the wrong colour, and the forest whispers.
> **Innkeeper:** "The road's gone. The *river's* gone. Where in the Nine Hells are we?"

**Beat 3: The hole.**
Scouts find a huge cave mouth an hour's walk away. At night things crawl out of it and scratch at the fences.
> **Innkeeper:** "Every night there's more of them. We won't last a month."
> **You** *(smiling)*: "Then we don't wait a month. We go in, we end it, and we're home by supper."

**Beat 4: The expedition.**
You gather everyone who can hold a pitchfork. A short, easy fight with goblins at the entrance makes the player feel strong.

**Beat 5: The ambush.**
The tunnel goes dark. A huge, amused voice:
> **Dungeon Master:** "Baa-aaa. Look at the little shepherd, taking his whole flock for a walk... and leaving the gate wide open."

Monsters pour in from all sides. People get hurt and scattered; some are dragged into the dark. You barely escape with a few others.

**Beat 6: Ruins.**
Back home, the town is smoking. Doors are broken in, the fields are trampled, the Tankard's sign hangs from one nail. The innkeeper sits on the steps.
> **Innkeeper:** "They came while we were gone. Every last one of us was gone."
> **You:** "...Then we start again. Properly this time."

**Gameplay begins:** a tent, a campfire, one plot of strange soil, and a list of missing names.

### 14.3 The acts (main story)
| Act | Name | What happens | New mechanics |
|---|---|---|---|
| 1 | **Ashes** | Clear the rubble, find survivors hiding in town and nearby, plant the first crops (normal + strange), patch the fence. | Farming, building, research, survivors as workers |
| 2 | **Supply Runs** | Send survivors out into the hostile world. Discover the **ruins of other towns** the Dungeon Master pulled here before you. | Expeditions (idle), map, new materials and recipes |
| 3 | **The Strike** | Send your best fighters to kill the Dungeon Master. **They fail**, but come back with a key piece of knowledge: the dungeon can only be taken **section by section**, and it's weakest **at night**. | Idle dungeon runs with stances, heroes, Abbey |
| 4 | **Night Shift** | You find the **Sleepless Elixir**. Day: run the town. Night: go to the dungeon with your party. Each section you clear, you **wall off and claim** (mushroom farm in the Fungal Depths, a forge in the Obsidian Forge...). | Day/night split, claiming dungeon sections |
| 5 | **The Seal** | Reach the Sanctum, face the Dungeon Master, seal the dungeon for good. | Finale |

### 14.4 Story ideas to keep
- **Most missing villagers are taken, not dead.** Finding them in the dungeon and in the wilds (and the reunion scenes) is a big emotional reward, and much cozier than permanent deaths.
- **Other lost towns:** you are not the first town the Dungeon Master pulled here. Their ruins hold recipes, diaries, tools, and maybe survivors. Mystery: why does he collect towns?
- **The player's arc:** from proud and reckless to a real leader. Keep some vanity for humour; the survivors tease you about the "supper" line.
- **The Sleepless Elixir** should have a light, funny side effect (you start hearing the Dungeon Master's commentary at night, plants grow toward you...).
- **Ending:** the dungeon sealed, and Hollowmere stays in the strange world, because it is home now. Possible secret ending: the way back home opens and you choose.

### 14.5 Keeping it cozy
- Darkness lives in the **story and in the dungeon**; the **town is safe**. Once the walls are up, home is never destroyed again.
- **No permanent loss in normal play:** heroes are resurrected, missing villagers are found, raids at worst damage walls (never crops or homes).
- The prologue does the heavy lifting, then the tone shifts to rebuilding, humour, and small wins.
- References for "dark story, cozy play": *Graveyard Keeper*, *Dredge*, *Spiritfarer*, *Cult of the Lamb*.

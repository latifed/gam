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

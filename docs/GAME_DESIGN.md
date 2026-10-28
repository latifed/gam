# Adventure Capital — Design Notes (brainstorm v0.1)

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

## 7. Currencies (draft)
| Currency | Source | Use | On-chain? |
|---|---|---|---|
| **Gold** | loot sold in town | everyday purchases | No (off-chain, keeps the economy tunable) |
| **Premium** (e.g. "Abbey Favor" / "Writs") | purchase, rare drops, achievements | instant resurrect, speedups, cosmetics | **[?]** |
| **Relics / rare gear** | boss and deep-floor drops | tradeable top-tier items | Candidate for NFTs |

Principle: **premium buys time and convenience, not power.** Avoid pay-to-win.

## 8. Web3 on Robinhood Chain: notes
- **Robinhood Chain** is an EVM-compatible L2 (built on Arbitrum), so standard Solidity, ERC-721/1155/20, and Ethereum tooling (Foundry/Hardhat, viem/wagmi) should work. **To check:** the current network status (testnet vs mainnet), RPC/chain ID, faucet, bridge, and what Robinhood lets games deploy.
- **Recommended architecture: hybrid.**
  - Game simulation (combat ticks, idle progress) runs **off-chain**, server-authoritative. Putting every tick on-chain is too slow and too expensive, and gives no benefit.
  - **On-chain:** ownership and things worth keeping:
    - **Hero NFT** (ERC-721): your hired adventurer, with level/class/history; a "service record" of tiers cleared.
    - **Relic gear** (ERC-1155): only rare+ items, minted when banked in town (not while carried, which fits the "only banked loot is safe" rule nicely).
    - **Premium currency**: either an off-chain balance bought with crypto, or a token **[?]**.
    - **Boss-kill / tier-clear achievements** as soulbound badges.
  - Server signs results (EIP-712 vouchers); the player claims/mints when they want. Gas sponsorship plus embedded/smart wallets so non-crypto players can start without a wallet popup.
- **Risks to keep in mind:**
  - A tradeable fungible token adds speculation, economy-balance and legal risk. Consider **no fungible token at launch**; start with NFTs for heroes/relics only.
  - Loot boxes or paid randomness with tradeable outputs can look like gambling in some jurisdictions. Keep paid items deterministic.
  - Bots in an idle game with tradeable items: server-authoritative sim, rate limits.
- **Theme fit:** you're literally a capitalist investing in adventurers. Possible gags: a dungeon "stock ticker" on the inn wall, quarterly reports from your hero, "dividends" from shops you invest in.

## 9. Tech sketch (proposal)
- **Client:** TypeScript + **Phaser 3** (or PixiJS) for the 2D tunnel scene; React (or plain DOM) for town/menus/ledger.
- **Server:** Node/TypeScript; a deterministic combat sim (seeded RNG) shared between client and server so the client can preview and the server can verify; offline progress computed from timestamps and Standing Orders.
- **Data:** Postgres (players, inventory, runs).
- **Chain:** Solidity contracts (Hero721, Relic1155, claim vouchers) with Foundry; wagmi/viem on the client.
- **Art:** pixel art, ~16–32 px characters. One tileset and enemy pack per tier. Start with placeholders.

## 10. MVP scope (proposal)
1. Town with Inn, Healer, Provisioner, Blacksmith, Abbey (simple menus).
2. One hero, warrior class, 3 stances, HP/stamina, teleport stones, death and resurrection.
3. **Tier 1 only** (Goblin Warrens, 10 floors, Gnashgut boss), side-scrolling tunnel scene.
4. 2 Standing Order slots, offline progress.
5. 3–4 timed events.
6. Web3 stubbed: wallet login and a Hero NFT mint on Robinhood Chain testnet. Everything else off-chain.

## 11. Open questions for us
1. Platform: browser-only, or mobile too (PWA)? Portrait or landscape?
2. One hero per player at the start, or a roster early on?
3. On death, lose all carried loot or a percentage?
4. Premium currency: off-chain only, or a token? Should we have a fungible token at all?
5. Which items, if any, are tradeable NFTs?
6. Art direction: pixel art (which resolution?) or hand-drawn 2D?
7. How "active" should it be: decisions only, or also timing/tap mechanics?
8. Session length target: check in every 5 minutes, every hour, or a few times a day?
9. Is the Dungeon Master a recurring character with dialogue (lots of writing) or mostly in the background?
10. Name of the town, the inn, the hero, and the game.

<div align="center">

# ⚔️ Dungeon Crawler

**A terminal RPG written in pure Python.**

Create a hero, pick a class, and battle your way through dungeons full of
monsters — gain experience, level up, collect loot, and defeat the Ancient Dragon.

[![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-none-success)](#%EF%B8%8F-tech)
[![Platform](https://img.shields.io/badge/platform-terminal-informational)](#-how-to-play)
[![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-red)](LICENSE)
[![Languages](https://img.shields.io/badge/languages-PT%20%C2%B7%20EN%20%C2%B7%20ES-blue)](#-languages)
![Status](https://img.shields.io/badge/version-v5-blueviolet)

<br>

<img src="assets/gameplay.gif" alt="Dungeon Crawler gameplay" width="560">

</div>

---

## 📖 Story

For a thousand years the kingdom of **Eldoria** thrived in the glow of the
**Heart of the World** — a buried ember of creation, guarded in the deep by the
Ancient Dragon **Varkhal**. While the dragon slept, the realm knew no winter it
could not survive and no wound it could not heal.

Then the Heart began to dim. Its fading light cracked the seal of Varkhal's lair,
and the guardian woke as a tyrant. From that fracture poured the **Blight**: rats
swelled into monsters in the caves, the forests rotted into shadow, the dead
clawed up from ancient ruins, venom-spiders nested in the dark, and a fallen
sorcerer crowned himself king of storms upon the **Thunder Mountain**. One by one
the regions fell silent — until only a single name remained on the muster roll.

Yours.

From the **Cave of Rats** to the **Forgotten Fortress**, you carve a path through
everything the Blight has unleashed, growing stronger with every kill. You keep a
**codex** of the horrors you meet, swear **oaths** before each region for glory and
gold, and chase the deeds that the bards will one day sing. At the end of the road
waits the **Dragon's Den** — and Varkhal himself.

But here is the cruel truth: slaying the dragon does **not** mend the Heart. With
its guardian gone, the fracture yawns wider, and the Blight pours out **without
end** — wave after wave, forever hungrier. There is no winning that tide. There is
only how long you stand, and how loud your legend echoes before the dark takes you.

> ⚔️ **Carve your saga.** Fill the **bestiary**, claim the **achievements**, master
> every **trial** — then step into the **endless** and see how far the last hero of
> Eldoria can go.

*The dungeon is deep. Your blade is sharp. The Heart is dying. Make it count.* 🐉

---

## 🎮 How to play

You only need **Python 3** — no installs, no dependencies.

```bash
python3 main.py
```

From the main menu you can start a **new game**, **continue** a saved run, or
check the **leaderboard**. Pick a name, a class, and a difficulty — then dive in.

---

## 🧙 Classes

| Class | Role | Abilities |
|------|------|-----------|
| 🛡️ **Warrior** | Tanky bruiser | Golpe Poderoso · Investida *(stun)* |
| 🔮 **Mage** | Glass cannon | Bola de Fogo · Raio Congelante *(stun)* |
| 🏹 **Archer** | Balanced ranged | Tiro Certeiro · Chuva de Flechas |
| ✨ **Paladin** | Sturdy healer | Luz Curativa · Martelo Sagrado *(stun)* |
| 🗡️ **Rogue** | Crit & poison | Golpe Sombrio *(poison)* · Apunhalar |

---

## ✨ Features

| System | What it does |
|--------|--------------|
| ⚔️ **Turn-based combat** | Attack, special abilities, defend, flee or use potions |
| 🎯 **Hit & crit rolls** | Attacks can miss or land critical hits |
| ☠️ **Status effects** | Poison (damage over time) and stun (skip a turn) |
| 📈 **Leveling** | Earn XP and gold, grow stronger every level |
| 🎒 **Inventory & gear** | Equip weapons and armor; manage your bag |
| 🪄 **Enchantments** | Gear with extra effects: +crit, +accuracy, poison-on-hit, regen |
| 🏪 **Shop** | Spend gold between stages — buy and sell items |
| 🎲 **Random events** | Chests, traps, fountains and a mysterious merchant |
| 🌋 **8 stages + boss** | Increasing difficulty up to the Ancient Dragon |
| ⚙️ **Difficulty** | Easy / Normal / Hard scale enemies and rewards |
| 💾 **Save & load** | Progress is autosaved after each stage |
| 🏆 **Leaderboard** | Best runs are ranked and saved between sessions |
| 🌍 **Languages** | Play in Portuguese, English or Spanish |
| 📖 **Bestiary** | A codex that fills in as you discover each monster |
| 🏅 **Achievements** | Unlockable goals saved across runs |
| 🎯 **Objectives** | Optional per-stage challenges for bonus gold |
| ♾️ **Endless mode** | Procedural waves after victory, chasing a high score |

---

## 🌍 Languages

The game is fully localized — menus, combat, item/monster/class names and all
messages. Pick your language on the **start screen** or switch any time from the
**main menu**; your choice is saved with your progress.

- 🇧🇷 **Português**
- 🇬🇧 **English**
- 🇪🇸 **Español**

---

## 📁 Project structure

```
main.py            # game entry point
game/
  ui.py            # terminal utilities (colors, screens, input)
  character.py     # base character class
  classes.py       # playable classes and abilities
  monster.py       # monsters and boss
  items.py         # items, potions, equipment and enchantments
  inventory.py     # inventory
  combat.py        # turn-based combat
  stages.py        # game stages
  difficulty.py    # difficulty levels and enemy scaling
  shop.py          # shop (buy / sell items)
  events.py        # random events between stages
  saves.py         # save / load progress
  scores.py        # high score leaderboard
  i18n.py          # translations (PT / EN / ES)
  bestiary.py      # monster codex
  achievements.py  # unlockable achievements
  quests.py        # optional stage objectives
  endless.py       # endless mode wave generator
```

---

## 🛠️ Tech

- **Pure Python 3** — standard library only, zero external dependencies.
- Runs anywhere a terminal does (macOS, Linux, Windows).

---

## 📜 License

**All Rights Reserved** — see [LICENSE](LICENSE). You may read the source code
for personal learning, but assets and content may not be reused, redistributed
or commercialized without written permission.

<div align="center">

*Made for fun. Grab a sword and good luck in the dungeon!* 🐉

</div>

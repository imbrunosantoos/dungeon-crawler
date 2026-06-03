<div align="center">

# ⚔️ Dungeon Crawler

**A terminal RPG written in pure Python.**

Create a hero, pick a class, and battle your way through dungeons full of
monsters — gain experience, level up, collect loot, and defeat the Ancient Dragon.

[![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-none-success)](#%EF%B8%8F-tech)
[![Platform](https://img.shields.io/badge/platform-terminal-informational)](#-how-to-play)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
![Status](https://img.shields.io/badge/version-v4-blueviolet)

</div>

---

## 🎮 How to play

You only need **Python 3** — no installs, no dependencies.

```bash
python3 main.py
```

From the main menu you can start a **new game**, **continue** a saved run, or
check the **leaderboard**. Pick a name, a class, and a difficulty — then dive in.

---

## 📸 Preview

**Main menu**

```text
===================
= DUNGEON CRAWLER =
===================

Um RPG de terminal

  [1] Novo jogo
  [2] Ver recordes
  [3] Sair
>
```

**Choose your class**

```text
Escolha sua classe:
  [1] Guerreiro — Vida 120, Ataque 18, Defesa 8  | Habilidades: Golpe Poderoso, Investida
  [2] Mago      — Vida 80,  Ataque 24, Defesa 4  | Habilidades: Bola de Fogo, Raio Congelante
  [3] Arqueiro  — Vida 100, Ataque 20, Defesa 6  | Habilidades: Tiro Certeiro, Chuva de Flechas
  [4] Paladino  — Vida 130, Ataque 16, Defesa 10 | Habilidades: Luz Curativa, Martelo Sagrado
  [5] Ladino    — Vida 95,  Ataque 21, Defesa 5  | Habilidades: Golpe Sombrio, Apunhalar
>
```

**Battle!**

```text
--------------------------------------------------
Aragorn (Nível 1)
  Vida:    [####################] 120/120
  Energia: 20/20
  Ataque: 18   Defesa: 8
  XP:     0/100   Ouro: 0

Rato Gigante  [#########-----------] 14/30
--------------------------------------------------
O que você faz?
  [1] Atacar
  [2] Habilidades especiais
  [3] Defender (reduz o próximo dano)
  [4] Fugir
  [5] Usar poção (2 disponível(is))
> 1

★ CRÍTICO! Você causa 34 de dano!

✔ Você derrotou Rato Gigante!
  + 30 XP
  + 10 de ouro
```

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
```

---

## 🛠️ Tech

- **Pure Python 3** — standard library only, zero external dependencies.
- Runs anywhere a terminal does (macOS, Linux, Windows).

---

## 📜 License

Released under the [MIT License](LICENSE) — free to use, modify and share.

<div align="center">

*Made for fun. Grab a sword and good luck in the dungeon!* 🐉

</div>

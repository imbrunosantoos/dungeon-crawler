# Dungeon Crawler ⚔️

A terminal RPG written in Python. Create a hero, pick a class, fight monsters
across increasingly difficult stages, gain experience, level up, collect items
and equipment — and defeat the final boss.

## How to run

You need Python 3 installed. Then, inside the project folder:

```bash
python3 main.py
```

## Features

### Core (v1)

- [x] Character with health, attack, defense, XP and level
- [x] Playable classes: Warrior, Mage and Archer
- [x] Monsters and a final boss
- [x] Turn-based combat
- [x] Rewards and level progression
- [x] Items, potions, inventory and equipment
- [x] Stages with increasing difficulty
- [x] Main menu, game loop and save/load progress

### v2

- [x] Difficulty levels (Easy / Normal / Hard) that scale enemies and gold
- [x] Shop between stages to buy and sell items with your gold
- [x] Random events while exploring (chest, trap, fountain, mysterious merchant)

### v3

- [x] Richer combat: hit chance (misses) and critical hits on normal attacks
- [x] Status effects: poison (damage over time) and stun (skip a turn)
- [x] Two new playable classes: Paladin (self-heal) and Rogue (crit + poison)
- [x] More monsters (some inflict status effects) and new stages/regions
- [x] High score leaderboard saved between runs, viewable from the main menu

## Code structure

```
main.py          # game entry point
game/            # game modules
  ui.py          # terminal utilities (colors, screens, input)
  character.py   # base character class
  classes.py     # playable classes
  monster.py     # monsters and boss
  items.py       # items, potions and equipment
  inventory.py   # inventory
  combat.py      # combat system
  stages.py      # game stages
  saves.py       # save / load progress
  difficulty.py  # difficulty levels and enemy scaling
  shop.py        # shop (buy / sell items)
  events.py      # random events between stages
  scores.py      # high score leaderboard
```

## Tech

- Pure Python 3 — no external dependencies (standard library only).

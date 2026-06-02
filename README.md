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

- [x] Project structure and terminal utilities
- [x] Character with health, attack, defense, XP and level
- [x] Playable classes: Warrior, Mage and Archer
- [x] Monsters and a boss
- [x] Turn-based combat
- [x] Rewards and level progression
- [x] Items and potions
- [x] Inventory and equipment
- [ ] Stages with increasing difficulty
- [ ] Main menu and game loop
- [ ] Save and load progress

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
```

## Tech

- Pure Python 3 — no external dependencies (standard library only).

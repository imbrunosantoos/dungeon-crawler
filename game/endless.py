"""Endless mode: procedurally scaled waves after beating the game."""

import random

from game.difficulty import aplicar_dificuldade
from game.monster import MODELOS_MONSTROS, criar_boss, criar_monstro


def gerar_inimigos(onda, dificuldade):
    """Build a wave's enemies: random monsters scaled up by the wave number,
    plus a boss every 5th wave."""
    quantidade = min(4, 2 + onda // 3)
    ids = list(MODELOS_MONSTROS.keys())
    inimigos = [criar_monstro(random.choice(ids)) for _ in range(quantidade)]
    if onda % 5 == 0:
        inimigos.append(criar_boss())

    # Difficulty multipliers first, then a wave factor that keeps growing.
    fator = 1 + 0.12 * onda
    for inim in inimigos:
        aplicar_dificuldade(inim, dificuldade)
        inim.hp_max = max(1, int(inim.hp_max * fator))
        inim.hp = inim.hp_max
        inim.ataque = max(1, int(inim.ataque * fator))
        # Scale rewards too, so the hero keeps progressing.
        inim.xp_recompensa = int(inim.xp_recompensa * fator)
        inim.ouro_recompensa = int(inim.ouro_recompensa * fator)
    return inimigos
